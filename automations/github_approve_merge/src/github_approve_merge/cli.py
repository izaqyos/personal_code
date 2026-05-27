from __future__ import annotations

import argparse
import asyncio
import signal
import sys
from pathlib import Path
from typing import Sequence

from github_approve_merge import __version__, retention
from github_approve_merge.actions import (
    EXIT_CODE_FAILURE,
    EXIT_CODE_INTERRUPTED,
    EXIT_CODE_USAGE,
    process_pr,
)
from github_approve_merge.auth import AuthStatus, check_storage_state, interactive_login
from github_approve_merge.browser import StorageStateError, open_context
from github_approve_merge.config import (
    DEFAULT_RETENTION_DAYS,
    DEFAULT_TIMEOUT_SECONDS,
    default_logs_dir,
    default_storage_state_path,
    generate_run_id,
)
from github_approve_merge.input_sources import InputSourceError, collect_urls
from github_approve_merge.logging_setup import RunContext, make_run_logger
from github_approve_merge.pages.files_page import FilesPage
from github_approve_merge.pages.pr_page import PRPage
from github_approve_merge.runner import Runner
from github_approve_merge.screenshots import capture


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gh-approve-merge",
        description="Approve and merge GitHub PRs in batch via Playwright.",
    )
    p.add_argument("--version", action="version", version=f"gh-approve-merge {__version__}")
    sub = p.add_subparsers(dest="subcommand", required=True)

    # auth
    auth = sub.add_parser("auth", help="Manage browser session for github.com.")
    auth_sub = auth.add_subparsers(dest="auth_subcommand", required=True)
    auth_login = auth_sub.add_parser("login", help="Open a headed browser and save session.")
    auth_login.add_argument("--storage-state", type=Path, default=default_storage_state_path())
    auth_status = auth_sub.add_parser("status", help="Show whether the saved session exists.")
    auth_status.add_argument("--storage-state", type=Path, default=default_storage_state_path())

    # run
    run = sub.add_parser("run", help="Approve and merge a batch of PRs.")
    run.add_argument("urls", nargs="*", help="PR URLs (in addition to --file / stdin).")
    run.add_argument("--file", type=Path, default=None,
                     help="Path to a file with one URL per line ('#' comments OK).")
    run.add_argument("--retention-days", type=int, default=DEFAULT_RETENTION_DAYS)
    run.add_argument("--storage-state", type=Path, default=default_storage_state_path())
    run.add_argument("--logs-dir", type=Path, default=default_logs_dir())
    run.add_argument("--run-id", default=None)
    run.add_argument("--resume", default=None, metavar="ID",
                     help="Resume a previous batch by reusing its logs/<ID>/ dir.")
    run.add_argument("--dry-run", action="store_true",
                     help="Classify PR states without clicking anything.")
    run.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    verbosity = run.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", action="store_true")
    verbosity.add_argument("--quiet", action="store_true")

    # gc
    gc = sub.add_parser("gc", help="Run the retention sweep without doing anything else.")
    gc.add_argument("--logs-dir", type=Path, default=default_logs_dir())
    gc.add_argument("--retention-days", type=int, default=DEFAULT_RETENTION_DAYS)

    return p


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.subcommand == "auth":
        if args.auth_subcommand == "login":
            return _cmd_auth_login(args.storage_state)
        if args.auth_subcommand == "status":
            return _cmd_auth_status(args.storage_state)
        return EXIT_CODE_USAGE

    if args.subcommand == "gc":
        deleted = retention.sweep(args.logs_dir, max_age_days=args.retention_days, skip=set())
        print(f"Deleted {len(deleted)} expired run dir(s) under {args.logs_dir}")
        return 0

    if args.subcommand == "run":
        return _cmd_run(args)

    parser.error(f"unknown subcommand: {args.subcommand}")
    return EXIT_CODE_USAGE


def _cmd_auth_login(storage_state_path: Path) -> int:
    try:
        asyncio.run(interactive_login(storage_state_path))
    except KeyboardInterrupt:
        print("Login cancelled.", file=sys.stderr)
        return EXIT_CODE_INTERRUPTED
    return 0


def _cmd_auth_status(storage_state_path: Path) -> int:
    result = check_storage_state(storage_state_path)
    print(f"storage_state: {result.status.value} ({result.message})")
    return 0 if result.status is AuthStatus.PRESENT else EXIT_CODE_FAILURE


