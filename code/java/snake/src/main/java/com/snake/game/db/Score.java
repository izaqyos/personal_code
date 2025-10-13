package com.snake.game.db;

import java.time.LocalDateTime;

/**
 * Represents a player score in the database
 */
public class Score {
    private int id;
    private String playerName;
    private int score;
    private LocalDateTime createdAt;
    
    /**
     * Creates a new score
     * @param id The score ID
     * @param playerName The player name
     * @param score The score value
     * @param createdAt When the score was created
     */
    public Score(int id, String playerName, int score, LocalDateTime createdAt) {
        this.id = id;
        this.playerName = playerName;
        this.score = score;
        this.createdAt = createdAt;
    }
    
    /**
     * Gets the score ID
     * @return The score ID
     */
    public int getId() {
        return id;
    }
    
    /**
     * Gets the player name
     * @return The player name
     */
    public String getPlayerName() {
        return playerName;
    }
    
    /**
     * Gets the score value
     * @return The score value
     */
    public int getScore() {
        return score;
    }
    
    /**
     * Gets when the score was created
     * @return When the score was created
     */
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    @Override
    public String toString() {
        return String.format("%s: %d", playerName, score);
    }
} 