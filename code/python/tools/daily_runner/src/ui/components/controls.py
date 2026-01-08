"""
Meeting control buttons for Streamlit UI.

This module provides the control panel with buttons
for pause/resume, next, skip, time adjustments, etc.
"""

import streamlit as st

from src.core.constants import TIME_INCREMENT_SECONDS
from src.core.meeting_manager import MeetingManager
from src.core.models import MeetingState


def render_controls(manager: MeetingManager) -> None:
    """
    Render the meeting control buttons (compact layout for sidebar).

    Args:
        manager: The meeting manager instance.
    """
    state = manager.state
    can_next = state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW, MeetingState.TRANSITION)
    can_skip = can_next
    can_adjust = state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW)

    # Row 1: Pause/Resume, Next, Skip (3 columns)
    c1, c2, c3 = st.columns(3)
    with c1:
        if state == MeetingState.PAUSED:
            if st.button("▶", use_container_width=True, help="Resume (P)"):
                manager.resume()
                st.rerun()
        elif state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW):
            if st.button("⏸", use_container_width=True, help="Pause (P)"):
                manager.pause()
                st.rerun()
        else:
            st.button("⏸", use_container_width=True, disabled=True)
    with c2:
        if st.button("⏭", use_container_width=True, disabled=not can_next, help="Next (N)") and can_next:
            manager.next_speaker()
            st.rerun()
    with c3:
        if st.button("⏩", use_container_width=True, disabled=not can_skip, help="Skip (S)") and can_skip:
            manager.skip_speaker()
            st.rerun()

    # Row 2: Time +/-, Start Now / End
    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("+30", use_container_width=True, disabled=not can_adjust, help="Add time (+)") and can_adjust:
            manager.add_time(TIME_INCREMENT_SECONDS)
            st.rerun()
    with c5:
        if st.button("-30", use_container_width=True, disabled=not can_adjust, help="Subtract time (-)") and can_adjust:
            manager.add_time(-TIME_INCREMENT_SECONDS)
            st.rerun()
    with c6:
        if state == MeetingState.TRANSITION:
            if st.button("🎤", use_container_width=True, help="Start Now"):
                manager.start_speaking()
                st.rerun()
        else:
            if st.button("🛑", use_container_width=True, help="End Meeting"):
                manager.end_meeting(save_history=True)
                st.rerun()

    # Row 3: Absent selector (full width)
    render_absent_selector(manager)


def render_absent_selector(manager: MeetingManager) -> None:
    """
    Render the absent member selector.

    Args:
        manager: The meeting manager instance.
    """
    speakers = manager.speaker_queue

    if not speakers:
        return

    # Create options list
    options = ["Select member..."] + [s.display_name for s in speakers]

    selected = st.selectbox(
        "Mark Absent",
        options=options,
        key="absent_selector",
        label_visibility="collapsed",
    )

    if selected and selected != "Select member...":
        # Find the member
        for speaker in speakers:
            if speaker.display_name == selected:
                manager.mark_absent(speaker.id)
                st.rerun()
                break


def render_time_controls(manager: MeetingManager) -> None:
    """
    Render time adjustment controls.

    Args:
        manager: The meeting manager instance.
    """
    state = manager.state
    can_adjust = state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            f"➕ Add {TIME_INCREMENT_SECONDS}s",
            use_container_width=True,
            disabled=not can_adjust,
        ):
            manager.add_time(TIME_INCREMENT_SECONDS)
            st.rerun()

    with col2:
        if st.button(
            f"➖ Remove {TIME_INCREMENT_SECONDS}s",
            use_container_width=True,
            disabled=not can_adjust,
        ):
            manager.add_time(-TIME_INCREMENT_SECONDS)
            st.rerun()
