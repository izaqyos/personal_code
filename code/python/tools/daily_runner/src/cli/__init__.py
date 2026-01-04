"""
CLI module for the Daily Standup Timer.

This module includes:
- app: Main CLI application entry point
- display: Terminal rendering with Rich
- commands: Keyboard command handlers
"""

from src.cli.app import CLIApp, main
from src.cli.commands import Command, KeyboardHandler, MockKeyboardHandler
from src.cli.display import CLIDisplay

__all__ = [
    "CLIApp",
    "CLIDisplay",
    "Command",
    "KeyboardHandler",
    "MockKeyboardHandler",
    "main",
]
