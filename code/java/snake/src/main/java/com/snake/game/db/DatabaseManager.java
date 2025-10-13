package com.snake.game.db;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Manages database connections and operations for the Snake game
 */
public class DatabaseManager {
    private static final Logger LOGGER = Logger.getLogger(DatabaseManager.class.getName());
    private static final String DB_URL = "jdbc:postgresql://localhost:5432/snake_game_db";
    private static final String DB_USER = "snake";
    private static final String DB_PASSWORD = "password";
    
    private static HikariDataSource dataSource;
    
    static {
        initialize();
    }
    
    /**
     * Initializes the database connection pool
     */
    private static void initialize() {
        try {
            HikariConfig config = new HikariConfig();
            config.setJdbcUrl(System.getProperty("DB_URL", DB_URL));
            config.setUsername(System.getProperty("DB_USER", DB_USER));
            config.setPassword(System.getProperty("DB_PASSWORD", DB_PASSWORD));
            config.setMaximumPoolSize(10);
            config.setMinimumIdle(2);
            config.setIdleTimeout(30000);
            config.setConnectionTimeout(20000);
            
            dataSource = new HikariDataSource(config);
            LOGGER.info("Database connection pool initialized successfully");
        } catch (Exception e) {
            LOGGER.log(Level.SEVERE, "Failed to initialize database connection pool", e);
        }
    }
    
    /**
     * Gets a connection from the pool
     * @return A database connection
     * @throws SQLException if connection fails
     */
    public static Connection getConnection() throws SQLException {
        if (dataSource == null) {
            initialize();
        }
        return dataSource.getConnection();
    }
    
    /**
     * Saves a player's score to the database
     * @param playerName The name of the player
     * @param score The player's score
     * @return true if score was saved successfully, false otherwise
     */
    public static boolean saveScore(String playerName, int score) {
        // Validate input
        if (playerName == null || playerName.trim().isEmpty()) {
            LOGGER.warning("Invalid player name: empty or null");
            return false;
        }
        
        if (score < 0) {
            LOGGER.warning("Invalid score: " + score + " (must be non-negative)");
            return false;
        }
        
        String sql = "INSERT INTO player_scores (player_name, score) VALUES (?, ?)";
        
        try (Connection conn = getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            
            pstmt.setString(1, playerName);
            pstmt.setInt(2, score);
            
            int rowsAffected = pstmt.executeUpdate();
            return rowsAffected > 0;
            
        } catch (SQLException e) {
            LOGGER.log(Level.SEVERE, "Error saving score", e);
            return false;
        }
    }
    
    /**
     * PlayerScore record to hold score data
     */
    public static class PlayerScore {
        private final String playerName;
        private final int score;
        private final Timestamp datePlayed;
        
        public PlayerScore(String playerName, int score, Timestamp datePlayed) {
            this.playerName = playerName;
            this.score = score;
            this.datePlayed = datePlayed;
        }
        
        public String getPlayerName() {
            return playerName;
        }
        
        public int getScore() {
            return score;
        }
        
        public Timestamp getDatePlayed() {
            return datePlayed;
        }
    }
    
    /**
     * Gets the top scores from the database
     * @param limit The maximum number of scores to return
     * @return A list of PlayerScore objects
     */
    public static List<PlayerScore> getTopScores(int limit) {
        String sql = "SELECT player_name, score, date_played FROM player_scores ORDER BY score DESC LIMIT ?";
        List<PlayerScore> scores = new ArrayList<>();
        
        try (Connection conn = getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            
            pstmt.setInt(1, limit);
            
            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    String playerName = rs.getString("player_name");
                    int score = rs.getInt("score");
                    Timestamp datePlayed = rs.getTimestamp("date_played");
                    
                    scores.add(new PlayerScore(playerName, score, datePlayed));
                }
            }
            
        } catch (SQLException e) {
            LOGGER.log(Level.SEVERE, "Error retrieving top scores", e);
        }
        
        return scores;
    }
    
    /**
     * Closes the database connection pool
     */
    public static void closeConnectionPool() {
        if (dataSource != null && !dataSource.isClosed()) {
            dataSource.close();
        }
    }
} 