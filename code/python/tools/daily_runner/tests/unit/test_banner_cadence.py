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
from src.banner.models import Schedules


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
                    "dr": "2026-05-10",
                    "go_nogo": "2026-05-14",
                    "prod": "2026-05-17",
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


def make_schedules_with_sprint_table() -> Schedules:
    """Same data + explicit sprints table from SoT."""
    base = make_schedules().model_dump(mode="json")
    base["sprints"] = {
        "26.Q1.4": {"start": "2026-03-08", "end": "2026-03-28"},
        "26.Q2.1": {"start": "2026-03-29", "end": "2026-04-18"},
        "26.Q2.2": {"start": "2026-04-19", "end": "2026-05-09"},
    }
    return Schedules.model_validate(base)


class TestCurrentSprint:
    @pytest.mark.parametrize(
        "today, expected",
        [
            (date(2026, 4, 13), "26.Q2.1"),  # mid-sprint (start = 4-12)
            (date(2026, 4, 12), "26.Q2.1"),  # sprint start day
            (date(2026, 4, 25), "26.Q2.1"),  # last day before next sprint (Q2.2 start = 4-26)
            (date(2026, 5, 2), "26.Q2.2"),   # in Q2.2 (start = 4-26 with DR=5-10)
            (date(2026, 5, 3), "26.Q2.2"),   # in Q2.2
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
        assert result == NextEvent(label="DR", target=date(2026, 5, 10), days_until=6)

    def test_returns_none_when_no_future_events(self) -> None:
        sched = make_schedules()
        assert next_event(sched, date(2030, 1, 1)) is None


class TestSprintTablePath:
    """When `sprints` table is present, it should override the DR-14 heuristic."""

    def test_current_sprint_uses_table_window(self) -> None:
        sched = make_schedules_with_sprint_table()
        # Apr 19 (Sprint #2 start per SoT-like table)
        assert current_sprint(sched, date(2026, 4, 19)) == "26.Q2.2"
        # May 4 (in Sprint #2 week 3 per SoT)
        assert current_sprint(sched, date(2026, 5, 4)) == "26.Q2.2"
        # May 9 (last day of Sprint #2)
        assert current_sprint(sched, date(2026, 5, 9)) == "26.Q2.2"

    def test_sprint_week_uses_table_start(self) -> None:
        sched = make_schedules_with_sprint_table()
        # Sprint #2 starts Apr 19. May 4 = day 16 → week 3.
        assert sprint_week(sched, "26.Q2.2", date(2026, 5, 4)) == 3

    def test_falls_back_to_heuristic_when_sprint_missing_from_table(self) -> None:
        """If sprints table exists but doesn't include this sprint_id, fall back to DR-14."""
        sched = make_schedules_with_sprint_table()
        # 26.Q1.4 IS in the table — let's test one that WOULD fall back.
        # Construct a schedule where rotation_schedule has an extra sprint not in sprints table.
        from src.banner.models import RotationEntry
        sched.rotation_schedule["26.Q3.1"] = RotationEntry(
            champion="x", dr=date(2026, 7, 1), go_nogo=date(2026, 7, 5), prod=date(2026, 7, 8)
        )
        # Sprint Q3.1 not in sprints table → fallback to DR-14 = Jun 17
        assert sprint_week(sched, "26.Q3.1", date(2026, 6, 17)) == 1
        assert sprint_week(sched, "26.Q3.1", date(2026, 6, 24)) == 2
