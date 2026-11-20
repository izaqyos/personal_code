# senior_dev_craft

A Claude Code skill suite for writing quality, idiomatic, readable code **with** an LLM, the way a senior
engineer does it. It frames before coding, sets a proportionate NFR budget, builds test-first in small
verified steps, proves the NFRs, hardens through lenses and closes with an independent critic pass. Every
phase is grounded in **your own audited knowledge base and code** (an LLM wiki with graded sources), not
generic advice.

Languages: **Python ≥ 3.11** and **TypeScript ≥ 5.8 / Node ≥ 20**.

## Skills (Claude Code)
| Command | Phase | What it does |
|---|---|---|
| `/craft <task>` · `/craft showcase <task>` · `/craft quick <task>` | orchestrator | runs the loop; `showcase` = gates + narration + 45-min time boxes for a live screen share |
| `/craft-frame <task>` | design | restate, trace an example, ≤3 MCQ questions, **NFR budget**, 2 designs → pick, interfaces, failure modes, test list |
| `/craft-build` | code | TDD in ≤30-line increments, playbook idioms, gates green each step |
| `/craft-test [focus]` | test | fault injection, property, concurrency/idempotency, bounded-resource, micro-bench, contract, LLM eval sets |
| `/craft-harden [lens]` | NFRs | lens pass at budgeted levels: finding → fix → proving test; names what it deliberately doesn't build |
| `/craft-review [path]` | critic | fresh-eyes principal-engineer persona; every finding has a triggering input and is verified |

Install: `./install.sh` (symlinks `skills/*` into `~/.claude/skills`; `--copy`, `--remove`).
Other tools: `adapters/cursor/craft.mdc`, `adapters/AGENTS.block.md`, `adapters/PROMPT.md` (paste into any chat).

## The LLM wiki: graded sources from your repos
`wiki/catalog.toml` lists every candidate KB/code source, each with a grade. `wiki/index.md` is the routing table the skills read. It's generated from the catalog, and the skills read at most 3 sources per phase.

| Grade | Label | Routed |
|---|---|---|
| A | exemplar | in full: imitate it |
| B | ok | only the sections named in `use` |
| C | weak | no |
| D | legacy | no |

Every route must have an A source. When none passed, the gap was filled with a page written for the suite and then promoted into the KB (catalog `kind = "gap"`: `~/work/git/personal_KB/system-design/*-in-code.md` and friends, plus the TS and Python playbooks). The KB is the single source of truth, and the tests execute those pages' runnable examples.

Audit results (2026-11-03, details in `wiki/audit.md`): 7 A · 16 B · 4 C · 8 D across `personal_KB` and `personal_code`, with 7 topic gaps filled. `personal_KB_private` is never in scope.

```bash
python3 wiki/audit.py scan            # automated quality signals per source (snippets, legacy markers, tests)
python3 wiki/audit.py render          # regenerate wiki/index.md after editing catalog.toml
python3 wiki/audit.py check           # paths exist, grades valid, every route has an A source, index fresh
```

## Layout
```
skills/        craft, craft-frame, craft-build, craft-test, craft-harden, craft-review (SKILL.md each)
playbooks/     nfr-lenses, python, typescript-node, llm-collaboration, design-note-template
wiki/          catalog.toml → index.md · audit.md + audit.py · profile.md
adapters/      cursor rule, AGENTS.md block, paste-anywhere prompt
rehearsal/     tasks/*.md, showcase-script.md, cheat-card.html → cheat-card.pdf
tests/         test_suite.py (structure, grounding, snippets, install), snippets.py
```

## Tests
```bash
uv run --with pytest pytest -q                           # structure, catalog, snippet execution, install
CRAFT_RUN_EXEMPLARS=1 uv run --with pytest pytest -q     # also re-run the A-grade code exemplars' own suites
```
