"""CLI tests: build_pipeline and the evaluate functions are faked."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from bug_triage import cli
from bug_triage.kb import KnowledgeBase
from bug_triage.models import (
    Bug,
    PipelineResult,
    TierTrace,
    TriageDecision,
)


def _result(bug: Bug) -> PipelineResult:
    return PipelineResult(
        decision=TriageDecision(
            component="auth-sso",
            team="Identity",
            assignee="Tobias Wren",
            severity="high",
            confidence=0.8,
            rationale=f"for {bug.id}",
            source="judge",
            escalated=False,
        ),
        trace=[TierTrace(tier="tier1", prediction=None, elapsed_ms=1.0)],
    )


class FakePipeline:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.bugs: list[Bug] = []

    def run(self, bug: Bug) -> PipelineResult:
        if self.error:
            raise self.error
        self.bugs.append(bug)
        return _result(bug)


@pytest.fixture
def fake_build(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    state: dict[str, Any] = {"calls": [], "pipeline": FakePipeline(), "tier1": object()}

    def build(judge: str, final: str, model: str) -> tuple[Any, Any, Any]:
        state["calls"].append((judge, final, model))
        return state["pipeline"], None, state["tier1"]

    monkeypatch.setattr(cli, "build_pipeline", build)
    return state


def test_triage_flags(fake_build: dict[str, Any], capsys: pytest.CaptureFixture[str]) -> None:
    rc = cli.main(["triage", "--title", "T", "--desc", "D", "--logs", "L", "--judge", "none"])
    assert rc == 0
    out = PipelineResult.model_validate_json(capsys.readouterr().out)
    assert out.decision.rationale == "for CLI-1"
    assert fake_build["calls"] == [("none", "on-disagreement", "gemma4:12b")]
    assert fake_build["pipeline"].bugs[0] == Bug(id="CLI-1", title="T", description="D", logs="L")


def test_triage_options_passed(fake_build: dict[str, Any]) -> None:
    cli.main(["triage", "--title", "T", "--desc", "D", "--final", "always", "--model", "m"])
    assert fake_build["calls"] == [("ollama", "always", "m")]


def test_triage_file(
    fake_build: dict[str, Any], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    f = tmp_path / "bug.json"
    f.write_text(json.dumps({"id": "X-9", "title": "t", "description": "d"}))
    assert cli.main(["triage", "--file", str(f)]) == 0
    assert "for X-9" in capsys.readouterr().out


@pytest.mark.parametrize(
    "argv", [[], ["triage"], ["triage", "--title", "T"], ["bogus"], ["eval", "--tiers", "9"]]
)
def test_usage_errors(fake_build: dict[str, Any], argv: list[str]) -> None:
    assert cli.main(argv) == 2


def test_help_is_ok(fake_build: dict[str, Any]) -> None:
    assert cli.main(["--help"]) == 0


def test_bad_json_file(
    fake_build: dict[str, Any], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    f = tmp_path / "bad.json"
    f.write_text("{nope")
    assert cli.main(["triage", "--file", str(f)]) == 1
    assert "invalid JSON" in capsys.readouterr().err


def test_invalid_bug_and_missing_file(fake_build: dict[str, Any], tmp_path: Path) -> None:
    f = tmp_path / "b.json"
    f.write_text(json.dumps({"id": "x"}))
    assert cli.main(["triage", "--file", str(f)]) == 1
    assert cli.main(["triage", "--file", str(tmp_path / "missing.json")]) == 1


def test_runtime_error(fake_build: dict[str, Any], capsys: pytest.CaptureFixture[str]) -> None:
    fake_build["pipeline"] = FakePipeline(RuntimeError("kaboom"))
    assert cli.main(["triage", "--title", "T", "--desc", "D"]) == 1
    err = capsys.readouterr().err
    assert err.strip() == "error: kaboom"


@pytest.fixture
def fake_eval(monkeypatch: pytest.MonkeyPatch, kb: KnowledgeBase) -> dict[str, Any]:
    import bug_triage.evaluate as ev
    import bug_triage.kb as kbmod

    bugs = kb_eval = kbmod.load_eval()[:7]
    state: dict[str, Any] = {"bugs": bugs, "kb_eval": kb_eval}

    def run_eval(b: Any, *, tier1: Any, runner: Any = None, limit: Any = None) -> str:
        state["args"] = (b, tier1, runner, limit)
        if runner is not None:
            for bug in b[: limit or len(b)]:
                runner.run(bug)
        return "REPORT"

    monkeypatch.setattr(ev, "run_eval", run_eval)
    monkeypatch.setattr(ev, "format_report", lambda r: f"formatted {r}")
    monkeypatch.setattr(kbmod, "load_eval", lambda *a, **k: bugs)
    return state


def test_eval_tier1(
    fake_build: dict[str, Any], fake_eval: dict[str, Any], capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main(["eval"]) == 0
    assert capsys.readouterr().out.strip() == "formatted REPORT"
    assert fake_build["calls"] == [("none", "never", "gemma4:12b")]
    _, tier1, runner, limit = fake_eval["args"]
    assert tier1 is fake_build["tier1"] and runner is None and limit is None


def test_eval_tier2(
    fake_build: dict[str, Any], fake_eval: dict[str, Any], capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main(["eval", "--tiers", "2", "--judge", "gemini", "--final", "always"]) == 0
    assert fake_build["calls"] == [("gemini", "never", "gemma4:12b")]
    assert fake_eval["args"][2] is not None
    err = capsys.readouterr().err
    assert "eval: 5/7 bugs" in err and "eval: 7/7 bugs" in err and "eval: 1/7" not in err


def test_eval_tier3_limit(
    fake_build: dict[str, Any], fake_eval: dict[str, Any], capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main(["eval", "--tiers", "3", "--limit", "3", "--model", "m"]) == 0
    assert fake_build["calls"] == [("ollama", "on-disagreement", "m")]
    assert fake_eval["args"][3] == 3
    assert fake_build["pipeline"].bugs == fake_eval["bugs"][:3]
    assert "eval: 3/3 bugs" in capsys.readouterr().err


def test_build_pipeline_real_wiring(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from bug_triage.final_claude import FinalTriager
    from bug_triage.judge import Judge

    p, kb, t1 = cli.build_pipeline("none", "never", "m")
    assert p.judge is None and p.final is None and isinstance(kb, KnowledgeBase)
    assert p.tier1 is t1
    p, _, _ = cli.build_pipeline("ollama", "always", "gemma-x")
    assert isinstance(p.judge, Judge) and isinstance(p.final, FinalTriager)
    assert p.policy == "always"


def test_build_pipeline_gemini(monkeypatch: pytest.MonkeyPatch) -> None:
    import bug_triage.llm.gemini_client as gc
    from bug_triage.judge import Judge

    class FakeGemini:
        name = "gemini"

    monkeypatch.setattr(gc, "GeminiClient", FakeGemini)
    p, _, _ = cli.build_pipeline("gemini", "never", "m")
    assert isinstance(p.judge, Judge) and p.final is None
