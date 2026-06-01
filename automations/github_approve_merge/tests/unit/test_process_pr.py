import pytest

from github_approve_merge.actions import process_pr, MergeDecision
from github_approve_merge.gh_client import GhAuthError, GhNotFound
from github_approve_merge.pr_state import PRState, StateFlag
from github_approve_merge.merge_action import MergeAction
from github_approve_merge.url import PRRef


PR = PRRef("perimeter-81", "repo", 1)


class FakeClient:
    """Stand-in for the PrClient adapter. Pre-canned classification + records actions."""

    def __init__(self, *, states, has_queue=False, raise_on_fetch=None):
        self._states = list(states)   # list of (PRState, set[flags])
        self.has_queue_val = has_queue
        self.raise_on_fetch = raise_on_fetch
        self.approved = False
        self.enqueued = False
        self.direct_merged = False
        self.auto_merged = False
        self.fetches = 0

    def classify(self, pr):
        if self.raise_on_fetch is not None:
            raise self.raise_on_fetch
        self.fetches += 1
        return self._states.pop(0)

    def has_queue(self, pr):
        return self.has_queue_val

    def approve(self, pr):
        self.approved = True

    def enqueue(self, pr):
        self.enqueued = True

    def direct_merge(self, pr, method):
        self.direct_merged = True

    def enable_auto_merge(self, pr, method):
        self.auto_merged = True


def always_yes(decisions):
    return [True] * len(decisions)


@pytest.mark.asyncio
async def test_merged_skips():
    c = FakeClient(states=[(PRState.MERGED, set())])
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge", gate=always_yes)
    assert r.status == "skipped-merged"
    assert not c.enqueued and not c.direct_merged


@pytest.mark.asyncio
async def test_open_mergeable_direct_merge():
    c = FakeClient(states=[(PRState.OPEN_MERGEABLE, set())], has_queue=False)
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge", gate=always_yes)
    assert r.status == "done"
    assert c.direct_merged and not c.approved


@pytest.mark.asyncio
async def test_open_mergeable_enqueue_on_queue_repo():
    c = FakeClient(states=[(PRState.OPEN_MERGEABLE, set())], has_queue=True)
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge", gate=always_yes)
    assert r.status == "queued"
    assert c.enqueued


@pytest.mark.asyncio
async def test_approvable_then_mergeable_approves_then_enqueues():
    c = FakeClient(states=[(PRState.OPEN_APPROVABLE, set()),
                           (PRState.OPEN_MERGEABLE, set())], has_queue=True)
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge", gate=always_yes)
    assert c.approved and c.enqueued
    assert r.status == "queued"


@pytest.mark.asyncio
async def test_approvable_still_approvable_needs_more():
    c = FakeClient(states=[(PRState.OPEN_APPROVABLE, set()),
                           (PRState.OPEN_APPROVABLE, set())])
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge", gate=always_yes)
    assert r.status == "skipped-needs-more-approvals"
    assert c.approved and not c.direct_merged


@pytest.mark.asyncio
async def test_gate_decline_records_cancelled():
    c = FakeClient(states=[(PRState.OPEN_MERGEABLE, set())])
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge",
                         gate=lambda decisions: [False])
    assert r.status == "cancelled"
    assert not c.direct_merged


@pytest.mark.asyncio
async def test_dry_run_reports_would_merge_no_action():
    c = FakeClient(states=[(PRState.OPEN_MERGEABLE, set())])
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge",
                         gate=always_yes, dry_run=True)
    assert r.status == "would-merge"
    assert not c.direct_merged and not c.approved


@pytest.mark.asyncio
async def test_auth_error_records_failed_auth():
    c = FakeClient(states=[], raise_on_fetch=GhAuthError("sso"))
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge", gate=always_yes)
    assert r.status == "failed-auth"


@pytest.mark.asyncio
async def test_not_found_records_failed_not_found():
    c = FakeClient(states=[], raise_on_fetch=GhNotFound("404"))
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge", gate=always_yes)
    assert r.status == "failed-not-found"
