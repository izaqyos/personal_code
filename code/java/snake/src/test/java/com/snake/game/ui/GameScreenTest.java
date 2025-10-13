package com.snake.game.ui;

import com.snake.game.SnakeGameApp;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.stage.Stage;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.condition.DisabledIf;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;
import org.testfx.framework.junit5.ApplicationExtension;
import org.testfx.framework.junit5.Start;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith({ApplicationExtension.class, MockitoExtension.class})
class GameScreenTest {
    
    private GameScreen gameScreen;
    
    @Spy
    private SnakeGameApp app = new SnakeGameApp();
    
    private static boolean isJava23OrHigher() {
        String version = System.getProperty("java.version");
        if (version.contains(".")) {
            int majorVersion = Integer.parseInt(version.split("\\.")[0]);
            return majorVersion >= 23;
        }
        return false;
    }
    
    @BeforeEach
    void checkJavaVersion() {
        if (isJava23OrHigher()) {
            System.out.println("Tests are running on Java 23+. Some tests may be skipped.");
        }
    }
    
    @Start
    private void start(Stage stage) {
        if (!isJava23OrHigher()) {
            gameScreen = new GameScreen(app);
        }
    }
    
    @Test
    @DisabledIf("isJava23OrHigher")
    void testGameInitialization() {
        gameScreen.setPlayerName("TestPlayer");
        gameScreen.startGame();
        
        assertNotNull(gameScreen.lookup("#scoreLabel"));
        assertFalse(gameScreen.lookup("#gameOverBox").isVisible());
    }
    
    @Test
    @DisabledIf("isJava23OrHigher")
    void testKeyboardControls() {
        gameScreen.setPlayerName("TestPlayer");
        gameScreen.startGame();
        
        // Test arrow keys
        gameScreen.handleKeyPress(new KeyEvent(KeyEvent.KEY_PRESSED, "", "", KeyCode.UP, false, false, false, false));
        gameScreen.handleKeyPress(new KeyEvent(KeyEvent.KEY_PRESSED, "", "", KeyCode.DOWN, false, false, false, false));
        gameScreen.handleKeyPress(new KeyEvent(KeyEvent.KEY_PRESSED, "", "", KeyCode.LEFT, false, false, false, false));
        gameScreen.handleKeyPress(new KeyEvent(KeyEvent.KEY_PRESSED, "", "", KeyCode.RIGHT, false, false, false, false));
        
        // Test pause
        gameScreen.handleKeyPress(new KeyEvent(KeyEvent.KEY_PRESSED, "", "", KeyCode.P, false, false, false, false));
        
        // Test escape
        gameScreen.handleKeyPress(new KeyEvent(KeyEvent.KEY_PRESSED, "", "", KeyCode.ESCAPE, false, false, false, false));
        verify(app).showPlayerNameScreen();
    }
    
    @Test
    @DisabledIf("isJava23OrHigher")
    void testGameOver() {
        gameScreen.setPlayerName("TestPlayer");
        gameScreen.startGame();
        
        // Force game over by moving snake to wall multiple times
        for (int i = 0; i < 30; i++) {
            gameScreen.handleKeyPress(new KeyEvent(KeyEvent.KEY_PRESSED, "", "", KeyCode.RIGHT, false, false, false, false));
            try {
                Thread.sleep(200);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        assertTrue(gameScreen.lookup("#gameOverBox").isVisible());
    }
    
    @Test
    @DisabledIf("isJava23OrHigher")
    void testRestartGame() {
        gameScreen.setPlayerName("TestPlayer");
        gameScreen.startGame();
        
        // Force game over
        for (int i = 0; i < 30; i++) {
            gameScreen.handleKeyPress(new KeyEvent(KeyEvent.KEY_PRESSED, "", "", KeyCode.RIGHT, false, false, false, false));
        }
        
        // Restart game with space
        gameScreen.handleKeyPress(new KeyEvent(KeyEvent.KEY_PRESSED, "", "", KeyCode.SPACE, false, false, false, false));
        assertFalse(gameScreen.lookup("#gameOverBox").isVisible());
    }
} 