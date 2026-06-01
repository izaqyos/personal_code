from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable

from github_approve_merge.gh_client import GhAuthError, GhNotFound
from github_approve_merge.merge_action import MergeAction, select_merge_action
from github_approve_merge.pr_state import PRState, StateFlag
from github_approve_merge.url import PRRef

EXIT_CODE_SUCCESS = 0
EXIT_CODE_FAILURE = 1
EXIT_CODE_USAGE = 2
EXIT_CODE_INTERRUPTED = 130

_log = logging.getLogger("gam")


class ExitClass(Enum):
    SUCCESS = "success"
    WARN = "warn"
    ERROR = "error"


STATUS_TO_EXIT_CLASS: dict[str, ExitClass] = {
    # Terminal success
    "done": ExitClass.SUCCESS,
    "queued": ExitClass.SUCCESS,
    "would-merge": ExitClass.SUCCESS,
    "skipped-merged": ExitClass.SUCCESS,
    # Terminal warn (user gave us a URL we couldn't/shouldn't merge, or declined the gate)
    "skipped-closed": ExitClass.WARN,
    "skipped-draft": ExitClass.WARN,
    "skipped-self": ExitClass.WARN,
    "skipped-needs-more-approvals": ExitClass.WARN,
    "cancelled": ExitClass.WARN,
    # Terminal error
    "failed-conflict": ExitClass.ERROR,
    "failed-required-check": ExitClass.ERROR,
    "failed-locked": ExitClass.ERROR,
    "failed-auth": ExitClass.ERROR,
    "failed-not-found": ExitClass.ERROR,
    "failed-interrupted": ExitClass.ERROR,
    "failed-exception": ExitClass.ERROR,
}


def aggregate_exit_code(statuses: list[str]) -> int:
    """Return EXIT_CODE_SUCCESS iff every status is SUCCESS-class. Otherwise EXIT_CODE_FAILURE.

    Empty input is treated as failure so the caller notices nothing was processed.
    Unknown statuses are conservatively treated as failures.
    """
    if not statuses:
        return EXIT_CODE_FAILURE
    for s in statuses:
        cls = STATUS_TO_EXIT_CLASS.get(s)
        if cls is None or cls is not ExitClass.SUCCESS:
            return EXIT_CODE_FAILURE
    return EXIT_CODE_SUCCESS


_STATE_TO_TERMINAL_STATUS: dict[PRState, str] = {
    PRState.MERGED: "skipped-merged",
    PRState.CLOSED: "skipped-closed",
    PRState.DRAFT: "skipped-draft",
    PRState.SELF_AUTHORED: "skipped-self",
    PRState.CONFLICT: "failed-conflict",
    PRState.REQUIRED_FAILING: "failed-required-check",
    PRState.LOCKED: "failed-locked",
}
_TERMINAL_STATES = set(_STATE_TO_TERMINAL_STATUS)
_MERGEABLE_STATES = {PRState.OPEN_MERGEABLE, PRState.REQUIRED_PENDING}


@dataclass(frozen=True)
class ProcessResult:
    status: str
    error_message: str = ""
    duration_ms: int = 0


@dataclass(frozen=True)
class MergeDecision:
    pr: PRRef
    state: PRState
    action: MergeAction
    will_approve: bool


# Gate: given the list of MergeDecisions, return a parallel list of bools (proceed?).
Gate = Callable[[list["MergeDecision"]], list[bool]]


def plan_pr(client, pr: PRRef, *, approve: bool, do_merge: bool,
            dry_run: bool = False) -> "MergeDecision | str":
    """Pass 1: classify and (if needed) approve, returning either a terminal status string
    or a MergeDecision to be gated+executed later. May raise GhError subclasses; callers
    map those to failed-* statuses. See spec §7."""
    state, flags = client.classify(pr)

    if state in _TERMINAL_STATES:
        return _STATE_TO_TERMINAL_STATUS[state]

    will_approve = (
        approve and state is PRState.OPEN_APPROVABLE
        and StateFlag.ALREADY_APPROVED not in flags
    )

    if dry_run:
        return "would-merge"

    if will_approve:
        client.approve(pr)
        state, flags = client.classify(pr)
        if state in _TERMINAL_STATES:
            return _STATE_TO_TERMINAL_STATUS[state]
        if state is PRState.OPEN_APPROVABLE:
            return "skipped-needs-more-approvals"

    if not do_merge or state not in _MERGEABLE_STATES:
        return "skipped-needs-more-approvals"

    action = select_merge_action(state, has_queue=client.has_queue(pr))
    return MergeDecision(pr=pr, state=state, action=action, will_approve=will_approve)


def execute_decision(client, decision: "MergeDecision", method: str) -> str:
    """Pass 2: perform the gated merge action. Returns the terminal status string."""
    if decision.action is MergeAction.ENQUEUE:
        client.enqueue(decision.pr)
        return "queued"
    if decision.action is MergeAction.DIRECT_MERGE:
        client.direct_merge(decision.pr, method)
        return "done"
    client.enable_auto_merge(decision.pr, method)
    return "done"


async def process_pr(
    client,
    pr: PRRef,
    *,
    approve: bool,
    do_merge: bool,
    method: str,
    gate: Gate,
    dry_run: bool = False,
) -> ProcessResult:
    """Single-PR convenience wrapper: plan → gate([decision]) → execute. The batch runner
    uses plan_pr/execute_decision directly so the gate sees all PRs at once."""
    started = time.monotonic()
    try:
        outcome = plan_pr(client, pr, approve=approve, do_merge=do_merge, dry_run=dry_run)
        if isinstance(outcome, MergeDecision):
            if not gate([outcome])[0]:
                status = "cancelled"
            else:
                status = execute_decision(client, outcome, method)
        else:
            status = outcome
        return _result(status, started)
    except GhAuthError as e:
        return ProcessResult("failed-auth", repr(e), _elapsed(started))
    except GhNotFound as e:
        return ProcessResult("failed-not-found", repr(e), _elapsed(started))
    except Exception as e:  # broad: batch must continue
        _log.error("process_pr failed", exc_info=True, extra={"pr": str(pr)})
        return ProcessResult("failed-exception", repr(e), _elapsed(started))


def _result(status: str, started: float) -> ProcessResult:
    return ProcessResult(status=status, duration_ms=_elapsed(started))


def _elapsed(started: float) -> int:
    return int((time.monotonic() - started) * 1000)
