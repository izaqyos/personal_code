"""
Main Streamlit application for the Daily Standup Timer.

This module provides the entry point and main page layout
for the Streamlit web interface.
"""

import time
from pathlib import Path

import streamlit as st

from src.core.meeting_manager import MeetingManager
from src.core.models import AppConfig, MeetingState
from src.data.config_manager import ConfigManager
from src.data.history_repository import HistoryRepository
from src.data.recovery_manager import RecoveryManager
from src.data.team_repository import TeamRepository
from src.ui.components.controls import render_controls
from src.ui.components.speaker_queue import render_speaker_queue
from src.ui.components.timer_display import render_timer

# Constants
PAGE_TITLE = "Daily Standup Timer"
PAGE_ICON = "⏱️"
REFRESH_INTERVAL_MS = 100
DATA_DIR = Path("data")
CONFIG_PATH = Path("config.json")


def init_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "meeting_manager" not in st.session_state:
        st.session_state.meeting_manager = None
    if "team_id" not in st.session_state:
        st.session_state.team_id = None
    if "config" not in st.session_state:
        config_mgr = ConfigManager(CONFIG_PATH)
        st.session_state.config = config_mgr.load()
    if "team_repo" not in st.session_state:
        teams_dir = Path(st.session_state.config.teams.directory)
        st.session_state.team_repo = TeamRepository(teams_dir=teams_dir)
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = time.time()


def get_meeting_manager() -> MeetingManager | None:
    """Get the current meeting manager from session state."""
    return st.session_state.get("meeting_manager")


def start_meeting(team_id: str) -> None:
    """
    Start a new meeting for the specified team.

    Args:
        team_id: The team identifier.
    """
    config: AppConfig = st.session_state.config
    team_repo: TeamRepository = st.session_state.team_repo

    # Initialize repositories
    history_repo = HistoryRepository(
        team_id=team_id,
        data_dir=DATA_DIR,
        max_entries=config.history.max_entries,
    )

    recovery_path = Path(config.recovery.file_path)
    recovery_mgr = RecoveryManager(
        recovery_path=recovery_path,
        auto_save_interval=config.recovery.auto_save_interval_seconds,
    )

    # Create meeting manager
    meeting_manager = MeetingManager(
        team_repo=team_repo,
        config=config,
        history_repo=history_repo,
        recovery_mgr=recovery_mgr,
    )

    # Start the meeting
    meeting_manager.start_meeting(team_id=team_id)

    # Store in session state
    st.session_state.meeting_manager = meeting_manager
    st.session_state.team_id = team_id


def end_meeting() -> None:
    """End the current meeting and save history."""
    manager = get_meeting_manager()
    if manager and manager.is_active:
        manager.end_meeting(save_history=True)
    st.session_state.meeting_manager = None
    st.session_state.team_id = None


def render_team_selection() -> None:
    """Render the team selection interface."""
    st.header("Select Team")

    team_repo: TeamRepository = st.session_state.team_repo
    teams = team_repo.list_teams()

    if not teams:
        st.error("No teams found! Please add team files to the teams directory.")
        return

    selected_team = st.selectbox(
        "Choose a team:",
        options=teams,
        format_func=lambda x: x.replace("_", " ").title(),
    )

    if st.button("Start Meeting", type="primary", use_container_width=True) and selected_team:
        start_meeting(selected_team)
        st.rerun()


def render_meeting_summary() -> None:
    """Render the meeting summary after completion."""
    manager = get_meeting_manager()
    if not manager:
        return

    st.header("Meeting Complete!")

    # Total duration
    total_mins = int(manager.meeting_elapsed // 60)
    total_secs = int(manager.meeting_elapsed % 60)
    st.metric("Total Duration", f"{total_mins:02d}:{total_secs:02d}")

    # Speaker summary table
    records = manager._state_manager.get_all_speaker_records()

    st.subheader("Speaker Summary")
    for record in records:
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.write(record.member.display_name)
        with col2:
            if record.is_absent:
                st.write("Absent")
            elif record.skipped:
                st.write("Skipped")
            else:
                mins = int(record.elapsed_seconds // 60)
                secs = int(record.elapsed_seconds % 60)
                st.write(f"{mins:02d}:{secs:02d}")
        with col3:
            if record.overtime_seconds > 0:
                st.write(f"+{int(record.overtime_seconds)}s overtime")
            elif not record.is_absent and not record.skipped:
                st.write("On time")

    if st.button("New Meeting", type="primary", use_container_width=True):
        st.session_state.meeting_manager = None
        st.session_state.team_id = None
        st.rerun()


def render_active_meeting() -> None:
    """Render the active meeting interface."""
    manager = get_meeting_manager()
    if not manager:
        return

    # Check for auto-transitions
    state = manager.state
    if state == MeetingState.TRANSITION:
        if manager.transition_time_remaining <= 0:
            manager.start_speaking()
            st.rerun()
    elif state == MeetingState.SPEAKING:
        manager.check_grace_period()

    # Layout: Timer on left, Queue on right
    col_timer, col_queue = st.columns([2, 1])

    with col_timer:
        render_timer(manager)

    with col_queue:
        render_speaker_queue(manager)

    # Controls at bottom
    st.divider()
    render_controls(manager)

    # Auto-refresh for timer updates
    time.sleep(REFRESH_INTERVAL_MS / 1000)
    st.rerun()


def main() -> None:
    """Main entry point for the Streamlit app."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
    )

    init_session_state()

    st.title(f"{PAGE_ICON} {PAGE_TITLE}")

    manager = get_meeting_manager()

    if manager is None:
        # No active meeting - show team selection
        render_team_selection()
    elif not manager.is_active:
        # Meeting ended - show summary
        render_meeting_summary()
    else:
        # Active meeting - show timer and controls
        render_active_meeting()


if __name__ == "__main__":
    main()
