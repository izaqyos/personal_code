import pytest

from github_approve_merge.gh_client import GhPR
from github_approve_merge.pr_state import PRState, StateFlag, classify


def mk(**over) -> GhPR:
    base = dict(number=1, state="OPEN", is_draft=False, locked=False,
                mergeable="MERGEABLE", merge_state_status="CLEAN",
                review_decision="APPROVED", author_login="bob",
                base_ref="master", reviews=[])
    base.update(over)
    return GhPR(**base)


@pytest.mark.parametrize("over,expected", [
    (dict(state="MERGED"), PRState.MERGED),
    (dict(state="CLOSED"), PRState.CLOSED),
    (dict(is_draft=True), PRState.DRAFT),
    (dict(locked=True), PRState.LOCKED),
    (dict(author_login="me"), PRState.SELF_AUTHORED),
    (dict(mergeable="CONFLICTING"), PRState.CONFLICT),
    (dict(merge_state_status="BLOCKED", review_decision="APPROVED"), PRState.REQUIRED_FAILING),
    # #271 regression: needs-approval PRs report BLOCKED (blocked on the review requirement),
    # not a failing check → must be approvable, not REQUIRED_FAILING.
    (dict(merge_state_status="BLOCKED", review_decision="REVIEW_REQUIRED"), PRState.OPEN_APPROVABLE),
    (dict(merge_state_status="BEHIND"), PRState.REQUIRED_PENDING),
    (dict(merge_state_status="UNSTABLE"), PRState.REQUIRED_PENDING),
    (dict(review_decision="REVIEW_REQUIRED", merge_state_status="CLEAN"), PRState.OPEN_APPROVABLE),
    (dict(review_decision="APPROVED", merge_state_status="CLEAN"), PRState.OPEN_MERGEABLE),
])
def test_classify_states(over, expected):
    state, _ = classify(mk(**over), me="me", has_queue=False)
    assert state == expected


def test_self_authored_takes_priority_over_open():
    state, _ = classify(mk(author_login="me", review_decision="REVIEW_REQUIRED"),
                        me="me", has_queue=False)
    assert state == PRState.SELF_AUTHORED


def test_already_approved_flag_set():
    pr = mk(review_decision="APPROVED",
            reviews=[{"author": {"login": "me"}, "state": "APPROVED"}])
    state, flags = classify(pr, me="me", has_queue=False)
    assert StateFlag.ALREADY_APPROVED in flags


def test_unknown_merge_state_is_conservatively_pending():
    state, _ = classify(mk(review_decision="APPROVED", merge_state_status="WEIRD"),
                        me="me", has_queue=False)
    assert state == PRState.REQUIRED_PENDING
