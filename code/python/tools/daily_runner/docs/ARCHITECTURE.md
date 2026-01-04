# Daily Standup Timer - Architecture Document

**Version:** 1.0
**Date:** 2026-01-04
**Author:** Yosi Izaq / Claude

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION LAYER                                 │
├─────────────────────────────────┬───────────────────────────────────────────┤
│                                 │                                           │
│   ┌─────────────────────────┐   │   ┌─────────────────────────────────┐     │
│   │     Streamlit UI        │   │   │        CLI Interface            │     │
│   │                         │   │   │                                 │     │
│   │  - Timer display        │   │   │  - Rich terminal UI             │     │
│   │  - Speaker queue        │   │   │  - Keyboard commands            │     │
│   │  - Control buttons      │   │   │  - Progress bars                │     │
│   │  - Analytics dashboard  │   │   │  - Color-coded output           │     │
│   │                         │   │   │                                 │     │
│   └───────────┬─────────────┘   │   └───────────────┬─────────────────┘     │
│               │                 │                   │                       │
└───────────────┼─────────────────┼───────────────────┼───────────────────────┘
                │                 │                   │
                └────────────────┬┴───────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           APPLICATION LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────────────┐   │
│   │  MeetingManager │   │   TimerEngine   │   │   AnalyticsService      │   │
│   │                 │   │                 │   │                         │   │
│   │ - start()       │   │ - tick()        │   │ - calculate_averages()  │   │
│   │ - pause()       │   │ - reset()       │   │ - get_trends()          │   │
│   │ - skip()        │   │ - add_time()    │   │ - get_overtime_stats()  │   │
│   │ - reorder()     │   │ - get_elapsed() │   │ - filter_by_date()      │   │
│   │ - end()         │   │ - get_remaining│   │                         │   │
│   └────────┬────────┘   └────────┬────────┘   └────────────┬────────────┘   │
│            │                     │                         │                │
│            └─────────────────────┼─────────────────────────┘                │
│                                  │                                          │
│                                  ▼                                          │
│                    ┌─────────────────────────┐                              │
│                    │      StateManager       │                              │
│                    │                         │                              │
│                    │  - current_state        │                              │
│                    │  - speaker_queue        │                              │
│                    │  - elapsed_times        │                              │
│                    │  - notify_observers()   │                              │
│                    └────────────┬────────────┘                              │
│                                 │                                           │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────────────┐   │
│   │  ConfigManager  │   │  TeamRepository │   │    HistoryRepository   │   │
│   │                 │   │                 │   │                         │   │
│   │ - load()        │   │ - get_members() │   │ - save_entry()          │   │
│   │ - save()        │   │ - get_active()  │   │ - get_entries()         │   │
│   │ - get_defaults()│   │ - update()      │   │ - enforce_limit()       │   │
│   └────────┬────────┘   └────────┬────────┘   └────────────┬────────────┘   │
│            │                     │                         │                │
│            ▼                     ▼                         ▼                │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                         File System                                  │   │
│   │                                                                      │   │
│   │  config.json    team_members.json    history.json    .session_*     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Project Structure

```
daily_runner/
├── docs/
│   ├── SPECIFICATION.md
│   └── ARCHITECTURE.md
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/                      # Core business logic
│   │   ├── __init__.py
│   │   ├── meeting_manager.py     # Meeting orchestration
│   │   ├── timer_engine.py        # Timer logic & accuracy
│   │   ├── state_manager.py       # State machine implementation
│   │   └── models.py              # Pydantic data models
│   │
│   ├── data/                      # Data access layer
│   │   ├── __init__.py
│   │   ├── config_manager.py      # Configuration handling
│   │   ├── team_repository.py     # Team member operations
│   │   ├── history_repository.py  # History CRUD & limits
│   │   └── recovery_manager.py    # Session recovery logic
│   │
│   ├── services/                  # Business services
│   │   ├── __init__.py
│   │   └── analytics_service.py   # Statistics & trends
│   │
│   ├── ui/                        # Streamlit interface
│   │   ├── __init__.py
│   │   ├── app.py                 # Main Streamlit entry
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── timer_display.py   # Timer widget
│   │   │   ├── speaker_queue.py   # Queue display & reorder
│   │   │   ├── controls.py        # Action buttons
│   │   │   └── analytics.py       # Dashboard components
│   │   └── styles.py              # CSS & theming
│   │
│   └── cli/                       # CLI interface
│       ├── __init__.py
│       ├── app.py                 # Main CLI entry
│       ├── display.py             # Terminal rendering
│       └── commands.py            # Command handlers
│
├── teams/                         # Team configuration files
│   └── sample_team.json           # Example team (copy to create your own)
│
├── data/                          # Generated data files (gitignored)
│   ├── history_<team_id>.json     # Per-team history
│   └── .session_recovery.json     # Recovery file (generated)
│
├── config.json                    # Application configuration
│
├── main.py                        # Entry point with mode selection
├── pyproject.toml                 # Project metadata & tool config
├── README.md
│
└── docs/
    ├── SPECIFICATION.md           # Requirements & user stories
    ├── ARCHITECTURE.md            # This document
    ├── IMPLEMENTATION_TODO.md     # Implementation checklist
    └── SDD.md                     # Software Design Document
```

