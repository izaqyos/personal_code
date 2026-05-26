# `github_approve_merge` — Design

**Status:** Approved 2026-05-26.
**Owner:** Yosi Izaq.
**Scope:** V1. Subsequent versions get their own brainstorm + spec.

## 1. Problem

Approving and merging a handful of PRs across multiple repos by hand is repetitive:
open PR → Files changed → Approve → back to PR → Merge → Confirm — for each PR. When
required CI is still pending you click "Merge when ready" instead. A batch of five PRs
takes ten minutes of focused clicking with no value-add.

We want a CLI that takes a list of PR URLs and does the clicking, with enough
observability (logs, screenshots) to forensically debug any failure, and enough
resilience to survive interruptions mid-batch.

## 2. Goals

- Approve and merge 1..N GitHub PRs in one command.
- Click "Merge when ready" (GitHub auto-merge) when required checks are still pending.
- Skip PRs that can't or shouldn't be merged (already-merged, draft, conflict, etc.)
  with a clear status; don't abort the batch.
- Capture logs (JSONL) and key-checkpoint + on-failure screenshots for every PR.
- Lazy-delete artifacts older than 10 days on each `run`.
- Survive interruption: a killed `run` can be resumed and the resumed `run` must not
  re-approve or double-merge anything.
- Ship with CHANGELOG, README, semantic versioning, structured logging, and a test
  suite (unit + fixture-driven Page Object + opt-in live smoke).

## 3. Non-goals (V1)

- GitHub Enterprise (GHES) support — `github.com` only.
- Adding comments on approve, requesting reviewers, or any review verb other than
  Approve.
- GitHub Search / `gh pr list`-style input (`--from-search`).
- Webhook / Slack notifications.
- Parallel processing of PRs within a single batch.
- Choosing the merge method (squash/merge/rebase) — we always click GitHub's
  pre-selected primary button.

## 4. Locked decisions

| # | Topic | Decision |
|---|-------|----------|
| 1 | Auth | Reused `storage_state.json`. One-time manual headed login (handles SSO/2FA); reused on every subsequent run. |
| 2 | "Merge later" semantics | When required checks are still pending, click GitHub's **"Merge when ready"** (auto-merge) button. |
| 3 | Self-PR | If the running user is the PR author, skip the entire PR with WARN. |
| 4 | Merge method | Use GitHub's pre-selected primary merge button. Never open the dropdown. |
| 5 | Concurrency | Sequential. One browser context, one PR at a time. |
| 6 | Screenshot policy | On failure + four key checkpoints per PR: `after-load`, `after-approve-submit`, `before-merge-click`, `after-merge`. ~4–8 PNGs per PR. |
| 7 | CLI input | Positional args + `--file PATH` + stdin (when not a TTY). Deduped (first occurrence wins), whitespace stripped, validated before any browser work. |
| 8 | Browser mode | Headless at runtime. Explicit `auth login` subcommand opens a headed browser and saves `storage_state.json`. `run` fails fast with a clear message if storage_state is missing or expired. |
| 9 | PR-state edge matrix | Merged → skip OK. Closed-not-merged → skip WARN. Conflict → skip ERROR + screenshot. Required-failing → skip ERROR + screenshot. Required-pending → "Merge when ready". Already-approved-by-me → skip approve, still merge. Draft → skip WARN. Locked → skip ERROR. Batch continues past failures; exit non-zero at end if any failed. |
| 10 | Test strategy | (1) unit tests with mocked browser, (2) Page Object tests against saved HTML fixtures via `file://`, (3) opt-in live smoke via `PYTEST_LIVE=1`. CI runs (1)+(2). |
| 11 | Logging | Stdlib `logging`. JSON-line file handler → `logs/<run_id>/run.jsonl`. Colorized text handler → stdout. Event schema in §7. |
| 12 | Retention | Lazy sweep at start of every `run`, before browser launch. Deletes `logs/<dir>/` whose `mtime` is older than `--retention-days` (default 10) × 86400 s. Skips the in-progress run dir. `storage_state.json` lives outside `logs/` and is structurally unreachable by the sweep. |
| 13 | Resume | `logs/<run_id>/state.jsonl` written per PR (`queued`, `in_progress`, `done`, `skipped-*`, `failed-*`). `run --resume <run_id>` reuses that dir and skips entries whose latest status is `done` or `skipped-*`. Each PR's flow still re-checks GitHub state at start — idempotency safety net so a stale or wrong state file can't cause double-action. |
| 14 | Exit codes | `0` if every PR ended `done` or `skipped-merged` (idempotent success). `1` if any PR ended `skipped-{closed,draft,self,needs-more-approvals}` (WARN-class) or `failed-*` (ERROR-class). `2` for argv/config errors before any PR processing. `130` on SIGINT/SIGTERM (POSIX convention). |
| 15 | Future hooks | Strict YAGNI. V1 ships approve + merge. New verbs/inputs/notifications come in separate brainstorm cycles. |

