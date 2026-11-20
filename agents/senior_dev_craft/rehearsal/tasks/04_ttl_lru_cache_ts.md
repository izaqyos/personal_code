# Task 04: TTL + LRU cache (TypeScript, ~30 min)

## Interviewer prompt
"Implement an in-memory cache for expensive lookups (say LLM responses): `get(key)`, `set(key, value)`,
max size with LRU eviction, and a per-entry TTL. Add a `getOrLoad(key, loader)` so concurrent misses
for the same key only call the loader once."

## Hidden NFR hooks
- **Performance (critical):** O(1) get/set via `Map` insertion order (delete + re-set moves an entry to the most-recent end).
- **Correctness:** TTL check on read (lazy expiry); eviction of the least-recently-used entry; `noUncheckedIndexedAccess`-safe code.
- **Concurrency (critical):** single-flight: an in-flight `Map<key, Promise<V>>`. A failed load is *not* cached, and the in-flight entry is cleared in `finally`.
- **Testability:** an injected `now: () => number` clock; no real timers.
- **Observability (basic):** hit/miss/eviction counters exposed via `stats()`.
- Not needed: cross-process sharing (that's Redis; name it), background sweeper timers (lazy expiry is enough at this scope).

## Expert moves
1. Frame: "Map gives O(1) LRU for free via insertion order". Show the delete-then-set trick.
2. Types: `class TtlLruCache<K, V>` with an explicit constructor options object; `readonly` fields; no `any`.
3. Tests first (vitest or `node --test`): eviction order, TTL expiry with a fake clock, single-flight (the loader is called once for 10 concurrent `getOrLoad`), a failed load isn't cached.
4. Use `~/work/git/personal_KB/typescript/typescript-node-playbook.md` idioms: erasable syntax, `satisfies` for options defaults, errors with `cause`.
5. Critic: "what happens if the loader throws synchronously? If the TTL is 0? If size is 0?" Validate the options in the constructor.

## Likely follow-ups
- "Stampede on expiry for a hot key?": single-flight already covers it. Add early refresh or jittered TTL.
- "Memory bound by bytes, not count?": a size estimator per entry plus a byte budget.
- "Distributed?": Redis with `SET key val PX ttl NX`, plus a lock or single-flight per instance; discuss consistency.