---

## 3. Component Details

### 3.1 Core Layer

#### TimerEngine (`src/core/timer_engine.py`)

**Responsibility:** Accurate time tracking with minimal drift.

```python
class TimerEngine:
    """
    High-precision timer using monotonic clock.
    Handles pause/resume without drift accumulation.
    """

    def __init__(self, duration_seconds: int):
        self.duration = duration_seconds
        self._start_time: float | None = None
        self._pause_time: float | None = None
        self._paused_duration: float = 0
        self._is_running: bool = False

    def start(self) -> None: ...
    def pause(self) -> None: ...
    def resume(self) -> None: ...
    def reset(self) -> None: ...
    def add_time(self, seconds: int) -> None: ...

    @property
    def elapsed_seconds(self) -> float: ...

    @property
    def remaining_seconds(self) -> float: ...

    @property
    def is_overtime(self) -> bool: ...

    @property
    def overtime_seconds(self) -> float: ...
```

**Key Implementation Details:**
- Uses `time.monotonic()` for drift-resistant timing
- Tracks paused duration separately to maintain accuracy
- Thread-safe for potential future async usage

---

#### StateManager (`src/core/state_manager.py`)

**Responsibility:** Manage meeting state transitions and notify observers.

```python
from enum import Enum, auto
from typing import Callable, List

class MeetingState(Enum):
    IDLE = auto()
    TRANSITION = auto()
    SPEAKING = auto()
    PAUSED = auto()
    GRACE = auto()
    COMPLETED = auto()

class StateManager:
    """
    State machine for meeting flow.
    Uses observer pattern for UI updates.
    """

    def __init__(self):
        self._state: MeetingState = MeetingState.IDLE
        self._observers: List[Callable] = []
        self._speaker_queue: List[str] = []
        self._current_speaker_index: int = 0
        self._speaker_times: dict[str, float] = {}

    def transition_to(self, new_state: MeetingState) -> bool:
        """Validate and perform state transition."""
        ...

    def add_observer(self, callback: Callable) -> None: ...
    def notify_observers(self) -> None: ...

    @property
    def current_speaker(self) -> str | None: ...

    @property
    def remaining_speakers(self) -> List[str]: ...
```

**State Transition Matrix:**

| From \ To | IDLE | TRANSITION | SPEAKING | PAUSED | GRACE | COMPLETED |
|-----------|------|------------|----------|--------|-------|-----------|
| IDLE | - | Y | - | - | - | - |
| TRANSITION | - | - | Y | Y | - | Y |
| SPEAKING | - | - | - | Y | Y | - |
| PAUSED | - | - | Y | - | - | - |
| GRACE | - | Y | - | Y | - | Y |
| COMPLETED | Y | - | - | - | - | - |

---

#### MeetingManager (`src/core/meeting_manager.py`)

**Responsibility:** High-level meeting orchestration.

