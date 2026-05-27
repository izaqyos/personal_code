# Security and confidentiality

This tool drives a real GitHub browser session against private organization
repositories. Its runtime artifacts can leak information about those repos.
This document is the operating manual for keeping that data inside your machine.

## Sensitive artifacts (created at runtime)

| Artifact | What it contains | Where it lives | Mitigation in V1 |
|---|---|---|---|
| `~/.config/github_approve_merge/storage_state.json` | Browser session cookies for github.com — equivalent to your login | `$XDG_CONFIG_HOME/github_approve_merge/` | Written `chmod 0600`. Treat like a credential. |
| `logs/<run_id>/run.jsonl` | PR slugs (`owner/repo#N`), states, durations, exception messages | `./logs/` (gitignored) | Auto-deleted after `--retention-days` (default 10). |
| `logs/<run_id>/state.jsonl` | PR slug + status transitions | same | same |
| `logs/<run_id>/summary.json` | List of PRs processed in a run | same | same |
| `logs/<run_id>/screenshots/*.png` | **Full-page captures of PR pages** — includes code diffs, comments, reviewer names | same | same |
| Shell history (`~/.zsh_history`) | Full CLI commands incl. PR URLs | OS-managed | Use `HISTIGNORE='gh-approve-merge*'` to keep them out. |

## Rules of operation

1. **Never share raw `logs/<run_id>/` artifacts externally** (Slack, support tickets, pastebins, public chats). Screenshots in particular are full PR captures and may include source code from private repos.
2. **Use `--redact-logs` when sharing logs is necessary for debugging.** It hashes the `pr` field in all JSON log files so the run can be analyzed without exposing repo names.
3. **Don't run the tool in a screenshare.** The terminal output includes PR URLs and the final summary table. Use `--quiet` if you must.
4. **Treat `storage_state.json` as a credential.** Don't commit it, don't paste it, don't sync it to cloud storage. If you suspect it leaked, revoke your GitHub session at https://github.com/settings/sessions and run `auth login` again.
5. **Refreshing fixtures may capture real repo HTML.** `scripts/refresh_fixtures.py` sanitizes by default (see its `--no-sanitize` flag if you want to skip). Always review the resulting `tests/fixtures/html/*.html` before committing — search for any organization-specific strings and replace with the standard placeholders (`acme-org`, `widgets-service`, `api-gateway`).

## Pre-commit guard

`scripts/check_no_org_leaks.sh` (run automatically by the git pre-commit hook
when installed) scans staged files for known organization-name patterns and
refuses commits that contain them.

Install the hook once:

```bash
ln -s ../../scripts/check_no_org_leaks.sh .git/hooks/pre-commit
```

(Run from the project root.)

## If something leaks

1. **Revoke the GitHub session** immediately at https://github.com/settings/sessions.
2. **Delete the artifact** from wherever it ended up. Note that public Git pushes are not retractable — assume any pushed history is permanent.
3. **Tell your security contact** if customer or internal source code was involved.