def _cmd_run(args) -> int:
    # --resume cannot combine with explicit URLs/file/stdin.
    has_args_input = bool(args.urls) or args.file is not None or not sys.stdin.isatty()
    if args.resume and has_args_input:
        print("error: --resume is mutually exclusive with URLs/--file/stdin", file=sys.stderr)
        return EXIT_CODE_USAGE

    # Collect URLs (unless resuming — in resume mode the URLs come from the existing state.jsonl).
    if args.resume:
        try:
            prs = _load_prs_from_state(args.logs_dir / args.resume)
        except InputSourceError as e:
            print(f"error: {e}", file=sys.stderr)
            return EXIT_CODE_USAGE
    else:
        try:
            # Only read stdin when no other input source is present, to avoid
            # accidentally consuming stdin when URLs/--file are already provided.
            use_stdin = (not args.urls and args.file is None and not sys.stdin.isatty())
            stdin = sys.stdin if use_stdin else None
            prs = collect_urls(args=args.urls, file_path=args.file, stdin=stdin)
        except InputSourceError as e:
            print(f"error: {e}", file=sys.stderr)
            return EXIT_CODE_USAGE

    run_id = args.resume or args.run_id or generate_run_id()
    run_dir = args.logs_dir / run_id
    ctx = RunContext(run_id=run_id, run_dir=run_dir)
    logger = make_run_logger(ctx, verbose=args.verbose, quiet=args.quiet)

    if not args.dry_run:
        deleted = retention.sweep(args.logs_dir, max_age_days=args.retention_days,
                                  skip={run_dir})
        if deleted:
            logger.info("retention swept %d old run dir(s)", len(deleted),
                        extra={"step": "retention"})

    try:
        return asyncio.run(_run_with_browser(args, ctx, prs))
    except StorageStateError as e:
        logger.error("storage_state error: %s", e, extra={"step": "auth"})
        return EXIT_CODE_FAILURE


async def _run_with_browser(args, ctx: RunContext, prs) -> int:
    async with open_context(
        storage_state_path=args.storage_state,
        headless=True,
        timeout_seconds=args.timeout_seconds,
    ) as bctx:
        # In dry-run mode the capture is a no-op so we leave zero side effects on disk
        # beyond state.jsonl + summary.json (which the spec considers part of the run record).
        capture_fn = _noop_capture if args.dry_run else capture

        # Build a process_pr closure that knows about the live browser context.
        async def process(ctx_, pr):
            page = await bctx.new_page()
            try:
                pr_page = PRPage(page)
                files_page = FilesPage(page)
                # Authenticated login is cached on ctx after the first PR.
                if ctx_.authenticated_login is None:
                    await pr_page.goto(pr)
                    ctx_.authenticated_login = await pr_page.authenticated_login()
                return await process_pr(
                    ctx_, pr,
                    pr_page=pr_page,
                    files_page=files_page,
                    capture=capture_fn,
                    dry_run=args.dry_run,
                )
            finally:
                await page.close()

        runner_obj = Runner(
            logs_dir=args.logs_dir,
            run_id=ctx.run_id,
            process_pr_fn=process,
            resume=bool(args.resume),
            ctx=ctx,
        )
        # Install signal handlers so Ctrl-C surfaces as CancelledError to process_pr.
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, _cancel_current_task)
            except NotImplementedError:
                pass  # Windows
        return await runner_obj.execute(prs)


def _cancel_current_task():
    task = asyncio.current_task()
    if task is not None:
        task.cancel()


async def _noop_capture(_pr_page, _ctx, _pr, _label):
    """Replacement for `capture` in dry-run mode — leaves no screenshot side effects."""
    return None


def _load_prs_from_state(run_dir: Path):
    import json

    from github_approve_merge.url import parse_pr_url

    state_path = run_dir / "state.jsonl"
    if not state_path.exists():
        raise InputSourceError(
            f"--resume target {run_dir} has no state.jsonl — nothing to resume"
        )
    seen: list[str] = []
    seen_set: set[str] = set()
    for line in state_path.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        pr_slug = rec.get("pr")
        if pr_slug and pr_slug not in seen_set:
            seen.append(pr_slug)
            seen_set.add(pr_slug)

    refs = []
    for slug in seen:
        owner_repo, _, number = slug.partition("#")
        owner, repo = owner_repo.split("/", 1)
        refs.append(parse_pr_url(f"https://github.com/{owner}/{repo}/pull/{number}"))
    return refs
