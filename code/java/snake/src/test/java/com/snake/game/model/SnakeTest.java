package com.snake.game.model;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.LinkedList;

class SnakeTest {
    
    private Snake snake;
    
    @BeforeEach
    void setUp() {
        snake = new Snake(10, 10, 3, Direction.RIGHT);
    }
    
    @Test
    void testInitialSnakeState() {
        assertEquals(3, snake.getBody().size());
        assertEquals(new Point(10, 10), snake.getBody().get(0)); // Head
        assertEquals(Direction.RIGHT, snake.getDirection());
    }
    
    @Test
    void testSnakeMovement() {
        Point initialHead = snake.getBody().get(0);
        snake.move();
        Point newHead = snake.getBody().get(0);
        
        assertEquals(initialHead.getX() + 1, newHead.getX());
        assertEquals(initialHead.getY(), newHead.getY());
    }
    
    @Test
    void testSnakeGrowth() {
        int initialLength = snake.getBody().size();
        snake.grow();
        assertEquals(initialLength + 1, snake.getBody().size());
    }
    
    @Test
    void testDirectionChange() {
        snake.setDirection(Direction.DOWN);
        assertEquals(Direction.DOWN, snake.getDirection());
        
        // Should not allow 180-degree turns
        snake.setDirection(Direction.UP);
        assertEquals(Direction.DOWN, snake.getDirection());
    }
    
    @Test
    void testWallCollision() {
        // Move snake to wall
        for (int i = 0; i < 10; i++) {
            snake.move();
        }
        assertTrue(snake.hasCollidedWithWall(20, 20));
    }
    
    @Test
    void testSelfCollision() {
        // Create a snake with its own collision scenario
        snake = new Snake(5, 5, 5, Direction.RIGHT);
        
        // Manually put the snake into a collision state by manipulating the body
        LinkedList<Point> body = new LinkedList<>();
        // Create a snake in a collision position
        body.add(new Point(5, 5)); // Head at (5,5)
        body.add(new Point(5, 6)); // Body right after the head
        body.add(new Point(6, 6));
        body.add(new Point(6, 5)); // Body curves back
        body.add(new Point(5, 5)); // Body segment at same position as head -> collision!
        
        // Replace the snake's body with our collision scenario
        java.lang.reflect.Field bodyField;
        try {
            bodyField = Snake.class.getDeclaredField("body");
            bodyField.setAccessible(true);
            bodyField.set(snake, body);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            fail("Unable to set up self-collision test: " + e.getMessage());
        }
        
        // Verify collision detection
        assertTrue(snake.hasCollidedWithSelf(), "Snake should detect collision with itself");
    }
    
    @Test
    void testIsHeadAt() {
        Point head = snake.getBody().get(0);
        assertTrue(snake.isHeadAt(head));
        assertFalse(snake.isHeadAt(new Point(0, 0)));
    }
} 