package com.snake.game.model;

/**
 * Represents the possible directions the snake can move
 */
public enum Direction {
    UP, DOWN, LEFT, RIGHT;
    
    /**
     * Checks if this direction is opposite to the given direction
     * @param dir The direction to check against
     * @return true if the directions are opposite, false otherwise
     */
    public boolean isOpposite(Direction dir) {
        return (this == UP && dir == DOWN) ||
               (this == DOWN && dir == UP) ||
               (this == LEFT && dir == RIGHT) ||
               (this == RIGHT && dir == LEFT);
    }
} 