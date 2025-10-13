package com.snake.game.ui;

import com.snake.game.SnakeGameApp;
import com.snake.game.db.DatabaseManager;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.List;

/**
 * Screen for displaying high scores
 */
public class HighScoreScreen extends BorderPane {
    
    private final SnakeGameApp app;
    private final TableView<ScoreEntry> scoreTable;
    
    /**
     * Creates a new high score screen
     * @param app The main application
     */
    public HighScoreScreen(SnakeGameApp app) {
        this.app = app;
        
        // Add CSS class for testing
        getStyleClass().add("high-score-screen");
        
        // Configure layout
        setPadding(new Insets(20));
        
        // Create title
        Label titleLabel = new Label("High Scores");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 24));
        
        // Create score table
        scoreTable = new TableView<>();
        scoreTable.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY);
        
        // Add columns
        TableColumn<ScoreEntry, String> nameColumn = new TableColumn<>("Player");
        nameColumn.setCellValueFactory(new PropertyValueFactory<>("playerName"));
        
        TableColumn<ScoreEntry, Integer> scoreColumn = new TableColumn<>("Score");
        scoreColumn.setCellValueFactory(new PropertyValueFactory<>("score"));
        
        TableColumn<ScoreEntry, String> dateColumn = new TableColumn<>("Date");
        dateColumn.setCellValueFactory(new PropertyValueFactory<>("dateString"));
        
        scoreTable.getColumns().addAll(nameColumn, scoreColumn, dateColumn);
        
        // Create back button
        Button backButton = new Button("Back to Menu");
        backButton.setPrefWidth(150);
        backButton.setId("backButton");
        backButton.setOnAction(e -> app.showPlayerNameScreen());
        
        Button newGameButton = new Button("New Game");
        newGameButton.setPrefWidth(150);
        newGameButton.setOnAction(e -> {
            if (app.getPlayerName() != null && !app.getPlayerName().isEmpty()) {
                app.showGameScreen(app.getPlayerName());
            } else {
                app.showPlayerNameScreen();
            }
        });
        
        // Create bottom panel
        VBox bottomPanel = new VBox(10);
        bottomPanel.setAlignment(Pos.CENTER);
        bottomPanel.setPadding(new Insets(20, 0, 0, 0));
        bottomPanel.getChildren().addAll(backButton, newGameButton);
        
        // Add components to layout
        VBox topPanel = new VBox(10);
        topPanel.setAlignment(Pos.CENTER);
        topPanel.getChildren().add(titleLabel);
        
        setTop(topPanel);
        setCenter(scoreTable);
        setBottom(bottomPanel);
    }
    
    /**
     * Loads scores from the database
     */
    public void loadScores() {
        scoreTable.getItems().clear();
        
        List<DatabaseManager.PlayerScore> scores = DatabaseManager.getTopScores(10);
        
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm");
        
        for (DatabaseManager.PlayerScore score : scores) {
            ScoreEntry entry = new ScoreEntry(
                    score.getPlayerName(),
                    score.getScore(),
                    dateFormat.format(score.getDatePlayed())
            );
            scoreTable.getItems().add(entry);
        }
    }
    
    /**
     * Score entry for the table view
     */
    public static class ScoreEntry {
        private final String playerName;
        private final int score;
        private final String dateString;
        
        public ScoreEntry(String playerName, int score, String dateString) {
            this.playerName = playerName;
            this.score = score;
            this.dateString = dateString;
        }
        
        public String getPlayerName() {
            return playerName;
        }
        
        public int getScore() {
            return score;
        }
        
        public String getDateString() {
            return dateString;
        }
    }
} 