# Daily Standup Timer - Specification Document

**Version:** 1.0
**Date:** 2026-01-04
**Author:** Yosi Izaq / Claude
**Team:** Imagine Dragons

---

## 1. Executive Summary

The Daily Standup Timer is a Python application designed to manage and optimize daily standup meetings for the Imagine Dragons team. The application enforces time limits per speaker, tracks meeting history, and provides analytics to identify patterns and improve meeting efficiency.

### Problem Statement
Daily standup meetings are taking too long, reducing team productivity and focus time.

### Solution
A timer application with:
- Per-developer configurable time limits (default: 3 minutes)
- Visual alerts and warnings
- Meeting history tracking and analytics
- Two interface modes: Streamlit UI and Interactive CLI

---

## 2. Functional Requirements

### 2.1 Core Timer Features

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | Global meeting timer tracking total elapsed time | Must |
| FR-02 | Individual timer per developer (default 180 seconds) | Must |
| FR-03 | 30-second transition period between speakers | Must |
| FR-04 | Visual warning at 30 seconds remaining (yellow) | Must |
| FR-05 | Visual alert at 0 seconds (red/flashing) | Must |
| FR-06 | Grace period of 15 seconds after timer expires | Must |
| FR-07 | Auto-advance to next speaker after grace period | Must |
| FR-08 | Overtime counter when speaker exceeds limit | Must |

### 2.2 Moderator Controls

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-09 | Pause/Resume global timer | Must |
| FR-10 | Pause/Resume individual speaker timer | Must |
| FR-11 | Skip current speaker (move to next) | Must |
| FR-12 | Add time to current speaker (+30s, +1m) | Must |
| FR-13 | Re-order remaining speakers during meeting | Must |
| FR-14 | Mark speaker as absent | Must |
| FR-15 | End meeting early | Must |
| FR-16 | Restart meeting (reset all timers) | Should |

### 2.3 Speaker Order Management

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-17 | Default alphabetical order by first name | Must |
| FR-18 | Drag-and-drop reorder in UI mode | Should |
| FR-19 | Number-based reorder in CLI mode | Must |
| FR-20 | Save custom order as new default | Could |
| FR-21 | Randomize order option | Could |

### 2.4 History & Analytics

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-22 | Save meeting data to history.json after each meeting | Must |
| FR-23 | Maximum 2000 entries with FIFO overwrite | Must |
| FR-24 | Track: date, total duration, per-person times | Must |
| FR-25 | Track: overtime per person, attendance | Must |
| FR-26 | Dashboard showing average meeting duration | Must |
| FR-27 | Dashboard showing per-person average time | Must |
| FR-28 | Dashboard showing overtime frequency per person | Must |
| FR-29 | Trend graph: meeting duration over time | Should |
| FR-30 | "Top overtime offenders" leaderboard | Should |
| FR-31 | Filter analytics by date range | Should |

### 2.5 Session Recovery

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-32 | Auto-save session state every 5 seconds | Must |
| FR-33 | Detect incomplete session on startup | Must |
| FR-34 | Prompt to resume or discard incomplete session | Must |
| FR-35 | Recovery file: `.session_recovery.json` | Must |

### 2.6 Configuration

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-36 | External `config.json` for all defaults | Must |
| FR-37 | Per-developer custom time limits | Should |
| FR-38 | Configurable transition time | Should |
| FR-39 | Configurable grace period | Should |
| FR-40 | Configurable warning threshold | Should |

### 2.7 Multi-Team Support

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-41 | Support multiple team JSON files in `teams/` directory | Must |
| FR-42 | Team selector dropdown in UI on startup | Must |
| FR-43 | Team selector prompt in CLI on startup | Must |
| FR-44 | Separate history files per team (`history_{team_id}.json`) | Must |
| FR-45 | Remember last selected team | Should |
| FR-46 | CLI flag to specify team: `--team <team_id>` | Should |
| FR-47 | Default team configurable in config.json (default: `imagine_dragons`) | Must |

---

## 3. Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | Timer accuracy | < 100ms drift per minute |
| NFR-02 | UI responsiveness | < 200ms for all interactions |
| NFR-03 | Startup time | < 3 seconds |
| NFR-04 | Memory usage | < 100MB |
| NFR-05 | Python version | 3.10+ |
| NFR-06 | Platform | macOS (primary), Linux (secondary) |
| NFR-07 | No internet required | Fully offline capable |

