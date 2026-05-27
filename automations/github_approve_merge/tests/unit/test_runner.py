import json
from pathlib import Path

import pytest

from github_approve_merge.actions import ProcessResult
from github_approve_merge.runner import Runner
from github_approve_merge.url import PRRef


PR1 = PRRef("o", "r", 1)
PR2 = PRRef("o", "r", 2)
PR3 = PRRef("o", "r", 3)


def _make_runner(tmp_path: Path, results: dict[str, ProcessResult]) -> Runner:
    """Build a Runner whose process_pr returns the canned result for each PR."""
    async def fake_process(ctx, pr, **_kwargs):
        return results[str(pr)]
    return Runner(
        logs_dir=tmp_path,
        run_id="20260526-143012-aaaa",
        process_pr_fn=fake_process,
    )


def _read_state(run_dir: Path) -> list[dict]:
    return [json.loads(l) for l in (run_dir / "state.jsonl").read_text().splitlines() if l]


def _read_summary(run_dir: Path) -> dict:
    return json.loads((run_dir / "summary.json").read_text())


@pytest.mark.asyncio
async def test_happy_path(tmp_path: Path):
    runner = _make_runner(tmp_path, {
        "o/r#1": ProcessResult(status="done", duration_ms=100),
        "o/r#2": ProcessResult(status="done", duration_ms=200),
    })
    exit_code = await runner.execute([PR1, PR2])
    assert exit_code == 0
    run_dir = tmp_path / "20260526-143012-aaaa"
    transitions = _read_state(run_dir)
    # 2 queued + 2 in_progress + 2 done = 6 lines
    statuses = [t["status"] for t in transitions]
    assert statuses == ["queued", "queued", "in_progress", "done", "in_progress", "done"]
    summary = _read_summary(run_dir)
    assert summary["exit_code"] == 0
    assert summary["counts"] == {"done": 2, "skipped": 0, "failed": 0}


@pytest.mark.asyncio
async def test_failure_in_one_pr_does_not_stop_batch(tmp_path: Path):
    runner = _make_runner(tmp_path, {
        "o/r#1": ProcessResult(status="failed-conflict"),
        "o/r#2": ProcessResult(status="done"),
    })
    exit_code = await runner.execute([PR1, PR2])
    assert exit_code == 1
    run_dir = tmp_path / "20260526-143012-aaaa"
    summary = _read_summary(run_dir)
    assert summary["counts"] == {"done": 1, "skipped": 0, "failed": 1}


@pytest.mark.asyncio
async def test_resume_skips_done_prs(tmp_path: Path):
    run_dir = tmp_path / "20260526-143012-aaaa"
    run_dir.mkdir()
    (run_dir / "state.jsonl").write_text(
        '{"ts":"...","pr":"o/r#1","status":"queued"}\n'
        '{"ts":"...","pr":"o/r#1","status":"in_progress"}\n'
        '{"ts":"...","pr":"o/r#1","status":"done","duration_ms":100}\n'
        '{"ts":"...","pr":"o/r#2","status":"queued"}\n'
    )

    called: list[str] = []

    async def fake_process(ctx, pr, **_kwargs):
        called.append(str(pr))
        return ProcessResult(status="done")

    runner = Runner(
        logs_dir=tmp_path,
        run_id="20260526-143012-aaaa",
        process_pr_fn=fake_process,
        resume=True,
    )
    exit_code = await runner.execute([PR1, PR2])
    assert exit_code == 0
    assert called == ["o/r#2"]   # PR1 was skipped (already done)


@pytest.mark.asyncio
async def test_warn_class_skip_yields_exit_1(tmp_path: Path):
    runner = _make_runner(tmp_path, {
        "o/r#1": ProcessResult(status="skipped-closed"),
    })
    exit_code = await runner.execute([PR1])
    assert exit_code == 1


@pytest.mark.asyncio
async def test_success_skip_yields_exit_0(tmp_path: Path):
    runner = _make_runner(tmp_path, {
        "o/r#1": ProcessResult(status="skipped-merged"),
    })
    exit_code = await runner.execute([PR1])
    assert exit_code == 0


@pytest.mark.asyncio
async def test_signal_marks_current_as_interrupted(tmp_path: Path):
    """If process_pr raises CancelledError mid-flight, the in-progress PR ends `failed-interrupted`."""
    import asyncio

    async def fake_process(ctx, pr, **_kwargs):
        if str(pr) == "o/r#2":
            raise asyncio.CancelledError()
        return ProcessResult(status="done")

    runner = Runner(
        logs_dir=tmp_path,
        run_id="20260526-143012-aaaa",
        process_pr_fn=fake_process,
    )
    exit_code = await runner.execute([PR1, PR2, PR3])
    assert exit_code == 130

    run_dir = tmp_path / "20260526-143012-aaaa"
    transitions = _read_state(run_dir)
    pr2_terminal = [t for t in transitions if t["pr"] == "o/r#2" and t["status"].startswith("failed")]
    assert pr2_terminal and pr2_terminal[-1]["status"] == "failed-interrupted"


@pytest.mark.asyncio
async def test_redact_logs_hashes_pr_in_state_jsonl(tmp_path: Path):
    """With redact_logs=True, state.jsonl and summary.json contain hashes, not raw slugs."""
    from github_approve_merge.logging_setup import RunContext

    ctx = RunContext(
        run_id="20260526-143012-aaaa",
        run_dir=tmp_path / "20260526-143012-aaaa",
        redact_logs=True,
    )

    async def fake_process(_ctx, pr, **_kwargs):
        return ProcessResult(status="done")

    runner = Runner(
        logs_dir=tmp_path,
        run_id="20260526-143012-aaaa",
        process_pr_fn=fake_process,
        ctx=ctx,
    )
    exit_code = await runner.execute([PR1])
    assert exit_code == 0

    state_lines = (tmp_path / "20260526-143012-aaaa" / "state.jsonl").read_text()
    summary = json.loads((tmp_path / "20260526-143012-aaaa" / "summary.json").read_text())
    # No raw slug anywhere.
    assert "o/r#1" not in state_lines
    assert "o/r#1" not in (tmp_path / "20260526-143012-aaaa" / "summary.json").read_text()
    assert "redacted-" in state_lines
    assert summary["prs"][0]["pr"].startswith("redacted-")
