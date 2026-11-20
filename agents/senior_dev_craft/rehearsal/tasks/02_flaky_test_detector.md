# Task 02: Flaky-test detector (Python, ~30 min)

## Interviewer prompt
"CI writes one line per test run: `timestamp,commit,test_id,outcome` (outcome PASS/FAIL/SKIP). Find flaky tests:
tests that both passed and failed on the **same commit**. Report them ranked by how often they flip."

## Hidden NFR hooks
- **Performance/scalability (critical):** logs can be GBs, so stream line by line; memory O(distinct (commit, test)), not O(lines).
- **Correctness:** SKIP doesn't count; the same commit across reruns; malformed lines (count and skip with a warning, don't crash).
- **Observability (basic):** report malformed-line count; log the summary, not every line.
- **Extensibility (basic):** input as `Iterable[str]` (file, S3 stream or test list all work); output as data, with printing done separately.
- Not needed: a database, parallelism (I/O-bound single pass is fast enough; say how you'd shard by commit if it weren't).

## Expert moves
1. Trace 5 lines by hand: commit c1 has t1 PASS and t1 FAIL → flaky. Commit c2 has only t1 PASS → not flaky on c2.
2. Data structure out loud: `dict[(commit, test), set[Outcome]]`, then aggregate per test: commits where flaky, flip count.
3. `TestResult.parse` value object with boundary validation (see `~/work/git/personal_KB/python/modern-python-playbook.md`). A generator pipeline for constant memory.
4. Tests: a parametrized table of small logs, a malformed-lines test, and a property test: shuffling the lines doesn't change the result.
5. State complexity: O(n) time, O(k) memory. Say "this streams" out loud.

## Likely follow-ups
- "Flips across *consecutive* runs, not just both outcomes?": sort by timestamp per (commit, test), count transitions.
- "100 GB of logs?": shard by hash(commit) across workers (map-reduce), merge counts.
- "How would you classify *why* it's flaky?" (their domain): cheap heuristics first (timeouts, order dependence), then an LLM judge on the stack traces, with human review. This is your bug-triage story.
