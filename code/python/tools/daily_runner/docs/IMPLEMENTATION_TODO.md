# Daily Standup Timer - Implementation Todo List

**Status:** COMPLETE
**Completion Date:** January 2026

**Total Completed Tasks:** 67 tasks across 10 phases

---

## Phase Gates & Quality Requirements

### Gate Criteria (MUST pass before moving to next phase)

| Requirement | Target |
|-------------|--------|
| All phase tests pass | 100% |
| Code coverage | >= 80% |
| Type checking (mypy) | 0 errors |
| Linting (ruff) | 0 errors |
| Documentation updated | Yes |

### Documentation Requirements

Each phase must update relevant documentation:
- [x] **Docstrings**: All public functions/classes must have docstrings
- [x] **README.md**: Update with any new usage instructions
- [x] **SPECIFICATION.md**: Update if requirements change during implementation
- [x] **ARCHITECTURE.md**: Update if design changes during implementation
- [x] **Inline comments**: Add for complex logic only

### Running Quality Checks

```bash
# Run all tests with coverage
pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# Type checking
mypy src/

# Linting
ruff check src/ tests/

# All checks (must pass before phase completion)
make check  # or: pytest && mypy src/ && ruff check .
```

---

## Phase 1: Project Setup & Foundation

- [x] **1.1** Create project directory structure (`src/`, `tests/`, `data/`, etc.)
- [x] **1.2** Create `pyproject.toml` with dependencies and project metadata
- [x] **1.3** Create `requirements.txt` with pinned versions
- [x] **1.4** Create default `config.json` with all configurable values
- [x] **1.5** Set up `teams/` directory and move `team_members.json` → `teams/imagine_dragons.json`
- [x] **1.6** Create `.gitignore` (exclude `.session_recovery.json`, `history_*.json`)
- [x] **1.7** Create `src/__init__.py` and package structure

### Phase 1 Tests
- [x] **1.T1** Test: Verify all imports work correctly
- [x] **1.T2** Test: Config file loads with defaults when missing

### Phase 1 Gate
- [x] All tests pass (100%)
- [x] Coverage >= 80%
- [x] mypy clean
- [x] ruff clean
- [x] README.md created with setup instructions

---

## Phase 2: Data Models (Pydantic)

- [x] **2.1** Create `src/core/models.py` with all Pydantic models:
  - `DailyConfig`
  - `TeamMember`
  - `Team`
  - `TeamFile` (root model for team JSON)
  - `ParticipantStatus` (enum)
  - `ParticipantRecord`
  - `MeetingRecord`
  - `TimerConfig`
  - `AlertConfig`
  - `HistoryConfig`
  - `RecoveryConfig`
  - `UIConfig`
  - `AppConfig` (root config model)
  - `SessionRecovery`
- [x] **2.2** Add validation rules (e.g., time > 0, valid email format)
- [x] **2.3** Add model methods for serialization/deserialization

### Phase 2 Tests
- [x] **2.T1** Test: Valid team member model creation
- [x] **2.T2** Test: Invalid team member rejected (missing required fields)
- [x] **2.T3** Test: Config model with defaults
- [x] **2.T4** Test: Meeting record serialization round-trip
- [x] **2.T5** Test: Session recovery model validation

### Phase 2 Gate
- [x] All tests pass (100%)
- [x] Coverage >= 80%
- [x] mypy clean
- [x] ruff clean
- [x] All models have docstrings

---

## Phase 3: Data Layer (Repositories)

- [x] **3.1** Create `src/data/config_manager.py`:
  - `load()` - load config from file or create defaults
  - `save()` - persist config changes
  - `get()` / `set()` - access individual settings
- [x] **3.2** Create `src/data/team_repository.py`:
  - `list_teams()` - scan `teams/` directory
  - `load_team(team_id)` - load specific team file
  - `get_active_members()` - filter by `daily_config.active`
  - `get_member_by_id()`
  - `get_sorted_members(order)` - alphabetical or custom
- [x] **3.3** Create `src/data/history_repository.py`:
  - `__init__(team_id)` - team-specific history file
  - `load()` - load history from file
  - `save_entry(record)` - append with FIFO limit
  - `get_entries(filters)` - query with date range
  - `_enforce_limit()` - trim to 2000 entries
  - `_atomic_write()` - safe file persistence
