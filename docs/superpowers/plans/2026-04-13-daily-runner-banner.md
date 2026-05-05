# Daily Runner Banner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an opt-in CLI banner to `daily_runner` that shows release-cadence context (sprint, week, champion, DoD, next event) plus optional free text, controlled by `-b`/`--banner-fields`/`--banner-text`/`--no-banner` flags.

**Architecture:** New isolated `src/banner/` module: pure data loader, pure date logic, pure rich-Panel renderer, thin orchestrator. Main CLI only adds flags and a single call. Schedules JSON path is configurable (absolute) with graceful degrade and example file when missing.

**Tech Stack:** Python 3.10+, `rich` (already a dep), `pydantic` (already a dep), `pytest` + `pytest-cov` for testing. Bash for launcher integration.

**Spec:** [docs/superpowers/specs/2026-04-13-daily-runner-banner-design.md](../specs/2026-04-13-daily-runner-banner-design.md)

---

## File Structure

**Project root for paths below:** `code/python/tools/daily_runner/`

### New files

| Path | Responsibility |
|---|---|
| `src/banner/__init__.py` | Public API: `render_banner(args, app_config) -> str \| None`. Orchestrates loader → cadence → renderer. |
| `src/banner/errors.py` | `BannerError` (base), `MissingScheduleError`, `MalformedScheduleError`. |
| `src/banner/schedule_loader.py` | `load_schedules(path: Path) -> Schedules`. Pure I/O + validation. |
| `src/banner/models.py` | Pydantic models: `Schedules`, `SprintInfo`, `RotationEntry`. |
| `src/banner/cadence.py` | Pure date logic: `current_sprint`, `sprint_week`, `dod_for`, `next_event`. |
| `src/banner/renderer.py` | `render_panel(fields_data, free_text, width) -> str`. Rich panel composition + width adaptation. |
| `tests/unit/test_banner_loader.py` | Loader tests. |
| `tests/unit/test_banner_models.py` | Model validation tests. |
| `tests/unit/test_banner_cadence.py` | Date-logic table tests. |
| `tests/unit/test_banner_renderer.py` | Width-adaptive rendering tests. |
| `tests/unit/test_banner_orchestrator.py` | `render_banner` orchestration tests. |
| `tests/unit/test_banner_cli.py` | CLI flag parsing + precedence tests. |
| `config/schedules.example.json` | Anonymized example, anchored at 2026-01-01. |

### Modified files

| Path | Change |
|---|---|
| `src/core/models.py` | Add `BannerConfig` pydantic model; add `banner: BannerConfig` field to `AppConfig`. |
| `main.py` | Register banner CLI flags; print banner before launching CLI mode. |
| `README.md` | Add Banner section. |
| `code/bash/tools/launcher/launcher.sh` | Add menu items `[2]` and `[3]`; renumber existing; update prompt range. |
| `code/bash/tools/launcher/README.md` | Document new menu items. |
| `code/bash/tools/launcher/CHANGELOG.md` | Entry for new options. |
| `code/python/tools/README.md` | One-line bump if daily_runner is mentioned. |
| `code/python/README.md` | Same. |
| `code/README.md` | Same. |

---

## Conventions used in this plan

- Run all `pytest` commands from `code/python/tools/daily_runner/` with the dev extras installed (`pip install -e ".[dev]"` once per checkout).
- Run all `git` commands from the repo root unless noted.
- Use `python -m pytest` form to avoid PATH ambiguity.
- Test file imports use `from src.banner.<module>` (matches existing `from src.cli.app` pattern).
- Type hints use Python 3.10+ syntax (`X | None`, `list[int]`).

---

## Task 1: Banner errors module

**Files:**
- Create: `code/python/tools/daily_runner/src/banner/__init__.py` (empty for now)
- Create: `code/python/tools/daily_runner/src/banner/errors.py`
- Create: `code/python/tools/daily_runner/tests/unit/test_banner_errors.py`

- [ ] **Step 1.1: Create empty package init**

```python
# code/python/tools/daily_runner/src/banner/__init__.py
"""Banner module for the daily standup CLI."""
```

- [ ] **Step 1.2: Write the failing test**

`code/python/tools/daily_runner/tests/unit/test_banner_errors.py`:

```python
"""Tests for banner error types."""

import pytest

from src.banner.errors import BannerError, MalformedScheduleError, MissingScheduleError


class TestBannerErrors:
    def test_banner_error_is_base_exception(self) -> None:
        assert issubclass(BannerError, Exception)

    def test_missing_schedule_error_is_banner_error(self) -> None:
        assert issubclass(MissingScheduleError, BannerError)

    def test_malformed_schedule_error_is_banner_error(self) -> None:
        assert issubclass(MalformedScheduleError, BannerError)

    def test_missing_schedule_carries_path(self) -> None:
        err = MissingScheduleError("/some/path/schedules.json")
        assert err.path == "/some/path/schedules.json"
        assert "/some/path/schedules.json" in str(err)

    def test_malformed_schedule_carries_reason(self) -> None:
        err = MalformedScheduleError("missing key: rotation_schedule")
        assert err.reason == "missing key: rotation_schedule"
        assert "missing key: rotation_schedule" in str(err)
```

- [ ] **Step 1.3: Run test to verify it fails**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_errors.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.banner.errors'`.

- [ ] **Step 1.4: Implement the module**

`code/python/tools/daily_runner/src/banner/errors.py`:

```python
"""Banner-specific exception types."""


class BannerError(Exception):
    """Base class for banner-related errors."""


class MissingScheduleError(BannerError):
    """Raised when the schedules.json file cannot be located or read."""

    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__(f"schedules.json not found at: {path}")


class MalformedScheduleError(BannerError):
    """Raised when schedules.json exists but cannot be parsed/validated."""

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(f"malformed schedules.json: {reason}")
```

- [ ] **Step 1.5: Run test to verify it passes**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_errors.py -v`
Expected: PASS — 5 passed.

- [ ] **Step 1.6: Commit**

```bash
git add code/python/tools/daily_runner/src/banner/__init__.py \
        code/python/tools/daily_runner/src/banner/errors.py \
        code/python/tools/daily_runner/tests/unit/test_banner_errors.py
git commit -m "feat(banner): add error types for daily_runner banner module"
```

---

## Task 2: Banner pydantic models

**Files:**
- Create: `code/python/tools/daily_runner/src/banner/models.py`
- Create: `code/python/tools/daily_runner/tests/unit/test_banner_models.py`

- [ ] **Step 2.1: Write the failing test**

`code/python/tools/daily_runner/tests/unit/test_banner_models.py`:

```python
"""Tests for banner pydantic models."""

from datetime import date

import pytest
from pydantic import ValidationError

from src.banner.models import RotationEntry, Schedules


class TestRotationEntry:
    def test_parses_minimal_entry(self) -> None:
        entry = RotationEntry(
            champion="yocheved",
            dr=date(2026, 4, 26),
            go_nogo=date(2026, 4, 30),
            prod=date(2026, 5, 3),
        )
        assert entry.champion == "yocheved"
        assert entry.dr == date(2026, 4, 26)
        assert entry.release_title is None

    def test_parses_with_release_title(self) -> None:
        entry = RotationEntry(
            champion="osher",
            dr=date(2026, 5, 17),
            go_nogo=date(2026, 5, 21),
            prod=date(2026, 5, 24),
            release_title="26.Q2.3.0",
        )
        assert entry.release_title == "26.Q2.3.0"

    def test_rejects_missing_champion(self) -> None:
        with pytest.raises(ValidationError):
            RotationEntry(
                dr=date(2026, 4, 26),
                go_nogo=date(2026, 4, 30),
                prod=date(2026, 5, 3),
            )


class TestSchedules:
    def test_parses_full_schedule(self) -> None:
        data = {
            "team_members": {"muhe": "U07ANSFJ8D9", "yocheved": "U07ANSFF3EX"},
            "rotation_schedule": {
                "26.Q2.1": {
                    "champion": "yocheved",
                    "dr": "2026-04-26",
                    "go_nogo": "2026-04-30",
                    "prod": "2026-05-03",
                },
            },
            "dod_schedule": {"2026-04-12": "chen", "2026-04-19": "yair"},
        }
        sched = Schedules.model_validate(data)
        assert "26.Q2.1" in sched.rotation_schedule
        assert sched.dod_schedule[date(2026, 4, 12)] == "chen"
        assert sched.team_members["muhe"] == "U07ANSFJ8D9"

    def test_rejects_missing_rotation_schedule(self) -> None:
        with pytest.raises(ValidationError):
            Schedules.model_validate({"dod_schedule": {}, "team_members": {}})

    def test_ignores_unknown_top_level_keys(self) -> None:
        data = {
            "team_members": {},
            "rotation_schedule": {},
            "dod_schedule": {},
            "_meta": {"description": "anything"},
            "tech_leads": {"yocheved": "X"},
        }
        sched = Schedules.model_validate(data)
        assert sched.rotation_schedule == {}
```

- [ ] **Step 2.2: Run test to verify it fails**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_models.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.banner.models'`.

