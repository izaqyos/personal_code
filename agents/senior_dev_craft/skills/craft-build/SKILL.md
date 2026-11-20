---
name: craft-build
description: Implement a framed design test-first in small verified increments (≤30 lines), with idiomatic Python or TypeScript/Node, the NFR decisions from the frame applied, and gates (lint, types, tests) green after every step. Use after craft-frame, or when asked to implement something with tests.
argument-hint: "[increment description]"
---

# craft-build: TDD in small, verified increments

SUITE = `~/work/git/personal_code/agents/senior_dev_craft`.

## Load (once)
- **Python:** `~/work/git/personal_KB/python/modern-python-playbook.md`, then the standards in `~/work/git/personal_code/agents/expert_python_coder/SKILL.md` and the tooling in its `AGENT_CONTEXT.md`.
- **TypeScript/Node:** `~/work/git/personal_KB/typescript/typescript-node-playbook.md`.
- Route through `SUITE/wiki/index.md` for each NFR lens the frame set to basic or critical. Read the A page(s), ≤3 in total.
- Follow the repo's existing conventions (layout, test runner, lint config) over these defaults.

## Each increment
1. Pick the next test group from the frame's test list. **Write the tests first** and run them. They must fail for the right reason (missing behavior, not an import typo).
2. Write the **smallest code that passes**, ≤ 30 lines. Show it in showcase mode, and narrate one "why" per non-obvious choice.
3. **Gates:**
   - Python: `ruff check`, `ruff format --check`, `mypy --strict`, `pytest`.
   - TS: `tsc --noEmit`, `eslint`, `vitest` / `node --test`.
   Report the actual results. Never claim a gate you didn't run.
4. **Refactor while green:** names, small functions, dead code removed. Run the gates again.
5. In showcase/standard mode, stop for "go" between increments if the human wants that granularity.

## Code standards (beyond the playbooks)
- Pure logic separated from I/O. Inject clock, randomness, sleep and network clients (constructor args with defaults).
- Validate at the boundary and trust inside. Specific errors with context, chained (`from err` / `{ cause }`).
- Apply exactly the NFR decisions from the budget: timeouts, bounded retries, bounded concurrency, capped pagination, structured logs. Nothing extra without saying so.
- No new dependencies without asking. Stdlib first.
- Comments explain *why*. Docstrings on public API only. No dead guards for inputs the contract excludes.

## LLM-collaboration rules (`SUITE/playbooks/llm-collaboration.md`)
- Read every generated line before accepting it. Check unfamiliar APIs against the installed version.
- If the same failure happens twice, stop and reason from the error. Don't patch at random.
- If the human takes the keyboard, follow along: run their change through the gates and comment only on real issues.

Hand over to `SUITE/skills/craft-test/SKILL.md` when the test list's functional groups are green.
