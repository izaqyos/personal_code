import pytest

from github_approve_merge.logging_setup import RunContext
from github_approve_merge.pr_state import PRState
from github_approve_merge.runner import run_batch
from github_approve_merge.url import PRRef

from tests.unit.test_process_pr import FakeClient


PR1 = PRRef("o", "r", 1)
PR2 = PRRef("o", "r", 2)
PR3 = PRRef("o", "r", 3)
RUN_ID = "20260601-120000-aaaa"


def always_yes(decisions):
    return [True] * len(decisions)


def factory_from(spec: dict):
    """spec: {pr_number: FakeClient kwargs}. Returns a client_factory(pr, me)."""
    def _factory(pr: PRRef, me: str):
        return FakeClient(**spec[pr.number])
    return _factory


@pytest.mark.asyncio
async def test_batch_gate_called_once_with_all_decisions(tmp_path):
    prs = [PR1, PR2]
    gate_calls = []

    def gate(decisions):
        gate_calls.append(len(decisions))
        return [True] * len(decisions)

    spec = {
        1: dict(states=[(PRState.OPEN_MERGEABLE, set())], has_queue=False),  # -> done
        2: dict(states=[(PRState.OPEN_MERGEABLE, set())], has_queue=True),   # -> queued
    }
    summary = await run_batch(prs, client_factory=factory_from(spec), me="me",
                              approve=True, do_merge=True, method="merge",
                              gate=gate, logs_dir=tmp_path, run_id=RUN_ID)
    assert gate_calls == [2]
    assert summary["counts"]["queued"] + summary["counts"]["done"] == 2
    assert summary["exit_code"] == 0


@pytest.mark.asyncio
async def test_gate_decline_cancels_all(tmp_path):
    spec = {1: dict(states=[(PRState.OPEN_MERGEABLE, set())])}
    summary = await run_batch([PR1], client_factory=factory_from(spec), me="me",
                              approve=True, do_merge=True, method="merge",
                              gate=lambda d: [False] * len(d), logs_dir=tmp_path, run_id=RUN_ID)
    assert summary["prs"][0]["status"] == "cancelled"
    assert summary["exit_code"] == 1   # cancelled is warn-class


@pytest.mark.asyncio
async def test_failure_in_one_pr_does_not_stop_batch(tmp_path):
    from github_approve_merge.gh_client import GhNotFound
    spec = {
        1: dict(states=[], raise_on_fetch=GhNotFound("404")),
        2: dict(states=[(PRState.OPEN_MERGEABLE, set())], has_queue=False),
    }
    summary = await run_batch([PR1, PR2], client_factory=factory_from(spec), me="me",
                              approve=True, do_merge=True, method="merge",
                              gate=always_yes, logs_dir=tmp_path, run_id=RUN_ID)
    statuses = {p["pr"]: p["status"] for p in summary["prs"]}
    assert statuses["o/r#1"] == "failed-not-found"
    assert statuses["o/r#2"] == "done"
    assert summary["counts"] == {"done": 1, "queued": 0, "skipped": 0, "failed": 1}


@pytest.mark.asyncio
async def test_dry_run_reports_would_merge_no_gate(tmp_path):
    gate_calls = []
    spec = {1: dict(states=[(PRState.OPEN_MERGEABLE, set())])}
    summary = await run_batch([PR1], client_factory=factory_from(spec), me="me",
                              approve=True, do_merge=True, method="merge",
                              gate=lambda d: gate_calls.append(len(d)) or [True],
                              logs_dir=tmp_path, run_id=RUN_ID, dry_run=True)
    assert summary["prs"][0]["status"] == "would-merge"
    assert gate_calls == []   # dry-run never gates


@pytest.mark.asyncio
async def test_resume_skips_done_prs(tmp_path):
    run_dir = tmp_path / RUN_ID
    run_dir.mkdir()
    (run_dir / "state.jsonl").write_text(
        '{"ts":"...","pr":"o/r#1","status":"done","duration_ms":100}\n'
    )
    built: list[int] = []

    def factory(pr: PRRef, me: str):
        built.append(pr.number)
        return FakeClient(states=[(PRState.OPEN_MERGEABLE, set())])

    summary = await run_batch([PR1, PR2], client_factory=factory, me="me",
                              approve=True, do_merge=True, method="merge",
                              gate=always_yes, logs_dir=tmp_path, run_id=RUN_ID, resume=True)
    assert built == [2]   # PR1 already done, skipped
    assert summary["exit_code"] == 0


@pytest.mark.asyncio
async def test_interrupt_marks_failed_interrupted(tmp_path):
    spec = {
        1: dict(states=[(PRState.OPEN_MERGEABLE, set())]),
        2: dict(states=[], raise_on_fetch=KeyboardInterrupt()),
    }
    summary = await run_batch([PR1, PR2], client_factory=factory_from(spec), me="me",
                              approve=True, do_merge=True, method="merge",
                              gate=always_yes, logs_dir=tmp_path, run_id=RUN_ID)
    assert summary["exit_code"] == 130
    statuses = {p["pr"]: p["status"] for p in summary["prs"]}
    assert statuses["o/r#2"] == "failed-interrupted"


@pytest.mark.asyncio
async def test_redact_logs_hashes_pr(tmp_path):
    run_dir = tmp_path / RUN_ID
    ctx = RunContext(run_id=RUN_ID, run_dir=run_dir, redact_logs=True)
    spec = {1: dict(states=[(PRState.OPEN_MERGEABLE, set())])}
    summary = await run_batch([PR1], client_factory=factory_from(spec), me="me",
                              approve=True, do_merge=True, method="merge",
                              gate=always_yes, logs_dir=tmp_path, run_id=RUN_ID, ctx=ctx)
    state_lines = (run_dir / "state.jsonl").read_text()
    assert "o/r#1" not in state_lines
    assert "redacted-" in state_lines
    assert summary["prs"][0]["pr"].startswith("redacted-")