## 5. Architecture

Layered, with the Playwright Page Object Model:

```
github_approve_merge/
├── src/github_approve_merge/
│   ├── __init__.py            # __version__
│   ├── __main__.py            # python -m github_approve_merge → cli.main()
│   ├── cli.py                 # argparse: subcommands auth/run/gc
│   ├── config.py              # paths, defaults, constants
│   ├── url.py                 # parse + validate PR URLs → PRRef(owner,repo,number)
│   ├── input_sources.py       # collect URLs from argv + --file + stdin, dedupe
│   ├── auth.py                # login flow, storage_state.json load/save/expired-check
│   ├── browser.py             # async_playwright lifecycle, context factory
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── selectors.py       # central selector constants
│   │   ├── pr_page.py         # PRPage Page Object
│   │   └── files_page.py      # FilesPage Page Object
│   ├── actions.py             # process_pr() — composes pages, owns the per-PR flow
│   ├── pr_state.py            # PRState enum, StateFlag enum, detect_state()
│   ├── runner.py              # Runner: batch loop, state.jsonl, summary, signal handler
│   ├── logging_setup.py       # JSON file handler + colored stdout handler + LoggerAdapter
│   ├── screenshots.py         # capture(page, ctx, label) → Path
│   └── retention.py           # sweep(logs_root, max_age_days, skip)
├── tests/
│   ├── unit/                  # url, input_sources, pr_state, retention, runner (mocked browser)
│   ├── pages/                 # Page Object tests against fixtures via file://
│   ├── live/                  # PYTEST_LIVE=1 smoke
│   ├── fixtures/html/         # 11 snapshotted HTML pages (see §10)
│   └── conftest.py            # PYTEST_LIVE gate, browser fixture
├── docs/superpowers/specs/    # this file
├── docs/superpowers/plans/    # writing-plans output
├── scripts/
│   └── refresh_fixtures.py    # documented helper to re-snapshot fixtures when GitHub UI drifts
├── pyproject.toml             # uv-managed; deps: playwright, pytest, pytest-asyncio
├── README.md
├── CHANGELOG.md               # Keep-a-Changelog format
├── .python-version            # 3.12
└── .gitignore                 # logs/, storage_state.json, .venv/
```

**Per-PR data flow:**

```
CLI args + --file + stdin → input_sources → [PRRef, …]
  → retention.sweep(logs_root, days, skip={current_run_dir})
  → browser.launch(storage_state)
  → for each PRRef:
      runner.process(pr):
        state.jsonl ← {status: in_progress}
        PRPage.goto(pr) → screenshot "after-load"
        state, flags = detect_state(page, me=ctx.authenticated_login)

        # Phase 1: terminal classification on initial state.
        if state in {MERGED, CLOSED, DRAFT, LOCKED, SELF_AUTHORED,
                     CONFLICT, REQUIRED_FAILING}:
          state.jsonl ← {status: <mapped from state>} → next PR

        # Phase 2: approve if needed.
        if state == OPEN_APPROVABLE and ALREADY_APPROVED not in flags:
          FilesPage: open → select_approve → submit_review
          screenshot "after-approve-submit"
          PRPage.goto(pr); state, flags = detect_state(...)  # refresh
          # The post-approve state can be anything; re-run terminal classification.
          if state in {MERGED, CLOSED, DRAFT, LOCKED, CONFLICT, REQUIRED_FAILING}:
            state.jsonl ← {status: <mapped>} → next PR
          if state == OPEN_APPROVABLE:
            # Approve submitted but PR still needs more reviewers.
            state.jsonl ← {status: skipped-needs-more-approvals} → next PR

        # Phase 3: merge.
        screenshot "before-merge-click"
        if state == REQUIRED_PENDING:
          PRPage.click_merge_when_ready()
        else:  # OPEN_MERGEABLE
          PRPage.click_merge_and_confirm()
        PRPage.wait_for_merged()
        screenshot "after-merge"
        state.jsonl ← {status: done}
  → write summary.json
  → print summary table
  → exit 0 | 1
```

