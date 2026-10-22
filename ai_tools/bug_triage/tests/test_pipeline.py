"""Pipeline tests with stub tiers implementing the Protocols."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from bug_triage.models import Bug, Tier1Result, TriageSuggestion
from bug_triage.pipeline import Pipeline

Mk1 = Callable[..., Tier1Result]
MkS = Callable[..., TriageSuggestion]


class StubTier1:
    def __init__(self, result: Tier1Result) -> None:
        self.result = result

    def predict(self, bug: Bug) -> Tier1Result:
        return self.result

    def contact(self, component: str) -> str:
        return f"contact-of-{component}"


class StubJudge:
    def __init__(self, result: TriageSuggestion | Exception) -> None:
        self.result = result
        self.calls = 0

    def suggest(self, bug: Bug, t1: Tier1Result) -> TriageSuggestion:
        self.calls += 1
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


class StubFinal:
    def __init__(self, result: TriageSuggestion | Exception) -> None:
        self.result = result
        self.calls = 0

    def decide(self, bug: Bug, t1: Tier1Result, s: TriageSuggestion) -> TriageSuggestion:
        self.calls += 1
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


def test_tier1_only(sample_bug: Bug, make_tier1_result: Mk1) -> None:
    t1 = make_tier1_result()
    res = Pipeline(StubTier1(t1)).run(sample_bug)
    d = res.decision
    assert (d.source, d.severity, d.rationale, d.escalated) == (
        "tier1",
        "medium",
        "tier1 only",
        False,
    )
    assert d.confidence == t1.top_score() and d.component == "auth-sso"
    assert [t.tier for t in res.trace] == ["tier1"]
    assert res.trace[0].elapsed_ms == t1.elapsed_ms
    assert res.trace[0].prediction == t1.to_prediction()


def test_judge_no_escalation(sample_bug: Bug, make_tier1_result: Mk1, make_suggestion: MkS) -> None:
    final = StubFinal(make_suggestion())
    res = Pipeline(
        StubTier1(make_tier1_result()), StubJudge(make_suggestion(severity="high")), final
    ).run(sample_bug)
    assert res.decision.source == "judge" and not res.decision.escalated
    assert res.decision.severity == "high" and final.calls == 0
    assert [t.tier for t in res.trace] == ["tier1", "judge"]
    assert res.trace[1].elapsed_ms >= 0 and res.trace[1].error is None
    assert res.trace[1].prediction is not None and res.trace[1].prediction.component == "auth-sso"


@pytest.mark.parametrize(
    "override",
    [
        {"component": "web-ui"},
        {"confidence": 0.5},
    ],
)
def test_disagreement_escalates(
    sample_bug: Bug, make_tier1_result: Mk1, make_suggestion: MkS, override: dict[str, Any]
) -> None:
    final = StubFinal(make_suggestion(rationale="final says", severity="critical"))
    res = Pipeline(
        StubTier1(make_tier1_result()), StubJudge(make_suggestion(**override)), final
    ).run(sample_bug)
    d = res.decision
    assert final.calls == 1
    assert (d.source, d.escalated, d.final_error) == ("final", True, None)
    assert d.rationale == "final says" and d.severity == "critical"
    assert [t.tier for t in res.trace] == ["tier1", "judge", "final"]
    assert res.trace[2].prediction is not None


def test_confidence_at_threshold_does_not_escalate(
    sample_bug: Bug, make_tier1_result: Mk1, make_suggestion: MkS
) -> None:
    p = Pipeline(
        StubTier1(make_tier1_result()),
        StubJudge(make_suggestion(confidence=0.7)),
        StubFinal(make_suggestion()),
    )
    assert not p.should_escalate(make_tier1_result(), make_suggestion(confidence=0.7))
    assert p.run(sample_bug).decision.source == "judge"


def test_custom_threshold(make_tier1_result: Mk1, make_suggestion: MkS) -> None:
    p = Pipeline(
        StubTier1(make_tier1_result()), None, StubFinal(make_suggestion()), confidence_threshold=0.9
    )
    assert p.should_escalate(make_tier1_result(), make_suggestion(confidence=0.8))


def test_policy_always_and_never(
    sample_bug: Bug, make_tier1_result: Mk1, make_suggestion: MkS
) -> None:
    f1 = StubFinal(make_suggestion())
    always = Pipeline(
        StubTier1(make_tier1_result()), StubJudge(make_suggestion()), f1, policy="always"
    )
    assert always.run(sample_bug).decision.escalated and f1.calls == 1
    f2 = StubFinal(make_suggestion())
    never = Pipeline(
        StubTier1(make_tier1_result()),
        StubJudge(make_suggestion(component="web-ui", confidence=0.1)),
        f2,
        policy="never",
    )
    assert not never.run(sample_bug).decision.escalated and f2.calls == 0


def test_no_final_no_escalation(
    sample_bug: Bug, make_tier1_result: Mk1, make_suggestion: MkS
) -> None:
    p = Pipeline(
        StubTier1(make_tier1_result()),
        StubJudge(make_suggestion(component="web-ui")),
        None,
        policy="always",
    )
    assert not p.should_escalate(make_tier1_result(), make_suggestion())
    res = p.run(sample_bug)
    assert res.decision.source == "judge" and not res.decision.escalated


def test_judge_raises_fallback(
    sample_bug: Bug, make_tier1_result: Mk1, make_suggestion: MkS
) -> None:
    final = StubFinal(make_suggestion())
    t1 = make_tier1_result()
    res = Pipeline(
        StubTier1(t1), StubJudge(RuntimeError("ollama down")), final, policy="always"
    ).run(sample_bug)
    d = res.decision
    assert (d.source, d.severity, d.escalated) == ("tier1", "medium", False)
    assert d.rationale == "fallback: ollama down" and d.confidence == t1.top_score()
    assert final.calls == 0
    assert [t.tier for t in res.trace] == ["tier1", "judge"]
    assert res.trace[1].error == "ollama down" and res.trace[1].prediction is None


def test_final_raises_keeps_judge(
    sample_bug: Bug, make_tier1_result: Mk1, make_suggestion: MkS
) -> None:
    res = Pipeline(
        StubTier1(make_tier1_result()),
        StubJudge(make_suggestion(severity="low")),
        StubFinal(ValueError("claude down")),
        policy="always",
    ).run(sample_bug)
    d = res.decision
    assert (d.source, d.escalated, d.final_error) == ("judge", True, "claude down")
    assert d.severity == "low"
    assert res.trace[2].tier == "final" and res.trace[2].error == "claude down"
    assert res.trace[2].prediction is None


def test_links_come_from_tier1(
    sample_bug: Bug, make_tier1_result: Mk1, make_suggestion: MkS
) -> None:
    t1 = make_tier1_result(duplicate_of="BUG-1001", known_issue=None)
    judge_says = make_suggestion(duplicate_of=None, known_issue="KI-001")
    res = Pipeline(StubTier1(t1), StubJudge(judge_says)).run(sample_bug)
    d = res.decision
    assert (d.duplicate_of, d.known_issue) == ("BUG-1001", None)
    judge_trace = res.trace[1].prediction
    assert judge_trace is not None
    assert (judge_trace.duplicate_of, judge_trace.known_issue) == (None, "KI-001")


def test_links_from_tier1_after_final(
    sample_bug: Bug, make_tier1_result: Mk1, make_suggestion: MkS
) -> None:
    t1 = make_tier1_result(known_issue="KI-001")
    final = StubFinal(make_suggestion(duplicate_of="BUG-1001", known_issue=None))
    res = Pipeline(StubTier1(t1), StubJudge(make_suggestion()), final, policy="always").run(
        sample_bug
    )
    d = res.decision
    assert d.source == "final"
    assert (d.duplicate_of, d.known_issue) == (None, "KI-001")


def test_routes_to_team_with_contact_of_decided_component(
    sample_bug: Bug, make_tier1_result: Mk1, make_suggestion: MkS
) -> None:
    final = StubFinal(make_suggestion(component="web-ui", team="Experience", confidence=0.9))
    res = Pipeline(
        StubTier1(make_tier1_result()), StubJudge(make_suggestion(component="web-ui")), final
    ).run(sample_bug)
    assert res.decision.assignee == "contact-of-web-ui"
    judge_trace = res.trace[1].prediction
    assert judge_trace is not None and judge_trace.assignee == "contact-of-web-ui"


@pytest.mark.parametrize("bad", [-0.1, 1.5])
def test_invalid_threshold(make_tier1_result: Mk1, bad: float) -> None:
    with pytest.raises(ValueError):
        Pipeline(StubTier1(make_tier1_result()), confidence_threshold=bad)
