from pathlib import Path

import pytest

from github_approve_merge.logging_setup import RunContext
from github_approve_merge.screenshots import capture
from github_approve_merge.url import PRRef


@pytest.mark.asyncio
async def test_capture_checkpoint_writes_png_with_counter(page, fixture_url, tmp_path: Path):
    ctx = RunContext(run_id="20260526-143012-7af3", run_dir=tmp_path)
    pr = PRRef("acme-org", "widgets-service", 561)
    await page.goto(fixture_url("pr_mergeable.html"))

    p1 = await capture(page, ctx, pr, "after-load")
    p2 = await capture(page, ctx, pr, "before-merge-click")

    assert p1 == Path("screenshots/acme-org__widgets-service__561__01-after-load.png")
    assert p2 == Path("screenshots/acme-org__widgets-service__561__02-before-merge-click.png")
    assert (tmp_path / p1).exists()
    assert (tmp_path / p2).exists()


@pytest.mark.asyncio
async def test_capture_error_skips_counter(page, fixture_url, tmp_path: Path):
    ctx = RunContext(run_id="rid", run_dir=tmp_path)
    pr = PRRef("o", "r", 1)
    await page.goto(fixture_url("pr_conflict.html"))

    p = await capture(page, ctx, pr, "error-conflict-detected")
    assert p == Path("screenshots/o__r__1__error-conflict-detected.png")
    assert (tmp_path / p).exists()


@pytest.mark.asyncio
async def test_capture_never_raises_on_failure(monkeypatch, page, fixture_url, tmp_path: Path):
    ctx = RunContext(run_id="rid", run_dir=tmp_path)
    pr = PRRef("o", "r", 1)
    await page.goto(fixture_url("pr_mergeable.html"))

    async def boom(*_args, **_kwargs):
        raise RuntimeError("disk full")

    monkeypatch.setattr(page, "screenshot", boom)

    # Should swallow the error and return None instead of raising.
    result = await capture(page, ctx, pr, "after-load")
    assert result is None
