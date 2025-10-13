package com.snake.game.ui;

import com.snake.game.SnakeGameApp;
import com.snake.game.model.Direction;
import com.snake.game.model.Food;
import com.snake.game.model.Game;
import com.snake.game.model.Point;
import com.snake.game.model.Snake;
import javafx.animation.AnimationTimer;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;

import java.util.List;

/**
 * Screen for the actual Snake game
 */
public class GameScreen extends BorderPane {
    
    private final SnakeGameApp app;
    private Game game;
    private Canvas gameCanvas;
    private GraphicsContext gc;
    private AnimationTimer gameLoop;
    private Label scoreLabel;
    private VBox gameOverBox;
    private long lastUpdate = 0;
    
    // Game settings
    private static final int CELL_SIZE = 25;
    private static final int GAME_WIDTH = 20;
    private static final int GAME_HEIGHT = 20;
    private static final long UPDATE_FREQUENCY = 150_000_000; // nanoseconds (150ms)
    
    /**
     * Creates a new game screen
     * @param app The main application
     */
    public GameScreen(SnakeGameApp app) {
        this.app = app;
        
        // Add CSS class for testing
        getStyleClass().add("game-screen");
        
        // Create game model
        game = new Game(GAME_WIDTH, GAME_HEIGHT);
        
        // Set up layout
        setPadding(new Insets(10));
        
        // Create the game canvas
        gameCanvas = new Canvas(GAME_WIDTH * CELL_SIZE, GAME_HEIGHT * CELL_SIZE);
        gc = gameCanvas.getGraphicsContext2D();
        
        // Create score panel
        scoreLabel = new Label("Score: 0");
        scoreLabel.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        
        HBox topPanel = new HBox(10);
        topPanel.setAlignment(Pos.CENTER);
        topPanel.getChildren().add(scoreLabel);
        
        // Create game over panel (initially hidden)
        gameOverBox = createGameOverPanel();
        gameOverBox.setVisible(false);
        gameOverBox.setManaged(false); // Don't take up space when not visible
        
        // Create a stackpane to overlay game over panel on canvas
        StackPane gameContainer = new StackPane();
        gameContainer.getChildren().addAll(gameCanvas, gameOverBox);
        
        // Add components to layout
        setTop(topPanel);
        setCenter(gameContainer);
        
        // Create game loop
        gameLoop = new AnimationTimer() {
            @Override
            public void handle(long now) {
                if (now - lastUpdate >= UPDATE_FREQUENCY) {
                    updateGame();
                    renderGame();
                    lastUpdate = now;
                }
            }
        };
    }
    
    /**
     * Creates the game over panel
     * @return The game over panel
     */
    private VBox createGameOverPanel() {
        VBox panel = new VBox(15);  // Increased spacing
        panel.setAlignment(Pos.CENTER);
        panel.setPadding(new Insets(25));
        panel.setStyle("-fx-background-color: rgba(0, 0, 0, 0.85); -fx-background-radius: 10;");
        panel.setMinWidth(300);
        panel.setMaxWidth(300);
        panel.setMinHeight(300);
        
        Label gameOverLabel = new Label("Game Over!");
        gameOverLabel.setFont(Font.font("Arial", FontWeight.BOLD, 28));
        gameOverLabel.setTextFill(Color.RED);
        
        Label finalScoreLabel = new Label();
        finalScoreLabel.setFont(Font.font("Arial", 20));
        finalScoreLabel.setTextFill(Color.WHITE);
        finalScoreLabel.setPadding(new Insets(10, 0, 20, 0));
        
        // Style for all buttons
        String buttonStyle = "-fx-font-size: 14px; -fx-background-radius: 5; -fx-padding: 8 15 8 15;";
        
        Button restartButton = new Button("Play Again");
        restartButton.setPrefWidth(200);
        restartButton.setStyle(buttonStyle + "-fx-background-color: #4CAF50; -fx-text-fill: white;");
        restartButton.setOnAction(e -> startGame());
        
        Button menuButton = new Button("Main Menu");
        menuButton.setPrefWidth(200);
        menuButton.setStyle(buttonStyle + "-fx-background-color: #2196F3; -fx-text-fill: white;");
        menuButton.setOnAction(e -> app.showPlayerNameScreen());
        
        Button highScoreButton = new Button("High Scores");
        highScoreButton.setPrefWidth(200);
        highScoreButton.setStyle(buttonStyle + "-fx-background-color: #FF9800; -fx-text-fill: white;");
        highScoreButton.setOnAction(e -> app.showHighScoreScreen());
        
        VBox buttonBox = new VBox(10);
        buttonBox.setAlignment(Pos.CENTER);
        buttonBox.getChildren().addAll(restartButton, menuButton, highScoreButton);
        
        panel.getChildren().addAll(
                gameOverLabel,
                finalScoreLabel,
                buttonBox
        );
        
        // Store reference to update when game ends
        panel.setUserData(finalScoreLabel);
        
        return panel;
    }
    
