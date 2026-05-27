"""Re-snapshot the HTML fixtures from real GitHub pages.

Usage:
    python scripts/refresh_fixtures.py FIXTURE_NAME PR_URL [--no-sanitize]

Example:
    python scripts/refresh_fixtures.py pr_mergeable.html \\
        https://github.com/acme-org/widgets-service/pull/42

Sanitization (enabled by default):
    The captured HTML is scrubbed before being written to disk:

    * github.com/<owner>/... paths — the owner segment is replaced with
      ``acme-org`` so that organization names do not leak into committed
      fixtures.
    * ``<meta name="user-login" content="...">`` — content replaced with
      ``reviewer-bot``.
    * ``https://avatars.githubusercontent.com/...`` URLs — replaced with
      ``https://avatars.example.com/default.png``.
    * Email-looking strings — replaced with ``placeholder@example.com``.

    After sanitization a second-pass check verifies that none of the known
    org-internal substrings (defined in ``_KNOWN_ORG_PATTERNS``) survive.  If
    any do, the script exits non-zero and refuses to write the fixture.

    Pass ``--no-sanitize`` to skip both passes (NOT RECOMMENDED — fixtures may
    then contain org-internal names).

Run when fixture-based tests fail after a GitHub UI redesign — review the new
content and commit.
"""
from __future__ import annotations

import argparse
import asyncio
import re
import sys
from pathlib import Path

from playwright.async_api import async_playwright

from github_approve_merge.config import default_storage_state_path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "html"

_KNOWN_ORG_PATTERNS = [
    r"perimeter-81",
    r"perimeter81-",
    r"platform-global-domain",
    r"checkpoint\.com",
    r"p81-",
    r"saferx",
    r"saferdock",
    r"harmony-sase",
    r"Check Point",
    r"CheckPoint",
]


def sanitize_html(html: str) -> str:
    """Apply best-effort PII/org-name redaction to captured GitHub HTML.

    - github.com/<owner>/... → github.com/acme-org/... (owner replaced regardless)
    - meta[name=user-login] content → reviewer-bot
    - avatars.githubusercontent.com URLs → placeholder
    - email-looking strings (<word>@<word>.<tld>) → placeholder@example.com
    """
    # github.com URLs: replace owner segment.
    html = re.sub(
        r"(https?://github\.com/)[A-Za-z0-9_.-]+(/)",
        r"\1acme-org\2",
        html,
    )
    # user-login meta tag.
    html = re.sub(
        r'(<meta\s+name="user-login"\s+content=")[^"]*(")',
        r"\1reviewer-bot\2",
        html,
    )
    # avatar URLs.
    html = re.sub(
        r"https?://avatars\.githubusercontent\.com/[^\"'\s]+",
        "https://avatars.example.com/default.png",
        html,
    )
    # email-looking text.
    html = re.sub(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        "placeholder@example.com",
        html,
    )
    return html


def assert_no_known_leaks(html: str, source_label: str = "output") -> None:
    """Raise if any known org-leak pattern survived sanitization."""
    leaks: list[tuple[str, int]] = []
    for pattern in _KNOWN_ORG_PATTERNS:
        for m in re.finditer(pattern, html):
            line_no = html.count("\n", 0, m.start()) + 1
            leaks.append((pattern, line_no))
    if leaks:
        msg = f"\nERROR: sanitization left these patterns in the {source_label}:\n"
        for pattern, line_no in leaks:
            msg += f"  - {pattern!r} at line {line_no}\n"
        msg += "Refusing to write fixture. Use --no-sanitize to override (NOT RECOMMENDED), or report the unhandled pattern.\n"
        raise RuntimeError(msg)


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("fixture_name", help="must end in .html")
    p.add_argument("pr_url", help="github.com PR URL to capture")
    p.add_argument(
        "--no-sanitize",
        action="store_true",
        help="Disable sanitization (NOT RECOMMENDED — fixtures may contain org-internal names)",
    )
    return p.parse_args(argv)


async def main() -> int:
    args = parse_args()
    args.sanitize = not args.no_sanitize
    name = args.fixture_name
    url = args.pr_url
    target = FIXTURES_DIR / name
    if not name.endswith(".html"):
        print("fixture name must end with .html", file=sys.stderr)
        return 2

    storage_state = default_storage_state_path()
    if not storage_state.exists():
        print(
            f"missing storage_state at {storage_state}. Run `gh-approve-merge auth login`.",
            file=sys.stderr,
        )
        return 2

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(storage_state=str(storage_state))
        page = await ctx.new_page()
        await page.goto(url, wait_until="networkidle")
        html = await page.content()
        if args.sanitize:
            html = sanitize_html(html)
            assert_no_known_leaks(html, source_label=f"fixture {name}")
        target.write_text(html)
        print(f"wrote {target} ({len(html)} bytes)")
        await browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
