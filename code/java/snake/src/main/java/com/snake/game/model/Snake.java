package com.snake.game.model;

import java.util.LinkedList;
import java.util.List;

/**
 * Represents the snake in the game
 */
public class Snake {
    private LinkedList<Point> body;
    private Direction direction;
    private boolean hasEaten;
    
    /**
     * Creates a new snake with the given starting position and direction
     * @param startX The starting X coordinate
     * @param startY The starting Y coordinate
     * @param initialLength The initial length of the snake
     * @param direction The initial direction of the snake
     */
    public Snake(int startX, int startY, int initialLength, Direction direction) {
        this.body = new LinkedList<>();
        this.direction = direction;
        this.hasEaten = false;
        
        // Create the initial snake body
        for (int i = 0; i < initialLength; i++) {
            int x = startX;
            int y = startY;
            
            switch (direction) {
                case RIGHT:
                    x -= i;
                    break;
                case LEFT:
                    x += i;
                    break;
                case DOWN:
                    y -= i;
                    break;
                case UP:
                    y += i;
                    break;
            }
            
            body.add(new Point(x, y));
        }
    }
    
    /**
     * Moves the snake in its current direction
     */
    public void move() {
        Point head = getHead();
        Point newHead = new Point(head.getX(), head.getY());
        
        // Calculate new head position based on direction
        switch (direction) {
            case UP:
                newHead.setY(head.getY() - 1);
                break;
            case DOWN:
                newHead.setY(head.getY() + 1);
                break;
            case LEFT:
                newHead.setX(head.getX() - 1);
                break;
            case RIGHT:
                newHead.setX(head.getX() + 1);
                break;
        }
        
        // Add new head
        body.addFirst(newHead);
        
        // If the snake hasn't eaten, remove the tail to maintain length
        if (!hasEaten) {
            body.removeLast();
        } else {
            // Reset the eaten flag
            hasEaten = false;
        }
    }
    
    /**
     * Changes the direction of the snake
     * @param newDirection The new direction
     */
    public void setDirection(Direction newDirection) {
        // Prevent the snake from moving in the opposite direction
        if (!direction.isOpposite(newDirection)) {
            direction = newDirection;
        }
    }
    
    /**
     * Gets the current direction of the snake
     * @return The current direction
     */
    public Direction getDirection() {
        return direction;
    }
    
    /**
     * Gets the head of the snake
     * @return The head position
     */
    public Point getHead() {
        return body.getFirst();
    }
    
    /**
     * Gets the entire body of the snake
     * @return The list of points representing the snake's body
     */
    public List<Point> getBody() {
        return body;
    }
    
    /**
     * Marks that the snake has eaten food
     * This will cause the snake to grow on the next move
     */
    public void grow() {
        hasEaten = true;
        // Add a temporary segment to immediately increase the length
        // This segment will be kept after the next move due to hasEaten flag
        Point tail = body.getLast();
        body.addLast(new Point(tail));
    }
    
    /**
     * Checks if the snake has collided with itself
     * @return true if the snake has collided with itself, false otherwise
     */
    public boolean hasCollidedWithSelf() {
        if (body.size() <= 1) {
            return false;
        }
        
        Point head = getHead();
        
        // Skip the head and check for collisions with the rest of the body
        // Start from index 1 to skip the head itself
        for (int i = 1; i < body.size(); i++) {
            Point segment = body.get(i);
            
            // Use equals to ensure proper comparison of coordinates
            if (head.getX() == segment.getX() && head.getY() == segment.getY()) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Checks if the snake has collided with a wall
     * @param width The width of the game area
     * @param height The height of the game area
     * @return true if the snake has collided with a wall, false otherwise
     */
    public boolean hasCollidedWithWall(int width, int height) {
        Point head = getHead();
        return head.getX() < 0 || head.getX() >= width || head.getY() < 0 || head.getY() >= height;
    }
    
    /**
     * Checks if the snake's head is at the given position
     * @param point The position to check
     * @return true if the snake's head is at the given position, false otherwise
     */
    public boolean isHeadAt(Point point) {
        return getHead().equals(point);
    }
    
    /**
     * Gets the length of the snake
     * @return The length of the snake
     */
    public int getLength() {
        return body.size();
    }
} 