The Page Objects own *how* to click things. `actions.process_pr` owns *what* happens
per PR. `runner` owns the batch loop, state file, and signal handling. None of these
layers know about the others' internals.

## 6. CLI surface

```text
gh-approve-merge --help
gh-approve-merge --version

gh-approve-merge auth login   [--storage-state PATH]
gh-approve-merge auth status  [--storage-state PATH]

gh-approve-merge run [URL ...]
                     [--file PATH]            # one URL per line, # comments, blanks OK
                                              # stdin auto-detected when not a TTY
                     [--retention-days N]     # default 10
                     [--storage-state PATH]
                     [--logs-dir PATH]        # default ./logs
                     [--run-id ID]            # default YYYYMMDD-HHMMSS-<rand4>
                     [--resume ID]            # reuse logs/ID/state.jsonl, skip done/skipped-*
                     [--dry-run]              # parse + classify state, no clicks
                     [--timeout-seconds N]    # per-step Playwright timeout, default 30
                     [--verbose | --quiet]

gh-approve-merge gc  [--logs-dir PATH] [--retention-days N]
```

**Default paths:**
- `storage_state.json` → `~/.config/github_approve_merge/storage_state.json` (XDG-style,
  permissions `0600` on write).
- `logs/` → cwd-relative `./logs/`.

**Conflict rules:**
- Args + `--file` + stdin all merge into one deduped list. First occurrence wins on
  ordering.
- `--resume <ID>` is mutually exclusive with `[URL ...]` and `--file`/stdin. Args + resume
  together → exit `2` with a clear error.
- `--dry-run` skips the retention sweep too (no side effects of any kind).
- `auth status` doesn't open a browser; it does a HEAD request to
  `https://github.com/settings/profile` with the saved cookies and reports
  valid / expired / missing.

## 7. On-disk layout, JSONL schemas

### 7.1 Per-run directory

```
logs/
└── 20260526-143012-7af3/                  # <run_id>
    ├── run.jsonl                          # all log events
    ├── state.jsonl                        # per-PR status (append-only)
    ├── summary.json                       # written at end (or on signal)
    └── screenshots/
        ├── acme-org__widgets-service__561__01-after-load.png
        ├── acme-org__widgets-service__561__02-after-approve-submit.png
        ├── acme-org__widgets-service__561__03-before-merge-click.png
        ├── acme-org__widgets-service__561__04-after-merge.png
        └── acme-org__api-gateway__101__error-conflict-detected.png
```

**Screenshot slug:** `<owner>__<repo>__<pr_number>__<NN>-<label>.png` for checkpoints
(double-underscore between segments to disambiguate single-underscore repo names),
`<owner>__<repo>__<pr_number>__error-<reason>.png` for errors (no counter — error
images sort to the end).

### 7.2 `run.jsonl` event schema

One JSON object per line.

Required keys: `ts` (UTC ISO-8601 with millisecond precision and a trailing `Z`),
`level`, `run_id`, `step`, `msg`.

Optional keys: `pr` (`owner/repo#N`), `state`, `screenshot` (path relative to the
run dir), `duration_ms`, `exception` (object: `{type, repr, traceback}`).

Example:

```json
{"ts":"2026-05-26T14:30:13.421Z","level":"INFO","run_id":"20260526-143012-7af3","pr":"acme-org/widgets-service#561","step":"after-load","msg":"PR page loaded","state":"OPEN_APPROVABLE","duration_ms":1842}
{"ts":"2026-05-26T14:30:21.044Z","level":"ERROR","run_id":"20260526-143012-7af3","pr":"acme-org/api-gateway#101","step":"detect-state","msg":"merge conflict detected","state":"CONFLICT","screenshot":"screenshots/acme-org__api-gateway__101__error-conflict-detected.png"}
```

