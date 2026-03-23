---
name: learn
description: Yosi's learning companion — proactive briefing, progress updates, schedule management. Use when asked about learning status, what to study today, marking items done, advancing schedule week/cycle, or any question about learning tracks. Triggers on /learn, @yosi_learn, or learning-related questions.
---

# yosi_learn_helper — Learning Companion

## On Every Invocation

### Step 1: Read data

Always read these two files first:
1. `/Users/yosii/work/git/personal_KB/learning/config/schedule.yaml`
2. `/Users/yosii/work/git/personal_KB/learning/config/tracks.yaml`

If file tools are available, also read:
3. `/Users/yosii/work/git/personal_code/agents/yosi_learn_helper/AGENT_CONTEXT.md`
(This has full schema details. If unavailable, use the Schema Summary section at the bottom of this file.)

### Step 2: Compute state

**Current week (source of truth):** `schedule.current_week`

**Advisory date-check:** Compute `floor((today - schedule.start_date).days / 7) % schedule.cycle_length + 1`. If this differs from `current_week`, flag it in the briefing as a suggestion.

**Active track:** `schedule.weeks[current_week - 1].track`

**Week start date:** `start_date + (current_week - 1) * 7 days`

**Per-track progress %** (see Progress Formulas section):
- udemy: avg of all item `progress` values
- leetcode: % of items with `status: done`
- ml: % of `phases[].items[]` with `status: done` (NOT llm_components)
- python: `current_week / total_weeks * 100`
- other: priority-ordered formula per section, then average

**Overall %:** average of all 5 track percentages

### Step 3: Render briefing

```
Cycle {current_cycle} · Week {current_week} of {cycle_length}  |  Active: {active_track_label}
Week started: {week_start_date}  |  Today: {today's date}

FOCUS: {top in-progress item in active track, or first not-started if none in-progress}
NEXT UP: {next not-started item after FOCUS}

Overall: {overall_pct}%
─────────────────────────────────────────────
Udemy       {pct}%  {in_progress/not_started/done}
LeetCode    {pct}%  {in_progress/not_started/done}
ML Models   {pct}%  {in_progress/not_started/done}
Python      {pct}%  {in_progress/not_started/done}
Other       {pct}%  {in_progress/not_started/done}
─────────────────────────────────────────────
What would you like to do?
```

If date-derived week ≠ stored week, append:
```
Note: Based on today's date you appear to be in week {date_week}. Say "move to week {date_week}" to update.
```

### Step 4: Wait for command

---

## Commands

### Mark item done / in progress / not started
**Triggers:** "mark X done", "X is done", "I finished X", "mark X in progress", "start X", "reset X"
**Action:**
1. Search for item by name (case-insensitive, partial match). Look in all tracks.
2. If ambiguous (multiple matches in different locations), ask: "I found 'X' in [location A] and [location B] — which one?"
3. Edit `status` field on the matched item in `tracks.yaml`
4. Re-read `tracks.yaml` to verify
5. Confirm: "Done. [Item name] → [new status]. [Track name]: [new %]% ([change]%)"

### Set progress percentage
**Triggers:** "set X to N%", "X is N% done", "update X to N percent"
**Action:**
1. Find item, validate N is 0–100
2. Edit `progress` field in `tracks.yaml`
3. Re-read, confirm: "Done. [Item] progress → N%. [Track]: [new %]%"

### Advance Python curriculum week
**Triggers:** "I finished Python week N", "mark Python week N done", "Python is at week N", "set Python week to N"
**Action:**
1. Edit `tracks[id=python].current_week` to N (this is the curriculum week, separate from schedule week)
2. Re-read, confirm: "Done. Python curriculum week → N. Python: [new %]%"

### Move schedule to week N
**Triggers:** "move to week N", "we're in week N", "advance to week N", "set week to N"
**Action:**
1. Validate N is 1–cycle_length
2. Edit `schedule.current_week` to N
3. Re-read, confirm: "Done. Schedule moved to week N. Active track: [new track label]"

### Start next cycle
**Triggers:** "start next cycle", "begin cycle N", "new cycle", "reset cycle"
**Action:**
1. Edit `schedule.yaml`:
   - `current_cycle`: increment by 1
   - `current_week`: set to 1
   - `start_date`: set to today's date, ISO 8601 format (YYYY-MM-DD)
