# github_approve_merge

Approve and merge a batch of GitHub PRs from the command line, driven by a
real browser via Playwright. Logs every step, captures screenshots, and
survives interruption.

## Install

Requires Python 3.12. Recommended: install with `uv`.

```bash
uv venv
uv pip install -e .
uv run playwright install chromium
```

Or with `pipx`:

```bash
pipx install -e .
playwright install chromium
```

## One-time login

```bash
gh-approve-merge auth login
```

This opens a real Chromium window. Sign in to github.com (SSO/2FA all work).
The session is saved to `~/.config/github_approve_merge/storage_state.json`
with mode `0600`. **Treat this file like a credential** — it grants
PR-merging power on your account.

Check it exists later:

```bash
gh-approve-merge auth status
```

## Approve + merge PRs

Pass URLs as args, via a file, or piped on stdin:

```bash
# Args
gh-approve-merge run \
  https://github.com/acme-org/widgets-service/pull/561 \
  https://github.com/acme-org/api-gateway/pull/101

# File
gh-approve-merge run --file ~/prs.txt

# Pipe
gh pr list --json url -q '.[].url' | gh-approve-merge run
```

A `urls.txt` file looks like:

```
# Comments and blank lines OK
https://github.com/owner/repo/pull/1
https://github.com/owner/repo/pull/2
```

## What it does, per PR

1. Loads the PR page.
2. Inspects the state. If merged / closed / draft / locked / conflict / required-check failing / your own PR — records the result and moves on.
3. If approval is needed (and you haven't already approved): goes to the Files-changed tab, picks "Approve", submits.
4. Goes back to the PR.
5. If required checks are still pending, clicks "Merge when ready" (auto-merge). Otherwise clicks the primary "Merge" button, then "Confirm".

It never opens the merge-method dropdown — whatever GitHub pre-selects (your repo default) is what gets used.

## Where artifacts land

```
./logs/<YYYYMMDD-HHMMSS-rand4>/
  run.jsonl         # every log event
  state.jsonl       # per-PR status transitions
  summary.json      # final summary (also written on Ctrl-C)
  screenshots/      # 4 checkpoints per PR + one on each failure
```

Old run dirs are deleted lazily on every `run` (default: keep 10 days).
Override with `--retention-days N`, or run the sweep alone with
`gh-approve-merge gc`.

## Resume after Ctrl-C / crash

```bash
gh-approve-merge run --resume 20260526-143012-7af3
```

The resumed run skips any PR whose latest status is `done` or `skipped-*`.
Each PR is also re-classified against GitHub before action, so a stale
state file cannot cause double-action.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Every PR ended `done` or `skipped-merged` (success-class). |
| 1 | Any PR ended in a warn-class skip (closed/draft/self/needs-more-approvals) or a failure. |
| 2 | Usage / configuration error before any PR was touched. |
| 130 | Interrupted (SIGINT / SIGTERM). |

## Troubleshooting

- **`storage_state not found`** — run `gh-approve-merge auth login`.
- **Selector resolution failed in CI** — GitHub redesigned a widget. Refresh fixtures with `python scripts/refresh_fixtures.py <name>.html <url>` and update the affected selector in `src/github_approve_merge/pages/selectors.py`.
- **Re-running a failed batch** — `gh-approve-merge run --resume <run-id>`.

## Development

```bash
uv pip install -e ".[dev]"
uv run pytest                       # unit + page-object tests
PYTEST_LIVE=1 LIVE_TEST_PR_URL=https://... uv run pytest tests/live
```

See `docs/superpowers/specs/2026-05-26-github-approve-merge-design.md` for the full design.
