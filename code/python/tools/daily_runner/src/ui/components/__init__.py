"""
Streamlit UI components for the Daily Standup Timer.

This module includes:
- timer_display: Timer visualization components
- speaker_queue: Speaker queue display and reordering
- controls: Meeting control buttons
- analytics: Analytics dashboard components
"""

from src.ui.components.analytics import (
    render_analytics_dashboard,
    render_attendance_stats,
    render_duration_trend,
    render_overtime_leaderboard,
    render_person_stats,
    render_summary_stats,
)
from src.ui.components.controls import (
    render_absent_selector,
    render_controls,
    render_time_controls,
)
from src.ui.components.speaker_queue import (
    render_speaker_card,
    render_speaker_queue,
)
from src.ui.components.timer_display import (
    format_time,
    get_status_text,
    get_timer_color,
    render_timer,
    render_transition,
)

__all__ = [
    # Timer
    "render_timer",
    "render_transition",
    "format_time",
    "get_timer_color",
    "get_status_text",
    # Queue
    "render_speaker_queue",
    "render_speaker_card",
    # Controls
    "render_controls",
    "render_absent_selector",
    "render_time_controls",
    # Analytics
    "render_analytics_dashboard",
    "render_summary_stats",
    "render_duration_trend",
    "render_overtime_leaderboard",
    "render_attendance_stats",
    "render_person_stats",
]
