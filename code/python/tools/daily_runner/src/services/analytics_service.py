"""
Analytics service for meeting statistics and insights.

This module provides statistical analysis of meeting history data,
including duration trends, per-person stats, and attendance metrics.
"""

import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from src.core.models import MeetingRecord, ParticipantStatus
from src.data.history_repository import HistoryRepository

logger = logging.getLogger(__name__)


@dataclass
class SummaryStats:
    """Overall meeting statistics."""

    total_meetings: int = 0
    total_duration_seconds: float = 0.0
    avg_duration_seconds: float = 0.0
    total_overtime_seconds: float = 0.0
    avg_overtime_seconds: float = 0.0
    total_participants: int = 0
    avg_participants_per_meeting: float = 0.0
    on_time_rate: float = 0.0  # Percentage of meetings that finished on time


@dataclass
class PersonStats:
    """Statistics for an individual team member."""

    member_id: str
    display_name: str
    total_meetings: int = 0
    total_time_seconds: float = 0.0
    avg_time_seconds: float = 0.0
    total_overtime_seconds: float = 0.0
    avg_overtime_seconds: float = 0.0
    times_absent: int = 0
    times_skipped: int = 0
    attendance_rate: float = 0.0


@dataclass
class DurationTrendPoint:
    """A single data point in the duration trend."""

    date: str  # YYYY-MM-DD
    meeting_count: int = 0
    total_duration_seconds: float = 0.0
    avg_duration_seconds: float = 0.0


@dataclass
class OvertimeEntry:
    """Entry in the overtime leaderboard."""

    member_id: str
    display_name: str
    total_overtime_seconds: float = 0.0
    overtime_count: int = 0
    avg_overtime_seconds: float = 0.0


@dataclass
class AttendanceStats:
    """Attendance statistics."""

    total_possible_attendances: int = 0
    total_present: int = 0
    total_absent: int = 0
    total_skipped: int = 0
    overall_attendance_rate: float = 0.0
    per_person: dict[str, dict[str, float]] = field(default_factory=dict)


