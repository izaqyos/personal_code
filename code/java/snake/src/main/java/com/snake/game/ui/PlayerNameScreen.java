package com.snake.game.ui;

import com.snake.game.SnakeGameApp;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;

/**
 * Screen for entering player name
 */
public class PlayerNameScreen extends VBox {
    
    private final SnakeGameApp app;
    private final TextField nameField;
    
    /**
     * Creates a new player name screen
     * @param app The main application
     */
    public PlayerNameScreen(SnakeGameApp app) {
        this.app = app;
        
        // Add CSS class for testing
        getStyleClass().add("player-name-screen");
        
        // Configure layout
        setSpacing(20);
        setPadding(new Insets(30));
        setAlignment(Pos.CENTER);
        
        // Create title
        Label titleLabel = new Label("Snake Game");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 24));
        
        // Create name input
        Label nameLabel = new Label("Enter Your Name:");
        nameLabel.setFont(Font.font("Arial", 16));
        
        nameField = new TextField();
        nameField.setMaxWidth(200);
        nameField.setPromptText("Enter your name");
        nameField.setId("playerNameField"); // Add ID for testing
        
        // Create buttons
        Button startButton = new Button("Start Game");
        startButton.setPrefWidth(200);
        startButton.setId("startButton"); // Add ID for testing
        startButton.setOnAction(e -> startGame());
        
        Button highScoreButton = new Button("High Scores");
        highScoreButton.setPrefWidth(150);
        highScoreButton.setOnAction(e -> app.showHighScoreScreen());
        
        // Add components to layout
        getChildren().addAll(
                titleLabel,
                nameLabel,
                nameField,
                startButton,
                highScoreButton
        );
        
        // Allow enter key to start game
        nameField.setOnAction(e -> startGame());
    }
    
    /**
     * Starts the game with the entered player name
     */
    private void startGame() {
        String playerName = nameField.getText().trim();
        
        if (playerName.isEmpty()) {
            playerName = "Player";
        }
        
        app.showGameScreen(playerName);
    }
} 