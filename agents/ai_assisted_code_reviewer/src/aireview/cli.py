"""aireview CLI.

aireview context    build .ai-review/out/context.md for a harness agent to read
aireview validate   validate agent-written findings.json, merge tool checks, render report
aireview run        full pipeline with an LLM runner (claude | mock) — what CI uses
aireview checks     deterministic checks only (no LLM)
aireview wiki-lint  lint the wiki (ids, severities, routing)
aireview route      show which wiki pages apply to given paths
aireview install    install the kit into a repo
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import load_config
from .diff import GitError
from .install import ALL, install
from .pipeline import (
    Paths,
    build_context,
    bundle_text,
    finalize,
    load_pr_body,
    write_outputs,
)
from .runners import RunnerError, extract_findings, get_runner
from .wiki import lint, load_wiki


def _common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--repo", default=".", help="repo root (default: cwd)")
    p.add_argument("--base", help="base ref to diff against (default: config 'base')")
    p.add_argument(
        "--pr-body",
        help="PR title/description file (default: $GITHUB_EVENT_PATH or .ai-review/out/pr_body.md)",
    )
    p.add_argument("--diff-file", help="use this unified diff instead of running git")
    p.add_argument(
        "--include-uncommitted",
        action="store_true",
        help="also review uncommitted changes to tracked files",
    )
    p.add_argument(
        "--labels",
        default="",
        help="comma-separated PR labels (for the override label)",
    )
    p.add_argument("--gate", choices=["advisory", "blocker"], help="override config gate mode")
    p.add_argument("--out-dir", help="where to write outputs (default: .ai-review/out)")
    p.add_argument("--quiet", action="store_true", help="don't print the report")


def _setup(args):
    repo = Path(args.repo).resolve()
    cfg = load_config(repo)
    if args.gate:
        cfg["gate"] = args.gate
    diff_text = Path(args.diff_file).read_text() if args.diff_file else None
    pr_body = load_pr_body(repo, args.pr_body)
    ctx, wiki = build_context(
        repo,
        cfg,
        base=args.base,
        pr_body=pr_body,
        include_uncommitted=args.include_uncommitted,
        diff_text=diff_text,
    )
    return repo, cfg, ctx, wiki


def _labels(args) -> list[str]:
    return [label.strip() for label in args.labels.split(",") if label.strip()]


def _finish(args, repo, result) -> int:
    out = write_outputs(repo, result, Path(args.out_dir) if args.out_dir else None)
    if not args.quiet:
        print(result.markdown)
    print(
        f"[aireview] status={result.gate.status} report={out / 'report.md'}",
        file=sys.stderr,
    )
    return result.gate.exit_code


def cmd_context(args) -> int:
    repo, cfg, ctx, wiki = _setup(args)
    text = bundle_text(repo, ctx, wiki, cfg)
    out = Path(args.out_dir) if args.out_dir else Paths(repo).out
    out.mkdir(parents=True, exist_ok=True)
    (out / "context.md").write_text(text)
    print(f"Wrote {out / 'context.md'}")
    print(f"  files: {len(ctx.reviewable)} reviewable / {len(ctx.files)} changed")
    print(f"  wiki pages: {', '.join(ctx.routed) or 'none'}")
    print(f"  tool findings: {len(ctx.tool_findings)}")
    return 0


def cmd_validate(args) -> int:
    repo, cfg, ctx, wiki = _setup(args)
    path = Path(args.findings) if args.findings else Paths(repo).out / "findings.json"
    raw = extract_findings(path.read_text())
    return _finish(args, repo, finalize(repo, ctx, wiki, raw, cfg, labels=_labels(args)))


def cmd_checks(args) -> int:
    repo, cfg, ctx, wiki = _setup(args)
    return _finish(
        args,
        repo,
        finalize(
            repo,
            ctx,
            wiki,
            [],
            cfg,
            labels=_labels(args),
            notes=["Deterministic checks only (no LLM review)."],
        ),
    )


def cmd_run(args) -> int:
    repo, cfg, ctx, wiki = _setup(args)
    text = bundle_text(repo, ctx, wiki, cfg)
    out = Path(args.out_dir) if args.out_dir else Paths(repo).out
    out.mkdir(parents=True, exist_ok=True)
    (out / "context.md").write_text(text)
    notes: list[str] = []
    raw: list = []
    if not ctx.reviewable:
        notes.append("Nothing reviewable in the diff; LLM review skipped.")
    else:
        try:
            raw = get_runner(args.runner, cfg, args.mock_response).review(text, repo)
        except RunnerError as e:
            notes.append(f"LLM review failed ({e}); showing deterministic checks only.")
            if args.strict:
                result = finalize(repo, ctx, wiki, [], cfg, labels=_labels(args), notes=notes)
                _finish(args, repo, result)
                return 2
    (out / "findings.raw.json").write_text(json.dumps({"findings": raw}, indent=2))
    return _finish(
        args,
        repo,
        finalize(repo, ctx, wiki, raw, cfg, labels=_labels(args), notes=notes),
    )


def cmd_wiki_lint(args) -> int:
    wiki = load_wiki(Paths(Path(args.repo).resolve()).wiki)
    errors, warnings = lint(wiki)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(
        f"{len(wiki.rules)} rules, {len(wiki.pages)} pages, "
        f"{len(errors)} error(s), {len(warnings)} warning(s)"
    )
    return 1 if errors or (args.strict and warnings) else 0


def cmd_route(args) -> int:
    wiki = load_wiki(Paths(Path(args.repo).resolve()).wiki)
    for page, reasons in wiki.route(args.paths).items():
        print(f"{page}  <- {', '.join(dict.fromkeys(reasons))}")
    return 0


def cmd_install(args) -> int:
    groups = [g.strip() for g in args.only.split(",")] if args.only else None
    target = Path(args.target).resolve()
    for action, path in install(target, groups, args.force):
        print(f"{action:14} {path.relative_to(target)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="aireview",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("context", help="write the review bundle for an agent")
    _common(p)
    p.set_defaults(fn=cmd_context)

    p = sub.add_parser("validate", help="validate agent findings and render the report")
    _common(p)
    p.add_argument("--findings", help="findings JSON (default: .ai-review/out/findings.json)")
    p.set_defaults(fn=cmd_validate)

    p = sub.add_parser("checks", help="deterministic checks only")
    _common(p)
    p.set_defaults(fn=cmd_checks)

    p = sub.add_parser("run", help="full pipeline with an LLM runner")
    _common(p)
    p.add_argument("--runner", choices=["claude", "mock"], default="claude")
    p.add_argument("--mock-response", help="canned model output for --runner mock")
    p.add_argument("--strict", action="store_true", help="exit 2 if the LLM step fails")
    p.set_defaults(fn=cmd_run)

    p = sub.add_parser("wiki-lint", help="lint the wiki")
    p.add_argument("--repo", default=".")
    p.add_argument("--strict", action="store_true", help="fail on warnings too")
    p.set_defaults(fn=cmd_wiki_lint)

    p = sub.add_parser("route", help="show wiki pages routed for paths")
    p.add_argument("paths", nargs="+")
    p.add_argument("--repo", default=".")
    p.set_defaults(fn=cmd_route)

    p = sub.add_parser("install", help="install the kit into a repo")
    p.add_argument("target", nargs="?", default=".")
    p.add_argument("--only", help=f"comma-separated groups: {','.join(ALL)} (core always included)")
    p.add_argument("--force", action="store_true", help="overwrite existing files")
    p.set_defaults(fn=cmd_install)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.fn(args)
    except (GitError, RunnerError, FileNotFoundError, ValueError) as e:
        print(f"aireview: error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
