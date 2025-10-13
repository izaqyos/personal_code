package com.snake.game.model;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class FoodTest {
    
    private Food food;
    private Snake snake;
    
    @BeforeEach
    void setUp() {
        food = new Food();
        snake = new Snake(10, 10, 3, Direction.RIGHT);
        
        // Ensure food starts at a non-zero position to test randomization
        food.setPosition(5, 5);
    }
    
    @Test
    void testInitialFoodState() {
        assertNotNull(food.getPosition());
    }
    
    @Test
    void testRandomizePosition() {
        Point oldPosition = new Point(food.getPosition().getX(), food.getPosition().getY());
        food.randomizePosition(20, 20, snake);
        Point newPosition = food.getPosition();
        
        // Position should be within bounds
        assertTrue(newPosition.getX() >= 0 && newPosition.getX() < 20);
        assertTrue(newPosition.getY() >= 0 && newPosition.getY() < 20);
        
        // Food should not be on snake
        assertFalse(snake.getBody().contains(newPosition));
    }
    
    @Test
    void testSetPosition() {
        int x = 5;
        int y = 5;
        food.setPosition(x, y);
        assertEquals(x, food.getPosition().getX());
        assertEquals(y, food.getPosition().getY());
    }
    
    @Test
    void testMultipleRandomizations() {
        // Set food to a known position before testing
        food.setPosition(0, 0);
        Point firstPos = new Point(food.getPosition().getX(), food.getPosition().getY());
        
        // Use a small grid to increase chance of different positions
        boolean foundDifferent = false;
        
        // Try multiple times to randomize position
        for (int i = 0; i < 30; i++) {
            food.randomizePosition(20, 20, snake);
            Point currentPos = food.getPosition();
            
            if (currentPos.getX() != firstPos.getX() || currentPos.getY() != firstPos.getY()) {
                foundDifferent = true;
                break;
            }
        }
        
        assertTrue(foundDifferent, "Food should be able to appear in different positions");
    }
} 