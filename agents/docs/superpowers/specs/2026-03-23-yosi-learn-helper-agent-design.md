# yosi_learn_helper Agent — Design Spec

**Date:** 2026-03-23
**Status:** Draft
**Location:** `agents/yosi_learn_helper/`

---

## Overview

A conversational Claude skill that helps Yosi manage his personal learning system. On every invocation it generates a proactive briefing — current cycle/week, active track, item-level progress — and accepts natural-language commands to update progress, mark items done, and advance the schedule.

Invocation:
- Claude Code: `/learn` (via Skill tool, name `learn`)
- Cursor: `@yosi_learn` (attaches `SKILL.md` + `AGENT_CONTEXT.md` as context)

---

## Goals

- Proactive briefing on every invocation (no need to ask "where am I?")
- Natural-language progress updates ("mark LDA done", "set Claude Code to 85%")
- Schedule advancement ("move to week 3", "start next cycle")
- Track-level and item-level status queries ("how am I doing on ML?")
- YAML mutations via Claude's Edit tool — no separate CLI required

---

## Non-Goals

- No Python CLI component
- Does not edit `MASTER_LEARNING_ROADMAP.md` (human-maintained)
- No notification system or cron scheduling
- No web UI or API

---

## File Structure

```
agents/
└── yosi_learn_helper/
    ├── SKILL.md           # Behavior protocol: triggers, briefing format, command handling
    ├── AGENT_CONTEXT.md   # Schema reference: file paths, YAML conventions, track types
    └── README.md          # How to invoke from Claude Code and Cursor
```

### Data sources (read-only except schedule.yaml and tracks.yaml)

```
personal_KB/learning/
├── MASTER_LEARNING_ROADMAP.md   # Human-maintained source of truth (read-only for agent)
└── config/
    ├── tracks.yaml              # All track/item progress (agent reads + writes)
    └── schedule.yaml            # Current cycle/week position (agent reads + writes)
```

---

## Architecture

### Approach: SKILL.md + AGENT_CONTEXT.md (Modular)

**SKILL.md** — the behavior layer. Contains:
- Trigger conditions and invocation instructions
- Briefing generation protocol (what to read, what to compute, how to format)
- Command recognition and handling (mark done, update %, advance week/cycle)
- Mutation rules (which fields are agent-editable)
- Cursor `@yosi_learn` instructions

**AGENT_CONTEXT.md** — the knowledge layer. Contains:
- Canonical file paths for all data sources
- Full YAML schema with field-by-field docs for each track type
- Status enum values (`not_started`, `in_progress`, `done`)
- Progress computation formula per track type
- Round-robin schedule logic
- `start_date` → current calendar week formula
- Mutation safety rules (human-only fields)

### Data Flow

```
Invocation (/learn or @yosi_learn)
    → Load SKILL.md
    → Read AGENT_CONTEXT.md
    → Read config/schedule.yaml
    → Read config/tracks.yaml
    → Compute derived state:
        - current calendar week from start_date
        - active track from schedule.weeks[current_week]
        - per-track progress %
        - overall % (average of all tracks)
    → Render briefing
    → Accept commands
```

### Mutation Flow

```
User: "mark LDA done"
    → Parse intent: set item status
    → Locate item in tracks.yaml (ml track, phase 1, "LDA (Latent Dirichlet Allocation)")
    → Edit tracks.yaml: status: done
    → Re-read tracks.yaml to verify
    → Confirm: "Done. LDA marked complete. ML Models track: 15% (+5%)"
```

---

## Behavior Protocol

### On Every Invocation

1. Read `AGENT_CONTEXT.md`, `schedule.yaml`, `tracks.yaml`
2. Use `schedule.yaml:current_week` as the authoritative current week (see Source of Truth note below)
3. Optionally compute the date-derived week as advisory: `floor((today - start_date).days / 7) % cycle_length + 1`. If it differs from `current_week`, mention it in the briefing as a suggestion ("Based on today's date you may be in week 2 — say 'move to week 2' to update").
4. Identify active track from `schedule.weeks[current_week - 1].track`
5. Render briefing (see format below)
6. Prompt for commands

**Source of Truth for current_week:** `schedule.yaml:current_week` always wins. The date formula is advisory only — it informs suggestions but never overrides the stored value. The user explicitly controls week position via "move to week N" or "start next cycle".

### Briefing Format

```
Cycle {N} · Week {W} of {cycle_length}  |  Active: {track_label}
Week started: {week_start_date}  |  Today: {today}

FOCUS: {top in-progress item in active track with current progress}
NEXT UP: {next not_started item in active track}

Overall: {overall_pct}% across all tracks
─────────────────────────────────────────────
Udemy       {pct}%  {status_label}
LeetCode    {pct}%  {status_label}  {← active if applicable}
ML Models   {pct}%  {status_label}
Python      {pct}%  {status_label}
Other       {pct}%  {status_label}
─────────────────────────────────────────────
What would you like to do?
```

Note: Track names in the briefing are display-only labels, not command shortcuts. Commands always use natural language (e.g., "how am I doing on LeetCode?", not "[B]").

### Commands

| Natural language | Action | Fields edited |
|---|---|---|
| "mark X done / in progress / not started" | Set item status | `tracks.yaml` → item `status` |
| "set [course] to N%" | Set item progress | `tracks.yaml` → item `progress` |
| "move to week N" | Advance/set week | `schedule.yaml` → `current_week` |
| "start next cycle" | New cycle | `schedule.yaml` → increment `current_cycle`, set `current_week: 1`, set `start_date` to today's date in ISO 8601 format (e.g., "2026-05-11") |
| "what should I do today?" | Focused recommendation from active track | (read-only) |
| "how am I doing on [track]?" | Deep-dive track summary | (read-only) |
| "what's next after this week?" | Show upcoming schedule weeks | (read-only) |

