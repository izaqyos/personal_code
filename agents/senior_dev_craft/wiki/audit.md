# Source audit: KB + code refs for the craft wiki

**Audited:** 2026-11-03 · **Scope:** `personal_KB` and `personal_code` (plus one file in `~/work/practice`). `personal_KB_private` is never in scope.
**Tooling:** `python3 wiki/audit.py scan` (automated signals) + a manual read of every candidate.
**Source of truth:** `catalog.toml`. `index.md` is generated from it (`audit.py render`), and `audit.py check` enforces the rules.

## Rubric

| # | Criterion | Fails if |
|---|---|---|
| 1 | Current | Python < 3.11 idioms; JS `var`/callbacks/CommonJS; no async/await or AbortController; deprecated libs |
| 2 | Correct | Claims or code are wrong (Python snippets parsed + ruff-checked; manual read for logic bugs) |
| 3 | Clean code | Untyped, swallowed errors, globals, unclear naming |
| 4 | NFR-aware | Contradicts the NFR lenses: wall clock for durations, no timeouts, unbounded retries |
| 5 | Distilled | Raw dump or pasted chat answer instead of distilled knowledge |
| 6 | Showcase-safe | Private, employer or interview-prep framing (the screen is shared) |

## Grades

| Grade | Label | Routed? | Meaning |
|---|---|---|---|
| **A** | exemplar | in full | Passes all 6. Imitate its code and style. |
| **B** | ok | partially | Sound ideas, flawed code. Agents read only the sections in `use` and write code to the playbook standards. |
| **C** | weak | no | Not needed, not verified, or not showcase-safe. |
| **D** | legacy | no | Outdated, wrong, or a raw dump. A replacement exists in this suite. |

**Rule:** every route needs at least one A source. A topic with none gets a **gap-fill page**, written here to grade A and verified the same way.

## Results

| Grade | Count | Sources |
|---|---|---|
| A | 7 | `ai-principles`, `langgraph-recipe`, `kb-xss`, `kb-deserialization`, `epc-context`, `bug-triage` (172 tests, mypy strict, ruff clean), `code-reviewer` (140 tests, ruff clean) |
| B | 16 | system-design guides (×10), perf guides (×2), OrderProcessing designs (×3), `kb-ts-saga` |
| C | 4 | `perf-microbench`, `ops-scalability`, `ops-security-oauth2`, `idiomatic-python` |
| D | 8 | `ops-ts-examples`, `kb-py-{concurrency,logging,collections}`, `kb-node-{patterns,idioms,timers,testing}` |

### Notable findings
- **The guides are good concept material, but their code shouldn't be imitated.** Every Python snippet is untyped. Rate limiters and the circuit breaker time durations with `time.time()` (wall clock, which jumps with NTP) instead of `time.monotonic()`.
- **The circuit breaker code has logic bugs:**
  - `failure_count` never resets on success in CLOSED, so it opens after 5 failures *ever*, not 5 in a row.
  - HALF_OPEN lets unlimited trial calls through at once.
  - `except Exception as e` leaves `e` unused, and `CircuitOpenError` is undefined.
- **OrderProcessing TS examples (D):**
  - The comment says "Step 1: Validate input" but there is no validation.
  - Every `catch` returns 500 without logging or `next(err)`.
  - `req.body.status as Order['status']` is an unvalidated cast.
  - Order creation isn't idempotent, even though the sibling `Idempotency_Design.md` says it must be.
- **Legacy KB pages (D):** frontmatter says `legacy` + `capture_type: source`. The Node pages use `var`, error-first callbacks and CommonJS. `12-logging.md` is a pasted chat answer built on `basicConfig`. Git dates are misleading: they all show the 2026-10-14 purge commit.
- **The idiomatic-Python cheat sheet (C)** has strong, modern content, but it's written as interview prep. Its content moved into `~/work/git/personal_KB/python/modern-python-playbook.md`.
- **Fixed during the audit:** `ai_assisted_code_reviewer` was not lint-clean (18 findings under your global ruff rules, 21 files unformatted). It now has an explicit `[tool.ruff]` config, is clean and formatted, and still passes 140 tests. That's why it can be A.

## Gap fills (written for this suite, graded A; promoted into the KB 2026-11-03)

| Route | Gap page | Replaces / supersedes |
|---|---|---|
| resilience | `~/work/git/personal_KB/system-design/resilience-patterns.md` | circuit-breaker + saga code, OrderProcessing error-handling code |
| performance | `~/work/git/personal_KB/system-design/performance-and-latency.md` | `perf-microbench` snippets |
| scalability | `~/work/git/personal_KB/system-design/scalability-in-code.md` | (only B prose existed) |
| rate-limiting | `~/work/git/personal_KB/system-design/rate-limiting-in-code.md` | rate-limiter snippets (wall clock, untyped) |
| extensibility | `~/work/git/personal_KB/system-design/extensibility-seams.md` | (only B prose existed) |
| observability | `~/work/git/personal_KB/system-design/observability-in-code.md` | `kb-python/12-logging.md` |
| typescript-node | `~/work/git/personal_KB/typescript/typescript-node-playbook.md` | `kb-nodejs/{17,21,10,03}`, `ops-ts-examples` |
| python | `~/work/git/personal_KB/python/modern-python-playbook.md` | `kb-python/{56,67}`, idiomatic-Python cheat sheet |

## KB follow-ups (approved 2026-11-03)
1. ✅ Deprecated the 7 legacy D pages in `personal_KB` (`kb-python` §12/§56/§67, `kb-nodejs` §03/§10/§17/§21): `status: deprecated` + replacement pointer, `log.md` entry, OKF gate green.
2. ✅ Promoted the 8 gap pages into `personal_KB` (`system-design/`, `typescript/`, `python/`). The suite copies were deleted; the catalog points at the KB, which is the single source of truth.
3. ✅ Fixed the circuit-breaker and rate-limiter snippets in `personal_code/guides` (monotonic clock, consecutive-failure reset, half-open probe limit, types) and put a warning on the D-graded OrderProcessing TS examples.
