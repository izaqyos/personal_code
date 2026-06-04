from __future__ import annotations

from enum import Enum, auto

from github_approve_merge.gh_client import GhPR


class PRState(Enum):
    """Terminal classification of a PR's current state. See spec §6."""

    MERGED = auto()
    CLOSED = auto()
    DRAFT = auto()
    LOCKED = auto()
    SELF_AUTHORED = auto()
    CONFLICT = auto()
    REQUIRED_FAILING = auto()
    REQUIRED_PENDING = auto()
    OPEN_MERGEABLE = auto()
    OPEN_APPROVABLE = auto()


class StateFlag(Enum):
    """Modifier flags that combine with a PRState."""

    ALREADY_APPROVED = auto()


# mergeStateStatus values meaning "blocked on a hard requirement" → failing (only when
# the PR is already approved; see classify()).
_FAILING_STATUS = {"BLOCKED", "DIRTY"}


def classify(pr: GhPR, *, me: str | None, has_queue: bool) -> tuple[PRState, set[StateFlag]]:
    """Classify a PR from structured `gh` fields. See spec §6.

    `has_queue` is accepted for symmetry with the action layer but does not change the
    state — a merge-queue repo still classifies as OPEN_MERGEABLE/REQUIRED_PENDING; the
    queue only changes the *action* (see merge_action.select_merge_action).
    """
    flags: set[StateFlag] = set()

    if pr.state == "MERGED":
        return PRState.MERGED, flags
    if pr.state == "CLOSED":
        return PRState.CLOSED, flags
    if pr.is_draft:
        return PRState.DRAFT, flags
    if pr.locked:
        return PRState.LOCKED, flags
    if me and pr.author_login == me:
        return PRState.SELF_AUTHORED, flags
    if pr.mergeable == "CONFLICTING":
        return PRState.CONFLICT, flags

    if me and pr.approved_by(me):
        flags.add(StateFlag.ALREADY_APPROVED)

    # Review-first. A PR awaiting approval reports mergeStateStatus=BLOCKED *because* the
    # review is the missing requirement (this is the #271 case). So if it isn't approved
    # yet, it's approvable — we defer any check-failure judgment until after we approve and
    # re-classify. Only once APPROVED does BLOCKED/DIRTY mean a hard requirement is failing.
    if pr.review_decision != "APPROVED":
        return PRState.OPEN_APPROVABLE, flags

    mss = pr.merge_state_status
    if mss in _FAILING_STATUS:
        return PRState.REQUIRED_FAILING, flags
    if mss == "CLEAN":
        return PRState.OPEN_MERGEABLE, flags
    # BEHIND / UNSTABLE / HAS_HOOKS / UNKNOWN / anything unrecognized → conservatively pending
    # (routes to the gated enqueue/auto-merge path, never a blind direct merge).
    return PRState.REQUIRED_PENDING, flags