---

## 4. User Stories

### As a Moderator (Team Lead)

1. **Start Daily**: I want to start the daily standup with one click/command so the meeting begins immediately.

2. **Monitor Time**: I want to see the global timer and current speaker's remaining time prominently so I know the meeting status at a glance.

3. **Handle Overtime**: I want visual alerts when someone exceeds their time so I can politely interrupt without watching the clock.

4. **Adjust on the Fly**: I want to skip absent team members or reorder speakers so the meeting flows naturally.

5. **Review History**: I want to see which meetings ran long and who contributed to overtime so I can address patterns.

### As a Team Member

1. **Know My Time**: I want to see my remaining time clearly so I can wrap up appropriately.

2. **Fair Treatment**: I want everyone to have the same time limit so no one dominates the meeting.

---

## 5. Data Models

### 5.1 Team Members (Enhanced Schema)

**File:** `team_members.json`

```json
{
  "team": {
    "name": "Imagine Dragons",
    "emoji": "🐉",
    "group_manager": {
      "name": "Keren Greenblat",
      "email": "kereng@checkpoint.com"
    },
    "team_leader": {
      "name": "Yosi Izaq",
      "email": "yosii@checkpoint.com"
    }
  },
  "members": [
    {
      "id": "chen",
      "name": "Chen Ben Hamo",
      "display_name": "Chen",
      "email": "chenben@checkpoint.com",
      "github": "chkp-chenben",
      "role": "Cross-stack developer",
      "specialization": ["Route table", "tunnel operations", "DNS policy"],
      "daily_config": {
        "default_time_seconds": 180,
        "active": true
      }
    }
  ]
}
```

**Suggested Additions to Existing Schema:**

| Field | Type | Purpose |
|-------|------|---------|
| `id` | string | Unique identifier for history tracking |
| `display_name` | string | Short name for UI (e.g., "Muhe" for Muhammad) |
| `daily_config.default_time_seconds` | int | Per-person time override |
| `daily_config.active` | bool | Exclude from daily when on vacation |

### 5.2 Configuration Schema

**File:** `config.json`

```json
{
  "version": "1.0",
  "timer": {
    "default_speaker_time_seconds": 180,
    "transition_time_seconds": 30,
    "grace_period_seconds": 15,
    "warning_threshold_seconds": 30
  },
  "alerts": {
    "warning_color": "#FFA500",
    "overtime_color": "#FF0000",
    "flash_on_overtime": true
  },
  "history": {
    "file_path": "history_{team_id}.json",
    "max_entries": 2000
  },
  "recovery": {
    "enabled": true,
    "auto_save_interval_seconds": 5,
    "file_path": ".session_recovery.json"
  },
  "ui": {
    "theme": "light",
    "show_avatars": false
  },
  "teams": {
    "directory": "teams",
    "default_team": "imagine_dragons"
  },
  "default_order": "alphabetical"
}
```

### 5.3 History Entry Schema

**File:** `history.json`

```json
{
  "version": "1.0",
  "entries": [
    {
      "id": "2026-01-04T09:00:00Z",
      "date": "2026-01-04",
      "start_time": "09:00:00",
      "end_time": "09:18:45",
      "total_duration_seconds": 1125,
      "expected_duration_seconds": 1230,
      "status": "completed",
      "participants": [
        {
          "member_id": "chen",
          "display_name": "Chen",
          "status": "present",
          "allocated_time_seconds": 180,
          "actual_time_seconds": 165,
          "overtime_seconds": 0,
          "order_position": 1
        },
        {
          "member_id": "muhe",
          "display_name": "Muhe",
          "status": "absent",
          "allocated_time_seconds": 0,
          "actual_time_seconds": 0,
          "overtime_seconds": 0,
          "order_position": null
        }
      ],
      "notes": ""
    }
  ]
}
```

### 5.4 Session Recovery Schema

**File:** `.session_recovery.json`

