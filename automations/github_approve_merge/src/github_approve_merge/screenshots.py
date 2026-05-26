from __future__ import annotations

import logging
from pathlib import Path

from playwright.async_api import Page

from github_approve_merge.logging_setup import RunContext
from github_approve_merge.url import PRRef

_log = logging.getLogger("gam")


async def capture(page: Page, ctx: RunContext, pr: PRRef, label: str) -> Path | None:
    """Take a full-page screenshot and write it under `ctx.run_dir/screenshots/`.

    Filename: `<owner>__<repo>__<pr_num>__<NN>-<label>.png` for checkpoint labels;
    `<owner>__<repo>__<pr_num>__<label>.png` (no counter) when label starts with
    `error-`. Returns the path RELATIVE to ctx.run_dir, so log events stay portable.

    Never raises on failure — a broken screenshot must not abort the per-PR flow.
    """
    slug = _slug_for(pr, label, ctx)
    rel = Path("screenshots") / f"{slug}.png"
    full = ctx.run_dir / rel
    full.parent.mkdir(parents=True, exist_ok=True)
    try:
        await page.screenshot(path=str(full), full_page=True)
    except Exception as e:  # pragma: no cover - defensive, exercised by monkeypatch test
        _log.warning(
            "screenshot failed for %s (%s): %s",
            pr, label, e,
            extra={"pr": str(pr), "step": label},
        )
        return None
    return rel


def _slug_for(pr: PRRef, label: str, ctx: RunContext) -> str:
    base = f"{pr.owner}__{pr.repo}__{pr.number}"
    if label.startswith("error-"):
        return f"{base}__{label}"
    counter_key = f"{ctx.run_id}/{pr}"
    n = ctx.screenshot_counters.get(counter_key, 0) + 1
    ctx.screenshot_counters[counter_key] = n
    return f"{base}__{n:02d}-{label}"
