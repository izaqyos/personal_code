"""
Fleet management module for Space Invaders.
"""
import pygame
import random
from typing import List, Tuple

from src.utils.settings import (
    SCREEN_WIDTH, ALIEN_ROWS, ALIENS_PER_ROW,
    ALIEN_X_SPACING, ALIEN_Y_SPACING,
    ALIEN_X_OFFSET, ALIEN_Y_OFFSET,
    ALIEN_MOVE_TIME, ALIEN_MOVE_TIME_DECREASE,
    ALIEN_MOVE_DISTANCE, ALIEN_DESCENT
)
from src.game.alien import Alien


class FleetManager:
    """
    Manager class for the alien fleet.
    Handles creation, movement, and actions of all aliens.
    """
    
    def __init__(self, game):
        """Initialize the fleet manager."""
        self.game = game
        self.screen = game.screen
        self.aliens = pygame.sprite.Group()
        self.direction = 1  # 1 for right, -1 for left
        self.speed = ALIEN_MOVE_DISTANCE
        self.level = 1
        
        # Movement timing
        self.move_time = ALIEN_MOVE_TIME
        self.last_move_time = 0
        
        # Load aliens
        self.create_fleet()
        
    def create_fleet(self):
        """Create the fleet of aliens."""
        self.aliens.empty()
        
        # Create aliens
        for row in range(ALIEN_ROWS):
            for column in range(ALIENS_PER_ROW):
                self._create_alien(row, column)
                
    def _create_alien(self, row: int, column: int):
        """
        Create an alien at a specific grid position.
        
        Args:
            row: Row index (0 is top)
            column: Column index (0 is leftmost)
        """
        alien = Alien(self.game, row, column)
        
        # Calculate position
        alien.x = ALIEN_X_OFFSET + column * ALIEN_X_SPACING
        alien.y = ALIEN_Y_OFFSET + row * ALIEN_Y_SPACING
        
        # Update sprite position
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        
        # Add to group
        self.aliens.add(alien)
        
    def update(self):
        """Update the alien fleet."""
        current_time = pygame.time.get_ticks()
        
        # Move aliens based on time interval
        if current_time - self.last_move_time > self.move_time:
            self._move_aliens()
            self.last_move_time = current_time
            
            # Allow some aliens to shoot
            self._alien_shooting()
        
    def _move_aliens(self):
        """Move the alien fleet."""
        # Check if fleet reached edge
        if self._check_fleet_edges():
            # Change direction and move down
            self.direction *= -1
            for alien in self.aliens:
                alien.y += ALIEN_DESCENT
        
        # Move all aliens horizontally
        for alien in self.aliens:
            alien.x += self.speed * self.direction
            alien.update()
            
    def _check_fleet_edges(self) -> bool:
        """
        Check if any alien in the fleet has reached the edge.
        
        Returns:
            bool: True if fleet should change direction
        """
        for alien in self.aliens:
            if (alien.rect.right >= SCREEN_WIDTH and self.direction > 0) or (alien.rect.left <= 0 and self.direction < 0):
                return True
        return False
    
    def draw(self):
        """Draw all aliens to the screen."""
        for alien in self.aliens:
            alien.draw()
            
    def _alien_shooting(self):
        """Allow some random aliens to shoot."""
        # Only bottom-most aliens from each column can shoot
        shooting_aliens = self._get_bottom_row_aliens()
        
        # Choose up to 2 random aliens to shoot
        shooters = random.sample(shooting_aliens, min(2, len(shooting_aliens))) if shooting_aliens else []
        for alien in shooters:
            alien.shoot()
    
    def _get_bottom_row_aliens(self) -> List[Alien]:
        """
        Get the bottom-most alien from each column.
        
        Returns:
            List[Alien]: List of bottom aliens
        """
        # Dictionary to store the bottom-most alien in each column
        bottom_aliens = {}
        
        for alien in self.aliens:
            column = alien.column
            
            # If we haven't seen an alien in this column, or this one is lower
            if column not in bottom_aliens or alien.rect.y > bottom_aliens[column].rect.y:
                bottom_aliens[column] = alien
                
        return list(bottom_aliens.values())
    
    def increase_speed(self):
        """Increase the fleet speed for the next level."""
        self.move_time = max(200, self.move_time - ALIEN_MOVE_TIME_DECREASE)
        self.level += 1
        
    def aliens_reached_bottom(self) -> bool:
        """
        Check if any aliens have reached the bottom of the screen.
        
        Returns:
            bool: True if an alien reached the bottom
        """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens:
            if alien.rect.bottom >= screen_rect.bottom - 50:  # Allow some space for player
                return True
        return False 