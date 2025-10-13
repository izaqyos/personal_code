"""
Player module for Space Invaders.
"""
import time
import pygame
from pygame.sprite import Sprite
from typing import Tuple

from src.utils.settings import (
    SCREEN_WIDTH, PLAYER_SPEED, PLAYER_SIZE, 
    BULLET_COOLDOWN, WHITE
)
from src.game.bullet import Bullet


class Player(Sprite):
    """
    Player class representing the ship controlled by the player.
    """
    
    def __init__(self, game):
        """Initialize the player ship."""
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        
        # Create a simple player ship surface (placeholder for an actual sprite)
        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(WHITE)
        
        # Set the player's starting position
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, self.screen_rect.bottom - 20)
        
        # Movement flags
        self.moving_right = False
        self.moving_left = False
        
        # Exact position (for decimal movement)
        self.x = float(self.rect.x)
        
        # Shooting
        self.last_shot_time = 0
        
    def update(self):
        """Update player position based on movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += PLAYER_SPEED
        if self.moving_left and self.rect.left > 0:
            self.x -= PLAYER_SPEED
            
        # Update rect position from self.x
        self.rect.x = self.x
        
    def draw(self):
        """Draw the player ship to the screen."""
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """Center the ship at the bottom of the screen."""
        self.rect.midbottom = (SCREEN_WIDTH // 2, self.screen_rect.bottom - 20)
        self.x = float(self.rect.x)
        
    def shoot(self) -> bool:
        """
        Create a new bullet.
        
        Returns:
            bool: True if a bullet was fired, False if on cooldown
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < BULLET_COOLDOWN:
            return False
            
        # Create a new bullet and add it to the bullets group
        bullet = Bullet(self.game, self.rect.midtop)
        self.game.player_bullets.add(bullet)
        
        # Play shooting sound
        # self.game.sounds.play_shoot()
        
        # Update last shot time
        self.last_shot_time = current_time
        
        return True 