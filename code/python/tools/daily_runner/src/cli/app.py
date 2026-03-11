"""
Main CLI application for the Daily Standup Timer.

This module provides the entry point and main event loop
for the command-line interface.
"""

import argparse
import logging
import signal
import sys
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

from rich.console import Console, Group
from rich.live import Live

from src.cli.commands import Command, KeyboardHandler
from src.cli.display import CLIDisplay
from src.core.constants import (
    CLI_REFRESH_INTERVAL_SECONDS,
    CLI_REFRESH_PER_SECOND,
    LOG_BACKUP_COUNT,
    LOG_DATE_FORMAT,
    LOG_DIR,
    LOG_FILE_NAME,
    LOG_FORMAT,
    LOG_MAX_BYTES,
    TIME_INCREMENT_SECONDS,
)
from src.core.meeting_manager import MeetingManager
from src.core.models import AppConfig, MeetingState
from src.data.config_manager import ConfigManager
from src.data.history_repository import HistoryRepository
from src.data.recovery_manager import RecoveryManager
from src.data.team_repository import TeamRepository

logger = logging.getLogger(__name__)

# Refresh rate for the display (use constant from core.constants)
REFRESH_INTERVAL = CLI_REFRESH_INTERVAL_SECONDS


class CLIApp:
    """
    Main CLI application controller.

    Manages the event loop, keyboard input, display rendering,
    and coordinates the meeting manager.
    """

    def __init__(
        self,
        config: AppConfig,
        team_repo: TeamRepository,
        keyboard: KeyboardHandler | None = None,
        console: Console | None = None,
    ) -> None:
        """
        Initialize the CLI application.

        Args:
            config: Application configuration.
            team_repo: Team data repository.
            keyboard: Optional keyboard handler (for testing).
            console: Optional Rich console (for testing).
        """
        self._config = config
        self._team_repo = team_repo
        self._console = console or Console()
        self._display = CLIDisplay(self._console)
        self._keyboard = keyboard or KeyboardHandler()

        # Set warning threshold from config
        self._display.set_warning_threshold(
            self._config.timer.warning_threshold_seconds
        )

        # Components initialized per-session
        self._meeting_manager: MeetingManager | None = None
        self._history_repo: HistoryRepository | None = None
        self._recovery_mgr: RecoveryManager | None = None

        # State
        self._running = False
        self._team_id: str | None = None
        self._in_absent_picker = False
        self._in_recovery_prompt = False
        self._last_interaction_time: float = 0.0

    def run(self, team_id: str | None = None) -> int:
        """
        Run the CLI application.

        Args:
            team_id: Optional team ID to use directly.

        Returns:
            Exit code (0 for success).
        """
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._handle_interrupt)
        signal.signal(signal.SIGTERM, self._handle_interrupt)

        try:
            with self._keyboard:
                # Select team
                if team_id:
                    self._team_id = team_id
                else:
                    self._team_id = self._select_team()

                if not self._team_id:
                    return 0  # User quit

                # Initialize repositories for this team
                self._init_repositories()

                # Check for recovery
                if self._check_recovery() and not self._handle_recovery_prompt():
                    return 0  # User quit

                # Start meeting if not restored
                if self._meeting_manager is None or not self._meeting_manager.is_active:
                    self._start_new_meeting()

                # Run main loop
                return self._main_loop()

        except KeyboardInterrupt:
            return 0
        finally:
            self._cleanup()

    def _init_repositories(self) -> None:
        """Initialize repositories for the current team."""
        assert self._team_id is not None

        data_dir = Path(self._config.history.file_path).parent
        data_dir = Path("data")  # Use standard data directory

        self._history_repo = HistoryRepository(
            team_id=self._team_id,
            data_dir=data_dir,
            max_entries=self._config.history.max_entries,
        )

        recovery_path = Path(self._config.recovery.file_path)
        self._recovery_mgr = RecoveryManager(
            recovery_path=recovery_path,
            auto_save_interval=self._config.recovery.auto_save_interval_seconds,
        )

        self._meeting_manager = MeetingManager(
            team_repo=self._team_repo,
            config=self._config,
            history_repo=self._history_repo,
            recovery_mgr=self._recovery_mgr,
        )

    def _select_team(self) -> str | None:
        """
        Show team selection menu.

        Returns:
            Selected team ID or None if cancelled.
        """
        teams = self._team_repo.list_teams()
        if not teams:
            self._console.print("[red]No teams found![/red]")
            return None

        if len(teams) == 1:
            return teams[0]

        self._display.clear()
        self._console.print(self._display.render_team_selection(teams))

        while True:
            result = self._keyboard.process_input(timeout=0.5)
            if result is None:
                continue

            if result.command == Command.QUIT:
                return None

            # Check for number selection
            num = KeyboardHandler.get_number_from_command(result.command)
            if num is not None and 1 <= num <= len(teams):
                return teams[num - 1]

    def _check_recovery(self) -> bool:
        """Check if a recovery session exists."""
        if self._recovery_mgr is None:
            return False
        return self._recovery_mgr.has_recovery()

    def _handle_recovery_prompt(self) -> bool:
        """
        Handle recovery session prompt.

        Returns:
            True to continue, False to quit.
        """
        if self._recovery_mgr is None or self._meeting_manager is None:
            return True

        info = self._recovery_mgr.get_recovery_info()
        if info is None:
            return True

        self._display.clear()
        self._console.print(
            self._display.render_recovery_prompt(
                team_id=info.get("team_id", "Unknown"),
                started_at=info.get("started_at", "Unknown"),
                speaker_index=int(info.get("speaker_index", "0")),
                total_speakers=int(info.get("total_speakers", "0")),
            )
        )

        self._in_recovery_prompt = True
        while self._in_recovery_prompt:
            result = self._keyboard.process_input(timeout=0.5)
            if result is None:
                continue

            if result.command == Command.RESUME_SESSION:
                # Restore session
                if self._meeting_manager.restore_session():
                    self._in_recovery_prompt = False
                    return True
                else:
                    self._console.print("[red]Failed to restore session[/red]")
                    self._meeting_manager.discard_recovery()
                    self._in_recovery_prompt = False
                    return True

            elif result.command in (Command.NEXT_SPEAKER, Command.NUMBER_2):
                # Start new meeting
                self._meeting_manager.discard_recovery()
                self._in_recovery_prompt = False
                return True

            elif result.command == Command.QUIT:
                self._in_recovery_prompt = False
                return False

        return True

    def _start_new_meeting(self) -> None:
        """Start a new meeting."""
        if self._meeting_manager is None or self._team_id is None:
            return

        try:
            self._meeting_manager.start_meeting(team_id=self._team_id)
        except ValueError as e:
            self._console.print(f"[red]Error starting meeting: {e}[/red]")
            raise

    def _main_loop(self) -> int:
        """
        Main event loop.

        Returns:
            Exit code.
        """
        if self._meeting_manager is None:
            return 1

        self._running = True
        self._reset_interaction_time()
        last_state = self._meeting_manager.state

        with Live(
            self._render_display(),
            console=self._console,
            refresh_per_second=CLI_REFRESH_PER_SECOND,
            transient=True,
        ) as live:
            while self._running and self._meeting_manager.is_active:
                # Process keyboard input
                result = self._keyboard.process_input(timeout=REFRESH_INTERVAL)
                if result is not None:
                    self._handle_command(result.command)
                    self._reset_interaction_time()

                # Check inactivity timeout
                if self._check_inactivity():
                    logger.info(
                        "Inactivity timeout reached (%ds), auto-closing meeting",
                        self._config.timer.inactivity_timeout_seconds,
                    )
                    self._quit_meeting()
                    continue

                # Check for state transitions
                current_state = self._meeting_manager.state
                if current_state != last_state:
                    last_state = current_state

                    # Auto-start speaking after transition
                    if current_state == MeetingState.TRANSITION:
                        # Wait for transition to complete
                        pass
                    elif (
                        last_state == MeetingState.TRANSITION
                        and current_state == MeetingState.SPEAKING
                    ):
                        pass

                # Check transition timer
                if (
                    current_state == MeetingState.TRANSITION
                    and self._meeting_manager.transition_time_remaining <= 0
                ):
                    self._meeting_manager.start_speaking()

                # Check grace period and overflow transitions
                if current_state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW):
                    self._meeting_manager.check_grace_period()

                # Update display
                live.update(self._render_display())

        # Show summary
        self._display.clear()
        if self._meeting_manager is not None:
            records = self._meeting_manager.get_all_speaker_records()
            self._console.print(
                self._display.render_meeting_summary(
                    total_duration=self._meeting_manager.meeting_elapsed,
                    speaker_records=records,
                )
            )

        return 0

    def _render_display(self) -> Group:
        """
        Render the current display state.

        Returns:
            Rich Group with all display components.
        """
        if self._meeting_manager is None:
            return Group()

        state = self._meeting_manager.state
        components = []

        # Header
        team_name = self._team_id or "Unknown"
        components.append(
            self._display.render_header(
                team_name=team_name,
            )
        )

        # Timer or transition
        if state == MeetingState.TRANSITION:
            speaker = self._meeting_manager.current_speaker
            components.append(
                self._display.render_transition(
                    next_speaker=speaker.display_name if speaker else "Unknown",
                    remaining_seconds=self._meeting_manager.transition_time_remaining,
                )
            )
        else:
            speaker = self._meeting_manager.current_speaker
            speaker_time = self._config.timer.default_speaker_time_seconds
            if speaker and speaker.daily_config:
                speaker_time = speaker.daily_config.default_time_seconds

            components.append(
                self._display.render_timer(
                    remaining_seconds=self._meeting_manager.speaker_time_remaining,
                    total_seconds=speaker_time,
                    state=state,
                    speaker_name=speaker.display_name if speaker else None,
                )
            )

        # Speaker queue
        components.append(
            self._display.render_queue(
                speakers=self._meeting_manager.speaker_queue,
                current_index=self._meeting_manager.current_speaker_index,
                speaker_records=self._meeting_manager.get_all_speaker_records(),
                current_speaker_elapsed=self._meeting_manager.speaker_time_elapsed,
            )
        )

        # Controls
        components.append(self._display.render_controls(state))

        return Group(*components)

    def _handle_command(self, command: Command) -> None:
        """
        Handle a keyboard command.

        Args:
            command: The command to handle.
        """
        if self._meeting_manager is None:
            return

        state = self._meeting_manager.state

        if command == Command.PAUSE_RESUME:
            if state == MeetingState.PAUSED:
                self._meeting_manager.resume()
            elif state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW):
                self._meeting_manager.pause()

        elif command == Command.NEXT_SPEAKER:
            if state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW, MeetingState.TRANSITION):
                self._meeting_manager.next_speaker()

        elif command == Command.SKIP_SPEAKER:
            if state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW, MeetingState.TRANSITION):
                self._meeting_manager.skip_speaker()

        elif command == Command.ADD_TIME:
            if state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW):
                self._meeting_manager.add_time(TIME_INCREMENT_SECONDS)

        elif command == Command.SUBTRACT_TIME:
            if state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW):
                self._meeting_manager.add_time(-TIME_INCREMENT_SECONDS)

        elif command == Command.MARK_ABSENT:
            self._handle_absent_picker()

        elif command == Command.QUIT:
            self._quit_meeting()

    def _handle_absent_picker(self) -> None:
        """Show and handle the absent member picker."""
        if self._meeting_manager is None:
            return

        speakers = self._meeting_manager.speaker_queue
        if not speakers:
            return

        self._in_absent_picker = True
        self._display.clear()
        self._console.print(self._display.render_absent_picker(speakers))

        while self._in_absent_picker:
            result = self._keyboard.process_input(timeout=0.5)
            if result is None:
                continue

            if result.command == Command.CANCEL:
                self._in_absent_picker = False
                return

            num = KeyboardHandler.get_number_from_command(result.command)
            if num is not None and 1 <= num <= len(speakers):
                member = speakers[num - 1]
                self._meeting_manager.mark_absent(member.id)
                self._in_absent_picker = False
                return

    def _quit_meeting(self) -> None:
        """End the meeting and quit."""
        if self._meeting_manager is not None and self._meeting_manager.is_active:
            self._meeting_manager.end_meeting(save_history=True)
        self._running = False

    def _reset_interaction_time(self) -> None:
        """Reset the inactivity timer to now."""
        self._last_interaction_time = time.monotonic()

    def _check_inactivity(self) -> bool:
        """Check if the inactivity timeout has been exceeded."""
        if self._last_interaction_time == 0.0:
            return False
        elapsed = time.monotonic() - self._last_interaction_time
        return elapsed > self._config.timer.inactivity_timeout_seconds

    def _handle_interrupt(self, _signum: int, _frame: object) -> None:
        """Handle interrupt signal."""
        self._running = False

    def _cleanup(self) -> None:
        """Cleanup resources."""
        if self._meeting_manager is not None and self._meeting_manager.is_active:
            # Don't save if interrupted - recovery will handle it
            pass


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    from src import __version__

    parser = argparse.ArgumentParser(
        description="Daily Standup Timer - CLI Interface",
        prog="daily-timer",
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--team",
        "-t",
        type=str,
        help="Team ID to use (skips selection menu)",
    )
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default="config.json",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    return parser.parse_args()


def setup_logging(verbose: bool) -> None:
    """
    Configure logging with rotating file handler.

    Console logging is disabled to avoid interfering with Rich Live display.
    All logs go to file only. Use `tail -f logs/daily_timer.log` to monitor.

    Args:
        verbose: If True, enable DEBUG level in file logging.
    """
    log_level = logging.DEBUG if verbose else logging.INFO

    # Create logs directory if needed
    log_dir = Path(LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / LOG_FILE_NAME

    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # Root logger setup
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear any existing handlers
    root_logger.handlers.clear()

    # File handler only - no console to avoid interfering with Rich Live
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    logging.info(f"Logging initialized: file={log_file}, level={logging.getLevelName(log_level)}")


def main() -> int:
    """Main entry point for the CLI."""
    args = parse_args()

    # Setup logging with rotation
    setup_logging(args.verbose)

    # Load configuration
    config_mgr = ConfigManager(Path(args.config))
    config = config_mgr.load()

    # Initialize team repository
    teams_dir = Path(config.teams.directory)
    team_repo = TeamRepository(teams_dir=teams_dir)

    # Create and run app
    app = CLIApp(config=config, team_repo=team_repo)
    return app.run(team_id=args.team)


if __name__ == "__main__":
    sys.exit(main())
