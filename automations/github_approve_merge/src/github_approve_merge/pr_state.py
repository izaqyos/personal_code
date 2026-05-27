from __future__ import annotations

from enum import Enum, auto

from playwright.async_api import Page

from github_approve_merge.pages import selectors as S
from github_approve_merge.pages.pr_page import PRPage


class PRState(Enum):
    """Terminal classification of a PR's current state. See spec §9."""

    MERGED = auto()
    CLOSED = auto()
    DRAFT = auto()
    LOCKED = auto()
    SELF_AUTHORED = auto()
    CONFLICT = auto()
    REQUIRED_FAILING = auto()
    REQUIRED_PENDING = auto()
    OPEN_MERGEABLE = auto()
    OPEN_APPROVABLE = auto()


class StateFlag(Enum):
    """Modifier flags that combine with a PRState. See spec §9."""

    ALREADY_APPROVED = auto()


async def detect_state(page: Page, *, me: str | None) -> tuple[PRState, set[StateFlag]]:
    """Inspect the loaded PR page DOM and classify it. See spec §9.

    `me` is the authenticated user's login (e.g. "reviewer-bot"). Pass None to skip the
    self-PR check.
    """
    flags: set[StateFlag] = set()

    # 1-2: header status badges.
    if await _text_visible(page, S.STATE_BADGE_MERGED):
        return PRState.MERGED, flags
    if await _text_visible(page, S.STATE_BADGE_CLOSED):
        return PRState.CLOSED, flags

    # 3: draft.
    if await _text_visible(page, S.DRAFT_BADGE_TEXT):
        return PRState.DRAFT, flags

    # 4: locked.
    if await _text_visible(page, S.LOCKED_NOTICE_TEXT):
        return PRState.LOCKED, flags

    # 5: authored by me?
    if me:
        author = await PRPage(page).pr_author_login()
        if author and author == me:
            return PRState.SELF_AUTHORED, flags

    # 6: merge conflict.
    if await _text_visible(page, S.CONFLICT_NOTICE_TEXT):
        return PRState.CONFLICT, flags

    # 7-8: required-statuses widget. Distinguish failing from pending.
    if await _text_visible(page, S.REQUIRED_STATUS_TEXT):
        # "Merge when ready" present → pending; otherwise treat as failing.
        if await page.get_by_role("button", name=S.MERGE_WHEN_READY_NAME).count() > 0:
            return PRState.REQUIRED_PENDING, flags
        return PRState.REQUIRED_FAILING, flags

    # 9: already-approved-by-me flag (combines with OPEN_*).
    if me and await _approved_by(page, me):
        flags.add(StateFlag.ALREADY_APPROVED)

    # 10-11: default — merge button enabled vs not.
    pr_page = PRPage(page)
    btn = pr_page.merge_button()
    if await btn.count() > 0 and await btn.is_enabled():
        return PRState.OPEN_MERGEABLE, flags
    return PRState.OPEN_APPROVABLE, flags


async def _text_visible(page: Page, pattern) -> bool:
    locator = page.get_by_text(pattern)
    return await locator.count() > 0


async def _approved_by(page: Page, login: str) -> bool:
    panel = page.locator("#reviewers-panel")
    if await panel.count() == 0:
        return False
    text = await panel.first.text_content() or ""
    return login in text and "approved these changes" in text.lower()
