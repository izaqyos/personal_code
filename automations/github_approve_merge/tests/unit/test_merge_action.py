import pytest

from github_approve_merge.pr_state import PRState
from github_approve_merge.merge_action import MergeAction, select_merge_action


@pytest.mark.parametrize("state,has_queue,expected", [
    (PRState.OPEN_MERGEABLE, True, MergeAction.ENQUEUE),
    (PRState.OPEN_MERGEABLE, False, MergeAction.DIRECT_MERGE),
    (PRState.REQUIRED_PENDING, True, MergeAction.ENQUEUE),
    (PRState.REQUIRED_PENDING, False, MergeAction.AUTO_MERGE),
])
def test_select(state, has_queue, expected):
    assert select_merge_action(state, has_queue=has_queue) == expected


def test_non_mergeable_state_raises():
    with pytest.raises(ValueError):
        select_merge_action(PRState.CONFLICT, has_queue=False)
