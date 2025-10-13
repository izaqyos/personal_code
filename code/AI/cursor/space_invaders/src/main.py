"""
Main entry point for Space Invaders game.
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game.game import SpaceInvaders


def main():
    """Main function to start the game."""
    game = SpaceInvaders()
    game.run()


if __name__ == "__main__":
    main() 