```python
class MeetingManager:
    """
    Orchestrates meeting flow using TimerEngine and StateManager.
    Provides simplified API for UI layers.
    """

    def __init__(
        self,
        team_repo: TeamRepository,
        config: ConfigManager,
        history_repo: HistoryRepository,
        recovery_manager: RecoveryManager
    ):
        self.state_manager = StateManager()
        self.global_timer = TimerEngine(duration_seconds=0)  # Count-up
        self.speaker_timer: TimerEngine | None = None
        ...

    # Meeting lifecycle
    def start_meeting(self, speaker_order: List[str] | None = None) -> None: ...
    def end_meeting(self, save_history: bool = True) -> None: ...

    # Speaker controls
    def next_speaker(self) -> None: ...
    def skip_speaker(self) -> None: ...
    def mark_absent(self, member_id: str) -> None: ...

    # Timer controls
    def pause(self) -> None: ...
    def resume(self) -> None: ...
    def add_time(self, seconds: int) -> None: ...

    # Order management
    def reorder_speakers(self, new_order: List[str]) -> None: ...

    # Recovery
    def check_recovery(self) -> bool: ...
    def restore_session(self) -> None: ...
    def discard_recovery(self) -> None: ...
```

---

### 3.2 Data Layer

#### Models (`src/core/models.py`)

**Using Pydantic for validation and serialization:**

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class ParticipantStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    SKIPPED = "skipped"

class DailyConfig(BaseModel):
    default_time_seconds: int = 180
    active: bool = True

class TeamMember(BaseModel):
    id: str
    name: str
    display_name: str
    email: str
    github: Optional[str] = None
    role: Optional[str] = None
    specialization: List[str] = Field(default_factory=list)
    daily_config: DailyConfig = Field(default_factory=DailyConfig)

class ParticipantRecord(BaseModel):
    member_id: str
    display_name: str
    status: ParticipantStatus
    allocated_time_seconds: int
    actual_time_seconds: float
    overtime_seconds: float = 0
    order_position: Optional[int] = None

class MeetingRecord(BaseModel):
    id: str
    date: str
    start_time: str
    end_time: str
    total_duration_seconds: float
    expected_duration_seconds: int
    status: str
    participants: List[ParticipantRecord]
    notes: str = ""

class AppConfig(BaseModel):
    version: str = "1.0"
    timer: TimerConfig
    alerts: AlertConfig
    history: HistoryConfig
    recovery: RecoveryConfig
    ui: UIConfig
    default_order: str = "alphabetical"
```

---

#### HistoryRepository (`src/data/history_repository.py`)

**Responsibility:** CRUD operations with 2000 entry limit.

```python
class HistoryRepository:
    MAX_ENTRIES = 2000

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._history: List[MeetingRecord] = []
        self._load()

    def _load(self) -> None:
        """Load history from file, handle corruption gracefully."""
        ...

    def save_entry(self, record: MeetingRecord) -> None:
        """
        Add entry, enforce FIFO limit, persist to disk.
        """
        self._history.append(record)
        if len(self._history) > self.MAX_ENTRIES:
            self._history = self._history[-self.MAX_ENTRIES:]
        self._persist()

    def get_entries(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int | None = None
    ) -> List[MeetingRecord]:
        """Query history with optional filters."""
        ...

    def _persist(self) -> None:
        """Atomic write with backup."""
        ...
```

---

### 3.3 Services Layer

#### AnalyticsService (`src/services/analytics_service.py`)

```python
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class MeetingStats:
    average_duration: float
    total_meetings: int
    on_time_rate: float
    overtime_leader: str

@dataclass
class PersonStats:
    member_id: str
    display_name: str
    average_time: float
    overtime_percentage: float
    attendance_rate: float
    trend: str  # "up", "down", "stable"

class AnalyticsService:
    def __init__(self, history_repo: HistoryRepository):
        self.history = history_repo

    def get_summary_stats(
        self,
        days: int = 30
    ) -> MeetingStats: ...

    def get_per_person_stats(
        self,
        days: int = 30
    ) -> List[PersonStats]: ...

    def get_duration_trend(
        self,
        days: int = 30
    ) -> List[Dict[str, float]]: ...

    def get_overtime_leaderboard(
        self,
        limit: int = 5
    ) -> List[tuple[str, float]]: ...
```

---

## 4. Data Flow

### 4.1 Starting a Meeting

```
User clicks "Start Meeting"
         │
         ▼
┌─────────────────────────┐
│   UI Layer (Streamlit)  │
│   or CLI Layer          │
└───────────┬─────────────┘
            │ meeting_manager.start_meeting()
            ▼
