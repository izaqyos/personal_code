"""Pydantic models shared by all triage tiers (frozen contract, see docs/INTERFACES.md)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Severity = Literal["low", "medium", "high", "critical"]
TierName = Literal["tier1", "judge", "final"]
Source = Literal["tier1", "judge", "final", "human"]
FinalPolicy = Literal["always", "on-disagreement", "never"]


class Bug(BaseModel):
    """An incoming bug report."""

    id: str
    title: str
    description: str
    logs: str = ""

    def text(self) -> str:
        """Title, description and logs joined by newlines, stripped."""
        return f"{self.title}\n{self.description}\n{self.logs}".strip()


class LabeledBug(Bug):
    """A bug with confirmed triage labels."""

    component: str
    team: str
    assignee: str
    severity: Severity
    duplicate_of: str | None = None
    known_issue: str | None = None


class Candidate(BaseModel):
    """A scored component candidate."""

    label: str
    score: float = Field(ge=0.0, le=1.0)


class SimilarBug(BaseModel):
    """A retrieved similar past bug."""

    bug_id: str
    title: str
    score: float = Field(ge=0.0, le=1.0)
    component: str
    assignee: str
    duplicate_of: str | None = None


class KnownIssueHit(BaseModel):
    """A retrieved known issue."""

    id: str
    title: str
    score: float = Field(ge=0.0, le=1.0)


class Prediction(BaseModel):
    """Triage labels predicted by a tier.

    The routing decision is component -> team. ``assignee`` is only a suggested first contact
    (the component's default owner from the KB); no tier tries to predict the person.
    """

    component: str
    team: str
    assignee: str
    duplicate_of: str | None = None
    known_issue: str | None = None


class Tier1Result(BaseModel):
    """Output of the TF-IDF tier: classifier candidates plus retrieval context."""

    component_candidates: list[Candidate]
    team: str
    assignee: str
    similar_bugs: list[SimilarBug]
    known_issue_hits: list[KnownIssueHit]
    duplicate_of: str | None
    known_issue: str | None
    elapsed_ms: float

    def top_component(self) -> str:
        """Label of the best component candidate."""
        if not self.component_candidates:
            raise ValueError("no component candidates")
        return self.component_candidates[0].label

    def top_score(self) -> float:
        """Score of the best component candidate."""
        if not self.component_candidates:
            raise ValueError("no component candidates")
        return self.component_candidates[0].score

    def to_prediction(self) -> Prediction:
        """Convert to a plain Prediction."""
        return Prediction(
            component=self.top_component(),
            team=self.team,
            assignee=self.assignee,
            duplicate_of=self.duplicate_of,
            known_issue=self.known_issue,
        )


class TriageSuggestion(BaseModel):
    """LLM output (judge and final tier): team routing plus severity and rationale, no person."""

    component: str
    team: str
    duplicate_of: str | None = None
    known_issue: str | None = None
    severity: Severity
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str


class TriageDecision(TriageSuggestion):
    """The final decision, with provenance and the suggested first contact."""

    assignee: str
    source: Source
    escalated: bool

    def to_prediction(self) -> Prediction:
        """The labels of this decision as a plain Prediction."""
        return Prediction(
            component=self.component,
            team=self.team,
            assignee=self.assignee,
            duplicate_of=self.duplicate_of,
            known_issue=self.known_issue,
        )


class TierTrace(BaseModel):
    """One tier's contribution to a pipeline run."""

    tier: TierName
    prediction: Prediction | None
    elapsed_ms: float
    error: str | None = None


class PipelineResult(BaseModel):
    """Final decision plus per-tier trace.

    ``decision`` is None when the tiers could not decide (the judge failed twice, or the final tier
    failed on an escalated bug); ``needs_human`` then says why, and a person picks the team.
    """

    decision: TriageDecision | None
    trace: list[TierTrace]
    needs_human: str | None = None
