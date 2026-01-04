# Software Design Document (SDD)
## Daily Standup Timer Application

**Version:** 1.0.0
**Last Updated:** January 2026
**Target Audience:** Developers onboarding to this codebase

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Python Tooling & Development Setup](#2-python-tooling--development-setup)
3. [Dependencies & Libraries](#3-dependencies--libraries)
4. [Project Structure](#4-project-structure)
5. [Architecture Overview](#5-architecture-overview)
6. [Core Module Design](#6-core-module-design)
7. [Data Layer Design](#7-data-layer-design)
8. [Service Layer](#8-service-layer)
9. [UI Layer](#9-ui-layer)
10. [Design Patterns](#10-design-patterns)
11. [Python Idioms & Best Practices](#11-python-idioms--best-practices)
12. [Testing Strategy](#12-testing-strategy)
13. [Configuration Reference](#13-configuration-reference)

---

## 1. Project Overview

### Purpose
A Python application for managing daily standup meetings with per-developer timers, visual alerts, meeting history tracking, and analytics.

### Key Features
- Per-developer configurable timers (default: 3 minutes)
- Visual warnings and overtime alerts
- Dual interface: Rich CLI and Streamlit web UI
- Meeting history with FIFO storage limits
- Session recovery for crash resilience
- Multi-team support with separate configurations
- Analytics dashboard with trends and statistics

### System Requirements
- Python 3.10+ (uses union type syntax `X | Y`, `match` statements)
- macOS or Linux (tested platforms)

---

## 2. Python Tooling & Development Setup

### 2.1 Package Management (pyproject.toml)

The project uses **PEP 517/518** build system with `setuptools`:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"
```

**Key sections explained:**

```toml
[project]
name = "daily-standup-timer"
version = "1.0.0"
requires-python = ">=3.10"  # Minimum Python version
dependencies = [...]         # Runtime dependencies
```

**Entry point** (creates `daily-timer` CLI command):
```toml
[project.scripts]
daily-timer = "src.cli.app:main"
```

### 2.2 Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install with dev dependencies
pip install -e ".[dev]"
```

The `-e` flag enables **editable mode** - changes to source code take effect without reinstalling.

### 2.3 Type Checking (mypy)

Configuration in `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.10"
strict = true                    # Enable all strict checks
disallow_untyped_defs = true     # All functions must have type hints
plugins = ["pydantic.mypy"]      # Enable Pydantic type checking
```

**Run type checking:**
```bash
mypy src/
```

**Key mypy features used:**
- `strict = true`: Maximum type safety
- Pydantic plugin: Validates model field types at compile time
- Override ignores for external libs without stubs (streamlit, rich)

### 2.4 Linting (ruff)

Ruff replaces flake8, isort, and pyupgrade in a single fast tool:

```toml
[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes (undefined names, etc.)
    "I",      # isort (import sorting)
    "B",      # flake8-bugbear (common bugs)
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade (modern Python syntax)
    "ARG",    # unused arguments
    "SIM",    # simplify code suggestions
]
```

**Run linting:**
```bash
ruff check src/ tests/
ruff check --fix src/  # Auto-fix issues
```

### 2.5 Testing (pytest)

Configuration:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["-v", "--tb=short", "--strict-markers"]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow tests",
]

[tool.coverage.run]
source = ["src"]
branch = true           # Track branch coverage
fail_under = 80         # CI fails below 80% coverage
```

**Run tests:**
```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=term-missing

# Specific test file
pytest tests/unit/test_models.py

# By marker
pytest -m unit
```

---

## 3. Dependencies & Libraries

### 3.1 Runtime Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| **pydantic** | >=2.0 | Data validation, serialization, settings management |
| **python-dateutil** | >=2.8 | Date/time parsing and manipulation |
| **streamlit** | >=1.29 | Web UI framework |
| **rich** | >=13.0 | Terminal formatting, tables, progress bars |
| **filelock** | >=3.12 | Cross-platform file locking for concurrent access |

### 3.2 Development Dependencies

| Library | Purpose |
|---------|---------|
| **pytest** | Test framework |
| **pytest-cov** | Coverage reporting |
| **pytest-asyncio** | Async test support |
| **mypy** | Static type checking |
| **ruff** | Linting and formatting |

### 3.3 Library Deep Dive

#### Pydantic v2

Used for **all data models** with strict validation:

```python
from pydantic import BaseModel, Field, field_validator

class TeamMember(BaseModel):
    model_config = ConfigDict(strict=True)  # No type coercion

    id: str = Field(
        ...,                           # Required field
        min_length=1,
        max_length=50,
        pattern=r"^[a-z][a-z0-9_]*$",  # Regex validation
    )
    email: EmailStr                    # Built-in email validation
    daily_config: DailyConfig = Field(
        default_factory=DailyConfig,   # Mutable default
    )
```

**Key Pydantic patterns:**
- `model_config = ConfigDict(strict=True)` - No automatic type coercion
- `Field(...)` - Required field marker
- `Field(default_factory=...)` - Safe mutable defaults
- `model_validate(data)` - Parse dict to model
- `model_dump(mode="json")` - Serialize to JSON-safe dict

#### Rich Library

Used for CLI terminal output:

```python
from rich.console import Console
from rich.live import Live
from rich.table import Table

console = Console()

# Live updating display (used for timer)
with Live(renderable, refresh_per_second=10) as live:
    while running:
        live.update(new_renderable)
```

#### filelock

Ensures atomic file operations:

```python
from filelock import FileLock

lock_path = file_path.with_suffix(".lock")
with FileLock(lock_path):
    # Safe to read/write file
    data = file_path.read_text()
```

---

## 4. Project Structure

```
daily_runner/
├── src/
│   ├── __init__.py
│   ├── core/                    # Business logic (no external deps)
│   │   ├── __init__.py
│   │   ├── constants.py         # Magic numbers, color codes
│   │   ├── models.py            # Pydantic data models
│   │   ├── time_utils.py        # Time formatting utilities
│   │   ├── timer_engine.py      # High-precision countdown timer
│   │   ├── state_manager.py     # Meeting state machine
│   │   └── meeting_manager.py   # Main orchestrator
│   │
│   ├── data/                    # Data access layer
│   │   ├── __init__.py
│   │   ├── config_manager.py    # App configuration
│   │   ├── team_repository.py   # Team data access
│   │   ├── history_repository.py # Meeting history storage
│   │   └── recovery_manager.py  # Session crash recovery
│   │
│   ├── services/                # Business services
│   │   ├── __init__.py
│   │   └── analytics_service.py # Meeting analytics
│   │
│   ├── cli/                     # Command-line interface
│   │   ├── __init__.py
│   │   ├── app.py               # CLI entry point & main loop
│   │   ├── commands.py          # Keyboard handler
│   │   └── display.py           # Rich terminal rendering
│   │
│   └── ui/                      # Streamlit web interface
│       ├── __init__.py
│       ├── app.py               # Streamlit entry point
│       └── components/          # Reusable UI components
│           ├── analytics.py
│           ├── controls.py
│           ├── speaker_queue.py
│           └── timer_display.py
│
├── tests/
│   ├── conftest.py              # Shared fixtures
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
│
├── teams/                       # Team JSON files
│   └── imagine_dragons.json
│
├── data/                        # Runtime data (gitignored)
│   ├── history_*.json
│   └── .session_recovery.json
│
├── config.json                  # Application configuration
├── pyproject.toml               # Project metadata & tools config
└── README.md
```

### Layer Rules

1. **Core** - Pure Python, no external dependencies except stdlib
2. **Data** - File I/O, uses Core models
3. **Services** - Business logic, uses Data + Core
4. **CLI/UI** - User interface, uses all layers

**Dependency flow:** `UI/CLI → Services → Data → Core`

---

## 5. Architecture Overview

### 5.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  ┌─────────────────────┐    ┌─────────────────────────┐     │
│  │   CLI (Rich)        │    │   Web UI (Streamlit)    │     │
│  │   - app.py          │    │   - app.py              │     │
│  │   - display.py      │    │   - components/         │     │
│  │   - commands.py     │    │                         │     │
│  └──────────┬──────────┘    └───────────┬─────────────┘     │
└─────────────┼───────────────────────────┼───────────────────┘
              │                           │
              ▼                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      Service Layer                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              AnalyticsService                        │    │
│  │  - Summary stats, trends, per-person breakdowns     │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Core Layer                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                   MeetingManager                        │ │
│  │  - Orchestrates timer, state, recovery                 │ │
│  │  - Coordinates all meeting operations                  │ │
│  └────────────────────────────────────────────────────────┘ │
│         │                    │                    │          │
│         ▼                    ▼                    ▼          │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐ │
│  │ TimerEngine │    │ StateManager │    │     Models      │ │
│  │ - Countdown │    │ - FSM        │    │ - Pydantic      │ │
│  │ - Pause     │    │ - Observer   │    │ - Validation    │ │
│  │ - Overtime  │    │ - Queue      │    │ - Serialization │ │
│  └─────────────┘    └──────────────┘    └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│  ┌───────────────┐ ┌─────────────┐ ┌───────────────────────┐│
│  │ ConfigManager │ │TeamRepository│ │ HistoryRepository    ││
│  │ - Load/Save   │ │- Load teams │ │ - FIFO storage       ││
│  │ - Defaults    │ │- Cache      │ │ - Date filtering     ││
│  └───────────────┘ └─────────────┘ └───────────────────────┘│
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   RecoveryManager                      │  │
│  │  - Auto-save session state                            │  │
│  │  - Crash recovery                                     │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Data Flow

```
User Action → UI Handler → MeetingManager → StateManager
                                         → TimerEngine
                                         → RecoveryManager (auto-save)
                                         → HistoryRepository (on meeting end)
```

---

## 6. Core Module Design

### 6.1 Models (`src/core/models.py`)

All data structures are **Pydantic BaseModel** subclasses:

#### Enum Definitions

```python
class MeetingState(str, Enum):
    """State machine states for meeting flow."""
    IDLE = "idle"           # No meeting active
    TRANSITION = "transition"  # Between speakers
    SPEAKING = "speaking"   # Speaker has the floor
    PAUSED = "paused"       # Meeting paused
    GRACE = "grace"         # Overtime grace period
    COMPLETED = "completed" # Meeting ended
```

**Why `str, Enum`?** - Enables direct JSON serialization without custom encoders.

#### Model Hierarchy

```
AppConfig (root config)
├── TimerConfig
├── AlertConfig
├── HistoryConfig
├── RecoveryConfig
├── UIConfig
└── TeamsConfig

TeamFile (team data)
├── TeamInfo
└── list[TeamMember]
    └── DailyConfig

MeetingRecord (history entry)
└── list[ParticipantRecord]

SessionRecovery (crash recovery state)
└── list[CompletedSpeakerRecord]
```

### 6.2 Timer Engine (`src/core/timer_engine.py`)

**High-precision countdown timer using `time.monotonic()`**

```python
class TimerEngine:
    """Uses monotonic clock for drift-resistant timing."""

    def __init__(self, duration_seconds: int) -> None:
        self._duration = float(duration_seconds)
        self._state = TimerState.IDLE
        self._start_time: float | None = None
        self._accumulated_elapsed: float = 0.0

    @property
    def elapsed_seconds(self) -> float:
        """Total elapsed, accounting for pauses."""
        if self._state == TimerState.RUNNING:
            return self._accumulated_elapsed + (time.monotonic() - self._start_time)
        return self._accumulated_elapsed

    @property
    def remaining_seconds(self) -> float:
        """Returns negative when in overtime."""
        return self._duration - self.elapsed_seconds
```

**Why `time.monotonic()`?**
- Not affected by system clock changes
- Guaranteed to never go backwards
- Perfect for measuring elapsed intervals

### 6.3 State Manager (`src/core/state_manager.py`)

**Finite State Machine with Observer pattern:**

```python
# Valid state transitions matrix
VALID_TRANSITIONS: dict[MeetingState, set[MeetingState]] = {
    MeetingState.IDLE: {MeetingState.TRANSITION, MeetingState.SPEAKING},
    MeetingState.TRANSITION: {MeetingState.SPEAKING, MeetingState.PAUSED, MeetingState.COMPLETED},
    MeetingState.SPEAKING: {MeetingState.PAUSED, MeetingState.GRACE, MeetingState.TRANSITION, MeetingState.COMPLETED},
    MeetingState.PAUSED: {MeetingState.SPEAKING, MeetingState.TRANSITION, MeetingState.COMPLETED},
    MeetingState.GRACE: {MeetingState.SPEAKING, MeetingState.PAUSED, MeetingState.TRANSITION, MeetingState.COMPLETED},
    MeetingState.COMPLETED: set(),  # Terminal state
}

class StateManager:
    def transition_to(self, new_state: MeetingState) -> None:
        """Validates transition before changing state."""
        if not self.is_valid_transition(new_state):
            raise InvalidStateTransitionError(...)

        old_state = self._state
        self._state = new_state
        self._notify_observers(old_state, new_state)
```

### 6.4 Meeting Manager (`src/core/meeting_manager.py`)

**Central orchestrator using Dependency Injection:**

```python
class MeetingManager:
    def __init__(
        self,
        team_repo: TeamRepository,      # Injected
        config: AppConfig,              # Injected
        history_repo: HistoryRepository, # Injected
        recovery_mgr: RecoveryManager,   # Injected
    ) -> None:
        # Core components (created internally)
        self._state_manager = StateManager()
        self._speaker_timer: TimerEngine | None = None
```

**Key responsibilities:**
- Meeting lifecycle (start, end, pause, resume)
- Speaker queue management
- Timer coordination
- Event notification to observers
- Recovery state generation

### 6.5 Constants (`src/core/constants.py`)

**Centralized magic numbers:**

```python
# Time defaults
DEFAULT_SPEAKER_TIME_SECONDS = 180  # 3 minutes
DEFAULT_WARNING_THRESHOLD_SECONDS = 30
TIME_INCREMENT_SECONDS = 30  # +/- buttons

# Color scheme
COLORS = {
    "normal": "#00ff00",    # Green
    "warning": "#ffff00",   # Yellow
    "overtime": "#ff0000",  # Red
    "paused": "#0066ff",    # Blue
}
```

---

## 7. Data Layer Design

### 7.1 Repository Pattern

All data access follows the **Repository Pattern**:

```python
class HistoryRepository:
    """Abstracts file storage details from business logic."""

    def __init__(self, team_id: str, data_dir: Path, max_entries: int):
        self._file_path = data_dir / f"history_{team_id}.json"
        self._lock_path = self._file_path.with_suffix(".lock")

    def save_entry(self, record: MeetingRecord) -> None:
        """Atomic save with FIFO limit enforcement."""
        with FileLock(self._lock_path):
            # Temp file + atomic rename pattern
            temp_path.write_text(json.dumps(data))
            temp_path.replace(self._file_path)
```

### 7.2 Atomic File Operations

All repositories use the same safe write pattern:

```python
def _save(self) -> None:
    temp_path = self._file_path.with_suffix(".tmp")
    try:
        with FileLock(self._lock_path):
            temp_path.write_text(json.dumps(data))
            temp_path.replace(self._file_path)  # Atomic on POSIX
    except Exception:
        temp_path.unlink(missing_ok=True)  # Cleanup
        raise
```

### 7.3 Lazy Loading with Caching

```python
class TeamRepository:
    def __init__(self):
        self._cache: dict[str, TeamFile] = {}

    def load_team(self, team_id: str, use_cache: bool = True) -> TeamFile:
        if use_cache and team_id in self._cache:
            return self._cache[team_id]

        team = TeamFile.model_validate(json.loads(...))
        self._cache[team_id] = team
        return team
```

---

## 8. Service Layer

### 8.1 Analytics Service (`src/services/analytics_service.py`)

**Stateless service with repository dependency:**

```python
class AnalyticsService:
    def __init__(self, history_repo: HistoryRepository) -> None:
        self._history_repo = history_repo

    def get_summary_stats(self, days: int = 30) -> SummaryStats:
        entries = self._get_filtered_entries(days)
        return SummaryStats(
            total_meetings=len(entries),
            avg_duration_seconds=total_duration / len(entries),
            on_time_rate=on_time_count / len(entries),
        )
```

**Return types use dataclasses for simple DTOs:**

```python
@dataclass
class SummaryStats:
    total_meetings: int = 0
    avg_duration_seconds: float = 0.0
    on_time_rate: float = 0.0
```

**Why dataclass vs Pydantic here?**
- Read-only output DTOs, no validation needed
- Slightly lighter weight
- Clear separation: Pydantic for I/O, dataclass for internal DTOs

---

## 9. UI Layer

### 9.1 CLI Application (`src/cli/app.py`)

**Event loop architecture:**

```python
class CLIApp:
    def _main_loop(self) -> int:
        with Live(self._render_display(), refresh_per_second=10) as live:
            while self._running and self._meeting_manager.is_active:
                # Non-blocking input check
                result = self._keyboard.process_input(timeout=0.1)
                if result:
                    self._handle_command(result.command)

                # State-based logic
                if state == MeetingState.TRANSITION:
                    if transition_remaining <= 0:
                        self._meeting_manager.start_speaking()

                # Update display
                live.update(self._render_display())
```

**Key patterns:**
- `Rich Live` for real-time display updates
- Non-blocking keyboard input with timeout
- Command pattern for input handling

### 9.2 Streamlit UI (`src/ui/`)

**Component-based architecture:**

```python
# src/ui/app.py
def main():
    st.set_page_config(page_title="Daily Timer")

    # Session state initialization
    if "manager" not in st.session_state:
        st.session_state.manager = create_manager()

    # Render components
    render_timer(st.session_state.manager)
    render_controls(st.session_state.manager)
    render_speaker_queue(st.session_state.manager)
```

**Streamlit session state** - persists across reruns:
```python
st.session_state.manager  # MeetingManager instance
st.session_state.team_id  # Current team
```

---

## 10. Design Patterns

### 10.1 Patterns Used

| Pattern | Location | Purpose |
|---------|----------|---------|
| **Repository** | `data/*_repository.py` | Abstract data storage |
| **Observer** | `StateManager`, `MeetingManager` | Notify on state changes |
| **State Machine** | `StateManager` | Valid state transitions |
| **Dependency Injection** | `MeetingManager.__init__` | Testability, flexibility |
| **Factory Method** | `AppConfig.create_default()` | Default object creation |
| **Command** | `cli/commands.py` | Encapsulate user actions |

### 10.2 Observer Pattern Example

```python
# Type alias for callbacks
StateObserver = Callable[[MeetingState, MeetingState], None]

class StateManager:
    def __init__(self):
        self._observers: list[StateObserver] = []

    def add_observer(self, callback: StateObserver) -> None:
        if callback not in self._observers:
            self._observers.append(callback)

    def _notify_observers(self, old: MeetingState, new: MeetingState) -> None:
        for observer in self._observers:
            try:
                observer(old, new)
            except Exception as e:
                logger.error(f"Observer error: {e}")
```

### 10.3 Dependency Injection Example

```python
# Production usage
def create_production_manager() -> MeetingManager:
    config_mgr = ConfigManager()
    config = config_mgr.load()

    return MeetingManager(
        team_repo=TeamRepository(Path("teams")),
        config=config,
        history_repo=HistoryRepository(team_id, Path("data")),
        recovery_mgr=RecoveryManager(Path("data/.recovery.json")),
    )

# Test usage with mocks
def test_meeting_manager():
    manager = MeetingManager(
        team_repo=MockTeamRepository(),
        config=test_config,
        history_repo=MockHistoryRepository(),
        recovery_mgr=MockRecoveryManager(),
    )
```

---

## 11. Python Idioms & Best Practices

### 11.1 Type Hints (Python 3.10+)

```python
# Union types (3.10+ syntax)
def load(self, path: Path | None = None) -> AppConfig:
    ...

# Generic collections (no need for typing.List)
speakers: list[TeamMember] = []
records: dict[str, SpeakerRecord] = {}

# Optional with default
def get(self, key: str, default: Any = None) -> Any:
    ...
```

### 11.2 Dataclasses vs Pydantic

```python
# Use Pydantic for external data (files, API, user input)
class TeamMember(BaseModel):
    model_config = ConfigDict(strict=True)
    id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")

# Use dataclass for internal DTOs
@dataclass
class SpeakerRecord:
    member: TeamMember
    elapsed_seconds: float = 0.0
```

### 11.3 Context Managers

```python
# File locking
with FileLock(lock_path):
    data = file_path.read_text()

# Keyboard input mode
class KeyboardHandler:
    def __enter__(self) -> Self:
        self._setup_terminal()
        return self

    def __exit__(self, *args) -> None:
        self._restore_terminal()

# Usage
with keyboard_handler:
    # Terminal in raw mode
    ...
# Terminal restored automatically
```

### 11.4 Property Decorators

```python
class TimerEngine:
    @property
    def is_running(self) -> bool:
        """Read-only computed property."""
        return self._state == TimerState.RUNNING

    @property
    def remaining_seconds(self) -> float:
        """Computed value, not stored."""
        return self._duration - self.elapsed_seconds
```

### 11.5 Enum Best Practices

```python
class MeetingState(str, Enum):
    """Inherit from str for JSON serialization."""
    IDLE = "idle"

# Access patterns
state = MeetingState.IDLE
state.value  # "idle" (string)
state.name   # "IDLE" (enum name)
```

### 11.6 Default Argument Gotcha

```python
# WRONG - Mutable default shared between calls
def __init__(self, items: list = []):
    self.items = items

# CORRECT - Factory creates new list each call
def __init__(self, items: list | None = None):
    self.items = items or []

# CORRECT in Pydantic - Use default_factory
class Config(BaseModel):
    items: list[str] = Field(default_factory=list)
```

### 11.7 Path Handling

```python
from pathlib import Path

# Always use Path, not string concatenation
file_path = data_dir / f"history_{team_id}.json"
lock_path = file_path.with_suffix(".lock")
backup_path = file_path.with_suffix(".corrupted.json")

# Check existence
if file_path.exists():
    data = file_path.read_text()

# Create parents
data_dir.mkdir(parents=True, exist_ok=True)
```

---

## 12. Testing Strategy

### 12.1 Test Structure

```
tests/
├── conftest.py          # Shared fixtures
├── unit/
│   ├── test_models.py           # Pydantic models
│   ├── test_timer_engine.py     # Timer logic
│   ├── test_state_manager.py    # State machine
│   ├── test_meeting_manager.py  # Orchestration
│   ├── test_data_layer.py       # Repositories
│   ├── test_analytics_service.py
│   ├── test_cli.py
│   └── test_time_utils.py
└── integration/
```

### 12.2 Fixtures (`conftest.py`)

```python
@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Isolated temporary directory per test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def sample_team_data() -> dict[str, Any]:
    """Reusable test data."""
    return {
        "team": {"name": "Test Team", "emoji": ""},
        "members": [
            {"id": "alice", "name": "Alice", ...},
            {"id": "bob", "name": "Bob", ...},
        ]
    }

@pytest.fixture
def temp_team_file(temp_dir: Path, sample_team_data) -> Path:
    """Creates actual file for integration tests."""
    teams_dir = temp_dir / "teams"
    teams_dir.mkdir()
    path = teams_dir / "test_team.json"
    path.write_text(json.dumps(sample_team_data))
    return path
```

### 12.3 Test Patterns

**Testing Pydantic models:**
```python
class TestTeamMember:
    def test_valid_member(self, sample_team_data):
        member = TeamMember.model_validate(sample_team_data["members"][0])
        assert member.id == "alice"

    def test_invalid_id_pattern(self):
        with pytest.raises(ValidationError):
            TeamMember(id="Invalid-ID", ...)  # Must be lowercase
```

**Testing state transitions:**
```python
class TestStateManager:
    def test_valid_transition(self):
        sm = StateManager()
        sm.transition_to(MeetingState.TRANSITION)
        assert sm.state == MeetingState.TRANSITION

    def test_invalid_transition_raises(self):
        sm = StateManager()
        with pytest.raises(InvalidStateTransitionError):
            sm.transition_to(MeetingState.COMPLETED)  # Can't go IDLE -> COMPLETED
```

**Testing with time:**
```python
def test_timer_elapsed(self):
    timer = TimerEngine(duration_seconds=60)
    timer.start()
    time.sleep(0.1)  # Wait 100ms
    assert timer.elapsed_seconds >= 0.1
```

---

## 13. Configuration Reference

### 13.1 Application Config (`config.json`)

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
    "file_path": "data/history_{team_id}.json",
    "max_entries": 2000
  },
  "recovery": {
    "enabled": true,
    "auto_save_interval_seconds": 5,
    "file_path": "data/.session_recovery.json"
  },
  "teams": {
    "directory": "teams",
    "default_team": "imagine_dragons"
  }
}
```

### 13.2 Team Config (`teams/<team_id>.json`)

```json
{
  "team": {
    "name": "Imagine Dragons",
    "emoji": "",
    "team_leader": {
      "name": "Yosi Izaq",
      "email": "yosi@example.com"
    }
  },
  "members": [
    {
      "id": "alice",
      "name": "Alice Anderson",
      "display_name": "Alice",
      "email": "alice@example.com",
      "github": "alice-dev",
      "role": "Developer",
      "specialization": ["frontend", "react"],
      "daily_config": {
        "default_time_seconds": 180,
        "active": true
      }
    }
  ]
}
```

---

## Quick Reference Card

### Run Commands

```bash
# Install
pip install -e ".[dev]"

# Run Streamlit UI (default mode)
python main.py
python main.py --team sample_team

# Run CLI mode
python main.py --mode cli

# View meeting history
python main.py --mode history
python main.py --mode history --days 7 --limit 10
python main.py --mode history --team sample_team

# Using installed command (after pip install)
daily-timer --team sample_team
daily-timer --mode history

# Tests
pytest                              # All tests
pytest --cov=src                    # With coverage
pytest tests/unit/test_models.py   # Specific file

# Type check
mypy src/

# Lint
ruff check src/ tests/
ruff check --fix src/
```

### Key Classes to Understand

1. `MeetingManager` - Start here, it orchestrates everything
2. `StateManager` - Understand the state machine
3. `TimerEngine` - How timing works
4. `models.py` - All data structures
5. `CLIApp._main_loop()` - Event loop pattern

### Common Tasks

| Task | Where to Look |
|------|---------------|
| Add new meeting state | `models.py`, `state_manager.py` VALID_TRANSITIONS |
| Change timer behavior | `timer_engine.py` |
| Add analytics metric | `analytics_service.py` |
| Modify CLI display | `cli/display.py` |
| Add team field | `models.py` TeamMember |
| Change storage format | `data/*_repository.py` |

---

*Document generated for Daily Standup Timer v1.0.0*
