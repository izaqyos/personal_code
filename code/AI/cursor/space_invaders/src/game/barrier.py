"""
Barrier module for Space Invaders.
"""
import pygame
from pygame.sprite import Sprite
from typing import Tuple, List

from src.utils.settings import (
    SCREEN_WIDTH, GREEN, 
    BARRIER_COUNT, BARRIER_WIDTH, BARRIER_HEIGHT, BARRIER_POSITION_Y
)


class BarrierBlock(Sprite):
    """
    Individual block that makes up a barrier.
    """
    
    def __init__(self, x: int, y: int, size: int, screen):
        """
        Initialize a barrier block.
        
        Args:
            x: X coordinate
            y: Y coordinate
            size: Size of the block
            screen: The game screen
        """
        super().__init__()
        self.screen = screen
        self.size = size
        self.image = pygame.Surface((size, size))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw(self):
        """Draw the barrier block."""
        self.screen.blit(self.image, self.rect)


class Barrier(Sprite):
    """
    Barrier that protects the player from alien bullets.
    Made up of multiple BarrierBlock objects.
    """
    
    def __init__(self, screen, position: Tuple[int, int]):
        """
        Initialize a barrier.
        
        Args:
            screen: The game screen
            position: (x, y) center position of the barrier
        """
        super().__init__()
        self.screen = screen
        self.blocks = pygame.sprite.Group()
        self.position = position
        self.width = BARRIER_WIDTH
        self.height = BARRIER_HEIGHT
        
        # Create barrier shape
        self._create_barrier()
        
    def _create_barrier(self):
        """Create the barrier shape using blocks."""
        block_size = 8  # Size of each block
        
        # Center position
        center_x, center_y = self.position
        
        # Calculate the top-left position
        start_x = center_x - (self.width // 2)
        start_y = center_y - (self.height // 2)
        
        # Basic barrier design (rectangle with a notch in the middle-top)
        for row in range(self.height // block_size):
            for col in range(self.width // block_size):
                # Skip blocks to create a notch in the top-middle
                if (row < 2 and 
                    col >= (self.width // block_size) // 2 - 2 and 
                    col <= (self.width // block_size) // 2 + 1):
                    continue
                
                # Create block
                block_x = start_x + (col * block_size)
                block_y = start_y + (row * block_size)
                block = BarrierBlock(block_x, block_y, block_size, self.screen)
                self.blocks.add(block)
                
    def update(self):
        """Update the barrier (currently does nothing)."""
        pass
    
    def draw(self):
        """Draw all blocks in the barrier."""
        for block in self.blocks:
            block.draw()


class BarrierManager:
    """
    Manager class for all barriers.
    """
    
    def __init__(self, game):
        """
        Initialize the barrier manager.
        
        Args:
            game: The game instance
        """
        self.game = game
        self.screen = game.screen
        self.barriers = []
        
        # Create barriers
        self._create_barriers()
        
    def _create_barriers(self):
        """Create all barriers."""
        # Calculate barrier positions
        screen_width = SCREEN_WIDTH
        spacing = screen_width // (BARRIER_COUNT + 1)
        
        for i in range(BARRIER_COUNT):
            x_pos = spacing * (i + 1)
            barrier = Barrier(self.screen, (x_pos, BARRIER_POSITION_Y))
            self.barriers.append(barrier)
            
    def update(self):
        """Update all barriers."""
        for barrier in self.barriers:
            barrier.update()
            
    def draw(self):
        """Draw all barriers."""
        for barrier in self.barriers:
            barrier.draw()
            
    def get_all_blocks(self) -> pygame.sprite.Group:
        """
        Get all barrier blocks as a group for collision detection.
        
        Returns:
            pygame.sprite.Group: All barrier blocks
        """
        all_blocks = pygame.sprite.Group()
        for barrier in self.barriers:
            all_blocks.add(barrier.blocks)
            
        return all_blocks 