"""
Analytics dashboard component for Streamlit UI.

This module provides visualizations and statistics
for meeting history and performance metrics.
"""

from pathlib import Path

import streamlit as st

from src.core.constants import COLORS, DEFAULT_ANALYTICS_DAYS
from src.data.history_repository import HistoryRepository
from src.services.analytics_service import AnalyticsService

# Chart color scheme (from shared constants)
CHART_COLORS = {
    "primary": COLORS["normal"],
    "secondary": COLORS["paused"],
    "warning": COLORS["warning"],
    "danger": COLORS["overtime"],
}

# Default number of days for analytics
DEFAULT_DAYS = DEFAULT_ANALYTICS_DAYS


def render_analytics_dashboard(team_id: str, data_dir: Path) -> None:
    """
    Render the full analytics dashboard.

    Args:
        team_id: Team identifier.
        data_dir: Path to data directory.
    """
    # Initialize services
    history_repo = HistoryRepository(team_id=team_id, data_dir=data_dir)
    analytics = AnalyticsService(history_repo=history_repo)

    st.header("Analytics Dashboard")

    # Date range selector
    days = st.slider("Time Range (days)", min_value=7, max_value=90, value=DEFAULT_DAYS)

    # Summary stats row
    render_summary_stats(analytics, days)

    st.divider()

    # Charts row
    col1, col2 = st.columns(2)

    with col1:
        render_duration_trend(analytics, days)

    with col2:
        render_overtime_leaderboard(analytics, days)

    st.divider()

    # Attendance stats
    render_attendance_stats(analytics, days)


def render_summary_stats(analytics: AnalyticsService, days: int) -> None:
    """
    Render summary statistics cards.

    Args:
        analytics: Analytics service instance.
        days: Number of days to analyze.
    """
    stats = analytics.get_summary_stats(days)

    cols = st.columns(4)

    with cols[0]:
        st.metric(
            "Total Meetings",
            stats.total_meetings,
        )

    with cols[1]:
        avg_mins = stats.avg_duration_seconds / 60
        st.metric(
            "Avg Duration",
            f"{avg_mins:.1f} min",
        )

    with cols[2]:
        st.metric(
            "On-Time Rate",
            f"{stats.on_time_rate:.0%}",
        )

    with cols[3]:
        avg_overtime = stats.avg_overtime_seconds
        st.metric(
            "Avg Overtime",
            f"{avg_overtime:.0f}s",
        )


def render_duration_trend(analytics: AnalyticsService, days: int) -> None:
    """
    Render meeting duration trend chart.

    Args:
        analytics: Analytics service instance.
        days: Number of days to analyze.
    """
    st.subheader("Meeting Duration Trend")

    trend_data = analytics.get_duration_trend(days)

    if not trend_data:
        st.info("No meeting data available for the selected period.")
        return

    # Prepare data for chart
    chart_data = {
        "Date": [p.date for p in trend_data],
        "Duration (min)": [p.avg_duration_seconds / 60 for p in trend_data],
    }

    st.line_chart(
        chart_data,
        x="Date",
        y="Duration (min)",
        color=CHART_COLORS["primary"],
    )


def render_overtime_leaderboard(
    analytics: AnalyticsService,
    days: int,
    limit: int = 5,
) -> None:
    """
    Render overtime leaderboard.

    Args:
        analytics: Analytics service instance.
        days: Number of days to analyze.
        limit: Maximum number of entries.
    """
    st.subheader("Overtime Leaderboard")

    leaderboard = analytics.get_overtime_leaderboard(limit=limit, days=days)

    if not leaderboard:
        st.info("No overtime data available.")
        return

    # Render as horizontal bar chart
    chart_data = {
        "Member": [entry.member_id for entry in leaderboard],
        "Overtime (s)": [entry.total_overtime_seconds for entry in leaderboard],
    }

    st.bar_chart(
        chart_data,
        x="Member",
        y="Overtime (s)",
        color=CHART_COLORS["warning"],
        horizontal=True,
    )


def render_attendance_stats(analytics: AnalyticsService, days: int) -> None:
    """
    Render attendance statistics.

    Args:
        analytics: Analytics service instance.
        days: Number of days to analyze.
    """
    st.subheader("Attendance Statistics")

    stats = analytics.get_attendance_stats(days)

    cols = st.columns(3)

    with cols[0]:
        st.metric("Total Present", stats.total_present)

    with cols[1]:
        st.metric("Total Absent", stats.total_absent)

    with cols[2]:
        st.metric("Attendance Rate", f"{stats.overall_attendance_rate:.0%}")

    # Per-person breakdown if available
    if stats.per_person:
        st.write("**Per-Person Attendance:**")
        sorted_members = sorted(
            stats.per_person.items(),
            key=lambda x: x[1].get("attendance_rate", 0),
            reverse=True,
        )
        for member_id, member_stats in sorted_members[:5]:
            rate = member_stats.get("attendance_rate", 0)
            st.write(f"- {member_id}: {rate:.0%}")


def render_person_stats(analytics: AnalyticsService, days: int) -> None:
    """
    Render per-person statistics.

    Args:
        analytics: Analytics service instance.
        days: Number of days to analyze.
    """
    st.subheader("Individual Statistics")

    person_stats = analytics.get_per_person_stats(days)

    if not person_stats:
        st.info("No individual data available.")
        return

    # Create table
    table_data = []
    for ps in person_stats:
        # Calculate on-time rate (no overtime / total meetings)
        on_time_count = ps.total_meetings - (1 if ps.total_overtime_seconds > 0 else 0)
        on_time_rate = on_time_count / ps.total_meetings if ps.total_meetings > 0 else 0.0
        table_data.append({
            "Member": ps.member_id,
            "Meetings": ps.total_meetings,
            "Avg Time (s)": f"{ps.avg_time_seconds:.0f}",
            "Total Overtime (s)": f"{ps.total_overtime_seconds:.0f}",
            "On-Time Rate": f"{on_time_rate:.0%}",
        })

    st.dataframe(table_data, use_container_width=True)
