---
name: craft-frame
description: Frame a coding task like a senior engineer before writing code — restate, trace an example, ask ≤3 multiple-choice questions, set an NFR budget (security, resilience, performance, scalability, observability, extensibility), compare 2 designs, fix interfaces, failure modes and the test list. Use at the start of any non-trivial build.
argument-hint: "<task>"
---

# craft-frame: understand and design

SUITE = `~/work/git/personal_code/agents/senior_dev_craft`. Route through `SUITE/wiki/index.md` rows `design`,
`ai-collab` and the language row, and read ≤3 sources. The template is `SUITE/playbooks/design-note-template.md`,
and the lens checklist is `SUITE/playbooks/nfr-lenses.md`.

## Steps
1. **Restate** in 2–3 lines: inputs, outputs, constraints (language/version, deps allowed, time box, scale n).
2. **Trace one concrete example by hand**, input → output, including one edge case. If the brief has examples, check they agree with each other.
3. **Ask ≤3 questions, only if blocking.** Each one is multiple choice with a recommendation: "Duplicates: (a) keep last [recommended: matches upsert semantics], (b) keep first, (c) error". Anything not blocking: state the assumption and continue.
4. **NFR budget.** For each lens in `nfr-lenses.md`, set a level of none/basic/critical from the requirements, with a one-line decision and its cost. Say what is deliberately not built. This table is the main senior signal, so keep it honest and small.
5. **Two designs, one pick.** One line each with pro/con, then pick, with the reason tied to the budget. Give complexity for the stated n.
6. **Interfaces:** signatures / endpoint + schema, data model and invariants. Put seams *only* at likely-change points (`~/work/git/personal_KB/system-design/extensibility-seams.md`).
7. **Failure modes:** dependency slow/down, bad input, duplicates, partial failure → the behavior for each.
8. **Test list:** one line per behavior, grouped as happy / edges / errors / NFR proofs. These become the failing tests in build.
9. Write the note (fill in the template) to `DESIGN.md`, or show it in chat in showcase mode.

## Gate
Stop for approval in `showcase` and `standard` modes. Then hand over to `SUITE/skills/craft-build/SKILL.md`.

## Anti-patterns
Coding before the example is traced. Open-ended questions. An NFR table with everything "critical". Abstractions with no
named likely change. A test list that only covers the happy path.
