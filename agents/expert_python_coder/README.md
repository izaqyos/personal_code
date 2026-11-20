# expert_python_coder

An agent that writes, reviews and teaches idiomatic, readable Python with high unit-test coverage.
The human stays the engineer of record: plan first, tests first, small verified steps.

## Invocation

### Claude Code (recommended)

| Command | Mode |
|---------|------|
| `/epc <task>` | **build**: plan → tests → code → verify (pytest + coverage, ruff, mypy) → report |
| `/epc interview <task>` | **interview**: build, in small increments, waiting for approval after each step |
| `/epc review <path>` | **review**: what the code does, then bugs/risks/smells by severity with fixes |
| `/epc drill [topic]` | **drill**: a snippet with planted bugs for code-comprehension practice, scored |

Registered as a global command in `~/.claude/commands/epc.md`, which loads the files below.

### Cursor / other tools

Attach `SKILL.md` and `AGENT_CONTEXT.md` (`@` mention in Cursor), or paste `PROMPT.md` into any LLM chat
when only a plain chat box is available.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Behavior: modes, workflow, Python standards |
| `AGENT_CONTEXT.md` | Knowledge: tool commands, default layout, testing and review checklists, common Python traps |
| `PROMPT.md` | Condensed, tool-independent version to paste into any LLM |
| `README.md` | This file |
| `~/.claude/commands/epc.md` | Global Claude Code command (thin loader) |

## Quality bar

- Tests written before code, behavior-focused, parametrized; ≥ 90% line + branch coverage on new code.
- `ruff check` + `ruff format --check` + `mypy` clean.
- No dead code or defensive guards for inputs the contract excludes.
