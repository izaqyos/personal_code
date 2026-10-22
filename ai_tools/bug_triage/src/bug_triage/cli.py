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
from bug_triage.models import Bug, LabeledBug, PipelineResult
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
    pipeline, _, _ = build_pipeline(args.judge, args.final, args.model)
    print(pipeline.run(bug).model_dump_json(indent=2))
    return 0


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
