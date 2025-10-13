"""
Game settings and configuration.
"""

# Display settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Space Invaders"
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player settings
PLAYER_SPEED = 5
PLAYER_SIZE = (50, 40)
PLAYER_LIVES = 3

# Bullet settings
BULLET_SPEED = 10
BULLET_WIDTH = 3
BULLET_HEIGHT = 15
BULLET_COLOR = YELLOW
BULLET_COOLDOWN = 250  # milliseconds

# Alien settings
ALIEN_ROWS = 5
ALIENS_PER_ROW = 11
ALIEN_X_SPACING = 60
ALIEN_Y_SPACING = 50
ALIEN_X_OFFSET = 50
ALIEN_Y_OFFSET = 50
ALIEN_POINTS = {
    0: 30,  # Top row
    1: 20,  # Middle rows
    2: 20,
    3: 10,  # Bottom rows
    4: 10
}
ALIEN_MOVE_TIME = 1000  # milliseconds
ALIEN_MOVE_TIME_DECREASE = 50  # milliseconds (speed increase per level)
ALIEN_MOVE_DISTANCE = 10
ALIEN_DESCENT = 20

# Game settings
SCORE_FILE = "data/highscores.json"
DEFAULT_HIGH_SCORE = 0

# Barrier settings
BARRIER_COUNT = 4
BARRIER_WIDTH = 80
BARRIER_HEIGHT = 60
BARRIER_POSITION_Y = 450

# UFO settings
UFO_POINTS = 100
UFO_SPEED = 3
UFO_SPAWN_CHANCE = 0.002  # Chance per frame 