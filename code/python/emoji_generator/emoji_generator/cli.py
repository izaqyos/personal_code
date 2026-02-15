"""
CLI and REPL interface for Emoji Generator.

Two modes:
  - CLI (one-shot): `devmoji "pr merged"` -> shows matches, copies to clipboard
  - REPL (interactive): `devmoji --repl` -> loop of query/pick/copy
"""

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from emoji_generator.engine import EmojiMatchingEngine, MatchResult, MIN_CONFIDENCE
from emoji_generator.registry import (
    EmojiEntry,
    load_registry,
    get_default_yaml_path,
    generate_yaml_snippet,
    append_entry_to_yaml,
)

console = Console()


def copy_to_clipboard(text: str) -> bool:
    """Copy text to system clipboard. Returns True on success."""
    try:
        import pyperclip

        pyperclip.copy(text)
        return True
    except Exception:
        return False


def display_results(results: list[MatchResult], query: str) -> None:
    """Display search results as a rich table."""
    table = Table(
        title=f'Results for: "{query}"',
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
        title_style="bold",
    )
    table.add_column("#", style="bold yellow", width=3, justify="right")
    table.add_column("Emoji", width=8, justify="center")
    table.add_column("Description", style="white", min_width=30)
    table.add_column("Score", style="green", width=7, justify="right")

    for i, result in enumerate(results, 1):
        score_pct = f"{result.score:.0%}"
        table.add_row(
            str(i),
            result.entry.emoji,
            result.entry.description,
            score_pct,
        )

    console.print()
    console.print(table)


def display_no_match(query: str, yaml_path: Path) -> None:
    """Display the no-match message with a ready-to-paste YAML snippet."""
    snippet = generate_yaml_snippet(query)

    console.print()
    console.print(
        Panel(
            f'[bold yellow]No good match found for:[/bold yellow] "{query}"\n\n'
            f"[dim]Best scores were below {MIN_CONFIDENCE:.0%} confidence threshold.[/dim]\n\n"
            f"[bold green]To add this, paste the following into emojis.yaml:[/bold green]\n"
            f"[dim]{yaml_path}[/dim]\n"
            f"[cyan]{snippet}[/cyan]",
            title="[bold red]No Match[/bold red]",
            border_style="yellow",
        )
    )


def display_all_emojis(entries: list[EmojiEntry]) -> None:
    """Display all available emojis in a table."""
    table = Table(
        title="All Available Dev Emojis",
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
        title_style="bold",
    )
    table.add_column("#", style="dim", width=3, justify="right")
    table.add_column("Emoji", width=8, justify="center")
    table.add_column("Name", style="yellow", min_width=20)
    table.add_column("Description", style="white", min_width=35)

    for i, entry in enumerate(entries, 1):
        table.add_row(str(i), entry.emoji, entry.name, entry.description)

    console.print()
    console.print(table)
    console.print(f"\n[dim]Total: {len(entries)} emoji entries[/dim]")


def prompt_selection(results: list[MatchResult], no_copy: bool = False) -> str | None:
    """Prompt the user to pick a result. Returns the selected emoji or None."""
    if not results:
        return None

    console.print(
        "\n[bold]Pick a number[/bold] [dim](or Enter for #1, 'q' to skip):[/dim] ",
        end="",
    )

    try:
        choice = input().strip()
    except (EOFError, KeyboardInterrupt):
        return None

    if choice.lower() == "q" or choice.lower() == "quit":
        return None

    # Default to first result
    if choice == "":
        idx = 0
    else:
        try:
            idx = int(choice) - 1
        except ValueError:
            console.print("[yellow]Invalid choice.[/yellow]")
            return None

    if 0 <= idx < len(results):
        emoji = results[idx].entry.emoji
        if not no_copy:
            if copy_to_clipboard(emoji):
                console.print(f"\n[bold green]Copied to clipboard:[/bold green] {emoji}")
            else:
                console.print(
                    f"\n[yellow]Could not copy to clipboard.[/yellow] Emoji: {emoji}"
                )
        else:
            console.print(f"\n[bold]Selected:[/bold] {emoji}")
        return emoji
    else:
        console.print("[yellow]Invalid choice.[/yellow]")
        return None


def handle_repl_add(query: str, yaml_path: Path, engine: EmojiMatchingEngine) -> None:
    """Handle the [a]dd flow in REPL mode -- add a new emoji entry and hot-reload."""
    console.print("\n[bold cyan]Add new emoji entry[/bold cyan]")
    console.print(f'[dim]Description will be:[/dim] "{query.lower().strip()}"')
    console.print("[bold]Enter the emoji to use[/bold] [dim](e.g. 🎯🔥):[/dim] ", end="")

    try:
        emoji_input = input().strip()
    except (EOFError, KeyboardInterrupt):
        console.print("[dim]Cancelled.[/dim]")
        return

    if not emoji_input:
        console.print("[dim]Cancelled.[/dim]")
        return

    append_entry_to_yaml(yaml_path, emoji_input, query)
    console.print(f"[bold green]Added![/bold green] {emoji_input} -> \"{query.lower().strip()}\"")

    # Hot-reload the engine
    entries = load_registry(yaml_path)
    engine.rebuild(entries)
    console.print("[dim]Engine reloaded with new entry.[/dim]")


