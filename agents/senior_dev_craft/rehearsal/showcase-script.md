# Showcase script: 45 minutes of coding with an LLM (screen share)

Goal: show them **how an expert works with AI**, not that the AI can code. What they should see: framing before code, a proportionate NFR budget, tests as the oracle, small verified steps, catching the model's mistakes, and grounding in your own engineering knowledge.

## Before the call (T-30 min)
- [ ] Fresh scratch dir: `mkdir -p ~/work/scratch/r2 && cd ~/work/scratch/r2 && git init -q`. Python: `uv init --lib -q`. TS: `npm init -y && npm i -D typescript vitest @types/node`.
- [ ] `claude` started there; `/craft` autocompletes (skills installed). Terminal font large, dark theme.
- [ ] **Screen hygiene:** close Slack/mail/WhatsApp/personal tabs, notifications off (Focus), no `personal_KB_private` or career folders open, terminal cleared. Share **one window**, not the whole desktop.
- [ ] Backup: `adapters/PROMPT.md` open in an editor tab, in case they ask you to use *their* tool or a plain chat.
- [ ] Water. The cheat card (PDF) on a second screen or on paper.

## Opening (min 0–2): set the frame out loud
"I'll work the way I do on real projects. I frame first, with a small design note and an explicit NFR budget, so I build what the problem needs and no more. Then tests first, in small steps, and I read every line the model writes. I've packaged my workflow as Claude Code skills grounded in my own engineering notes. You'll see it cite them."
→ type: `/craft showcase <their task, pasted verbatim>`

## Frame (min 2–10)
- Let it restate, then **you** trace one example out loud (paper or a comment). Correct anything it got wrong. That's a visible expert move.
- Answer its MCQ questions quickly. Overrule a recommendation once if you have a reason ("keep-first, because CI reruns are later attempts").
- **NFR table:** read it, adjust one level ("security is critical here, the payload is external") and strike one item ("no circuit breaker at this scope; it's the next step").
- Two designs → pick, with the reason. Say the complexity. Say "go".

## Build (min 10–32)
- Increment 1: the core happy-path tests → code. **Read the diff out loud in one breath per function.** Run the gates and show green.
- Increment 2: edges + errors. Increment 3: the NFR decision that matters most (retry/limit/idempotency/streaming).
- **Planned expert moments (do at least two):**
  1. Catch something: an invented API, a missing timeout, a swallowed exception, a test that asserts nothing. "Classic LLM failure. Let me check the actual signature."
  2. Take the keyboard for a two-line fix: "faster if I just do it." Then let it continue.
  3. Ask it for an alternative: "give me the async version's trade-off in two lines". Then decide yourself.
  4. Say a "deliberately not built" item out loud.
- If you're overrunning at min 28: skip to the most important NFR test and say what you're cutting.

## Test + harden (min 32–38)
- `/craft-test fault` (or let the loop do it): a fake that times out/429s, asserting attempts and delays with an injected clock. **Show it run.**
- Harden: a quick lens table. Fix one real finding with its test.

## Review (min 38–43)
- `/craft-review`: the critic persona. When it reports findings: "I want a triggering input for each, because critics hallucinate too." Verify one live.

## Wrap (min 43–45)
- Let the wrap print: evidence (tests, coverage, lint/types), NFR budget vs delivered, not-built list, next steps.
- One sentence: "Same loop scales to a team: the skills are plain markdown in git, the wiki is graded, and the gates are in CI."

## If they ask about the skills
"The suite is six phase skills plus playbooks. The interesting part is the grounding. It routes to my own KB and code, which I audited and graded A–D. Only A sources are used in full and B sources only in parts; legacy pages are excluded, and topics with no good source got new pages whose examples run in CI." This is the LLM-wiki-over-RAG story from your code-review agent.

## Recovery lines
- The model goes off track: "Stop. Back to the plan: step 2 only." (Rejecting is part of the skill.)
- A test fails unexpectedly: "Good, that's what tests are for." Read the error, form a hypothesis, then fix. No random patches.
- Out of time: "Here's where I'd go next", then the not-built list.
