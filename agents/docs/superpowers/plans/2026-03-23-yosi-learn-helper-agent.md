# yosi_learn_helper Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a conversational Claude skill (`/learn`, `@yosi_learn`) that proactively briefs Yosi on his learning status and accepts natural-language commands to update progress, mark items done, and advance the schedule.

**Architecture:** Two-file skill (SKILL.md = behavior layer, AGENT_CONTEXT.md = knowledge layer). SKILL.md is self-contained for Cursor compatibility and embeds a schema summary. On every invocation Claude reads both live YAML config files, computes derived state, and opens with a status briefing.

**Tech Stack:** Markdown skill files, YAML data files, Claude's built-in Read + Edit tools for all mutations.

**Spec:** `docs/superpowers/specs/2026-03-23-yosi-learn-helper-agent-design.md`

---

## Task 0: Create Agent Directory

**Files:**
- Create directory: `/Users/yosii/work/git/personal_code/agents/yosi_learn_helper/`

- [ ] **Step 1: Create the directory**

```bash
mkdir -p /Users/yosii/work/git/personal_code/agents/yosi_learn_helper
```

Expected: no error, directory exists.

---

## Task 1: YAML Migration — Add `progress` to LeetCode items

**Files:**
- Modify: `/Users/yosii/work/git/personal_KB/learning/config/tracks.yaml`

The LeetCode `items[]` array currently has no `progress` field. The skill's progress formula requires it (% of items `done` is derived, but the field must exist for consistency with other tracks and future use).

- [ ] **Step 1: Verify the current state**

Open `/Users/yosii/work/git/personal_KB/learning/config/tracks.yaml` and confirm all 16 LeetCode items under `id: leetcode` → `items:` have no `progress` field.

Expected: 16 items, each with only `name:` and `status: not_started`.

- [ ] **Step 2: Add `progress: 0` to all 16 LeetCode items**

For every item under `id: leetcode` → `items:`, add `progress: 0` directly after `status:`. The result for each item should look like:

```yaml
      - name: "Arrays & Strings"
        status: not_started
        progress: 0
```

Apply this to all 16 items:
Arrays & Strings, Hash Maps, Two Pointers, Sliding Window, Binary Search, Linked Lists, Stacks & Queues, Trees & BST, Graphs & BFS/DFS, Dynamic Programming, Greedy, Backtracking, Heap / Priority Queue, Tries, Union Find, Intervals.

- [ ] **Step 3: Validate YAML is still parseable**

Run:
```bash
python3 -c "import yaml; yaml.safe_load(open('/Users/yosii/work/git/personal_KB/learning/config/tracks.yaml'))" && echo "VALID"
```
Expected output: `VALID`

- [ ] **Step 4: Commit from personal_KB repo**

```bash
cd /Users/yosii/work/git/personal_KB
git add learning/config/tracks.yaml
git commit -m "chore: add progress field to all LeetCode items (agent prep)"
```

---

## Task 2: Create AGENT_CONTEXT.md

**Files:**
- Create: `/Users/yosii/work/git/personal_code/agents/yosi_learn_helper/AGENT_CONTEXT.md`

This is the knowledge layer. It contains canonical file paths, full schema with field-by-field docs, progress formulas, and mutation rules. It supplements SKILL.md when file tools are available.

- [ ] **Step 1: Create the file with the following exact content**

```markdown
# yosi_learn_helper — Agent Context

This file is read by the learning helper agent on every invocation (when file tools are available).
It supplements SKILL.md with the full schema reference.

---

## Canonical File Paths

| File | Absolute Path | Agent Access |
|------|--------------|--------------|
| tracks.yaml | `/Users/yosii/work/git/personal_KB/learning/config/tracks.yaml` | Read + Write |
| schedule.yaml | `/Users/yosii/work/git/personal_KB/learning/config/schedule.yaml` | Read + Write |
| Master Roadmap | `/Users/yosii/work/git/personal_KB/learning/MASTER_LEARNING_ROADMAP.md` | Read only |
| This file | `/Users/yosii/work/git/personal_code/agents/yosi_learn_helper/AGENT_CONTEXT.md` | Read only |

---

## schedule.yaml — Full Schema

```yaml
cycle_length: 8           # integer — total weeks per round-robin cycle
current_cycle: 1          # integer — which cycle we're in (agent-editable)
current_week: 1           # integer 1–cycle_length — position in current cycle (agent-editable)
start_date: "2026-03-23"  # ISO 8601 string — date current cycle started (agent-editable)
weeks:                    # array — one entry per week in the cycle (human-only)
  - week: 1               # integer — week number (1-indexed)
    track: udemy          # string — matches track id in tracks.yaml
    label: "Udemy AI/Bedrock"  # string — display label
