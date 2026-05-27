from __future__ import annotations

from playwright.async_api import Locator, Page

from github_approve_merge.pages import selectors as S
from github_approve_merge.url import PRRef


class PRPage:
    """Page Object for the PR overview page (the merge widget lives here)."""

    def __init__(self, page: Page):
        self.page = page

    # --- Navigation ---------------------------------------------------------

    async def goto(self, pr: PRRef) -> None:
        url = f"https://github.com/{pr.owner}/{pr.repo}/pull/{pr.number}"
        await self.page.goto(url, wait_until="domcontentloaded")

    # --- Locators (no clicks; used by tests and by action methods) ---------

    def merge_button(self) -> Locator:
        return self.page.get_by_role("button", name=S.MERGE_BUTTON_NAME)

    def confirm_merge_button(self) -> Locator:
        return self.page.get_by_role("button", name=S.CONFIRM_MERGE_NAME)

    def merge_when_ready_button(self) -> Locator:
        # GitHub uses either label depending on the moment in the rollout.
        primary = self.page.get_by_role("button", name=S.MERGE_WHEN_READY_NAME)
        return primary.or_(self.page.get_by_role("button", name=S.ENABLE_AUTO_MERGE_NAME))

    # --- High-level actions -------------------------------------------------

    async def click_merge_and_confirm(self) -> None:
        await self.merge_button().click()
        await self.confirm_merge_button().click()

    async def click_merge_when_ready(self) -> None:
        await self.merge_when_ready_button().click()
        # GitHub may show a confirm dialog with the same text; click it if present.
        confirm = self.confirm_merge_button()
        if await confirm.count() > 0 and await confirm.first.is_visible():
            await confirm.first.click()

    async def wait_for_merged(self, timeout_ms: int = 30_000) -> None:
        """Wait for either the merged-state badge or the 'Merge when ready' state to settle."""
        merged = self.page.get_by_text(S.STATE_BADGE_MERGED).first
        scheduled = self.page.get_by_role("button", name=S.MERGE_WHEN_READY_NAME)
        await merged.or_(scheduled).wait_for(state="attached", timeout=timeout_ms)

    # --- Identity lookups ---------------------------------------------------

    async def authenticated_login(self) -> str | None:
        el = self.page.locator(S.USER_LOGIN_META)
        if await el.count() == 0:
            return None
        return await el.first.get_attribute("content")

    async def pr_author_login(self) -> str | None:
        el = self.page.locator(S.PR_AUTHOR_LINK_CSS)
        if await el.count() == 0:
            return None
        text = await el.first.text_content()
        return text.strip() if text else None

    async def detect_state(self, *, me: str | None):
        # Delegates to the module-level function for testability.
        from github_approve_merge.pr_state import detect_state as _ds
        return await _ds(self.page, me=me)
