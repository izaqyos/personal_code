from __future__ import annotations

from enum import Enum, auto

from github_approve_merge.pr_state import PRState


class MergeAction(Enum):
    ENQUEUE = auto()        # repo uses a merge queue
    DIRECT_MERGE = auto()   # mergeable now, no queue
    AUTO_MERGE = auto()     # checks pending, no queue → enable auto-merge


_MERGEABLE_STATES = {PRState.OPEN_MERGEABLE, PRState.REQUIRED_PENDING}


def select_merge_action(state: PRState, *, has_queue: bool) -> MergeAction:
    if state not in _MERGEABLE_STATES:
        raise ValueError(f"{state} is not a mergeable state")
    if has_queue:
        return MergeAction.ENQUEUE
    if state is PRState.OPEN_MERGEABLE:
        return MergeAction.DIRECT_MERGE
    return MergeAction.AUTO_MERGE
