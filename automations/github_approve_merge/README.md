# github_approve_merge

Approve and merge a batch of GitHub PRs from the command line, driven by the
GitHub CLI (`gh`). Auto-detects merge queues, gates every merge behind an
explicit confirmation, logs every step, and survives interruption.

## Install

Requires Python 3.12 and the [GitHub CLI](https://cli.github.com/). Recommended: install with `uv`.

```bash
uv venv
uv pip install -e .
```

## Prerequisite: gh auth (SSO-authorized)

This tool uses your existing `gh` login — no separate browser session, no stored
credentials of its own.

```bash
gh auth login            # once; complete SSO authorization for the org in your browser
gh-approve-merge doctor  # checks gh is installed, logged in, and SSO-authorized
```

If the org uses SAML SSO, the token must be authorized for it (GitHub prompts you
in the browser the first time, or via `gh auth refresh`). `doctor` tells you if
something's missing.

## Verbs

```bash
gh-approve-merge approve URLS...   # approve only (no merge)
gh-approve-merge merge   URLS...   # merge only (gated; no approve)
gh-approve-merge run     URLS...   # approve + merge (gated)
```

Pass URLs as args, via `--file`, or piped on stdin:

```bash
gh-approve-merge run \
  https://github.com/acme-org/widgets-service/pull/561 \
  https://github.com/acme-org/api-gateway/pull/101

gh-approve-merge run --file ~/prs.txt
gh pr list --json url -q '.[].url' | gh-approve-merge merge
```

## The merge gate

`merge` and `run` **never merge without your confirmation.** They classify every
PR, print a plan table, and wait:

```
Merge plan:
  acme-org/widgets-service#561    OPEN_MERGEABLE    enqueue (merge queue)
  acme-org/api-gateway#101        OPEN_APPROVABLE   approve → direct merge
Proceed with merge for 2 PR(s)? [y/N]:
```

- `--yes` skips the gate (for scripts/cron).
- `--confirm-each` asks per PR instead of one batch prompt.
- `--dry-run` prints the plan and exits — no approve, no merge, no gate.

The gate is independent of review verdict: an unapproved PR still appears in the
plan with its intended action; you decide.

## What it does, per PR

1. Reads the PR via `gh` and classifies it from structured fields (state, draft,
   locked, mergeable, mergeStateStatus, reviewDecision, author).
2. Terminal states (merged / closed / draft / locked / conflict / required-check
   failing / your own PR) are recorded and skipped.
3. If approval is needed (and `approve`/`run`, and you haven't already approved),
   submits an approval, then re-classifies.
4. Picks the merge action automatically: **enqueue** if the repo uses a merge
   queue, else **direct merge** if mergeable now, else **enable auto-merge** if
   checks are still pending.
5. Executes only after the gate is satisfied.

Direct merges use `--merge-method` (default `merge`; `squash`/`rebase` available),
falling back to an allowed method if the repo disallows the chosen one. Merge-queue
repos ignore the method — the queue decides.

## Where artifacts land

```
./logs/<YYYYMMDD-HHMMSS-rand4>/
  run.jsonl         # every log event
  state.jsonl       # per-PR status transitions
  summary.json      # final summary
```

Old run dirs are deleted lazily on every run (default: keep 10 days). Override
with `--retention-days N`, or run the sweep alone with `gh-approve-merge gc`.

## Resume after Ctrl-C / crash

```bash
gh-approve-merge run --resume 20260601-143012-7af3
```

Skips any PR whose latest status is `done`, `queued`, or `skipped-*`. Each PR is
re-classified against GitHub before action, so a stale state file can't cause
double-action.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Every PR ended `done`, `queued`, `skipped-merged`, or (in `--dry-run`) `would-merge` (success-class). |
| 1 | Any PR ended in a warn-class skip (closed/draft/self/needs-more-approvals/cancelled) or a failure. |
| 2 | Usage / configuration error before any PR was touched. |
| 130 | Interrupted (SIGINT / SIGTERM). |

## Troubleshooting

- **`gh not ready` / `failed-auth`** — run `gh auth login` and authorize the token
  for the org's SSO. Verify with `gh-approve-merge doctor`.
- **`failed-not-found`** — wrong owner/repo/number, or the token can't see the repo.
- **Re-running a failed batch** — `gh-approve-merge run --resume <run-id>`.

## Development

```bash
uv sync --extra dev
uv run pytest                # unit tests (fake gh runner; no network)
PYTEST_LIVE=1 uv run pytest tests/live    # read-only live smoke against a real PR
```

See `docs/superpowers/specs/2026-06-01-github-approve-merge-api-backend-design.md` for the design.

## Security

See [SECURITY.md](SECURITY.md) for the data-handling rules. Highlights:

- The tool stores no credentials of its own — it uses your `gh` token.
- `logs/` contains repo/PR slugs. Use `--redact-logs` to hash them before sharing externally.
- Install the pre-commit guard once: `ln -s ../../scripts/check_no_org_leaks.sh .git/hooks/pre-commit` (run from project root).
```
