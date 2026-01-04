"""
Unit tests for the Analytics Service.

Test coverage for Phase 7:
- 7.T1: Average duration calculated correctly
- 7.T2: Per-person stats aggregate properly
- 7.T3: Trend data points match date range
- 7.T4: Overtime leaderboard sorted correctly
- 7.T5: Empty history returns zero/empty stats
- 7.T6: Date filtering works correctly
- 7.T7: Attendance percentage calculated correctly
"""

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from src.core.models import (
    MeetingRecord,
    MeetingStatus,
    ParticipantRecord,
    ParticipantStatus,
)
from src.data.history_repository import HistoryRepository
from src.services.analytics_service import (
    AnalyticsService,
    AttendanceStats,
    DurationTrendPoint,
    OvertimeEntry,
    PersonStats,
    SummaryStats,
)

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def temp_data_dir(tmp_path: Path) -> Path:
    """Create a temporary data directory."""
    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


@pytest.fixture
def empty_history_repo(temp_data_dir: Path) -> HistoryRepository:
    """Create a history repository with no entries."""
    repo = HistoryRepository(team_id="test_team", data_dir=temp_data_dir)
    repo.load()
    return repo


def create_sample_meeting_records() -> list[MeetingRecord]:
    """Create sample meeting records for testing."""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)

    return [
        MeetingRecord(
            id=f"{two_days_ago.strftime('%Y-%m-%dT')}09:00:00",
            date=two_days_ago.strftime("%Y-%m-%d"),
            start_time="09:00:00",
            end_time="09:12:00",
            total_duration_seconds=720.0,  # 12 minutes
            expected_duration_seconds=900,  # 15 minutes
            status=MeetingStatus.COMPLETED,
            team_id="test_team",
            participants=[
                ParticipantRecord(
                    member_id="alice",
                    display_name="Alice",
                    status=ParticipantStatus.PRESENT,
                    allocated_time_seconds=180,
                    actual_time_seconds=160.0,
                    overtime_seconds=0.0,
                    order_position=1,
                ),
                ParticipantRecord(
                    member_id="bob",
                    display_name="Bob",
                    status=ParticipantStatus.PRESENT,
                    allocated_time_seconds=180,
                    actual_time_seconds=200.0,
                    overtime_seconds=20.0,
                    order_position=2,
                ),
                ParticipantRecord(
                    member_id="charlie",
                    display_name="Charlie",
                    status=ParticipantStatus.ABSENT,
                    allocated_time_seconds=180,
                    actual_time_seconds=0.0,
                    overtime_seconds=0.0,
                    order_position=3,
                ),
            ],
        ),
        MeetingRecord(
            id=f"{yesterday.strftime('%Y-%m-%dT')}09:00:00",
            date=yesterday.strftime("%Y-%m-%d"),
            start_time="09:00:00",
            end_time="09:18:00",
            total_duration_seconds=1080.0,  # 18 minutes
            expected_duration_seconds=900,  # 15 minutes - OVERTIME
            status=MeetingStatus.COMPLETED,
            team_id="test_team",
            participants=[
                ParticipantRecord(
                    member_id="alice",
                    display_name="Alice",
                    status=ParticipantStatus.PRESENT,
                    allocated_time_seconds=180,
                    actual_time_seconds=180.0,
                    overtime_seconds=0.0,
                    order_position=1,
                ),
                ParticipantRecord(
                    member_id="bob",
                    display_name="Bob",
                    status=ParticipantStatus.PRESENT,
                    allocated_time_seconds=180,
                    actual_time_seconds=240.0,
                    overtime_seconds=60.0,
                    order_position=2,
                ),
                ParticipantRecord(
                    member_id="charlie",
                    display_name="Charlie",
                    status=ParticipantStatus.SKIPPED,
                    allocated_time_seconds=180,
                    actual_time_seconds=0.0,
                    overtime_seconds=0.0,
                    order_position=3,
                ),
            ],
        ),
        MeetingRecord(
            id=f"{today.strftime('%Y-%m-%dT')}09:00:00",
            date=today.strftime("%Y-%m-%d"),
            start_time="09:00:00",
            end_time="09:10:00",
            total_duration_seconds=600.0,  # 10 minutes
            expected_duration_seconds=900,  # 15 minutes - ON TIME
            status=MeetingStatus.COMPLETED,
            team_id="test_team",
            participants=[
                ParticipantRecord(
                    member_id="alice",
                    display_name="Alice",
                    status=ParticipantStatus.PRESENT,
                    allocated_time_seconds=180,
                    actual_time_seconds=150.0,
                    overtime_seconds=0.0,
                    order_position=1,
                ),
                ParticipantRecord(
                    member_id="bob",
                    display_name="Bob",
                    status=ParticipantStatus.PRESENT,
                    allocated_time_seconds=180,
                    actual_time_seconds=150.0,
                    overtime_seconds=0.0,
                    order_position=2,
                ),
                ParticipantRecord(
                    member_id="charlie",
                    display_name="Charlie",
                    status=ParticipantStatus.PRESENT,
                    allocated_time_seconds=180,
                    actual_time_seconds=150.0,
                    overtime_seconds=0.0,
                    order_position=3,
                ),
            ],
        ),
    ]