```json
{
  "session_id": "2026-01-04T09:00:00Z",
  "started_at": "2026-01-04T09:00:00Z",
  "last_updated": "2026-01-04T09:05:30Z",
  "global_elapsed_seconds": 330,
  "current_speaker_index": 2,
  "speaker_order": ["chen", "miri", "muhe", "osher", "yair", "yocheved"],
  "completed_speakers": [
    {"member_id": "chen", "actual_time_seconds": 175},
    {"member_id": "miri", "actual_time_seconds": 125}
  ],
  "current_speaker_elapsed_seconds": 30,
  "is_in_transition": false,
  "absent_members": []
}
```

---

## 6. Interface Specifications

### 6.1 Streamlit UI Layout

```
+------------------------------------------------------------------+
|  🐉 Imagine Dragons Daily Standup                    [Analytics]  |
+------------------------------------------------------------------+
|                                                                   |
|     TOTAL TIME: 08:45 / ~21:00                                   |
|     ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░  42%                  |
|                                                                   |
+------------------------------------------------------------------+
|                                                                   |
|  CURRENT SPEAKER                                                  |
|  ┌────────────────────────────────────────────────────────────┐  |
|  │                                                            │  |
|  │              👤 MUHE (Muhammad)                            │  |
|  │                                                            │  |
|  │                   2:15                                     │  |
|  │              ████████████░░░░░  75%                        │  |
|  │                                                            │  |
|  │    [⏸ Pause]  [+30s]  [+1m]  [Skip ⏭]                     │  |
|  │                                                            │  |
|  └────────────────────────────────────────────────────────────┘  |
|                                                                   |
+------------------------------------------------------------------+
|  QUEUE                                        [🔀 Reorder]        |
|  ┌──────────────────────────────────────────────────────────┐    |
|  │  ✅ Chen (2:55)  ✅ Miri (2:45)  🎤 Muhe  ⏳ Osher       │    |
|  │  ⏳ Yair  ⏳ Yocheved                                    │    |
|  └──────────────────────────────────────────────────────────┘    |
+------------------------------------------------------------------+
|  [⏸ Pause All]  [End Meeting]  [Mark Absent ▼]                   |
+------------------------------------------------------------------+
```

**Color States:**
- **Green**: Time remaining > 30s
- **Yellow/Orange**: Time remaining <= 30s (warning)
- **Red**: Overtime (timer shows negative or overtime count)
- **Flashing Red**: Grace period exceeded

### 6.2 CLI Interface Layout

```
╔══════════════════════════════════════════════════════════════════╗
║  🐉 Imagine Dragons Daily Standup                                ║
║  Total: 08:45 / ~21:00                                           ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║   CURRENT: Muhe (Muhammad)                                       ║
║   ┌─────────────────────────────────────────────────────────┐    ║
║   │                        2:15                             │    ║
║   │   [████████████████████░░░░░░░░░░]  75%                 │    ║
║   └─────────────────────────────────────────────────────────┘    ║
║                                                                   ║
║   Queue: ✅Chen ✅Miri 🎤Muhe ⏳Osher ⏳Yair ⏳Yocheved         ║
║                                                                   ║
╠══════════════════════════════════════════════════════════════════╣
║  Commands:                                                        ║
║  [p]ause  [s]kip  [+] add 30s  [a]bsent  [r]eorder  [q]uit       ║
╚══════════════════════════════════════════════════════════════════╝
```

### 6.3 Analytics Dashboard (Streamlit)

```
+------------------------------------------------------------------+
|  📊 Analytics Dashboard                    [Last 30 days ▼]       |
+------------------------------------------------------------------+
|                                                                   |
|  SUMMARY                                                          |
|  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  |
|  │ Avg Daily  │  │ Total      │  │ On-Time    │  │ Overtime   │  |
|  │  18:32     │  │ Meetings   │  │   Rate     │  │  Leader    │  |
|  │ (target:21)│  │    22      │  │   68%      │  │   Yair     │  |
|  └────────────┘  └────────────┘  └────────────┘  └────────────┘  |
|                                                                   |
+------------------------------------------------------------------+
|  MEETING DURATION TREND                                           |
|  25m │                                                            |
|  20m │──────────────────────────────────── target                 |
|  15m │    ╭─╮  ╭──╮     ╭╮                                        |
|  10m │╭──╯   ╰─╯    ╰───╯╰──╮╭──                                 |
|   5m │                                                            |
|      └──────────────────────────────────────────────────          |
|        Jan 1                                    Jan 4             |
+------------------------------------------------------------------+
|  PER-PERSON STATS                                                 |
|  ┌────────────────────────────────────────────────────────────┐  |
|  │ Name       │ Avg Time │ Overtime % │ Attendance │ Trend    │  |
|  │────────────│──────────│────────────│────────────│──────────│  |
|  │ Chen       │  2:45    │    5%      │   100%     │    ↓     │  |
|  │ Miri       │  2:30    │    0%      │    95%     │    →     │  |
|  │ Muhe       │  2:55    │   10%      │   100%     │    →     │  |
|  │ Osher      │  3:15    │   25%      │    90%     │    ↑     │  |
|  │ Yair       │  3:30    │   35%      │   100%     │    ↑     │  |
|  │ Yocheved   │  2:40    │    5%      │    85%     │    ↓     │  |
|  └────────────────────────────────────────────────────────────┘  |
+------------------------------------------------------------------+
```

