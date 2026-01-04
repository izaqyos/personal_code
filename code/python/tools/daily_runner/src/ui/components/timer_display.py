"""
Timer display component for Streamlit UI.

This module provides the visual timer display including
countdown, progress bar, and status indicators.
"""

import streamlit as st

from src.core.constants import COLORS, DEFAULT_WARNING_THRESHOLD_SECONDS
from src.core.meeting_manager import MeetingManager
from src.core.models import MeetingState
from src.core.time_utils import format_time_mmss

# Color constants (from shared constants)
COLOR_NORMAL = COLORS["normal"]
COLOR_WARNING = COLORS["warning"]
COLOR_OVERTIME = COLORS["overtime"]
COLOR_PAUSED = COLORS["paused"]
COLOR_TRANSITION = COLORS["transition"]

# Thresholds
WARNING_THRESHOLD_SECONDS = DEFAULT_WARNING_THRESHOLD_SECONDS


def get_timer_color(remaining: float, state: MeetingState) -> str:
    """
    Get the appropriate color for the timer based on state.

    Args:
        remaining: Remaining seconds.
        state: Current meeting state.

    Returns:
        Hex color code string.
    """
    if state == MeetingState.PAUSED:
        return COLOR_PAUSED
    if state == MeetingState.TRANSITION:
        return COLOR_TRANSITION
    if remaining < 0:
        return COLOR_OVERTIME
    if remaining <= WARNING_THRESHOLD_SECONDS:
        return COLOR_WARNING
    return COLOR_NORMAL


def format_time(seconds: float) -> str:
    """
    Format seconds as MM:SS string.

    Args:
        seconds: Time in seconds (can be negative).

    Returns:
        Formatted time string.
    """
    # Delegate to shared utility
    return format_time_mmss(seconds)


def get_status_text(state: MeetingState, remaining: float) -> str:
    """
    Get the status text for current state.

    Args:
        state: Current meeting state.
        remaining: Remaining seconds.

    Returns:
        Status text string.
    """
    if state == MeetingState.PAUSED:
        return "PAUSED"
    if state == MeetingState.TRANSITION:
        return "TRANSITION"
    if remaining < 0:
        return "OVERTIME"
    if remaining <= WARNING_THRESHOLD_SECONDS:
        return "WARNING"
    return "SPEAKING"


def render_timer(manager: MeetingManager) -> None:
    """
    Render the timer display component.

    Args:
        manager: The meeting manager instance.
    """
    state = manager.state
    speaker = manager.current_speaker

    # Container for timer
    with st.container():
        # Speaker name
        if speaker:
            st.subheader(speaker.display_name)
        else:
            st.subheader("No Speaker")

        # Get timing info
        if state == MeetingState.TRANSITION:
            remaining = manager.transition_time_remaining
            total = manager._config.timer.transition_time_seconds
        else:
            remaining = manager.speaker_time_remaining
            total = manager._config.timer.default_speaker_time_seconds
            if speaker and speaker.daily_config:
                total = speaker.daily_config.default_time_seconds

        # Timer color
        color = get_timer_color(remaining, state)

        # Large timer display using markdown
        time_str = format_time(remaining)
        st.markdown(
            f"""
            <div style="text-align: center;">
                <h1 style="color: {color}; font-size: 5rem; font-family: monospace; margin: 0;">
                    {time_str}
                </h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Status indicator
        status = get_status_text(state, remaining)
        st.markdown(
            f"""
            <div style="text-align: center;">
                <span style="color: {color}; font-size: 1.5rem; font-weight: bold;">
                    [{status}]
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Progress bar (only when not in transition or paused)
        if state not in (MeetingState.TRANSITION, MeetingState.PAUSED) and total > 0:
            elapsed = max(0, total - remaining)
            progress = min(elapsed / total, 1.0)
            st.progress(progress)


def render_transition(manager: MeetingManager) -> None:
    """
    Render the transition display between speakers.

    Args:
        manager: The meeting manager instance.
    """
    speaker = manager.current_speaker
    remaining = manager.transition_time_remaining

    st.markdown(
        """
        <div style="text-align: center;">
            <h3 style="color: #666;">Next Up</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if speaker:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <h2 style="color: {COLOR_TRANSITION};">{speaker.display_name}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div style="text-align: center;">
            <p style="color: #ffff00; font-size: 1.2rem;">
                Starting in {int(remaining)}s
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
