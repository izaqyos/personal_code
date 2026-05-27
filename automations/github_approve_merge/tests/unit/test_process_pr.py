from pathlib import Path

import pytest

from github_approve_merge.actions import ProcessResult, process_pr
from github_approve_merge.logging_setup import RunContext
from github_approve_merge.pr_state import PRState, StateFlag
from github_approve_merge.url import PRRef


class FakePage:
    """Minimal stand-in for playwright.Page used by FakePRPage.detect_state seam."""


class FakePRPage:
    def __init__(self, states: list[tuple[PRState, set[StateFlag]]]):
        # Each call to detect_state pops the next pre-canned state.
        self._states = list(states)
        self.merge_clicked = False
        self.merge_when_ready_clicked = False
        self.goto_calls = 0

    async def goto(self, pr: PRRef) -> None:
        self.goto_calls += 1

    async def detect_state(self, me: str | None):
        return self._states.pop(0)

    async def click_merge_and_confirm(self):
        self.merge_clicked = True

    async def click_merge_when_ready(self):
        self.merge_when_ready_clicked = True

    async def wait_for_merged(self, timeout_ms: int = 30_000):
        pass


class FakeFilesPage:
    def __init__(self):
        self.approve_submitted = False

    async def goto(self, pr: PRRef):
        pass

    async def select_approve_and_submit(self):
        self.approve_submitted = True


@pytest.fixture
def ctx(tmp_path: Path) -> RunContext:
    return RunContext(
        run_id="rid",
        run_dir=tmp_path,
        authenticated_login="reviewer-bot",
    )


PR = PRRef("o", "r", 1)


@pytest.mark.asyncio
async def test_merged_state_skips(ctx):
    pr_page = FakePRPage([(PRState.MERGED, set())])
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=FakeFilesPage(),
                              capture=_noop_capture)
    assert result == ProcessResult(status="skipped-merged")
    assert not pr_page.merge_clicked


@pytest.mark.asyncio
async def test_closed_state_skips_warn(ctx):
    pr_page = FakePRPage([(PRState.CLOSED, set())])
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=FakeFilesPage(),
                              capture=_noop_capture)
    assert result.status == "skipped-closed"


@pytest.mark.asyncio
async def test_self_authored_state_skips(ctx):
    pr_page = FakePRPage([(PRState.SELF_AUTHORED, set())])
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=FakeFilesPage(),
                              capture=_noop_capture)
    assert result.status == "skipped-self"


@pytest.mark.asyncio
async def test_conflict_fails(ctx):
    pr_page = FakePRPage([(PRState.CONFLICT, set())])
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=FakeFilesPage(),
                              capture=_noop_capture)
    assert result.status == "failed-conflict"


@pytest.mark.asyncio
async def test_open_mergeable_path(ctx):
    pr_page = FakePRPage([(PRState.OPEN_MERGEABLE, set())])
    fp = FakeFilesPage()
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=fp, capture=_noop_capture)
    assert result.status == "done"
    assert pr_page.merge_clicked
    assert not fp.approve_submitted  # No approve step needed.


@pytest.mark.asyncio
async def test_open_approvable_path_approves_then_merges(ctx):
    # First detect: needs approve. After approve+refresh: mergeable.
    pr_page = FakePRPage([
        (PRState.OPEN_APPROVABLE, set()),
        (PRState.OPEN_MERGEABLE, set()),
    ])
    fp = FakeFilesPage()
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=fp, capture=_noop_capture)
    assert result.status == "done"
    assert fp.approve_submitted
    assert pr_page.merge_clicked


@pytest.mark.asyncio
async def test_already_approved_skips_approve_still_merges(ctx):
    pr_page = FakePRPage([(PRState.OPEN_MERGEABLE, {StateFlag.ALREADY_APPROVED})])
    fp = FakeFilesPage()
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=fp, capture=_noop_capture)
    assert result.status == "done"
    assert not fp.approve_submitted
    assert pr_page.merge_clicked


@pytest.mark.asyncio
async def test_required_pending_uses_merge_when_ready(ctx):
    pr_page = FakePRPage([(PRState.REQUIRED_PENDING, set())])
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=FakeFilesPage(),
                              capture=_noop_capture)
    assert result.status == "done"
    assert pr_page.merge_when_ready_clicked


@pytest.mark.asyncio
async def test_post_approve_state_still_approvable_means_needs_more_reviewers(ctx):
    pr_page = FakePRPage([
        (PRState.OPEN_APPROVABLE, set()),
        (PRState.OPEN_APPROVABLE, set()),  # didn't unlock merge
    ])
    fp = FakeFilesPage()
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=fp, capture=_noop_capture)
    assert result.status == "skipped-needs-more-approvals"
    assert fp.approve_submitted
    assert not pr_page.merge_clicked


@pytest.mark.asyncio
async def test_dry_run_classifies_but_does_not_act(ctx):
    pr_page = FakePRPage([(PRState.OPEN_MERGEABLE, set())])
    fp = FakeFilesPage()
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=fp,
                              capture=_noop_capture, dry_run=True)
    assert result.status == "skipped-merged" or result.status.startswith("skipped-")
    assert not pr_page.merge_clicked
    assert not fp.approve_submitted


@pytest.mark.asyncio
async def test_unexpected_exception_yields_failed_exception(ctx):
    class Boom(FakePRPage):
        async def click_merge_and_confirm(self):
            raise RuntimeError("network gone")
    pr_page = Boom([(PRState.OPEN_MERGEABLE, set())])
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=FakeFilesPage(),
                              capture=_noop_capture)
    assert result.status == "failed-exception"
    assert "network gone" in result.error_message


async def _noop_capture(_pr_page, _ctx, _pr, _label):
    return None


@pytest.mark.asyncio
async def test_dry_run_already_approved_returns_skipped_merged(ctx):
    """OPEN_APPROVABLE + ALREADY_APPROVED in dry-run should report skipped-merged,
    not failed-exception (would have merged via the bypass-approve path)."""
    pr_page = FakePRPage([(PRState.OPEN_APPROVABLE, {StateFlag.ALREADY_APPROVED})])
    fp = FakeFilesPage()
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=fp,
                              capture=_noop_capture, dry_run=True)
    assert result.status == "skipped-merged"
    assert not pr_page.merge_clicked
    assert not fp.approve_submitted


@pytest.mark.asyncio
async def test_conflict_takes_error_screenshot(ctx):
    captured_labels: list[str] = []

    async def recording_capture(_pp, _ctx, _pr, label):
        captured_labels.append(label)
        return None

    pr_page = FakePRPage([(PRState.CONFLICT, set())])
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=FakeFilesPage(),
                              capture=recording_capture)
    assert result.status == "failed-conflict"
    assert "error-conflict" in captured_labels
