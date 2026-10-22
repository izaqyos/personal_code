"""Three-tier orchestration: Tier 1 always, judge optional, final tier by escalation policy."""

from __future__ import annotations

import logging
import time
from typing import Protocol

from bug_triage.models import (
    Bug,
    FinalPolicy,
    PipelineResult,
    Prediction,
    Tier1Result,
    TierName,
    TierTrace,
    TriageDecision,
    TriageSuggestion,
)

logger = logging.getLogger(__name__)


class Tier1Like(Protocol):
    """Tier 1 classifier/retriever."""

    def predict(self, bug: Bug) -> Tier1Result: ...


class JudgeLike(Protocol):
    """Tier 2 LLM judge."""

    def suggest(self, bug: Bug, t1: Tier1Result) -> TriageSuggestion: ...


class FinalLike(Protocol):
    """Tier 3 final triage."""

    def decide(self, bug: Bug, t1: Tier1Result, s: TriageSuggestion) -> TriageSuggestion: ...


def _ms(start: float) -> float:
    return (time.perf_counter() - start) * 1000.0


class Pipeline:
    """Runs the tiers and records a trace."""

    def __init__(
        self,
        tier1: Tier1Like,
        judge: JudgeLike | None = None,
        final: FinalLike | None = None,
        *,
        policy: FinalPolicy = "on-disagreement",
        confidence_threshold: float = 0.7,
    ) -> None:
        if not 0.0 <= confidence_threshold <= 1.0:
            raise ValueError("confidence_threshold must be in [0, 1]")
        self.tier1 = tier1
        self.judge = judge
        self.final = final
        self.policy = policy
        self.confidence_threshold = confidence_threshold

    def should_escalate(self, t1: Tier1Result, s: TriageSuggestion) -> bool:
        """Whether the final tier should review this suggestion."""
        if self.final is None or self.policy == "never":
            return False
        if self.policy == "always":
            return True
        return (
            s.component != t1.top_component()
            or s.assignee != t1.assignee
            or s.confidence < self.confidence_threshold
        )

    @staticmethod
    def _tier1_decision(t1: Tier1Result, rationale: str) -> TriageDecision:
        p = t1.to_prediction()
        return TriageDecision(
            **p.model_dump(),
            severity="medium",
            confidence=t1.top_score(),
            rationale=rationale,
            source="tier1",
            escalated=False,
        )

    def run(self, bug: Bug) -> PipelineResult:
        """Triage one bug."""
        t1 = self.tier1.predict(bug)
        trace = [TierTrace(tier="tier1", prediction=t1.to_prediction(), elapsed_ms=t1.elapsed_ms)]
        if self.judge is None:
            return PipelineResult(decision=self._tier1_decision(t1, "tier1 only"), trace=trace)

        start = time.perf_counter()
        try:
            suggestion = self.judge.suggest(bug, t1)
        except Exception as exc:
            logger.warning("judge failed, falling back to tier1: %s", exc)
            trace.append(
                TierTrace(tier="judge", prediction=None, elapsed_ms=_ms(start), error=str(exc))
            )
            return PipelineResult(
                decision=self._tier1_decision(t1, f"fallback: {exc}"), trace=trace
            )
        trace.append(
            TierTrace(tier="judge", prediction=_as_prediction(suggestion), elapsed_ms=_ms(start))
        )
        suggestion = _tier1_links(suggestion, t1)

        if self.final is not None and self.should_escalate(t1, suggestion):
            start = time.perf_counter()
            try:
                decided = self.final.decide(bug, t1, suggestion)
            except Exception as exc:
                logger.warning("final tier failed, keeping judge decision: %s", exc)
                trace.append(
                    TierTrace(tier="final", prediction=None, elapsed_ms=_ms(start), error=str(exc))
                )
                decision = _decision(suggestion, "judge", True, str(exc))
            else:
                trace.append(
                    TierTrace(
                        tier="final", prediction=_as_prediction(decided), elapsed_ms=_ms(start)
                    )
                )
                decision = _decision(_tier1_links(decided, t1), "final", True, None)
            return PipelineResult(decision=decision, trace=trace)
        return PipelineResult(decision=_decision(suggestion, "judge", False, None), trace=trace)


def _tier1_links(s: TriageSuggestion, t1: Tier1Result) -> TriageSuggestion:
    """Keep Tier 1's threshold-gated duplicate/known-issue links.

    Linking is a retrieval question: on the eval set the tuned TF-IDF thresholds were right on
    97.5% (dup) / 92.5% (KI) of bugs, the LLM judge on 72.5% / 87.5%. Traces keep the raw
    judge/final output so the per-tier rows still show it.
    """
    return s.model_copy(update={"duplicate_of": t1.duplicate_of, "known_issue": t1.known_issue})


def _as_prediction(s: TriageSuggestion) -> Prediction:
    return Prediction(
        component=s.component,
        team=s.team,
        assignee=s.assignee,
        duplicate_of=s.duplicate_of,
        known_issue=s.known_issue,
    )


def _decision(
    s: TriageSuggestion, source: TierName, escalated: bool, final_error: str | None
) -> TriageDecision:
    return TriageDecision(
        **s.model_dump(), source=source, escalated=escalated, final_error=final_error
    )
