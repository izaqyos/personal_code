# `github_approve_merge` v2 — API Backend — Design

**Status:** Approved 2026-06-01.
**Owner:** Yosi Izaq.
**Supersedes:** the Playwright/browser approach in `2026-05-26-github-approve-merge-design.md` (V1).
**Scope:** v2. Replaces the browser backend with the GitHub API via the `gh` CLI.

## 1. Problem

V1 drives a headless Chromium with a reused `storage_state.json` (locked decision #1).
Two live sessions on 2026-05-31 / 2026-06-01 proved that assumption is broken in this
environment:

1. **SSO expiry.** The github.com session worked but the SAML SSO authorization for the
   `perimeter-81` org lapsed. Org-gated pages (e.g. `/files`) redirected to a "Single
   sign-on to Perimeter81" interstitial, so the approve radio never existed and
   `radio.check()` timed out after 30s → opaque `failed-exception`.
2. **SSO blocked in automation.** The IdP / device policy will not let SSO be completed
   inside the Playwright-launched browser at all, so `storage_state` can never be
   refreshed for org-gated write actions.

Meanwhile, the GitHub CLI (`gh`) — authenticated with an SSO-authorized token — read and
merged the same PRs cleanly with no browser. The fix is to make the API the backend.

A secondary V1 defect found in the same session: dry-run reported `skipped-merged` (which
means "already merged") for PRs it would *act on*, telling the user the opposite of the
truth. Fixed on branch `fix/dry-run-would-merge-label` (`would-merge`); that behavior
carries into v2.

## 2. Goals

- Approve and/or merge 1..N GitHub PRs in one command, via the GitHub API (`gh`).
- No browser, no `storage_state.json`, no SSO-in-automation. Reuse `gh`'s existing auth.
- Handle the real merge spectrum: merge-queue repos (enqueue), directly-mergeable repos
  (direct merge), and pending-checks (enable auto-merge / enqueue).
- **Explicit human control of every merge.** Nothing merges autonomously; merge always
  passes a confirmation gate, independent of review verdict.
- Batch-first: a list of PRs, one plan, one confirmation.
- Clear, typed failures (`failed-auth` with an actionable message) instead of opaque
  timeouts or misclassifications.
- Keep V1's observability/resilience: JSONL run/state logs, `summary.json`, `--resume`
  with a GitHub re-check, `--redact-logs`, retention sweep.
- Wire into `launcher.sh` (submenu) and `pr_reviewer_agent.md` (review → gated-merge handoff).

## 3. Non-goals (v2)

- GitHub Enterprise (GHES) — `github.com` only.
- Review verbs other than Approve (no comment/request-changes/request-reviewers).
- GitHub Search / `--from-search` input.
- Webhook / Slack notifications.
- Parallel processing within a batch (stays sequential).
- A native Python GitHub client / direct httpx calls — we shell out to `gh` (decision §4.2).
- Browser fallback — v2 removes Playwright entirely (decision §4.1).

## 4. Locked decisions

| # | Topic | Decision |
|---|-------|----------|
| 1 | Backend positioning | **API replaces Playwright.** Delete `browser.py`, `pages/`, `screenshots.py`, `auth.py`, HTML fixtures, `tests/pages/`, `scripts/refresh_fixtures.py`, the `auth login` subcommand, and the Playwright dependency. No browser fallback. |
| 2 | API access | **Shell out to `gh`.** Reuse `gh`'s SSO-authorized token, keyring, and multi-account handling — zero auth code in this tool. `run`/`merge` require `gh` on PATH and a logged-in account. |
| 3 | Merge logic | **Auto-detect per PR.** If the base branch has a merge queue → enqueue (GraphQL `enqueuePullRequest`). Else if mergeable now → direct merge. Else if required checks pending → enable auto-merge. |
| 4 | Direct-merge method | Default **merge commit**; `--merge-method {merge,squash,rebase}` overrides. If the chosen method is disallowed by the repo, fall back to an allowed method and log it. (Merge-queue repos ignore this — the queue dictates strategy.) |
| 5 | Merge gate | **Explicit human control.** `merge`/`run` print a plan table and block for confirmation before any merge, regardless of review verdict. `--yes` bypasses (opt-in, for scripts/cron). `--confirm-each` gates per-PR. `--dry-run` prints the plan and exits without gating or acting. |
| 6 | Verbs | `approve` (approve only), `merge` (merge only, gated), `run` (classify → optional approve → gated merge). `--no-approve` on `run` skips the approve step. |
| 7 | Classification | Pure function over one `gh pr view --json` call plus a merge-queue probe. No DOM, no rendering race. See §6. |
| 8 | Auth preflight | `auth status` (kept, repurposed) / `doctor`: checks `gh` on PATH, `gh auth status`, and token SSO-authorization; prints exactly what is wrong. Replaces the V1 "storage_state present?" check. |
| 9 | Observability | Keep JSONL `run.jsonl` + per-PR `state.jsonl` + `summary.json`. Screenshots removed (no browser). |
| 10 | Resilience | Keep `--resume <run_id>` (skip `done`/`skipped-*`, re-check GitHub before acting), `--redact-logs` (hash PR slugs), retention sweep (default 10 days, also via `gc`). |
| 11 | Dry-run labels | Actionable states report `would-merge` (success-class); terminal states keep their real status (`skipped-merged` only for genuinely-merged). Carried from the V1 fix. |
| 12 | Integrations | Rewrite the `launcher.sh` submenu; add a "Handoff to merger" section to `pr_reviewer_agent.md`. See §9. |
| 13 | Data handling | All runtime artifacts (logs/summaries) stay local; they reference `perimeter-81` repo/PR slugs. `--redact-logs` hashes slugs for shareable artifacts. No tokens or customer data are ever written. |

## 5. Architecture & module layout

```
src/github_approve_merge/
  gh_client.py     NEW  thin wrapper over `gh` subprocess: build argv, run, parse JSON,
                        map failures to typed errors. Injectable runner for tests.
  pr_state.py      REWRITTEN  classify from API fields (was DOM scraping).
  actions.py       CHANGED   process_pr flow calls gh_client; adds the merge gate.
  cli.py           CHANGED   verbs approve/merge/run + auth status/doctor + gc; drops auth login.
  runner.py        KEPT      batch, resume, state.jsonl, summary.json.
  logging_setup.py KEPT
  retention.py     KEPT
  input_sources.py KEPT
  url.py           KEPT
  config.py        KEPT/trimmed (drop storage_state/headless knobs).

DELETED: browser.py, auth.py, pages/, screenshots.py,
         tests/fixtures/html/, tests/pages/, scripts/refresh_fixtures.py.
```

**`gh_client.py` is the single seam.** It owns every `gh` invocation, parses stdout JSON,
and translates non-zero exits / stderr into typed exceptions (`GhNotFound`, `GhAuthError`,
`GhError`). All other modules speak Python objects, never subprocess details. Unit tests
inject a fake runner that returns canned `(stdout, stderr, returncode)` — no real `gh`.

**Preflight.** `run`/`merge`/`approve` first call a preflight: `gh` on PATH and
`gh auth status` succeeds. On failure → exit with a clear `failed-auth`-class message
pointing at `gh auth login` / SSO authorization, *before* touching any PR.

## 6. PR classification (`pr_state.py`)

Inputs per PR:
- `gh pr view <n> --repo <owner>/<repo> --json number,state,isDraft,locked,mergeable,mergeStateStatus,reviewDecision,author,baseRefName`
- Merge-queue probe (GraphQL): `repository.mergeQueue(branch: <baseRefName>)` non-null ⇒ queue.
- Authenticated login: `gh api user --jq .login` (cached per run).
- Already-approved-by-me: from `reviewDecision` + `gh pr view --json reviews` (latest review by `me` is `APPROVED`).

Mapping to the existing terminal states + `ALREADY_APPROVED` flag:

| API signal | State |
|---|---|
| `state == MERGED` | `MERGED` → skip OK (`skipped-merged`) |
| `state == CLOSED` | `CLOSED` → skip WARN (`skipped-closed`) |
| `isDraft` | `DRAFT` → skip WARN (`skipped-draft`) |
| `locked` | `LOCKED` → skip ERROR (`failed-locked`) |
| `author.login == me` | `SELF_AUTHORED` → skip WARN (`skipped-self`) |
| `mergeable == CONFLICTING` | `CONFLICT` → skip ERROR (`failed-conflict`) |
| required checks failing (`mergeStateStatus` BLOCKED w/ failed contexts) | `REQUIRED_FAILING` → skip ERROR (`failed-required-check`) |
| checks pending (`BEHIND`/`UNSTABLE`/queued) | `REQUIRED_PENDING` → auto-merge / enqueue |
| `reviewDecision != APPROVED` and not approved-by-me | `OPEN_APPROVABLE` |
| `reviewDecision == APPROVED`, mergeable | `OPEN_MERGEABLE` |
| latest review by me is APPROVED | `ALREADY_APPROVED` flag (combines with OPEN_*) |

`gh` failures never produce a state — they raise, and `process_pr` records
`failed-auth` / `failed-not-found` / `failed-exception`.

> Note: `mergeStateStatus` is a GraphQL enum (`CLEAN`, `BLOCKED`, `BEHIND`, `DIRTY`,
> `UNSTABLE`, `HAS_HOOKS`, `DRAFT`, `UNKNOWN`). The classifier maps these explicitly; an
> unrecognized value is treated conservatively as `REQUIRED_PENDING` (safe: it routes to
> the gated auto-merge/enqueue path, never a blind direct merge).

## 7. Per-PR flow, merge gate, and batch

`process_pr(pr, *, approve: bool, do_merge: bool, method, gate)`:

1. Classify (§6).
2. If terminal state → record status, continue (batch never aborts).
3. If `dry_run` → record the dry-run label (`would-merge` for actionable states) and continue.
4. If `OPEN_APPROVABLE` and not `ALREADY_APPROVED` and `approve` → `gh pr review --approve`, re-classify.
   - If still `OPEN_APPROVABLE` after our approval (needs more approvals) → `skipped-needs-more-approvals`.
5. **Merge gate** (only if `do_merge`): the chosen merge action is computed but **not executed**
   until the gate is satisfied (plan confirmed, or `--yes`, or per-PR confirm).
6. Execute the merge action by decision §4.3: enqueue (GraphQL) / direct merge (`gh pr merge`) /
   enable auto-merge. Record `done` (or `queued` for merge-queue — a success-class terminal status).

**Gate mechanics.** The runner collects all per-PR plans first, prints one table
(`PR | state | intended action`), then asks once: `Proceed with merge for N PR(s)? [y/N]`.
`--confirm-each` asks per PR at step 5. `--yes` skips. `--dry-run` prints the table and
exits before any gate or action. The gate is **independent of review verdict** — an
unapproved or not-yet-green PR still appears in the plan with its intended action (which may
be "approve → enqueue" or "skip: needs checks"); the human decides.

**Statuses & exit classes** (extends V1 `actions.py`):
- Success-class (exit 0): `done`, `queued`, `skipped-merged`, `would-merge`.
- Warn-class (exit 1): `skipped-closed`, `skipped-draft`, `skipped-self`, `skipped-needs-more-approvals`, `cancelled` (user declined the gate).
- Error-class (exit 1): `failed-conflict`, `failed-required-check`, `failed-locked`, `failed-auth`, `failed-not-found`, `failed-exception`, `failed-interrupted`.
- `2` usage/config error before processing; `130` on SIGINT/SIGTERM.

> Declining the gate records `cancelled` for the un-acted PRs (warn-class, exit 1) so the
> outcome is unambiguous in `summary.json` — "nothing merged because you said no", not a silent success.

## 8. CLI surface

```
gh-approve-merge auth status        # gh on PATH? logged in? SSO authorized?  (alias: doctor)
gh-approve-merge approve [opts] URLS...    # approve only
gh-approve-merge merge   [opts] URLS...    # merge only (gated)
gh-approve-merge run     [opts] URLS...    # classify -> [approve] -> gated merge
gh-approve-merge gc [--retention-days N]   # retention sweep only
```

Options on approve/merge/run: `--file PATH`, stdin (non-TTY), `--dry-run`,
`--merge-method {merge,squash,rebase}` (default `merge`), `--yes`, `--confirm-each`,
`--no-approve` (run only), `--resume ID`, `--redact-logs`, `--retention-days N`,
`--logs-dir DIR`, `--run-id ID`, `--verbose | --quiet`. Inputs deduped (first wins),
whitespace-stripped, validated before any `gh` call.

## 9. Integrations

### 9.1 `launcher.sh` (option [9] → `handle_github_merger_menu`)

Rewrite the submenu (`show_github_merger_menu` + handler) — remove the browser-login item,
keep the dry-run-then-confirm idiom used elsewhere in the launcher:

| Key | Label | Command |
|---|---|---|
| 1 | Doctor (gh + SSO) | `uv run gh-approve-merge auth status` |
| 2 | Dry-Run (plan) | `uv run gh-approve-merge run --dry-run <input>` |
| 3 | Approve only | `uv run gh-approve-merge approve <input>` |
| 4 | Merge (gated) | `uv run gh-approve-merge merge <input>` |
| 5 | Run = approve + merge (gated) | `uv run gh-approve-merge run <input>` |
| 6 | Cleanup Old Logs (GC) | `uv run gh-approve-merge gc` |
| 0 | Back | — |

Input sub-prompt (paste URLs / file path) and the `--redact-logs` prompt stay as today.
The merge gate is handled by the tool itself (interactive `[y/N]`), so the launcher does
**not** pass `--yes`. The `$GITHUB_MERGER_VENV` reference and the browser-login copy are removed.

### 9.2 `pr_reviewer_agent.md`

Add a **"Handoff to merger"** section near the Final Verdict:

- **Hard rule:** the reviewer agent **never merges and never approves** autonomously. It
  produces a verdict only.
- On a verdict of "Approved for merge" (and *only* with the human's go-ahead), it writes the
  reviewed PR URL(s) to a list file and surfaces the exact command:
  `cd $GITHUB_MERGER_DIR && uv run gh-approve-merge merge --file <list>` (or `run` to also
  approve). That command runs behind the tool's confirmation gate.
- This keeps explicit human control end-to-end and is batch-friendly (the agent commonly
  reviews several PRs at once; they flow into one gated merge).

## 10. Testing

- **Unit:** inject a fake `gh` runner returning canned JSON/exit codes. Cover the classifier
  (every row of §6), the flow (approve→re-check, terminal short-circuits), the merge-action
  selector (queue vs direct vs auto-merge), and the gate (confirm / decline / `--yes` /
  `--confirm-each`). No network.
- **Fixtures:** small sanitized JSON captures of real `gh pr view --json` output replace the
  HTML fixtures.
- **Live smoke:** opt-in `PYTEST_LIVE=1`, read-only `gh pr view` against a real PR.
- CI runs unit + fixture tests.

## 11. Migration / rollout

- Bump to `0.2.0`. CHANGELOG documents the backend swap, removed `auth login`, new verbs,
  and the merge gate as a breaking change.
- README rewrite: prerequisites become "`gh` installed and `gh auth login` (SSO-authorized)"
  instead of `auth login`. Document the gate and `--yes`.
- The V1 `fix/dry-run-would-merge-label` commit is folded in (its `would-merge` behavior is
  decision §4.11).
```
