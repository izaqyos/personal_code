# Inactivity Timeout Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Auto-close the daily standup CLI after 5 minutes of keyboard inactivity to prevent forgotten sessions.

**Architecture:** Track `time.monotonic()` of last key press in `CLIApp`. Check elapsed inactivity each main loop iteration. When threshold exceeded, call existing `_quit_meeting()` for graceful end. Configurable via `config.json`.

**Tech Stack:** Python, Pydantic models, time.monotonic(), pytest

---

## Task 1: Add `inactivity_timeout_seconds` to TimerConfig model

**Files:**
- Modify: `src/core/models.py:193-228` (TimerConfig class)
- Test: `tests/unit/test_models.py`

**Step 1: Write the failing test**

Add to `tests/unit/test_models.py`:

```python
class TestInactivityTimeoutConfig:
    """Tests for inactivity_timeout_seconds in TimerConfig."""

    def test_timer_config_default_inactivity_timeout(self) -> None:
        """TimerConfig should default to 300s inactivity timeout."""
        config = TimerConfig()
        assert config.inactivity_timeout_seconds == 300

    def test_timer_config_custom_inactivity_timeout(self) -> None:
        """TimerConfig should accept custom inactivity timeout."""
        config = TimerConfig(inactivity_timeout_seconds=600)
        assert config.inactivity_timeout_seconds == 600

    def test_timer_config_inactivity_timeout_minimum(self) -> None:
        """TimerConfig should reject inactivity timeout below 60s."""
        with pytest.raises(ValidationError):
            TimerConfig(inactivity_timeout_seconds=30)

    def test_timer_config_inactivity_timeout_maximum(self) -> None:
        """TimerConfig should reject inactivity timeout above 1800s."""
        with pytest.raises(ValidationError):
            TimerConfig(inactivity_timeout_seconds=3600)
```

**Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/unit/test_models.py::TestInactivityTimeoutConfig -v`
Expected: FAIL — `TimerConfig` has no `inactivity_timeout_seconds` field

**Step 3: Write minimal implementation**

Add to `TimerConfig` in `src/core/models.py`:

```python
inactivity_timeout_seconds: int = Field(
    default=300,
    ge=60,
    le=1800,
    description="Auto-close meeting after this many seconds of no keyboard input (60-1800)",
)
```

**Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/unit/test_models.py::TestInactivityTimeoutConfig -v`
Expected: 4 PASS

**Step 5: Run all model tests to check for regressions**

Run: `.venv/bin/python -m pytest tests/unit/test_models.py -v`
Expected: All PASS

**Step 6: Commit**

```bash
git add src/core/models.py tests/unit/test_models.py
git commit -m "feat(daily-runner): add inactivity_timeout_seconds to TimerConfig"
```

---

## Task 2: Add inactivity timeout logic to CLIApp

**Files:**
- Modify: `src/cli/app.py:1-10` (add `import time`), `src/cli/app.py:52-88` (CLIApp.__init__), `src/cli/app.py:261-326` (_main_loop)
- Test: `tests/unit/test_cli.py`

**Step 1: Write the failing tests**

Add to `tests/unit/test_cli.py`:

```python
import time


class TestInactivityTimeout:
    """Tests for inactivity timeout in CLIApp."""

    def _create_app(self, tmp_path: Path, timeout_seconds: int = 300):
        """Helper to create CLIApp with configurable inactivity timeout."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig, TimerConfig
        from src.data.team_repository import TeamRepository

        timer_config = TimerConfig(inactivity_timeout_seconds=timeout_seconds)
        config = AppConfig(timer=timer_config)

        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()
        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        keyboard = MockKeyboardHandler()
        app = CLIApp(
            config=config,
            team_repo=team_repo,
            keyboard=keyboard,
            console=console,
        )
        return app, keyboard

    def test_last_interaction_time_initialized(self, tmp_path: Path) -> None:
        """CLIApp should initialize _last_interaction_time to 0."""
        app, _ = self._create_app(tmp_path)
        assert app._last_interaction_time == 0.0

    def test_check_inactivity_returns_false_when_active(self, tmp_path: Path) -> None:
        """_check_inactivity should return False when recently active."""
        app, _ = self._create_app(tmp_path)
        app._last_interaction_time = time.monotonic()
        assert app._check_inactivity() is False

    def test_check_inactivity_returns_true_when_idle(self, tmp_path: Path) -> None:
        """_check_inactivity should return True when idle beyond threshold."""
        app, _ = self._create_app(tmp_path, timeout_seconds=60)
        app._last_interaction_time = time.monotonic() - 61
        assert app._check_inactivity() is True

    def test_check_inactivity_returns_false_before_timeout(self, tmp_path: Path) -> None:
        """_check_inactivity should return False when within threshold."""
        app, _ = self._create_app(tmp_path, timeout_seconds=60)
        app._last_interaction_time = time.monotonic() - 30
        assert app._check_inactivity() is False

    def test_reset_interaction_time(self, tmp_path: Path) -> None:
        """_reset_interaction_time should update to current monotonic time."""
        app, _ = self._create_app(tmp_path)
        before = time.monotonic()
        app._reset_interaction_time()
        after = time.monotonic()
        assert before <= app._last_interaction_time <= after
```

**Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/unit/test_cli.py::TestInactivityTimeout -v`
Expected: FAIL — `CLIApp` has no `_last_interaction_time`, `_check_inactivity`, or `_reset_interaction_time`

**Step 3: Write minimal implementation**

In `src/cli/app.py`:

1. Add `import time` at the top (after `import signal`).

2. Add to `__init__` (after `self._in_recovery_prompt = False`):
```python
self._last_interaction_time: float = 0.0
```

3. Add new methods after `_quit_meeting`:
```python
def _reset_interaction_time(self) -> None:
    """Reset the inactivity timer to now."""
    self._last_interaction_time = time.monotonic()

def _check_inactivity(self) -> bool:
    """Check if the inactivity timeout has been exceeded."""
    if self._last_interaction_time == 0.0:
        return False
    elapsed = time.monotonic() - self._last_interaction_time
    return elapsed > self._config.timer.inactivity_timeout_seconds
```

4. In `_main_loop`, at the start (after `self._running = True`):
```python
self._reset_interaction_time()
```

5. In `_main_loop`, after `self._handle_command(result.command)`:
```python
self._reset_interaction_time()
```

6. In `_main_loop`, after the keyboard input block and before the state transition checks, add:
```python
# Check inactivity timeout
if self._check_inactivity():
    logger.info(
        "Inactivity timeout reached (%ds), auto-closing meeting",
        self._config.timer.inactivity_timeout_seconds,
    )
    self._quit_meeting()
    continue
```

**Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/unit/test_cli.py::TestInactivityTimeout -v`
Expected: 5 PASS

**Step 5: Run all CLI tests to check for regressions**

Run: `.venv/bin/python -m pytest tests/unit/test_cli.py -v`
Expected: All PASS (99 + 5 = 104)

**Step 6: Commit**

```bash
git add src/cli/app.py tests/unit/test_cli.py
git commit -m "feat(daily-runner): add inactivity timeout to CLI main loop"
```

---

## Task 3: Update config files

**Files:**
- Modify: `config.json`
- Modify: `config.test.json`
- Modify: `tests/conftest.py` (sample_config fixture)

**Step 1: Update config.json**

Add `"inactivity_timeout_seconds": 300` to the `timer` section.

**Step 2: Update config.test.json**

Add `"inactivity_timeout_seconds": 30` to the `timer` section.

**Step 3: Update test fixture**

Add `"inactivity_timeout_seconds": 30` to the `sample_config` fixture's `timer` dict in `tests/conftest.py`.

**Step 4: Run config loading tests**

Run: `.venv/bin/python -m pytest tests/unit/test_config_loading.py -v`
Expected: All PASS

**Step 5: Run full test suite**

Run: `.venv/bin/python -m pytest tests/ -v`
Expected: All PASS

**Step 6: Commit**

```bash
git add config.json config.test.json tests/conftest.py
git commit -m "feat(daily-runner): add inactivity timeout to config files"
```
