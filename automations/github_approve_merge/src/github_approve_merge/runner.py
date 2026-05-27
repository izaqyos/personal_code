from __future__ import annotations

import asyncio
import json
import logging
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Awaitable, Callable

from github_approve_merge.actions import (
    EXIT_CODE_FAILURE,
    EXIT_CODE_INTERRUPTED,
    EXIT_CODE_SUCCESS,
    STATUS_TO_EXIT_CLASS,
    ExitClass,
    ProcessResult,
)
from github_approve_merge.logging_setup import RunContext
from github_approve_merge.url import PRRef

_log = logging.getLogger("gam")

ProcessFn = Callable[..., Awaitable[ProcessResult]]


class Runner:
    """Orchestrates a batch: iterates PRs, writes state.jsonl per transition, writes summary.json."""

    def __init__(
        self,
        *,
        logs_dir: Path,
        run_id: str,
        process_pr_fn: ProcessFn,
        resume: bool = False,
        ctx: RunContext | None = None,
    ):
        self.logs_dir = logs_dir
        self.run_id = run_id
        self.run_dir = logs_dir / run_id
        self.process_pr_fn = process_pr_fn
        self.resume = resume
        self.ctx = ctx or RunContext(run_id=run_id, run_dir=self.run_dir)

    async def execute(self, prs: list[PRRef]) -> int:
        self.run_dir.mkdir(parents=True, exist_ok=True)
        started = _utcnow_iso()
        completed_on_resume = self._load_completed_for_resume() if self.resume else set()

        # Queue every PR up front so a SIGINT before the first one still leaves a record.
        for pr in prs:
            if self.ctx.pr_token(pr) in completed_on_resume:
                continue
            self._append_state(pr, "queued")

        interrupted = False
        results: list[tuple[PRRef, ProcessResult]] = []
        for pr in prs:
            slug = self.ctx.pr_token(pr)
            if slug in completed_on_resume:
                _log.info("resume: skipping already-done PR", extra={"pr": slug, "step": "resume"})
                continue

            self._append_state(pr, "in_progress")
            try:
                result = await self.process_pr_fn(self.ctx, pr)
            except asyncio.CancelledError:
                self._append_state(pr, "failed-interrupted")
                results.append((pr, ProcessResult(status="failed-interrupted")))
                interrupted = True
                break
            self._append_state(pr, result.status, duration_ms=result.duration_ms,
                               error_message=result.error_message)
            results.append((pr, result))

        exit_code = self._compute_exit_code(results, interrupted)
        self._write_summary(started, results, exit_code)
        self._print_summary(results, exit_code)
        return exit_code

    # --- state.jsonl --------------------------------------------------------

    def _state_path(self) -> Path:
        return self.run_dir / "state.jsonl"

    def _append_state(self, pr: PRRef, status: str, *, duration_ms: int = 0,
                      error_message: str = "") -> None:
        record = {"ts": _utcnow_iso(), "pr": self.ctx.pr_token(pr), "status": status}
        if duration_ms:
            record["duration_ms"] = duration_ms
        if error_message:
            record["error"] = error_message
        with self._state_path().open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def _load_completed_for_resume(self) -> set[str]:
        """Read existing state.jsonl (if any) and return the PRs whose latest status is terminal+success-class."""
        path = self._state_path()
        if not path.exists():
            return set()
        latest: dict[str, str] = {}
        for line in path.read_text().splitlines():
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
            if status == "done" or status.startswith("skipped-"):
                done.add(pr)
            elif cls is ExitClass.SUCCESS:
                done.add(pr)
        return done

    # --- summary -----------------------------------------------------------

    def _compute_exit_code(self, results: list[tuple[PRRef, ProcessResult]], interrupted: bool) -> int:
        if interrupted:
            return EXIT_CODE_INTERRUPTED
        for _pr, r in results:
            cls = STATUS_TO_EXIT_CLASS.get(r.status)
            if cls is None or cls is not ExitClass.SUCCESS:
                return EXIT_CODE_FAILURE
        return EXIT_CODE_SUCCESS

    def _write_summary(self, started: str, results: list[tuple[PRRef, ProcessResult]], exit_code: int) -> None:
        counts = Counter()
        for _pr, r in results:
            cls = STATUS_TO_EXIT_CLASS.get(r.status, ExitClass.ERROR)
            if r.status == "done":
                counts["done"] += 1
            elif cls is ExitClass.ERROR:
                counts["failed"] += 1
            else:
                counts["skipped"] += 1
        summary = {
            "run_id": self.run_id,
            "started": started,
            "ended": _utcnow_iso(),
            "exit_code": exit_code,
            "counts": {"done": counts["done"], "skipped": counts["skipped"], "failed": counts["failed"]},
            "prs": [
                {"pr": self.ctx.pr_token(pr), "status": r.status, "duration_ms": r.duration_ms}
                for pr, r in results
            ],
        }
        (self.run_dir / "summary.json").write_text(json.dumps(summary, indent=2))

    def _print_summary(self, results: list[tuple[PRRef, ProcessResult]], exit_code: int) -> None:
        print()
        print(f"=== github_approve_merge summary (run {self.run_id}) ===")
        for pr, r in results:
            print(f"  {str(pr):<60s}  {r.status:<28s}  {r.duration_ms} ms")
        print(f"Exit: {exit_code}")


def _utcnow_iso() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"
