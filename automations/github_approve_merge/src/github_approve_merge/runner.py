from __future__ import annotations

import json
import logging
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from github_approve_merge.actions import (
    EXIT_CODE_FAILURE,
    EXIT_CODE_INTERRUPTED,
    EXIT_CODE_SUCCESS,
    STATUS_TO_EXIT_CLASS,
    ExitClass,
    MergeDecision,
    ProcessResult,
    execute_decision,
    plan_pr,
)
from github_approve_merge.gh_client import GhAuthError, GhNotFound
from github_approve_merge.logging_setup import RunContext
from github_approve_merge.url import PRRef

_log = logging.getLogger("gam")

# client_factory(pr, me) -> a PrClient-shaped adapter.
ClientFactory = Callable[[PRRef, str], object]
# gate(decisions) -> parallel list of bools (proceed?).
Gate = Callable[[list[MergeDecision]], list[bool]]


async def run_batch(
    prs: list[PRRef],
    *,
    client_factory: ClientFactory,
    me: str,
    approve: bool,
    do_merge: bool,
    method: str,
    gate: Gate,
    logs_dir: Path,
    run_id: str,
    dry_run: bool = False,
    resume: bool = False,
    ctx: RunContext | None = None,
) -> dict:
    """Two-pass batch: (1) classify+approve each PR collecting MergeDecisions, (2) gate ALL
    decisions once, (3) execute the gated ones. Writes state.jsonl per transition and
    summary.json; returns the summary dict. See spec §7."""
    run_dir = logs_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    ctx = ctx or RunContext(run_id=run_id, run_dir=run_dir)
    state_path = run_dir / "state.jsonl"
    started = _utcnow_iso()

    completed = _load_completed_for_resume(state_path) if resume else set()
    pending = [pr for pr in prs if ctx.pr_token(pr) not in completed]

    # Queue everything up front so a SIGINT before work still leaves a record.
    for pr in pending:
        _append_state(state_path, ctx, pr, "queued")

    results: list[tuple[PRRef, ProcessResult]] = []
    decisions: list[tuple[PRRef, object, MergeDecision]] = []
    started_at: dict[str, float] = {}
    interrupted = False

    # --- Pass 1: plan (classify + approve) ---------------------------------
    for pr in pending:
        token = ctx.pr_token(pr)
        _append_state(state_path, ctx, pr, "in_progress")
        started_at[token] = time.monotonic()
        client = client_factory(pr, me)
        try:
            outcome = plan_pr(client, pr, approve=approve, do_merge=do_merge, dry_run=dry_run)
        except (KeyboardInterrupt, SystemExit):
            _record(results, state_path, ctx, pr, ProcessResult("failed-interrupted"))
            interrupted = True
            break
        except GhAuthError as e:
            _record(results, state_path, ctx, pr, _finish("failed-auth", started_at[token], repr(e)))
            continue
        except GhNotFound as e:
            _record(results, state_path, ctx, pr, _finish("failed-not-found", started_at[token], repr(e)))
            continue
        except Exception as e:  # broad: batch must continue
            _log.error("plan_pr failed", exc_info=True, extra={"pr": token})
            _record(results, state_path, ctx, pr, _finish("failed-exception", started_at[token], repr(e)))
            continue

        if isinstance(outcome, MergeDecision):
            decisions.append((pr, client, outcome))
        else:
            _record(results, state_path, ctx, pr, _finish(outcome, started_at[token]))

    # --- Gate: confirm ALL merges at once ----------------------------------
    if decisions and not dry_run and not interrupted:
        proceed = gate([d for _pr, _c, d in decisions])
    else:
        proceed = [False] * len(decisions)

    # --- Pass 2: execute the gated merges ----------------------------------
    if not interrupted:
        for (pr, client, decision), ok in zip(decisions, proceed):
            token = ctx.pr_token(pr)
            if not ok:
                _record(results, state_path, ctx, pr, _finish("cancelled", started_at[token]))
                continue
            try:
                status = execute_decision(client, decision, method)
            except GhAuthError as e:
                status_result = _finish("failed-auth", started_at[token], repr(e))
            except GhNotFound as e:
                status_result = _finish("failed-not-found", started_at[token], repr(e))
            except Exception as e:  # broad: batch must continue
                _log.error("execute_decision failed", exc_info=True, extra={"pr": token})
                status_result = _finish("failed-exception", started_at[token], repr(e))
            else:
                status_result = _finish(status, started_at[token])
            _record(results, state_path, ctx, pr, status_result)

    exit_code = _compute_exit_code(results, interrupted)
    summary = _build_summary(ctx, run_id, started, results, exit_code)
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    _print_summary(run_id, results, exit_code)
    return summary


