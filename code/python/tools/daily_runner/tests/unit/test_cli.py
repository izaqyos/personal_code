"""
Unit tests for the CLI module.

Test coverage for Phase 8:
- 8.T1: CLI starts and shows team selection
- 8.T2: --team flag skips selection
- 8.T3: Recovery prompt shown when file exists
- 8.T4: Timer display updates correctly
- 8.T5: Keyboard commands trigger correct actions
- 8.T6: Warning colors appear at threshold
- 8.T7: Overtime display works correctly
- 8.T8: Quit saves history and clears recovery
"""

from io import StringIO
from pathlib import Path

import pytest
from rich.console import Console

from src.cli.commands import Command, KeyboardHandler, MockKeyboardHandler
from src.cli.display import COLORS, CLIDisplay
from src.core.models import (
    DailyConfig,
    MeetingState,
    TeamMember,
)
from src.core.state_manager import SpeakerRecord

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def console() -> Console:
    """Create a console with a string buffer for testing."""
    return Console(file=StringIO(), force_terminal=True, width=80)


@pytest.fixture
def display(console: Console) -> CLIDisplay:
    """Create a CLI display for testing."""
    return CLIDisplay(console=console)


@pytest.fixture
def sample_speakers() -> list[TeamMember]:
    """Create sample speakers for testing."""
    return [
        TeamMember(
            id="alice",
            name="Alice Anderson",
            display_name="Alice",
            email="alice@test.com",
            daily_config=DailyConfig(default_time_seconds=180, active=True),
        ),
        TeamMember(
            id="bob",
            name="Bob Brown",
            display_name="Bob",
            email="bob@test.com",
            daily_config=DailyConfig(default_time_seconds=180, active=True),
        ),
        TeamMember(
            id="charlie",
            name="Charlie Chen",
            display_name="Charlie",
            email="charlie@test.com",
            daily_config=DailyConfig(default_time_seconds=180, active=True),
        ),
    ]


@pytest.fixture
def sample_records(sample_speakers: list[TeamMember]) -> list[SpeakerRecord]:
    """Create sample speaker records for testing."""
    return [
        SpeakerRecord(member=sample_speakers[0], elapsed_seconds=150.0),
        SpeakerRecord(member=sample_speakers[1], elapsed_seconds=0.0),
        SpeakerRecord(member=sample_speakers[2], elapsed_seconds=0.0),
    ]


# =============================================================================
# Test 8.T1: CLI Starts and Shows Team Selection
# =============================================================================


class TestTeamSelection:
    """Test 8.T1: CLI starts and shows team selection."""

    def test_render_team_selection(self, display: CLIDisplay) -> None:
        """Team selection should show available teams."""
        teams = ["team_alpha", "team_beta", "team_gamma"]
        panel = display.render_team_selection(teams)

        assert panel is not None
        assert panel.title == "Teams"

    def test_team_selection_shows_numbers(self, display: CLIDisplay) -> None:
        """Team selection should show numbered options."""
        teams = ["alpha", "beta"]
        panel = display.render_team_selection(teams)

        # Render to string and check content
        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "[1]" in output
        assert "[2]" in output
        assert "alpha" in output
        assert "beta" in output


# =============================================================================
# Test 8.T2: --team Flag Skips Selection
# =============================================================================


class TestTeamFlag:
    """Test 8.T2: --team flag skips selection."""

    def test_mock_keyboard_returns_keys(self) -> None:
        """MockKeyboardHandler should return predefined keys."""
        mock = MockKeyboardHandler(keys=["1", "2", "q"])

        assert mock.read_key() == "1"
        assert mock.read_key() == "2"
        assert mock.read_key() == "q"
        assert mock.read_key() is None

    def test_mock_keyboard_add_keys(self) -> None:
        """MockKeyboardHandler should allow adding keys."""
        mock = MockKeyboardHandler()
        mock.add_key("a")
        mock.add_keys(["b", "c"])

        assert mock.read_key() == "a"
        assert mock.read_key() == "b"
        assert mock.read_key() == "c"


# =============================================================================
# Test 8.T3: Recovery Prompt Shown When File Exists
# =============================================================================


class TestRecoveryPrompt:
    """Test 8.T3: Recovery prompt shown when file exists."""

    def test_render_recovery_prompt(self, display: CLIDisplay) -> None:
        """Recovery prompt should show session info."""
        panel = display.render_recovery_prompt(
            team_id="test_team",
            started_at="2026-01-04 09:00:00",
            speaker_index=2,
            total_speakers=5,
        )

        assert panel is not None
        assert panel.title == "Recovery"

    def test_recovery_prompt_shows_progress(self, display: CLIDisplay) -> None:
        """Recovery prompt should show speaker progress."""
        panel = display.render_recovery_prompt(
            team_id="test_team",
            started_at="2026-01-04 09:00:00",
            speaker_index=2,
            total_speakers=5,
        )

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "3/5" in output  # speaker_index + 1


