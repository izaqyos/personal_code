"""
Alien module for Space Invaders.
"""
import pygame
import random
from pygame.sprite import Sprite
from typing import Tuple

from src.utils.settings import (
    RED, GREEN, BLUE, ALIEN_POINTS
)
from src.game.bullet import Bullet


class Alien(Sprite):
    """
    Alien class representing the enemy invaders.
    """
    
    def __init__(self, game, row: int, column: int):
        """
        Initialize an alien at a specific grid position.
        
        Args:
            game: The game instance
            row: The row index (0 is top row)
            column: The column index
        """
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.row = row
        self.column = column
        
        # Select color based on row
        if row == 0:
            color = RED
        elif row in (1, 2):
            color = GREEN
        else:
            color = BLUE
            
        # Create a simple alien surface (placeholder for sprite)
        self.width, self.height = 40, 40
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        
        # Set initial position
        self.rect = self.image.get_rect()
        
        # Store exact position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def update(self):
        """
        Update alien position. This is called when the fleet moves.
        The actual movement logic is in the fleet manager.
        """
        # Update rect position from stored exact position
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self):
        """Draw the alien to the screen."""
        self.screen.blit(self.image, self.rect)
        
    def get_points(self) -> int:
        """
        Get the point value for this alien.
        
        Returns:
            int: Points for destroying this alien
        """
        return ALIEN_POINTS.get(self.row, 10)
        
    def shoot(self) -> bool:
        """
        Attempt to fire a bullet.
        
        Returns:
            bool: True if a bullet was fired
        """
        # Random chance to shoot
        if random.random() < 0.01:
            bullet = Bullet(self.game, self.rect.midbottom, is_alien=True)
            self.game.alien_bullets.add(bullet)
            return True
        return False 