┌─────────────────────────┐
│    MeetingManager       │
│                         │
│ 1. Check for recovery   │
│ 2. Load team members    │
│ 3. Sort by order        │
│ 4. Initialize timers    │
│ 5. Start global timer   │
│ 6. Transition to first  │
└───────────┬─────────────┘
            │
            ├──► StateManager.transition_to(TRANSITION)
            │
            ├──► Global TimerEngine.start()
            │
            ├──► RecoveryManager.start_auto_save()
            │
            ▼
┌─────────────────────────┐
│    StateManager         │
│                         │
│ notify_observers()      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   UI Updates            │
│   - Show timer          │
│   - Show queue          │
│   - Enable controls     │
└─────────────────────────┘
```

### 4.2 Timer Tick (Every 100ms)

```
┌─────────────────────────┐
│   TimerEngine.tick()    │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Calculate remaining   │
│   time using monotonic  │
│   clock                 │
└───────────┬─────────────┘
            │
            ├─── remaining > 30s ──► Normal state (green)
            │
            ├─── remaining <= 30s ──► Warning state (yellow)
            │
            ├─── remaining <= 0s ──► StateManager → GRACE
            │
            └─── grace expired ──► MeetingManager.next_speaker()
```

### 4.3 Saving History

```
MeetingManager.end_meeting()
         │
         ▼
┌─────────────────────────┐
│  Collect all speaker    │
│  times from StateManager│
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Build MeetingRecord    │
│  with all participants  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  HistoryRepository      │
│  .save_entry()          │
│                         │
│  1. Append to list      │
│  2. Check > 2000?       │
│  3. Trim oldest if yes  │
│  4. Atomic write        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  RecoveryManager        │
│  .clear_session()       │
└─────────────────────────┘
```

---

## 5. Technology Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| Language | Python 3.10+ | Team familiarity, rapid development |
| UI Framework | Streamlit 1.29+ | Quick prototyping, built-in widgets |
| CLI Framework | Rich | Beautiful terminal UI, progress bars |
| Data Validation | Pydantic 2.x | Type safety, JSON serialization |
| Time Handling | `time.monotonic()` | Drift-resistant, not affected by system clock |
| File Locking | `filelock` | Safe concurrent access |
| Testing | pytest + pytest-asyncio | Standard Python testing |
| Linting | ruff | Fast, comprehensive linting |
| Type Checking | mypy | Static type verification |

---

## 6. Key Design Decisions

### 6.1 Why Separate TimerEngine from StateManager?

**Single Responsibility**: TimerEngine handles only time calculation with precision. StateManager handles only state transitions and observer notifications. This separation allows:
- Independent testing of timing accuracy
- Easier reasoning about state machine logic
- Potential future reuse of timer in other contexts

### 6.2 Why Observer Pattern for UI Updates?

Both Streamlit and CLI need to react to state changes. Observer pattern allows:
- Loose coupling between core logic and UI
- Easy addition of new UI modes (web, mobile)
- Centralized state change handling

### 6.3 Why Pydantic for Models?

- Automatic JSON serialization/deserialization
- Runtime validation catches data errors early
- IDE autocompletion and type hints
- Easy schema evolution with defaults

### 6.4 Why Atomic File Writes?

History and config files are critical. Atomic writes prevent corruption:
```python
def _persist(self):
    temp_path = self.file_path.with_suffix('.tmp')
    temp_path.write_text(json.dumps(self._data, indent=2))
    temp_path.replace(self.file_path)  # Atomic on POSIX
```

---

## 7. Session Recovery Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                      Application Startup                         │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Check for             │
                    │ .session_recovery.json│
                    └───────────┬───────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
            File exists?              No file
                    │                       │
                    ▼                       ▼
            ┌───────────────┐        Normal startup
            │ Parse & validate│
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────────────────────────────────┐
            │ Show Dialog:                               │
            │ "Previous session found (09:05 today)     │
            │  Chen, Miri completed. Muhe was speaking. │
            │                                           │
            │  [Resume Session]    [Discard & Start New]│
            └───────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
    Resume                  Discard
        │                       │
        ▼                       ▼
    Restore state         Delete recovery file
    Continue meeting      Start fresh
```

**Recovery Data Captured:**
- Session start timestamp
- Global elapsed time
- Current speaker index
- Completed speakers with their times
- Current speaker's elapsed time
- Absent members list
- In-transition flag

---

## 8. Error Handling Strategy

### 8.1 File Operations

