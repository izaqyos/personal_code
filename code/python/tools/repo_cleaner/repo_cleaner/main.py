"""CLI entry point for Repo Cleaner."""

import sys
from pathlib import Path
from typing import List, Optional

import click

from repo_cleaner import __version__
from repo_cleaner.config.manager import ConfigManager
from repo_cleaner.core.exceptions import RepoCleanerError
from repo_cleaner.core.logger import setup_logger
from repo_cleaner.detectors import ALL_DETECTORS
from repo_cleaner.utils.prompts import print_error, print_info, print_success


# List of available language names
AVAILABLE_LANGUAGES = [d.name for d in ALL_DETECTORS]


def validate_languages(
    ctx: click.Context,
    param: click.Parameter,
    value: Optional[str],
) -> Optional[List[str]]:
    """Validate and parse the languages parameter.
    
    Args:
        ctx: Click context
        param: Click parameter
        value: Comma-separated language string
        
    Returns:
        List of language names or None
    """
    if value is None:
        return None
    
    languages = [lang.strip().lower() for lang in value.split(",")]
    
    invalid = [lang for lang in languages if lang not in AVAILABLE_LANGUAGES]
    if invalid:
        raise click.BadParameter(
            f"Unknown language(s): {', '.join(invalid)}. "
            f"Available: {', '.join(AVAILABLE_LANGUAGES)}"
        )
    
    return languages


@click.command()
@click.option(
    "--target", "-t",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    default=".",
    help="Target directory to clean (default: current directory)",
)
@click.option(
    "--dry-run", "-n",
    is_flag=True,
    default=False,
    help="Preview changes without deleting anything",
)
@click.option(
    "--force", "-f",
    is_flag=True,
    default=False,
    help="Skip all confirmation prompts (non-interactive mode)",
)
@click.option(
    "--config", "-c",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default=None,
    help="Path to configuration file",
)
@click.option(
    "--languages", "-l",
    callback=validate_languages,
    default=None,
    help=f"Comma-separated list of languages to clean (default: auto-detect). "
         f"Available: {', '.join(AVAILABLE_LANGUAGES)}",
)
@click.option(
    "--exclude", "-e",
    multiple=True,
    help="Patterns to exclude (can be specified multiple times)",
)
@click.option(
    "--rescan",
    is_flag=True,
    default=False,
    help="Force a fresh scan (ignore cached layout)",
)
@click.option(
    "--detailed-report",
    is_flag=True,
    default=False,
    help="Include detailed item list in cleanup report",
)
@click.option(
    "--history",
    is_flag=True,
    default=False,
    help="Show cleanup history and exit",
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    default=False,
    help="Show verbose output",
)
@click.option(
    "--quiet", "-q",
    is_flag=True,
    default=False,
    help="Suppress non-error output",
)
@click.option(
    "--list-languages",
    is_flag=True,
    default=False,
    help="List available language cleaners and exit",
)
@click.version_option(version=__version__, prog_name="repo-cleaner")
def main(
    target: str,
    dry_run: bool,
    force: bool,
    config: Optional[str],
    languages: Optional[List[str]],
    exclude: tuple,
    rescan: bool,
    detailed_report: bool,
    history: bool,
    verbose: bool,
    quiet: bool,
    list_languages: bool,
) -> None:
    """Repo Cleaner - Clean build artifacts from your repositories.
    
    This tool detects and removes build artifacts, cache directories,
    and other generated files from various programming languages and
    frameworks including Python, Node.js, Java, C/C++, React, Angular,
    and Vue.js.
    
    Supports monorepos with multiple projects - it will recursively scan
    for projects and clean each one, with per-project confirmation prompts
    (unless -f/--force is used).
    
    \b
    Examples:
        repo-cleaner                    # Clean current directory interactively
        repo-cleaner -t ~/projects/app  # Clean specific directory
        repo-cleaner -n                 # Dry run (preview only)
        repo-cleaner -f                 # Force mode (no prompts)
        repo-cleaner -l python,node     # Clean only Python and Node.js artifacts
        repo-cleaner -e "vendor/**"     # Exclude vendor directory
        repo-cleaner --rescan           # Force fresh project scan
        repo-cleaner --history          # Show cleanup history
    """
    # List languages and exit
    if list_languages:
        print_info("Available language cleaners:")
        for detector in ALL_DETECTORS:
            print(f"  - {detector.name}: {detector.display_name}")
        return
    
    # Setup logging
    import logging
    if quiet:
        log_level = logging.ERROR
    elif verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    setup_logger(level=log_level)
    
    # Show history and exit
    if history:
        from repo_cleaner.core.history import HistoryManager
        history_manager = HistoryManager()
        history_manager.print_history(limit=20)
        return
    
    # Resolve target path
    target_path = Path(target).resolve()
    
    # Create configuration manager
    config_path = Path(config) if config else None
    config_manager = ConfigManager(
        config_path=config_path,
        target_dir=target_path,
    )
    
    try:
        # Load configuration
        config_manager.load()
        
        # Use MonorepoCleaner for recursive scanning
        from repo_cleaner.core.monorepo_cleaner import MonorepoCleaner
        
        cleaner = MonorepoCleaner(
            config=config_manager,
            dry_run=dry_run,
            force=force,
            verbose=verbose,
            rescan=rescan,
            detailed_report=detailed_report,
        )
        
        # Show banner
        if not quiet:
            print()
            print("=" * 60)
            print(f"  Repo Cleaner v{__version__}")
            print(f"  Target: {target_path}")
            if dry_run:
                print("  Mode: DRY RUN (no files will be deleted)")
            if force:
                print("  Mode: Force (no prompts)")
            print("=" * 60)
        
        # Execute cleaning
        exclude_list = list(exclude) if exclude else None
        report = cleaner.clean(
            path=target_path,
            languages=languages,
            exclude_patterns=exclude_list,
        )
        
        # Exit with appropriate code
        if not report.success:
            sys.exit(1)
        
    except RepoCleanerError as e:
        print_error(str(e))
        if verbose and e.details:
            print_error(f"Details: {e.details}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print_info("Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
