# YosiBuilder

A harness-agnostic build method: a strong model designs and plans, cheap models build and review each small task
card against free deterministic gates, and every card's result and cost goes into a ledger so the setup can be
tuned over time. Any agent harness (Claude Code, Codex, Antigravity, Aider, a human) can follow this file.

## Roles

| Role | Default | Does | Never does |
|---|---|---|---|
| Architect (chief) | Opus, interactive session | Frames the work, writes the design (SDD) and test plan (DTP), cuts cards, reviews milestones, reads `yb report`, talks to the user | Writes feature code |
| Lead (head of QA) | Gemini Hydrogen via `agy`, plan mode | Reviews each card's diff and gate output, returns accept or reject with findings | Edits code |
| Worker (coder, tester, devops) | Claude Haiku, lean headless `claude -p` | Implements one card: code and tests, runs the gates, fixes findings | Touches files outside the card; commits |
| Tie-breaker | Claude Sonnet | One extra cycle (worker and lead) for a card the crew could not finish | Runs on cards that are going fine |
| Runner | `bin/yb` (a script, not a model) | Worktrees, dispatch, free gates, review, merge, state, ledger | Judgement calls |

A **crew** is the worker and lead pair. Named crews (`yb run --crew NAME`, or `YB_CREW`):

| Crew | Worker | Lead | Use when |
|---|---|---|---|
| `default` | Haiku | Hydrogen | Normal work |
| `no-claude` | Hydrogen | Hydrogen | Claude quota is low |
| `claude` | Sonnet | Sonnet | Gemini is unavailable, or for comparison |
| `flash` | Gemini Flash | Hydrogen | Experiments only (token-heavy in tests) |

`--mode hybrid` puts local Qwen (Aider + Ollama) in front of the crew's worker; `--mode local` is Qwen only.
Both are kept for private or offline work; measured, they did not save usage (EXPERIMENTS.md).

## Invariants (hold at all times)

1. **Interrupt-resistant.** All state lives in `<repo>/.ybuild/` (git-excluded): `STATE.json` (per card status,
   reviews, attempts, `next_action`), `WORKLOG.md` (append-only), `DECISIONS.md`, `SDD.md`, `DTP.md`, `cards/`,
   `runs/` (full logs), `usage.jsonl` (every model call: role, provider, model, tokens, cost). Any role resumes by
   reading this file, the state files, `git status`, `git log` and `git worktree list`, and continues from
   `next_action`.
2. **TDD at three levels.** Unit, component and end-to-end tests; tests come first in every card's test plan; a
   bug fix starts with a failing test.
3. **Clean code, no slop.** Small single-purpose functions, small cohesive classes, low complexity, DRY,
   encapsulation, typed code, specific errors. No dead code, speculative options, commented-out code, restating
   comments, swallowed exceptions or filler.

## Flow

1. **Architect: frame.** Goal, constraints, non-functional budget, two designs and the choice, interfaces,
   failure modes, test list. Write `PLAN.md` in `.ybuild/` and get the user's approval.
2. **Architect: contracts first.** Shared types and interfaces, the scaffold and the gates config for the
   language (see Languages below). Commit before any card runs.
3. **Architect: design and test plan.** `.ybuild/SDD.md`: modules, classes, signatures with types, errors,
   constants, the algorithm in a few lines each. `.ybuild/DTP.md`: every test by name with inputs and exact
   expected output or error. Check that the design fits the gates (for example, a loop the design puts in one
   function must fit the complexity limit), or the worker and the lead will disagree.
4. **Architect: cards.** From `templates/task-card.md`, each carrying its full slice of the SDD and DTP: one
   module and its tests, the exact import line, a test command that runs in seconds, no open design decisions.
5. **Runner: `yb run [--crew C] [--mode M] <cards...>`.** Per card: worktree and branch `yb/<id>`; the worker
   builds until the **free gates** are clean (tests; the card's lint command; every test named in the test plan
   exists; mutation test of the card's source: in Python each statement replaced by `pass`, in C-like languages
   each simple statement deleted, and each comparison or `&&`/`||` flipped must fail a test);
   then the lead reviews; accept merges. Up to `YB_MAX_REVIEWS` cycles, then one Sonnet tie-break cycle, then
   `blocked`. The run stops at the first blocked card.
6. **Monitoring.** After each card `yb` prints its cost and the crew's rolling acceptance and cost, and warns
   when acceptance over the last `YB_WINDOW` cards drops below `YB_ALERT_ACCEPT`. `yb report` compares crews
   across all builds.
7. **Escalation.** A blocked card goes back to the architect: re-scope, split, or sharpen its design and test
   plan. Record the decision in `DECISIONS.md`.
8. **Milestone review (architect).** Full gates on main, read the merged diff for drift and slop, read
   `yb report`, adjust crews, prices or card style, update the plan, report to the user.

## Languages

Python, Node.js (JavaScript, TypeScript, NestJS and the rest of the npm ecosystem), Rust, Java, C and C++. A card
names its language with `lang:` (`python`, `node`/`ts`/`js`/`nestjs`, `rust`, `java`, `c`, `cpp`) or `yb` infers it
from the `edit:` files (`.h` counts as C++ when any C++ file is present). The language decides which edited files
are tests, how failures are pulled out of gate output, the idioms appended to the worker and lead prompts
(`roles/lang/<lang>.md`), and the mutation budget. The gates themselves are always the card's `test:` and `lint:`
commands, and the worker may run exactly the programs those commands start (`uv run`, `npx jest`, `cargo test`,
`cmake`, `ctest`, `./gradlew`...), nothing else.

