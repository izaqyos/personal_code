"""
Bullet module for Space Invaders.
"""
import pygame
from pygame.sprite import Sprite
from typing import Tuple

from src.utils.settings import (
    BULLET_SPEED, BULLET_WIDTH, BULLET_HEIGHT, BULLET_COLOR
)


class Bullet(Sprite):
    """
    Bullet class for projectiles fired by the player and aliens.
    """
    
    def __init__(self, game, position: Tuple[int, int], is_alien=False):
        """
        Initialize a bullet at the given position.
        
        Args:
            game: The game instance
            position: (x, y) position to create the bullet
            is_alien: True if this is an alien bullet, False for player bullet
        """
        super().__init__()
        self.screen = game.screen
        self.is_alien = is_alien
        
        # Create bullet rect
        self.rect = pygame.Rect(0, 0, BULLET_WIDTH, BULLET_HEIGHT)
        self.rect.midtop = position
        
        # Store position as decimal
        self.y = float(self.rect.y)
        
        # Speed and direction depend on who fired the bullet
        self.speed = -BULLET_SPEED if not is_alien else BULLET_SPEED
        self.color = BULLET_COLOR
    
    def update(self):
        """Move the bullet up or down the screen."""
        # Update decimal position
        self.y += self.speed
        
        # Update rect position
        self.rect.y = self.y
    
    def draw(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect) 