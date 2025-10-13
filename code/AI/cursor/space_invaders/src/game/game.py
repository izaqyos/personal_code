"""
Main game module for Space Invaders.
"""
import pygame
import sys
import random
from enum import Enum, auto
from typing import List, Dict, Tuple, Optional
from pygame.sprite import Sprite

from src.utils.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS, BLACK, WHITE,
    PLAYER_LIVES, UFO_SPAWN_CHANCE, UFO_POINTS
)
from src.utils.score_manager import ScoreManager
from src.game.player import Player
from src.game.fleet import FleetManager
from src.game.barrier import BarrierManager
from src.game.ui import MainMenu, GameOverMenu, HighScoreMenu, HUD


class GameState(Enum):
    """Enum for game states."""
    MAIN_MENU = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    HIGH_SCORES = auto()
    PAUSED = auto()


class UFO(Sprite):
    """UFO sprite class."""
    
    def __init__(self, screen, direction: int):
        """
        Initialize the UFO.
        
        Args:
            screen: The game screen
            direction: Movement direction (1 for right, -1 for left)
        """
        super().__init__()
        self.screen = screen
        self.direction = direction
        self.speed = 3
        
        # Create UFO image
        self.image = pygame.Surface((60, 30))
        self.image.fill((255, 0, 0))  # Red UFO
        
        # Position
        self.rect = self.image.get_rect()
        
        # Set initial position (left or right edge)
        if self.direction > 0:
            self.rect.right = 0  # Start from left
        else:
            self.rect.left = SCREEN_WIDTH  # Start from right
            
        self.rect.y = 50  # Near top of screen
        
    def update(self):
        """Update UFO position."""
        # Move UFO
        self.rect.x += self.speed * self.direction
        
    def draw(self):
        """Draw the UFO."""
        self.screen.blit(self.image, self.rect)


