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

    def test_parses_with_sprints_table(self) -> None:
        from datetime import date
        data = {
            "team_members": {},
            "rotation_schedule": {
                "26.Q2.1": {
                    "champion": "alice",
                    "dr": "2026-04-26",
                    "go_nogo": "2026-04-30",
                    "prod": "2026-05-03",
                },
            },
            "dod_schedule": {},
            "sprints": {
                "26.Q2.1": {"start": "2026-03-29", "end": "2026-04-18"},
            },
        }
        sched = Schedules.model_validate(data)
        assert sched.sprints["26.Q2.1"].start == date(2026, 3, 29)
        assert sched.sprints["26.Q2.1"].end == date(2026, 4, 18)

    def test_sprints_default_to_empty_dict(self) -> None:
        # Backward compat: schedules without `sprints` still parse.
        data = {
            "team_members": {},
            "rotation_schedule": {},
            "dod_schedule": {},
        }
        sched = Schedules.model_validate(data)
        assert sched.sprints == {}