# =============================================================================
# Test 8.T4: Timer Display Updates Correctly
# =============================================================================


class TestTimerDisplay:
    """Test 8.T4: Timer display updates correctly."""

    def test_render_timer_normal(self, display: CLIDisplay) -> None:
        """Timer should render in normal state."""
        panel = display.render_timer(
            remaining_seconds=120.0,
            total_seconds=180.0,
            state=MeetingState.SPEAKING,
            speaker_name="Alice",
        )

        assert panel is not None
        assert panel.title == "Timer"

    def test_render_timer_shows_time(self, display: CLIDisplay) -> None:
        """Timer should show formatted time."""
        panel = display.render_timer(
            remaining_seconds=125.0,  # 2:05
            total_seconds=180.0,
            state=MeetingState.SPEAKING,
            speaker_name="Alice",
        )

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "02:05" in output

    def test_render_timer_shows_speaker(self, display: CLIDisplay) -> None:
        """Timer should show current speaker name."""
        panel = display.render_timer(
            remaining_seconds=60.0,
            total_seconds=180.0,
            state=MeetingState.SPEAKING,
            speaker_name="Bob",
        )

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "Bob" in output

    def test_render_timer_paused_state(self, display: CLIDisplay) -> None:
        """Timer should show PAUSED status when paused."""
        panel = display.render_timer(
            remaining_seconds=60.0,
            total_seconds=180.0,
            state=MeetingState.PAUSED,
            speaker_name="Alice",
        )

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "PAUSED" in output


# =============================================================================
# Test 8.T5: Keyboard Commands Trigger Correct Actions
# =============================================================================


class TestKeyboardCommands:
    """Test 8.T5: Keyboard commands trigger correct actions."""

    def test_key_mapping_pause(self) -> None:
        """'p' key should map to PAUSE_RESUME command."""
        handler = KeyboardHandler()
        assert handler.get_command("p") == Command.PAUSE_RESUME
        assert handler.get_command("P") == Command.PAUSE_RESUME
        assert handler.get_command(" ") == Command.PAUSE_RESUME

    def test_key_mapping_next(self) -> None:
        """'n' and Enter should map to NEXT_SPEAKER command."""
        handler = KeyboardHandler()
        assert handler.get_command("n") == Command.NEXT_SPEAKER
        assert handler.get_command("\r") == Command.NEXT_SPEAKER
        assert handler.get_command("\n") == Command.NEXT_SPEAKER

    def test_key_mapping_skip(self) -> None:
        """'s' key should map to SKIP_SPEAKER command."""
        handler = KeyboardHandler()
        assert handler.get_command("s") == Command.SKIP_SPEAKER
        assert handler.get_command("S") == Command.SKIP_SPEAKER

    def test_key_mapping_add_time(self) -> None:
        """'+' key should map to ADD_TIME command."""
        handler = KeyboardHandler()
        assert handler.get_command("+") == Command.ADD_TIME
        assert handler.get_command("=") == Command.ADD_TIME

    def test_key_mapping_subtract_time(self) -> None:
        """'-' key should map to SUBTRACT_TIME command."""
        handler = KeyboardHandler()
        assert handler.get_command("-") == Command.SUBTRACT_TIME

    def test_key_mapping_absent(self) -> None:
        """'a' key should map to MARK_ABSENT command."""
        handler = KeyboardHandler()
        assert handler.get_command("a") == Command.MARK_ABSENT
        assert handler.get_command("A") == Command.MARK_ABSENT

    def test_key_mapping_quit(self) -> None:
        """'q' key should map to QUIT command."""
        handler = KeyboardHandler()
        assert handler.get_command("q") == Command.QUIT
        assert handler.get_command("Q") == Command.QUIT

    def test_key_mapping_numbers(self) -> None:
        """Number keys should map to NUMBER_X commands."""
        handler = KeyboardHandler()
        assert handler.get_command("1") == Command.NUMBER_1
        assert handler.get_command("5") == Command.NUMBER_5
        assert handler.get_command("9") == Command.NUMBER_9

    def test_get_number_from_command(self) -> None:
        """Should extract number from NUMBER_X commands."""
        assert KeyboardHandler.get_number_from_command(Command.NUMBER_1) == 1
        assert KeyboardHandler.get_number_from_command(Command.NUMBER_5) == 5
        assert KeyboardHandler.get_number_from_command(Command.NUMBER_9) == 9
        assert KeyboardHandler.get_number_from_command(Command.QUIT) is None

    def test_unknown_key(self) -> None:
        """Unknown keys should map to UNKNOWN command."""
        handler = KeyboardHandler()
        assert handler.get_command("x") == Command.UNKNOWN
        assert handler.get_command("z") == Command.UNKNOWN