### After Any YAML Mutation

1. Confirm the specific change made
2. Show updated progress for the affected track
3. Re-display the relevant portion of the briefing

---

## YAML Schema (summary)

### schedule.yaml

```yaml
cycle_length: 8          # weeks per cycle
current_cycle: 1         # which cycle we're in
current_week: 1          # which week within the cycle (1-indexed)
start_date: "2026-03-23" # date cycle started (ISO 8601)
weeks:
  - week: 1
    track: udemy         # matches track id in tracks.yaml
    label: "Udemy AI/Bedrock"
```

**Agent-editable:** `current_cycle`, `current_week`, `start_date`

### tracks.yaml — Item status

All items share:
```yaml
status: not_started | in_progress | done
progress: 0-100      # optional, % complete (Udemy courses + Rust)
```

**Agent-editable:** `status`, `progress` on any item
**Human-only:** structural fields (`name`, `instructor`, `detail`, `detail_paths`, `color`, `priority`)

### Track types

| Track id | Items live under | Progress formula |
|---|---|---|
| `udemy` | `tiers[].items[]` | avg `progress` field of all items across all tiers (treat missing `progress` as 0) |
| `leetcode` | `items[]` | `(count of items where status=done / total items) * 100` |
| `ml` | `phases[].items[]` only | `(count of done items in phases / total items in phases) * 100`. `llm_components[]` is shown separately in deep-dive but excluded from the % to avoid double-counting (Attention and Transformer appear in both arrays). |
| `python` | top-level track fields | `(track.current_week / track.total_weeks) * 100`. Source fields: `tracks[id=python].current_week` (integer, 1–48, agent-editable) and `tracks[id=python].total_weeks` (integer, human-only). When user says "I finished Python week 5" or similar, the agent updates `tracks[id=python].current_week`. This field is separate from `schedule.yaml:current_week` (which tracks the round-robin cycle position). |
| `other` | `sections[]` | Per section, evaluate in this priority order: (1) if `status=done` → 100, regardless of any `progress` value; (2) if `status=in_progress` and `progress` is present → use `progress`; (3) if `status=in_progress` and `progress` is absent → 50; (4) if `status=not_started` → 0, regardless of any `progress` value. Final track % = avg of all section values. |

**Ambiguous item names:** If a command targets an item name that appears in multiple locations (e.g., "Attention mechanism" exists in both `phases[3].items[]` and `llm_components[]`), the agent asks the user to disambiguate before editing. Example: "I found 'Attention mechanism' in Phase 4 and in LLM Components — which one should I update?"

---

## One-Time Setup Steps (before agent goes live)

These are migration tasks to run once during implementation — they fix gaps in the current YAML data before the agent depends on them.

| Task | Action | File |
|---|---|---|
| LeetCode items missing `progress` field | Add `progress: 0` to all 16 LeetCode items | `tracks.yaml` |
| `detail_paths` surfacing | No data change needed — agent reads these paths when user asks for a deep-dive on a track | — |

---

## Cursor Compatibility

- `@yosi_learn` in Cursor attaches `SKILL.md` as context (Cursor `@` mentions attach a single file)
- `SKILL.md` must be self-contained enough to work alone: it must contain all behavior rules and the full briefing protocol inline, not delegated to `AGENT_CONTEXT.md`
- `SKILL.md` instructs: "If file tools are available, also read `AGENT_CONTEXT.md` from the same directory for full schema details. If not (e.g., Cursor without file tools enabled), the schema summary embedded in this file is sufficient."
- `AGENT_CONTEXT.md` is a companion for Claude Code and for Cursor users who manually attach both files
- `README.md` documents how to attach both files in Cursor (drag into context or use `@` + `@` for both)

---

## AGENT_CONTEXT.md Skeleton

The knowledge layer file must contain these sections (implementer fills in full content):

```markdown
# yosi_learn_helper — Agent Context

## Canonical File Paths
- tracks.yaml:   /Users/yosii/work/git/personal_KB/learning/config/tracks.yaml
- schedule.yaml: /Users/yosii/work/git/personal_KB/learning/config/schedule.yaml
- roadmap:       /Users/yosii/work/git/personal_KB/learning/MASTER_LEARNING_ROADMAP.md (read-only)

## Schedule Schema
[full schedule.yaml field docs]

## Track Schema by Type
[per-track field docs: udemy, leetcode, ml, python, other]

## Progress Formulas
[exact formulas per track as defined in spec]

## Status Enum
not_started | in_progress | done

## Agent-Editable Fields
[list of fields the agent may write]

## Human-Only Fields
[list of fields the agent must never write]

## Round-Robin Logic
[8-week cycle explanation, week-to-track mapping]
```

---

## Files Not To Touch

- `MASTER_LEARNING_ROADMAP.md` — human-maintained, agent never edits this
- App source files (`learning/app/src/`) — dashboard is separate from agent
- Track `name`, `instructor`, `detail`, `color`, `priority` fields — structural, human-only

---

## Success Criteria

- Invoking `/learn` gives an accurate, up-to-date briefing without any extra prompting
- "Mark X done" correctly edits the right item in `tracks.yaml`
- "Move to week 3" correctly updates `schedule.yaml`
- "Start next cycle" increments cycle, resets week, updates start_date
- Agent never touches human-only fields
- Works from both Claude Code (`/learn`) and Cursor (`@yosi_learn`)
