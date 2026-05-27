from __future__ import annotations

import contextlib
import json
from pathlib import Path
from typing import AsyncIterator

from playwright.async_api import BrowserContext, async_playwright


class StorageStateError(RuntimeError):
    """Raised when storage_state.json is missing or unparseable."""


@contextlib.asynccontextmanager
async def open_context(
    *,
    storage_state_path: Path,
    headless: bool,
    timeout_seconds: float = 30.0,
) -> AsyncIterator[BrowserContext]:
    """Launch chromium + open a context loaded from storage_state_path.

    Raises StorageStateError if the storage_state.json file is missing or
    unparseable. Sets a default per-step timeout on the context.
    """
    if not storage_state_path.exists():
        raise StorageStateError(
            f"storage_state not found at {storage_state_path}. "
            "Run `gh-approve-merge auth login` first."
        )
    try:
        # Pre-validate the JSON so Playwright doesn't crash mid-launch with a vague error.
        json.loads(storage_state_path.read_text())
    except json.JSONDecodeError as e:
        raise StorageStateError(
            f"could not parse storage_state at {storage_state_path}: {e}"
        ) from e

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        try:
            ctx = await browser.new_context(storage_state=str(storage_state_path))
            ctx.set_default_timeout(timeout_seconds * 1000)
            try:
                yield ctx
            finally:
                await ctx.close()
        finally:
            await browser.close()
