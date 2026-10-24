"""Tests for the evaluation harness (stub tier 1 / stub runner)."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from bug_triage.evaluate import EvalReport, TierMetrics, format_report, run_eval
from bug_triage.models import (
    Bug,
    Candidate,
    LabeledBug,
    PipelineResult,
    Prediction,
    Tier1Result,
    TierTrace,
    TriageDecision,
)

Make = Callable[..., Tier1Result]


def _lb(i: int, comp: str, who: str, dup: str | None = None, ki: str | None = None) -> LabeledBug:
    return LabeledBug(
        id=f"E{i}",
        title="t",
        description="d",
        component=comp,
        team="T-" + comp,
        assignee=who,
        severity="low",
        duplicate_of=dup,
        known_issue=ki,
    )


BUGS = [
    _lb(1, "a", "x"),
    _lb(2, "b", "y", dup="D1"),
    _lb(3, "c", "z", ki="K1"),
    _lb(4, "a", "x"),
]


class StubTier1:
    """Predicts from a script keyed by bug id."""

    def __init__(self, make: Make, script: dict[str, dict[str, object]]) -> None:
        self.make, self.script = make, script

    def predict(self, bug: Bug) -> Tier1Result:
        s = self.script[bug.id]
        return self.make(
            component_candidates=[Candidate(label=str(s["comp"]), score=0.9)],
            team=s["team"],
            assignee=s["who"],
            duplicate_of=s.get("dup"),
            known_issue=s.get("ki"),
            elapsed_ms=s["ms"],
        )


def _t1(make: Make) -> StubTier1:
    return StubTier1(
        make,
        {
            # correct everywhere
            "E1": dict(comp="a", team="T-a", who="x", ms=1.0),
            # comp right, assignee wrong, dup right
            "E2": dict(comp="b", team="T-b", who="WRONG", dup="D1", ms=2.0),
            # comp wrong, team wrong, ki missed
            "E3": dict(comp="a", team="T-a", who="x", ms=3.0),
            # all right but spurious dup and ki
            "E4": dict(comp="a", team="T-a", who="x", dup="D9", ki="K9", ms=4.0),
        },
    )


def test_tier1_only_metrics(make_tier1_result: Make) -> None:
    rep = run_eval(BUGS, tier1=_t1(make_tier1_result))
    assert rep.n == 4
    assert rep.escalation_rate == 0.0
    (m,) = rep.tiers
    assert m.tier == "tier1"
    assert m.n == 4
    assert m.acc_component == 0.75
    assert m.acc_team == 0.75
    assert m.acc_assignee == 0.5
    assert m.acc_duplicate == 0.75  # only E4 has a spurious dup
    assert m.acc_known_issue == 0.5
    assert m.error_rate == 0.25  # only E3 (comp wrong); E2's wrong assignee is not routing
    assert m.mean_ms == 2.5
    assert rep.final_decision == m


def test_dup_ki_none_counts_correct(make_tier1_result: Make) -> None:
    rep = run_eval(BUGS[:1], tier1=_t1(make_tier1_result))
    assert rep.tiers[0].acc_duplicate == 1.0
    assert rep.tiers[0].acc_known_issue == 1.0
    assert rep.tiers[0].error_rate == 0.0


def test_limit_and_empty(make_tier1_result: Make) -> None:
    t1 = _t1(make_tier1_result)
    rep = run_eval(BUGS, tier1=t1, limit=2)
    assert rep.n == 2
    assert rep.tiers[0].mean_ms == 1.5
    with pytest.raises(ValueError):
        run_eval([], tier1=t1)
    with pytest.raises(ValueError):
        run_eval(BUGS, tier1=t1, limit=0)


def _pred(comp: str, who: str, **kw: str | None) -> Prediction:
    return Prediction(component=comp, team="T-" + comp, assignee=who, **kw)


def _decision(comp: str, who: str, escalated: bool, source: str = "judge") -> TriageDecision:
    return TriageDecision(
        component=comp,
        team="T-" + comp,
        assignee=who,
        severity="low",
        confidence=0.5,
        rationale="r",
        source=source,  # type: ignore[arg-type]
        escalated=escalated,
    )


class StubRunner:
    def __init__(self, results: dict[str, PipelineResult]) -> None:
        self.results = results

    def run(self, bug: Bug) -> PipelineResult:
        return self.results[bug.id]


def test_runner_per_tier_metrics(make_tier1_result: Make) -> None:
    results = {
        # tier1 wrong, judge right, no escalation
        "E1": PipelineResult(
            decision=_decision("a", "x", False),
            trace=[
                TierTrace(tier="tier1", prediction=_pred("z", "x"), elapsed_ms=1.0),
                TierTrace(tier="judge", prediction=_pred("a", "x"), elapsed_ms=100.0),
            ],
        ),
        # judge failed (prediction None); no decision, left for a human
        "E2": PipelineResult(
            decision=None,
            needs_human="judge failed: boom",
            trace=[
                TierTrace(tier="tier1", prediction=_pred("q", "y"), elapsed_ms=3.0),
                TierTrace(tier="judge", prediction=None, elapsed_ms=50.0, error="boom"),
            ],
        ),
        # escalated to final, which fixes it
        "E3": PipelineResult(
            decision=_decision("c", "z", True, "final"),
            trace=[
                TierTrace(tier="tier1", prediction=_pred("c", "bad"), elapsed_ms=2.0),
                TierTrace(tier="judge", prediction=_pred("a", "z"), elapsed_ms=200.0),
                TierTrace(tier="final", prediction=_pred("c", "z"), elapsed_ms=1000.0),
            ],
        ),
    }
    bugs = [BUGS[0], BUGS[1], BUGS[2]]
    rep = run_eval(bugs, tier1=_t1(make_tier1_result), runner=StubRunner(results))
    assert [m.tier for m in rep.tiers] == ["tier1", "judge", "final"]
    t1, judge, final = rep.tiers
    assert (t1.n, judge.n, final.n) == (3, 2, 1)
    assert t1.error_rate == pytest.approx(2 / 3)  # z!=a ; q!=b ; E3 bad assignee only
    assert judge.error_rate == pytest.approx(0.5)  # E1 right, E3 comp wrong
    assert judge.mean_ms == 150.0
    assert final.error_rate == 0.0
    assert final.mean_ms == 1000.0
    d = rep.final_decision
    assert d.tier == "final"
    assert d.n == 2  # E2 has no automatic decision
    assert d.error_rate == 0.0
    assert d.mean_ms == pytest.approx((101.0 + 1202.0) / 2)
    assert rep.escalation_rate == pytest.approx(1 / 3)
    assert rep.human_rate == pytest.approx(1 / 3)
    assert "left for a human: 33.3%" in format_report(rep)


def test_runner_all_left_for_human(make_tier1_result: Make) -> None:
    res = PipelineResult(
        decision=None,
        needs_human="judge failed: boom",
        trace=[TierTrace(tier="tier1", prediction=_pred("a", "x"), elapsed_ms=1.0)],
    )
    rep = run_eval(BUGS[:1], tier1=_t1(make_tier1_result), runner=StubRunner({"E1": res}))
    assert rep.human_rate == 1.0
    assert (rep.final_decision.n, rep.final_decision.error_rate) == (0, 0.0)
    assert rep.final_decision.mean_ms == 0.0


def test_runner_tier_never_ran(make_tier1_result: Make) -> None:
    res = PipelineResult(
        decision=_decision("a", "x", False, "tier1"),
        trace=[TierTrace(tier="tier1", prediction=_pred("a", "x"), elapsed_ms=1.0)],
    )
    rep = run_eval(BUGS[:1], tier1=_t1(make_tier1_result), runner=StubRunner({"E1": res}))
    assert [m.tier for m in rep.tiers] == ["tier1"]


def _m(tier: str, err: float) -> TierMetrics:
    return TierMetrics(
        tier=tier,  # type: ignore[arg-type]
        n=40,
        acc_component=0.9,
        acc_team=0.95,
        acc_assignee=0.8,
        acc_duplicate=0.7,
        acc_known_issue=0.6,
        error_rate=err,
        mean_ms=12.34,
    )


def test_format_report_full() -> None:
    rep = EvalReport(
        tiers=[_m("tier1", 0.275), _m("judge", 0.125)],
        final_decision=_m("final", 0.05),
        escalation_rate=0.25,
        n=40,
    )
    text = format_report(rep)
    lines = text.splitlines()
    for col in ("tier", "n", "comp", "team", "assignee", "dup", "KI", "error", "ms"):
        assert col in lines[0]
    assert "90.0%" in text
    assert "12.3" in text
    assert "escalation rate: 25.0%" in text
    assert "left for a human" not in text
    assert lines[-1] == "error: tier1 27.5% → judge 12.5% → final 5.0%"


def test_format_report_tier1_only(make_tier1_result: Make) -> None:
    rep = run_eval(BUGS, tier1=_t1(make_tier1_result))
    assert format_report(rep).splitlines()[-1] == "error: tier1 25.0% → final 25.0%"
