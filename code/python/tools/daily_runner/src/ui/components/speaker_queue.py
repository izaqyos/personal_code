"""
Speaker queue component for Streamlit UI.

This module provides the speaker queue display showing
all speakers, their status, and elapsed times.
"""

import streamlit as st

from src.core.constants import COLORS
from src.core.meeting_manager import MeetingManager
from src.core.time_utils import format_time_mmss  # Shared time formatting

# Status colors (from shared constants)
STATUS_COLORS = {
    "speaking": COLORS["current"],
    "done": COLORS["completed"],
    "pending": COLORS["pending"],
    "absent": COLORS["absent"],
    "skipped": COLORS["skipped"],
}


def render_speaker_queue(manager: MeetingManager) -> None:
    """
    Render the speaker queue display (compact for sidebar).

    Args:
        manager: The meeting manager instance.
    """
    st.markdown("**Queue**")

    speakers = manager.speaker_queue
    current_index = manager.current_speaker_index
    records = manager.get_all_speaker_records()

    # Build lookup for records
    records_by_id = {r.member.id: r for r in records}

    # Render each speaker as compact single line
    for i, speaker in enumerate(speakers):
        record = records_by_id.get(speaker.id)
        is_current = i == current_index
        is_completed = i < current_index
        is_absent = record.is_absent if record else False
        is_skipped = record.skipped if record else False

        # Determine icon and color
        if is_absent:
            icon = "🚫"
            color = STATUS_COLORS["absent"]
        elif is_skipped:
            icon = "⏩"
            color = STATUS_COLORS["skipped"]
        elif is_current:
            icon = "▶"
            color = STATUS_COLORS["speaking"]
        elif is_completed:
            icon = "✓"
            color = STATUS_COLORS["done"]
        else:
            icon = "○"
            color = STATUS_COLORS["pending"]

        # Format time (compact)
        time_str = ""
        if record and (is_completed or is_current) and not is_absent and not is_skipped:
            time_str = format_time_mmss(record.elapsed_seconds, show_sign=False)
            if record.overtime_seconds > 0:
                time_str = f"⚠{time_str}"

        # Get first name only for compact display
        name = speaker.display_name.split()[0] if speaker.display_name else "?"

        # Style
        style = f"color:{color}; font-size:0.85rem;"
        if is_current:
            style += "font-weight:bold;"
        if is_absent or is_skipped:
            style += "text-decoration:line-through; opacity:0.6;"

        # Single line: icon name time
        line = f"{icon} {name}"
        if time_str:
            line += f" {time_str}"

        st.markdown(f'<div style="{style}">{line}</div>', unsafe_allow_html=True)


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
