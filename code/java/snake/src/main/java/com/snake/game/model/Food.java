package com.snake.game.model;

import java.util.List;
import java.util.Random;

/**
 * Represents food in the game
 */
public class Food {
    private Point position;
    private Random random;
    
    /**
     * Creates a new food object
     */
    public Food() {
        this.random = new Random();
        this.position = new Point(0, 0);
    }
    
    /**
     * Gets the current position of the food
     * @return The position of the food
     */
    public Point getPosition() {
        return position;
    }
    
    /**
     * Sets the position of the food
     * @param x The x coordinate
     * @param y The y coordinate
     */
    public void setPosition(int x, int y) {
        if (this.position == null) {
            this.position = new Point(x, y);
        } else {
            this.position.setX(x);
            this.position.setY(y);
        }
    }
    
    /**
     * Randomly places the food in an empty cell
     * @param width The width of the game area
     * @param height The height of the game area
     * @param snake The snake to avoid when placing food
     */
    public void randomizePosition(int width, int height, Snake snake) {
        List<Point> snakeBody = snake.getBody();
        
        // Store current position to ensure we don't place it in the same spot
        Point oldPosition = new Point(position.getX(), position.getY());
        
        Point newPosition;
        int attempts = 0;
        do {
            int x = random.nextInt(width);
            int y = random.nextInt(height);
            newPosition = new Point(x, y);
            
            // Avoid infinite loop by limiting attempts
            attempts++;
            if (attempts > 100) {
                // After many attempts, just find any valid position
                if (!isPositionOccupied(newPosition, snakeBody)) {
                    break;
                }
            }
        } while (isPositionOccupied(newPosition, snakeBody) || 
                 (oldPosition.equals(newPosition) && attempts < 10));
        
        setPosition(newPosition.getX(), newPosition.getY());
    }
    
    /**
     * Checks if a position is occupied by the snake
     * @param position The position to check
     * @param snakeBody The snake's body
     * @return true if the position is occupied, false otherwise
     */
    private boolean isPositionOccupied(Point position, List<Point> snakeBody) {
        for (Point bodyPart : snakeBody) {
            if (bodyPart.equals(position)) {
                return true;
            }
        }
        return false;
    }
} 