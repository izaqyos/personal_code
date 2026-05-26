from __future__ import annotations

from playwright.async_api import Locator, Page

from github_approve_merge.pages import selectors as S
from github_approve_merge.url import PRRef


class FilesPage:
    """Page Object for the Files-changed tab (where the Approve form lives)."""

    def __init__(self, page: Page):
        self.page = page

    async def goto(self, pr: PRRef) -> None:
        url = f"https://github.com/{pr.owner}/{pr.repo}/pull/{pr.number}/files"
        await self.page.goto(url, wait_until="domcontentloaded")

    def approve_radio(self) -> Locator:
        return self.page.locator(
            f'input[type="radio"][name="pull_request_review[event]"][value="{S.APPROVE_RADIO_VALUE}"]'
        )

    def submit_review_button(self) -> Locator:
        return self.page.get_by_role("button", name=S.SUBMIT_REVIEW_NAME)

    async def select_approve_and_submit(self) -> None:
        radio = self.approve_radio()
        await radio.check()
        await self.submit_review_button().click()
