"""Evaluation harness: per-tier and final-decision accuracy on a labeled set."""

from __future__ import annotations

import logging
from typing import Protocol

from pydantic import BaseModel

from bug_triage.models import (
    Bug,
    LabeledBug,
    PipelineResult,
    Prediction,
    Tier1Result,
    TierName,
)

logger = logging.getLogger(__name__)


class Tier1Like(Protocol):
    """Anything that can produce a Tier1Result."""

    def predict(self, bug: Bug) -> Tier1Result: ...


class RunnerLike(Protocol):
    """Anything that can run the full pipeline."""

    def run(self, bug: Bug) -> PipelineResult: ...


class TierMetrics(BaseModel):
    """Accuracy metrics of one tier."""

    tier: TierName
    n: int
    acc_component: float
    acc_team: float
    acc_assignee: float
    acc_duplicate: float
    acc_known_issue: float
    error_rate: float
    mean_ms: float


class EvalReport(BaseModel):
    """Evaluation result over a labeled set."""

    tiers: list[TierMetrics]
    final_decision: TierMetrics  # over the bugs the tiers decided; n can be below the report's n
    escalation_rate: float
    n: int
    human_rate: float = 0.0  # share of bugs left for a person (no automatic decision)


def _metrics(tier: TierName, rows: list[tuple[LabeledBug, Prediction, float]]) -> TierMetrics:
    n = len(rows)

    def share(flags: list[bool]) -> float:
        return sum(flags) / n if n else 0.0

    return TierMetrics(
        tier=tier,
        n=n,
        acc_component=share([p.component == b.component for b, p, _ in rows]),
        acc_team=share([p.team == b.team for b, p, _ in rows]),
        acc_assignee=share([p.assignee == b.assignee for b, p, _ in rows]),
        acc_duplicate=share([p.duplicate_of == b.duplicate_of for b, p, _ in rows]),
        acc_known_issue=share([p.known_issue == b.known_issue for b, p, _ in rows]),
        # Routing error. Assignee is reported separately: its labels are capped at ~70% by data.
        error_rate=share([p.component != b.component or p.team != b.team for b, p, _ in rows]),
        mean_ms=sum(ms for _, _, ms in rows) / n if n else 0.0,
    )


def run_eval(
    bugs: list[LabeledBug],
    *,
    tier1: Tier1Like,
    runner: RunnerLike | None = None,
    limit: int | None = None,
) -> EvalReport:
    """Evaluate Tier 1 alone, or every tier of a pipeline runner."""
    subset = bugs[:limit] if limit is not None else list(bugs)
    if not subset:
        raise ValueError("no bugs to evaluate")

    if runner is None:
        rows: list[tuple[LabeledBug, Prediction, float]] = []
        for bug in subset:
            res = tier1.predict(bug)
            rows.append((bug, res.to_prediction(), res.elapsed_ms))
        t1 = _metrics("tier1", rows)
        return EvalReport(
            tiers=[t1],
            final_decision=t1.model_copy(),
            escalation_rate=0.0,
            n=len(subset),
        )

    per_tier: dict[TierName, list[tuple[LabeledBug, Prediction, float]]] = {}
    final_rows: list[tuple[LabeledBug, Prediction, float]] = []
    escalated = 0
    human = 0
    for bug in subset:
        result = runner.run(bug)
        elapsed = 0.0
        for tr in result.trace:
            elapsed += tr.elapsed_ms
            if tr.prediction is not None:
                per_tier.setdefault(tr.tier, []).append((bug, tr.prediction, tr.elapsed_ms))
        if result.decision is None:
            human += 1
            continue
        final_rows.append((bug, result.decision.to_prediction(), elapsed))
        escalated += int(result.decision.escalated)

    order: list[TierName] = ["tier1", "judge", "final"]
    tiers = [_metrics(t, per_tier[t]) for t in order if t in per_tier]
    return EvalReport(
        tiers=tiers,
        final_decision=_metrics("final", final_rows),
        escalation_rate=escalated / len(subset),
        human_rate=human / len(subset),
        n=len(subset),
    )


def _row(label: str, m: TierMetrics) -> str:
    return (
        f"{label:<8} | {m.n:>4} | {m.acc_component:>6.1%} | {m.acc_team:>6.1%} | "
        f"{m.acc_assignee:>8.1%} | {m.acc_duplicate:>6.1%} | {m.acc_known_issue:>6.1%} | "
        f"{m.error_rate:>6.1%} | {m.mean_ms:>8.1f}"
    )


def format_report(report: EvalReport) -> str:
    """Render the report as an aligned text table plus a one-line error summary."""
    header = (
        f"{'tier':<8} | {'n':>4} | {'comp':>6} | {'team':>6} | {'assignee':>8} | "
        f"{'dup':>6} | {'KI':>6} | {'error':>6} | {'ms':>8}"
    )
    lines = [header, "-" * len(header)]
    lines.extend(_row(m.tier, m) for m in report.tiers)
    lines.append(_row("decision", report.final_decision))
    lines.append(f"escalation rate: {report.escalation_rate:.1%} (n={report.n})")
    if report.human_rate:
        lines.append(f"left for a human: {report.human_rate:.1%} (decision row over the rest)")
    parts = [f"{m.tier} {m.error_rate:.1%}" for m in report.tiers if m.tier != "final"]
    parts.append(f"final {report.final_decision.error_rate:.1%}")
    lines.append("error: " + " → ".join(parts))
    return "\n".join(lines)
