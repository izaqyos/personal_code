package com.snake.game;

import com.snake.game.db.DatabaseManager;
import com.snake.game.ui.GameScreen;
import com.snake.game.ui.HighScoreScreen;
import com.snake.game.ui.PlayerNameScreen;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;

/**
 * Main application class for the Snake game
 */
public class SnakeGameApp extends Application {
    
    private Stage primaryStage;
    private String currentPlayerName;
    
    /**
     * Application entry point
     * @param args Command line arguments
     */
    public static void main(String[] args) {
        launch(args);
    }
    
    @Override
    public void start(Stage primaryStage) {
        this.primaryStage = primaryStage;
        primaryStage.setTitle("Snake Game");
        primaryStage.setResizable(false);
        
        // Show player name screen first
        showPlayerNameScreen();
        
        primaryStage.show();
    }
    
    @Override
    public void stop() {
        // Close database connection pool when application closes
        DatabaseManager.closeConnectionPool();
    }
    
    /**
     * Shows the player name input screen
     */
    public void showPlayerNameScreen() {
        PlayerNameScreen playerNameScreen = new PlayerNameScreen(this);
        Scene scene = new Scene(playerNameScreen, 400, 300);
        primaryStage.setScene(scene);
        primaryStage.sizeToScene();
    }
    
    /**
     * Shows the game screen with the specified player name
     * @param playerName The name of the player
     */
    public void showGameScreen(String playerName) {
        this.currentPlayerName = playerName;
        GameScreen gameScreen = new GameScreen(this);
        gameScreen.setPlayerName(playerName);
        gameScreen.startGame();
        
        Scene scene = new Scene(gameScreen, 600, 600);
        scene.setOnKeyPressed(gameScreen::handleKeyPress);
        
        primaryStage.setScene(scene);
        primaryStage.sizeToScene();
        
        // Request focus to capture key events
        gameScreen.requestFocus();
    }
    
    /**
     * Shows the high score screen
     */
    public void showHighScoreScreen() {
        HighScoreScreen highScoreScreen = new HighScoreScreen(this);
        highScoreScreen.loadScores();
        
        Scene scene = new Scene(highScoreScreen, 400, 400);
        primaryStage.setScene(scene);
        primaryStage.sizeToScene();
    }
    
    /**
     * Gets the current player name
     * @return The current player name
     */
    public String getPlayerName() {
        return currentPlayerName;
    }
}