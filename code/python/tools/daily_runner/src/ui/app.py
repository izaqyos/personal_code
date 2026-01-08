"""
Main Streamlit application for the Daily Standup Timer.

This module provides the entry point and main page layout
for the Streamlit web interface. Optimized for compact sidebar display.
"""

import time
from pathlib import Path

import streamlit as st
import streamlit_hotkeys as hotkeys

from src.core.meeting_manager import MeetingManager
from src.core.models import AppConfig, MeetingState
from src.data.config_manager import ConfigManager
from src.data.history_repository import HistoryRepository
from src.data.recovery_manager import RecoveryManager
from src.data.team_repository import TeamRepository
from src.core.time_utils import format_time_mmss
from src.ui.components.controls import render_controls
from src.ui.components.speaker_queue import render_speaker_queue
from src.ui.components.timer_display import render_timer

# Constants
PAGE_TITLE = "Daily Timer"
PAGE_ICON = "⏱️"
REFRESH_INTERVAL_MS = 100
DATA_DIR = Path("data")
CONFIG_PATH = Path("config.json")

# Compact CSS to reduce Streamlit's default spacing
COMPACT_CSS = """
<style>
    /* Reduce main container padding */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0.5rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        max-width: 100%;
    }
    /* Reduce header size */
    h1 { font-size: 1.2rem !important; margin-bottom: 0.5rem !important; }
    h2, h3 { font-size: 1rem !important; margin: 0.3rem 0 !important; }
    /* Compact buttons */
    .stButton > button {
        padding: 0.2rem 0.4rem;
        font-size: 0.85rem;
        min-height: 2rem;
    }
    /* Reduce spacing between elements */
    .stMarkdown, .stProgress { margin-bottom: 0.2rem !important; }
    div[data-testid="stVerticalBlock"] > div { gap: 0.3rem !important; }
    /* Compact selectbox */
    .stSelectbox { margin-bottom: 0.2rem; }
    .stSelectbox > div > div { font-size: 0.85rem; }
    /* Hide Streamlit branding for cleaner look */
    #MainMenu, footer, header { visibility: hidden; }
    /* Progress bar height */
    .stProgress > div > div { height: 0.3rem !important; }
</style>
"""

# Keyboard shortcuts - using number keys to avoid Vimium conflicts
# Bindings are created lazily to avoid issues at module load time


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
        try:
            start_meeting(selected_team)
            st.rerun()
        except Exception as e:
            st.error(f"Failed to start meeting: {e}")


def render_meeting_summary() -> None:
    """Render the meeting summary after completion."""
    manager = get_meeting_manager()
    if not manager:
        return

    st.header("Meeting Complete!")

    # Total duration
    st.metric("Total Duration", format_time_mmss(manager.meeting_elapsed, show_sign=False))

    # Speaker summary table
    records = manager.get_all_speaker_records()

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
                st.write(format_time_mmss(record.elapsed_seconds, show_sign=False))
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
    """Render the active meeting interface (compact vertical layout)."""
    manager = get_meeting_manager()
    if not manager:
        return

    # Check for auto-transitions
    state = manager.state
    if state == MeetingState.TRANSITION:
        if manager.transition_time_remaining <= 0:
            manager.start_speaking()
            st.rerun()
    elif state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW):
        manager.check_grace_period()

    # Compact vertical layout (stacked for sidebar use)
    render_timer(manager)
    render_controls(manager)
    render_speaker_queue(manager)
    render_keyboard_legend()

    # Auto-refresh for timer updates
    time.sleep(REFRESH_INTERVAL_MS / 1000)
    st.rerun()


def inject_compact_styles() -> None:
    """Inject compact CSS."""
    st.markdown(COMPACT_CSS, unsafe_allow_html=True)


def setup_hotkeys() -> None:
    """Activate keyboard shortcuts using streamlit-hotkeys."""
    bindings = [
        hotkeys.hk("pause", "1", help="Pause/Resume timer"),
        hotkeys.hk("next", "2", help="Next speaker"),
        hotkeys.hk("skip", "3", help="Skip speaker"),
        hotkeys.hk("add_time", "4", help="Add 30 seconds"),
        hotkeys.hk("sub_time", "5", help="Subtract 30 seconds"),
        hotkeys.hk("end", "0", help="End meeting"),
    ]
    hotkeys.activate(bindings)


def handle_hotkey_actions(manager: MeetingManager) -> bool:
    """
    Handle keyboard shortcut actions.

    Returns True if an action was handled (requires rerun).
    """
    state = manager.state
    can_next = state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW, MeetingState.TRANSITION)
    can_adjust = state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW)
    handled = False

    if hotkeys.pressed("pause"):
        if state == MeetingState.PAUSED:
            manager.resume()
        elif state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW):
            manager.pause()
        handled = True

    if hotkeys.pressed("next") and can_next:
        manager.next_speaker()
        handled = True

    if hotkeys.pressed("skip") and can_next:
        manager.skip_speaker()
        handled = True

    if hotkeys.pressed("add_time") and can_adjust:
        manager.add_time(30)
        handled = True

    if hotkeys.pressed("sub_time") and can_adjust:
        manager.add_time(-30)
        handled = True

    if hotkeys.pressed("end"):
        manager.end_meeting(save_history=True)
        handled = True

    return handled


def render_keyboard_legend() -> None:
    """Render keyboard shortcut legend using streamlit-hotkeys."""
    st.markdown(
        '<div style="font-size:0.75rem;color:#888;margin-top:0.5rem;'
        'border-top:1px solid #444;padding-top:0.5rem;">'
        "<b>⌨️ Shortcuts</b></div>",
        unsafe_allow_html=True,
    )
    # Use the built-in legend from streamlit-hotkeys
    hotkeys.legend()


def main() -> None:
    """Main entry point for the Streamlit app."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    inject_compact_styles()
    init_session_state()

    st.markdown(f"**{PAGE_ICON} {PAGE_TITLE}**")

    manager = get_meeting_manager()

    # Setup and handle keyboard shortcuts if meeting is active
    if manager and manager.is_active:
        setup_hotkeys()
        if handle_hotkey_actions(manager):
            st.rerun()

    if manager is None:
        # No active meeting - show team selection
        render_team_selection()
    elif not manager.is_active:
        # Meeting ended - show summary
        render_meeting_summary()
    else:
        # Active meeting - show timer, controls, queue, and keyboard legend
        render_active_meeting()


if __name__ == "__main__":
    main()