```

**Agent-editable fields:** `current_cycle`, `current_week`, `start_date`
**Human-only:** `cycle_length`, `weeks[].week`, `weeks[].track`, `weeks[].label`

---

## tracks.yaml — Schema by Track

### Track: udemy (id: udemy)

```yaml
id: udemy
name: "Udemy Courses"
priority: 1
color: accent-udemy          # human-only
tiers:                       # array of tier objects
  - tier: 1                  # integer
    label: "Finish & AI/Bedrock"
    items:
      - name: "Course Name"  # string — human-only
        instructor: "Name"   # string — human-only
        status: not_started  # enum — agent-editable
        progress: 0          # integer 0–100 — agent-editable
```

**Progress formula:** `avg(item.progress for all items across all tiers)`, treating missing `progress` as 0. Round to nearest integer.

---

### Track: leetcode (id: leetcode)

```yaml
id: leetcode
name: "LeetCode"
priority: 2
items:                       # flat array of topic items
  - name: "Arrays & Strings" # string — human-only
    status: not_started      # enum — agent-editable
    progress: 0              # integer 0–100 — agent-editable
```

**Progress formula:** `round((count of items where status="done") / total_items * 100)`

---

### Track: ml (id: ml)

```yaml
id: ml
name: "ML Models"
priority: 3
phases:                      # array of phase objects
  - name: "Phase 1: Classical NLP"
    items:
      - name: "Bag of Words (BOW)"
        detail: "vectorize sentences in numpy"  # human-only
        status: not_started  # enum — agent-editable
llm_components:              # separate array — DISPLAY ONLY, not counted in progress %
  - name: "Attention Mechanism"
    status: done             # enum — agent-editable (but excluded from track % calculation)
```

**Progress formula:** `round((count of done items in phases[].items[] only) / total_phase_items * 100)`
**IMPORTANT:** Do NOT count `llm_components[]` toward the percentage. "Attention mechanism" and "Transformer architecture" appear in both arrays — counting both would inflate the %. Show `llm_components[]` in deep-dives as a separate section.

---

### Track: python (id: python)

```yaml
id: python
name: "Python Practice"
priority: 4
current_week: 1     # integer 1–48 — agent-editable (tracks curriculum position)
total_weeks: 48     # integer — human-only
cycles:             # array — display only, not used for progress calculation
  - cycle: 1
    weeks: "1-12"
    focus: "Foundation & Idioms"
    status: in_progress  # agent-editable
```

**Progress formula:** `round(track.current_week / track.total_weeks * 100)`
**Field clarification:** `tracks[id=python].current_week` is the Python curriculum week (1–48). This is SEPARATE from `schedule.yaml:current_week` (the round-robin cycle week, 1–8). They are independent.

When user says "I finished Python week 5" → update `tracks[id=python].current_week = 5`.
When user says "move to week 3" → update `schedule.yaml:current_week = 3`.

---

### Track: other (id: other)

```yaml
id: other
name: "Other Plans"
priority: 5
sections:
  - name: "Rust"
    status: in_progress  # enum — agent-editable
    progress: 3          # integer 0–100 — optional, agent-editable
    detail_paths:        # list of related files — human-only
      - "personal_code/code/rust/learning/..."
    notes: "..."         # human-only