def run_single_query(
    engine: EmojiMatchingEngine,
    query: str,
    top_k: int,
    no_copy: bool,
    first: bool,
    yaml_path: Path,
) -> None:
    """Run a single query and display results."""
    results = engine.search(query, top_k=top_k)

    if not results:
        display_no_match(query, yaml_path)
        return

    display_results(results, query)

    if first:
        # Auto-select first result
        emoji = results[0].entry.emoji
        if not no_copy:
            if copy_to_clipboard(emoji):
                console.print(f"\n[bold green]Copied to clipboard:[/bold green] {emoji}")
            else:
                console.print(f"\n[yellow]Could not copy to clipboard.[/yellow] Emoji: {emoji}")
        else:
            console.print(f"\n[bold]Selected:[/bold] {emoji}")
    else:
        prompt_selection(results, no_copy=no_copy)


def run_repl(engine: EmojiMatchingEngine, top_k: int, no_copy: bool, yaml_path: Path) -> None:
    """Run the interactive REPL loop."""
    try:
        from prompt_toolkit import PromptSession
        from prompt_toolkit.history import FileHistory
        from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

        history_path = Path.home() / ".devmoji_history"
        session = PromptSession(
            history=FileHistory(str(history_path)),
            auto_suggest=AutoSuggestFromHistory(),
        )
        use_prompt_toolkit = True
    except ImportError:
        use_prompt_toolkit = False

    console.print(
        Panel(
            "[bold cyan]Dev Emoji Generator[/bold cyan] -- Interactive Mode\n\n"
            "Type a phrase to find matching emojis.\n"
            "Commands: [bold]quit[/bold] | [bold]list[/bold] | [bold]help[/bold]",
            border_style="cyan",
        )
    )

    while True:
        try:
            if use_prompt_toolkit:
                query = session.prompt("devmoji> ").strip()
            else:
                console.print("[bold cyan]devmoji>[/bold cyan] ", end="")
                query = input().strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Bye![/dim]")
            break

        if not query:
            continue

        if query.lower() in ("quit", "exit", "q"):
            console.print("[dim]Bye![/dim]")
            break

        if query.lower() == "list":
            display_all_emojis(engine.entries)
            continue

        if query.lower() == "help":
            console.print(
                "\n[bold]Commands:[/bold]\n"
                "  [cyan]<any phrase>[/cyan]  Search for matching emojis\n"
                "  [cyan]list[/cyan]          Show all available emojis\n"
                "  [cyan]quit[/cyan]          Exit the REPL\n"
                "  [cyan]help[/cyan]          Show this help\n"
            )
            continue

        results = engine.search(query, top_k=top_k)

        if not results:
            display_no_match(query, yaml_path)
            console.print(
                "\n[bold]Want to add it?[/bold] [dim]([/dim][bold cyan]a[/bold cyan][dim])dd"
                " / any other key to skip:[/dim] ",
                end="",
            )
            try:
                add_choice = input().strip().lower()
            except (EOFError, KeyboardInterrupt):
                continue

            if add_choice == "a":
                handle_repl_add(query, yaml_path, engine)
            continue

        display_results(results, query)
        prompt_selection(results, no_copy=no_copy)


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="devmoji",
        description="Find the perfect dev emoji combo using natural language.",
        epilog="Examples:\n"
        '  devmoji "pr merged"          Search for PR merged emoji\n'
        '  devmoji -1 "deployed"        Auto-pick top result\n'
        "  devmoji --repl               Interactive mode\n"
        "  devmoji --list               Show all emojis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "query",
        nargs="?",
        default=None,
        help="Natural language query (e.g. 'pr approved and merged')",
    )
    parser.add_argument(
        "-r",
        "--repl",
        action="store_true",
        help="Start interactive REPL mode",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        metavar="N",
        help="Number of results to show (default: 5)",
    )
    parser.add_argument(
        "-1",
        "--first",
        action="store_true",
        help="Auto-select the top result (skip prompt)",
    )
    parser.add_argument(
        "--no-copy",
        action="store_true",
        help="Don't copy to clipboard, just display",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_all",
        help="List all available emojis",
    )
    parser.add_argument(
        "--yaml",
        type=str,
        default=None,
        metavar="PATH",
        help="Path to custom emojis.yaml file",
    )

    return parser


def main() -> None:
    """Main entry point for the CLI."""
    parser = build_parser()
    args = parser.parse_args()

    # Determine YAML path
    yaml_path = Path(args.yaml) if args.yaml else get_default_yaml_path()

    # Load registry
    try:
        entries = load_registry(yaml_path)
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] YAML file not found: {yaml_path}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error loading registry:[/bold red] {e}")
        sys.exit(1)

    if not entries:
        console.print("[bold yellow]Warning:[/bold yellow] No emoji entries found in registry.")
        sys.exit(1)

    # Build engine
    engine = EmojiMatchingEngine(entries)

    # List all emojis
    if args.list_all:
        display_all_emojis(entries)
        return

    # REPL mode
    if args.repl:
        run_repl(engine, top_k=args.top, no_copy=args.no_copy, yaml_path=yaml_path)
        return

    # CLI mode requires a query
    if not args.query:
        parser.print_help()
        sys.exit(1)

    run_single_query(
        engine=engine,
        query=args.query,
        top_k=args.top,
        no_copy=args.no_copy,
        first=args.first,
        yaml_path=yaml_path,
    )