### 7.3 `state.jsonl` schema

Append-only, one line per state transition per PR.

```json
{"ts":"2026-05-26T14:30:12.901Z","pr":"acme-org/widgets-service#561","status":"queued"}
{"ts":"2026-05-26T14:30:13.420Z","pr":"acme-org/widgets-service#561","status":"in_progress"}
{"ts":"2026-05-26T14:30:38.110Z","pr":"acme-org/widgets-service#561","status":"done","duration_ms":25210}
```

Allowed `status` values, grouped by **exit-class** (the single source of truth that
maps a status to its exit-code contribution; encoded in `actions.STATUS_TO_EXIT_CLASS`):

- **Progress (non-terminal):** `queued`, `in_progress`.
- **Terminal — success class (exit 0 contribution):** `done`, `skipped-merged`.
- **Terminal — warn class (exit 1 contribution):** `skipped-closed`, `skipped-draft`,
  `skipped-self`, `skipped-needs-more-approvals`.
- **Terminal — error class (exit 1 contribution):** `failed-conflict`,
  `failed-required-check`, `failed-locked`, `failed-interrupted`, `failed-exception`.

`skipped-needs-more-approvals` is recorded when, after the tool submits an Approve,
the post-approve re-detect shows the PR still has unmet review requirements (typical
in repos that require 2+ approvals). The tool can't help further; user needs an
additional reviewer.

`skipped-already-approved` (without the `-done` suffix) is **not** a terminal status
in `state.jsonl`. ALREADY_APPROVED is a `StateFlag` that bypasses the approve step; the
PR continues to the merge step and ends in `done` or one of the `failed-*` statuses.

### 7.4 `summary.json` schema

Written on clean exit and on signal-handled shutdown.

```json
{
  "run_id": "20260526-143012-7af3",
  "started": "2026-05-26T14:30:12.901Z",
  "ended":   "2026-05-26T14:32:48.110Z",
  "exit_code": 1,
  "counts": {"done": 3, "skipped": 1, "failed": 1},
  "prs": [{"pr":"...","status":"done","duration_ms":25210}, ...]
}
```

### 7.5 `storage_state.json`

Lives at `~/.config/github_approve_merge/storage_state.json`. Written with
`chmod 0600`. Contains cookies + localStorage as serialized by
`BrowserContext.storage_state()`.

## 8. Logging, screenshots, retention internals

**Logging.** One `logging.Logger` named `gam`. Attached at `run` startup:

1. `JSONLineFileHandler` → `logs/<run_id>/run.jsonl`. Custom `JSONFormatter` produces
   the schema in §7.2 from `LogRecord` plus any `extra={…}` passed at the call site.
2. `ColorConsoleHandler` (stdout). Format:
   `HH:MM:SS LEVEL [pr=owner/repo#N step=…] msg`. Level → ANSI color.

`--verbose` → DEBUG on both handlers. `--quiet` → WARNING on stdout; file handler
stays at DEBUG always so post-mortem is always rich. A small `LoggerAdapter` injects
`run_id`, `pr`, and `step` from a `RunContext` dataclass so action code stays terse
(`log.info("approve submitted")`).

**Dependencies.** Stdlib only for logging (no `rich`, no `structlog`). ~30 lines for
the JSON formatter and color console handler. Aligns with the existing `gemini_etl`
posture in this repo.

**Screenshots.** `screenshots.capture(page, ctx, label) -> Path`:

- Writes `logs/<run_id>/screenshots/<slug>.png`. `fullPage=True` always — the merge
  widget can be far below the fold on PRs with many checks.
- Returns the **relative** path so log events stay portable when a run dir is moved
  or zipped.
- Auto-prepends a two-digit counter per `(run_id, pr_ref)` for checkpoint labels.
  Error labels skip the counter and use `error-<reason>`.
- Never raises: a screenshot failure is logged at WARN with the original exception
  attached but does not interrupt the per-PR flow.

**Retention.** `retention.sweep(logs_root: Path, max_age_days: int, skip: set[Path])
-> list[Path]`:

- Walks immediate children of `logs_root`.
- Eligible only if all of: it's a directory; its name matches
  `^\d{8}-\d{6}-[a-f0-9]{4}$`; `time.time() - st_mtime > max_age_days * 86400`;
  not in `skip` (which always contains the current run dir).