```python
class FileOperationError(Exception):
    """Base exception for file operations."""
    pass

class HistoryCorruptedError(FileOperationError):
    """History file is corrupted."""
    pass

def load_history_safe(path: Path) -> List[MeetingRecord]:
    """
    Load history with corruption recovery.
    """
    try:
        data = json.loads(path.read_text())
        return [MeetingRecord(**entry) for entry in data["entries"]]
    except json.JSONDecodeError:
        # Backup corrupted file
        backup_path = path.with_suffix(f'.corrupted.{datetime.now():%Y%m%d%H%M%S}')
        path.rename(backup_path)
        logger.warning(f"Corrupted history backed up to {backup_path}")
        return []
    except ValidationError as e:
        logger.error(f"History validation failed: {e}")
        # Attempt partial recovery...
```

### 8.2 Graceful Degradation

| Failure | Degraded Behavior |
|---------|-------------------|
| Config missing | Use hardcoded defaults |
| Team file missing | Prompt for manual entry |
| History corrupted | Start fresh, backup old |
| Recovery corrupted | Discard, start fresh |
| Analytics fail | Show "Data unavailable" |

---

## 9. Testing Strategy

### 9.1 Unit Tests

```
tests/
├── unit/
│   ├── test_timer_engine.py     # Time accuracy, pause/resume
│   ├── test_state_manager.py    # State transitions, edge cases
│   ├── test_models.py           # Pydantic validation
│   └── test_history_repo.py     # FIFO limit, atomic writes
```

### 9.2 Integration Tests

```
tests/
├── integration/
│   ├── test_meeting_flow.py     # Full meeting lifecycle
│   ├── test_recovery.py         # Crash recovery scenarios
│   └── test_analytics.py        # Stats calculation
```

### 9.3 Key Test Cases

**TimerEngine:**
- Timer accuracy over 5 minutes (< 100ms drift)
- Pause/resume maintains accuracy
- Add time extends correctly
- Overtime calculation correct

**StateManager:**
- All valid transitions succeed
- Invalid transitions raise exceptions
- Observers notified on every transition

**HistoryRepository:**
- Exactly 2000 entries maintained
- Oldest removed when limit exceeded
- Survives process crash mid-write

---

## 10. Future Considerations

### 10.1 Potential Enhancements (Not in MVP)

| Feature | Complexity | Notes |
|---------|------------|-------|
| Slack integration | Medium | Post summary to channel |
| Audio alerts | Low | Platform-specific sound playback |
| Team sync (multi-device) | High | Would need server component |
| Voice recognition | High | Auto-detect speaker changes |
| Calendar integration | Medium | Auto-start at scheduled time |

### 10.2 Scalability Notes

Current design supports:
- Teams up to ~50 members (UI becomes crowded beyond this)
- History of 2000 meetings (~4 years of daily standups)
- Analytics across full history in < 1 second

If larger scale needed:
- SQLite instead of JSON for history
- Pagination for analytics
- Background processing for stats

---

## 11. Dependencies

**requirements.txt:**

```
# Core
pydantic>=2.0.0
python-dateutil>=2.8.0

# UI
streamlit>=1.29.0

# CLI
rich>=13.0.0

# File safety
filelock>=3.12.0

# Dev
pytest>=7.0.0
pytest-cov>=4.0.0
mypy>=1.0.0
ruff>=0.1.0
```

---

## 12. Configuration Example

**config.json:**

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

---

## 13. Running the Application

### Quick Start

```bash
# Install dependencies
pip install -e ".[dev]"

# Run Streamlit UI (default)
python main.py

# Run CLI mode
python main.py --mode cli

# View meeting history
python main.py --mode history

# Specify team directly
python main.py --team sample_team

# Using installed command (after pip install)
daily-timer --team sample_team
```

### Available Commands

| Command | Description |
|---------|-------------|
| `python main.py` | Start Streamlit web UI (default) |
| `python main.py --mode cli` | Start CLI terminal mode |
| `python main.py --mode history` | View meeting history |
| `python main.py --team <id>` | Skip team selection |
| `python main.py --days N` | History: days to look back (default: 30) |
| `python main.py --limit N` | History: max entries to show (default: 20) |
| `python main.py -v` | Enable verbose logging |
| `daily-timer` | Installed CLI command |

### Development Commands

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=term-missing

# Type checking
mypy src/

# Linting
ruff check src/ tests/
```
