"""
Time utility functions for the Daily Standup Timer.

This module provides shared time formatting and calculation
functions to eliminate code duplication across the codebase.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

# Israel timezone
ISRAEL_TZ = ZoneInfo("Asia/Jerusalem")

# Default team emojis (fallback when team file doesn't specify)
DEFAULT_TEAM_EMOJIS = {
    "imagine_dragons": "🐉",
    "sample_team": "🚀",
}


def format_team_name(team_id: str, emoji: str | None = None) -> str:
    """
    Format a team ID into a human-readable display name.

    Converts snake_case to Title Case and appends emoji.

    Args:
        team_id: The team identifier (e.g., "imagine_dragons").
        emoji: Optional emoji to append. If None, uses default lookup.

    Returns:
        Formatted team name (e.g., "Imagine Dragons 🐉").

    Examples:
        >>> format_team_name("imagine_dragons")
        'Imagine Dragons 🐉'
        >>> format_team_name("my_team", "🎯")
        'My Team 🎯'
    """
    # Convert snake_case to Title Case
    display_name = team_id.replace("_", " ").title()

    # Get emoji
    if emoji is None:
        emoji = DEFAULT_TEAM_EMOJIS.get(team_id, "")

    if emoji:
        return f"{display_name} {emoji}"
    return display_name


def format_timestamp_israel(timestamp: str | datetime) -> str:
    """
    Format a timestamp for display in Israel timezone.

    Removes milliseconds, adds space between date and time.

    Args:
        timestamp: ISO format timestamp string or datetime object.

    Returns:
        Formatted timestamp (e.g., "2026-01-12 10:56:40").

    Examples:
        >>> format_timestamp_israel("2026-01-12T10:56:40.314177")
        '2026-01-12 10:56:40'
    """
    if isinstance(timestamp, str):
        # Parse ISO format, handle various formats
        try:
            # Try parsing with fractional seconds
            if "." in timestamp:
                dt = datetime.fromisoformat(timestamp)
            else:
                dt = datetime.fromisoformat(timestamp)
        except ValueError:
            # Return as-is if parsing fails
            return timestamp.replace("T", " ").split(".")[0]
    else:
        dt = timestamp

    # Convert to Israel timezone if naive
    dt = dt.replace(tzinfo=ISRAEL_TZ) if dt.tzinfo is None else dt.astimezone(ISRAEL_TZ)

    # Format without milliseconds, with space separator
    return dt.strftime("%Y-%m-%d %H:%M:%S")


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
