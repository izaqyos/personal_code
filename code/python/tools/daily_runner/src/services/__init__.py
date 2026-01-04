"""
Services module for the Daily Standup Timer.

This module includes:
- analytics_service: Meeting statistics and trend analysis
"""

from src.services.analytics_service import (
    AnalyticsService,
    AttendanceStats,
    DurationTrendPoint,
    OvertimeEntry,
    PersonStats,
    SummaryStats,
)

__all__ = [
    "AnalyticsService",
    "AttendanceStats",
    "DurationTrendPoint",
    "OvertimeEntry",
    "PersonStats",
    "SummaryStats",
]