2. Re-read, show new state: "Done. Cycle [N] started. Week 1 of 8. Active: [track]"

### Deep-dive on a track
**Triggers:** "how am I doing on X?", "show me ML", "tell me about Python", "LeetCode status"
**Action:**
Show all items for the track with their status. Include:
- udemy: tiers + items with % progress bars
- leetcode: all topics with done/not-started counts
- ml: phases with items + separate llm_components section
- python: cycles, current week position, next milestone
- other: all sections with status and notes

If track has `detail_paths`, list them: "Relevant files to consult: [paths]"

### What to study today
**Triggers:** "what should I study today?", "what should I focus on?", "give me a plan", "session plan"
**Action:**
Based on active track and in-progress items, recommend:
1. Primary: the most-progressed in-progress item (e.g., "Claude Code at 76% → aim for section X today")
2. Secondary: the next not-started item to begin
3. Time budget suggestion: e.g., "1 hr main focus + 20 min on secondary"

### What's coming up
**Triggers:** "what's next after this week?", "upcoming schedule", "what comes after week N?"
**Action:**
Show the next 3–4 weeks from `schedule.weeks`, their tracks, and a brief status of each track.

---

## Progress Formulas

**udemy:** `round(sum(item.progress for all items in all tiers) / total_items)`. Treat missing `progress` as 0.

**leetcode:** `round((count where status="done") / total_items * 100)`

**ml:** `round((count where status="done" in phases[].items[] only) / len(phases[].items[]) * 100)`
Do NOT include `llm_components[]` in this count — those items overlap with phases and would double-count.

**python:** `round(track.current_week / track.total_weeks * 100)`
Use `tracks[id=python].current_week` and `tracks[id=python].total_weeks` (top-level fields on the track, not inside `cycles[]`).

**other:** Per section, evaluate in this priority order:
1. `status=done` → 100 (regardless of `progress`)
2. `status=in_progress` AND `progress` present → use `progress`
3. `status=in_progress` AND `progress` absent → 50
4. `status=not_started` → 0 (regardless of `progress`)
Track % = `round(avg(section_values))`

**Overall:** `round(avg(udemy_pct, leetcode_pct, ml_pct, python_pct, other_pct))`

---

## Mutation Rules

**Surgical edits only.** Use Claude's Edit tool to change the exact field. Never reformat, restructure, or reorder YAML.

**After every mutation:**
1. Re-read the edited file to verify the change
2. Confirm with user: exact field changed, new value, updated track %

**Agent-editable:**
- `tracks.yaml`: `status` and `progress` on any item/section; `cycles[].status` on python; `tracks[id=python].current_week`
- `schedule.yaml`: `current_week`, `current_cycle`, `start_date`

**Never touch:**
- `MASTER_LEARNING_ROADMAP.md`
- `learning/app/src/` (React dashboard)
- `name`, `instructor`, `detail`, `detail_paths`, `color`, `priority`, `total_weeks`, `current_day`, `subtitle`, `label`, `track`
- Structural shape: no adding or removing items, tiers, phases, sections; no adding `progress` to ml items (they don't have it)

---

## Schema Summary (embedded for Cursor — no file tools needed)

### schedule.yaml
```yaml
cycle_length: 8          # human-only
current_cycle: 1         # agent-editable
current_week: 1          # agent-editable, 1–cycle_length
start_date: "2026-03-23" # agent-editable, ISO 8601
weeks:
  - week: 1              # human-only
    track: udemy         # human-only
    label: "..."         # human-only
```

### tracks.yaml — key structures

**udemy:** `tiers[].items[]` — item has `name` (human), `instructor` (human), `status` (editable), `progress` 0–100 (editable)

**leetcode:** `items[]` — item has `name` (human), `status` (editable), `progress` 0–100 (editable)

**ml:** `phases[].items[]` — item has `name` (human), `detail` (human), `status` (editable)
     `llm_components[]` — same structure, shown in deep-dives only, not counted in %

**python:** top-level `current_week` (editable, 1–48), `current_day` (human-only, never touch), `total_weeks: 48` (human-only), `cycles[]` (display only)

**other:** `sections[]` — section has `name` (human), `status` (editable), `progress` optional (editable), `detail_paths` (human), `notes` (human). Current sections: Rust (in_progress, progress:3), System Design (not_started), Performance (not_started), Networking (not_started), Prompt Engineering (in_progress, no progress field → case 3 → 50)
