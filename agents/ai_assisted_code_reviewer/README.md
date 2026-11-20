# AI-assisted code reviewer

An AI code review tool that developers run from **whatever agent harness they already use**
(Claude Code, Cursor, Copilot, Codex…) and that CI runs on every PR. It is grounded in a
**team-owned LLM wiki** instead of RAG, so developers need no API keys.

```
                     ┌──────────────── .ai-review/ (in each repo) ────────────────┐
                     │ REVIEW.md          ← the one procedure (steps, rubric, JSON) │
 dev: /ai-review ──► │ wiki/index.md      ← routing table: path globs → pages      │
 (CC/Cursor/Copilot) │ wiki/**/*.md       ← rules: ID, severity, Why, Bad/Good     │
                     │ pr-rules.json      ← PR template requirements               │
 CI: aireview run ─► │ config.json        ← gate mode, thresholds, globs           │
                     └─────────────────────────────────────────────────────────────┘
                                     │
   aireview CLI (stdlib Python): diff ─► deterministic checks ─► route wiki ─► bundle
                                     ─► LLM (harness agent | claude -p | mock)
                                     ─► VALIDATE ─► report.md / report.json ─► gate
```

## What it checks

| Layer | Checks | How |
|---|---|---|
| **Deterministic** (always, no LLM) | committed secrets · PR template sections/checkboxes/ticket · migration PR has rollback plan · source changed without tests · PR size | `aireview checks` |
| **LLM, grounded in the wiki** | authz/IDOR, injection, PII in logs, SSRF · swallowed errors, async pitfalls, breaking API changes · destructive migrations · missing negative/authz tests · team conventions linters can't express · incident-derived pitfalls · does the PR description match the diff · prompt injection in PR text | agent follows `REVIEW.md` |
| **Validation** (the trust layer) | drops findings with unknown rule IDs, files not in the diff, lines outside changed hunks, confidence < 0.6, in-code suppressions, duplicates, schema errors; `general` (rule-less) findings can't block; cap trims nits first and never drops blockers | `findings.validate` |

Every finding cites a wiki rule ID. **Teams turn a check off by deleting its rule from
the wiki, and turn one on by writing a rule.**

## Who uses it, and how

| Who | When | Command |
|---|---|---|
| Author | before pushing | Claude Code: `/ai-review` · Cursor: `/ai-review` command or ask "review my branch" (rule `ai-review.mdc`) · Copilot: `ai-review` prompt · Codex/others: AGENTS.md |
| CI | every PR | `.github/workflows/ai-review.yml` → `aireview run --runner claude` posts/updates one PR comment |
| Reviewer | reading the PR | the comment: blockers first, evidence, fixes, what was dropped and why |
| Tech lead / owners | ongoing | edit `.ai-review/wiki/`, run `aireview wiki-lint` |

Local flow inside any harness (defined in `REVIEW.md`):

1. `aireview context --base origin/main` writes `.ai-review/out/context.md`, which holds the procedure, the deterministic results, the routed wiki pages and the diff, with an explicit untrusted-input boundary.
2. The agent reviews in passes: security, then correctness, then tests, then conventions, then the PR description.
3. The agent verifies each finding against the code, then writes `.ai-review/out/findings.json`.
4. `aireview validate` merges in the tool findings, validates everything, and renders the report.

Without the CLI installed, `REVIEW.md` has fallback steps (plain `git diff` and manual routing through `index.md`), so the instructions still work in any harness.

## Install into a repo

```bash
pipx install /path/to/ai_assisted_code_reviewer      # or pip install git+https://…
cd your-repo
aireview install                       # all harnesses + CI
aireview install --only claude,ci      # or pick groups: core, claude, cursor, agents, copilot, ci
aireview wiki-lint
```

`install` never overwrites existing files without `--force`. `CLAUDE.md`, `AGENTS.md` and `copilot-instructions.md`
get an idempotent `<!-- ai-review:start/end -->` block appended. Your content is preserved.

### CI setup
1. Add the `ANTHROPIC_API_KEY` secret. Only CI needs it; developers don't.
2. Set `AIREVIEW_PIP` in the workflow to where you host this package.
3. Start with `"gate": "advisory"`. Switch to `"blocker"` once findings are trusted. The PR label `ai-review-override` bypasses the gate.

The workflow hardening, which is tested:
- It triggers on `pull_request`, never `pull_request_target`.
- It skips fork PRs, so secrets never reach untrusted code.
- It gets `contents: read` permission only.
- PR text never touches the shell script.
- Claude runs with `Read,Grep,Glob` only. Bash, Edit, Write and web tools are disallowed.

## Writing wiki rules

```md
### SEC-002: Scope every resource lookup to the caller's tenant
**Severity:** blocker
**Why:** Loading by client-supplied id without an ownership check is IDOR.
**Bad:**
```ts …```
**Good:**
```ts …```
```

