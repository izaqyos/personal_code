import pytest

from github_approve_merge.pages.files_page import FilesPage


@pytest.mark.asyncio
async def test_approve_radio_locator_resolves(page, fixture_url):
    await page.goto(fixture_url("files_can_approve.html"))
    locator = FilesPage(page).approve_radio()
    assert await locator.count() == 1


@pytest.mark.asyncio
async def test_approve_radio_absent_when_already_approved(page, fixture_url):
    await page.goto(fixture_url("files_already_approved.html"))
    locator = FilesPage(page).approve_radio()
    # Fixture deliberately omits the approve radio in this state.
    assert await locator.count() == 0


@pytest.mark.asyncio
async def test_submit_review_locator_resolves(page, fixture_url):
    await page.goto(fixture_url("files_can_approve.html"))
    locator = FilesPage(page).submit_review_button()
    assert await locator.count() == 1


@pytest.mark.asyncio
async def test_select_approve_then_submit_succeeds_against_fixture(page, fixture_url):
    # No backend, so this just verifies the method completes without raising:
    # the radio is selected and the submit button is clicked.
    # The fixture uses type="button" on the submit so the form doesn't navigate.
    await page.goto(fixture_url("files_can_approve.html"))
    fp = FilesPage(page)
    await fp.select_approve_and_submit()
    assert await fp.approve_radio().is_checked()