- [ ] **Step 2.3: Implement the module**

`code/python/tools/daily_runner/src/banner/models.py`:

```python
"""Pydantic models for parsing schedules.json."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class RotationEntry(BaseModel):
    """One sprint entry from rotation_schedule."""

    model_config = ConfigDict(extra="ignore")

    champion: str
    dr: date
    go_nogo: date
    prod: date
    release_title: str | None = None


class Schedules(BaseModel):
    """Top-level schedules.json contents."""

    model_config = ConfigDict(extra="ignore")

    team_members: dict[str, str] = Field(default_factory=dict)
    rotation_schedule: dict[str, RotationEntry]
    dod_schedule: dict[date, str] = Field(default_factory=dict)
```

- [ ] **Step 2.4: Run test to verify it passes**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_models.py -v`
Expected: PASS — 6 passed.

- [ ] **Step 2.5: Commit**

```bash
git add code/python/tools/daily_runner/src/banner/models.py \
        code/python/tools/daily_runner/tests/unit/test_banner_models.py
git commit -m "feat(banner): add pydantic models for schedules.json"
```

---

## Task 3: Schedule loader + example file

**Files:**
- Create: `code/python/tools/daily_runner/src/banner/schedule_loader.py`
- Create: `code/python/tools/daily_runner/config/schedules.example.json`
- Create: `code/python/tools/daily_runner/tests/unit/test_banner_loader.py`

- [ ] **Step 3.1: Write the failing test**

`code/python/tools/daily_runner/tests/unit/test_banner_loader.py`:

```python
"""Tests for schedule_loader."""

import json
from pathlib import Path

import pytest

from src.banner.errors import MalformedScheduleError, MissingScheduleError
from src.banner.schedule_loader import load_schedules


VALID_DATA = {
    "team_members": {"yocheved": "U07ANSFF3EX"},
    "rotation_schedule": {
        "26.Q2.1": {
            "champion": "yocheved",
            "dr": "2026-04-26",
            "go_nogo": "2026-04-30",
            "prod": "2026-05-03",
        },
    },
    "dod_schedule": {"2026-04-12": "chen"},
}