- Add the page to the routing table in `wiki/index.md` (`| Paths | Pages |`; `*` = always).
- Keep pages short (≲150 lines). Agents read only the routed pages, not the whole wiki.
- When the reviewer is wrong, **fix the rule** (add a Good example or an exemption). When an incident happens, add a `PIT-*` rule.
- For an intentional exception in code, use `// review-ignore SEC-002: reason`. The reason is mandatory.

## Demo (mock TypeScript/Express service)

`demo/sample_service/` holds a billing service (`base/`) and a deliberately bad PR (`pr/`). The PR contains:
- IDOR, SQL injection, and a router mounted without auth
- a hardcoded Stripe key and PII in logs
- an uncapped `limit`, `forEach(async)`, and a swallowed error
- a `DROP COLUMN` with no down migration
- no tests, a placeholder PR body, and a prompt-injection comment in the PR body

```bash
python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'
demo/run_demo.sh            # offline; mock LLM output that includes hallucinations → watch validation drop them
demo/run_demo.sh --live     # real review via Claude Code headless (uses your CC login)
demo/run_demo.sh --setup    # build the repo, then: cd $TMPDIR/aireview-demo && claude  →  /ai-review main
demo/present.sh             # presenter walkthrough, 13 paused steps (--live, --auto)
```

**Presenter guide (PDF):** `docs/presenter_guide.pdf`. It has step-by-step talking points for `present.sh`, likely questions with answers, a rollout plan and a cheat sheet. Rebuild it with `python3 docs/build_guide.py`.

Sample outputs are in `demo/sample_reports/`:
- `mock_report.md`: 22 kept, 8 dropped (hallucinated line, unknown rule, file not in diff, low confidence, suppressed, duplicates, schema error).
- `live_claude_report.md`: the real Claude Code run found all seeded issues (5 blockers, 11 major) with 0 findings dropped, and flagged the prompt injection.

## Tests

```bash
.venv/bin/pytest            # 140 tests, ~3s
```

| Area | Tests | What they cover |
|---|---|---|
| Diff parsing | `test_diff.py` | adds, deletes, renames, binary files, multi-hunk diffs, uncommitted mode |
| Glob matching | `test_globs.py` | glob semantics |
| Wiki | `test_wiki.py` | rule parsing, ignoring headings inside code fences, routing, lint; the shipped wiki is lint-clean |
| Deterministic checks | `test_checks.py` | PR template, secrets, tests-touched, size |
| Validation | `test_findings.py` | every drop reason, dedupe, cap, suppressions |
| Report and gate | `test_report.py` | gate matrix, rendering |
| Runners | `test_runners.py` | JSON extraction, claude command is read-only, subprocess errors and timeouts |
| Install | `test_install.py` | idempotency, marked blocks, adapters stay thin pointers to `REVIEW.md`, workflow hardening |
| End to end | `test_e2e_demo.py` | full pipeline on the demo repo through the CLI, plus `run_demo.sh` itself |

Key-shaped test and demo fixtures are assembled at runtime, so secret scanners on this repo stay quiet (`gitleaks detect` is clean).

## Layout

```
src/aireview/
  cli.py          context | validate | run | checks | wiki-lint | route | install
  diff.py         unified diff parser + git collection
  wiki.py         rule parser, routing index, lint
  checks.py       deterministic checks
  bundle.py       context bundle (trusted/untrusted sections)
  findings.py     Finding model + validation
  suppress.py     review-ignore comments
  report.py       gate + markdown/JSON
  runners/        claude (headless), mock
  install.py      kit installer
  payload/        what gets installed: ai-review/ (REVIEW.md, wiki, configs), adapters, workflow, PR template
demo/             sample service, PR body, mock LLM output, run_demo.sh, sample reports
tests/
```

## Design choices and limits

- **No RAG.** Routing by path globs is deterministic, explainable ("why did it read authz.md? because `src/routes/**`"), and works in any harness that can read files. It stops scaling at roughly hundreds of pages. At that point split the wiki per team or service, and keep shared security pages in the `*` row.
- **The LLM is an untrusted proposer.** Anything it says that can't be tied to a wiki rule and a changed line is dropped and listed in the report, so you can see what was filtered.
- **Gating is narrow on purpose.** Only `blocker` findings that cite a rule can fail the build. `general` findings can't, and humans can override with a label.
- **Not covered here:** SAST, dependency CVEs and linters. Run semgrep, gitleaks, `npm audit` and eslint as their own CI steps. The `REVIEW.md` instructions tell the agent not to repeat what those tools catch.
- **Next ideas:**
  - Inline PR review comments, one per finding, instead of a single comment.
  - Tracking each finding's acceptance rate from reactions, to tune rules.
  - A `wiki-suggest` command that drafts rule edits from disputed findings.
  - A shared wiki package for many repos.