    /**
     * Sets the player name for the game
     * @param playerName The name of the player
     */
    public void setPlayerName(String playerName) {
        game.setPlayerName(playerName);
    }
    
    /**
     * Starts or restarts the game
     */
    public void startGame() {
        // Initialize game model
        game.initialize();
        
        // Hide game over panel
        gameOverBox.setVisible(false);
        gameOverBox.setManaged(false);
        
        // Start game loop
        lastUpdate = 0;
        gameLoop.start();
    }
    
    /**
     * Updates the game state
     */
    private void updateGame() {
        game.update();
        
        // Update score label
        scoreLabel.setText("Score: " + game.getScore());
        
        // Check if game is over
        if (game.isGameOver()) {
            gameLoop.stop();
            showGameOver();
        }
    }
    
    /**
     * Shows the game over screen
     */
    private void showGameOver() {
        Label finalScoreLabel = (Label) gameOverBox.getUserData();
        finalScoreLabel.setText("Your Score: " + game.getScore());
        gameOverBox.setVisible(true);
        gameOverBox.setManaged(true);
        
        // Center the game over box
        gameOverBox.toFront();
        gameOverBox.requestFocus();
        
        // Style for better visibility
        gameOverBox.setStyle("-fx-background-color: rgba(0, 0, 0, 0.8); -fx-padding: 20px; -fx-background-radius: 10;");
        
        // Ensure UI is updated
        gameOverBox.requestLayout();
        this.requestLayout();
    }
    
    /**
     * Renders the game on the canvas
     */
    private void renderGame() {
        // Clear canvas
        gc.setFill(Color.BLACK);
        gc.fillRect(0, 0, gameCanvas.getWidth(), gameCanvas.getHeight());
        
        // Draw grid lines (optional)
        gc.setStroke(Color.DARKGRAY);
        gc.setLineWidth(0.5);
        
        for (int x = 0; x <= GAME_WIDTH; x++) {
            gc.strokeLine(x * CELL_SIZE, 0, x * CELL_SIZE, GAME_HEIGHT * CELL_SIZE);
        }
        
        for (int y = 0; y <= GAME_HEIGHT; y++) {
            gc.strokeLine(0, y * CELL_SIZE, GAME_WIDTH * CELL_SIZE, y * CELL_SIZE);
        }
        
        // Draw food
        Food food = game.getFood();
        Point foodPos = food.getPosition();
        gc.setFill(Color.RED);
        gc.fillOval(
                foodPos.getX() * CELL_SIZE, 
                foodPos.getY() * CELL_SIZE, 
                CELL_SIZE, 
                CELL_SIZE
        );
        
        // Draw snake
        Snake snake = game.getSnake();
        List<Point> snakeBody = snake.getBody();
        
        // Draw snake body
        gc.setFill(Color.LIMEGREEN);
        for (int i = 1; i < snakeBody.size(); i++) {
            Point segment = snakeBody.get(i);
            gc.fillRect(
                    segment.getX() * CELL_SIZE, 
                    segment.getY() * CELL_SIZE, 
                    CELL_SIZE, 
                    CELL_SIZE
            );
        }
        
        // Draw snake head with different color
        Point head = snakeBody.get(0);
        gc.setFill(Color.GREEN);
        gc.fillRect(
                head.getX() * CELL_SIZE, 
                head.getY() * CELL_SIZE, 
                CELL_SIZE, 
                CELL_SIZE
        );
    }
    
    /**
     * Handles key press events for controlling the snake
     * @param event The key press event
     */
    public void handleKeyPress(KeyEvent event) {
        KeyCode code = event.getCode();
        
        if (game.isGameOver()) {
            if (code == KeyCode.SPACE) {
                startGame();
            }
            return;
        }
        
        switch (code) {
            case UP:
                game.changeDirection(Direction.UP);
                break;
            case DOWN:
                game.changeDirection(Direction.DOWN);
                break;
            case LEFT:
                game.changeDirection(Direction.LEFT);
                break;
            case RIGHT:
                game.changeDirection(Direction.RIGHT);
                break;
            case P:
                game.togglePause();
                break;
            case ESCAPE:
                gameLoop.stop();
                app.showPlayerNameScreen();
                break;
            default:
                break;
        }
        
        event.consume();
    }
}