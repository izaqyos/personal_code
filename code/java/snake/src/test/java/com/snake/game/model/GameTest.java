package com.snake.game.model;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class GameTest {
    
    private Game game;
    
    @BeforeEach
    void setUp() {
        game = new Game(20, 20);
        game.setPlayerName("TestPlayer");
        game.initialize();
    }
    
    @Test
    void testInitialGameState() {
        assertFalse(game.isGameOver());
        assertFalse(game.isPaused());
        assertEquals(0, game.getScore());
        assertEquals("TestPlayer", game.getPlayerName());
        assertNotNull(game.getSnake());
        assertNotNull(game.getFood());
    }
    
    @Test
    void testGameUpdate() {
        Point initialHead = game.getSnake().getBody().get(0);
        game.update();
        Point newHead = game.getSnake().getBody().get(0);
        
        // Snake should have moved
        assertNotEquals(initialHead, newHead);
    }
    
    @Test
    void testScoreIncrease() {
        // Place food at snake's next position
        Point snakeHead = game.getSnake().getBody().get(0);
        int nextX = snakeHead.getX() + 1;
        int nextY = snakeHead.getY();
        game.getFood().setPosition(nextX, nextY);
        
        game.update();
        assertEquals(10, game.getScore());
    }
    
    @Test
    void testGameOver() {
        // Move snake to wall
        for (int i = 0; i < 20; i++) {
            game.update();
        }
        
        assertTrue(game.isGameOver());
    }
    
    @Test
    void testPauseGame() {
        Point beforePause = game.getSnake().getBody().get(0);
        game.togglePause();
        game.update();
        Point afterPause = game.getSnake().getBody().get(0);
        
        assertTrue(game.isPaused());
        assertEquals(beforePause, afterPause);
    }
    
    @Test
    void testChangeDirection() {
        game.changeDirection(Direction.DOWN);
        assertEquals(Direction.DOWN, game.getSnake().getDirection());
        
        // Should not change direction when paused
        game.togglePause();
        game.changeDirection(Direction.UP);
        assertEquals(Direction.DOWN, game.getSnake().getDirection());
    }
    
    @Test
    void testDimensions() {
        assertEquals(20, game.getWidth());
        assertEquals(20, game.getHeight());
    }
} 