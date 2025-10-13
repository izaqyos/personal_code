#!/usr/bin/env python3
"""
Space Invaders game runner script.
Provides functionality to run the game, run tests, and display help.
"""
import os
import sys
import subprocess
import argparse
from typing import Optional


def run_game() -> None:
    """Run the Space Invaders game."""
    try:
        subprocess.run([sys.executable, "src/main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running game: {e}")
        sys.exit(1)


def run_tests() -> None:
    """Run the game's test suite."""
    try:
        subprocess.run([sys.executable, "-m", "unittest", "discover", "tests"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running tests: {e}")
        sys.exit(1)


def show_help() -> None:
    """Display help information about the game."""
    help_text = """
Space Invaders Game Help

Commands:
    run.py game      - Run the Space Invaders game
    run.py test     - Run the game's test suite
    run.py help     - Show this help message

Game Controls:
    Left Arrow     - Move ship left
    Right Arrow    - Move ship right
    Space          - Shoot
    P              - Pause game
    Q or ESC       - Quit game

Game Features:
    - Classic Space Invaders gameplay
    - Score tracking and high scores
    - Progressive difficulty levels
    - Defensive barriers
    - UFO bonus enemies
    - Multiple lives
    - Pause functionality

Installation:
    1. Clone the repository
    2. Set up the conda environment:
       conda create -n space_invaders python=3.11 numpy -y
       conda activate space_invaders
       pip install pygame
    3. Run the game:
       python run.py game

For more information, see the README.md file.
"""
    print(help_text)


def main() -> None:
    """Main entry point for the run script."""
    parser = argparse.ArgumentParser(description="Space Invaders game runner")
    parser.add_argument(
        "command",
        choices=["game", "test", "help"],
        help="Command to execute (game, test, or help)"
    )
    
    args = parser.parse_args()
    
    if args.command == "game":
        run_game()
    elif args.command == "test":
        run_tests()
    elif args.command == "help":
        show_help()


if __name__ == "__main__":
    main() 