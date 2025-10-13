package com.snake.game;

import javafx.application.Platform;
import javafx.scene.Node;
import javafx.stage.Stage;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.condition.DisabledIf;
import org.testfx.api.FxRobot;
import org.testfx.framework.junit5.ApplicationExtension;
import org.testfx.framework.junit5.Start;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(ApplicationExtension.class)
class SnakeGameAppTest {
    
    private SnakeGameApp app;
    
    private static boolean isJava23OrHigher() {
        String version = System.getProperty("java.version");
        if (version.contains(".")) {
            int majorVersion = Integer.parseInt(version.split("\\.")[0]);
            return majorVersion >= 23;
        }
        return false;
    }
    
    @Start
    private void start(Stage stage) {
        app = new SnakeGameApp();
        app.start(stage);
    }
    
    @Test
    void testInitialScreen(FxRobot robot) {
        // Initial screen should be PlayerNameScreen
        Node playerNameField = robot.lookup("#playerNameField").queryAs(Node.class);
        Node startButton = robot.lookup("#startButton").queryAs(Node.class);
        
        assertNotNull(playerNameField);
        assertNotNull(startButton);
        assertTrue(playerNameField.isVisible());
        assertTrue(startButton.isVisible());
    }
    
    @Test
    void testNavigationToGame(FxRobot robot) {
        // Enter player name and start game
        robot.clickOn("#playerNameField").write("TestPlayer");
        robot.clickOn("#startButton");
        
        // Should be on game screen
        assertNotNull(robot.lookup(".game-screen").queryAs(Node.class));
    }
    
    @Test
    @DisabledIf("isJava23OrHigher")
    void testNavigationToHighScores(FxRobot robot) throws Exception {
        // Use CountDownLatch to wait for JavaFX thread operations
        CountDownLatch latch = new CountDownLatch(1);
        
        // Navigate to high scores on JavaFX thread
        Platform.runLater(() -> {
            try {
                app.showHighScoreScreen();
            } finally {
                latch.countDown();
            }
        });
        
        // Wait for JavaFX operations to complete
        assertTrue(latch.await(5, TimeUnit.SECONDS));
        
        // Should be on high scores screen
        Node highScoreScreen = robot.lookup(".high-score-screen").queryAs(Node.class);
        Node backButton = robot.lookup("#backButton").queryAs(Node.class);
        
        assertNotNull(highScoreScreen);
        assertNotNull(backButton);
    }
    
    @Test
    void testPlayerNamePersistence(FxRobot robot) {
        String testName = "TestPlayer";
        robot.clickOn("#playerNameField").write(testName);
        robot.clickOn("#startButton");
        
        assertEquals(testName, app.getPlayerName());
    }
} 