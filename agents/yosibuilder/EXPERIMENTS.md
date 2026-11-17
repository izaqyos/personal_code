# Experiments

## 2026-11-16: does the local worker save cloud usage?

Setup: three small cards (slugify, parse_duration, LRUCache), each with a full design and test plan
(signatures, steps, exact test names and cases). Each card was built twice from the same commit:
`--mode cloud` (Sonnet worker + Sonnet lead) and `--mode hybrid` (qwen3-coder:30b draft + local clean-up,
Sonnet lead, Sonnet fix on reject). Cost is the CLI's list-price `total_cost_usd`, used as a proxy for
subscription usage. One run per card per mode, so the numbers are indicative, not statistics.

| Card | Cloud: rounds, $, wall | Hybrid: rounds, $, wall | Hybrid vs cloud |
|---|---|---|---|
| T1 slugify | 1, $0.051, 24 s | 1, $0.022, 42 s | -56% |
| T2 parse_duration | 1, $0.058, 28 s | 2, $0.084, 78 s | +44% |
| T3 LRUCache | 1, $0.055, 25 s | 2, $0.091, 264 s | +66% |
| Total | 3/3 first round, $0.164, 77 s | 1/3 first round, $0.197, 384 s | +20% |

Per-call costs: Sonnet worker about $0.035-0.043, Sonnet lead about $0.018-0.026.
Qwen rejections: a missing type annotation and a boilerplate docstring (T2); a test that skipped the card's
scenario and read private state, duplicated code, and a missing class docstring (T3).

Break-even: a hybrid card costs one lead call if Qwen passes first time (about $0.022) and lead + cloud fix + lead
if not (about $0.086); a cloud card costs about $0.055. Hybrid saves usage only if Qwen's first-time accept rate
is above about 50%. Observed: 1/3.

Other findings:
- A default headless `claude -p` call carries about 44k tokens of overhead (MCP tools, memory, settings); with
  `--strict-mcp-config --setting-sources "" --no-session-persistence` it is under 1k. The largest saving found.
- With a full design and test plan, the Sonnet worker passed every card first time at about $0.05 per card. The
  spec made the cloud worker cheap, so there was little typing left for the local model to save.
- Earlier runs with behaviour-only cards (no design or test plan): Qwen blocked 3/3 runs on slugify.

## 2026-11-16/17: free gates, and six crews on six cards

Changes before this run: free deterministic gates (ruff `ANN`, `D`, `C901` max 5; a test-plan name check; a
built-in mutation test), the worker loops on them before any review; three harder cards added (T4 text chunker,
T5 token bucket with injected clock, T6 typed retry decorator). Every crew built T1-T6 from the same commit, one
run each, `--mode cloud` unless noted. Results are in the ledger (`yb report`, source `experiment-2026-11-16`).

| Crew (worker / lead) | Accepted | At first review | Claude $ / card | Weighted $ / accepted card | Gemini tokens |
|---|---|---|---|---|---|
| Sonnet / Sonnet | 5/6 | 5 | 0.136 | 0.163 | 0 |
| Qwen hybrid, Sonnet fixes / Sonnet | 5/6 | 1 | 0.090 | 0.108 | 0 |
| Hydrogen / Sonnet | 5/6 | 4 | 0.036 | 0.117 | 1.3M |
| Hydrogen / Hydrogen | 6/6 | 4 | 0.000 | 0.068 | 1.5M |
| **Haiku / Hydrogen** | **6/6** | **6** | **0.007** | **0.012** | 0.08M |
| Flash / Hydrogen | 5/6 | 3 | 0.000 | 0.272 | 5.0M |

Weighted dollars use `config/prices.json` (Gemini at the placeholder rate, weight 0.25). Wall times are not
compared: the machine slept overnight during several runs.

Findings:
- Haiku with a full design and test plan matched or beat every other worker, at about 1/20 of Sonnet's Claude
  cost. The detailed card moves the thinking to the architect; a small worker is then enough. Made the default.
- T6 blocked both Sonnet-led crews for a card defect, not a worker one: the design put the whole retry loop in
  one nested function, over the C901 limit of 5, so workers extracted a helper and the Sonnet lead rejected the
  helper as off-design. The Hydrogen lead accepted it. Lesson: check the design against the gates (Flow step 3).
  The Hydrogen lead is also the more lenient one; compare its verdicts with Sonnet's on real work before
  trusting it fully.
- Flash used 3-5 times the tokens of Hydrogen through `agy` agent loops, and its first run failed outright: `agy`
  denied a harmless `ls`, which ends a headless turn with no output. Workers now allow read-only commands.
- The mutation test caught real gaps in every crew's first drafts (boundary values such as `capacity == 1`).
- A mutant that loops forever needs its whole process group killed on timeout, not just the shell (fixed).
- Wall time for Qwen hybrid was several times the cloud crews', and it still spent Claude on fixes and reviews.
