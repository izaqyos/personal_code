"""Tests for models.py."""

from __future__ import annotations

from collections.abc import Callable

import pytest
from pydantic import ValidationError

from bug_triage.models import (
    Bug,
    Candidate,
    KnownIssueHit,
    LabeledBug,
    PipelineResult,
    Prediction,
    SimilarBug,
    Tier1Result,
    TierTrace,
    TriageDecision,
    TriageSuggestion,
)


def test_bug_text_joins_and_strips() -> None:
    assert Bug(id="1", title="T", description="D", logs="L").text() == "T\nD\nL"
    assert Bug(id="1", title="T", description="D").text() == "T\nD"


def test_labeled_bug_defaults_and_severity() -> None:
    lb = LabeledBug(
        id="1", title="t", description="d", component="c", team="x", assignee="a", severity="high"
    )
    assert lb.duplicate_of is None and lb.known_issue is None and lb.logs == ""
    with pytest.raises(ValidationError):
        LabeledBug(
            id="1",
            title="t",
            description="d",
            component="c",
            team="x",
            assignee="a",
            severity="urgent",
        )  # type: ignore[arg-type]


@pytest.mark.parametrize("score", [-0.01, 1.01])
def test_scores_rejected_out_of_bounds(score: float) -> None:
    with pytest.raises(ValidationError):
        Candidate(label="a", score=score)
    with pytest.raises(ValidationError):
        KnownIssueHit(id="KI-1", title="t", score=score)
    with pytest.raises(ValidationError):
        SimilarBug(bug_id="b", title="t", score=score, component="c", assignee="a")


@pytest.mark.parametrize("conf", [0.0, 0.5, 1.0])
def test_confidence_bounds_accepted(
    conf: float, make_suggestion: Callable[..., TriageSuggestion]
) -> None:
    assert make_suggestion(confidence=conf).confidence == conf


@pytest.mark.parametrize("conf", [-0.1, 1.5])
def test_confidence_rejected(conf: float, make_suggestion: Callable[..., TriageSuggestion]) -> None:
    with pytest.raises(ValidationError):
        make_suggestion(confidence=conf)


def test_tier1_helpers(make_tier1_result: Callable[..., Tier1Result]) -> None:
    t1 = make_tier1_result(duplicate_of="BUG-1001", known_issue="KI-001")
    assert t1.top_component() == "auth-sso"
    assert t1.top_score() == 0.7
    assert t1.to_prediction() == Prediction(
        component="auth-sso",
        team="Identity",
        assignee="Tobias Wren",
        duplicate_of="BUG-1001",
        known_issue="KI-001",
    )


def test_tier1_empty_candidates(make_tier1_result: Callable[..., Tier1Result]) -> None:
    t1 = make_tier1_result(component_candidates=[])
    with pytest.raises(ValueError):
        t1.top_component()
    with pytest.raises(ValueError):
        t1.top_score()


def test_decision_and_pipeline_result(make_suggestion: Callable[..., TriageSuggestion]) -> None:
    s = make_suggestion()
    d = TriageDecision(**s.model_dump(), source="judge", escalated=False)
    assert d.final_error is None
    trace = TierTrace(
        tier="judge",
        prediction=Prediction(**s.model_dump(include=set(Prediction.model_fields))),
        elapsed_ms=3.0,
    )
    assert trace.error is None
    res = PipelineResult(decision=d, trace=[trace])
    assert PipelineResult.model_validate_json(res.model_dump_json()) == res


def test_decision_source_literal(make_suggestion: Callable[..., TriageSuggestion]) -> None:
    with pytest.raises(ValidationError):
        TriageDecision(**make_suggestion().model_dump(), source="oracle", escalated=False)  # type: ignore[arg-type]