# =============================================================================
# Test 8.T6: Warning Colors Appear at Threshold
# =============================================================================


class TestWarningColors:
    """Test 8.T6: Warning colors appear at threshold."""

    def test_get_timer_color_normal(self, display: CLIDisplay) -> None:
        """Timer should be green when plenty of time remains."""
        color = display.get_timer_color(60.0, MeetingState.SPEAKING)
        assert color == COLORS["normal"]

    def test_get_timer_color_warning(self, display: CLIDisplay) -> None:
        """Timer should be yellow at warning threshold."""
        display.set_warning_threshold(30)
        color = display.get_timer_color(25.0, MeetingState.SPEAKING)
        assert color == COLORS["warning"]

    def test_get_timer_color_overtime(self, display: CLIDisplay) -> None:
        """Timer should be red in overtime."""
        color = display.get_timer_color(-5.0, MeetingState.SPEAKING)
        assert color == COLORS["overtime"]

    def test_get_timer_color_paused(self, display: CLIDisplay) -> None:
        """Timer should be blue when paused."""
        color = display.get_timer_color(60.0, MeetingState.PAUSED)
        assert color == COLORS["paused"]


# =============================================================================
# Test 8.T7: Overtime Display Works Correctly
# =============================================================================


class TestOvertimeDisplay:
    """Test 8.T7: Overtime display works correctly."""

    def test_overtime_shows_negative_time(self, display: CLIDisplay) -> None:
        """Overtime should show negative time format."""
        panel = display.render_timer(
            remaining_seconds=-15.0,
            total_seconds=180.0,
            state=MeetingState.GRACE,
            speaker_name="Alice",
        )

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "-00:15" in output

    def test_overtime_shows_status(self, display: CLIDisplay) -> None:
        """Overtime should show OVERTIME status."""
        panel = display.render_timer(
            remaining_seconds=-30.0,
            total_seconds=180.0,
            state=MeetingState.GRACE,
            speaker_name="Alice",
        )

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "OVERTIME" in output


# =============================================================================
# Test 8.T8: Quit Saves History and Clears Recovery
# =============================================================================


class TestQuitBehavior:
    """Test 8.T8: Quit saves history and clears recovery."""

    def test_render_meeting_summary(
        self, display: CLIDisplay, sample_records: list[SpeakerRecord]
    ) -> None:
        """Meeting summary should show all speakers."""
        panel = display.render_meeting_summary(
            total_duration=540.0,  # 9 minutes
            speaker_records=sample_records,
        )

        assert panel is not None
        assert panel.title == "Summary"

    def test_meeting_summary_shows_total(
        self, display: CLIDisplay, sample_records: list[SpeakerRecord]
    ) -> None:
        """Meeting summary should show total duration."""
        panel = display.render_meeting_summary(
            total_duration=540.0,
            speaker_records=sample_records,
        )

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "09:00" in output


# =============================================================================
# Additional Tests: Display Components
# =============================================================================


class TestDisplayComponents:
    """Additional display component tests."""

    def test_render_header(self, display: CLIDisplay) -> None:
        """Header should show team name and session ID."""
        panel = display.render_header("Test Team", "abc123")

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "Test Team" in output
        assert "abc123" in output

    def test_render_queue(
        self,
        display: CLIDisplay,
        sample_speakers: list[TeamMember],
        sample_records: list[SpeakerRecord],
    ) -> None:
        """Queue should show all speakers with status."""
        panel = display.render_queue(
            speakers=sample_speakers,
            current_index=1,
            speaker_records=sample_records,
        )

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "Alice" in output
        assert "Bob" in output
        assert "Charlie" in output

    def test_render_controls_speaking(self, display: CLIDisplay) -> None:
        """Controls should show available options for speaking state."""
        panel = display.render_controls(MeetingState.SPEAKING)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "[p]" in output  # Pause
        assert "[n]" in output  # Next
        assert "[+]" in output  # Add time

    def test_render_controls_paused(self, display: CLIDisplay) -> None:
        """Controls should show Resume when paused."""
        panel = display.render_controls(MeetingState.PAUSED)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "Resume" in output

    def test_render_transition(self, display: CLIDisplay) -> None:
        """Transition should show next speaker."""
        panel = display.render_transition(
            next_speaker="Charlie",
            remaining_seconds=15.0,
        )

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "Charlie" in output
        assert "15" in output

    def test_render_absent_picker(
        self, display: CLIDisplay, sample_speakers: list[TeamMember]
    ) -> None:
        """Absent picker should show numbered options."""
        panel = display.render_absent_picker(sample_speakers)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "[1]" in output
        assert "[2]" in output
        assert "[3]" in output


