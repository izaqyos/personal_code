# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-06-01

### Changed (breaking)

- Backend swapped from Playwright/`storage_state` to the GitHub API via the `gh` CLI.
- Removed `auth login` (no browser). Prerequisite is now `gh auth login` (SSO-authorized token).
- New verbs: `approve`, `merge`, `run`. `merge`/`run` require confirmation (the merge gate)
  unless `--yes`. `--merge-method` (default `merge`). `--confirm-each` for per-PR gating.

### Added

- Auto-detected merge action per PR: enqueue (merge queue) / direct merge / enable auto-merge.
- `auth status` / `doctor` checks `gh` install + login + SSO authorization with an actionable message.
- Statuses `queued` (enqueued) and `cancelled` (gate declined); dry-run reports `would-merge`.
- Merge-method fallback when the repo disallows the chosen method.

### Removed

- Playwright dependency, browser/page-object code, screenshots, HTML fixtures, and the
  fixture-refresh script.

## [0.1.0] - 2026-05-27

### Added

- `auth login` / `auth status` / `run` / `gc` subcommands.
- Batch approve + merge of GitHub PRs via Playwright.
- "Merge when ready" auto-merge when required checks are pending.
- PR-state classifier: MERGED / CLOSED / DRAFT / LOCKED / SELF_AUTHORED / CONFLICT / REQUIRED_FAILING / REQUIRED_PENDING / OPEN_MERGEABLE / OPEN_APPROVABLE plus the ALREADY_APPROVED flag.
- JSONL run log (`run.jsonl`) and per-PR state file (`state.jsonl`).
- Checkpoint screenshots (after-load, after-approve-submit, before-merge-click, after-merge) plus on-failure screenshots.
- 10-day lazy-delete retention sweep on every `run`, also runnable via `gc`.
- `--resume <id>` to retry an interrupted batch; idempotency safety net re-checks GitHub state.
- Three-tier test suite: unit (pure logic), Page Object tests against HTML fixtures, opt-in live smoke (`PYTEST_LIVE=1`).
- `scripts/refresh_fixtures.py` helper for re-snapshotting HTML fixtures after GitHub UI changes.
