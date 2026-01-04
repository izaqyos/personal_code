"""
Terminal display rendering using Rich.

This module provides Rich-based terminal UI components
for the CLI interface including timers, speaker queues,
and status displays.
"""

from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table
from rich.text import Text

from src.core.constants import DEFAULT_WARNING_THRESHOLD_SECONDS
from src.core.models import MeetingState, TeamMember
from src.core.state_manager import SpeakerRecord
from src.core.time_utils import format_time_mmss

# Color scheme for Rich (terminal color names)
COLORS = {
    "normal": "green",
    "warning": "yellow",
    "overtime": "red",
    "paused": "blue",
    "transition": "cyan",
    "completed": "dim",
    "current": "bold white",
    "pending": "dim white",
}


class CLIDisplay:
    """
    Rich-based terminal display for the standup timer.

    Renders the meeting state, timers, speaker queue,
    and available controls to the terminal.
    """

    def __init__(self, console: Console | None = None) -> None:
        """
        Initialize the display.

        Args:
            console: Optional Rich console instance.
        """
        self.console = console or Console()
        self._warning_threshold = DEFAULT_WARNING_THRESHOLD_SECONDS

    def set_warning_threshold(self, seconds: int) -> None:
        """Set the warning threshold in seconds."""
        self._warning_threshold = seconds

    def render_header(self, team_name: str, session_id: str | None = None) -> Panel:
        """
        Render the header banner.

        Args:
            team_name: Name of the team.
            session_id: Optional session identifier.

        Returns:
            A Rich Panel with the header.
        """
        title = Text("Daily Standup Timer", style="bold white")
        subtitle = Text(f"Team: {team_name}", style="cyan")
        if session_id:
            subtitle.append(f" | Session: {session_id}", style="dim")

        content = Group(
            Align.center(title),
            Align.center(subtitle),
        )

        return Panel(content, border_style="blue", padding=(0, 2))

    def render_timer(
        self,
        remaining_seconds: float,
        total_seconds: float,
        state: MeetingState,
        speaker_name: str | None = None,
    ) -> Panel:
        """
        Render the main timer display.

        Args:
            remaining_seconds: Time remaining in seconds.
            total_seconds: Total allocated time in seconds.
            state: Current meeting state.
            speaker_name: Name of current speaker.

        Returns:
            A Rich Panel with the timer display.
        """
        # Determine color based on state and remaining time
        if state == MeetingState.PAUSED:
            color = COLORS["paused"]
            status = "PAUSED"
        elif state == MeetingState.TRANSITION:
            color = COLORS["transition"]
            status = "TRANSITION"
        elif remaining_seconds < 0:
            color = COLORS["overtime"]
            status = "OVERTIME"
        elif remaining_seconds <= self._warning_threshold:
            color = COLORS["warning"]
            status = "WARNING"
        else:
            color = COLORS["normal"]
            status = "SPEAKING"

        # Format time using shared utility
        time_str = format_time_mmss(remaining_seconds)

        # Create timer text
        timer_text = Text(time_str, style=f"bold {color}")
        timer_text.stylize(f"bold {color}")

        # Add speaker name if available
        content_items = []
        if speaker_name:
            speaker_text = Text(speaker_name, style="bold white")
            content_items.append(Align.center(speaker_text))

        content_items.append(Align.center(timer_text))

        # Add status indicator
        status_text = Text(f"[{status}]", style=color)
        content_items.append(Align.center(status_text))

        # Progress bar (only if not overtime)
        if total_seconds > 0 and state not in (MeetingState.TRANSITION, MeetingState.PAUSED):
            progress = Progress(
                TextColumn(""),
                BarColumn(bar_width=40, complete_style=color, finished_style=color),
                TextColumn(""),
                expand=False,
            )
            task = progress.add_task("", total=total_seconds)
            elapsed = max(0, total_seconds - remaining_seconds)
            progress.update(task, completed=min(elapsed, total_seconds))
            content_items.append(Align.center(progress))

        content = Group(*content_items)
        return Panel(content, border_style=color, title="Timer", padding=(1, 2))

    def render_queue(
        self,
        speakers: list[TeamMember],
        current_index: int,
        speaker_records: list[SpeakerRecord],
    ) -> Panel:
        """
        Render the speaker queue.

        Args:
            speakers: List of speakers in order.
            current_index: Index of current speaker (-1 if not started).
            speaker_records: Records with timing info.

        Returns:
            A Rich Panel with the queue display.
        """
        table = Table(show_header=True, header_style="bold", box=None, padding=(0, 1))
        table.add_column("#", style="dim", width=3)
        table.add_column("Speaker", min_width=15)
        table.add_column("Status", width=12)
        table.add_column("Time", width=8)

        # Build a lookup for speaker records
        records_by_id = {r.member.id: r for r in speaker_records}

        for i, speaker in enumerate(speakers):
            record = records_by_id.get(speaker.id)
            is_current = i == current_index
            is_completed = i < current_index
            is_absent = record.is_absent if record else False
            is_skipped = record.skipped if record else False

            # Determine style and status
            if is_absent:
                style = "dim strike"
                status = "Absent"
            elif is_skipped:
                style = "dim strike"
                status = "Skipped"
            elif is_current:
                style = COLORS["current"]
                status = "Speaking"
            elif is_completed:
                style = COLORS["completed"]
                status = "Done"
            else:
                style = COLORS["pending"]
                status = "Pending"

            # Format time
            time_str = ""
            if record and (is_completed or is_current):
                time_str = format_time_mmss(record.elapsed_seconds, show_sign=False)
                if record.overtime_seconds > 0:
                    time_str = f"[red]{time_str}[/red]"

            # Add marker for current speaker
            marker = ">" if is_current else ""

            table.add_row(
                f"{marker}{i + 1}",
                speaker.display_name,
                status,
                time_str,
                style=style,
            )

        return Panel(table, title="Speaker Queue", border_style="blue")

    def render_controls(self, state: MeetingState) -> Panel:
        """
        Render available keyboard controls.

        Args:
            state: Current meeting state.

        Returns:
            A Rich Panel with available controls.
        """
        controls = []

        if state == MeetingState.PAUSED:
            controls.append(("[p]", "Resume"))
        elif state in (MeetingState.SPEAKING, MeetingState.GRACE):
            controls.append(("[p]", "Pause"))

        if state in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.TRANSITION):
            controls.append(("[n]", "Next"))
            controls.append(("[s]", "Skip"))

        if state in (MeetingState.SPEAKING, MeetingState.GRACE):
            controls.append(("[+]", "+30s"))
            controls.append(("[-]", "-30s"))

        controls.append(("[a]", "Absent"))
        controls.append(("[q]", "Quit"))

        # Format controls
        control_text = Text()
        for i, (key, action) in enumerate(controls):
            if i > 0:
                control_text.append("  |  ", style="dim")
            control_text.append(key, style="bold cyan")
            control_text.append(f" {action}", style="white")

        return Panel(
            Align.center(control_text),
            border_style="dim",
            padding=(0, 1),
        )

    def render_transition(
        self,
        next_speaker: str,
        remaining_seconds: float,
    ) -> Panel:
        """
        Render the transition screen between speakers.

        Args:
            next_speaker: Name of the upcoming speaker.
            remaining_seconds: Transition time remaining.

        Returns:
            A Rich Panel for the transition display.
        """
        content_items = [
            Align.center(Text("Next Up", style="dim")),
            Align.center(Text(next_speaker, style="bold cyan")),
            Align.center(Text("")),
            Align.center(Text(f"Starting in {int(remaining_seconds)}s", style="yellow")),
        ]

        content = Group(*content_items)
        return Panel(content, border_style="cyan", title="Transition", padding=(1, 2))

    def render_meeting_summary(
        self,
        total_duration: float,
        speaker_records: list[SpeakerRecord],
    ) -> Panel:
        """
        Render the meeting summary after completion.

        Args:
            total_duration: Total meeting duration in seconds.
            speaker_records: Final speaker records.

        Returns:
            A Rich Panel with the summary.
        """
        # Format total time
        total_str = format_time_mmss(total_duration, show_sign=False)

        table = Table(show_header=True, header_style="bold", box=None)
        table.add_column("Speaker", min_width=15)
        table.add_column("Time", width=10)
        table.add_column("Status", width=10)

        for record in speaker_records:
            if record.is_absent:
                status = "[dim]Absent[/dim]"
                time_str = "-"
            elif record.skipped:
                status = "[dim]Skipped[/dim]"
                time_str = "-"
            else:
                status = "[green]Complete[/green]"
                time_str = format_time_mmss(record.elapsed_seconds, show_sign=False)
                if record.overtime_seconds > 0:
                    time_str = f"[red]{time_str}[/red]"

            table.add_row(record.member.display_name, time_str, status)

        content = Group(
            Align.center(Text("Meeting Complete!", style="bold green")),
            Align.center(Text("")),
            Align.center(Text(f"Total Duration: {total_str}", style="cyan")),
            Align.center(Text("")),
            table,
        )

        return Panel(content, title="Summary", border_style="green", padding=(1, 2))

    def render_recovery_prompt(
        self,
        team_id: str,
        started_at: str,
        speaker_index: int,
        total_speakers: int,
    ) -> Panel:
        """
        Render the recovery session prompt.

        Args:
            team_id: Team identifier.
            started_at: When the session started.
            speaker_index: Current speaker position.
            total_speakers: Total number of speakers.

        Returns:
            A Rich Panel with recovery info.
        """
        content = Group(
            Align.center(Text("Previous Session Found", style="bold yellow")),
            Align.center(Text("")),
            Align.center(Text(f"Team: {team_id}", style="white")),
            Align.center(Text(f"Started: {started_at}", style="white")),
            Align.center(Text(f"Progress: Speaker {speaker_index + 1}/{total_speakers}", style="white")),
            Align.center(Text("")),
            Align.center(Text("[r] Resume  |  [n] New Meeting", style="cyan")),
        )

        return Panel(content, title="Recovery", border_style="yellow", padding=(1, 2))

    def render_team_selection(self, teams: list[str]) -> Panel:
        """
        Render team selection menu.

        Args:
            teams: List of available team IDs.

        Returns:
            A Rich Panel with team options.
        """
        content_items = [
            Align.center(Text("Select a Team", style="bold")),
            Align.center(Text("")),
        ]

        for i, team in enumerate(teams, 1):
            content_items.append(
                Align.center(Text(f"[{i}] {team}", style="cyan"))
            )

        content_items.append(Align.center(Text("")))
        content_items.append(Align.center(Text("Enter number or [q] to quit", style="dim")))

        content = Group(*content_items)
        return Panel(content, title="Teams", border_style="blue", padding=(1, 2))

    def render_absent_picker(self, speakers: list[TeamMember]) -> Panel:
        """
        Render absent member picker.

        Args:
            speakers: List of speakers to choose from.

        Returns:
            A Rich Panel with speaker options.
        """
        content_items = [
            Align.center(Text("Mark as Absent", style="bold")),
            Align.center(Text("")),
        ]

        for i, speaker in enumerate(speakers, 1):
            content_items.append(
                Align.center(Text(f"[{i}] {speaker.display_name}", style="cyan"))
            )

        content_items.append(Align.center(Text("")))
        content_items.append(Align.center(Text("Enter number or [Esc] to cancel", style="dim")))

        content = Group(*content_items)
        return Panel(content, title="Absent", border_style="yellow", padding=(1, 2))

    def get_timer_color(
        self,
        remaining_seconds: float,
        state: MeetingState,
    ) -> str:
        """
        Get the appropriate color for the current timer state.

        Args:
            remaining_seconds: Time remaining.
            state: Current meeting state.

        Returns:
            Color name string.
        """
        if state == MeetingState.PAUSED:
            return COLORS["paused"]
        elif remaining_seconds < 0:
            return COLORS["overtime"]
        elif remaining_seconds <= self._warning_threshold:
            return COLORS["warning"]
        return COLORS["normal"]

    def clear(self) -> None:
        """Clear the terminal screen."""
        self.console.clear()

    def print(self, renderable: object) -> None:
        """Print to the console."""
        self.console.print(renderable)
