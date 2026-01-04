"""
Speaker queue component for Streamlit UI.

This module provides the speaker queue display showing
all speakers, their status, and elapsed times.
"""

import streamlit as st

from src.core.constants import COLORS
from src.core.meeting_manager import MeetingManager
from src.core.time_utils import format_time_mmss

# Status colors (from shared constants)
STATUS_COLORS = {
    "speaking": COLORS["current"],
    "done": COLORS["completed"],
    "pending": COLORS["pending"],
    "absent": COLORS["absent"],
    "skipped": COLORS["skipped"],
}


def format_elapsed(seconds: float) -> str:
    """
    Format elapsed seconds as MM:SS.

    Args:
        seconds: Elapsed time in seconds.

    Returns:
        Formatted time string.
    """
    # Delegate to shared utility (no sign for elapsed)
    return format_time_mmss(seconds, show_sign=False)


def render_speaker_queue(manager: MeetingManager) -> None:
    """
    Render the speaker queue display.

    Args:
        manager: The meeting manager instance.
    """
    st.subheader("Speaker Queue")

    speakers = manager.speaker_queue
    current_index = manager.current_speaker_index
    records = manager._state_manager.get_all_speaker_records()

    # Build lookup for records
    records_by_id = {r.member.id: r for r in records}

    # Render each speaker
    for i, speaker in enumerate(speakers):
        record = records_by_id.get(speaker.id)
        is_current = i == current_index
        is_completed = i < current_index
        is_absent = record.is_absent if record else False
        is_skipped = record.skipped if record else False

        # Determine status and styling
        if is_absent:
            status = "Absent"
            color = STATUS_COLORS["absent"]
            icon = "🚫"
        elif is_skipped:
            status = "Skipped"
            color = STATUS_COLORS["skipped"]
            icon = "⏭️"
        elif is_current:
            status = "Speaking"
            color = STATUS_COLORS["speaking"]
            icon = "🎤"
        elif is_completed:
            status = "Done"
            color = STATUS_COLORS["done"]
            icon = "✅"
        else:
            status = "Pending"
            color = STATUS_COLORS["pending"]
            icon = "⏳"

        # Format time
        time_str = ""
        if record and (is_completed or is_current) and not is_absent and not is_skipped:
            time_str = format_elapsed(record.elapsed_seconds)
            if record.overtime_seconds > 0:
                time_str = f"⚠️ {time_str}"

        # Render row
        marker = "▶" if is_current else " "
        cols = st.columns([0.5, 3, 2, 1.5])

        with cols[0]:
            st.write(marker)
        with cols[1]:
            style = "font-weight: bold;" if is_current else ""
            if is_absent or is_skipped:
                style += "text-decoration: line-through; opacity: 0.6;"
            st.markdown(
                f'<span style="{style}">{icon} {speaker.display_name}</span>',
                unsafe_allow_html=True,
            )
        with cols[2]:
            st.markdown(
                f'<span style="color: {color};">{status}</span>',
                unsafe_allow_html=True,
            )
        with cols[3]:
            if time_str:
                st.write(time_str)


def render_speaker_card(
    speaker_name: str,
    status: str,
    elapsed: str,
    is_current: bool = False,
    is_overtime: bool = False,
) -> None:
    """
    Render a single speaker card.

    Args:
        speaker_name: Display name of the speaker.
        status: Current status text.
        elapsed: Elapsed time string.
        is_current: Whether this is the current speaker.
        is_overtime: Whether the speaker went overtime.
    """
    border_color = "#00ff00" if is_current else "#333333"
    bg_color = "#1a1a2e" if is_current else "#0f0f1a"
    time_color = "#ff0000" if is_overtime else "#ffffff"

    st.markdown(
        f"""
        <div style="
            border: 2px solid {border_color};
            border-radius: 8px;
            padding: 10px;
            margin: 5px 0;
            background-color: {bg_color};
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: {'bold' if is_current else 'normal'};">
                    {speaker_name}
                </span>
                <span style="color: {time_color};">{elapsed}</span>
            </div>
            <div style="color: #888; font-size: 0.9em;">{status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
