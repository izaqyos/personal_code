# leetcode_coach

A coaching agent for LeetCode practice. Guides problem selection, scaffolding, hints, and post-solve review. Never solves problems for the user.

## Invocation

### Claude Code (recommended)

Type `/leetcode-coach` in any Claude Code session.

### Cursor

**Option A (single file):**
1. In Cursor chat, type `@` and search for `SKILL.md`
2. Select `agents/leetcode_coach/SKILL.md`
3. Type your request (e.g., "let's practice LeetCode")

**Option B (both files — full context):**
1. Attach both `SKILL.md` and `AGENT_CONTEXT.md` via `@` mention

## What It Does

### Session lifecycle:
1. **Pick** — suggests 2-3 problems for the current topic at different difficulties
2. **Scaffold** — creates solution file with description, signature, and test cases
3. **Solve** — user works; agent provides hints when asked (never code, never answers)
4. **Review** — correctness, Python style, complexity analysis, alternative approaches

### Hint strategies (context-dependent mix):
- **Socratic** — guiding questions
- **Pattern-based** — names the pattern
- **Layered** — escalating: nudge → bigger hint → pseudocode

### Post-solve review covers:
- Correctness + edge cases
- Python style tips
- Time/space complexity analysis
- Alternative approaches (novel DS, algorithms, math, probabilistic/large-scale)

## Data Files

| File | Purpose |
|------|---------|
| `interviewQs/leetcode/*.md` | Problem banks + solve logs (agent creates/appends) |
| `interviewQs/leetcode/*.py` | Solution files (agent scaffolds) |
| `personal_KB/learning/config/tracks.yaml` | Topic list and status (read only) |
| `personal_KB/learning/config/schedule.yaml` | Current week/track (read only) |

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Behavior layer — session lifecycle, hint engine, review protocol |
| `AGENT_CONTEXT.md` | Knowledge layer — paths, schema, topic mapping |
| `README.md` | This file |
