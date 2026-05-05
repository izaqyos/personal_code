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


def _sprint_start_for(sched: Schedules, sprint_id: str) -> date:
    """Sprint start date: explicit `sprints` table when present, else DR - 14."""
    if sprint_id in sched.sprints:
        return sched.sprints[sprint_id].start
    return sched.rotation_schedule[sprint_id].dr - timedelta(days=SPRINT_START_OFFSET_FROM_DR)


def _sorted_sprint_ids(sched: Schedules) -> list[str]:
    return sorted(sched.rotation_schedule.keys(), key=lambda k: sched.rotation_schedule[k].dr)


def current_sprint(sched: Schedules, today: date) -> str | None:
    ids = _sorted_sprint_ids(sched)
    if not ids:
        return None

    earliest_start = _sprint_start_for(sched, ids[0])
    if today < earliest_start:
        return ids[0]

    current = ids[0]
    for sprint_id in ids:
        start = _sprint_start_for(sched, sprint_id)
        if today >= start:
            current = sprint_id
        else:
            break
    return current


def sprint_week(sched: Schedules, sprint_id: str, today: date) -> int:
    start = _sprint_start_for(sched, sprint_id)
    delta_days = (today - start).days
    week = delta_days // 7 + 1
    return max(1, min(3, week))


def _sunday_of(d: date) -> date:
    """Return the Sunday on or before `d`."""
    # weekday(): Mon=0..Sat=5, Sun=6 → days since Sunday: Mon=1..Sat=6, Sun=0
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
