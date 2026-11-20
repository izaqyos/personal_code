---
name: craft
description: Senior-engineer coding loop with an LLM — frame (design + NFR budget) → build (TDD) → test → harden (NFR lenses) → review (critic) — grounded in the user's audited KB/code wiki. Use for any non-trivial coding task, or `/craft showcase <task>` for a live, narrated, time-boxed session (e.g. an interview screen share).
argument-hint: "[showcase|quick] <task>"
---

# craft: the loop

**Suite root (SUITE):** `~/work/git/personal_code/agents/senior_dev_craft`. All paths below are relative to it.

## On every invocation
1. Read `wiki/profile.md` once per session. It sets the register: senior, evidence-based, proportionate.
2. Pick the mode from the first word of the arguments:
   - `showcase`: live session. Gates after frame and after every build increment, a one-line "why" per decision, visible time boxes.
   - `quick`: no gates, compressed narration, for small tasks.
   - otherwise `standard`: gates after frame and before hardening.
3. Detect the language from the repo (`pyproject.toml` / `package.json` / `tsconfig.json`) or the task. Ask only if it's genuinely ambiguous.
4. Run the phases in order. For each phase, read and follow its skill file. Those files are the source of truth.

| # | Phase | Skill file | Showcase box (45 min) | Output |
|---|---|---|---|---|
| 1 | Frame | `skills/craft-frame/SKILL.md` | 8 min | design note with NFR budget, test list |
| 2 | Build | `skills/craft-build/SKILL.md` | 20 min | code + tests in ≤30-line increments, gates green |
| 3 | Test | `skills/craft-test/SKILL.md` | 4 min | NFR proof tests (fault injection, property, concurrency) |
| 4 | Harden | `skills/craft-harden/SKILL.md` | 4 min | lens findings → fixes → proving tests |
| 5 | Review | `skills/craft-review/SKILL.md` | 5 min | ranked findings, each verified |
| 6 | Docs | `playbooks/project-docs.md` | 2 min | `README.md` + `ARCHITECTURE.md` (with Mermaid diagrams), commands verified |
| 7 | Wrap | (below) | 2 min | summary with numbers |

## Grounding: the LLM wiki (every phase)
- Start each phase by routing through `wiki/index.md`: pick the rows for this phase, the NFR lenses at basic or critical, and the language.
- Read **at most 3** sources, A grade first. **B** sources: read only the sections listed. Never open C/D sources (they aren't routed).
- **Cite what you used** in one short line: "Using your resilience page: full jitter inside a deadline."
- If a root or page is missing (another machine), skip it, say so, and fall back to the playbooks.
- Never read `personal_KB_private` or anything outside the routed paths. The screen may be shared.

## Narration rules (showcase)
- Before each phase, say the phase name and its time box. When a box is overrun, say what you're cutting.
- One line per decision: "dict over list: O(1) lookups by test id".
- At a gate, stop and ask for "go". Proposed decisions are multiple choice with a recommendation.
- Show evidence, not claims: run tests and print the numbers.
- When the human takes the keyboard, follow their lead. Say a disagreement once, with the reason, then do what they decide.

## Project docs (always, every mode, `quick` included)
Every run leaves **`README.md`** (purpose, features, install, usage + config, test, run, limitations) and
**`ARCHITECTURE.md`** (high-level overview, a Mermaid component diagram of the major boxes, a sequence diagram of the
main flow through the system, key decisions, NFR placement, extension points) at the project root. Follow the
templates in `playbooks/project-docs.md`. Write them from the code as built, update them in place if they exist, and
run every README command before the wrap. A run without both files is not done.

## Wrap (always)
- **Built:** files, how to run them (point at `README.md` / `ARCHITECTURE.md`). **Evidence:** tests (count, coverage), lint/type results, any timing.
  Re-run the gates for the wrap and copy the numbers **verbatim** from that output. Never round up
  ("99%" is not "100%"); in the 03/11 dry run the model overclaimed exactly this way.
- **NFR budget vs delivered:** one line per lens at basic/critical.
- **Deliberately not built,** and the next step for each ("extension ready" points).
- **Wiki used:** the sources cited. Anything missing or wrong in them goes in a one-line "wiki feedback" note.
