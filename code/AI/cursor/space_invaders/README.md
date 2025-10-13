# Space Invaders

A classic Space Invaders game implementation in Python using Pygame.

## Description

This project is a modern implementation of the classic arcade game Space Invaders, where the player controls a ship at the bottom of the screen and shoots at alien invaders descending from the top of the screen.

## Features

- Classic Space Invaders gameplay
- Score tracking and persistence
- Progressive difficulty levels
- Modern graphics and sound effects

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/space_invaders.git
   cd space_invaders
   ```

2. Set up the conda environment:
   ```
   conda create -n space_invaders python=3.11 numpy -y
   conda activate space_invaders
   pip install pygame
   ```

## Usage

To run the game, make sure the conda environment is activated, then run:

```
python src/main.py
```

## Controls

- **Left Arrow**: Move ship left
- **Right Arrow**: Move ship right
- **Space**: Shoot
- **P**: Pause game
- **Q**: Quit game
- **ESC**: Exit game

## Project Structure

```
space_invaders/
├── src/                # Source code directory
│   ├── game/           # Game logic modules
│   └── utils/          # Utility functions
├── tests/              # Test directory
├── assets/             # Game assets
│   ├── images/         # Sprites and images
│   ├── sounds/         # Sound effects and music
│   └── fonts/          # Game fonts
├── data/               # Save data and high scores
├── README.md           # This file
└── CHANGELOG.md        # Version history
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 