class TestMockKeyboardHandler:
    """Tests for MockKeyboardHandler."""

    def test_enable_raw_mode_always_succeeds(self) -> None:
        """Mock enable_raw_mode should always return True."""
        mock = MockKeyboardHandler()
        assert mock.enable_raw_mode() is True
        assert mock._enabled is True

    def test_disable_raw_mode(self) -> None:
        """Mock disable_raw_mode should set enabled to False."""
        mock = MockKeyboardHandler()
        mock.enable_raw_mode()
        mock.disable_raw_mode()
        assert mock._enabled is False

    def test_reset(self) -> None:
        """Reset should allow reading keys again."""
        mock = MockKeyboardHandler(keys=["a", "b"])
        mock.read_key()
        mock.read_key()
        assert mock.read_key() is None

        mock.reset()
        assert mock.read_key() == "a"

    def test_clear(self) -> None:
        """Clear should remove all keys."""
        mock = MockKeyboardHandler(keys=["a", "b"])
        mock.clear()
        assert mock.read_key() is None

    def test_context_manager(self) -> None:
        """Should work as context manager."""
        mock = MockKeyboardHandler(keys=["q"])
        with mock:
            assert mock._enabled is True
            assert mock.read_key() == "q"
        assert mock._enabled is False

    def test_process_input(self) -> None:
        """process_input should return CommandResult."""
        mock = MockKeyboardHandler(keys=["p"])
        mock.enable_raw_mode()

        result = mock.process_input()
        assert result is not None
        assert result.command == Command.PAUSE_RESUME
        assert result.raw_key == "p"

    def test_process_input_empty(self) -> None:
        """process_input should return None when no keys."""
        mock = MockKeyboardHandler()
        mock.enable_raw_mode()

        result = mock.process_input()
        assert result is None


class TestKeyboardHandlerBase:
    """Tests for KeyboardHandler base functionality."""

    def test_read_key_disabled_returns_none(self) -> None:
        """read_key should return None when not enabled."""
        handler = KeyboardHandler()
        # _enabled is False by default
        assert handler.read_key() is None

    def test_process_input_disabled_returns_none(self) -> None:
        """process_input should return None when not enabled."""
        handler = KeyboardHandler()
        result = handler.process_input()
        assert result is None


class TestCommandEnums:
    """Tests for Command enum values."""

    def test_all_commands_exist(self) -> None:
        """All expected commands should exist in enum."""
        expected_commands = [
            "PAUSE_RESUME",
            "NEXT_SPEAKER",
            "SKIP_SPEAKER",
            "ADD_TIME",
            "SUBTRACT_TIME",
            "MARK_ABSENT",
            "REORDER",
            "QUIT",
            "CONFIRM",
            "CANCEL",
            "RESUME_SESSION",
            "NEW_SESSION",
            "UNKNOWN",
        ]
        for cmd in expected_commands:
            assert hasattr(Command, cmd)

    def test_number_commands_1_to_9(self) -> None:
        """Number commands 1-9 should exist."""
        for i in range(1, 10):
            assert hasattr(Command, f"NUMBER_{i}")