| Language | Example `test:` | Example `lint:` | Mutant timeout, memory |
|---|---|---|---|
| Python | `uv run pytest tests/unit/test_x.py -q` | `uv run ruff check src tests` | 20 s, 2 GB |
| Node / TS / Nest | `npx jest src/users --ci` or `npx vitest run src/x` | `npx tsc --noEmit && npx eslint src/users` | 60 s, 4 GB |
| Rust | `cargo test -q --lib x::` | `cargo clippy -q -- -D warnings` | 120 s, 4 GB |
| Java | `mvn -q test -Dtest=XTest` or `./gradlew test --tests XTest` | `mvn -q -DskipTests verify` (checkstyle/spotbugs) | 180 s, 4 GB |
| C | `cmake -S . -B build && cmake --build build && ctest --test-dir build -R x` | `-Wall -Wextra -Werror` in the build, or `clang-tidy` | 120 s, 4 GB |
| C++ | same as C, GoogleTest or Catch2 | same as C | 120 s, 4 GB |

Optional card headers: `setup:` runs once in a new worktree (default for Node: `npm ci`/`pnpm install`/`yarn
install` from the lockfile, since worktrees have no `node_modules`; none for the others: uv, cargo, Maven and
Gradle use their caches); `mutants:` caps the mutants per file (default 40, `0` turns the mutation gate off);
`mutation_timeout:` seconds per mutant run; `mutant_mem_mb:` memory cap per mutant run (card, then
`YB_MUTANT_MEM_MB`, then the language default). Compiled languages rebuild per mutant, so keep their test commands
narrow (one module, incremental build) or lower `mutants:`. Test plans name tests the way the language does:
`test_x`, `fn x()`, `void x()`, `TEST(Suite, X)`, or quoted titles `it("...")`/`test("...")`/`TEST_CASE("...")`.
Gradle's daemon is turned off for mutant runs (a daemon outlives the killed process group).

## Results and pricing ledger

Every built card appends one entry to `YB_LEDGER` (default `~/.local/share/yosibuilder/ledger.jsonl`, outside any
repo): repo, card, crew, worker and lead models, mode, status, reviews, attempts, seconds, per-provider dollars and
tokens, weighted cost, and the first lines of the findings it blocked on.

- Claude dollars come from the CLI (`total_cost_usd`, list price), a proxy for subscription usage.
- Other providers report tokens only; `config/prices.json` turns them into estimated dollars (per-model prices,
  with an `unpriced` placeholder rate). Replace the placeholder with real prices when known.
- `weighted_usd` = each provider's dollars times its weight in `config/prices.json` (Claude 1.0, Gemini 0.25,
  local 0): Claude quota is the scarce resource, so it counts most. Tune the weights as quotas change.
- Tuning loop: change one thing (crew, card style, gate, prompt), build real cards, compare `yb report --last N`
  before and after, keep what wins, and note it in EXPERIMENTS.md.

## Rules for every role

- Never push, never create remotes, never send code anywhere beyond the configured model providers.
- Use the expensive models for judgement and design, the cheap ones for typing.
- Report only what was run and observed. A claim without a command and its output does not count.
- Never use flags that skip permission checks. Workers get file tools plus an explicit command allow-list.
- Stop and ask the user on licences, secrets, scope changes, or anything that bends an invariant.

## Setup (once per machine)

- Claude Code CLI signed in (`claude auth login`). Cloud calls run lean (`--strict-mcp-config
  --setting-sources "" --no-session-persistence --output-format json`): a default headless call carries about
  44k tokens of overhead, a lean one under 1k.
- Antigravity CLI `agy` signed in; `agy models` lists the Gemini models. Workers run `--mode accept-edits
  --sandbox` with the card's gate programs plus `command(ls|cat|grep|find|head)` allowed: in headless mode a denied command ends the turn
  with no output, so the allow-list must cover harmless read commands. Leads run `--mode plan`.
- Optional, for `--mode hybrid` or `local`: Ollama with `qwen3-coder:30b`, Aider, `config/aider.model.settings.yml`.
- `bin/yb` on the PATH or called by its full path.

## Environment

| Variable | Default | Meaning |
|---|---|---|
| `YB_CREW` | `default` | Crew name (see above) |
| `YB_FIX_CMD`, `YB_LEAD_CMD` | from the crew | Override the worker or lead command (prompt on stdin); the crew is logged as `<name>+custom` |
| `YB_MAX_REVIEWS` | `3` | Review cycles before the tie-break |
| `YB_CLOUD_ROUNDS` | `2` | Worker attempts per cycle to reach clean free gates |
| `YB_TIEBREAK` | `1` | `0` disables the Sonnet tie-break cycle |
| `YB_LEDGER` | `~/.local/share/yosibuilder/ledger.jsonl` | Results and pricing ledger |
| `YB_MUTANT_MEM_MB` | language default | Memory cap per mutant test run, unless the card sets `mutant_mem_mb:` |
| `YB_WINDOW`, `YB_ALERT_ACCEPT` | `20`, `0.8` | Rolling window and acceptance alert threshold |
| `YB_LOCAL_MODEL`, `YB_LOCAL_ROUNDS`, `YB_RED_STREAK` | `qwen3-coder:30b`, `5`, `2` | Hybrid and local modes |
