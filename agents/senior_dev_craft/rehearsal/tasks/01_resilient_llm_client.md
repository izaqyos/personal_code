# Task 01: Resilient LLM API client (Python, ~30 min)

## Interviewer prompt
"Our QA agents call an LLM API a lot. Write a small client wrapper: `complete(prompt) -> str`. The vendor
sometimes times out, returns 429 with `Retry-After`, or 5xx. We have a quota of ~60 requests/minute."

## Hidden NFR hooks
- **Resilience (critical):** per-call timeout; retry only 429/5xx/timeouts; exponential backoff + full jitter; total deadline.
- **Rate limiting (critical):** client-side token bucket (1 req/s, burst ~5); honor `Retry-After` over its own backoff.
- **Extensibility (basic):** a transport seam (`Protocol`), so tests use a fake and the vendor is swappable.
- **Observability (basic):** log attempt, status, latency, tokens. Never log the prompt (it may hold user data).
- **Security (basic):** API key from env, never logged. Don't echo vendor error bodies to callers verbatim.
- Not needed: a circuit breaker (name it as the next step if outages last minutes), caching (prompts rarely repeat).

## Expert moves
1. Frame: trace "429 with Retry-After: 2 → wait 2 s, not the backoff value". Ask one MCQ: "Non-retryable 400: raise immediately [rec] / return None".
2. NFR budget table out loud. The pick: sync + injected `sleep`/`clock`, or async. Choose sync unless they say async.
3. Tests first with a **fake transport** scripted per call: `[Timeout, 429(2), 200]` → asserts attempts=3 and slept=[backoff, 2].
4. Reuse the shapes from `~/work/git/personal_KB/system-design/resilience-patterns.md` (retry) and `~/work/git/personal_KB/system-design/rate-limiting-in-code.md` (bucket). Cite them.
5. Critic pass: "is the deadline enforced across retries? Is jitter applied? Is 401 retried by mistake?"

## Likely follow-ups
- "Make it async and run 100 prompts concurrently": `Semaphore` + `TaskGroup`, bucket shared, sleep outside the semaphore.
- "Add a circuit breaker": the 3 correctness points (monotonic clock, reset on success, one half-open probe).
- "How do you test the timing without waiting?": injected clock/sleep, record sleeps, assert the sequence.
- "Cost control?": max tokens, cache by prompt hash for deterministic calls, route to a cheaper model first.
