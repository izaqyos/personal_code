# leetcode_coach

A LeetCode practice coaching agent that guides problem-solving without giving answers.

## Invocation

### Claude Code (recommended)

Type `/leetcode-coach` in any Claude Code session. Registered as a global command.

### Cursor

**Option A (single file):**
1. In Cursor chat, type `@` and search for `SKILL.md`
2. Select `agents/leetcode_coach/SKILL.md`
3. Type your request (e.g., "let's practice LeetCode")

**Option B (both files — full context):**
1. Attach both `SKILL.md` and `AGENT_CONTEXT.md` via `@` mention

## Session Lifecycle

1. **Pick** — suggests 2-3 problems for current topic at different difficulties
2. **Scaffold** — creates solution file with description, signature, test cases
3. **Solve** — user works; agent provides hints when asked (never code)
4. **Review** — correctness, Python style, complexity, alternative approaches

## Data Files

| File | Purpose |
|------|---------|
| `interviewQs/leetcode/*.md` | Problem banks + solve logs |
| `interviewQs/leetcode/*.py` | Solution files |
| `personal_KB/learning/config/tracks.yaml` | Topic list and status (read only) |
| `personal_KB/learning/config/schedule.yaml` | Current week/track (read only) |

## Agent Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Overview for Cursor `@` mention |
| `AGENT_CONTEXT.md` | Full schema: paths, topic mapping, solve log format |
| `README.md` | This file |
| `~/.claude/commands/leetcode-coach.md` | Global Claude Code command (full behavior) |
