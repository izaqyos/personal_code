---
name: craft-harden
description: Walk the code through the NFR lenses (security, resilience, performance/latency, scalability, rate limits, observability, extensibility, LLM-specific) at the levels set in the frame's budget; each finding becomes fix + test that proves it. Proportionate — no gold-plating. Use after build or on existing code before shipping.
argument-hint: "[lens ...]"
---

# craft-harden: NFR lens pass

SUITE = `~/work/git/personal_code/agents/senior_dev_craft`. Checklist: `SUITE/playbooks/nfr-lenses.md`. For each lens at
basic or critical, route through `SUITE/wiki/index.md` and read its A page. The red-flag lists at the bottom of each gap page (catalog `kind = "gap"`, e.g. `~/work/git/personal_KB/system-design/resilience-patterns.md`)
are the scan targets.

## Steps
1. Re-read the NFR budget from the frame (`DESIGN.md` or the chat). No budget yet? Set one first, per `craft-frame` step 4.
2. For each lens at **basic** or **critical**, scan the diff for that lens's red flags and answer its "Ask" question.
3. Record each finding as one row: **lens · location · problem · triggering input/scenario · fix · proving test**.
4. Fix in priority order: security → data loss/correctness under failure → resource exhaustion → the rest. Every fix lands with the test that would have caught it (`SUITE/skills/craft-test/SKILL.md`), and the gates stay green.
5. **Proportionality:** a lens at **none** gets no work, and an idea above its level gets *named, not built*: "Circuit breaker: not needed at basic; it's the next step if the vendor's SLA is weak."
6. Output the table and the "deliberately not built" list.

## Always-on checks (any level)
- Untrusted input validated at the boundary. No string-built SQL/shell. No unsafe deserialization.
- No secrets or PII in code, logs or errors.
- Every remote call has a timeout. No unbounded retry, queue, fan-out or page size.
- Errors aren't swallowed. A failure path is observable (logged once, with context).
- Code that calls an LLM treats its output as untrusted: parse, validate, have a fallback, and set token/latency limits.