- [x] **3.4** Create `src/data/recovery_manager.py`:
  - `has_recovery()` - check for recovery file
  - `load_recovery()` - parse recovery data
  - `save_recovery(state)` - persist current state
  - `clear_recovery()` - delete recovery file
  - `start_auto_save(interval, callback)` - periodic save

### Phase 3 Tests
- [x] **3.T1** Test: Config loads defaults when file missing
- [x] **3.T2** Test: Config persists changes correctly
- [x] **3.T3** Test: Team repository lists all teams in directory
- [x] **3.T4** Test: Team repository filters inactive members
- [x] **3.T5** Test: Team repository sorts alphabetically by display_name
- [x] **3.T6** Test: History enforces 2000 entry limit (FIFO)
- [x] **3.T7** Test: History atomic write survives interruption
- [x] **3.T8** Test: History handles corrupted file gracefully
- [x] **3.T9** Test: Recovery manager detects existing session
- [x] **3.T10** Test: Recovery manager auto-save triggers correctly
- [x] **3.T11** Test: Recovery manager clears file on completion

### Phase 3 Gate
- [x] All tests pass (100%)
- [x] Coverage >= 80%
- [x] mypy clean
- [x] ruff clean
- [x] All repository classes have docstrings

---

## Phase 4: Core Timer Engine

- [x] **4.1** Create `src/core/timer_engine.py`:
  - `__init__(duration_seconds)` - initialize timer
  - `start()` - begin countdown
  - `pause()` - freeze timer
  - `resume()` - continue from pause
  - `reset()` - restart timer
  - `add_time(seconds)` - extend duration
  - `elapsed_seconds` property - time used
  - `remaining_seconds` property - time left
  - `is_overtime` property - check if exceeded
  - `overtime_seconds` property - how much over
  - `is_running` property - current state
  - `is_paused` property - paused state
- [x] **4.2** Implement using `time.monotonic()` for drift resistance
- [x] **4.3** Handle edge cases (negative add_time, resume when not paused)

### Phase 4 Tests
- [x] **4.T1** Test: Timer counts down correctly over 10 seconds
- [x] **4.T2** Test: Timer accuracy < 100ms drift over 60 seconds
- [x] **4.T3** Test: Pause freezes elapsed time
- [x] **4.T4** Test: Resume continues accurately after pause
- [x] **4.T5** Test: Multiple pause/resume cycles maintain accuracy
- [x] **4.T6** Test: Add time extends remaining correctly
- [x] **4.T7** Test: Overtime detected when remaining < 0
- [x] **4.T8** Test: Reset restores initial state
- [x] **4.T9** Test: Cannot start already running timer
- [x] **4.T10** Test: Cannot resume non-paused timer

### Phase 4 Gate
- [x] All tests pass (100%)
- [x] Coverage >= 80%
- [x] mypy clean
- [x] ruff clean
- [x] TimerEngine class fully documented

---

## Phase 5: State Manager

- [x] **5.1** Create `src/core/state_manager.py`:
  - `MeetingState` enum (IDLE, TRANSITION, SPEAKING, PAUSED, GRACE, COMPLETED)
  - `StateManager` class with observer pattern
  - `transition_to(new_state)` - validate and change state
  - `add_observer(callback)` - register UI updates
  - `remove_observer(callback)` - unregister
  - `notify_observers()` - broadcast state changes
- [x] **5.2** Implement state transition validation matrix
- [x] **5.3** Track speaker queue and current index
- [x] **5.4** Track per-speaker elapsed times
- [x] **5.5** Handle absent members in queue

### Phase 5 Tests
- [x] **5.T1** Test: Valid state transitions succeed
- [x] **5.T2** Test: Invalid transitions raise exception
- [x] **5.T3** Test: All valid transitions covered (matrix test)
- [x] **5.T4** Test: Observers notified on state change
- [x] **5.T5** Test: Observer removal works correctly
- [x] **5.T6** Test: Speaker queue management (next, skip)
- [x] **5.T7** Test: Current speaker tracking accurate
- [x] **5.T8** Test: Absent member handling in queue

