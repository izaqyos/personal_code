"""Command line interface: ``bug-triage triage`` and ``bug-triage eval``."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import ValidationError

from bug_triage.kb import KnowledgeBase
from bug_triage.models import Bug, LabeledBug, PipelineResult, Severity, TriageDecision
from bug_triage.pipeline import Pipeline

if TYPE_CHECKING:
    from bug_triage.tier1_tfidf import Tier1Classifier

DEFAULT_MODEL = "gemma4:12b"


def build_pipeline(
    judge: str, final: str, model: str
) -> tuple[Pipeline, KnowledgeBase, Tier1Classifier]:
    """Wire the concrete tiers (imports are lazy so unused backends are never loaded)."""
    from bug_triage.tier1_tfidf import Tier1Classifier

    kb = KnowledgeBase.load()
    tier1 = Tier1Classifier(kb).fit()
    judge_obj: Any = None
    if judge == "ollama":
        from bug_triage.judge import Judge
        from bug_triage.llm.ollama_client import OllamaClient

        judge_obj = Judge(OllamaClient(model=model), kb)
    elif judge == "gemini":
        from bug_triage.judge import Judge
        from bug_triage.llm.gemini_client import GeminiClient

        judge_obj = Judge(GeminiClient(), kb)
    final_obj: Any = None
    policy: Any = final
    if final != "never":
        from bug_triage.final_claude import FinalTriager

        final_obj = FinalTriager(kb)
    return Pipeline(tier1, judge_obj, final_obj, policy=policy), kb, tier1


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bug-triage", description="Mock 3-tier bug triage.")
    sub = parser.add_subparsers(dest="command", required=True)

    tri = sub.add_parser("triage", help="triage a single bug")
    tri.add_argument("--title")
    tri.add_argument("--desc")
    tri.add_argument("--logs", default="")
    tri.add_argument("--file", type=Path, help="JSON file with id/title/description/logs")
    tri.add_argument("--judge", choices=["ollama", "gemini", "none"], default="ollama")
    tri.add_argument(
        "--final", choices=["always", "on-disagreement", "never"], default="on-disagreement"
    )
    tri.add_argument("--model", default=DEFAULT_MODEL)

    ev = sub.add_parser("eval", help="evaluate on the held-out set")
    ev.add_argument("--tiers", type=int, choices=[1, 2, 3], default=1)
    ev.add_argument("--judge", choices=["ollama", "gemini"], default="ollama")
    ev.add_argument(
        "--final", choices=["always", "on-disagreement", "never"], default="on-disagreement"
    )
    ev.add_argument("--model", default=DEFAULT_MODEL)
    ev.add_argument("--limit", type=int, default=None)
    return parser


def _load_bug(args: argparse.Namespace) -> Bug:
    if args.file is not None:
        try:
            return Bug.model_validate(json.loads(args.file.read_text(encoding="utf-8")))
        except OSError as exc:
            raise ValueError(f"cannot read {args.file}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON in {args.file}: {exc}") from exc
        except ValidationError as exc:
            raise ValueError(f"invalid bug in {args.file}: {exc}") from exc
    return Bug(id="CLI-1", title=args.title, description=args.desc, logs=args.logs)


def _cmd_triage(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    if args.file is None and (args.title is None or args.desc is None):
        parser.error("triage needs --title and --desc, or --file")
    bug = _load_bug(args)
    pipeline, kb, _ = build_pipeline(args.judge, args.final, args.model)
    result = pipeline.run(bug)
    if result.needs_human is not None and sys.stdin.isatty():
        result = ask_human(result, kb)
    print(result.model_dump_json(indent=2))
    return 0


SEVERITIES: tuple[Severity, ...] = ("low", "medium", "high", "critical")


def _ask(prompt: str) -> str | None:
    """Prompt on stderr (stdout carries the JSON); None on end of input."""
    print(prompt, end="", file=sys.stderr, flush=True)
    line = sys.stdin.readline()
    return None if line == "" else line.strip()


def ask_human(result: PipelineResult, kb: KnowledgeBase) -> PipelineResult:
    """Ask a person to pick the component when the tiers could not decide.

    The person's choice becomes the decision (source "human"); nothing falls back to Tier 1.
    Empty input or end of input leaves the bug undecided.
    """
    names = sorted(kb.components)
    print(f"\nNo automatic decision ({result.needs_human}). Pick the component:", file=sys.stderr)
    for i, name in enumerate(names, 1):
        print(f"  {i:>2}) {name} -> {kb.owner_team(name)}", file=sys.stderr)
    t1 = result.trace[0].prediction
    if t1 is not None:
        print(f"  (Tier 1 guessed {t1.component}; a hint, not a decision)", file=sys.stderr)
    component: str | None = None
    while component is None:
        answer = _ask("component (number or name, Enter = leave undecided): ")
        if not answer:
            return result
        if answer.isdigit() and 1 <= int(answer) <= len(names):
            component = names[int(answer) - 1]
        elif kb.is_valid_component(answer):
            component = answer
        else:
            print(f"  unknown component: {answer}", file=sys.stderr)
    severity: Severity | None = None
    while severity is None:
        answer = _ask("severity (low/medium/high/critical, Enter = medium): ")
        severity = next((s for s in SEVERITIES if s == (answer or "medium")), None)
        if severity is None:
            print(f"  unknown severity: {answer}", file=sys.stderr)
    decision = TriageDecision(
        component=component,
        team=kb.owner_team(component),
        assignee=kb.default_assignee(component),
        duplicate_of=t1.duplicate_of if t1 else None,
        known_issue=t1.known_issue if t1 else None,
        severity=severity,
        confidence=1.0,
        rationale=f"human decision ({result.needs_human})",
        source="human",
        escalated=False,
    )
    return result.model_copy(update={"decision": decision})


class _Progress:
    """Wraps a runner and reports progress to stderr every 5 bugs."""

    def __init__(self, inner: Pipeline, total: int) -> None:
        self.inner = inner
        self.total = total
        self.done = 0

    def run(self, bug: Bug) -> PipelineResult:
        result = self.inner.run(bug)
        self.done += 1
        if self.done % 5 == 0 or self.done == self.total:
            print(f"eval: {self.done}/{self.total} bugs", file=sys.stderr)
        return result


def _cmd_eval(args: argparse.Namespace) -> int:
    from bug_triage.evaluate import format_report, run_eval
    from bug_triage.kb import load_eval

    judge = "none" if args.tiers == 1 else args.judge
    final = "never" if args.tiers < 3 else args.final
    pipeline, _, tier1 = build_pipeline(judge, final, args.model)
    bugs: list[LabeledBug] = load_eval()
    total = min(len(bugs), args.limit) if args.limit is not None else len(bugs)
    runner = None if args.tiers == 1 else _Progress(pipeline, total)
    report = run_eval(bugs, tier1=tier1, runner=runner, limit=args.limit)
    print(format_report(report))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point: 0 ok, 1 runtime error, 2 usage error."""
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    parser = _parser()
    try:
        args = parser.parse_args(argv)
        if args.command == "triage":
            return _cmd_triage(args, parser)
        return _cmd_eval(args)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 2
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
