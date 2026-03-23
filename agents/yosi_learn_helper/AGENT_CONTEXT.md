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
current_day: 2      # integer — human-only, NEVER TOUCH
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

**Live sections and their formula case:**
- Rust: in_progress, progress: 3 → case 2 → 3
- System Design: not_started → case 4 → 0
- Performance: not_started → case 4 → 0
- Networking: not_started → case 4 → 0
- Prompt Engineering: in_progress, no progress field → case 3 → 50

**Progress formula (per section, evaluated in priority order):**
1. `status=done` → 100 (overrides any `progress` value present)
2. `status=in_progress` AND `progress` field present → use `progress` value
3. `status=in_progress` AND `progress` field absent → 50
4. `status=not_started` → 0 (overrides any `progress` value present)

**Track % = average of all section values (integer, round to nearest)**
Example: (3+0+0+0+50)/5 = 10.6 → 11%

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
| 8 | other | Rotate: Rust / SysDes |

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
