import pytest

from github_approve_merge.pages.pr_page import PRPage


@pytest.mark.asyncio
async def test_merge_button_locator_resolves(page, fixture_url):
    await page.goto(fixture_url("pr_mergeable.html"))
    locator = PRPage(page).merge_button()
    assert await locator.count() == 1
    assert await locator.is_enabled()


@pytest.mark.asyncio
async def test_merge_button_disabled_on_needs_approval(page, fixture_url):
    await page.goto(fixture_url("pr_needs_approval.html"))
    locator = PRPage(page).merge_button()
    # The button exists but is disabled.
    assert await locator.count() == 1
    assert not await locator.is_enabled()


@pytest.mark.asyncio
async def test_merge_when_ready_locator_resolves_on_ci_pending(page, fixture_url):
    await page.goto(fixture_url("pr_ci_pending.html"))
    locator = PRPage(page).merge_when_ready_button()
    assert await locator.count() == 1
    assert await locator.is_enabled()


@pytest.mark.asyncio
async def test_confirm_merge_locator_resolves(page, fixture_url):
    await page.goto(fixture_url("pr_mergeable.html"))
    locator = PRPage(page).confirm_merge_button()
    assert await locator.count() == 1


@pytest.mark.asyncio
async def test_user_login_lookup(page, fixture_url):
    await page.goto(fixture_url("pr_mergeable.html"))
    assert await PRPage(page).authenticated_login() == "reviewer-bot"


@pytest.mark.asyncio
async def test_pr_author_lookup(page, fixture_url):
    await page.goto(fixture_url("pr_self.html"))
    assert await PRPage(page).pr_author_login() == "reviewer-bot"