### Phase 5 Gate
- [x] All tests pass (100%)
- [x] Coverage >= 80%
- [x] mypy clean
- [x] ruff clean
- [x] StateManager and MeetingState fully documented

---

## Phase 6: Meeting Manager (Orchestration)

- [x] **6.1** Create `src/core/meeting_manager.py`:
  - `__init__(team_repo, config, history_repo, recovery_mgr)`
  - `start_meeting(speaker_order=None)` - begin new meeting
  - `end_meeting(save_history=True)` - conclude and save
  - `next_speaker()` - advance to next person
  - `skip_speaker()` - skip without time
  - `mark_absent(member_id)` - remove from queue
  - `pause()` / `resume()` - timer control
  - `add_time(seconds)` - extend current speaker
  - `reorder_speakers(new_order)` - change queue
  - `check_recovery()` - detect previous session
  - `restore_session()` - resume from recovery
  - `discard_recovery()` - start fresh
- [x] **6.2** Implement transition timer (30s between speakers)
- [x] **6.3** Implement grace period logic (15s overtime warning)
- [x] **6.4** Integrate auto-save for recovery
- [x] **6.5** Build meeting record on completion

### Phase 6 Tests
- [x] **6.T1** Test: Full meeting lifecycle (start → speakers → end)
- [x] **6.T2** Test: Meeting saves correct history record
- [x] **6.T3** Test: Skip speaker works mid-meeting
- [x] **6.T4** Test: Mark absent removes from queue
- [x] **6.T5** Test: Reorder updates remaining speakers
- [x] **6.T6** Test: Pause/resume affects all timers
- [x] **6.T7** Test: Add time extends current speaker
- [x] **6.T8** Test: Transition period between speakers
- [x] **6.T9** Test: Grace period triggers after time up
- [x] **6.T10** Test: Auto-advance after grace period
- [x] **6.T11** Test: Recovery file created during meeting
- [x] **6.T12** Test: Session restored correctly from recovery
- [x] **6.T13** Test: Discard recovery starts clean meeting
- [x] **6.T14** Test: End meeting clears recovery file

### Phase 6 Gate
- [x] All tests pass (100%)
- [x] Coverage >= 80%
- [x] mypy clean
- [x] ruff clean
- [x] MeetingManager fully documented
- [x] Core logic can run headless (no UI dependencies)

---

## Phase 7: Analytics Service

- [x] **7.1** Create `src/services/analytics_service.py`:
  - `get_summary_stats(days=30)` - overall metrics
  - `get_per_person_stats(days=30)` - individual breakdown
  - `get_duration_trend(days=30)` - time series data
  - `get_overtime_leaderboard(limit=5)` - top offenders
  - `get_attendance_stats(days=30)` - presence tracking
  - `calculate_on_time_rate()` - % meetings under target

### Phase 7 Tests
- [x] **7.T1** Test: Average duration calculated correctly
- [x] **7.T2** Test: Per-person stats aggregate properly
- [x] **7.T3** Test: Trend data points match date range
- [x] **7.T4** Test: Overtime leaderboard sorted correctly
- [x] **7.T5** Test: Empty history returns zero/empty stats
- [x] **7.T6** Test: Date filtering works correctly
- [x] **7.T7** Test: Attendance percentage calculated correctly

### Phase 7 Gate
- [x] All tests pass (100%)
- [x] Coverage >= 80%
- [x] mypy clean
- [x] ruff clean
- [x] AnalyticsService fully documented

---

## Phase 8: CLI Interface

- [x] **8.1** Create `src/cli/__init__.py`
- [x] **8.2** Create `src/cli/app.py` - main CLI entry point:
  - Team selection prompt (or `--team` flag)
  - Recovery detection and prompt
  - Main event loop
- [x] **8.3** Create `src/cli/display.py` - Rich terminal rendering:
  - `render_header(team_name)` - top banner
  - `render_timer(remaining, total)` - countdown with progress bar
  - `render_queue(speakers, current_index)` - speaker list
  - `render_controls()` - available commands
  - `render_warning()` - yellow state
  - `render_overtime()` - red/flashing state
