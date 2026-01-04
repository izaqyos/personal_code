"""
Time utility functions for the Daily Standup Timer.

This module provides shared time formatting and calculation
functions to eliminate code duplication across the codebase.
"""


def format_time_mmss(seconds: float, show_sign: bool = True) -> str:
    """
    Format seconds as MM:SS string.

    Args:
        seconds: Time in seconds (can be negative for overtime).
        show_sign: Whether to include minus sign for negative values.

    Returns:
        Formatted time string (e.g., "02:30" or "-00:15").

    Examples:
        >>> format_time_mmss(150)
        '02:30'
        >>> format_time_mmss(-15)
        '-00:15'
        >>> format_time_mmss(-15, show_sign=False)
        '00:15'
    """
    is_negative = seconds < 0
    abs_seconds = abs(seconds)
    mins = int(abs_seconds // 60)
    secs = int(abs_seconds % 60)
    sign = "-" if is_negative and show_sign else ""
    return f"{sign}{mins:02d}:{secs:02d}"


def seconds_to_minutes(seconds: float) -> float:
    """
    Convert seconds to minutes.

    Args:
        seconds: Time in seconds.

    Returns:
        Time in minutes.
    """
    return seconds / 60.0


def minutes_to_seconds(minutes: float) -> float:
    """
    Convert minutes to seconds.

    Args:
        minutes: Time in minutes.

    Returns:
        Time in seconds.
    """
    return minutes * 60.0


def calculate_progress(elapsed: float, total: float) -> float:
    """
    Calculate progress as a fraction (0.0 to 1.0+).

    Args:
        elapsed: Elapsed time in seconds.
        total: Total allocated time in seconds.

    Returns:
        Progress fraction (can exceed 1.0 in overtime).
    """
    if total <= 0:
        return 0.0
    return elapsed / total


def is_overtime(remaining: float) -> bool:
    """
    Check if the timer is in overtime.

    Args:
        remaining: Remaining time in seconds.

    Returns:
        True if in overtime (negative remaining time).
    """
    return remaining < 0


def is_warning_threshold(remaining: float, threshold: float) -> bool:
    """
    Check if remaining time is at or below the warning threshold.

    Args:
        remaining: Remaining time in seconds.
        threshold: Warning threshold in seconds.

    Returns:
        True if at or below threshold.
    """
    return 0 <= remaining <= threshold
