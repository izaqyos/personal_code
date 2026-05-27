from __future__ import annotations

from enum import Enum

EXIT_CODE_SUCCESS = 0
EXIT_CODE_FAILURE = 1
EXIT_CODE_USAGE = 2
EXIT_CODE_INTERRUPTED = 130


class ExitClass(Enum):
    SUCCESS = "success"
    WARN = "warn"
    ERROR = "error"


STATUS_TO_EXIT_CLASS: dict[str, ExitClass] = {
    # Terminal success
    "done": ExitClass.SUCCESS,
    "skipped-merged": ExitClass.SUCCESS,
    # Terminal warn (user gave us a URL we couldn't merge)
    "skipped-closed": ExitClass.WARN,
    "skipped-draft": ExitClass.WARN,
    "skipped-self": ExitClass.WARN,
    "skipped-needs-more-approvals": ExitClass.WARN,
    # Terminal error
    "failed-conflict": ExitClass.ERROR,
    "failed-required-check": ExitClass.ERROR,
    "failed-locked": ExitClass.ERROR,
    "failed-interrupted": ExitClass.ERROR,
    "failed-exception": ExitClass.ERROR,
}


def aggregate_exit_code(statuses: list[str]) -> int:
    """Return EXIT_CODE_SUCCESS iff every status is SUCCESS-class. Otherwise EXIT_CODE_FAILURE.

    Empty input is treated as failure so the caller notices that nothing was processed.
    Unknown statuses are conservatively treated as failures.
    """
    if not statuses:
        return EXIT_CODE_FAILURE
    for s in statuses:
        cls = STATUS_TO_EXIT_CLASS.get(s)
        if cls is None or cls is not ExitClass.SUCCESS:
            return EXIT_CODE_FAILURE
    return EXIT_CODE_SUCCESS


import logging  # noqa: E402
import time
from dataclasses import dataclass
from typing import Awaitable, Callable, Protocol

from github_approve_merge.logging_setup import RunContext
from github_approve_merge.pr_state import PRState, StateFlag
from github_approve_merge.url import PRRef


_log = logging.getLogger("gam")


# Mapping from terminal PRState to a status string for state.jsonl.
_STATE_TO_TERMINAL_STATUS: dict[PRState, str] = {
    PRState.MERGED: "skipped-merged",
    PRState.CLOSED: "skipped-closed",
    PRState.DRAFT: "skipped-draft",
    PRState.SELF_AUTHORED: "skipped-self",
    PRState.CONFLICT: "failed-conflict",
    PRState.REQUIRED_FAILING: "failed-required-check",
    PRState.LOCKED: "failed-locked",
}
_TERMINAL_STATES: set[PRState] = set(_STATE_TO_TERMINAL_STATUS)


@dataclass(frozen=True)
class ProcessResult:
    status: str
    error_message: str = ""
    duration_ms: int = 0


# Structural protocols make the action layer browser-agnostic; tests inject fakes.

class PRPageProto(Protocol):
    async def goto(self, pr: PRRef) -> None: ...
    async def detect_state(self, *, me: str | None): ...
    async def click_merge_and_confirm(self) -> None: ...
    async def click_merge_when_ready(self) -> None: ...
    async def wait_for_merged(self, timeout_ms: int = ...) -> None: ...


class FilesPageProto(Protocol):
    async def goto(self, pr: PRRef) -> None: ...
    async def select_approve_and_submit(self) -> None: ...


CaptureFn = Callable[[object, RunContext, PRRef, str], Awaitable[object]]


async def process_pr(
    ctx: RunContext,
    pr: PRRef,
    *,
    pr_page: PRPageProto,
    files_page: FilesPageProto,
    capture: CaptureFn,
    dry_run: bool = False,
) -> ProcessResult:
    """Execute the full per-PR flow described in spec §5."""
    started = time.monotonic()
    try:
        await pr_page.goto(pr)
        await capture(pr_page, ctx, pr, "after-load")

        state, flags = await pr_page.detect_state(me=ctx.authenticated_login)

        if state in _TERMINAL_STATES:
            status = _STATE_TO_TERMINAL_STATUS[state]
            if status.startswith("failed-"):
                await capture(pr_page, ctx, pr, f"error-{status.removeprefix('failed-')}")
            return _result(status, started)

        if dry_run:
            return _result(_dry_run_status_for(state, flags), started)

        if state is PRState.OPEN_APPROVABLE and StateFlag.ALREADY_APPROVED not in flags:
            await files_page.goto(pr)
            await files_page.select_approve_and_submit()
            await capture(pr_page, ctx, pr, "after-approve-submit")
            await pr_page.goto(pr)
            state, flags = await pr_page.detect_state(me=ctx.authenticated_login)
            if state in _TERMINAL_STATES:
                status = _STATE_TO_TERMINAL_STATUS[state]
                if status.startswith("failed-"):
                    await capture(pr_page, ctx, pr, f"error-{status.removeprefix('failed-')}")
                return _result(status, started)
            if state is PRState.OPEN_APPROVABLE:
                return _result("skipped-needs-more-approvals", started)

        await capture(pr_page, ctx, pr, "before-merge-click")
        if state is PRState.REQUIRED_PENDING:
            await pr_page.click_merge_when_ready()
        else:  # OPEN_MERGEABLE
            await pr_page.click_merge_and_confirm()
        await pr_page.wait_for_merged()
        await capture(pr_page, ctx, pr, "after-merge")
        return _result("done", started)

    except Exception as e:  # broad on purpose: batch must continue
        _log.error("process_pr failed", exc_info=True, extra={"pr": str(pr), "step": "process_pr"})
        return ProcessResult(
            status="failed-exception",
            error_message=repr(e),
            duration_ms=_elapsed(started),
        )


def _result(status: str, started: float) -> ProcessResult:
    return ProcessResult(status=status, duration_ms=_elapsed(started))


def _elapsed(started: float) -> int:
    return int((time.monotonic() - started) * 1000)


def _dry_run_status_for(state: PRState, _flags: set[StateFlag]) -> str:
    """In dry-run return what the action WOULD have ended in."""
    if state in (PRState.OPEN_APPROVABLE, PRState.OPEN_MERGEABLE, PRState.REQUIRED_PENDING):
        return "skipped-merged"
    return _STATE_TO_TERMINAL_STATUS.get(state, "failed-exception")