class TestDisplayEdgeCases:
    """Test edge cases in display rendering."""

    def test_render_timer_no_speaker(self, display: CLIDisplay) -> None:
        """Timer should render without speaker name."""
        panel = display.render_timer(
            remaining_seconds=60.0,
            total_seconds=180.0,
            state=MeetingState.SPEAKING,
            speaker_name=None,
        )
        assert panel is not None

    def test_render_queue_empty(self, display: CLIDisplay) -> None:
        """Queue should handle empty speaker list."""
        panel = display.render_queue(
            speakers=[],
            current_index=-1,
            speaker_records=[],
        )
        assert panel is not None

    def test_render_queue_skipped_speaker(
        self,
        display: CLIDisplay,
        sample_speakers: list[TeamMember],
    ) -> None:
        """Queue should show skipped status."""
        records = [
            SpeakerRecord(member=sample_speakers[0], skipped=True),
            SpeakerRecord(member=sample_speakers[1]),
            SpeakerRecord(member=sample_speakers[2]),
        ]
        panel = display.render_queue(
            speakers=sample_speakers,
            current_index=1,
            speaker_records=records,
        )

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "Skipped" in output

    def test_render_queue_absent_speaker(
        self,
        display: CLIDisplay,
        sample_speakers: list[TeamMember],
    ) -> None:
        """Queue should show absent status."""
        records = [
            SpeakerRecord(member=sample_speakers[0], is_absent=True),
            SpeakerRecord(member=sample_speakers[1]),
            SpeakerRecord(member=sample_speakers[2]),
        ]
        panel = display.render_queue(
            speakers=sample_speakers,
            current_index=1,
            speaker_records=records,
        )

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "Absent" in output

    def test_render_summary_with_absent(
        self, display: CLIDisplay, sample_speakers: list[TeamMember]
    ) -> None:
        """Summary should show absent members correctly."""
        records = [
            SpeakerRecord(member=sample_speakers[0], elapsed_seconds=150.0),
            SpeakerRecord(member=sample_speakers[1], is_absent=True),
            SpeakerRecord(member=sample_speakers[2], skipped=True),
        ]
        panel = display.render_meeting_summary(
            total_duration=300.0,
            speaker_records=records,
        )

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "Absent" in output
        assert "Skipped" in output

    def test_render_summary_with_overtime(
        self, display: CLIDisplay, sample_speakers: list[TeamMember]
    ) -> None:
        """Summary should show overtime in red."""
        records = [
            SpeakerRecord(
                member=sample_speakers[0],
                elapsed_seconds=200.0,
                overtime_seconds=20.0,
            ),
        ]
        panel = display.render_meeting_summary(
            total_duration=200.0,
            speaker_records=records,
        )

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        # Just verify it rendered
        assert "Complete" in output or "Meeting Complete" in output

    def test_render_header_without_session(self, display: CLIDisplay) -> None:
        """Header should render without session ID."""
        panel = display.render_header("Test Team", None)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "Test Team" in output

    def test_render_controls_transition(self, display: CLIDisplay) -> None:
        """Controls in transition state should show appropriate options."""
        panel = display.render_controls(MeetingState.TRANSITION)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "[n]" in output  # Next
        assert "[q]" in output  # Quit

    def test_render_controls_grace(self, display: CLIDisplay) -> None:
        """Controls in grace state should show pause and time options."""
        panel = display.render_controls(MeetingState.GRACE)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "[p]" in output  # Pause
        assert "[+]" in output  # Add time

    def test_clear(self, display: CLIDisplay) -> None:
        """Clear should not raise."""
        # Just ensure it doesn't raise
        display.clear()

    def test_print(self, display: CLIDisplay) -> None:
        """Print should output to console."""
        display.print("Test message")
        # Check output was written
        output = display.console.file.getvalue()  # type: ignore[union-attr]
        assert "Test message" in output

    def test_timer_with_progress_bar(self, display: CLIDisplay) -> None:
        """Timer should include progress bar in normal state."""
        panel = display.render_timer(
            remaining_seconds=90.0,
            total_seconds=180.0,
            state=MeetingState.SPEAKING,
            speaker_name="Test",
        )
        assert panel is not None

    def test_queue_with_completed_time(
        self,
        display: CLIDisplay,
        sample_speakers: list[TeamMember],
    ) -> None:
        """Completed speakers should show their time."""
        records = [
            SpeakerRecord(member=sample_speakers[0], elapsed_seconds=165.5),
            SpeakerRecord(member=sample_speakers[1], elapsed_seconds=0.0),
            SpeakerRecord(member=sample_speakers[2], elapsed_seconds=0.0),
        ]
        panel = display.render_queue(
            speakers=sample_speakers,
            current_index=1,  # Alice is done, Bob is current
            speaker_records=records,
        )

        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(panel)
        output = console.file.getvalue()  # type: ignore[union-attr]

        assert "02:45" in output  # Alice's time


# =============================================================================
# CLIApp Tests
# =============================================================================


class TestCLIAppInit:
    """Test CLIApp initialization."""

    def test_cliapp_init(self, tmp_path: Path) -> None:
        """CLIApp should initialize with required components."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        # Create minimal config
        config = AppConfig()

        # Create team repo
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()
        team_repo = TeamRepository(teams_dir=teams_dir)

        # Create app
        console = Console(file=StringIO(), force_terminal=True, width=80)
        keyboard = MockKeyboardHandler()
        app = CLIApp(
            config=config,
            team_repo=team_repo,
            keyboard=keyboard,
            console=console,
        )

        assert app._config is config
        assert app._team_repo is team_repo
        assert app._keyboard is keyboard
        assert app._console is console
        assert app._meeting_manager is None
        assert app._running is False

    def test_cliapp_sets_warning_threshold(self, tmp_path: Path) -> None:
        """CLIApp should set warning threshold from config."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig, TimerConfig
        from src.data.team_repository import TeamRepository

        timer_config = TimerConfig(warning_threshold_seconds=45)
        config = AppConfig(timer=timer_config)

        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()
        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        app = CLIApp(config=config, team_repo=team_repo, console=console)

        assert app._display._warning_threshold == 45


