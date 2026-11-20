# Design note template (fits on one screen)

`craft-frame` fills this in before any code. Keep each section to 1–4 lines. Write it into `DESIGN.md` at the
repo root (or show it in chat during a live session).

```markdown
# <feature>: design note

**Problem:** <one sentence: who needs what, and why now>
**Inputs → outputs:** <shapes, sizes (n), sources; example in → example out>
**Out of scope:** <what we deliberately won't do>

## NFR budget
| Lens | Level | Decision | Cost |
|---|---|---|---|
| Security | none/basic/critical | <e.g. validate at boundary; no secrets in logs> | <~lines/time> |
| Resilience | | | |
| Performance | | <budget: p99 / throughput / n> | |
| Scalability | | | |
| Observability | | | |
| Extensibility | | <seams at likely-change points only> | |

## Design
- **Option A** <one line> — pro / con
- **Option B** <one line> — pro / con
- **Pick:** <A|B> because <reason tied to the budget>

**API / interfaces:** <signatures or endpoint + schema>
**Data model:** <records, keys, invariants>
**Failure modes:** <dependency down / slow / bad input / duplicate → behavior>
**Complexity:** <time / space for the stated n>

## Test plan
- happy: <...>   - edges: <empty, one, dup, boundary, unicode, huge>   - errors: <...>
- NFR proofs: <fault injection / property test / concurrency test / micro-bench>

## Extension points (named, not built)
<seam> → <likely future change>
```
