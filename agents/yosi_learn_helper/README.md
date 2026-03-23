# yosi_learn_helper

A conversational Claude skill that proactively briefs you on your learning status
and handles natural-language commands to manage progress and schedule.

## Invocation

### Claude Code (recommended)

Type `/learn` in any Claude Code session. The Skill tool loads `SKILL.md` automatically.

If `/learn` isn't registered yet, invoke it manually:
> "Use the yosi_learn_helper skill at `/Users/yosii/work/git/personal_code/agents/yosi_learn_helper/SKILL.md`"

Or use the Skill tool directly in Claude Code:
```
Skill: learn
```

### Cursor

**Option A (single file — minimal setup):**
1. In Cursor chat, type `@` and search for `SKILL.md`
2. Select `agents/yosi_learn_helper/SKILL.md`
3. Type your request (e.g., "give me my learning briefing")

**Option B (both files — full schema context):**
1. Attach both `SKILL.md` and `AGENT_CONTEXT.md` via `@` mention
2. This gives the full schema reference for more accurate responses

**Option C (add as Cursor Doc):**
1. Open Cursor Settings → Features → Docs
2. Add: `/Users/yosii/work/git/personal_code/agents/yosi_learn_helper/SKILL.md`
3. Name it `yosi_learn`
4. Now `@yosi_learn` works directly in Cursor chat

## What It Does

On every invocation, the agent:
1. Reads `config/schedule.yaml` and `config/tracks.yaml` from the personal_KB repo
2. Computes current cycle/week, active track, per-track progress, overall %
3. Opens with a status briefing

Then accepts commands:

| Command | Example |
|---------|---------|
| Mark item done | "mark LDA done" |
| Set progress | "set Claude Code to 85%" |
| Advance Python week | "I finished Python week 5" |
| Move schedule week | "move to week 3" |
| Start next cycle | "start next cycle" |
| Track deep-dive | "how am I doing on ML?" |
| Today's plan | "what should I study today?" |
| Upcoming schedule | "what's next after this week?" |

## Data Files

| File | Purpose |
|------|---------|
| `personal_KB/learning/config/tracks.yaml` | All track + item progress (agent writes) |
| `personal_KB/learning/config/schedule.yaml` | Current cycle/week position (agent writes) |
| `personal_KB/learning/MASTER_LEARNING_ROADMAP.md` | Source of truth (human-maintained, read-only) |

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Behavior layer — self-contained, works in Cursor |
| `AGENT_CONTEXT.md` | Knowledge layer — full schema, read when file tools available |
| `README.md` | This file |
