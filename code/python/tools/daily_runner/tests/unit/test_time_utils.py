"""
Unit tests for time utility functions.

Tests for src/core/time_utils.py
"""

from src.core.time_utils import (
    calculate_progress,
    format_time_mmss,
    is_overtime,
    is_warning_threshold,
    minutes_to_seconds,
    seconds_to_minutes,
)


class TestFormatTimeMmss:
    """Tests for format_time_mmss function."""

    def test_format_zero(self) -> None:
        """Zero seconds should format as 00:00."""
        assert format_time_mmss(0) == "00:00"

    def test_format_seconds_only(self) -> None:
        """Seconds under 60 should format correctly."""
        assert format_time_mmss(30) == "00:30"
        assert format_time_mmss(59) == "00:59"

    def test_format_minutes_and_seconds(self) -> None:
        """Minutes and seconds should format correctly."""
        assert format_time_mmss(60) == "01:00"
        assert format_time_mmss(90) == "01:30"
        assert format_time_mmss(125) == "02:05"

    def test_format_large_duration(self) -> None:
        """Large durations should format correctly."""
        assert format_time_mmss(3600) == "60:00"
        assert format_time_mmss(3661) == "61:01"

    def test_format_negative_with_sign(self) -> None:
        """Negative values should include minus sign by default."""
        assert format_time_mmss(-15) == "-00:15"
        assert format_time_mmss(-90) == "-01:30"

    def test_format_negative_without_sign(self) -> None:
        """show_sign=False should omit minus sign."""
        assert format_time_mmss(-15, show_sign=False) == "00:15"
        assert format_time_mmss(-90, show_sign=False) == "01:30"

    def test_format_fractional_truncates(self) -> None:
        """Fractional seconds should truncate (not round)."""
        assert format_time_mmss(30.9) == "00:30"
        assert format_time_mmss(59.99) == "00:59"


class TestSecondsToMinutes:
    """Tests for seconds_to_minutes function."""

    def test_convert_zero(self) -> None:
        """Zero seconds should convert to zero minutes."""
        assert seconds_to_minutes(0) == 0.0

    def test_convert_full_minute(self) -> None:
        """60 seconds should convert to 1 minute."""
        assert seconds_to_minutes(60) == 1.0

    def test_convert_partial_minute(self) -> None:
        """Partial minutes should convert correctly."""
        assert seconds_to_minutes(90) == 1.5
        assert seconds_to_minutes(30) == 0.5


class TestMinutesToSeconds:
    """Tests for minutes_to_seconds function."""

    def test_convert_zero(self) -> None:
        """Zero minutes should convert to zero seconds."""
        assert minutes_to_seconds(0) == 0.0

    def test_convert_full_minute(self) -> None:
        """1 minute should convert to 60 seconds."""
        assert minutes_to_seconds(1) == 60.0

    def test_convert_partial_minute(self) -> None:
        """Partial minutes should convert correctly."""
        assert minutes_to_seconds(1.5) == 90.0
        assert minutes_to_seconds(0.5) == 30.0


class TestCalculateProgress:
    """Tests for calculate_progress function."""

    def test_zero_elapsed(self) -> None:
        """Zero elapsed should return 0.0 progress."""
        assert calculate_progress(0, 180) == 0.0

    def test_full_progress(self) -> None:
        """Full elapsed should return 1.0 progress."""
        assert calculate_progress(180, 180) == 1.0

    def test_half_progress(self) -> None:
        """Half elapsed should return 0.5 progress."""
        assert calculate_progress(90, 180) == 0.5

    def test_overtime_progress(self) -> None:
        """Overtime should return > 1.0 progress."""
        assert calculate_progress(200, 180) > 1.0

    def test_zero_total(self) -> None:
        """Zero total should return 0.0 to avoid division by zero."""
        assert calculate_progress(100, 0) == 0.0

    def test_negative_total(self) -> None:
        """Negative total should return 0.0."""
        assert calculate_progress(100, -10) == 0.0


class TestIsOvertime:
    """Tests for is_overtime function."""

    def test_positive_remaining_not_overtime(self) -> None:
        """Positive remaining is not overtime."""
        assert is_overtime(30) is False
        assert is_overtime(0.1) is False

    def test_zero_remaining_not_overtime(self) -> None:
        """Zero remaining is not overtime (exactly on time)."""
        assert is_overtime(0) is False

    def test_negative_remaining_is_overtime(self) -> None:
        """Negative remaining is overtime."""
        assert is_overtime(-1) is True
        assert is_overtime(-30) is True


class TestIsWarningThreshold:
    """Tests for is_warning_threshold function."""

    def test_above_threshold_not_warning(self) -> None:
        """Above threshold should not be warning."""
        assert is_warning_threshold(60, 30) is False

    def test_at_threshold_is_warning(self) -> None:
        """Exactly at threshold should be warning."""
        assert is_warning_threshold(30, 30) is True

    def test_below_threshold_is_warning(self) -> None:
        """Below threshold should be warning."""
        assert is_warning_threshold(15, 30) is True

    def test_zero_is_warning(self) -> None:
        """Zero remaining should be warning."""
        assert is_warning_threshold(0, 30) is True

    def test_negative_not_warning(self) -> None:
        """Negative (overtime) should not be warning."""
        assert is_warning_threshold(-1, 30) is False
