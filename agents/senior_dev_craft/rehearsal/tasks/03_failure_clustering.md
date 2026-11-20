# Task 03: Group test failures by stack-trace signature (Python, ~30 min)

## Interviewer prompt
"Given a list of failure records `{test_id, message, stacktrace}`, group failures that are 'the same bug'
and return the top K groups with counts and an example. Traces differ in line numbers, memory addresses, ids and temp paths."

## Hidden NFR hooks
- **Correctness:** normalization rules (line numbers, hex addresses, UUIDs, numbers, temp paths) → a stable signature. Keep the top N frames only.
- **Performance (basic):** precompiled regexes; `Counter` + `heapq.nlargest` / `most_common(k)`; O(n · trace length).
- **Extensibility (critical-ish):** normalizers as an ordered list of `(pattern, replacement)` data, so a new rule doesn't touch the code. A `Signer` protocol leaves room for an embedding-based signer later.
- **Security (basic):** traces can contain secrets or PII (tokens in URLs). Redact before storing or printing examples.
- Not needed: ML clustering for v1 (name it as the step after the deterministic baseline: "LLM at the edges, code in the middle").

## Expert moves
1. Trace two traces by hand that differ only in line numbers and an address → same signature.
2. Design pick: deterministic normalization + a hash (explainable, fast) **vs** embeddings + clustering (fuzzy, costly). Deterministic first, with the cost argument.
3. Tests: a parametrized normalizer table (input line → normalized), a group-count test, a top-K tie-break test (stable ordering).
4. Property: normalizing is idempotent (`norm(norm(x)) == norm(x)`).
5. Mention evaluation: a small labeled set of "same bug" pairs gives precision/recall for the signer. That's the eval mindset.

## Likely follow-ups
- "Two different bugs collide in one signature?": include the exception type + top 3 app frames, and exclude framework frames.
- "Use an LLM?": embeddings for near-duplicates when the deterministic signature misses; an LLM to *name* the cluster. Cache by signature, and keep a human in the loop.
- "Streaming / incremental?": maintain `Counter` + an examples dict; merge partial results from workers.