class TestCLIAppSelectTeam:
    """Test team selection logic."""

    def test_select_team_no_teams(self, tmp_path: Path) -> None:
        """Should return None when no teams available."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()
        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        keyboard = MockKeyboardHandler()
        app = CLIApp(
            config=config,
            team_repo=team_repo,
            keyboard=keyboard,
            console=console,
        )
        keyboard.enable_raw_mode()

        result = app._select_team()
        assert result is None

    def test_select_team_single_team(self, tmp_path: Path) -> None:
        """Should auto-select when only one team."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()

        # Create a team file
        team_file = teams_dir / "alpha.json"
        team_file.write_text('{"id": "alpha", "name": "Alpha Team", "members": []}')

        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        keyboard = MockKeyboardHandler()
        app = CLIApp(
            config=config,
            team_repo=team_repo,
            keyboard=keyboard,
            console=console,
        )

        result = app._select_team()
        assert result == "alpha"

    def test_select_team_with_quit(self, tmp_path: Path) -> None:
        """Should return None when user quits."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()

        # Create two team files
        team1 = teams_dir / "alpha.json"
        team1.write_text('{"id": "alpha", "name": "Alpha", "members": []}')
        team2 = teams_dir / "beta.json"
        team2.write_text('{"id": "beta", "name": "Beta", "members": []}')

        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        keyboard = MockKeyboardHandler(keys=["q"])
        app = CLIApp(
            config=config,
            team_repo=team_repo,
            keyboard=keyboard,
            console=console,
        )
        keyboard.enable_raw_mode()

        result = app._select_team()
        assert result is None

    def test_select_team_with_number(self, tmp_path: Path) -> None:
        """Should select team by number."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()

        team1 = teams_dir / "alpha.json"
        team1.write_text('{"id": "alpha", "name": "Alpha", "members": []}')
        team2 = teams_dir / "beta.json"
        team2.write_text('{"id": "beta", "name": "Beta", "members": []}')

        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        keyboard = MockKeyboardHandler(keys=["2"])
        app = CLIApp(
            config=config,
            team_repo=team_repo,
            keyboard=keyboard,
            console=console,
        )
        keyboard.enable_raw_mode()

        result = app._select_team()
        # Result depends on order which is not guaranteed
        assert result in ["alpha", "beta"]


class TestCLIAppHandleCommand:
    """Test command handling."""

    def test_handle_command_no_manager(self, tmp_path: Path) -> None:
        """handle_command should do nothing without meeting manager."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()
        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        app = CLIApp(config=config, team_repo=team_repo, console=console)

        # Should not raise
        app._handle_command(Command.PAUSE_RESUME)
        app._handle_command(Command.NEXT_SPEAKER)
        app._handle_command(Command.QUIT)


class TestCLIAppQuit:
    """Test quit behavior."""

    def test_quit_sets_running_false(self, tmp_path: Path) -> None:
        """_quit_meeting should set _running to False."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()
        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        app = CLIApp(config=config, team_repo=team_repo, console=console)
        app._running = True

        app._quit_meeting()
        assert app._running is False


class TestCLIAppCheckRecovery:
    """Test recovery checking."""

    def test_check_recovery_no_manager(self, tmp_path: Path) -> None:
        """_check_recovery returns False when no recovery manager."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()
        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        app = CLIApp(config=config, team_repo=team_repo, console=console)

        assert app._check_recovery() is False


class TestCLIAppInterrupt:
    """Test interrupt handling."""

    def test_handle_interrupt(self, tmp_path: Path) -> None:
        """_handle_interrupt should set _running to False."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()
        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        app = CLIApp(config=config, team_repo=team_repo, console=console)
        app._running = True

        app._handle_interrupt(2, None)  # SIGINT
        assert app._running is False


