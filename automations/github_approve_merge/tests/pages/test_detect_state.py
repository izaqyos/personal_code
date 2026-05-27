import pytest

from github_approve_merge.pr_state import PRState, StateFlag, detect_state


@pytest.mark.asyncio
async def test_merged(page, fixture_url):
    await page.goto(fixture_url("pr_merged.html"))
    state, flags = await detect_state(page, me="reviewer-bot")
    assert state is PRState.MERGED
    assert flags == set()


@pytest.mark.asyncio
async def test_closed(page, fixture_url):
    await page.goto(fixture_url("pr_closed.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.CLOSED


@pytest.mark.asyncio
async def test_draft(page, fixture_url):
    await page.goto(fixture_url("pr_draft.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.DRAFT


@pytest.mark.asyncio
async def test_locked(page, fixture_url):
    await page.goto(fixture_url("pr_locked.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.LOCKED


@pytest.mark.asyncio
async def test_self_authored(page, fixture_url):
    await page.goto(fixture_url("pr_self.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.SELF_AUTHORED


@pytest.mark.asyncio
async def test_conflict(page, fixture_url):
    await page.goto(fixture_url("pr_conflict.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.CONFLICT


@pytest.mark.asyncio
async def test_required_failing(page, fixture_url):
    await page.goto(fixture_url("pr_required_check_failing.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.REQUIRED_FAILING


@pytest.mark.asyncio
async def test_required_pending(page, fixture_url):
    await page.goto(fixture_url("pr_ci_pending.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.REQUIRED_PENDING


@pytest.mark.asyncio
async def test_open_mergeable(page, fixture_url):
    await page.goto(fixture_url("pr_mergeable.html"))
    state, flags = await detect_state(page, me="reviewer-bot")
    assert state is PRState.OPEN_MERGEABLE
    assert StateFlag.ALREADY_APPROVED not in flags


@pytest.mark.asyncio
async def test_open_approvable(page, fixture_url):
    await page.goto(fixture_url("pr_needs_approval.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.OPEN_APPROVABLE


@pytest.mark.asyncio
async def test_already_approved_flag(page, fixture_url):
    await page.goto(fixture_url("pr_already_approved_by_me.html"))
    state, flags = await detect_state(page, me="reviewer-bot")
    assert state is PRState.OPEN_MERGEABLE
    assert StateFlag.ALREADY_APPROVED in flags
