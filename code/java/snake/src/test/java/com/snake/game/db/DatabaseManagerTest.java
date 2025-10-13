package com.snake.game.db;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@Testcontainers
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class DatabaseManagerTest {
    
    @Container
    private static final PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:latest")
            .withDatabaseName("snake_test")
            .withUsername("test")
            .withPassword("test");
    
    @BeforeAll
    void setUp() {
        postgres.start();
        
        // Configure DatabaseManager with test container
        System.setProperty("DB_URL", postgres.getJdbcUrl());
        System.setProperty("DB_USER", postgres.getUsername());
        System.setProperty("DB_PASSWORD", postgres.getPassword());
        
        // Initialize database
        try (Connection conn = DatabaseManager.getConnection()) {
            conn.createStatement().execute(
                "CREATE TABLE IF NOT EXISTS player_scores (" +
                "id SERIAL PRIMARY KEY," +
                "player_name VARCHAR(50) NOT NULL," +
                "score INTEGER NOT NULL," +
                "date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP" +
                ")"
            );
        } catch (SQLException e) {
            fail("Failed to initialize test database", e);
        }
    }
    
    @BeforeEach
    void clearDatabase() {
        // Clear all existing data before each test
        try (Connection conn = DatabaseManager.getConnection();
             PreparedStatement ps = conn.prepareStatement("DELETE FROM player_scores")) {
            ps.executeUpdate();
        } catch (SQLException e) {
            fail("Failed to clear test database", e);
        }
    }
    
    @Test
    void testSaveScore() {
        // Save a specific player name and score
        String testPlayer = "TestPlayerUnique";
        int testScore = 123;
        
        boolean result = DatabaseManager.saveScore(testPlayer, testScore);
        assertTrue(result);
        
        // Get the top score which should be what we just saved
        List<DatabaseManager.PlayerScore> scores = DatabaseManager.getTopScores(1);
        assertFalse(scores.isEmpty());
        assertEquals(testPlayer, scores.get(0).getPlayerName());
        assertEquals(testScore, scores.get(0).getScore());
    }
    
    @Test
    void testGetTopScores() {
        // Save multiple scores
        DatabaseManager.saveScore("Player1", 100);
        DatabaseManager.saveScore("Player2", 200);
        DatabaseManager.saveScore("Player3", 150);
        
        List<DatabaseManager.PlayerScore> topScores = DatabaseManager.getTopScores(3);
        assertEquals(3, topScores.size());
        assertEquals(200, topScores.get(0).getScore()); // Highest score first
        assertEquals("Player2", topScores.get(0).getPlayerName());
    }
    
    @Test
    void testConnectionPool() {
        try (Connection conn1 = DatabaseManager.getConnection();
             Connection conn2 = DatabaseManager.getConnection()) {
            
            assertNotNull(conn1);
            assertNotNull(conn2);
            assertNotSame(conn1, conn2);
        } catch (SQLException e) {
            fail("Failed to get connections from pool", e);
        }
    }
    
    @Test
    void testInvalidScoreSave() {
        // Test with invalid player name
        boolean result = DatabaseManager.saveScore("", 100);
        assertFalse(result);
        
        // Test with negative score
        result = DatabaseManager.saveScore("TestPlayer", -100);
        assertFalse(result);
    }
} 