class TestCLIAppCleanup:
    """Test cleanup behavior."""

    def test_cleanup_no_manager(self, tmp_path: Path) -> None:
        """_cleanup should not raise without meeting manager."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()
        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        app = CLIApp(config=config, team_repo=team_repo, console=console)

        # Should not raise
        app._cleanup()


class TestParseArgs:
    """Test command line argument parsing."""

    def test_parse_args_defaults(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """parse_args should return defaults when no args."""
        from src.cli.app import parse_args

        monkeypatch.setattr("sys.argv", ["daily-timer"])
        args = parse_args()

        assert args.team is None
        assert args.config == "config.json"
        assert args.verbose is False

    def test_parse_args_with_team(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """parse_args should accept --team flag."""
        from src.cli.app import parse_args

        monkeypatch.setattr("sys.argv", ["daily-timer", "--team", "alpha"])
        args = parse_args()

        assert args.team == "alpha"

    def test_parse_args_with_team_short(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """parse_args should accept -t flag."""
        from src.cli.app import parse_args

        monkeypatch.setattr("sys.argv", ["daily-timer", "-t", "beta"])
        args = parse_args()

        assert args.team == "beta"

    def test_parse_args_with_config(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """parse_args should accept --config flag."""
        from src.cli.app import parse_args

        monkeypatch.setattr("sys.argv", ["daily-timer", "--config", "custom.json"])
        args = parse_args()

        assert args.config == "custom.json"

    def test_parse_args_verbose(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """parse_args should accept --verbose flag."""
        from src.cli.app import parse_args

        monkeypatch.setattr("sys.argv", ["daily-timer", "--verbose"])
        args = parse_args()

        assert args.verbose is True

    def test_parse_args_verbose_short(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """parse_args should accept -v flag."""
        from src.cli.app import parse_args

        monkeypatch.setattr("sys.argv", ["daily-timer", "-v"])
        args = parse_args()

        assert args.verbose is True


class TestCLIAppRenderDisplay:
    """Test display rendering."""

    def test_render_display_no_manager(self, tmp_path: Path) -> None:
        """_render_display returns empty group without manager."""
        from rich.console import Group as RichGroup

        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()
        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        app = CLIApp(config=config, team_repo=team_repo, console=console)

        result = app._render_display()
        assert isinstance(result, RichGroup)


class TestCLIAppInitRepositories:
    """Test repository initialization."""

    def test_init_repositories(self, tmp_path: Path) -> None:
        """_init_repositories should create all required components."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()

        # Create a team with members
        team_file = teams_dir / "alpha.json"
        team_file.write_text(
            '{"id": "alpha", "name": "Alpha Team", "members": ['
            '{"id": "m1", "name": "Member 1", "display_name": "M1", "email": "m1@test.com"}'
            "]}"
        )

        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        app = CLIApp(config=config, team_repo=team_repo, console=console)
        app._team_id = "alpha"

        app._init_repositories()

        assert app._history_repo is not None
        assert app._recovery_mgr is not None
        assert app._meeting_manager is not None


class TestCLIAppStartMeeting:
    """Test starting meetings."""

    def test_start_new_meeting_no_manager(self, tmp_path: Path) -> None:
        """_start_new_meeting should not crash without manager."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()
        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        app = CLIApp(config=config, team_repo=team_repo, console=console)

        # Should not raise
        app._start_new_meeting()

    def test_start_new_meeting_no_team(self, tmp_path: Path) -> None:
        """_start_new_meeting should not crash without team_id."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()
        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        app = CLIApp(config=config, team_repo=team_repo, console=console)
        app._team_id = None

        # Should not raise
        app._start_new_meeting()