```

**Progress formula (per section, evaluated in priority order):**
1. `status=done` → 100 (overrides any `progress` value present)
2. `status=in_progress` AND `progress` field present → use `progress` value
3. `status=in_progress` AND `progress` field absent → 50
4. `status=not_started` → 0 (overrides any `progress` value present)

**Track % = average of all section values (integer, round to nearest)**

---

## Status Enum

All `status` fields use: `not_started` | `in_progress` | `done`

---

## Round-Robin Schedule

8-week repeating cycle. Current mapping:

| Weeks | Track | Focus |
|-------|-------|-------|
| 1–2 | udemy | Udemy AI/Bedrock courses |
| 3 | leetcode | LeetCode problems |
| 4–5 | ml | ML models / NLP roadmap |
| 6 | python | Python 48-week curriculum |
| 7 | leetcode | LeetCode second pass |
| 8 | other | Rust / System Design / etc. |

---

## Current Week — Source of Truth

`schedule.yaml:current_week` is always authoritative.

Advisory check (show as suggestion in briefing if different):
`date_week = floor((today - start_date).days / 7) % cycle_length + 1`

Example: if start_date=2026-03-23 and today=2026-04-06, that's 14 days → week 3.

---

## All Agent-Editable Fields

| File | Field | Notes |
|------|-------|-------|
| schedule.yaml | `current_week` | 1–cycle_length |
| schedule.yaml | `current_cycle` | increment on new cycle |
| schedule.yaml | `start_date` | ISO 8601, set to today on new cycle |
| tracks.yaml | `items[].status` | any track, any item |
| tracks.yaml | `items[].progress` | udemy, leetcode, and other tracks only. ml track items have no `progress` field — do NOT add one. |
| tracks.yaml | `sections[].status` | other track |
| tracks.yaml | `sections[].progress` | other track |
| tracks.yaml | `cycles[].status` | python track |
| tracks.yaml | python track `current_week` | top-level field on python track |

## Never Touch

- `MASTER_LEARNING_ROADMAP.md`
- `learning/app/src/` (React dashboard — separate system)
- Any `name`, `instructor`, `detail`, `detail_paths`, `color`, `priority`, `total_weeks`, `current_day`, `subtitle`, `label`, `track` fields
- Structural YAML shape (no adding/removing items, tiers, phases, sections; no adding new fields to ml items)
```

- [ ] **Step 2: Verify the file was created**

```bash
wc -l /Users/yosii/work/git/personal_code/agents/yosi_learn_helper/AGENT_CONTEXT.md
```
Expected: file exists, ~150+ lines.

- [ ] **Step 3: Commit**

```bash
cd /Users/yosii/work/git/personal_code
git add agents/yosi_learn_helper/AGENT_CONTEXT.md
git commit -m "feat: add yosi_learn_helper AGENT_CONTEXT.md (knowledge layer)"
```

---

## Task 3: Create SKILL.md

**Files:**
- Create: `/Users/yosii/work/git/personal_code/agents/yosi_learn_helper/SKILL.md`

This is the primary behavior file. It must be self-contained (Cursor attaches a single file via `@yosi_learn`), so it embeds a schema summary inline. When file tools are available, it also instructs Claude to read AGENT_CONTEXT.md for the full schema.

- [ ] **Step 1: Create the file with the following exact content**

````markdown
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
````

- [ ] **Step 2: Verify the file was created**

```bash
wc -l /Users/yosii/work/git/personal_code/agents/yosi_learn_helper/SKILL.md
```
Expected: file exists, ~200+ lines.

- [ ] **Step 3: Commit**

```bash
cd /Users/yosii/work/git/personal_code
git add agents/yosi_learn_helper/SKILL.md
git commit -m "feat: add yosi_learn_helper SKILL.md (behavior layer)"
```

---

## Task 4: Create README.md

**Files:**
- Create: `/Users/yosii/work/git/personal_code/agents/yosi_learn_helper/README.md`

