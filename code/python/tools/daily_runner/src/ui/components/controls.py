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
    Render the meeting control buttons.

    Args:
        manager: The meeting manager instance.
    """
    state = manager.state

    # Main control row
    cols = st.columns(5)

    # Pause/Resume button
    with cols[0]:
        if state == MeetingState.PAUSED:
            if st.button("▶️ Resume", use_container_width=True):
                manager.resume()
                st.rerun()
        elif state in (MeetingState.SPEAKING, MeetingState.GRACE):
            if st.button("⏸️ Pause", use_container_width=True):
                manager.pause()
                st.rerun()
        else:
            st.button("⏸️ Pause", use_container_width=True, disabled=True)

    # Next speaker button
    with cols[1]:
        can_next = state in (
            MeetingState.SPEAKING,
            MeetingState.GRACE,
            MeetingState.TRANSITION,
        )
        if st.button("⏭️ Next", use_container_width=True, disabled=not can_next) and can_next:
            manager.next_speaker()
            st.rerun()

    # Skip speaker button
    with cols[2]:
        can_skip = state in (
            MeetingState.SPEAKING,
            MeetingState.GRACE,
            MeetingState.TRANSITION,
        )
        if st.button("⏩ Skip", use_container_width=True, disabled=not can_skip) and can_skip:
            manager.skip_speaker()
            st.rerun()

    # Add time button
    with cols[3]:
        can_adjust = state in (MeetingState.SPEAKING, MeetingState.GRACE)
        if st.button(f"+{TIME_INCREMENT_SECONDS}s", use_container_width=True, disabled=not can_adjust) and can_adjust:
            manager.add_time(TIME_INCREMENT_SECONDS)
            st.rerun()

    # Subtract time button
    with cols[4]:
        can_adjust = state in (MeetingState.SPEAKING, MeetingState.GRACE)
        if st.button(f"-{TIME_INCREMENT_SECONDS}s", use_container_width=True, disabled=not can_adjust) and can_adjust:
            manager.add_time(-TIME_INCREMENT_SECONDS)
            st.rerun()

    # Secondary control row
    cols2 = st.columns(3)

    # Mark absent button
    with cols2[0]:
        render_absent_selector(manager)

    # Start speaking button (for transition state)
    with cols2[1]:
        if state == MeetingState.TRANSITION and st.button("🎤 Start Now", use_container_width=True):
            manager.start_speaking()
            st.rerun()

    # End meeting button
    with cols2[2]:
        if st.button("🛑 End Meeting", use_container_width=True, type="secondary"):
            manager.end_meeting(save_history=True)
            st.rerun()


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
    can_adjust = state in (MeetingState.SPEAKING, MeetingState.GRACE)

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
