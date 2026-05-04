#!/usr/bin/env python3
"""
Main entry point for Daily Standup Timer.

Supports CLI, Streamlit UI, and history viewing modes.
"""

import argparse
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

from src.core.time_utils import format_team_name


def show_history(team_id: str | None, days: int, limit: int) -> int:
    """
    Display meeting history in a formatted table.

    Args:
        team_id: Team ID to show history for (None for team selection).
        days: Number of days to look back.
        limit: Maximum number of entries to show.

    Returns:
        Exit code.
    """
    from rich.console import Console
    from rich.table import Table

    from src.data.config_manager import ConfigManager
    from src.data.history_repository import HistoryRepository
    from src.data.team_repository import TeamRepository

    console = Console()

    # Load config and get team
    config_mgr = ConfigManager()
    config = config_mgr.load()
    teams_dir = Path(config.teams.directory)
    team_repo = TeamRepository(teams_dir=teams_dir)

    # Select team if not provided
    if not team_id:
        teams = team_repo.list_teams()
        if not teams:
            console.print("[red]No teams found![/red]")
            return 1
        if len(teams) == 1:
            team_id = teams[0]
        else:
            console.print("\n[bold]Available Teams:[/bold]")
            for i, t in enumerate(teams, 1):
                console.print(f"  {i}. {t}")
            console.print()
            try:
                choice = input("Select team number: ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(teams):
                    team_id = teams[idx]
                else:
                    console.print("[red]Invalid selection[/red]")
                    return 1
            except (ValueError, KeyboardInterrupt):
                console.print("\n[yellow]Cancelled[/yellow]")
                return 0

    # Load history
    data_dir = Path("data")
    history_repo = HistoryRepository(team_id=team_id, data_dir=data_dir)

    # Calculate date range
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    entries = history_repo.get_entries(start_date=start_date, end_date=end_date)

    if not entries:
        formatted_team = format_team_name(team_id)
        console.print(f"\n[yellow]No meetings found for team '{formatted_team}' in the last {days} days.[/yellow]")
        return 0

    # Apply limit (most recent first)
    entries = entries[-limit:] if limit < len(entries) else entries
    entries = list(reversed(entries))  # Show newest first

    # Get formatted team name with emoji
    formatted_team = format_team_name(team_id)

    # Display summary
    console.print(f"\n[bold cyan]Meeting History: {formatted_team}[/bold cyan]")
    console.print(f"[dim]Showing {len(entries)} meetings from last {days} days[/dim]\n")

    # Create meetings table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Date", style="cyan", width=12)
    table.add_column("Time", style="dim", width=15)
    table.add_column("Duration", justify="right", width=10)
    table.add_column("Speakers", justify="center", width=10)
    table.add_column("On-Time", justify="center", width=10)
    table.add_column("Overtime", justify="right", width=10)

    total_duration = 0.0
    total_overtime = 0.0
    total_speakers = 0
    on_time_count = 0

    for entry in entries:
        # Calculate stats
        duration_mins = entry.total_duration_seconds / 60
        total_duration += entry.total_duration_seconds

        present = [p for p in entry.participants if p.status.value == "present"]
        overtime = sum(p.overtime_seconds for p in present)
        total_overtime += overtime
        total_speakers += len(present)

        speakers_on_time = sum(1 for p in present if p.overtime_seconds == 0)
        on_time_count += speakers_on_time

        # Format values
        time_range = f"{entry.start_time[:5]}-{entry.end_time[:5]}"
        duration_str = f"{duration_mins:.1f} min"
        speakers_str = str(len(present))
        on_time_str = f"{speakers_on_time}/{len(present)}"
        overtime_str = f"{overtime:.0f}s" if overtime > 0 else "-"

        # Color overtime
        if overtime > 60:
            overtime_str = f"[red]{overtime_str}[/red]"
        elif overtime > 0:
            overtime_str = f"[yellow]{overtime_str}[/yellow]"

        table.add_row(
            entry.date,
            time_range,
            duration_str,
            speakers_str,
            on_time_str,
            overtime_str,
        )

    console.print(table)

    # Summary stats
    if entries:
        avg_duration = (total_duration / len(entries)) / 60
        on_time_rate = (on_time_count / total_speakers * 100) if total_speakers > 0 else 0

        console.print()
        summary = Table(show_header=False, box=None)
        summary.add_column("Label", style="bold")
        summary.add_column("Value")
        summary.add_row("Total Meetings:", str(len(entries)))
        summary.add_row("Avg Duration:", f"{avg_duration:.1f} min")
        summary.add_row("On-Time Rate:", f"{on_time_rate:.0f}%")
        summary.add_row("Total Overtime:", f"{total_overtime:.0f}s")
        console.print(summary)

    # Option to show detailed view
    console.print("\n[dim]Use --limit N to see more entries, --days N to change date range[/dim]")

    return 0


KNOWN_BANNER_FIELDS: frozenset[str] = frozenset(
    {"sprint", "sprint_week", "champion", "dod", "next_event"}
)


def _parse_banner_value(
    value: str | None,
    known: frozenset[str] | set[str] = KNOWN_BANNER_FIELDS,
) -> tuple[list[str] | None, str | None]:
    """Disambiguate the value passed to bare `-b VALUE`.

    Returns (fields_list, free_text). Exactly one is non-None, or both None
    when no value is given.
    """
    if value is None or value == "":
        return (None, None)
    if " " in value:
        return (None, value)
    tokens = value.split(",")
    if all(tok in known for tok in tokens):
        return (tokens, None)
    return (None, value)


def _build_parser() -> argparse.ArgumentParser:
    from src import __version__

    parser = argparse.ArgumentParser(
        description="Daily Standup Timer",
        prog="daily-timer",
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["cli", "ui", "history"],
        default="ui",
        help="Mode: 'ui' for Streamlit (default), 'cli' for terminal, 'history' to view past meetings",
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
    parser.add_argument(
        "--days",
        "-d",
        type=int,
        default=30,
        help="Number of days to show in history mode (default: 30)",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=20,
        help="Maximum entries to show in history mode (default: 20)",
    )
    parser.add_argument(
        "-b",
        dest="banner_value",
        nargs="?",
        const="",
        default=None,
        help="Show banner; optional VALUE is fields-csv (sprint,dod) or free text.",
    )
    parser.add_argument(
        "--banner-fields",
        type=lambda s: [t.strip() for t in s.split(",") if t.strip()],
        default=None,
        help="Explicit comma-separated cadence fields to show.",
    )
    parser.add_argument(
        "--banner-text",
        type=str,
        default=None,
        help="Free text line shown under the cadence banner.",
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Force banner off, overriding -b and config.",
    )
    return parser


def main() -> int:
    """Main entry point with mode selection."""
    parser = _build_parser()
    args = parser.parse_args()

    # Disambiguate bare `-b VALUE` into fields or text if not already explicit.
    derived_fields, derived_text = _parse_banner_value(args.banner_value, KNOWN_BANNER_FIELDS)
    if args.banner_fields is None:
        args.banner_fields = derived_fields
    if args.banner_text is None:
        args.banner_text = derived_text

    if args.mode == "history":
        return show_history(args.team, args.days, args.limit)

    elif args.mode == "ui":
        # Launch Streamlit UI
        ui_path = Path(__file__).parent / "src" / "ui" / "app.py"
        cmd = ["streamlit", "run", str(ui_path)]
        if args.team:
            cmd.extend(["--", "--team", args.team])
        return subprocess.call(cmd)

    else:
        # Run CLI mode
        from src.cli.app import main as cli_main

        # Reconstruct sys.argv for CLI
        sys.argv = ["daily-timer"]
        if args.team:
            sys.argv.extend(["--team", args.team])
        if args.config != "config.json":
            sys.argv.extend(["--config", args.config])
        if args.verbose:
            sys.argv.append("--verbose")

        return cli_main()


if __name__ == "__main__":
    sys.exit(main())
