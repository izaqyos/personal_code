import json
from pathlib import Path

import pytest

from github_approve_merge.browser import StorageStateError, open_context


@pytest.mark.asyncio
async def test_open_context_with_valid_storage_state(tmp_path: Path):
    ss = tmp_path / "ss.json"
    ss.write_text(json.dumps({"cookies": [], "origins": []}))
    async with open_context(storage_state_path=ss, headless=True) as ctx:
        page = await ctx.new_page()
        await page.goto("about:blank")
        assert await page.title() == ""


@pytest.mark.asyncio
async def test_open_context_missing_storage_state_raises(tmp_path: Path):
    with pytest.raises(StorageStateError, match="not found"):
        async with open_context(storage_state_path=tmp_path / "missing.json", headless=True):
            pass


@pytest.mark.asyncio
async def test_open_context_unreadable_storage_state_raises(tmp_path: Path):
    bad = tmp_path / "ss.json"
    bad.write_text("not json")
    with pytest.raises(StorageStateError, match="parse"):
        async with open_context(storage_state_path=bad, headless=True):
            pass
