"""
Keyboard command handlers for the CLI interface.

This module processes keyboard input and maps commands
to meeting manager actions.
"""

import contextlib
import logging
import sys
import termios
import tty
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

logger = logging.getLogger(__name__)


class Command(Enum):
    """Available CLI commands."""

    PAUSE_RESUME = auto()
    NEXT_SPEAKER = auto()
    SKIP_SPEAKER = auto()
    ADD_TIME = auto()
    SUBTRACT_TIME = auto()
    MARK_ABSENT = auto()
    REORDER = auto()
    QUIT = auto()
    CONFIRM = auto()
    CANCEL = auto()
    NUMBER_1 = auto()
    NUMBER_2 = auto()
    NUMBER_3 = auto()
    NUMBER_4 = auto()
    NUMBER_5 = auto()
    NUMBER_6 = auto()
    NUMBER_7 = auto()
    NUMBER_8 = auto()
    NUMBER_9 = auto()
    RESUME_SESSION = auto()
    NEW_SESSION = auto()
    UNKNOWN = auto()


# Key mappings
KEY_MAP: dict[str, Command] = {
    "p": Command.PAUSE_RESUME,
    "P": Command.PAUSE_RESUME,
    " ": Command.PAUSE_RESUME,  # Space also pauses
    "n": Command.NEXT_SPEAKER,
    "N": Command.NEXT_SPEAKER,
    "\r": Command.NEXT_SPEAKER,  # Enter
    "\n": Command.NEXT_SPEAKER,  # Enter
    "s": Command.SKIP_SPEAKER,
    "S": Command.SKIP_SPEAKER,
    "+": Command.ADD_TIME,
    "=": Command.ADD_TIME,  # Common typo
    "-": Command.SUBTRACT_TIME,
    "_": Command.SUBTRACT_TIME,
    "a": Command.MARK_ABSENT,
    "A": Command.MARK_ABSENT,
    "r": Command.RESUME_SESSION,
    "R": Command.REORDER,
    "q": Command.QUIT,
    "Q": Command.QUIT,
    "\x1b": Command.CANCEL,  # Escape
    "y": Command.CONFIRM,
    "Y": Command.CONFIRM,
    "1": Command.NUMBER_1,
    "2": Command.NUMBER_2,
    "3": Command.NUMBER_3,
    "4": Command.NUMBER_4,
    "5": Command.NUMBER_5,
    "6": Command.NUMBER_6,
    "7": Command.NUMBER_7,
    "8": Command.NUMBER_8,
    "9": Command.NUMBER_9,
}


@dataclass
class CommandResult:
    """Result of command processing."""

    command: Command
    raw_key: str
    handled: bool = False
    message: str | None = None


# Type for command handlers
CommandHandler = Callable[[Command], bool]


class KeyboardHandler:
    """
    Handles keyboard input for the CLI.

    Reads single keystrokes without requiring Enter,
    and maps them to commands.
    """

    def __init__(self) -> None:
        """Initialize the keyboard handler."""
        self._old_settings: list[Any] | None = None
        self._enabled = False

    def enable_raw_mode(self) -> bool:
        """
        Enable raw terminal mode for single-key input.

        Returns:
            True if raw mode was enabled successfully.
        """
        if not sys.stdin.isatty():
            logger.warning("stdin is not a tty, keyboard input disabled")
            return False

        try:
            self._old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
            self._enabled = True
            return True
        except termios.error as e:
            logger.warning(f"Failed to enable raw mode: {e}")
            return False

    def disable_raw_mode(self) -> None:
        """Restore normal terminal mode."""
        if self._old_settings is not None:
            with contextlib.suppress(termios.error):
                termios.tcsetattr(
                    sys.stdin, termios.TCSADRAIN, self._old_settings
                )
            self._old_settings = None
        self._enabled = False

    def read_key(self, timeout: float | None = None) -> str | None:
        """
        Read a single keystroke.

        Args:
            timeout: Optional timeout in seconds.

        Returns:
            The key pressed, or None if timeout.
        """
        if not self._enabled:
            return None

        import select

        # Check if input is available
        if timeout is not None:
            ready, _, _ = select.select([sys.stdin], [], [], timeout)
            if not ready:
                return None

        try:
            return sys.stdin.read(1)
        except OSError:
            return None

    def get_command(self, key: str) -> Command:
        """
        Map a key to a command.

        Args:
            key: The key that was pressed.

        Returns:
            The corresponding Command.
        """
        return KEY_MAP.get(key, Command.UNKNOWN)

    def process_input(self, timeout: float = 0.1) -> CommandResult | None:
        """
        Read and process keyboard input.

        Args:
            timeout: Time to wait for input in seconds.

        Returns:
            CommandResult if a key was pressed, None otherwise.
        """
        key = self.read_key(timeout)
        if key is None:
            return None

        command = self.get_command(key)
        return CommandResult(command=command, raw_key=key)

    @staticmethod
    def get_number_from_command(command: Command) -> int | None:
        """
        Extract a number from a number command.

        Args:
            command: The command to check.

        Returns:
            The number (1-9) or None if not a number command.
        """
        number_commands = {
            Command.NUMBER_1: 1,
            Command.NUMBER_2: 2,
            Command.NUMBER_3: 3,
            Command.NUMBER_4: 4,
            Command.NUMBER_5: 5,
            Command.NUMBER_6: 6,
            Command.NUMBER_7: 7,
            Command.NUMBER_8: 8,
            Command.NUMBER_9: 9,
        }
        return number_commands.get(command)

    def __enter__(self) -> "KeyboardHandler":
        """Context manager entry - enable raw mode."""
        self.enable_raw_mode()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Context manager exit - restore terminal."""
        self.disable_raw_mode()


class MockKeyboardHandler(KeyboardHandler):
    """
    Mock keyboard handler for testing.

    Allows injecting predefined key sequences for testing
    without requiring actual keyboard input.
    """

    def __init__(self, keys: list[str] | None = None) -> None:
        """
        Initialize with optional predefined keys.

        Args:
            keys: List of keys to return in sequence.
        """
        super().__init__()
        self._keys = list(keys) if keys else []
        self._index = 0

    def add_keys(self, keys: list[str]) -> None:
        """
        Add keys to the queue.

        Args:
            keys: Keys to add.
        """
        self._keys.extend(keys)

    def add_key(self, key: str) -> None:
        """
        Add a single key to the queue.

        Args:
            key: Key to add.
        """
        self._keys.append(key)

    def enable_raw_mode(self) -> bool:
        """Mock enable - always succeeds."""
        self._enabled = True
        return True

    def disable_raw_mode(self) -> None:
        """Mock disable."""
        self._enabled = False

    def read_key(self, _timeout: float | None = None) -> str | None:
        """
        Return the next key from the queue.

        Args:
            _timeout: Ignored in mock.

        Returns:
            Next key or None if queue empty.
        """
        if self._index < len(self._keys):
            key = self._keys[self._index]
            self._index += 1
            return key
        return None

    def reset(self) -> None:
        """Reset the key queue index."""
        self._index = 0

    def clear(self) -> None:
        """Clear all keys and reset."""
        self._keys = []
        self._index = 0
