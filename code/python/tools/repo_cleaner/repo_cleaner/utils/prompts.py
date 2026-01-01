"""Interactive prompt utilities for Repo Cleaner."""

import sys
from typing import List, Optional, Callable


# Try to import colorama for Windows support
try:
    from colorama import Fore, Style, init
    init()
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

# ANSI color codes (used when colorama not available)
COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "reset": "\033[0m",
    "bold": "\033[1m",
}


def _supports_color() -> bool:
    """Check if the terminal supports color output."""
    if not hasattr(sys.stdout, "isatty"):
        return False
    if not sys.stdout.isatty():
        return False
    
    # Check for dumb terminal
    import os
    if os.environ.get("TERM") == "dumb":
        return False
    
    return True


def _colorize(text: str, color: str) -> str:
    """Apply color to text if supported.
    
    Args:
        text: Text to colorize
        color: Color name (red, green, yellow, blue, cyan, magenta)
        
    Returns:
        Colorized text or original text if colors not supported
    """
    if not _supports_color():
        return text
    
    if HAS_COLORAMA:
        color_map = {
            "red": Fore.RED,
            "green": Fore.GREEN,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "white": Fore.WHITE,
        }
        color_code = color_map.get(color, "")
        return f"{color_code}{text}{Style.RESET_ALL}"
    else:
        color_code = COLORS.get(color, "")
        reset = COLORS.get("reset", "")
        return f"{color_code}{text}{reset}"


def print_success(message: str) -> None:
    """Print a success message in green.
    
    Args:
        message: Message to print
    """
    print(_colorize(f"✓ {message}", "green"))


def print_warning(message: str) -> None:
    """Print a warning message in yellow.
    
    Args:
        message: Message to print
    """
    print(_colorize(f"⚠ {message}", "yellow"))


def print_error(message: str) -> None:
    """Print an error message in red.
    
    Args:
        message: Message to print
    """
    print(_colorize(f"✗ {message}", "red"))


def print_info(message: str) -> None:
    """Print an info message in cyan.
    
    Args:
        message: Message to print
    """
    print(_colorize(f"ℹ {message}", "cyan"))


def confirm_action(
    message: str,
    default: bool = False,
    non_interactive: bool = False,
) -> bool:
    """Prompt for confirmation.
    
    Args:
        message: Message to display
        default: Default value if user just presses Enter
        non_interactive: If True, return default without prompting
        
    Returns:
        True if user confirmed, False otherwise
    """
    if non_interactive:
        return default
    
    default_str = "Y/n" if default else "y/N"
    prompt = f"{message} [{default_str}]: "
    
    try:
        response = input(prompt).strip().lower()
        
        if not response:
            return default
        
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        
        return default
    except (EOFError, KeyboardInterrupt):
        print()  # Newline after ^C
        return False


def prompt_selection(
    message: str,
    options: List[str],
    default: int = 0,
    allow_all: bool = True,
    non_interactive: bool = False,
) -> List[int]:
    """Prompt user to select from a list of options.
    
    Args:
        message: Message to display
        options: List of options to choose from
        default: Default selection index
        allow_all: Whether to allow selecting all options
        non_interactive: If True, return default without prompting
        
    Returns:
        List of selected indices
    """
    if non_interactive:
        return [default]
    
    if not options:
        return []
    
    print(f"\n{message}")
    print("-" * 40)
    
    for i, option in enumerate(options):
        marker = "*" if i == default else " "
        print(f"  {marker} [{i + 1}] {option}")
    
    if allow_all:
        print(f"    [a] All options")
    print(f"    [q] Cancel")
    print()
    
    try:
        response = input("Select option(s) (comma-separated): ").strip().lower()
        
        if not response:
            return [default]
        
        if response == "q":
            return []
        
        if response == "a" and allow_all:
            return list(range(len(options)))
        
        # Parse comma-separated numbers
        selected = []
        for part in response.split(","):
            part = part.strip()
            try:
                idx = int(part) - 1  # Convert to 0-indexed
                if 0 <= idx < len(options):
                    selected.append(idx)
            except ValueError:
                continue
        
        return selected if selected else [default]
    except (EOFError, KeyboardInterrupt):
        print()
        return []


def create_progress_callback(
    total: int,
    prefix: str = "Progress",
    width: int = 40,
) -> Callable[[int], None]:
    """Create a progress callback function.
    
    Args:
        total: Total number of items
        prefix: Prefix text for progress bar
        width: Width of progress bar
        
    Returns:
        Callback function that accepts current count
    """
    # Try to use tqdm if available
    try:
        from tqdm import tqdm
        pbar = tqdm(total=total, desc=prefix, unit="items")
        
        def callback(current: int) -> None:
            pbar.update(1)
            if current >= total:
                pbar.close()
        
        return callback
    except ImportError:
        pass
    
    # Fallback to simple progress bar
    def callback(current: int) -> None:
        if total <= 0:
            return
        
        percent = min(100, int(100 * current / total))
        filled = int(width * current / total)
        bar = "█" * filled + "░" * (width - filled)
        
        print(f"\r{prefix}: [{bar}] {percent}% ({current}/{total})", end="", flush=True)
        
        if current >= total:
            print()  # Newline at end
    
    return callback


def display_summary(
    title: str,
    items: List[tuple],
    total_size: Optional[int] = None,
) -> None:
    """Display a summary with items and sizes.
    
    Args:
        title: Summary title
        items: List of (name, size) tuples
        total_size: Optional total size to display
    """
    from repo_cleaner.utils.filesystem import format_size
    
    print(f"\n{_colorize(title, 'cyan')}")
    print("=" * 60)
    
    for name, size in items:
        size_str = format_size(size) if isinstance(size, int) else str(size)
        print(f"  {name}: {size_str}")
    
    if total_size is not None:
        print("-" * 60)
        print(f"  {_colorize('Total', 'bold')}: {format_size(total_size)}")
    
    print()

