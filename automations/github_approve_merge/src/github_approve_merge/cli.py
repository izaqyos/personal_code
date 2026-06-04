from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Sequence

from github_approve_merge import __version__, retention
from github_approve_merge.actions import EXIT_CODE_FAILURE, EXIT_CODE_USAGE
from github_approve_merge.config import (
    DEFAULT_RETENTION_DAYS,
    default_logs_dir,
    generate_run_id,
)
from github_approve_merge.gate import make_gate
from github_approve_merge.gh_client import GhAuthError, GhClient, PrClient
from github_approve_merge.input_sources import InputSourceError, collect_urls
from github_approve_merge.logging_setup import RunContext, make_run_logger
from github_approve_merge.runner import run_batch
from github_approve_merge.url import parse_pr_url


def _add_batch_options(sp: argparse.ArgumentParser) -> None:
    sp.add_argument("urls", nargs="*", help="PR URLs (in addition to --file / stdin).")
    sp.add_argument("--file", type=Path, default=None,
                    help="Path to a file with one URL per line ('#' comments OK).")
    sp.add_argument("--dry-run", action="store_true",
                    help="Classify PRs and print the plan without approving or merging.")
    sp.add_argument("--merge-method", choices=["merge", "squash", "rebase"], default="merge",
                    help="Merge method for direct (non-queue) merges. Default: merge.")
    sp.add_argument("--yes", action="store_true",
                    help="Skip the confirmation gate (for scripts/cron).")
    sp.add_argument("--confirm-each", action="store_true",
                    help="Confirm each PR individually instead of one batch prompt.")
    sp.add_argument("--resume", default=None, metavar="ID",
                    help="Resume a previous batch by reusing its logs/<ID>/ dir.")
    sp.add_argument("--retention-days", type=int, default=DEFAULT_RETENTION_DAYS)
    sp.add_argument("--logs-dir", type=Path, default=default_logs_dir())
    sp.add_argument("--run-id", default=None)
    sp.add_argument("--redact-logs", action="store_true",
                    help="Hash PR slugs in state.jsonl/summary.json so the run dir can be "
                         "shared externally.")
    v = sp.add_mutually_exclusive_group()
    v.add_argument("--verbose", action="store_true")
    v.add_argument("--quiet", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gh-approve-merge",
        description="Approve and merge GitHub PRs in batch via the GitHub CLI (gh).",
    )
    p.add_argument("--version", action="version", version=f"gh-approve-merge {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    auth = sub.add_parser("auth", help="Check gh auth / SSO authorization.")
    auth_sub = auth.add_subparsers(dest="auth_command", required=True)
    auth_sub.add_parser("status", help="Check gh is installed, logged in, and SSO-authorized.")

    sub.add_parser("doctor", help="Alias for `auth status`.")

    _add_batch_options(sub.add_parser("approve", help="Approve PRs (no merge)."))
    _add_batch_options(sub.add_parser("merge", help="Merge PRs (gated; no approve)."))
    run = sub.add_parser("run", help="Approve + merge PRs (gated).")
    _add_batch_options(run)
    run.add_argument("--no-approve", action="store_true",
                     help="Skip the approve step; merge only.")

    gc = sub.add_parser("gc", help="Run the retention sweep without doing anything else.")
    gc.add_argument("--logs-dir", type=Path, default=default_logs_dir())
    gc.add_argument("--retention-days", type=int, default=DEFAULT_RETENTION_DAYS)

    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command in ("auth", "doctor"):
        return _cmd_doctor()

    if args.command == "gc":
        deleted = retention.sweep(args.logs_dir, max_age_days=args.retention_days, skip=set())
        print(f"Deleted {len(deleted)} expired run dir(s) under {args.logs_dir}")
        return 0

    if args.command == "approve":
        return _cmd_batch(args, approve=True, do_merge=False)
    if args.command == "merge":
        return _cmd_batch(args, approve=False, do_merge=True)
    if args.command == "run":
        return _cmd_batch(args, approve=not args.no_approve, do_merge=True)

    return EXIT_CODE_USAGE


def _cmd_doctor() -> int:
    gh = GhClient()
    try:
        gh.preflight()
        login = gh.current_login()
    except GhAuthError as e:
        print(f"gh auth: NOT OK — {e}", file=sys.stderr)
        print("Fix: run `gh auth login` and authorize the token for the org's SSO.",
              file=sys.stderr)
        return EXIT_CODE_FAILURE
    print(f"gh auth: OK — logged in as {login}")
    return 0


def _cmd_batch(args, *, approve: bool, do_merge: bool) -> int:
    gh = GhClient()
    try:
        gh.preflight()
        me = gh.current_login()
    except GhAuthError as e:
        print(f"error: gh not ready — {e}", file=sys.stderr)
        print("Fix: run `gh auth login` (and authorize SSO for the org).", file=sys.stderr)
        return EXIT_CODE_FAILURE

    has_input = bool(args.urls) or args.file is not None or not sys.stdin.isatty()
    if args.resume and has_input:
        print("error: --resume is mutually exclusive with URLs/--file/stdin", file=sys.stderr)
        return EXIT_CODE_USAGE

    try:
        if args.resume:
            prs = _load_prs_from_state(args.logs_dir / args.resume)
        else:
            use_stdin = (not args.urls and args.file is None and not sys.stdin.isatty())
            prs = collect_urls(args=args.urls, file_path=args.file,
                               stdin=sys.stdin if use_stdin else None)
    except InputSourceError as e:
        print(f"error: {e}", file=sys.stderr)
        return EXIT_CODE_USAGE

    run_id = args.resume or args.run_id or generate_run_id()
    run_dir = args.logs_dir / run_id
    ctx = RunContext(run_id=run_id, run_dir=run_dir, redact_logs=args.redact_logs)
    logger = make_run_logger(ctx, verbose=args.verbose, quiet=args.quiet)

    if not args.dry_run:
        deleted = retention.sweep(args.logs_dir, max_age_days=args.retention_days, skip={run_dir})
        if deleted:
            logger.info("retention swept %d old run dir(s)", len(deleted), extra={"step": "retention"})

    gate = make_gate(assume_yes=args.yes, confirm_each=args.confirm_each)

    def client_factory(pr, me_):
        return PrClient(gh=gh, owner=pr.owner, repo=pr.repo, number=pr.number, me=me_)

    summary = asyncio.run(run_batch(
        prs,
        client_factory=client_factory,
        me=me,
        approve=approve,
        do_merge=do_merge,
        method=args.merge_method,
        gate=gate,
        logs_dir=args.logs_dir,
        run_id=run_id,
        dry_run=args.dry_run,
        resume=bool(args.resume),
        ctx=ctx,
    ))
    return summary["exit_code"]


def _load_prs_from_state(run_dir: Path):
    state_path = run_dir / "state.jsonl"
    if not state_path.exists():
        raise InputSourceError(f"--resume target {run_dir} has no state.jsonl — nothing to resume")
    seen: list[str] = []
    seen_set: set[str] = set()
    for line in state_path.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        slug = rec.get("pr")
        if slug and slug not in seen_set:
            seen.append(slug)
            seen_set.add(slug)
    refs = []
    for slug in seen:
        owner_repo, _, number = slug.partition("#")
        owner, repo = owner_repo.split("/", 1)
        refs.append(parse_pr_url(f"https://github.com/{owner}/{repo}/pull/{number}"))
    return refs