# --- helpers ---------------------------------------------------------------

def _finish(status: str, start_monotonic: float, error_message: str = "") -> ProcessResult:
    return ProcessResult(status=status, error_message=error_message,
                         duration_ms=int((time.monotonic() - start_monotonic) * 1000))


def _record(results, state_path, ctx, pr, result: ProcessResult) -> None:
    _append_state(state_path, ctx, pr, result.status,
                  duration_ms=result.duration_ms, error_message=result.error_message)
    results.append((pr, result))


def _append_state(state_path: Path, ctx: RunContext, pr: PRRef, status: str, *,
                  duration_ms: int = 0, error_message: str = "") -> None:
    record: dict[str, object] = {"ts": _utcnow_iso(), "pr": ctx.pr_token(pr), "status": status}
    if duration_ms:
        record["duration_ms"] = duration_ms
    if error_message:
        record["error"] = error_message
    with state_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def _load_completed_for_resume(state_path: Path) -> set[str]:
    """Return PRs whose latest status is terminal + success-class (skip on resume)."""
    if not state_path.exists():
        return set()
    latest: dict[str, str] = {}
    for line in state_path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue  # tolerate partial last line from SIGINT
        if "pr" in rec and "status" in rec:
            latest[rec["pr"]] = rec["status"]
    done: set[str] = set()
    for pr, status in latest.items():
        cls = STATUS_TO_EXIT_CLASS.get(status)
        if status == "done" or status.startswith("skipped-") or cls is ExitClass.SUCCESS:
            done.add(pr)
    return done


def _compute_exit_code(results: list[tuple[PRRef, ProcessResult]], interrupted: bool) -> int:
    if interrupted:
        return EXIT_CODE_INTERRUPTED
    for _pr, r in results:
        cls = STATUS_TO_EXIT_CLASS.get(r.status)
        if cls is None or cls is not ExitClass.SUCCESS:
            return EXIT_CODE_FAILURE
    return EXIT_CODE_SUCCESS


def _build_summary(ctx: RunContext, run_id: str, started: str,
                   results: list[tuple[PRRef, ProcessResult]], exit_code: int) -> dict:
    counts: Counter = Counter()
    for _pr, r in results:
        cls = STATUS_TO_EXIT_CLASS.get(r.status, ExitClass.ERROR)
        if r.status == "done":
            counts["done"] += 1
        elif r.status == "queued":
            counts["queued"] += 1
        elif cls is ExitClass.ERROR:
            counts["failed"] += 1
        else:
            counts["skipped"] += 1
    return {
        "run_id": run_id,
        "started": started,
        "ended": _utcnow_iso(),
        "exit_code": exit_code,
        "counts": {"done": counts["done"], "queued": counts["queued"],
                   "skipped": counts["skipped"], "failed": counts["failed"]},
        "prs": [
            {"pr": ctx.pr_token(pr), "status": r.status, "duration_ms": r.duration_ms}
            for pr, r in results
        ],
    }


def _print_summary(run_id: str, results: list[tuple[PRRef, ProcessResult]], exit_code: int) -> None:
    print()
    print(f"=== github_approve_merge summary (run {run_id}) ===")
    for pr, r in results:
        print(f"  {str(pr):<60s}  {r.status:<28s}  {r.duration_ms} ms")
    print(f"Exit: {exit_code}")


def _utcnow_iso() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"