---

## 7. State Machine

### Meeting States

```
                    ┌─────────────┐
                    │    IDLE     │
                    │ (No meeting)│
                    └──────┬──────┘
                           │ start_meeting()
                           ▼
                    ┌─────────────┐
         ┌─────────│  TRANSITION │◄────────────┐
         │         │ (30s break) │             │
         │         └──────┬──────┘             │
         │                │ transition_complete│
         │                ▼                    │
         │         ┌─────────────┐             │
         │    ┌───►│  SPEAKING   │─────┐       │
         │    │    │(timer runs) │     │       │
         │    │    └──────┬──────┘     │       │
         │    │           │            │       │
         │  resume()   pause()    time_up()   │
         │    │           │            │       │
         │    │    ┌──────▼──────┐     │       │
         │    └────│   PAUSED    │     │       │
         │         └─────────────┘     │       │
         │                             ▼       │
         │                      ┌───────────┐  │
         │                      │   GRACE   │  │
         │                      │ (15s warn)│  │
         │                      └─────┬─────┘  │
         │                            │        │
         │              ┌─────────────┴────────┘
         │              │ grace_expired OR next_speaker()
         │              ▼
         │       ┌─────────────┐
         │       │ NEXT_SPEAKER│
         │       └──────┬──────┘
         │              │
         │    ┌─────────┴─────────┐
         │    │                   │
         │    ▼ has_next          ▼ no_more
         └────┘              ┌─────────────┐
                             │  COMPLETED  │
                             │(save history)│
                             └──────┬──────┘
                                    │
                                    ▼
                             ┌─────────────┐
                             │    IDLE     │
                             └─────────────┘
```

---

## 8. Error Handling

| Scenario | Handling |
|----------|----------|
| `team_members.json` not found | Show setup wizard to create file |
| `config.json` not found | Create with defaults, notify user |
| `history.json` corrupted | Backup corrupted file, create new |
| Recovery file found on startup | Prompt: "Resume previous session?" |
| Member removed mid-meeting | Skip gracefully, log warning |
| All members marked absent | End meeting, save minimal record |

---

## 9. Acceptance Criteria

### MVP (Version 1.0) - COMPLETE

- [x] Timer counts down accurately for each speaker
- [x] Visual warning at 30 seconds remaining
- [x] Visual alert at overtime
- [x] Auto-advance after grace period
- [x] Moderator can pause/skip/add time
- [x] Meeting history saved to JSON
- [x] Both Streamlit and CLI modes functional
- [x] Session recovery works after crash

### Version 1.1 - COMPLETE

- [x] Full analytics dashboard
- [x] Trend graphs
- [x] Custom order persistence
- [x] Per-person time customization

### Running the Application

```bash
# Streamlit UI Mode (default)
python main.py

# CLI Mode
python main.py --mode cli

# View Meeting History
python main.py --mode history
python main.py --mode history --days 7 --limit 10

# Specify team directly
python main.py --team sample_team

# After pip install -e .
daily-timer --team sample_team
daily-timer --mode history
```

---

## 10. Glossary

| Term | Definition |
|------|------------|
| **Daily** | Daily standup meeting |
| **Speaker** | Team member currently giving their update |
| **Transition** | 30-second break between speakers |
| **Grace Period** | 15 seconds after timer expires before auto-advance |
| **Overtime** | Time spent beyond allocated limit |
| **Moderator** | Person controlling the meeting (typically Team Lead) |
