"""
Pytest fixtures for E2E tests.

This module provides fixtures for running Streamlit app tests with Playwright.
"""

import contextlib
import subprocess
import time
from collections.abc import Generator
from pathlib import Path

import pytest
from playwright.sync_api import Page

# Default test timeout
DEFAULT_TIMEOUT = 30000  # 30 seconds

# Streamlit app settings
STREAMLIT_PORT = 8502  # Use non-default port to avoid conflicts
STREAMLIT_URL = f"http://localhost:{STREAMLIT_PORT}"

# Project root directory (where pyproject.toml is)
PROJECT_ROOT = Path(__file__).parent.parent.parent


@pytest.fixture(scope="session")
def streamlit_app() -> Generator[str, None, None]:
    """
    Start the Streamlit app for testing.

    Yields the base URL of the running app.
    """
    # Start Streamlit in a subprocess from project root
    process = subprocess.Popen(
        [
            "streamlit",
            "run",
            "src/ui/app.py",
            "--server.port",
            str(STREAMLIT_PORT),
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=PROJECT_ROOT,  # Run from project root so teams/ is found
    )

    # Wait for the app to start
    max_wait = 30
    started = False
    for _ in range(max_wait):
        try:
            import urllib.request

            urllib.request.urlopen(STREAMLIT_URL, timeout=1)
            started = True
            break
        except Exception:
            time.sleep(1)

    if not started:
        process.terminate()
        raise RuntimeError("Streamlit app failed to start")

    yield STREAMLIT_URL

    # Cleanup: terminate the process
    process.terminate()
    process.wait(timeout=5)


@pytest.fixture
def app_page(page: Page, streamlit_app: str) -> Page:
    """
    Navigate to the Streamlit app and wait for it to load.

    Args:
        page: Playwright page object.
        streamlit_app: Base URL of the Streamlit app.

    Returns:
        The page object navigated to the app.
    """
    # Navigate and wait for network to settle
    page.goto(streamlit_app, wait_until="networkidle")
    # Extra wait for Streamlit's React app to render
    time.sleep(3)
    # Wait for Streamlit to fully load
    page.wait_for_selector("text=Daily Timer", timeout=DEFAULT_TIMEOUT)
    return page


@pytest.fixture
def meeting_page(app_page: Page) -> Page:
    """
    Start a meeting and return the page ready for testing.

    Args:
        app_page: Page with app loaded.

    Returns:
        Page with an active meeting.
    """
    # Select a team if available
    try:
        # Click the Start Meeting button
        app_page.click("button:has-text('Start Meeting')", timeout=10000)
        time.sleep(2)

        # Wait for meeting to start (TRANSITION state first)
        for _ in range(15):
            content = app_page.content()
            if any(state in content for state in ["SPEAKING", "TRANSITION", "PAUSED"]):
                break
            time.sleep(1)
        else:
            raise TimeoutError("Meeting state not found")

        # If in TRANSITION, click "Start Now" to skip to SPEAKING
        if "TRANSITION" in app_page.content():
            try:
                app_page.click("button:has-text('🎤')", timeout=3000)
                time.sleep(2)
            except Exception:
                pass  # Button might not be visible, wait for auto-transition

        # Wait for SPEAKING state
        for _ in range(35):  # 30s transition + buffer
            if "SPEAKING" in app_page.content():
                break
            time.sleep(1)
        else:
            raise TimeoutError("SPEAKING state not reached")

    except Exception as e:
        # If no teams available or other error, skip
        pytest.skip(f"Could not start meeting: {e}")

    return app_page


def wait_for_streamlit_rerun(page: Page, timeout: int = 5000) -> None:
    """
    Wait for Streamlit to complete a rerun after an action.

    Args:
        page: Playwright page object.
        timeout: Maximum wait time in milliseconds.
    """
    # Streamlit shows a "Running" indicator during reruns
    # Wait for it to disappear
    time.sleep(0.5)  # Brief pause for rerun to start
    with contextlib.suppress(Exception):
        # Widget may not appear for quick reruns
        page.wait_for_selector(
            "[data-testid='stStatusWidget']",
            state="hidden",
            timeout=timeout,
        )
