"""Re-snapshot the HTML fixtures from real GitHub pages.

Usage:
    python scripts/refresh_fixtures.py FIXTURE_NAME PR_URL

Example:
    python scripts/refresh_fixtures.py pr_mergeable.html \\
        https://github.com/sandbox-org/sandbox-repo/pull/42

This uses your saved storage_state, navigates to PR_URL, waits for the page to
settle, and writes `page.content()` to tests/fixtures/html/FIXTURE_NAME.

Run when fixture-based tests fail after a GitHub UI redesign — review the new
content, sanitise PII (commit hashes, real avatars), and commit.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright

from github_approve_merge.config import default_storage_state_path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "html"


async def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    name, url = sys.argv[1], sys.argv[2]
    target = FIXTURES_DIR / name
    if not name.endswith(".html"):
        print("fixture name must end with .html", file=sys.stderr)
        return 2

    storage_state = default_storage_state_path()
    if not storage_state.exists():
        print(f"missing storage_state at {storage_state}. Run `gh-approve-merge auth login`.",
              file=sys.stderr)
        return 2

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(storage_state=str(storage_state))
        page = await ctx.new_page()
        await page.goto(url, wait_until="networkidle")
        html = await page.content()
        target.write_text(html)
        print(f"wrote {target} ({len(html)} bytes)")
        await browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
