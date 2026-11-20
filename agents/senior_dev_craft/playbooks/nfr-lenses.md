# NFR lenses: questions, red flags, how much is enough

One page per lens lives in `wiki/` (route via `wiki/index.md`). This page is the checklist the skills
run through. **Proportionality is the point:** set a level per lens from the requirements, build exactly that,
and say out loud what you deliberately left out and what the next step would be.

## Levels (used in the frame's NFR budget table)
- **none**: not relevant at this scope. Say why in five words.
- **basic**: cheap hygiene every professional does by default.
- **critical**: a requirement drives it (SLA, money, data, scale, a hostile input). It costs design and test time.

| Lens | Ask | basic | critical | Red flags | Deep page |
|---|---|---|---|---|---|
| **Security** | What input is untrusted? What's the worst a caller can do? Any secrets/PII? | validate at the boundary, parameterized queries, no secrets in code/logs, least privilege | authz per resource (tenant scoping), rate limits, safe deserialization, dependency pinning + audit, threat model of the feature | `as T` casts on input, string-built SQL/shell, `pickle`/`yaml.load` on input, secrets in code, PII in logs | `kb-xss`, `kb-deserialization`, `code-reviewer` wiki |
| **Availability / resilience** | What does it call? What happens when that is slow, down or returns garbage? | timeouts everywhere, bounded retries with jitter on idempotent ops, clear errors | circuit breaker, idempotency keys, fallback/degrade, bulkheads, health/readiness | no timeout, `while True` retry, retrying 4xx, swallowed errors | `~/work/git/personal_KB/system-design/resilience-patterns.md` |
| **Performance / latency** | What's the budget (p50/p99, throughput)? What's n? | right complexity for n, no N+1, streaming for big inputs | measured hot path, bounded parallel I/O, caching with TTL, benchmark in CI | unbounded fan-out, sync I/O in async/event loop, unmeasured "optimizations" | `~/work/git/personal_KB/system-design/performance-and-latency.md` |
| **Scalability** | 10× users/data: what breaks first? | stateless handlers, capped pagination, bounded queues | partitioning by key, async workers + queue, idempotent consumers, cache layer | module-level state, unbounded queues/limits, per-item tasks | `~/work/git/personal_KB/system-design/scalability-in-code.md` |
| **Rate limiting / quotas** | Who could overload us? Whose quota do we consume? | honor `Retry-After`, bounded concurrency to vendors | token bucket per key, 429 contract, distributed limiter | IP-only keys behind a proxy, tight 429 retry loops | `~/work/git/personal_KB/system-design/rate-limiting-in-code.md` |
| **Observability** | At 3am, how do we know it's broken and why? | module loggers, structured fields, errors logged once with traceback | correlation ids, RED metrics, traces, LLM token/cost metrics, SLO alerts | `print`, f-string logs with user data, no request id | `~/work/git/personal_KB/system-design/observability-in-code.md` |
| **Extensibility** | What's likely to change (vendor, storage, rules, channels)? | DI through constructors, config over code | `Protocol` seams at likely-change points, versioned contracts/events | ABCs with one subclass, `if vendor == ...` everywhere, hard-coded models/limits | `~/work/git/personal_KB/system-design/extensibility-seams.md` |
| **Testability / quality** | How do we prove it works, and keep it working? | behavior tests, edge cases, deterministic (injected clock/rand) | property tests, fault injection, contract tests, coverage gate | sleeps in tests, real network, mocks of what you own | `skills/craft-test` |
| **LLM-specific** (when the code calls a model) | Cost per call? Latency? What if it's wrong or injected? | timeouts + retries, token limits, structured output parsing with validation | evals as a test set, LLM-as-untrusted-proposer + validation, prompt-injection boundary, caching, model routing (cheap first) | trusting model output as code/SQL/JSON, unbounded context, no eval | `langgraph-recipe`, `bug-triage`, `code-reviewer` |

## How to say it (examples)
- "Security is **critical** here: the payload comes from the internet. So zod at the boundary and an idempotency key. I'm not adding authz rules because auth is upstream, out of scope."
- "Scalability is **basic**: one process is fine for the stated 50 rps. Handlers are stateless and the queue is bounded, so scaling out is a deploy change, not a rewrite."