- Deletes via `shutil.rmtree(onerror=…)` that logs but doesn't raise.
- Returns deleted paths so the caller logs the count at INFO.
- Called once at the start of `run` (after argv parsing, before launching Playwright)
  and standalone via `gc`.
- `storage_state.json` is outside `logs_root` entirely. Untouchable by the sweep
  by construction.

**Signal handling.** Runner installs a SIGINT/SIGTERM handler that:

1. Marks the current `in_progress` PR (if any) as `failed-interrupted` in `state.jsonl`.
2. Writes `summary.json` with `exit_code: 130`.
3. Closes the browser context.
4. Exits 130.

This makes `--resume` reliable after Ctrl-C.

## 9. PR-state detection & selector strategy

**Selector preference order, for every element:**

1. Role + accessible name (`page.get_by_role("button", name=…)`). Stable across
   GitHub redesigns because aria roles/labels survive visual refreshes.
2. `data-` attributes (`[data-testid=…]`, `[data-disable-with=…]`).
3. CSS class — last resort, must carry a code comment explaining why.

All selectors live in `pages/selectors.py` as named constants. Never inlined in
action code. When GitHub changes, you grep one file.

**`detect_state(page, me) -> (PRState, set[StateFlag])`** runs after the PR page
has loaded. Checks run in the order below (cheapest / most decisive first); the
first matching check wins:

| Order | Check | Signal | Result |
|---|---|---|---|
| 1 | Closed status badge in header | `State.MERGED` badge | `MERGED` |
| 2 | | `State.CLOSED` badge (and not merged) | `CLOSED` |
| 3 | Draft? | "Draft" badge in header | `DRAFT` |
| 4 | Locked? | "This conversation has been locked" notice in merge box | `LOCKED` |
| 5 | Authored by me? | author handle == `me` | `SELF_AUTHORED` |
| 6 | Merge conflict? | "This branch has conflicts" in mergeability widget | `CONFLICT` |
| 7 | Required check failing? | "Required statuses must pass" with red `x` icon | `REQUIRED_FAILING` |
| 8 | Required check pending? | "Required statuses must pass" with yellow dot + "Merge when ready" button present | `REQUIRED_PENDING` |
| 9 | Already approved by me? (flag, doesn't short-circuit) | reviewers panel shows my login with `Approved` badge | adds `ALREADY_APPROVED` to flag set |
| 10 | Default: merge available | merge button present and enabled | `OPEN_MERGEABLE` |
| 11 | Default: approve form available | only the approve form is interactable | `OPEN_APPROVABLE` |

**Authenticated login lookup.** Read once at session start from a stable element
(e.g. `meta[name="user-login"]` on any GitHub page) and cached on `RunContext` for
the self-PR check.

## 10. Testing

**Unit tests (`tests/unit/`):**

- `test_url.py` — valid and invalid PR URLs; trailing slashes; `/files`, `/commits`,
  `#discussion_r…` suffixes normalize to the bare PR URL; non-`github.com` hosts
  raise a clear error.
- `test_input_sources.py` — args + file + stdin merging; dedupe preserves first
  occurrence order; `#` comment lines and blank lines in files; `--resume` ⊥
  explicit URLs.
- `test_pr_state.py` — every row of the state matrix has a fixture and an assertion.
  Runs Playwright against the HTML fixtures via `file://`.
- `test_retention.py` — tempdir with run dirs spanning mtimes 1–15 days, the
  current-run dir, a stray file, and a wrong-format dir name; assert exactly the
  right dirs are deleted; a misplaced `storage_state.json` under `logs/` survives
  because the name pattern doesn't match.
- `test_runner.py` — `FakeBrowser`+`FakePage` feed canned states; assert
  `state.jsonl` content, `summary.json` shape, signal-handler behavior, `--resume`
  skipping logic, and exit-code mapping.

**Page Object tests (`tests/pages/`):**

- Saved HTML fixtures served via `file://`. One per state the detector must
  recognize, plus separate Files-page fixtures for the FilesPage POs:

  | Fixture | Covers |
  |---|---|
  | `pr_mergeable.html` | `OPEN_MERGEABLE` (merge button enabled, no required checks pending) |
  | `pr_needs_approval.html` | `OPEN_APPROVABLE` (merge disabled, "Review required" sidebar) |
  | `pr_ci_pending.html` | `REQUIRED_PENDING` (yellow CI, "Merge when ready" button present) |
  | `pr_required_check_failing.html` | `REQUIRED_FAILING` |
  | `pr_conflict.html` | `CONFLICT` |
  | `pr_merged.html` | `MERGED` |
  | `pr_closed.html` | `CLOSED` (not merged) |
  | `pr_draft.html` | `DRAFT` |
  | `pr_locked.html` | `LOCKED` |
  | `pr_self.html` | `SELF_AUTHORED` (PR by `me`) |
  | `pr_already_approved_by_me.html` | `OPEN_MERGEABLE` + `ALREADY_APPROVED` flag |
  | `files_can_approve.html` | FilesPage with Approve radio interactable |
  | `files_already_approved.html` | FilesPage with prior approval visible |
- For each: launch Playwright, drive the relevant Page Object method, assert it
  locates exactly one visible element with the expected enabled state. Buttons are
  no-op in fixture mode — we verify the locator resolves correctly, not the click
  effect (no real backend).

**Fixture refresh.** `scripts/refresh_fixtures.py` (documented in
CONTRIBUTING/README, not part of V1 product surface) navigates a logged-in browser
to the canonical pages and writes `page.content()` to disk. Manual operation;
expected when CI selector tests fail after a GitHub redesign.

**Live smoke (`tests/live/`):** opt-in via `PYTEST_LIVE=1`. One test that
approves + merges a throwaway PR in a sandbox repo. Requires `LIVE_TEST_PR_URL`
env. Not run in CI. Run manually before each release.

**CI:** `pytest -m "not live"`. Target ≤30 s wall clock.

## 11. Mandatory deliverables (Yosi-stated, not optional)

- `README.md` — what it is, install (`uv tool install …` or `pipx install .`), `auth
  login` walkthrough, `run` examples, troubleshooting (where logs/screenshots land,
  how to read state.jsonl), security note (storage_state.json contains your session;
  treat as a credential).
- `CHANGELOG.md` — Keep-a-Changelog format. V1 release entry on first tag.
- Semantic versioning. `__version__` in `src/github_approve_merge/__init__.py`.
  Tag `v0.1.0` on first working version; `v1.0.0` once selectors hold up for one
  full week of daily use.
- Structured logging (§8).
- Test suite (§10).
- Interruption resilience (Q13 / §7.3 / signal handler in §8).

## 12. Out-of-scope risks (acknowledged, not solved here)

- **Selector drift.** GitHub redesigns will break Page Objects. Mitigation: tiered
  selector strategy (role+name preferred), fixture-driven tests catch breakage in
  CI before a `run`, `scripts/refresh_fixtures.py` is the documented recovery path.
- **GHES support.** Out of scope for V1. URL parser rejects non-`github.com` hosts
  with a clear message so the failure is loud, not silent.
- **Race with manual action.** If a user merges a PR in their browser while the
  tool is processing it, the tool will detect `MERGED` on re-check after approve
  (or click-merge will fail and the per-PR flow will record `failed-exception`).
  Acceptable; the idempotency layer guarantees no double-action.
- **Network flakiness.** Playwright per-step timeout (default 30 s, configurable
  via `--timeout-seconds`). Single failure → that PR ends `failed-exception`; the
  batch continues. No automatic retry in V1 — re-run with `--resume` to retry.

## 13. Glossary

- **PR ref:** `owner/repo#N` (e.g. `acme-org/widgets-service#561`).
- **Run ID:** `YYYYMMDD-HHMMSS-<rand4>`, e.g. `20260526-143012-7af3`. Stable per
  batch invocation. Used as `logs/<run_id>/`.
- **Page Object:** a class encapsulating selectors + behaviour for one screen
  (here: `PRPage`, `FilesPage`).
- **Lazy delete:** retention sweep piggybacked on every `run` start; no daemon, no
  cron required.
- **Idempotency safety net:** in addition to `state.jsonl` skip-on-resume, every
  per-PR flow re-reads GitHub state at the top and short-circuits if the PR is
  already in a terminal state.
