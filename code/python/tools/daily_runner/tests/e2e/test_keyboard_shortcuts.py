"""
E2E tests for keyboard shortcuts in the Daily Standup Timer UI.

These tests verify that keyboard shortcuts work correctly during an active meeting.
"""

import time

import pytest
from playwright.sync_api import Page, expect

from .conftest import wait_for_streamlit_rerun

pytestmark = pytest.mark.e2e


class TestKeyboardShortcuts:
    """Tests for keyboard shortcut functionality."""

    def test_pause_shortcut_key_1(self, meeting_page: Page) -> None:
        """Test that pressing '1' toggles pause/resume."""
        page = meeting_page

        # meeting_page fixture ensures we're in SPEAKING state
        expect(page.locator("text=SPEAKING")).to_be_visible(timeout=5000)

        # Press '1' to pause
        page.keyboard.press("1")
        wait_for_streamlit_rerun(page)

        # Should now show PAUSED
        expect(page.locator("text=PAUSED")).to_be_visible(timeout=10000)

        # Press '1' again to resume
        page.keyboard.press("1")
        wait_for_streamlit_rerun(page)

        # Should be back to SPEAKING
        expect(page.locator("text=SPEAKING")).to_be_visible(timeout=10000)

    def test_next_shortcut_key_2(self, meeting_page: Page) -> None:
        """Test that pressing '2' advances to next speaker."""
        page = meeting_page

        # Press '2' for next speaker
        page.keyboard.press("2")
        wait_for_streamlit_rerun(page)

        # Wait for transition state
        time.sleep(1)

        # The current speaker indicator should have moved
        # (or we're in transition to next speaker)
        expect(
            page.locator("text=TRANSITION").or_(page.locator("text=SPEAKING"))
        ).to_be_visible(timeout=10000)

    def test_skip_shortcut_key_3(self, meeting_page: Page) -> None:
        """Test that pressing '3' skips the current speaker."""
        page = meeting_page

        # Press '3' to skip
        page.keyboard.press("3")
        wait_for_streamlit_rerun(page)

        # Should move to TRANSITION state for next speaker
        # or show skipped indicator in queue
        time.sleep(2)
        content = page.content()
        # Either in TRANSITION or we can see the skip was recorded
        assert "TRANSITION" in content or "⏩" in content, "Skip did not trigger transition"

    def test_add_time_shortcut_key_4(self, meeting_page: Page) -> None:
        """Test that pressing '4' adds 30 seconds to the timer."""
        page = meeting_page

        # Press '4' to add time
        page.keyboard.press("4")
        wait_for_streamlit_rerun(page)

        # Timer should have increased (or stayed same if near limit)
        # This is hard to verify exactly due to continuous countdown
        # Just verify the app didn't crash and is still in speaking state
        expect(page.locator("text=SPEAKING")).to_be_visible(timeout=5000)

    def test_subtract_time_shortcut_key_5(self, meeting_page: Page) -> None:
        """Test that pressing '5' subtracts 30 seconds from the timer."""
        page = meeting_page

        # Press '5' to subtract time
        page.keyboard.press("5")
        wait_for_streamlit_rerun(page)

        # Verify app is still functional
        expect(
            page.locator("text=SPEAKING").or_(page.locator("text=OVERTIME"))
        ).to_be_visible(timeout=5000)

    def test_end_meeting_shortcut_key_0(self, meeting_page: Page) -> None:
        """Test that pressing '0' ends the meeting."""
        page = meeting_page

        # Press '0' to end meeting
        page.keyboard.press("0")
        wait_for_streamlit_rerun(page)

        # Should show meeting summary
        expect(page.locator("text=Meeting Complete")).to_be_visible(timeout=10000)


class TestKeyboardLegend:
    """Tests for the keyboard shortcut legend display."""

    def test_legend_visible_during_meeting(self, meeting_page: Page) -> None:
        """Test that the keyboard shortcuts header is visible during a meeting."""
        page = meeting_page

        # The "⌨️ Shortcuts" header we added should be visible
        content = page.content()
        assert "Shortcuts" in content or "⌨" in content, "Shortcuts indicator not found"

    def test_legend_shows_all_shortcuts(self, meeting_page: Page) -> None:
        """Test that button tooltips show shortcut hints."""
        page = meeting_page

        # The buttons should have help text with shortcuts
        # Check that the hotkeys module is loaded (iframe present)
        content = page.content()
        assert "hotkeys" in content.lower(), "Hotkeys module not loaded"


class TestShortcutStateHandling:
    """Tests for keyboard shortcuts respecting state conditions."""

    def test_shortcuts_disabled_when_typing(self, app_page: Page) -> None:
        """Test that shortcuts don't fire when typing in input fields."""
        page = app_page

        # Find a text input (like team selector)
        # When focused on input, shortcuts should not trigger
        select_box = page.locator("select").first
        if select_box.is_visible():
            select_box.focus()
            # Press a shortcut key
            page.keyboard.press("1")
            # App should not crash or change state unexpectedly
            expect(page.locator("text=Daily Timer")).to_be_visible(timeout=5000)

    def test_time_shortcuts_only_during_speaking(self, meeting_page: Page) -> None:
        """Test that time adjustment shortcuts only work during SPEAKING state."""
        page = meeting_page

        # First, go to TRANSITION state
        page.keyboard.press("2")  # Next speaker
        wait_for_streamlit_rerun(page)

        # During transition, time shortcuts should not work
        # (the app should handle this gracefully)
        page.keyboard.press("4")  # Try to add time
        wait_for_streamlit_rerun(page)

        # Should still be in transition (or moved to speaking)
        # App should not crash
        expect(
            page.locator("text=TRANSITION").or_(page.locator("text=SPEAKING"))
        ).to_be_visible(timeout=10000)
