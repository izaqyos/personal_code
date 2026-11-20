# Working with the LLM: the expert moves

Grounded in your own protocol (`KB/ml-and-ai/agentic/working-with-ai-on-prod-grade-projects.md`, grade A),
compressed for a live 45-minute session. The human is the engineer of record. The model is a fast,
well-read, overconfident pair who needs a spec, gates and review.

## Before any code
1. **Context first.** Give the model the task, the constraints (language/version, no new deps, time box), the files that matter, and the standards (this suite). A prompt is a spec: inputs, outputs, error behavior, NFR levels.
2. **Plan before code.** Ask for a short plan with interfaces and a test list, and review it once. Re-planning mid-build is where time and tokens burn.
3. **Ask for options, decide yourself.** "Give me 2 designs with trade-offs, recommend one." Decisions are multiple choice with a recommendation, never open-ended.
4. **Profile the data/examples before designing.** Trace one concrete example by hand. Briefs lie and data tells the truth.

## While building
5. **Small diffs.** ≤ 30 lines per step, each with its tests. Read every line before accepting it, and narrate one "why" per non-obvious choice.
6. **Tests are the eval set.** Write or approve the failing tests first, then let the model make them pass. A green suite plus the gates (ruff/mypy/tsc) is the acceptance criterion, not the model saying "done".
7. **Run instead of trusting.** Execute tests, the example and edge cases. "It should work" is not evidence.
8. **Distrust the model's characteristic failures:**
   - invented or outdated APIs and flags (check against the installed version);
   - dead defensive code and guards for impossible inputs;
   - swallowed errors and silent fallbacks;
   - over-abstraction (base classes for one implementation);
   - tests that assert nothing or mirror the implementation;
   - docs that claim features the code doesn't have (docs are claims, so grep them).
9. **Take the keyboard back** when a fix is two lines, when the model loops on the same failure twice, or when you know the answer. Say so: "faster if I just do it."
10. **LLM at the edges, code in the middle.** In the product too: the model understands and phrases, while deterministic code decides, computes and validates.

## After building
11. **Critic pass with a different persona**, with fresh eyes on the diff: "You're a principal engineer reviewing this for security, resilience and readability. Rank the findings, and prove each one with an input." Then verify each claim yourself. Critics hallucinate too.
12. **Proportionate hardening.** Walk the NFR lenses against the budget you set in the frame. Fix what the budget demands, and name the rest as next steps.
13. **Own mistakes as facts**: what happened, the fix, the test that proves it. No apologies, no drama.

## Things to say out loud (they show the ML/LLM fluency)
- "I'm giving it the constraints up front: it's much better at following a spec than at guessing one."
- "I'll have it propose two designs. I want to see the trade-off before it commits to one."
- "Tests first, so I have an oracle. The model's confidence isn't one."
- "That API doesn't exist in this version. Classic hallucination, so I'm checking the installed signature."
- "Second pass with a reviewer persona. Different framing surfaces different failures, like an ensemble."
- "This code calls an LLM, so I treat its output as untrusted input: parse, validate, and fall back."
- "Cheap deterministic checks first, then the model only where judgment is needed. It's cheaper, faster and explainable."
