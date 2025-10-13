"""
UI module for Space Invaders.
"""
import pygame
from typing import Callable, Tuple, List, Dict, Optional

from src.utils.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GREEN, RED
)


class Button:
    """Button class for menu navigation."""
    
    def __init__(
        self, 
        screen, 
        text: str, 
        position: Tuple[int, int],
        size: Tuple[int, int] = (200, 50),
        callback: Optional[Callable] = None,
        bg_color: Tuple[int, int, int] = BLACK,
        text_color: Tuple[int, int, int] = WHITE,
        hover_color: Tuple[int, int, int] = GREEN
    ):
        """
        Initialize a button.
        
        Args:
            screen: The game screen
            text: Button text
            position: (x, y) position (center of button)
            size: (width, height) of button
            callback: Function to call when button is clicked
            bg_color: Background color
            text_color: Text color
            hover_color: Color when mouse hovers
        """
        self.screen = screen
        self.text = text
        self.position = position
        self.size = size
        self.callback = callback
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont(None, 36)
        
        # Create rect
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.rect.center = position
        
        # State
        self.hovered = False
        
    def update(self, mouse_pos: Tuple[int, int], mouse_clicked: bool):
        """
        Update button state based on mouse.
        
        Args:
            mouse_pos: Current mouse position (x, y)
            mouse_clicked: Whether the mouse was clicked
        """
        # Check if mouse is over button
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Call callback if clicked
        if self.hovered and mouse_clicked and self.callback:
            self.callback()
            
    def draw(self):
        """Draw the button to the screen."""
        # Draw background
        color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(self.screen, color, self.rect)
        
        # Draw border
        pygame.draw.rect(self.screen, self.text_color, self.rect, 2)
        
        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.screen.blit(text_surf, text_rect)


class Menu:
    """Base class for game menus."""
    
    def __init__(self, game, title: str):
        """
        Initialize a menu.
        
        Args:
            game: The game instance
            title: Menu title
        """
        self.game = game
        self.screen = game.screen
        self.title = title
        self.buttons = []
        self.title_font = pygame.font.SysFont(None, 72)
        self.font = pygame.font.SysFont(None, 36)
        
    def update(self, events: List[pygame.event.Event]):
        """
        Update menu based on input events.
        
        Args:
            events: List of pygame events
        """
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
                
        for button in self.buttons:
            button.update(mouse_pos, mouse_clicked)
            
    def draw(self):
        """Draw the menu to the screen."""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw title
        title_surf = self.title_font.render(self.title, True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_surf, title_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw()


class MainMenu(Menu):
    """Main menu for the game."""
    
    def __init__(self, game):
        """Initialize the main menu."""
        super().__init__(game, "SPACE INVADERS")
        
        # Create buttons
        button_y = 250
        
        # Start button
        start_button = Button(
            self.screen,
            "START",
            (SCREEN_WIDTH // 2, button_y),
            callback=self.game.start_game
        )
        self.buttons.append(start_button)
        
        # High scores button
        button_y += 80
        highscores_button = Button(
            self.screen,
            "HIGH SCORES",
            (SCREEN_WIDTH // 2, button_y),
            callback=self.game.show_high_scores
        )
        self.buttons.append(highscores_button)
        
        # Quit button
        button_y += 80
        quit_button = Button(
            self.screen,
            "QUIT",
            (SCREEN_WIDTH // 2, button_y),
            callback=self.game.quit_game
        )
        self.buttons.append(quit_button)


class GameOverMenu(Menu):
    """Game over menu."""
    
    def __init__(self, game, score: int, is_high_score: bool):
        """
        Initialize the game over menu.
        
        Args:
            game: The game instance
            score: Final score
            is_high_score: Whether the score is a new high score
        """
        super().__init__(game, "GAME OVER")
        self.score = score
        self.is_high_score = is_high_score
        
        # Create buttons
        button_y = 350
        
        # Play again button
        restart_button = Button(
            self.screen,
            "PLAY AGAIN",
            (SCREEN_WIDTH // 2, button_y),
            callback=self.game.start_game
        )
        self.buttons.append(restart_button)
        
        # Main menu button
        button_y += 80
        menu_button = Button(
            self.screen,
            "MAIN MENU",
            (SCREEN_WIDTH // 2, button_y),
            callback=self.game.show_main_menu
        )
        self.buttons.append(menu_button)
        
    def draw(self):
        """Draw the game over menu."""
        super().draw()
        
        # Draw score
        score_text = f"Your Score: {self.score}"
        score_surf = self.font.render(score_text, True, WHITE)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(score_surf, score_rect)
        
        # Draw high score message if applicable
        if self.is_high_score:
            hs_surf = self.font.render("NEW HIGH SCORE!", True, GREEN)
            hs_rect = hs_surf.get_rect(center=(SCREEN_WIDTH // 2, 250))
            self.screen.blit(hs_surf, hs_rect)


class HighScoreMenu(Menu):
    """High score display menu."""
    
    def __init__(self, game, scores: List[Dict]):
        """
        Initialize the high score menu.
        
        Args:
            game: The game instance
            scores: List of score dictionaries
        """
        super().__init__(game, "HIGH SCORES")
        self.scores = scores
        
        # Back button
        back_button = Button(
            self.screen,
            "BACK",
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100),
            callback=self.game.show_main_menu
        )
        self.buttons.append(back_button)
        
    def draw(self):
        """Draw the high score menu."""
        super().draw()
        
        # Draw scores
        y_pos = 200
        for i, score_data in enumerate(self.scores[:10]):  # Show top 10
            score_text = f"{i+1}. {score_data['score']} - {score_data['date']}"
            score_surf = self.font.render(score_text, True, WHITE)
            score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            self.screen.blit(score_surf, score_rect)
            y_pos += 40


class HUD:
    """Head-up display for showing game info."""
    
    def __init__(self, game):
        """
        Initialize the HUD.
        
        Args:
            game: The game instance
        """
        self.game = game
        self.screen = game.screen
        self.font = pygame.font.SysFont(None, 36)
        
    def draw(self, score: int, high_score: int, lives: int, level: int):
        """
        Draw the HUD.
        
        Args:
            score: Current score
            high_score: High score
            lives: Remaining lives
            level: Current level
        """
        # Draw score
        score_surf = self.font.render(f"Score: {score}", True, WHITE)
        self.screen.blit(score_surf, (20, 20))
        
        # Draw high score
        hs_surf = self.font.render(f"High Score: {high_score}", True, WHITE)
        hs_rect = hs_surf.get_rect()
        hs_rect.right = SCREEN_WIDTH - 20
        hs_rect.top = 20
        self.screen.blit(hs_surf, hs_rect)
        
        # Draw lives
        lives_surf = self.font.render(f"Lives: {lives}", True, WHITE)
        self.screen.blit(lives_surf, (20, SCREEN_HEIGHT - 50))
        
        # Draw level
        level_surf = self.font.render(f"Level: {level}", True, WHITE)
        level_rect = level_surf.get_rect()
        level_rect.right = SCREEN_WIDTH - 20
        level_rect.bottom = SCREEN_HEIGHT - 20
        self.screen.blit(level_surf, level_rect) 