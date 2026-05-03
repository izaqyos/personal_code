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