class SpaceInvaders:
    """Main game class for Space Invaders."""
    
    def __init__(self):
        """Initialize the game."""
        # Initialize pygame
        pygame.init()
        
        # Create the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        
        # Set up the clock
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = GameState.MAIN_MENU
        self.running = True
        
        # Score manager
        self.score_manager = ScoreManager()
        
        # Create player
        self.player = None
        self.lives = PLAYER_LIVES
        
        # Create sprite groups
        self.player_bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        
        # Create fleet and barriers
        self.fleet_manager = None
        self.barrier_manager = None
        
        # Create UI
        self.main_menu = MainMenu(self)
        self.game_over_menu = None
        self.high_score_menu = None
        self.hud = HUD(self)
        
        # Level
        self.level = 1
        
        # UFO
        self.ufo = None
        
    def run(self):
        """Main game loop."""
        while self.running:
            # Handle events
            events = pygame.event.get()
            self._handle_events(events)
            
            # Update and render based on game state
            if self.state == GameState.MAIN_MENU:
                self._update_main_menu(events)
                self._render_main_menu()
            elif self.state == GameState.PLAYING:
                self._update_game()
                self._render_game()
            elif self.state == GameState.GAME_OVER:
                self._update_game_over(events)
                self._render_game_over()
            elif self.state == GameState.HIGH_SCORES:
                self._update_high_scores(events)
                self._render_high_scores()
            elif self.state == GameState.PAUSED:
                self._render_paused()
            
            # Update display
            pygame.display.flip()
            
            # Cap FPS
            self.clock.tick(FPS)
            
        # Clean up
        pygame.quit()
        sys.exit()
        
    def _handle_events(self, events: List[pygame.event.Event]):
        """
        Handle pygame events.
        
        Args:
            events: List of pygame events
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                
            if self.state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    # Player movement
                    if event.key == pygame.K_LEFT:
                        self.player.moving_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.player.moving_right = True
                    # Player shooting
                    elif event.key == pygame.K_SPACE:
                        self.player.shoot()
                    # Pause game
                    elif event.key == pygame.K_p:
                        self.state = GameState.PAUSED
                    # Quit game
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        self.show_main_menu()
                
                elif event.type == pygame.KEYUP:
                    # Player movement
                    if event.key == pygame.K_LEFT:
                        self.player.moving_left = False
                    elif event.key == pygame.K_RIGHT:
                        self.player.moving_right = False
                        
            elif self.state == GameState.PAUSED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.state = GameState.PLAYING
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        self.show_main_menu()
                        
    def _update_main_menu(self, events: List[pygame.event.Event]):
        """
        Update main menu.
        
        Args:
            events: List of pygame events
        """
        self.main_menu.update(events)
        
    def _render_main_menu(self):
        """Render main menu."""
        self.main_menu.draw()
        
    def _update_game(self):
        """Update game state."""
        # Update player
        self.player.update()
        
        # Update player bullets
        self.player_bullets.update()
        
        # Update alien bullets
        self.alien_bullets.update()
        
        # Update fleet
        self.fleet_manager.update()
        
        # Update barriers
        self.barrier_manager.update()
        
        # Check for UFO spawn
        self._check_ufo_spawn()
        
        # Update UFO if exists
        self._update_ufo()
        
        # Check for collisions
        self._check_collisions()
        
        # Check if level is complete
        if len(self.fleet_manager.aliens) == 0:
            self._next_level()
            
        # Check if game is over
        if self.fleet_manager.aliens_reached_bottom() or self.lives <= 0:
            self._game_over()
        
    def _render_game(self):
        """Render the game."""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw player
        self.player.draw()
        
        # Draw fleet
        self.fleet_manager.draw()
        
        # Draw barriers
        self.barrier_manager.draw()
        
        # Draw bullets
        for bullet in self.player_bullets:
            bullet.draw()
        
        for bullet in self.alien_bullets:
            bullet.draw()
            
        # Draw UFO if exists
        self._draw_ufo()
        
        # Draw HUD
        self.hud.draw(
            self.score_manager.get_current_score(),
            self.score_manager.get_high_score(),
            self.lives,
            self.level
        )
        
    def _update_game_over(self, events: List[pygame.event.Event]):
        """
        Update game over menu.
        
        Args:
            events: List of pygame events
        """
        self.game_over_menu.update(events)
        
    def _render_game_over(self):
        """Render game over screen."""
        self.game_over_menu.draw()
        
    def _update_high_scores(self, events: List[pygame.event.Event]):
        """
        Update high scores menu.
        
        Args:
            events: List of pygame events
        """
        self.high_score_menu.update(events)
        
    def _render_high_scores(self):
        """Render high scores screen."""
        self.high_score_menu.draw()
        
    def _render_paused(self):
        """Render paused screen."""
        # Render game in background
        self._render_game()
        
        # Draw translucent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw paused text
        font = pygame.font.SysFont(None, 72)
        text = font.render("PAUSED", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        # Draw instructions
        font = pygame.font.SysFont(None, 36)
        text = font.render("Press P to resume, ESC to quit", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(text, text_rect)
        
    def _check_collisions(self):
        """Check for collisions between game objects."""
        # Player bullets hitting aliens
        collisions = pygame.sprite.groupcollide(
            self.player_bullets, self.fleet_manager.aliens, True, True
        )
        
        # Add score for destroyed aliens
        for bullet, aliens in collisions.items():
            for alien in aliens:
                points = alien.get_points()
                self.score_manager.update_current_score(points)
                
        # Alien bullets hitting player
        if pygame.sprite.spritecollideany(self.player, self.alien_bullets):
            self._player_hit()
            
        # Bullet hits UFO
        if self.ufo:
            bullet = pygame.sprite.spritecollideany(self.ufo, self.player_bullets)
            if bullet:
                self.score_manager.update_current_score(UFO_POINTS)
                self.ufo = None
                self.player_bullets.remove(bullet)
            
        # Get all barrier blocks
        barrier_blocks = self.barrier_manager.get_all_blocks()
        
        # Player bullets hitting barriers
        pygame.sprite.groupcollide(self.player_bullets, barrier_blocks, True, True)
        
        # Alien bullets hitting barriers
        pygame.sprite.groupcollide(self.alien_bullets, barrier_blocks, True, True)
        
        # Remove bullets that go offscreen
        for bullet in self.player_bullets.copy():
            if bullet.rect.bottom <= 0:
                self.player_bullets.remove(bullet)
                
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= SCREEN_HEIGHT:
                self.alien_bullets.remove(bullet)
                
    def _player_hit(self):
        """Handle player being hit by alien bullet."""
        # Decrease lives
        self.lives -= 1
        
        # Remove all bullets
        self.player_bullets.empty()
        self.alien_bullets.empty()
        
        # Reset player position
        self.player.center_ship()
        
        # Pause briefly
        pygame.time.delay(1000)
        
    def _game_over(self):
        """Handle game over state."""
        # Save final score
        final_score = self.score_manager.get_current_score()
        is_high_score = self.score_manager.add_score(final_score)
        
        # Create game over menu
        self.game_over_menu = GameOverMenu(self, final_score, is_high_score)
        
        # Change state
        self.state = GameState.GAME_OVER
        
    def _next_level(self):
        """Start the next level."""
        # Increase level
        self.level += 1
        
        # Create new fleet with increased speed
        self.fleet_manager.create_fleet()
        self.fleet_manager.increase_speed()
        
        # Remove all bullets
        self.player_bullets.empty()
        self.alien_bullets.empty()
        
        # Reset player position
        self.player.center_ship()
        
        # Pause briefly
        pygame.time.delay(1000)
        
    def _check_ufo_spawn(self):
        """Randomly spawn a UFO."""
        if self.ufo is None and random.random() < UFO_SPAWN_CHANCE:
            self._spawn_ufo()
            
    def _spawn_ufo(self):
        """Create a new UFO."""
        # Choose a random direction
        direction = 1 if random.choice([True, False]) else -1
        
        # Create a new UFO sprite
        self.ufo = UFO(self.screen, direction)
                
    def _update_ufo(self):
        """Update UFO position."""
        if self.ufo:
            # Update UFO
            self.ufo.update()
            
            # Remove if off screen
            if (self.ufo.rect.left > SCREEN_WIDTH) or (self.ufo.rect.right < 0):
                self.ufo = None
                
    def _draw_ufo(self):
        """Draw the UFO if it exists."""
        if self.ufo:
            self.ufo.draw()
            
    def start_game(self):
        """Start a new game."""
        # Reset score
        self.score_manager.reset_current_score()
        
        # Reset lives
        self.lives = PLAYER_LIVES
        
        # Reset level
        self.level = 1
        
        # Create player
        self.player = Player(self)
        
        # Create fleet
        self.fleet_manager = FleetManager(self)
        
        # Create barriers
        self.barrier_manager = BarrierManager(self)
        
        # Reset bullets
        self.player_bullets.empty()
        self.alien_bullets.empty()
        
        # Reset UFO
        self.ufo = None
        
        # Change state
        self.state = GameState.PLAYING
        
    def show_main_menu(self):
        """Show the main menu."""
        self.state = GameState.MAIN_MENU
        
    def show_high_scores(self):
        """Show the high scores screen."""
        # Create high score menu with updated scores
        scores = self.score_manager.get_recent_scores()
        self.high_score_menu = HighScoreMenu(self, scores)
        
        # Change state
        self.state = GameState.HIGH_SCORES
        
    def quit_game(self):
        """Quit the game."""
        self.running = False 