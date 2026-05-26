import os
from pathlib import Path

import pytest
import pytest_asyncio
from playwright.async_api import Browser, async_playwright


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "html"


def pytest_collection_modifyitems(config, items):
    if os.environ.get("PYTEST_LIVE") == "1":
        return
    skip_live = pytest.mark.skip(reason="PYTEST_LIVE=1 not set")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)


@pytest_asyncio.fixture(scope="session")
async def browser() -> Browser:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        yield browser
        await browser.close()


@pytest_asyncio.fixture
async def page(browser: Browser):
    ctx = await browser.new_context()
    page = await ctx.new_page()
    yield page
    await ctx.close()


@pytest.fixture
def fixture_url():
    """Return a callable that builds a `file://` URL for a fixture filename."""
    def _build(name: str) -> str:
        return (FIXTURES_DIR / name).as_uri()
    return _build
