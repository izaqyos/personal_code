---
name: craft-test
description: Senior test strategy beyond happy-path TDD — table tests, property-based tests, fault injection (timeouts, 5xx, partial failure), concurrency and idempotency tests, latency micro-benchmarks, contract tests, and golden-set evals for LLM features. Use to prove NFRs or to strengthen a test suite.
argument-hint: "[focus: fault|property|concurrency|perf|contract|eval]"
---

# craft-test: prove behavior and NFRs

SUITE = `~/work/git/personal_code/agents/senior_dev_craft`. Route through `SUITE/wiki/index.md` row `testing`, plus the
row for each lens being proven. Python checklists: `~/work/git/personal_code/agents/expert_python_coder/AGENT_CONTEXT.md`.

## Pick tests by what the NFR budget promised
| Promise | Test that proves it | Python | TS/Node |
|---|---|---|---|
| Correct over many inputs | parametrized tables + **property test** with an invariant (round-trip, ordering, idempotence) | `pytest.mark.parametrize`, `hypothesis` | `test.each`, `fast-check` |
| Survives a dependency failing | **fault injection**: a fake that times out / 503s / returns garbage on call N | fake class or `monkeypatch`; injected `sleep`/`clock` | injected `fetchImpl`, fake timers |
| Retries are bounded | assert the attempt count and total delay with a fake clock | injected clock + recorded sleeps | `vi.useFakeTimers()` |
| Idempotent | same request twice → one side effect, same response; same key + different payload → conflict | direct | direct |
| Safe under concurrency | N concurrent calls → invariant holds (no lost updates, limit respected) | `asyncio.gather` / threads + a barrier | `Promise.all` |
| Bounded resources | queue/concurrency never exceeds the limit (record the peak) | counter in a fake | counter in a fake |
| Latency budget | micro-bench of the hot path: min of repeats, compared to a budget with margin; mark `slow` | `timeit.repeat`, `pytest-benchmark` | `performance.now()` loop / `tinybench` |
| Contract | consumer-side schema test of the API/event shape, including unknown-field tolerance | pydantic model round-trip | zod schema test |
| LLM feature quality | **golden set as an eval**: fixed inputs → expected labels, scored, with a threshold; deterministic fake for unit tests | pytest + a fixtures file | vitest + a fixtures file |

## Rules
- Behavior over implementation: test names read as sentences (`test_open_breaker_fails_fast_without_calling`).
- Deterministic: no sleeps, no real network, seeded randomness, injected clocks. Fakes over mocks for things you own.
- Each test proves one thing and fails with a message that says what broke.
- Coverage gate ≥ 90% line+branch on new code. Report the number, and don't chase 100% on glue code.
- For LLM-calling code, unit tests use a deterministic fake provider (`~/work/git/personal_KB/system-design/extensibility-seams.md`). Evals run separately against the real model and are scored, not asserted exactly.

Hand over to `SUITE/skills/craft-harden/SKILL.md`.