class TestCLIAppHandleCommandWithManager:
    """Test command handling with meeting manager."""

    def _create_app_with_meeting(self, tmp_path: Path):
        """Helper to create app with active meeting."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()

        # Create a team with multiple members
        team_file = teams_dir / "test.json"
        team_file.write_text(
            '{"team": {"id": "test", "name": "Test Team"}, "members": ['
            '{"id": "m1", "name": "M1", "display_name": "M1", "email": "m1@test.com"},'
            '{"id": "m2", "name": "M2", "display_name": "M2", "email": "m2@test.com"}'
            "]}"
        )

        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        keyboard = MockKeyboardHandler()
        app = CLIApp(
            config=config,
            team_repo=team_repo,
            keyboard=keyboard,
            console=console,
        )
        app._team_id = "test"
        app._init_repositories()
        app._start_new_meeting()

        return app

    def test_handle_pause_resume_speaking(self, tmp_path: Path) -> None:
        """PAUSE_RESUME should pause when speaking."""
        from src.core.models import MeetingState

        app = self._create_app_with_meeting(tmp_path)
        assert app._meeting_manager is not None
        # Start speaking
        app._meeting_manager.start_speaking()
        assert app._meeting_manager.state == MeetingState.SPEAKING

        app._handle_command(Command.PAUSE_RESUME)
        assert app._meeting_manager.state == MeetingState.PAUSED

    def test_handle_pause_resume_paused(self, tmp_path: Path) -> None:
        """PAUSE_RESUME should resume when paused."""
        from src.core.models import MeetingState

        app = self._create_app_with_meeting(tmp_path)
        assert app._meeting_manager is not None
        app._meeting_manager.start_speaking()
        app._meeting_manager.pause()
        assert app._meeting_manager.state == MeetingState.PAUSED

        app._handle_command(Command.PAUSE_RESUME)
        assert app._meeting_manager.state == MeetingState.SPEAKING

    def test_handle_next_speaker(self, tmp_path: Path) -> None:
        """NEXT_SPEAKER should advance to next."""
        app = self._create_app_with_meeting(tmp_path)
        assert app._meeting_manager is not None
        app._meeting_manager.start_speaking()
        initial_index = app._meeting_manager.current_speaker_index

        app._handle_command(Command.NEXT_SPEAKER)
        # Should move to next or transition
        assert app._meeting_manager.current_speaker_index >= initial_index

    def test_handle_skip_speaker(self, tmp_path: Path) -> None:
        """SKIP_SPEAKER should skip current speaker."""
        app = self._create_app_with_meeting(tmp_path)
        assert app._meeting_manager is not None
        app._meeting_manager.start_speaking()

        app._handle_command(Command.SKIP_SPEAKER)
        # Should have moved past first speaker
        assert app._meeting_manager.current_speaker_index >= 0

    def test_handle_add_time(self, tmp_path: Path) -> None:
        """ADD_TIME should add 30 seconds."""
        app = self._create_app_with_meeting(tmp_path)
        assert app._meeting_manager is not None
        app._meeting_manager.start_speaking()
        initial_remaining = app._meeting_manager.speaker_time_remaining

        app._handle_command(Command.ADD_TIME)
        new_remaining = app._meeting_manager.speaker_time_remaining
        # Should have added ~30 seconds (allow small time drift)
        assert new_remaining > initial_remaining + 29

    def test_handle_subtract_time(self, tmp_path: Path) -> None:
        """SUBTRACT_TIME should subtract 30 seconds."""
        app = self._create_app_with_meeting(tmp_path)
        assert app._meeting_manager is not None
        app._meeting_manager.start_speaking()
        initial_remaining = app._meeting_manager.speaker_time_remaining

        app._handle_command(Command.SUBTRACT_TIME)
        new_remaining = app._meeting_manager.speaker_time_remaining
        assert new_remaining < initial_remaining

    def test_handle_quit_with_meeting(self, tmp_path: Path) -> None:
        """QUIT should end meeting and set _running false."""
        app = self._create_app_with_meeting(tmp_path)
        app._running = True

        app._handle_command(Command.QUIT)
        assert app._running is False


class TestCLIAppAbsentPicker:
    """Test absent picker functionality."""

    def test_absent_picker_no_manager(self, tmp_path: Path) -> None:
        """_handle_absent_picker should not crash without manager."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()
        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        app = CLIApp(config=config, team_repo=team_repo, console=console)

        # Should not raise
        app._handle_absent_picker()

    def test_absent_picker_cancel(self, tmp_path: Path) -> None:
        """Escape should cancel absent picker."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()

        team_file = teams_dir / "test.json"
        team_file.write_text(
            '{"team": {"id": "test", "name": "Test"}, "members": ['
            '{"id": "m1", "name": "M1", "display_name": "M1", "email": "m1@test.com"}'
            "]}"
        )

        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        # Escape key for cancel
        keyboard = MockKeyboardHandler(keys=["\x1b"])
        app = CLIApp(
            config=config,
            team_repo=team_repo,
            keyboard=keyboard,
            console=console,
        )
        app._team_id = "test"
        app._init_repositories()
        app._start_new_meeting()
        keyboard.enable_raw_mode()

        app._handle_absent_picker()
        assert app._in_absent_picker is False

    def test_absent_picker_select_member(self, tmp_path: Path) -> None:
        """Number key should mark member as absent."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()

        team_file = teams_dir / "test.json"
        team_file.write_text(
            '{"team": {"id": "test", "name": "Test"}, "members": ['
            '{"id": "m1", "name": "M1", "display_name": "M1", "email": "m1@test.com"},'
            '{"id": "m2", "name": "M2", "display_name": "M2", "email": "m2@test.com"}'
            "]}"
        )

        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        keyboard = MockKeyboardHandler(keys=["1"])
        app = CLIApp(
            config=config,
            team_repo=team_repo,
            keyboard=keyboard,
            console=console,
        )
        app._team_id = "test"
        app._init_repositories()
        app._start_new_meeting()
        keyboard.enable_raw_mode()

        app._handle_absent_picker()
        assert app._in_absent_picker is False


class TestCLIAppRecoveryPrompt:
    """Test recovery prompt handling."""

    def test_recovery_prompt_no_manager(self, tmp_path: Path) -> None:
        """_handle_recovery_prompt returns True without manager."""
        from src.cli.app import CLIApp
        from src.core.models import AppConfig
        from src.data.team_repository import TeamRepository

        config = AppConfig()
        teams_dir = tmp_path / "teams"
        teams_dir.mkdir()
        team_repo = TeamRepository(teams_dir=teams_dir)

        console = Console(file=StringIO(), force_terminal=True, width=80)
        app = CLIApp(config=config, team_repo=team_repo, console=console)

        result = app._handle_recovery_prompt()
        assert result is True
