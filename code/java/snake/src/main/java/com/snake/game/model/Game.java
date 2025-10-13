package com.snake.game.model;

import com.snake.game.db.DatabaseManager;
import java.util.logging.Logger;

/**
 * Manages the game state and logic
 */
public class Game {
    private static final Logger LOGGER = Logger.getLogger(Game.class.getName());
    
    private static final int DEFAULT_WIDTH = 20;
    private static final int DEFAULT_HEIGHT = 20;
    private static final int INITIAL_SNAKE_LENGTH = 3;
    
    private final int width;
    private final int height;
    private Snake snake;
    private Food food;
    private boolean gameOver;
    private boolean paused;
    private int score;
    private String playerName;
    
    /**
     * Creates a new game with default dimensions
     */
    public Game() {
        this(DEFAULT_WIDTH, DEFAULT_HEIGHT);
    }
    
    /**
     * Creates a new game with the specified dimensions
     * @param width The width of the game area
     * @param height The height of the game area
     */
    public Game(int width, int height) {
        this.width = width;
        this.height = height;
        this.gameOver = false;
        this.paused = false;
        this.score = 0;
    }
    
    /**
     * Sets the player name
     * @param playerName The name of the player
     */
    public void setPlayerName(String playerName) {
        this.playerName = playerName;
    }
    
    /**
     * Gets the player name
     * @return The name of the player
     */
    public String getPlayerName() {
        return playerName;
    }
    
    /**
     * Initializes the game
     */
    public void initialize() {
        // Create snake in the middle of the screen moving right
        int startX = width / 2;
        int startY = height / 2;
        snake = new Snake(startX, startY, INITIAL_SNAKE_LENGTH, Direction.RIGHT);
        
        // Create and place food
        food = new Food();
        food.randomizePosition(width, height, snake);
        
        // Reset game state
        gameOver = false;
        paused = false;
        score = 0;
        
        LOGGER.info("Game initialized with player: " + playerName);
    }
    
    /**
     * Updates the game state
     */
    public void update() {
        if (gameOver || paused) {
            return;
        }
        
        // Move snake
        snake.move();
        
        // Check if snake ate food
        if (snake.isHeadAt(food.getPosition())) {
            score += 10;
            snake.grow();
            food.randomizePosition(width, height, snake);
        }
        
        // Check collisions
        if (snake.hasCollidedWithWall(width, height) || snake.hasCollidedWithSelf()) {
            gameOver = true;
            saveScore();
        }
    }
    
    /**
     * Changes the direction of the snake
     * @param direction The new direction
     */
    public void changeDirection(Direction direction) {
        if (!gameOver && !paused) {
            snake.setDirection(direction);
        }
    }
    
    /**
     * Toggles the paused state of the game
     */
    public void togglePause() {
        paused = !paused;
    }
    
    /**
     * Checks if the game is over
     * @return true if the game is over, false otherwise
     */
    public boolean isGameOver() {
        return gameOver;
    }
    
    /**
     * Checks if the game is paused
     * @return true if the game is paused, false otherwise
     */
    public boolean isPaused() {
        return paused;
    }
    
    /**
     * Gets the current score
     * @return The current score
     */
    public int getScore() {
        return score;
    }
    
    /**
     * Gets the snake
     * @return The snake
     */
    public Snake getSnake() {
        return snake;
    }
    
    /**
     * Gets the food
     * @return The food
     */
    public Food getFood() {
        return food;
    }
    
    /**
     * Gets the width of the game area
     * @return The width
     */
    public int getWidth() {
        return width;
    }
    
    /**
     * Gets the height of the game area
     * @return The height
     */
    public int getHeight() {
        return height;
    }
    
    /**
     * Saves the player's score to the database
     */
    private void saveScore() {
        if (playerName != null && !playerName.isEmpty()) {
            boolean success = DatabaseManager.saveScore(playerName, score);
            if (success) {
                LOGGER.info("Score saved: " + playerName + " - " + score);
            } else {
                LOGGER.warning("Failed to save score for: " + playerName);
            }
        }
    }
} 