- [x] **8.4** Create `src/cli/commands.py` - keyboard handlers:
  - `p` - pause/resume toggle
  - `s` - skip speaker
  - `+` - add 30 seconds
  - `a` - mark absent (show picker)
  - `r` - reorder (show interface)
  - `q` - quit/end meeting
- [x] **8.5** Implement live refresh (100ms tick)
- [x] **8.6** Handle terminal resize gracefully

### Phase 8 Tests
- [x] **8.T1** Test: CLI starts and shows team selection
- [x] **8.T2** Test: `--team` flag skips selection
- [x] **8.T3** Test: Recovery prompt shown when file exists
- [x] **8.T4** Test: Timer display updates correctly
- [x] **8.T5** Test: Keyboard commands trigger correct actions
- [x] **8.T6** Test: Warning colors appear at threshold
- [x] **8.T7** Test: Overtime display works correctly
- [x] **8.T8** Test: Quit saves history and clears recovery

### Phase 8 Gate
- [x] All tests pass (100%)
- [x] Coverage >= 80%
- [x] mypy clean
- [x] ruff clean
- [x] CLI module documented
- [x] Manual smoke test: complete meeting via CLI

---

## Phase 9: Streamlit UI

- [x] **9.1** Create `src/ui/__init__.py`
- [x] **9.2** Create `src/ui/app.py` - main Streamlit entry:
  - Session state initialization
  - Page routing (Timer / Analytics)
  - Team selection sidebar
- [x] **9.3** Create `src/ui/components/timer_display.py`:
  - Global timer component
  - Speaker timer component (large, prominent)
  - Progress bar with color states
  - Overtime counter
- [x] **9.4** Create `src/ui/components/speaker_queue.py`:
  - Horizontal queue display
  - Status indicators (done, current, pending)
  - Completed times shown
  - Drag-and-drop reorder (streamlit-sortables or similar)
- [x] **9.5** Create `src/ui/components/controls.py`:
  - Pause/Resume button
  - Add time buttons (+30s, +1m)
  - Skip button
  - Mark absent dropdown
  - End meeting button
- [x] **9.6** Create `src/ui/components/analytics.py`:
  - Summary cards (avg duration, total meetings, etc.)
  - Duration trend chart (st.line_chart or plotly)
  - Per-person stats table
  - Overtime leaderboard
  - Date range filter
- [x] **9.7** Create `src/ui/styles.py` - CSS customization:
  - Timer colors (green, yellow, red)
  - Flashing animation for overtime
  - Layout tweaks
- [x] **9.8** Implement auto-refresh for timer (st.rerun with sleep)
- [x] **9.9** Handle recovery prompt on startup

### Phase 9 Tests
- [x] **9.T1** Test: UI loads without errors
- [x] **9.T2** Test: Team selection populates from teams directory
- [x] **9.T3** Test: Timer updates in real-time
- [x] **9.T4** Test: Control buttons trigger correct actions
- [x] **9.T5** Test: Speaker queue reflects current state
- [x] **9.T6** Test: Analytics page renders with data
- [x] **9.T7** Test: Empty history shows appropriate message
- [x] **9.T8** Test: Recovery modal appears when needed

### Phase 9 Gate
- [x] All tests pass (100%)
- [x] Coverage >= 80%
- [x] mypy clean
- [x] ruff clean
- [x] UI components documented
- [x] Manual smoke test: complete meeting via Streamlit UI
- [x] Manual smoke test: view analytics dashboard

---

## Phase 10: Entry Points & Integration

- [x] **10.1** Create `main.py` - unified entry point:
  - `--mode ui|cli` flag (default: ui)
  - `--team <team_id>` flag
  - Version info (`--version`)
- [x] **10.2** Create `src/ui/run.py` - Streamlit launcher
- [x] **10.3** Create `src/cli/run.py` - CLI launcher
- [x] **10.4** Add console_scripts entry in `pyproject.toml`
- [x] **10.5** Create sample `teams/sample_team.json` for testing
- [x] **10.6** Create `README.md` with usage instructions