class AnalyticsService:
    """
    Service for analyzing meeting history data.

    Provides various statistical queries over meeting records
    including summary stats, per-person breakdowns, trends,
    and attendance metrics.
    """

    def __init__(self, history_repo: HistoryRepository) -> None:
        """
        Initialize the analytics service.

        Args:
            history_repo: Repository for accessing meeting history.
        """
        self._history_repo = history_repo

    def _get_date_range(self, days: int) -> tuple[str, str]:
        """
        Calculate start and end dates for a given number of days.

        Args:
            days: Number of days to look back.

        Returns:
            Tuple of (start_date, end_date) in YYYY-MM-DD format.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        return (
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
        )

    def _get_filtered_entries(self, days: int | None = None) -> list[MeetingRecord]:
        """
        Get meeting entries with optional day filter.

        Args:
            days: Number of days to look back (None for all).

        Returns:
            List of matching meeting records.
        """
        if days is None:
            return self._history_repo.get_entries()

        start_date, end_date = self._get_date_range(days)
        return self._history_repo.get_entries(start_date=start_date, end_date=end_date)

    def get_summary_stats(self, days: int = 30) -> SummaryStats:
        """
        Get overall meeting statistics.

        Args:
            days: Number of days to analyze.

        Returns:
            SummaryStats with aggregated metrics.
        """
        entries = self._get_filtered_entries(days)

        if not entries:
            return SummaryStats()

        total_duration = sum(e.total_duration_seconds for e in entries)
        total_overtime = sum(
            sum(p.overtime_seconds for p in e.participants)
            for e in entries
        )
        total_participants = sum(
            len([p for p in e.participants if p.status == ParticipantStatus.PRESENT])
            for e in entries
        )

        # Calculate on-time rate (meetings where total duration <= expected)
        on_time_count = sum(
            1 for e in entries
            if e.total_duration_seconds <= e.expected_duration_seconds
        )

        return SummaryStats(
            total_meetings=len(entries),
            total_duration_seconds=total_duration,
            avg_duration_seconds=total_duration / len(entries),
            total_overtime_seconds=total_overtime,
            avg_overtime_seconds=total_overtime / len(entries) if entries else 0.0,
            total_participants=total_participants,
            avg_participants_per_meeting=total_participants / len(entries),
            on_time_rate=on_time_count / len(entries) if entries else 0.0,
        )

    def get_per_person_stats(self, days: int = 30) -> list[PersonStats]:
        """
        Get statistics broken down by team member.

        Args:
            days: Number of days to analyze.

        Returns:
            List of PersonStats for each participant.
        """
        entries = self._get_filtered_entries(days)

        if not entries:
            return []

        # Aggregate stats per person
        person_data: dict[str, dict[str, float | int | str]] = defaultdict(
            lambda: {
                "display_name": "",
                "total_meetings": 0,
                "total_time": 0.0,
                "total_overtime": 0.0,
                "times_absent": 0,
                "times_skipped": 0,
                "possible_meetings": 0,
            }
        )

        for entry in entries:
            for participant in entry.participants:
                data = person_data[participant.member_id]
                data["display_name"] = participant.display_name
                data["possible_meetings"] = int(data["possible_meetings"]) + 1

                if participant.status == ParticipantStatus.PRESENT:
                    data["total_meetings"] = int(data["total_meetings"]) + 1
                    data["total_time"] = float(data["total_time"]) + participant.actual_time_seconds
                    data["total_overtime"] = float(data["total_overtime"]) + participant.overtime_seconds
                elif participant.status == ParticipantStatus.ABSENT:
                    data["times_absent"] = int(data["times_absent"]) + 1
                elif participant.status == ParticipantStatus.SKIPPED:
                    data["times_skipped"] = int(data["times_skipped"]) + 1

        # Build result list
        results = []
        for member_id, data in person_data.items():
            total_meetings = int(data["total_meetings"])
            possible_meetings = int(data["possible_meetings"])
            total_time = float(data["total_time"])
            total_overtime = float(data["total_overtime"])

            results.append(PersonStats(
                member_id=member_id,
                display_name=str(data["display_name"]),
                total_meetings=total_meetings,
                total_time_seconds=total_time,
                avg_time_seconds=total_time / total_meetings if total_meetings > 0 else 0.0,
                total_overtime_seconds=total_overtime,
                avg_overtime_seconds=total_overtime / total_meetings if total_meetings > 0 else 0.0,
                times_absent=int(data["times_absent"]),
                times_skipped=int(data["times_skipped"]),
                attendance_rate=total_meetings / possible_meetings if possible_meetings > 0 else 0.0,
            ))

        # Sort by total meetings descending
        results.sort(key=lambda x: x.total_meetings, reverse=True)
        return results

    def get_duration_trend(self, days: int = 30) -> list[DurationTrendPoint]:
        """
        Get duration trend data as daily aggregates.

        Args:
            days: Number of days to analyze.

        Returns:
            List of DurationTrendPoint ordered by date.
        """
        entries = self._get_filtered_entries(days)

        if not entries:
            return []

        # Aggregate by date
        daily_data: dict[str, dict[str, float | int]] = defaultdict(
            lambda: {"count": 0, "total_duration": 0.0}
        )

        for entry in entries:
            data = daily_data[entry.date]
            data["count"] = int(data["count"]) + 1
            data["total_duration"] = float(data["total_duration"]) + entry.total_duration_seconds

        # Build result list
        results = []
        for date, data in sorted(daily_data.items()):
            count = int(data["count"])
            total = float(data["total_duration"])
            results.append(DurationTrendPoint(
                date=date,
                meeting_count=count,
                total_duration_seconds=total,
                avg_duration_seconds=total / count if count > 0 else 0.0,
            ))

        return results

    def get_overtime_leaderboard(self, limit: int = 5, days: int = 30) -> list[OvertimeEntry]:
        """
        Get the top overtime offenders.

        Args:
            limit: Maximum number of entries to return.
            days: Number of days to analyze.

        Returns:
            List of OvertimeEntry sorted by total overtime descending.
        """
        entries = self._get_filtered_entries(days)

        if not entries:
            return []

        # Aggregate overtime per person
        overtime_data: dict[str, dict[str, float | int | str]] = defaultdict(
            lambda: {
                "display_name": "",
                "total_overtime": 0.0,
                "overtime_count": 0,
            }
        )

        for entry in entries:
            for participant in entry.participants:
                if participant.overtime_seconds > 0:
                    data = overtime_data[participant.member_id]
                    data["display_name"] = participant.display_name
                    data["total_overtime"] = float(data["total_overtime"]) + participant.overtime_seconds
                    data["overtime_count"] = int(data["overtime_count"]) + 1

        # Build and sort results
        results = []
        for member_id, data in overtime_data.items():
            total_overtime = float(data["total_overtime"])
            overtime_count = int(data["overtime_count"])
            results.append(OvertimeEntry(
                member_id=member_id,
                display_name=str(data["display_name"]),
                total_overtime_seconds=total_overtime,
                overtime_count=overtime_count,
                avg_overtime_seconds=total_overtime / overtime_count if overtime_count > 0 else 0.0,
            ))

        # Sort by total overtime descending and limit
        results.sort(key=lambda x: x.total_overtime_seconds, reverse=True)
        return results[:limit]

    def get_attendance_stats(self, days: int = 30) -> AttendanceStats:
        """
        Get attendance statistics.

        Args:
            days: Number of days to analyze.

        Returns:
            AttendanceStats with overall and per-person rates.
        """
        entries = self._get_filtered_entries(days)

        if not entries:
            return AttendanceStats()

        total_possible = 0
        total_present = 0
        total_absent = 0
        total_skipped = 0

        # Per-person attendance
        person_attendance: dict[str, dict[str, int | str]] = defaultdict(
            lambda: {"display_name": "", "present": 0, "possible": 0}
        )

        for entry in entries:
            for participant in entry.participants:
                total_possible += 1
                person_attendance[participant.member_id]["display_name"] = participant.display_name
                person_attendance[participant.member_id]["possible"] = int(
                    person_attendance[participant.member_id]["possible"]
                ) + 1

                if participant.status == ParticipantStatus.PRESENT:
                    total_present += 1
                    person_attendance[participant.member_id]["present"] = int(
                        person_attendance[participant.member_id]["present"]
                    ) + 1
                elif participant.status == ParticipantStatus.ABSENT:
                    total_absent += 1
                elif participant.status == ParticipantStatus.SKIPPED:
                    total_skipped += 1

        # Calculate per-person rates
        per_person: dict[str, dict[str, float]] = {}
        for member_id, data in person_attendance.items():
            present = int(data["present"])
            possible = int(data["possible"])
            per_person[member_id] = {
                "attendance_rate": present / possible if possible > 0 else 0.0,
                "meetings_attended": float(present),
                "meetings_possible": float(possible),
            }

        return AttendanceStats(
            total_possible_attendances=total_possible,
            total_present=total_present,
            total_absent=total_absent,
            total_skipped=total_skipped,
            overall_attendance_rate=total_present / total_possible if total_possible > 0 else 0.0,
            per_person=per_person,
        )

    def calculate_on_time_rate(self, days: int | None = None) -> float:
        """
        Calculate the percentage of meetings that finished on time.

        A meeting is considered "on time" if total_duration <= expected_duration.

        Args:
            days: Number of days to analyze (None for all time).

        Returns:
            Percentage as a float between 0.0 and 1.0.
        """
        entries = self._get_filtered_entries(days)

        if not entries:
            return 0.0

        on_time_count = sum(
            1 for e in entries
            if e.total_duration_seconds <= e.expected_duration_seconds
        )

        return on_time_count / len(entries)