@pytest.fixture
def history_repo_with_data(temp_data_dir: Path) -> HistoryRepository:
    """Create a history repository with sample data."""
    repo = HistoryRepository(team_id="test_team", data_dir=temp_data_dir)
    repo.load()

    # Add sample records using the repository's save method
    for record in create_sample_meeting_records():
        repo.save_entry(record)

    return repo


@pytest.fixture
def analytics_service(history_repo_with_data: HistoryRepository) -> AnalyticsService:
    """Create an analytics service with sample data."""
    return AnalyticsService(history_repo_with_data)


@pytest.fixture
def empty_analytics_service(empty_history_repo: HistoryRepository) -> AnalyticsService:
    """Create an analytics service with no data."""
    return AnalyticsService(empty_history_repo)


# =============================================================================
# Test 7.T1: Average Duration Calculated Correctly
# =============================================================================


class TestAverageDuration:
    """Test 7.T1: Average duration calculated correctly."""

    def test_summary_stats_avg_duration(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Average duration should be calculated correctly."""
        stats = analytics_service.get_summary_stats(days=30)

        # Total duration: 720 + 1080 + 600 = 2400
        # Average: 2400 / 3 = 800
        assert stats.total_meetings == 3
        assert stats.total_duration_seconds == 2400.0
        assert stats.avg_duration_seconds == 800.0

    def test_summary_stats_total_overtime(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Total overtime should aggregate correctly."""
        stats = analytics_service.get_summary_stats(days=30)

        # Total overtime: 0+20+0 + 0+60+0 + 0+0+0 = 80
        assert stats.total_overtime_seconds == 80.0
        assert abs(stats.avg_overtime_seconds - 80.0 / 3) < 0.01

    def test_summary_stats_on_time_rate(
        self, analytics_service: AnalyticsService
    ) -> None:
        """On-time rate should be calculated correctly."""
        stats = analytics_service.get_summary_stats(days=30)

        # Meeting 1: 720 <= 900 (on time)
        # Meeting 2: 1080 > 900 (overtime)
        # Meeting 3: 600 <= 900 (on time)
        # Rate: 2/3 = 0.666...
        assert abs(stats.on_time_rate - 2 / 3) < 0.01


# =============================================================================
# Test 7.T2: Per-Person Stats Aggregate Properly
# =============================================================================


class TestPerPersonStats:
    """Test 7.T2: Per-person stats aggregate properly."""

    def test_per_person_returns_all_members(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Should return stats for all participants."""
        stats = analytics_service.get_per_person_stats(days=30)

        member_ids = {s.member_id for s in stats}
        assert member_ids == {"alice", "bob", "charlie"}

    def test_per_person_meeting_count(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Meeting counts should be accurate per person."""
        stats = analytics_service.get_per_person_stats(days=30)
        stats_by_id = {s.member_id: s for s in stats}

        # Alice: present in all 3
        assert stats_by_id["alice"].total_meetings == 3
        # Bob: present in all 3
        assert stats_by_id["bob"].total_meetings == 3
        # Charlie: absent in 1, skipped in 1, present in 1
        assert stats_by_id["charlie"].total_meetings == 1

    def test_per_person_time_aggregation(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Total time should aggregate correctly per person."""
        stats = analytics_service.get_per_person_stats(days=30)
        stats_by_id = {s.member_id: s for s in stats}

        # Alice: 160 + 180 + 150 = 490
        assert stats_by_id["alice"].total_time_seconds == 490.0
        # Bob: 200 + 240 + 150 = 590
        assert stats_by_id["bob"].total_time_seconds == 590.0

    def test_per_person_overtime_aggregation(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Overtime should aggregate correctly per person."""
        stats = analytics_service.get_per_person_stats(days=30)
        stats_by_id = {s.member_id: s for s in stats}

        # Alice: 0
        assert stats_by_id["alice"].total_overtime_seconds == 0.0
        # Bob: 20 + 60 + 0 = 80
        assert stats_by_id["bob"].total_overtime_seconds == 80.0

    def test_per_person_absence_tracking(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Absences should be tracked correctly."""
        stats = analytics_service.get_per_person_stats(days=30)
        stats_by_id = {s.member_id: s for s in stats}

        # Charlie: 1 absent, 1 skipped
        assert stats_by_id["charlie"].times_absent == 1
        assert stats_by_id["charlie"].times_skipped == 1

    def test_per_person_sorted_by_meetings(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Results should be sorted by total meetings descending."""
        stats = analytics_service.get_per_person_stats(days=30)

        # First two (alice, bob) have 3 meetings, charlie has 1
        assert stats[0].total_meetings >= stats[1].total_meetings
        assert stats[1].total_meetings >= stats[2].total_meetings


# =============================================================================
# Test 7.T3: Trend Data Points Match Date Range
# =============================================================================


class TestDurationTrend:
    """Test 7.T3: Trend data points match date range."""

    def test_trend_returns_daily_points(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Should return one data point per day with meetings."""
        trend = analytics_service.get_duration_trend(days=30)

        # We have 3 meetings on 3 different days
        assert len(trend) == 3

    def test_trend_sorted_by_date(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Trend points should be sorted chronologically."""
        trend = analytics_service.get_duration_trend(days=30)

        dates = [t.date for t in trend]
        assert dates == sorted(dates)

    def test_trend_meeting_count_per_day(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Each day should show correct meeting count."""
        trend = analytics_service.get_duration_trend(days=30)

        # All days have exactly 1 meeting
        for point in trend:
            assert point.meeting_count == 1

    def test_trend_duration_per_day(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Duration should match the meeting for that day."""
        trend = analytics_service.get_duration_trend(days=30)

        # Day 1 (oldest): 720
        # Day 2: 1080
        # Day 3 (today): 600
        assert trend[0].total_duration_seconds == 720.0
        assert trend[1].total_duration_seconds == 1080.0
        assert trend[2].total_duration_seconds == 600.0

    def test_trend_avg_equals_total_for_single_meeting(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Average should equal total when only one meeting per day."""
        trend = analytics_service.get_duration_trend(days=30)

        for point in trend:
            assert point.avg_duration_seconds == point.total_duration_seconds


# =============================================================================
# Test 7.T4: Overtime Leaderboard Sorted Correctly
# =============================================================================


class TestOvertimeLeaderboard:
    """Test 7.T4: Overtime leaderboard sorted correctly."""

    def test_leaderboard_sorted_by_total_overtime(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Leaderboard should be sorted by total overtime descending."""
        leaderboard = analytics_service.get_overtime_leaderboard(limit=10, days=30)

        # Bob has 80 seconds overtime, Alice has 0
        assert len(leaderboard) == 1  # Only Bob has overtime
        assert leaderboard[0].member_id == "bob"
        assert leaderboard[0].total_overtime_seconds == 80.0

    def test_leaderboard_respects_limit(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Leaderboard should respect the limit parameter."""
        leaderboard = analytics_service.get_overtime_leaderboard(limit=1, days=30)

        assert len(leaderboard) <= 1

    def test_leaderboard_overtime_count(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Should track number of overtime occurrences."""
        leaderboard = analytics_service.get_overtime_leaderboard(limit=10, days=30)

        # Bob went overtime in 2 meetings
        bob_entry = leaderboard[0]
        assert bob_entry.overtime_count == 2

    def test_leaderboard_avg_overtime(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Average overtime should be calculated correctly."""
        leaderboard = analytics_service.get_overtime_leaderboard(limit=10, days=30)

        # Bob: 80 total / 2 occurrences = 40 avg
        bob_entry = leaderboard[0]
        assert bob_entry.avg_overtime_seconds == 40.0


# =============================================================================
# Test 7.T5: Empty History Returns Zero/Empty Stats
# =============================================================================


class TestEmptyHistory:
    """Test 7.T5: Empty history returns zero/empty stats."""

    def test_summary_stats_empty(
        self, empty_analytics_service: AnalyticsService
    ) -> None:
        """Summary stats should be zero with empty history."""
        stats = empty_analytics_service.get_summary_stats(days=30)

        assert stats.total_meetings == 0
        assert stats.total_duration_seconds == 0.0
        assert stats.avg_duration_seconds == 0.0
        assert stats.on_time_rate == 0.0

    def test_per_person_stats_empty(
        self, empty_analytics_service: AnalyticsService
    ) -> None:
        """Per-person stats should be empty list with no history."""
        stats = empty_analytics_service.get_per_person_stats(days=30)

        assert stats == []

    def test_duration_trend_empty(
        self, empty_analytics_service: AnalyticsService
    ) -> None:
        """Duration trend should be empty list with no history."""
        trend = empty_analytics_service.get_duration_trend(days=30)

        assert trend == []

    def test_overtime_leaderboard_empty(
        self, empty_analytics_service: AnalyticsService
    ) -> None:
        """Overtime leaderboard should be empty with no history."""
        leaderboard = empty_analytics_service.get_overtime_leaderboard(limit=5, days=30)

        assert leaderboard == []

    def test_attendance_stats_empty(
        self, empty_analytics_service: AnalyticsService
    ) -> None:
        """Attendance stats should be zero with no history."""
        stats = empty_analytics_service.get_attendance_stats(days=30)

        assert stats.total_possible_attendances == 0
        assert stats.overall_attendance_rate == 0.0

    def test_on_time_rate_empty(
        self, empty_analytics_service: AnalyticsService
    ) -> None:
        """On-time rate should be zero with no history."""
        rate = empty_analytics_service.calculate_on_time_rate(days=30)

        assert rate == 0.0


# =============================================================================
# Test 7.T6: Date Filtering Works Correctly
# =============================================================================


class TestDateFiltering:
    """Test 7.T6: Date filtering works correctly."""

    def test_filter_by_days_limits_results(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Filtering by days should limit results."""
        # All 3 meetings are within the last 30 days
        stats_30 = analytics_service.get_summary_stats(days=30)
        assert stats_30.total_meetings == 3

    def test_filter_excludes_old_meetings(
        self, temp_data_dir: Path
    ) -> None:
        """Old meetings should be excluded by date filter."""
        # Create history with an old meeting
        old_date = datetime.now() - timedelta(days=60)
        old_record = MeetingRecord(
            id=f"{old_date.strftime('%Y-%m-%d')}T09:00:00",
            date=old_date.strftime("%Y-%m-%d"),
            start_time="09:00:00",
            end_time="09:10:00",
            total_duration_seconds=600.0,
            expected_duration_seconds=900,
            status=MeetingStatus.COMPLETED,
            team_id="test_team",
            participants=[
                ParticipantRecord(
                    member_id="alice",
                    display_name="Alice",
                    status=ParticipantStatus.PRESENT,
                    allocated_time_seconds=180,
                    actual_time_seconds=150.0,
                    overtime_seconds=0.0,
                    order_position=1,
                )
            ],
        )

        repo = HistoryRepository(team_id="test_team", data_dir=temp_data_dir)
        repo.load()
        repo.save_entry(old_record)
        service = AnalyticsService(repo)

        # 30-day filter should exclude 60-day old meeting
        stats = service.get_summary_stats(days=30)
        assert stats.total_meetings == 0

    def test_on_time_rate_respects_filter(
        self, analytics_service: AnalyticsService
    ) -> None:
        """On-time rate should respect day filter."""
        # Test with all data
        rate_all = analytics_service.calculate_on_time_rate(days=None)
        # Should be 2/3 based on our sample data
        assert abs(rate_all - 2 / 3) < 0.01


# =============================================================================
# Test 7.T7: Attendance Percentage Calculated Correctly
# =============================================================================


class TestAttendanceStats:
    """Test 7.T7: Attendance percentage calculated correctly."""

    def test_overall_attendance_rate(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Overall attendance rate should be calculated correctly."""
        stats = analytics_service.get_attendance_stats(days=30)

        # Total participants: 3 meetings * 3 people = 9
        # Present: Meeting1(2) + Meeting2(2) + Meeting3(3) = 7
        # Rate: 7/9 = 0.777...
        assert stats.total_possible_attendances == 9
        assert stats.total_present == 7
        assert abs(stats.overall_attendance_rate - 7 / 9) < 0.01

    def test_attendance_absent_count(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Absent count should be tracked correctly."""
        stats = analytics_service.get_attendance_stats(days=30)

        # Charlie was absent once
        assert stats.total_absent == 1

    def test_attendance_skipped_count(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Skipped count should be tracked correctly."""
        stats = analytics_service.get_attendance_stats(days=30)

        # Charlie was skipped once
        assert stats.total_skipped == 1

    def test_per_person_attendance_rate(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Per-person attendance rates should be calculated correctly."""
        stats = analytics_service.get_attendance_stats(days=30)

        # Alice: 3/3 = 1.0
        assert stats.per_person["alice"]["attendance_rate"] == 1.0
        # Bob: 3/3 = 1.0
        assert stats.per_person["bob"]["attendance_rate"] == 1.0
        # Charlie: 1/3 = 0.333...
        assert abs(stats.per_person["charlie"]["attendance_rate"] - 1 / 3) < 0.01

    def test_per_person_meeting_counts(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Per-person meeting counts should be tracked."""
        stats = analytics_service.get_attendance_stats(days=30)

        assert stats.per_person["alice"]["meetings_attended"] == 3.0
        assert stats.per_person["alice"]["meetings_possible"] == 3.0
        assert stats.per_person["charlie"]["meetings_attended"] == 1.0
        assert stats.per_person["charlie"]["meetings_possible"] == 3.0


# =============================================================================
# Additional Tests: Edge Cases
# =============================================================================


class TestEdgeCases:
    """Additional edge case tests."""

    def test_summary_stats_participants_count(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Total participants should only count present members."""
        stats = analytics_service.get_summary_stats(days=30)

        # Present: 2+2+3 = 7
        assert stats.total_participants == 7
        # Avg: 7/3 = 2.333...
        assert abs(stats.avg_participants_per_meeting - 7 / 3) < 0.01

    def test_per_person_avg_time(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Average time per person should be calculated correctly."""
        stats = analytics_service.get_per_person_stats(days=30)
        stats_by_id = {s.member_id: s for s in stats}

        # Alice: 490/3 = 163.33...
        assert abs(stats_by_id["alice"].avg_time_seconds - 490 / 3) < 0.01

    def test_per_person_attendance_rate(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Attendance rate per person should be calculated correctly."""
        stats = analytics_service.get_per_person_stats(days=30)
        stats_by_id = {s.member_id: s for s in stats}

        # Alice: 3/3 = 1.0
        assert stats_by_id["alice"].attendance_rate == 1.0
        # Charlie: 1/3 = 0.333...
        assert abs(stats_by_id["charlie"].attendance_rate - 1 / 3) < 0.01

    def test_leaderboard_excludes_zero_overtime(
        self, analytics_service: AnalyticsService
    ) -> None:
        """Members with no overtime should not appear in leaderboard."""
        leaderboard = analytics_service.get_overtime_leaderboard(limit=10, days=30)

        member_ids = {e.member_id for e in leaderboard}
        assert "alice" not in member_ids
        assert "charlie" not in member_ids

    def test_dataclass_defaults(self) -> None:
        """Dataclasses should have sensible defaults."""
        summary = SummaryStats()
        assert summary.total_meetings == 0
        assert summary.on_time_rate == 0.0

        person = PersonStats(member_id="test", display_name="Test")
        assert person.total_meetings == 0
        assert person.attendance_rate == 0.0

        trend = DurationTrendPoint(date="2026-01-01")
        assert trend.meeting_count == 0

        overtime = OvertimeEntry(member_id="test", display_name="Test")
        assert overtime.total_overtime_seconds == 0.0

        attendance = AttendanceStats()
        assert attendance.overall_attendance_rate == 0.0