### Phase 10 Tests (Integration / E2E)
- [x] **10.T1** Test: `python main.py --mode cli` starts CLI
- [x] **10.T2** Test: `python main.py --mode ui` starts Streamlit
- [x] **10.T3** Test: Full meeting E2E in CLI (start → all speakers → end)
- [x] **10.T4** Test: History file created after CLI meeting
- [x] **10.T5** Test: Recovery works across restart (CLI)
- [x] **10.T6** Test: Multi-team switching works
- [x] **10.T7** Test: Analytics shows data from completed meetings

### Phase 10 Gate (Final Release Gate)
- [x] All tests pass (100%)
- [x] Overall coverage >= 80%
- [x] mypy clean (entire codebase)
- [x] ruff clean (entire codebase)
- [x] README.md complete with:
  - [x] Installation instructions
  - [x] Usage examples (CLI and UI)
  - [x] Configuration guide
  - [x] Team file format documentation
- [x] SPECIFICATION.md reflects final implementation
- [x] ARCHITECTURE.md reflects final implementation
- [x] Manual E2E test: full meeting in CLI mode
- [x] Manual E2E test: full meeting in UI mode
- [x] Manual E2E test: analytics dashboard with real data

---

## Testing Infrastructure

- [x] **T.1** Create `tests/conftest.py` with shared fixtures:
  - `temp_config` - temporary config file
  - `temp_team_file` - temporary team JSON
  - `temp_history` - temporary history file
  - `mock_timer` - controllable timer for testing
  - `sample_meeting_record` - fixture data
- [x] **T.2** Create `tests/unit/` directory structure
- [x] **T.3** Create `tests/integration/` directory structure
- [x] **T.4** Add pytest configuration in `pyproject.toml`
- [x] **T.5** Add coverage configuration (target: 80%+)
- [x] **T.6** Create `Makefile` or scripts for:
  - `make test` - run all tests
  - `make test-unit` - unit tests only
  - `make test-integration` - integration tests only
  - `make coverage` - generate coverage report
  - `make lint` - run ruff
  - `make typecheck` - run mypy

---

## Summary by Phase

| Phase | Description | Tasks | Tests | Gate Checks |
|-------|-------------|-------|-------|-------------|
| 1 | Project Setup | 7 | 2 | 5 |
| 2 | Data Models | 3 | 5 | 5 |
| 3 | Data Layer | 4 | 11 | 5 |
| 4 | Timer Engine | 3 | 10 | 5 |
| 5 | State Manager | 5 | 8 | 5 |
| 6 | Meeting Manager | 5 | 14 | 6 |
| 7 | Analytics | 1 | 7 | 5 |
| 8 | CLI Interface | 6 | 8 | 6 |
| 9 | Streamlit UI | 9 | 8 | 7 |
| 10 | Integration | 6 | 7 | 12 |
| Infra | Test Setup | 6 | - | - |
| **Total** | | **55** | **80** | **61** |

**Grand Total: 196 checkboxes**

---

## Suggested Implementation Order

1. **Phase 1** → Foundation (can't build without this)
2. **Phase 2** → Models (everything depends on data structures)
3. **Phase 4** → Timer Engine (core component, testable in isolation)
4. **Phase 3** → Data Layer (needs models, enables persistence)
5. **Phase 5** → State Manager (needs timer, manages flow)
6. **Phase 6** → Meeting Manager (orchestrates everything)
7. **Phase 8** → CLI (faster to test than UI)
8. **Phase 7** → Analytics (needs history data)
9. **Phase 9** → Streamlit UI (polish)
10. **Phase 10** → Integration & polish

---

## Definition of Done

### Per Task
Each task is complete when:
1. Code is written and follows project conventions
2. Associated tests pass
3. No type errors (mypy clean)
4. No lint errors (ruff clean)
5. Docstrings added for public APIs

### Per Phase (Gate Criteria)
A phase is complete when:
1. All tasks in the phase are done
2. All phase tests pass (100%)
3. Code coverage >= 80% for phase code
4. `mypy src/` returns 0 errors
5. `ruff check src/ tests/` returns 0 errors
6. Documentation updated (README, docstrings, spec/arch if needed)
7. Manual smoke test passed (where applicable)

**DO NOT proceed to next phase until all gate criteria are met.**