class TestLoadSchedules:
    def test_loads_valid_file(self, tmp_path: Path) -> None:
        path = tmp_path / "schedules.json"
        path.write_text(json.dumps(VALID_DATA))

        result = load_schedules(path)

        assert "26.Q2.1" in result.rotation_schedule
        assert result.rotation_schedule["26.Q2.1"].champion == "yocheved"

    def test_missing_file_raises(self, tmp_path: Path) -> None:
        path = tmp_path / "does_not_exist.json"

        with pytest.raises(MissingScheduleError) as exc_info:
            load_schedules(path)

        assert str(path) in exc_info.value.path

    def test_empty_path_raises(self) -> None:
        with pytest.raises(MissingScheduleError):
            load_schedules(Path(""))

    def test_invalid_json_raises_malformed(self, tmp_path: Path) -> None:
        path = tmp_path / "schedules.json"
        path.write_text("{not valid json")

        with pytest.raises(MalformedScheduleError) as exc_info:
            load_schedules(path)

        assert "json" in exc_info.value.reason.lower()

    def test_missing_required_key_raises_malformed(self, tmp_path: Path) -> None:
        path = tmp_path / "schedules.json"
        path.write_text(json.dumps({"team_members": {}, "dod_schedule": {}}))

        with pytest.raises(MalformedScheduleError):
            load_schedules(path)

    def test_path_with_tilde_expands(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("HOME", str(tmp_path))
        target = tmp_path / "schedules.json"
        target.write_text(json.dumps(VALID_DATA))

        result = load_schedules(Path("~/schedules.json"))

        assert "26.Q2.1" in result.rotation_schedule
```

- [ ] **Step 3.2: Run test to verify it fails**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_loader.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.banner.schedule_loader'`.

- [ ] **Step 3.3: Implement the loader**

`code/python/tools/daily_runner/src/banner/schedule_loader.py`:

```python
"""Loads and validates schedules.json from disk."""

import json
from pathlib import Path

from pydantic import ValidationError

from src.banner.errors import MalformedScheduleError, MissingScheduleError
from src.banner.models import Schedules


def load_schedules(path: Path) -> Schedules:
    """Load schedules.json from path. Raises BannerError subclasses on failure.

    Args:
        path: Path to schedules.json. Empty paths and `~`-prefixed paths are
            handled. Tilde is expanded against $HOME.

    Returns:
        A validated `Schedules` instance.

    Raises:
        MissingScheduleError: file is missing or path is empty.
        MalformedScheduleError: file is unreadable JSON or fails validation.
    """
    if not str(path):
        raise MissingScheduleError("")

    resolved = Path(str(path)).expanduser()

    if not resolved.is_file():
        raise MissingScheduleError(str(resolved))

    try:
        raw = json.loads(resolved.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise MalformedScheduleError(f"invalid JSON: {exc}") from exc

    try:
        return Schedules.model_validate(raw)
    except ValidationError as exc:
        raise MalformedScheduleError(str(exc)) from exc
```

- [ ] **Step 3.4: Run test to verify it passes**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_loader.py -v`
Expected: PASS — 6 passed.

- [ ] **Step 3.5: Create the example schedules file**

`code/python/tools/daily_runner/config/schedules.example.json`:

```json
{
  "_meta": {
    "description": "Example schedules.json — anonymized template anchored at 2026-01-01.",
    "instructions": [
      "Copy this file to your real schedules.json location and edit.",
      "Set banner.schedules_path in config.json to point at your file.",
      "Sprint keys follow YY.QN.S where N=quarter, S=sprint within quarter.",
      "DR is dry-run, go_nogo is the release decision date, prod is shipping date.",
      "dod_schedule maps the Sunday of each week to the Developer on Duty."
    ]
  },
  "team_members": {
    "alice": "UEXAMPLE001",
    "bob": "UEXAMPLE002",
    "carol": "UEXAMPLE003",
    "dave": "UEXAMPLE004"
  },
  "rotation_schedule": {
    "26.Q1.1": {
      "champion": "alice",
      "dr": "2026-01-18",
      "go_nogo": "2026-01-22",
      "prod": "2026-01-25",
      "release_title": "26.Q1.1.0"
    },
    "26.Q1.2": {
      "champion": "bob",
      "dr": "2026-02-08",
      "go_nogo": "2026-02-12",
      "prod": "2026-02-15",
      "release_title": "26.Q1.2.0"
    },
    "26.Q1.3": {
      "champion": "carol",
      "dr": "2026-03-01",
      "go_nogo": "2026-03-05",
      "prod": "2026-03-08",
      "release_title": "26.Q1.3.0"
    }
  },
  "dod_schedule": {
    "2026-01-04": "alice",
    "2026-01-11": "bob",
    "2026-01-18": "carol",
    "2026-01-25": "dave",
    "2026-02-01": "alice",
    "2026-02-08": "bob",
    "2026-02-15": "carol",
    "2026-02-22": "dave"
  }
}
```

- [ ] **Step 3.6: Verify example loads cleanly**

Run: `cd code/python/tools/daily_runner && python -c "from pathlib import Path; from src.banner.schedule_loader import load_schedules; print(load_schedules(Path('config/schedules.example.json')).rotation_schedule.keys())"`
Expected: `dict_keys(['26.Q1.1', '26.Q1.2', '26.Q1.3'])`

- [ ] **Step 3.7: Commit**

```bash
git add code/python/tools/daily_runner/src/banner/schedule_loader.py \
        code/python/tools/daily_runner/config/schedules.example.json \
        code/python/tools/daily_runner/tests/unit/test_banner_loader.py
git commit -m "feat(banner): add schedule_loader with example schedules.json"
```

---

## Task 4: Cadence date logic

**Files:**
- Create: `code/python/tools/daily_runner/src/banner/cadence.py`
- Create: `code/python/tools/daily_runner/tests/unit/test_banner_cadence.py`

This task is independent of Task 5 (renderer) — they can run in parallel.

- [ ] **Step 4.1: Write the failing test**

`code/python/tools/daily_runner/tests/unit/test_banner_cadence.py`:

```python
"""Tests for banner cadence (date-logic) helpers."""

from datetime import date

import pytest

from src.banner.cadence import (
    NextEvent,
    current_sprint,
    dod_for,
    next_event,
    sprint_week,
)
from src.banner.models import RotationEntry, Schedules


def make_schedules() -> Schedules:
    return Schedules.model_validate(
        {
            "team_members": {"yocheved": "U1", "osher": "U2", "muhammad": "U3"},
            "rotation_schedule": {
                "26.Q1.4": {
                    "champion": "yair",
                    "dr": "2026-03-29",
                    "go_nogo": "2026-04-02",
                    "prod": "2026-04-12",
                },
                "26.Q2.1": {
                    "champion": "yocheved",
                    "dr": "2026-04-26",
                    "go_nogo": "2026-04-30",
                    "prod": "2026-05-03",
                },
                "26.Q2.2": {
                    "champion": "osher",
                    "dr": "2026-05-17",
                    "go_nogo": "2026-05-21",
                    "prod": "2026-05-24",
                },
            },
            "dod_schedule": {
                "2026-04-05": "osher",
                "2026-04-12": "chen",
                "2026-04-19": "yair",
                "2026-04-26": "yocheved",
                "2026-05-03": "muhe",
            },
        }
    )


class TestCurrentSprint:
    @pytest.mark.parametrize(
        "today, expected",
        [
            (date(2026, 4, 13), "26.Q2.1"),  # mid-sprint (start = 4-12)
            (date(2026, 4, 12), "26.Q2.1"),  # sprint start day
            (date(2026, 5, 2), "26.Q2.1"),   # last day before next sprint
            (date(2026, 5, 3), "26.Q2.2"),   # next sprint starts (start = 5-3)
            (date(2026, 1, 1), "26.Q1.4"),   # before any sprint → earliest
            (date(2030, 1, 1), "26.Q2.2"),   # after last sprint → last
        ],
    )
    def test_returns_expected_sprint_id(self, today: date, expected: str) -> None:
        sched = make_schedules()
        assert current_sprint(sched, today) == expected


class TestSprintWeek:
    @pytest.mark.parametrize(
        "today, expected",
        [
            (date(2026, 4, 12), 1),  # sprint start
            (date(2026, 4, 18), 1),
            (date(2026, 4, 19), 2),
            (date(2026, 4, 25), 2),
            (date(2026, 4, 26), 3),  # DR day = week 3
            (date(2026, 5, 2), 3),
        ],
    )
    def test_returns_week_1_to_3(self, today: date, expected: int) -> None:
        sched = make_schedules()
        assert sprint_week(sched, "26.Q2.1", today) == expected


class TestDoDFor:
    @pytest.mark.parametrize(
        "today, expected",
        [
            (date(2026, 4, 12), "chen"),    # exact match
            (date(2026, 4, 14), "chen"),    # mid-week
            (date(2026, 4, 19), "yair"),    # next Sunday
            (date(2026, 4, 18), "chen"),    # Saturday rolls back to Sunday 4-12
        ],
    )
    def test_returns_dod_for_week_of(self, today: date, expected: str) -> None:
        sched = make_schedules()
        assert dod_for(sched, today) == expected

    def test_returns_none_when_no_match(self) -> None:
        sched = make_schedules()
        assert dod_for(sched, date(2025, 1, 1)) is None


class TestNextEvent:
    def test_pre_dr_returns_dr(self) -> None:
        sched = make_schedules()
        result = next_event(sched, date(2026, 4, 13))
        assert result == NextEvent(label="DR", target=date(2026, 4, 26), days_until=13)

    def test_dr_day_returns_prod(self) -> None:
        sched = make_schedules()
        result = next_event(sched, date(2026, 4, 26))
        assert result == NextEvent(label="Prod", target=date(2026, 5, 3), days_until=7)

    def test_between_dr_and_prod_returns_prod(self) -> None:
        sched = make_schedules()
        result = next_event(sched, date(2026, 4, 30))
        assert result == NextEvent(label="Prod", target=date(2026, 5, 3), days_until=3)

    def test_after_prod_returns_next_sprint_dr(self) -> None:
        sched = make_schedules()
        result = next_event(sched, date(2026, 5, 4))
        assert result == NextEvent(label="DR", target=date(2026, 5, 17), days_until=13)

    def test_returns_none_when_no_future_events(self) -> None:
        sched = make_schedules()
        assert next_event(sched, date(2030, 1, 1)) is None
```

- [ ] **Step 4.2: Run test to verify it fails**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_cadence.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.banner.cadence'`.

- [ ] **Step 4.3: Implement the module**

`code/python/tools/daily_runner/src/banner/cadence.py`:

```python
"""Pure date logic for banner cadence info. No I/O; takes `today` for testability."""

from dataclasses import dataclass
from datetime import date, timedelta

from src.banner.models import Schedules

SPRINT_LENGTH_DAYS = 21
SPRINT_START_OFFSET_FROM_DR = 14


@dataclass(frozen=True)
class NextEvent:
    label: str
    target: date
    days_until: int


def _sprint_start(dr: date) -> date:
    return dr - timedelta(days=SPRINT_START_OFFSET_FROM_DR)


def _sorted_sprint_ids(sched: Schedules) -> list[str]:
    return sorted(sched.rotation_schedule.keys(), key=lambda k: sched.rotation_schedule[k].dr)


def current_sprint(sched: Schedules, today: date) -> str | None:
    ids = _sorted_sprint_ids(sched)
    if not ids:
        return None

    earliest_start = _sprint_start(sched.rotation_schedule[ids[0]].dr)
    if today < earliest_start:
        return ids[0]

    current = ids[0]
    for sprint_id in ids:
        start = _sprint_start(sched.rotation_schedule[sprint_id].dr)
        if today >= start:
            current = sprint_id
        else:
            break
    return current


def sprint_week(sched: Schedules, sprint_id: str, today: date) -> int:
    entry = sched.rotation_schedule[sprint_id]
    start = _sprint_start(entry.dr)
    delta_days = (today - start).days
    week = delta_days // 7 + 1
    return max(1, min(3, week))


def _sunday_of(d: date) -> date:
    """Return the Sunday on or before `d` (Python: weekday() Sunday = 6)."""
    days_since_sunday = (d.weekday() + 1) % 7
    return d - timedelta(days=days_since_sunday)


def dod_for(sched: Schedules, today: date) -> str | None:
    sunday = _sunday_of(today)
    return sched.dod_schedule.get(sunday)


def next_event(sched: Schedules, today: date) -> NextEvent | None:
    ids = _sorted_sprint_ids(sched)
    for sprint_id in ids:
        entry = sched.rotation_schedule[sprint_id]
        if today < entry.dr:
            return NextEvent("DR", entry.dr, (entry.dr - today).days)
        if today < entry.prod:
            return NextEvent("Prod", entry.prod, (entry.prod - today).days)
    return None
```

- [ ] **Step 4.4: Run test to verify it passes**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_cadence.py -v`
Expected: PASS — 17 passed.

- [ ] **Step 4.5: Commit**

```bash
git add code/python/tools/daily_runner/src/banner/cadence.py \
        code/python/tools/daily_runner/tests/unit/test_banner_cadence.py
git commit -m "feat(banner): add pure cadence date logic with table-driven tests"
```

---

## Task 5: Renderer

**Files:**
- Create: `code/python/tools/daily_runner/src/banner/renderer.py`
- Create: `code/python/tools/daily_runner/tests/unit/test_banner_renderer.py`

This task is independent of Task 4 — they can run in parallel.

- [ ] **Step 5.1: Write the failing test**

`code/python/tools/daily_runner/tests/unit/test_banner_renderer.py`:

```python
"""Tests for the banner renderer (rich Panel composition + width adaptation)."""

from datetime import date

from src.banner.cadence import NextEvent
from src.banner.renderer import BannerData, render_banner_text, render_error_banner


def make_data(**overrides: object) -> BannerData:
    base = BannerData(
        today=date(2026, 4, 13),
        sprint_id="26.Q2.1",
        sprint_week=2,
        champion="yocheved",
        dod="yocheved",
        next_event=NextEvent("DR", date(2026, 4, 26), 13),
        free_text=None,
    )
    return base.model_copy(update=overrides) if hasattr(base, "model_copy") else base


class TestRenderBannerText:
    def test_wide_layout_includes_all_default_fields(self) -> None:
        data = make_data()
        out = render_banner_text(data, width=100)

        assert "26.Q2.1" in out
        assert "Week 2" in out
        assert "Yocheved" in out  # title-cased
        assert "DR" in out
        assert "13d" in out

    def test_narrow_layout_uses_short_labels(self) -> None:
        data = make_data()
        out = render_banner_text(data, width=60)

        assert "26.Q2.1" in out
        assert "Champ" in out or "Champion" in out
        assert "DoD" in out

    def test_tiny_layout_no_panel_chrome(self) -> None:
        data = make_data()
        out = render_banner_text(data, width=35)

        # No box-drawing characters
        assert "╭" not in out
        assert "╰" not in out
        assert "26.Q2.1" in out

    def test_free_text_appears_when_provided(self) -> None:
        data = make_data(free_text="welcome back Muhe!")
        out = render_banner_text(data, width=100)

        assert "welcome back Muhe!" in out

    def test_free_text_only_no_cadence_fields(self) -> None:
        data = BannerData(
            today=date(2026, 4, 13),
            sprint_id=None,
            sprint_week=None,
            champion=None,
            dod=None,
            next_event=None,
            free_text="hello world",
        )
        out = render_banner_text(data, width=100)

        assert "hello world" in out
        assert "26.Q2" not in out

    def test_two_day_countdown_marked(self) -> None:
        data = make_data(next_event=NextEvent("DR", date(2026, 4, 15), 2))
        out = render_banner_text(data, width=100)
        assert "2d" in out

    def test_day_of_event_shown(self) -> None:
        data = make_data(next_event=NextEvent("DR", date(2026, 4, 13), 0))
        out = render_banner_text(data, width=100)
        assert "today" in out.lower() or "0d" in out


class TestRenderErrorBanner:
    def test_includes_path(self) -> None:
        out = render_error_banner(
            schedule_path="/tmp/schedules.json",
            reason="file not found",
            free_text=None,
            width=100,
        )

        assert "/tmp/schedules.json" in out
        assert "Banner unavailable" in out or "unavailable" in out.lower()

    def test_includes_fix_instructions(self) -> None:
        out = render_error_banner(
            schedule_path="/tmp/schedules.json",
            reason="file not found",
            free_text=None,
            width=100,
        )

        assert "schedules.example.json" in out
        assert "--no-banner" in out

    def test_appends_free_text_when_provided(self) -> None:
        out = render_error_banner(
            schedule_path="/tmp/x.json",
            reason="missing",
            free_text="welcome back",
            width=100,
        )
        assert "welcome back" in out
```

- [ ] **Step 5.2: Run test to verify it fails**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_renderer.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.banner.renderer'`.

- [ ] **Step 5.3: Implement the renderer**

`code/python/tools/daily_runner/src/banner/renderer.py`:

```python
"""Renders banner data as a rich Panel string. Handles width adaptation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from io import StringIO

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from src.banner.cadence import NextEvent

WIDE_THRESHOLD = 80
TINY_THRESHOLD = 40


@dataclass
class BannerData:
    today: date
    sprint_id: str | None
    sprint_week: int | None
    champion: str | None
    dod: str | None
    next_event: NextEvent | None
    free_text: str | None


def _name(value: str | None) -> str:
    if not value:
        return "?"
    return value[:1].upper() + value[1:]


def _short_name(value: str | None) -> str:
    if not value:
        return "?"
    return _name(value)[:4]


def _countdown_str(ev: NextEvent) -> str:
    if ev.days_until == 0:
        return f"{ev.label} today · {ev.target.strftime('%a %b %d')}"
    return f"{ev.label} in {ev.days_until}d · {ev.target.strftime('%a %b %d')}"


def _short_countdown_str(ev: NextEvent) -> str:
    if ev.days_until == 0:
        return f"{ev.label} today"
    return f"{ev.label} in {ev.days_until}d"


def _capture(renderable: object, width: int) -> str:
    buf = StringIO()
    console = Console(file=buf, width=width, force_terminal=False, no_color=True)
    console.print(renderable)
    return buf.getvalue()


def _render_wide(data: BannerData, width: int) -> str:
    title_parts = []
    if data.sprint_id:
        title_parts.append(f"Sprint {data.sprint_id}")
    if data.sprint_week:
        title_parts.append(f"Week {data.sprint_week}")
    title_parts.append(data.today.strftime("%a %b %d"))
    title = " · ".join(title_parts)

    lines: list[str] = []
    if data.champion or data.dod:
        body = []
        if data.champion:
            body.append(f"Champion: {_name(data.champion)}")
        if data.dod:
            body.append(f"DoD: {_name(data.dod)}")
        lines.append("  ".join(body))
    if data.next_event:
        lines.append(_countdown_str(data.next_event))
    if data.free_text:
        lines.append(data.free_text)

    body = "\n".join(lines) if lines else " "
    panel = Panel(body, title=title, border_style="cyan", width=width)
    return _capture(panel, width)


def _render_narrow(data: BannerData, width: int) -> str:
    title_parts = []
    if data.sprint_id:
        title_parts.append(data.sprint_id)
    if data.sprint_week:
        title_parts.append(f"W{data.sprint_week}")
    title_parts.append(data.today.strftime("%b %d"))
    title = " · ".join(title_parts)

    lines: list[str] = []
    if data.champion or data.dod:
        parts = []
        if data.champion:
            parts.append(f"Champ: {_short_name(data.champion)}")
        if data.dod:
            parts.append(f"DoD: {_short_name(data.dod)}")
        lines.append("   ".join(parts))
    if data.next_event:
        lines.append(_short_countdown_str(data.next_event))
    if data.free_text:
        lines.append(data.free_text)

    body = "\n".join(lines) if lines else " "
    panel = Panel(body, title=title, border_style="cyan", width=width)
    return _capture(panel, width)


def _render_tiny(data: BannerData, width: int) -> str:
    parts: list[str] = []
    if data.sprint_id:
        sp = data.sprint_id
        if data.sprint_week:
            sp += f" W{data.sprint_week}"
        parts.append(sp)
    if data.champion:
        parts.append(f"Champ:{_short_name(data.champion)}")
    if data.dod:
        parts.append(f"DoD:{_short_name(data.dod)}")
    if data.next_event:
        parts.append(_short_countdown_str(data.next_event))
    line = " | ".join(parts)
    if data.free_text:
        return f"{line}\n{data.free_text}\n" if line else f"{data.free_text}\n"
    return line + "\n"


def render_banner_text(data: BannerData, width: int) -> str:
    if width < TINY_THRESHOLD:
        return _render_tiny(data, width)
    if width < WIDE_THRESHOLD:
        return _render_narrow(data, width)
    return _render_wide(data, width)


def render_error_banner(
    schedule_path: str,
    reason: str,
    free_text: str | None,
    width: int,
) -> str:
    body_lines = [
        f"schedules.json not found at:",
        f"  {schedule_path}",
        f"  ({reason})" if reason else "",
        "",
        "Fix:",
        "  1. Set banner.schedules_path in config.json",
        "  2. Or copy the example:",
        "     cp config/schedules.example.json \\",
        "        config/schedules.json",
        "  3. Or run with --no-banner to suppress",
    ]
    body = "\n".join(line for line in body_lines if line is not None)
    panel = Panel(
        body,
        title="⚠ Banner unavailable",
        border_style="yellow",
        width=max(width, TINY_THRESHOLD),
    )
    out = _capture(panel, max(width, TINY_THRESHOLD))
    if free_text:
        out += f"{free_text}\n"
    return out
```

- [ ] **Step 5.4: Run test to verify it passes**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_renderer.py -v`
Expected: PASS — 10 passed.

- [ ] **Step 5.5: Visual sanity check**

Run:
```bash
cd code/python/tools/daily_runner && python -c "
from datetime import date
from src.banner.cadence import NextEvent
from src.banner.renderer import BannerData, render_banner_text
data = BannerData(
    today=date(2026, 4, 13),
    sprint_id='26.Q2.1', sprint_week=2,
    champion='yocheved', dod='yocheved',
    next_event=NextEvent('DR', date(2026, 4, 26), 13),
    free_text='welcome back Muhe!',
)
print(render_banner_text(data, 100))
print('---')
print(render_banner_text(data, 60))
print('---')
print(render_banner_text(data, 35))
"
```
Expected: three banner variants printed, wide → narrow → tiny.

- [ ] **Step 5.6: Commit**

```bash
git add code/python/tools/daily_runner/src/banner/renderer.py \
        code/python/tools/daily_runner/tests/unit/test_banner_renderer.py
git commit -m "feat(banner): add width-adaptive renderer with rich panels"
```

---

## Task 6: Banner config schema

**Files:**
- Modify: `code/python/tools/daily_runner/src/core/models.py:311-360`
- Create test: extend `code/python/tools/daily_runner/tests/unit/test_config_loading.py` with new section

This task depends on nothing in Tasks 1-5; it can run in parallel with them. It must complete before Task 7.

- [ ] **Step 6.1: Write the failing test**

Append to `code/python/tools/daily_runner/tests/unit/test_config_loading.py` (end of file):

```python


class TestBannerConfig:
    """Tests for the new BannerConfig section."""

    def test_default_banner_config(self) -> None:
        from src.core.models import AppConfig

        cfg = AppConfig()
        assert cfg.banner.enabled is False
        assert cfg.banner.schedules_path == ""
        assert "sprint" in cfg.banner.default_fields

    def test_banner_config_round_trip(self) -> None:
        from src.core.models import AppConfig

        cfg = AppConfig.model_validate(
            {
                "banner": {
                    "enabled": True,
                    "schedules_path": "/tmp/schedules.json",
                    "default_fields": ["sprint", "dod"],
                },
            }
        )
        assert cfg.banner.enabled is True
        assert cfg.banner.schedules_path == "/tmp/schedules.json"
        assert cfg.banner.default_fields == ["sprint", "dod"]

    def test_banner_config_omitted_uses_defaults(self) -> None:
        from src.core.models import AppConfig

        cfg = AppConfig.model_validate({"version": "1.0"})
        assert cfg.banner.enabled is False
```

- [ ] **Step 6.2: Run test to verify it fails**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_config_loading.py::TestBannerConfig -v`
Expected: FAIL — `cfg.banner` does not exist.

- [ ] **Step 6.3: Add the BannerConfig model**

In `code/python/tools/daily_runner/src/core/models.py`, before the `class AppConfig` definition, add:

```python
class BannerConfig(BaseModel):
    """Banner configuration (cadence info shown before standup starts)."""

    model_config = ConfigDict(strict=True)

    enabled: bool = Field(
        default=False,
        description="Whether banner is shown by default; CLI flags override.",
    )
    schedules_path: str = Field(
        default="",
        description="Absolute path to schedules.json (empty = banner disabled).",
    )
    default_fields: list[str] = Field(
        default_factory=lambda: ["sprint", "sprint_week", "champion", "dod", "next_event"],
        description="Cadence fields shown when -b is bare.",
    )
```

Then in `AppConfig`, add the field (after `teams: TeamsConfig = ...`):

```python
    banner: BannerConfig = Field(
        default_factory=BannerConfig,
        description="Banner settings",
    )
```

- [ ] **Step 6.4: Run test to verify it passes**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_config_loading.py -v`
Expected: PASS — all tests including 3 new banner tests.

- [ ] **Step 6.5: Run the full test suite to verify no regressions**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/ -v`
Expected: PASS — all unit tests.

- [ ] **Step 6.6: Commit**

```bash
git add code/python/tools/daily_runner/src/core/models.py \
        code/python/tools/daily_runner/tests/unit/test_config_loading.py
git commit -m "feat(config): add BannerConfig section to AppConfig"
```

---

## Task 7: Banner orchestrator (`__init__.py`)

**Files:**
- Modify: `code/python/tools/daily_runner/src/banner/__init__.py`
- Create: `code/python/tools/daily_runner/tests/unit/test_banner_orchestrator.py`

Depends on Tasks 1, 2, 3, 4, 5, 6.

- [ ] **Step 7.1: Write the failing test**

`code/python/tools/daily_runner/tests/unit/test_banner_orchestrator.py`:

```python
"""Integration tests for the banner orchestrator."""

import json
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.banner import render_banner
from src.core.models import BannerConfig

VALID_DATA = {
    "team_members": {"yocheved": "U1"},
    "rotation_schedule": {
        "26.Q2.1": {
            "champion": "yocheved",
            "dr": "2026-04-26",
            "go_nogo": "2026-04-30",
            "prod": "2026-05-03",
        },
    },
    "dod_schedule": {"2026-04-12": "chen"},
}


def make_args(**kwargs: object) -> SimpleNamespace:
    return SimpleNamespace(
        banner_value=None,
        banner_fields=None,
        banner_text=None,
        no_banner=False,
        **kwargs,
    )


@pytest.fixture
def schedules_file(tmp_path: Path) -> Path:
    p = tmp_path / "schedules.json"
    p.write_text(json.dumps(VALID_DATA))
    return p


class TestRenderBanner:
    def test_returns_none_when_banner_disabled(self) -> None:
        cfg = BannerConfig(enabled=False)
        result = render_banner(make_args(), cfg, today=date(2026, 4, 13), width=100)
        assert result is None

    def test_returns_none_when_no_banner_overrides(self) -> None:
        cfg = BannerConfig(enabled=True)
        args = make_args(no_banner=True)
        result = render_banner(args, cfg, today=date(2026, 4, 13), width=100)
        assert result is None

    def test_free_text_only_skips_loader(self) -> None:
        cfg = BannerConfig(enabled=False, schedules_path="/nonexistent/path.json")
        args = make_args(banner_value="", banner_text="hello world")
        result = render_banner(args, cfg, today=date(2026, 4, 13), width=100)

        assert result is not None
        assert "hello world" in result
        # No error banner because loader was never called
        assert "unavailable" not in result.lower()

    def test_full_banner_renders_cadence(self, schedules_file: Path) -> None:
        cfg = BannerConfig(
            enabled=True,
            schedules_path=str(schedules_file),
            default_fields=["sprint", "champion"],
        )
        args = make_args(banner_value="")
        result = render_banner(args, cfg, today=date(2026, 4, 13), width=100)

        assert result is not None
        assert "26.Q2.1" in result
        assert "Yocheved" in result

    def test_explicit_fields_override_defaults(self, schedules_file: Path) -> None:
        cfg = BannerConfig(
            enabled=True,
            schedules_path=str(schedules_file),
            default_fields=["sprint", "champion"],
        )
        args = make_args(banner_value="", banner_fields=["dod"])
        result = render_banner(args, cfg, today=date(2026, 4, 13), width=100)

        assert result is not None
        # dod for 2026-04-12 (Sunday) is "chen"
        assert "Chen" in result

    def test_missing_schedule_file_renders_error_banner(self, tmp_path: Path) -> None:
        cfg = BannerConfig(
            enabled=True,
            schedules_path=str(tmp_path / "nope.json"),
        )
        args = make_args(banner_value="")
        result = render_banner(args, cfg, today=date(2026, 4, 13), width=100)

        assert result is not None
        assert "unavailable" in result.lower()
        assert "nope.json" in result

    def test_missing_schedule_with_text_appends_text(self, tmp_path: Path) -> None:
        cfg = BannerConfig(
            enabled=True,
            schedules_path=str(tmp_path / "nope.json"),
        )
        args = make_args(banner_value="", banner_text="welcome back")
        result = render_banner(args, cfg, today=date(2026, 4, 13), width=100)

        assert result is not None
        assert "welcome back" in result
```

- [ ] **Step 7.2: Run test to verify it fails**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_orchestrator.py -v`
Expected: FAIL — `render_banner` not exported from `src.banner`.

- [ ] **Step 7.3: Implement the orchestrator**

Replace `code/python/tools/daily_runner/src/banner/__init__.py` contents:

```python
"""Banner module for daily_runner CLI: cadence info + free text before standup."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Protocol

from src.banner.cadence import current_sprint, dod_for, next_event, sprint_week
from src.banner.errors import BannerError, MalformedScheduleError, MissingScheduleError
from src.banner.renderer import BannerData, render_banner_text, render_error_banner
from src.banner.schedule_loader import load_schedules


class _Args(Protocol):
    banner_value: str | None
    banner_fields: list[str] | None
    banner_text: str | None
    no_banner: bool


def _resolve_intent(args: _Args, config_enabled: bool) -> tuple[bool, list[str] | None, str | None]:
    """Return (banner_on, fields_or_None_for_default, free_text_or_None).

    Banner is ON if any banner-* CLI flag was passed OR config.enabled is True.
    --no-banner overrides everything.
    """
    if getattr(args, "no_banner", False):
        return (False, None, None)

    fields = getattr(args, "banner_fields", None)
    text = getattr(args, "banner_text", None)
    bare_b = getattr(args, "banner_value", None) is not None
    any_flag = bare_b or fields is not None or text is not None
    on = any_flag or config_enabled

    return (on, fields, text)


def _team_member_lookup(sched: Any, key: str | None) -> str | None:
    if not key:
        return None
    if hasattr(sched, "team_members") and key in sched.team_members:
        return key
    return key


def render_banner(
    args: _Args,
    config: Any,
    today: date | None = None,
    width: int | None = None,
) -> str | None:
    """Top-level entrypoint. Returns rendered banner string or None if banner is off.

    Args:
        args: argparse Namespace with banner flags.
        config: BannerConfig instance (enabled, schedules_path, default_fields).
        today: Date used for cadence math; defaults to date.today().
        width: Terminal width override; defaults to rich's autodetected width.
    """
    on, override_fields, free_text = _resolve_intent(args, getattr(config, "enabled", False))
    if not on:
        return None

    if today is None:
        today = date.today()

    if width is None:
        from rich.console import Console
        width = Console().width

    fields = override_fields if override_fields is not None else list(config.default_fields)

    # Free-text-only: skip the loader entirely.
    if not fields and free_text:
        data = BannerData(
            today=today,
            sprint_id=None,
            sprint_week=None,
            champion=None,
            dod=None,
            next_event=None,
            free_text=free_text,
        )
        return render_banner_text(data, width)

    if not fields:
        return None

    # Load schedules.
    schedules_path = getattr(config, "schedules_path", "") or ""
    try:
        sched = load_schedules(Path(schedules_path)) if schedules_path else None
        if sched is None:
            raise MissingScheduleError("")
    except BannerError as exc:
        reason = exc.reason if isinstance(exc, MalformedScheduleError) else str(exc)
        return render_error_banner(
            schedule_path=schedules_path or "(not configured)",
            reason=reason,
            free_text=free_text,
            width=width,
        )

    sprint_id = current_sprint(sched, today) if "sprint" in fields or "sprint_week" in fields else None
    week = sprint_week(sched, sprint_id, today) if sprint_id and "sprint_week" in fields else None
    champion = sched.rotation_schedule[sprint_id].champion if sprint_id and "champion" in fields else None
    dod = dod_for(sched, today) if "dod" in fields else None
    ev = next_event(sched, today) if "next_event" in fields else None

    data = BannerData(
        today=today,
        sprint_id=sprint_id if "sprint" in fields else None,
        sprint_week=week,
        champion=champion,
        dod=dod,
        next_event=ev,
        free_text=free_text,
    )
    return render_banner_text(data, width)


__all__ = ["render_banner"]
```

- [ ] **Step 7.4: Run tests to verify they pass**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_orchestrator.py -v`
Expected: PASS — 7 passed.

- [ ] **Step 7.5: Run all banner tests together**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_*.py -v`
Expected: PASS — all banner tests.

- [ ] **Step 7.6: Commit**

```bash
git add code/python/tools/daily_runner/src/banner/__init__.py \
        code/python/tools/daily_runner/tests/unit/test_banner_orchestrator.py
git commit -m "feat(banner): add orchestrator wiring loader/cadence/renderer"
```

---

## Task 8: CLI flag parsing in main.py

**Files:**
- Modify: `code/python/tools/daily_runner/main.py:167-249`
- Create: `code/python/tools/daily_runner/tests/unit/test_banner_cli.py`

Depends on Task 7.

- [ ] **Step 8.1: Write the failing test**

`code/python/tools/daily_runner/tests/unit/test_banner_cli.py`:

```python
"""Tests for banner CLI flag parsing and disambiguation."""

import argparse

import pytest

from main import _build_parser, _parse_banner_value


class TestParseBannerValue:
    @pytest.mark.parametrize(
        "value, known, expected",
        [
            (None, {"sprint", "dod"}, (None, None)),
            ("", {"sprint", "dod"}, (None, None)),
            ("sprint,dod", {"sprint", "dod"}, (["sprint", "dod"], None)),
            ("sprint", {"sprint", "dod"}, (["sprint"], None)),
            ("welcome back Muhe", {"sprint", "dod"}, (None, "welcome back Muhe")),
            ("hello", {"sprint", "dod"}, (None, "hello")),
            ("sprint,unknown", {"sprint", "dod"}, (None, "sprint,unknown")),
            ("Sprint", {"sprint", "dod"}, (None, "Sprint")),
        ],
    )
    def test_disambiguates(
        self,
        value: str | None,
        known: set[str],
        expected: tuple[list[str] | None, str | None],
    ) -> None:
        assert _parse_banner_value(value, known) == expected


class TestBannerArgs:
    def test_no_banner_flags_default(self) -> None:
        parser = _build_parser()
        args = parser.parse_args([])

        assert args.banner_value is None
        assert args.banner_fields is None
        assert args.banner_text is None
        assert args.no_banner is False

    def test_bare_b_flag(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["-b"])
        assert args.banner_value == ""

    def test_b_with_fields(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["-b", "sprint,dod"])
        assert args.banner_value == "sprint,dod"

    def test_b_with_free_text(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["-b", "welcome back Muhe"])
        assert args.banner_value == "welcome back Muhe"

    def test_explicit_fields_and_text(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(
            ["--banner-fields", "sprint,dod", "--banner-text", "hi"]
        )
        assert args.banner_fields == ["sprint", "dod"]
        assert args.banner_text == "hi"

    def test_no_banner(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["--no-banner"])
        assert args.no_banner is True

    def test_banner_text_only_enables_banner(self) -> None:
        """Without -b, but with --banner-text, banner should still be on."""
        from src.banner import _resolve_intent  # type: ignore[attr-defined]
        parser = _build_parser()
        args = parser.parse_args(["--banner-text", "hi"])
        on, _fields, text = _resolve_intent(args, config_enabled=False)
        assert on is True
        assert text == "hi"
```

- [ ] **Step 8.2: Run test to verify it fails**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_cli.py -v`
Expected: FAIL — `_build_parser` and `_parse_banner_value` not importable from `main`.

- [ ] **Step 8.3: Refactor main.py to expose the parser builder**

Open `code/python/tools/daily_runner/main.py`. Replace lines 167-222 (the `def main()` opening through `args = parser.parse_args()`) with:

```python
KNOWN_BANNER_FIELDS: frozenset[str] = frozenset(
    {"sprint", "sprint_week", "champion", "dod", "next_event"}
)


def _parse_banner_value(
    value: str | None,
    known: frozenset[str] | set[str] = KNOWN_BANNER_FIELDS,
) -> tuple[list[str] | None, str | None]:
    """Disambiguate the value passed to bare `-b VALUE`.

    Returns (fields_list, free_text). Exactly one is non-None, or both None
    when no value is given.
    """
    if value is None or value == "":
        return (None, None)
    if " " in value:
        return (None, value)
    tokens = value.split(",")
    if all(tok in known for tok in tokens):
        return (tokens, None)
    return (None, value)


def _build_parser() -> argparse.ArgumentParser:
    from src import __version__

    parser = argparse.ArgumentParser(
        description="Daily Standup Timer",
        prog="daily-timer",
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["cli", "ui", "history"],
        default="ui",
        help="Mode: 'ui' for Streamlit (default), 'cli' for terminal, 'history' to view past meetings",
    )
    parser.add_argument(
        "--team",
        "-t",
        type=str,
        help="Team ID to use (skips selection menu)",
    )
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default="config.json",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--days",
        "-d",
        type=int,
        default=30,
        help="Number of days to show in history mode (default: 30)",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=20,
        help="Maximum entries to show in history mode (default: 20)",
    )
    parser.add_argument(
        "-b",
        dest="banner_value",
        nargs="?",
        const="",
        default=None,
        help="Show banner; optional VALUE is fields-csv (sprint,dod) or free text.",
    )
    parser.add_argument(
        "--banner-fields",
        type=lambda s: [t.strip() for t in s.split(",") if t.strip()],
        default=None,
        help="Explicit comma-separated cadence fields to show.",
    )
    parser.add_argument(
        "--banner-text",
        type=str,
        default=None,
        help="Free text line shown under the cadence banner.",
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Force banner off, overriding -b and config.",
    )
    return parser


def main() -> int:
    """Main entry point with mode selection."""
    parser = _build_parser()
    args = parser.parse_args()

    # Disambiguate bare `-b VALUE` into fields or text if not already explicit.
    derived_fields, derived_text = _parse_banner_value(args.banner_value, KNOWN_BANNER_FIELDS)
    if args.banner_fields is None:
        args.banner_fields = derived_fields
    if args.banner_text is None:
        args.banner_text = derived_text
```

(Keep the `if args.mode == "history":` block and below unchanged.)

- [ ] **Step 8.4: Run test to verify it passes**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_cli.py -v`
Expected: PASS — 14 passed.

- [ ] **Step 8.5: Verify existing CLI still works**

Run: `cd code/python/tools/daily_runner && python main.py --version`
Expected: prints version, exits 0.

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/ -v`
Expected: all tests still pass.

- [ ] **Step 8.6: Commit**

```bash
git add code/python/tools/daily_runner/main.py \
        code/python/tools/daily_runner/tests/unit/test_banner_cli.py
git commit -m "feat(cli): add -b/--banner-fields/--banner-text/--no-banner flags"
```

---

## Task 9: Wire banner into CLI mode

**Files:**
- Modify: `code/python/tools/daily_runner/main.py` (cli mode block)

Depends on Tasks 7, 8.

- [ ] **Step 9.1: Add print-banner logic to cli mode branch**

In `code/python/tools/daily_runner/main.py`, find the `else:` branch starting `# Run CLI mode`. Modify to print the banner before invoking `cli_main()`. Replace that block with:

```python
    else:
        # Run CLI mode
        from src.banner import render_banner
        from src.cli.app import main as cli_main
        from src.data.config_manager import ConfigManager

        # Load config to access banner section.
        config_mgr = ConfigManager(Path(args.config) if args.config else None)
        app_config = config_mgr.load()
        banner_text = render_banner(args, app_config.banner)
        if banner_text:
            print(banner_text, end="")

        # Reconstruct sys.argv for CLI
        sys.argv = ["daily-timer"]
        if args.team:
            sys.argv.extend(["--team", args.team])
        if args.config != "config.json":
            sys.argv.extend(["--config", args.config])
        if args.verbose:
            sys.argv.append("--verbose")

        return cli_main()
```

- [ ] **Step 9.2: Add a smoke test**

Append to `code/python/tools/daily_runner/tests/unit/test_banner_cli.py`:

```python


class TestBannerInCliMode:
    """Smoke test: -b causes banner output on stdout before cli_main runs."""

    def test_banner_printed_before_cli(
        self,
        tmp_path,
        monkeypatch: pytest.MonkeyPatch,
        capsys,
    ) -> None:
        import json
        from unittest.mock import patch

        # Create example schedule
        sched_path = tmp_path / "schedules.json"
        sched_path.write_text(
            json.dumps(
                {
                    "team_members": {"yocheved": "U1"},
                    "rotation_schedule": {
                        "26.Q2.1": {
                            "champion": "yocheved",
                            "dr": "2026-04-26",
                            "go_nogo": "2026-04-30",
                            "prod": "2026-05-03",
                        },
                    },
                    "dod_schedule": {"2026-04-12": "chen"},
                }
            )
        )

        # Create a minimal config.json pointing at it
        cfg_path = tmp_path / "config.json"
        cfg_path.write_text(
            json.dumps(
                {
                    "version": "1.0",
                    "banner": {
                        "enabled": False,
                        "schedules_path": str(sched_path),
                        "default_fields": ["sprint", "champion"],
                    },
                }
            )
        )

        # Mock cli_main to a no-op returning 0
        with patch("src.cli.app.main", return_value=0):
            monkeypatch.chdir(tmp_path)
            monkeypatch.setattr(
                "sys.argv",
                ["daily-timer", "--mode", "cli", "--config", str(cfg_path), "-b"],
            )
            from main import main as run

            rc = run()

        captured = capsys.readouterr()
        assert rc == 0
        assert "26.Q2.1" in captured.out or "Yocheved" in captured.out
```

- [ ] **Step 9.3: Run the test**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/test_banner_cli.py::TestBannerInCliMode -v`
Expected: PASS.

- [ ] **Step 9.4: Run the full unit suite**

Run: `cd code/python/tools/daily_runner && python -m pytest tests/unit/ -v`
Expected: PASS.

- [ ] **Step 9.5: Manual smoke test**

Create a fake schedules.json + config.json in tmp:

```bash
cd code/python/tools/daily_runner
TMP=$(mktemp -d)
cp config/schedules.example.json $TMP/schedules.json
python -c "
import json
cfg = json.load(open('config.json'))
cfg['banner'] = {'enabled': False, 'schedules_path': '$TMP/schedules.json', 'default_fields': ['sprint','sprint_week','champion','dod','next_event']}
json.dump(cfg, open('$TMP/config.json', 'w'), indent=2)
"
python main.py --mode cli --config $TMP/config.json -b "welcome back Muhe" --team imagine_dragons --help 2>&1 | head -5
```
(The `--help` short-circuits before cli_main runs but verifies the parser accepts the flags.)

Then test the disambiguator:
```bash
python -c "from main import _parse_banner_value, KNOWN_BANNER_FIELDS as K; print(_parse_banner_value('sprint,dod', K)); print(_parse_banner_value('hi friend', K)); print(_parse_banner_value('', K))"
```
Expected: `(['sprint', 'dod'], None)` then `(None, 'hi friend')` then `(None, None)`.

- [ ] **Step 9.6: Commit**

```bash
git add code/python/tools/daily_runner/main.py \
        code/python/tools/daily_runner/tests/unit/test_banner_cli.py
git commit -m "feat(cli): print banner before standup when -b is passed"
```

---

## Task 10: Launcher menu integration

**Files:**
- Modify: `code/bash/tools/launcher/launcher.sh:479-499` (menu) and `:1149-1230` (handler)
- Modify: `code/bash/tools/launcher/CHANGELOG.md`
- Create test: `code/bash/tools/launcher/tests/test_banner_options.sh`

Depends on Task 9.

- [ ] **Step 10.1: Update the menu display function**

In `code/bash/tools/launcher/launcher.sh`, replace the `show_daily_timer_menu()` body (lines 480-498) with:

```bash
show_daily_timer_menu() {
	clear_screen
	echo ""
	echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════╗${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║         ⏱️  DAILY STANDUP TIMER MENU            ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[1]${CYAN}  Start Meeting (CLI)                     ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[2]${CYAN}  Start Meeting (CLI + Banner)            ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[3]${CYAN}  Start Meeting (CLI + Banner + Text)     ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[4]${CYAN}  Start Meeting (Web UI)                  ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[5]${CYAN}  View Meeting History                    ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[6]${CYAN}  View History (Custom Range)            ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║  ${YELLOW}[0]${CYAN}  ← Back to Main Menu                      ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
	echo ""
	printf "  ${BOLD}➜ Enter your choice [0-6]: ${NC}"
}
```

- [ ] **Step 10.2: Update the handler**

In `code/bash/tools/launcher/launcher.sh`, replace the `case "$choice" in` body inside `handle_daily_timer_menu` (the existing options 1-4 plus 0) with:

```bash
		case "$choice" in
		1)
			clear_screen
			echo -e "${CYAN}Starting Daily Standup (CLI mode)...${NC}"
			echo ""
			cd "$DAILY_RUNNER_DIR"
			source "$DAILY_RUNNER_VENV/bin/activate"
			python main.py --mode cli --team imagine_dragons
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		2)
			clear_screen
			echo -e "${CYAN}Starting Daily Standup (CLI + Banner)...${NC}"
			echo ""
			cd "$DAILY_RUNNER_DIR"
			source "$DAILY_RUNNER_VENV/bin/activate"
			python main.py --mode cli --team imagine_dragons -b
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		3)
			clear_screen
			echo -n "Enter banner text: "
			read banner_text
			echo ""
			echo -e "${CYAN}Starting Daily Standup (CLI + Banner + Text)...${NC}"
			echo ""
			cd "$DAILY_RUNNER_DIR"
			source "$DAILY_RUNNER_VENV/bin/activate"
			if [ -z "$banner_text" ]; then
				python main.py --mode cli --team imagine_dragons -b
			else
				python main.py --mode cli --team imagine_dragons --banner-fields sprint,sprint_week,champion,dod,next_event --banner-text "$banner_text"
			fi
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		4)
			clear_screen
			echo -e "${CYAN}Starting Daily Standup (Web UI)...${NC}"
			echo ""
			cd "$DAILY_RUNNER_DIR"
			source "$DAILY_RUNNER_VENV/bin/activate"
			python main.py --mode ui --team imagine_dragons
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		5)
			clear_screen
			echo -e "${CYAN}Meeting History (last 30 days):${NC}"
			echo ""
			cd "$DAILY_RUNNER_DIR"
			source "$DAILY_RUNNER_VENV/bin/activate"
			python main.py --mode history --team imagine_dragons
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		6)
			clear_screen
			echo -n "Enter number of days to show (default 30): "
			read days
			days=${days:-30}
			echo -n "Enter max entries to show (default 20): "
			read limit
			limit=${limit:-20}
			echo ""
			cd "$DAILY_RUNNER_DIR"
			source "$DAILY_RUNNER_VENV/bin/activate"
			python main.py --mode history --team imagine_dragons --days "$days" --limit "$limit"
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		0)
			return
			;;
		*)
			echo -e "${RED}Invalid choice. Please try again.${NC}"
			sleep 1
			;;
		esac
```

- [ ] **Step 10.3: Add launcher test**

`code/bash/tools/launcher/tests/test_banner_options.sh`:

```bash
#!/usr/bin/env bash
# Verifies that the daily timer menu now exposes 6 options and accepts banner choices.

set -e

LAUNCHER="$(cd "$(dirname "$0")/.." && pwd)/launcher.sh"
PASS=0
FAIL=0

assert_grep() {
	local pattern="$1"
	local description="$2"
	if grep -q -F -- "$pattern" "$LAUNCHER"; then
		echo "PASS: $description"
		PASS=$((PASS + 1))
	else
		echo "FAIL: $description (pattern: $pattern)"
		FAIL=$((FAIL + 1))
	fi
}

assert_grep "Start Meeting (CLI + Banner)" "Menu shows CLI + Banner option"
assert_grep "Start Meeting (CLI + Banner + Text)" "Menu shows CLI + Banner + Text option"
assert_grep "Enter your choice [0-6]" "Prompt range updated to 0-6"
assert_grep "main.py --mode cli --team imagine_dragons -b" "Banner option invokes -b"
assert_grep "Enter banner text:" "Banner+Text option prompts for text"
assert_grep "--banner-fields sprint,sprint_week,champion,dod,next_event --banner-text" "Banner+Text option passes both flags"

echo ""
echo "Total: $((PASS + FAIL)) tests, $PASS passed, $FAIL failed"
exit $FAIL
```

Make it executable:
```bash
chmod +x code/bash/tools/launcher/tests/test_banner_options.sh
```

- [ ] **Step 10.4: Run launcher tests**

Run: `bash code/bash/tools/launcher/tests/test_banner_options.sh`
Expected: All 6 PASS, exit 0.

Run: `bash code/bash/tools/launcher/tests/run_all.sh` (if it exists; otherwise run each test_*.sh in the tests dir).
Expected: PASS — no regressions.

- [ ] **Step 10.5: Add CHANGELOG entry**

Read `code/bash/tools/launcher/CHANGELOG.md` and prepend a new section at the top (after any header) with:

```markdown
## Unreleased

### Added
- Daily Timer menu: `[2] Start Meeting (CLI + Banner)` runs the standup with the cadence banner.
- Daily Timer menu: `[3] Start Meeting (CLI + Banner + Text)` prompts for free text and shows it under the banner.
- Renumbered: Web UI is now `[4]`, View History is now `[5]`, View History (Custom Range) is now `[6]`.
```

- [ ] **Step 10.6: Commit**

```bash
git add code/bash/tools/launcher/launcher.sh \
        code/bash/tools/launcher/tests/test_banner_options.sh \
        code/bash/tools/launcher/CHANGELOG.md
git commit -m "feat(launcher): add banner menu options to daily timer"
```

---

## Task 11: Documentation cascade

**Files:**
- Modify: `code/python/tools/daily_runner/README.md`
- Modify (if they reference daily_runner): `code/python/tools/README.md`, `code/python/README.md`, `code/README.md`
- Modify: `code/bash/tools/launcher/README.md`

Independent of Task 10 — can run in parallel.

- [ ] **Step 11.1: Read the existing daily_runner README**

Run: `cat code/python/tools/daily_runner/README.md | head -30`. Note the section style.

- [ ] **Step 11.2: Append a Banner section**

Append to `code/python/tools/daily_runner/README.md`:

```markdown
## Standup Banner

The CLI mode can show a banner with release-cadence context (sprint, week, release champion, Developer on Duty, next DR/prod event) plus an optional free-text greeting before the standup starts.

### Quick start

1. Point at your `schedules.json`:

   ```json
   {
     "banner": {
       "enabled": false,
       "schedules_path": "/absolute/path/to/schedules.json",
       "default_fields": ["sprint", "sprint_week", "champion", "dod", "next_event"]
     }
   }
   ```

2. Run with `-b`:

   ```bash
   python main.py --mode cli -b
   python main.py --mode cli -b sprint,champion,dod
   python main.py --mode cli -b "welcome back Muhe"
   python main.py --mode cli --banner-fields sprint,dod --banner-text "welcome back Muhe"
   python main.py --mode cli --no-banner   # explicit off, even if config enables it
   ```

### Available fields

| Field         | Description                                                      |
| ------------- | ---------------------------------------------------------------- |
| `sprint`      | Current sprint identifier (e.g. `26.Q2.1`)                       |
| `sprint_week` | Week 1, 2, or 3 of the current sprint                            |
| `champion`    | Release ambassador for the current sprint                        |
| `dod`         | Developer on Duty for the current week                           |
| `next_event`  | Closest upcoming DR or Prod release with countdown               |

### Layout adapts to terminal width

- ≥80 cols → full panel
- 40-79 cols → compact panel with shortened labels
- <40 cols → single-line plain text

### If `schedules.json` is missing

The banner shows an inline error explaining how to fix it; the standup continues normally. Two ways to recover:

1. Set `banner.schedules_path` in `config.json` to your real schedules file.
2. Or copy the bundled example: `cp config/schedules.example.json config/schedules.json`.
3. Or run with `--no-banner` to suppress.
```

- [ ] **Step 11.3: Update parent README breadcrumbs**

For each of `code/python/tools/README.md`, `code/python/README.md`, `code/README.md`:

```bash
grep -l "daily_runner\|daily-runner\|Daily Standup" code/README.md code/python/README.md code/python/tools/README.md 2>/dev/null
```

For every file the grep returns, read it and append `(now with optional standup banner showing release cadence)` to the daily_runner mention. If a file doesn't reference daily_runner, leave it alone.

- [ ] **Step 11.4: Update launcher README**

Read `code/bash/tools/launcher/README.md`. Find the daily timer section (search for "Daily" or "DAILY"). Add lines describing the new options:

```markdown
- `[2] Start Meeting (CLI + Banner)` — runs CLI standup with the cadence banner enabled.
- `[3] Start Meeting (CLI + Banner + Text)` — prompts for free text, then runs CLI standup with banner + text.
```

- [ ] **Step 11.5: Commit**

```bash
git add code/python/tools/daily_runner/README.md \
        code/bash/tools/launcher/README.md
# Conditionally add parent READMEs only if they were modified:
git add -u code/README.md code/python/README.md code/python/tools/README.md 2>/dev/null || true
git commit -m "docs(banner): document CLI banner feature across READMEs"
```

---

## Task 12: Coverage gate

**Files:**
- Verify: `code/python/tools/daily_runner/src/banner/`

Independent of Tasks 10, 11 — can run in parallel.

- [ ] **Step 12.1: Run coverage on the banner module**

Run:
```bash
cd code/python/tools/daily_runner
python -m pytest tests/unit/test_banner_*.py --cov=src.banner --cov-report=term-missing -v
```

- [ ] **Step 12.2: Verify ≥90% coverage**

Read the coverage table at the bottom of the output. For each file in `src/banner/`, check that the percentage is ≥90.

- [ ] **Step 12.3: If under 90%, add tests for missing lines**

For any file under 90%, look at the "Missing" column for line numbers, open the file, and add tests covering those branches. Common gaps: edge cases in `_parse_banner_value` for new field names, empty `next_event` in renderer, etc. Repeat 12.1 until ≥90%.

- [ ] **Step 12.4: Commit any added tests**

```bash
git add code/python/tools/daily_runner/tests/unit/test_banner_*.py
git commit -m "test(banner): raise coverage to ≥90%" || echo "no-op: coverage already met"
```

---

## Task 13: End-to-end smoke test

**Files:**
- Create: `code/python/tools/daily_runner/tests/integration/test_banner_e2e.py`

Final task. Depends on all previous.

- [ ] **Step 13.1: Write the E2E test**

`code/python/tools/daily_runner/tests/integration/test_banner_e2e.py`:

```python
"""End-to-end test: real example schedule, all CLI variants render."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

DAILY_RUNNER_DIR = Path(__file__).resolve().parents[2]


@pytest.fixture
def cfg_with_example_schedule(tmp_path: Path) -> Path:
    schedules_src = DAILY_RUNNER_DIR / "config" / "schedules.example.json"
    schedules_dst = tmp_path / "schedules.json"
    schedules_dst.write_text(schedules_src.read_text())

    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(
        json.dumps(
            {
                "version": "1.0",
                "banner": {
                    "enabled": False,
                    "schedules_path": str(schedules_dst),
                    "default_fields": [
                        "sprint",
                        "sprint_week",
                        "champion",
                        "dod",
                        "next_event",
                    ],
                },
            }
        )
    )
    return cfg_path


def _run(cfg: Path, *extra_args: str, timeout: int = 10) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    return subprocess.run(
        [
            sys.executable,
            "main.py",
            "--mode",
            "cli",
            "--config",
            str(cfg),
            "--team",
            "imagine_dragons",
            *extra_args,
        ],
        capture_output=True,
        text=True,
        cwd=DAILY_RUNNER_DIR,
        env=env,
        timeout=timeout,
        # We expect cli mode to fail without a real team setup, but the banner
        # should already have printed before the failure.
        check=False,
    )


def test_bare_b_prints_banner(cfg_with_example_schedule: Path) -> None:
    proc = _run(cfg_with_example_schedule, "-b")
    assert "26.Q1" in proc.stdout or "26.Q2" in proc.stdout

def test_b_with_text_prints_text(cfg_with_example_schedule: Path) -> None:
    proc = _run(cfg_with_example_schedule, "-b", "welcome back Muhe")
    assert "welcome back Muhe" in proc.stdout

def test_no_banner_suppresses_output(cfg_with_example_schedule: Path) -> None:
    proc = _run(cfg_with_example_schedule, "--no-banner")
    assert "26.Q1" not in proc.stdout
    assert "26.Q2" not in proc.stdout

def test_explicit_fields_and_text(cfg_with_example_schedule: Path) -> None:
    proc = _run(
        cfg_with_example_schedule,
        "--banner-fields",
        "sprint,dod",
        "--banner-text",
        "hello team",
    )
    assert "hello team" in proc.stdout

def test_missing_schedule_error_banner(tmp_path: Path) -> None:
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(
        json.dumps(
            {
                "version": "1.0",
                "banner": {
                    "enabled": False,
                    "schedules_path": "/definitely/does/not/exist.json",
                    "default_fields": ["sprint"],
                },
            }
        )
    )
    proc = _run(cfg_path, "-b")
    assert "unavailable" in proc.stdout.lower()
    assert "definitely/does/not/exist.json" in proc.stdout
```

- [ ] **Step 13.2: Run the E2E tests**

Run:
```bash
cd code/python/tools/daily_runner && python -m pytest tests/integration/test_banner_e2e.py -v
```
Expected: 5 passed.

- [ ] **Step 13.3: Commit**

```bash
git add code/python/tools/daily_runner/tests/integration/test_banner_e2e.py
git commit -m "test(banner): add E2E tests across all CLI variants"
```

---

## Parallel execution map

For the subagent-driven runner, the dependency graph is:

```
            ┌── Task 1 (errors)
            ├── Task 2 (models)         ─┐
Phase 1 ────┼── Task 3 (loader)          │
            ├── Task 4 (cadence)         │
            ├── Task 5 (renderer)        │
            └── Task 6 (config schema)  ─┘
                          │
                          ▼
Phase 2 ────────── Task 7 (orchestrator)
                          │
                          ▼
Phase 2 ────────── Task 8 (CLI parser)
                          │
                          ▼
Phase 2 ────────── Task 9 (CLI wiring)
                          │
                          ├── Task 10 (launcher)
Phase 3 ──────────────────┼── Task 11 (docs)
                          └── Task 12 (coverage)
                          │
                          ▼
Phase 4 ────────── Task 13 (E2E)
```

**Phase 1** (5-6 parallel agents): Tasks 1, 2, 3, 4, 5, 6 are file-disjoint and can run in parallel.
**Phase 2** (sequential): Tasks 7 → 8 → 9 must run in order (each depends on the previous).
**Phase 3** (3 parallel agents): Tasks 10, 11, 12 are file-disjoint.
**Phase 4** (single agent): Task 13.

**Important caveat for parallel runners:** Task 3 imports from Task 1 (errors) and Task 2 (models); if you run them as truly parallel agents, they MUST share a working tree, OR the runner must merge their outputs before Task 3 starts. Recommended approach: run them as parallel **subagents in the same worktree** (write-isolated by file path), not as parallel git branches.