- [ ] **Step 1: Create the file**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
cd /Users/yosii/work/git/personal_code
git add agents/yosi_learn_helper/README.md
git commit -m "feat: add yosi_learn_helper README (invocation docs)"
```

---

## Task 5: Validate — Manual Smoke Tests

**Files:** None created — validation only.

These are manual tests. Run them in a Claude Code session after the files are in place.

- [ ] **Test 1: Basic briefing**

In Claude Code, invoke:
```
/learn
```
Or: "Use the skill at `/Users/yosii/work/git/personal_code/agents/yosi_learn_helper/SKILL.md`"

Expected output includes:
- "Cycle 1 · Week 1 of 8"
- "Active: Udemy AI/Bedrock"
- Udemy at **7%** (avg of all 12 items across 3 tiers: 76+0+0+0+0+0+0+0+0+0+0+3 = 79 / 12 = 6.58 → 7%)
- ML at **13%** (2 done / 15 total phase items: Phase1:4 + Phase2:2 + Phase3:2 + Phase4:4 + Phase5:3 = 15; Attention+Transformer done = 2/15 = 13.3 → 13%)
- Python at **2%** (week 1 of 48 = 2.08 → 2%)
- Other at **30%** (Rust:3, SysDes:0, Perf:0, Networking:0, PromptEng:50 → avg(3+0+0+0+50)/5 = 10.6 → 11%). Note: verify the actual % against live data at test time.
- Overall % = avg of all 5 tracks
- "What would you like to do?"

- [ ] **Test 2: Mark an item done**

Say: "mark Naive Bayes Classifier done"

Expected:
- Agent finds the item in ml track, Phase 1
- Edits `tracks.yaml`: status: done on "Naive Bayes Classifier"
- Confirms: "Done. Naive Bayes Classifier → done. ML Models: [updated %]%"
- Re-verify by checking `tracks.yaml` directly

- [ ] **Test 3: Update course progress**

Say: "set Claude Code to 82%"

Expected:
- Agent edits `tracks.yaml`: progress: 82 on "Claude Code - The Practical Guide"
- Confirms with new Udemy %
- Re-verify `tracks.yaml`

- [ ] **Test 4: Move schedule week**

Say: "move to week 2"

Expected:
- Agent edits `schedule.yaml`: current_week: 2
- Confirms: "Done. Schedule moved to week 2. Active track: Udemy AI/Bedrock"
- Re-verify `schedule.yaml`
- Then say "move to week 1" to reset

- [ ] **Test 5: Ambiguous item (expected disambiguation)**

The ml track has "Attention mechanism" in `phases[3].items[]` and "Attention Mechanism" in `llm_components[]` (different capitalization, same concept). The agent should catch this on case-insensitive matching.

Say: "mark attention mechanism not started"

Expected:
- Agent matches the name case-insensitively against both phases items AND llm_components
- Finds matches in two locations: Phase 4 and LLM Components
- Asks before editing: "I found 'Attention mechanism' in Phase 4 and in LLM Components — which one should I update?"
- Do NOT confirm which one to update (we're only testing that disambiguation is triggered, not the edit itself)
- Type "cancel" or "never mind" to abort

- [ ] **Test 6: Track deep-dive**

Say: "how am I doing on ML?"

Expected:
- Shows all phases with item statuses
- Shows llm_components as a separate section (5 done, 3 planned)
- Lists detail_paths for reference

- [ ] **Test 7: Today's plan**

Say: "what should I study today?"

Expected:
- Recommends Claude Code Practical Guide as primary (76%)
- Mentions Amazon Bedrock as next-up
- Gives a time budget suggestion

- [ ] **Test 8: Start next cycle**

First note the current values: `current_cycle: 1`, `current_week: 1`, `start_date: "2026-03-23"`.

Say: "start next cycle"

Expected:
- Agent edits `schedule.yaml`: `current_cycle: 2`, `current_week: 1`, `start_date: "{today's date in YYYY-MM-DD}"`
- Confirms: "Done. Cycle 2 started. Week 1 of 8. Active: Udemy AI/Bedrock"
- Re-verify `schedule.yaml` directly

**Cleanup:** Say "move to week 1" then manually reset `current_cycle: 1` and `start_date: "2026-03-23"` in `schedule.yaml`.

- [ ] **Test 9: Upcoming schedule**

Say: "what's next after this week?"

Expected:
- Shows weeks 2–4 (or similar) from `schedule.weeks`
- Includes track labels and a brief status note for each upcoming track
- Does not error on week boundary (e.g., if on week 8, wraps to next cycle)
