# Snake Game 🐍

A classic Snake game built with JavaFX, featuring high score tracking and a modern user interface.

## 🎮 How to Play

### Starting the Game
1. Launch the game
2. Enter your name when prompted
3. The game will start automatically

### Controls
- **Arrow Keys**: Control the snake's direction
  - ↑ Up Arrow: Move up
  - ↓ Down Arrow: Move down
  - ← Left Arrow: Move left
  - → Right Arrow: Move right
- **P Key**: Pause/Resume the game
- **ESC Key**: Return to main menu
- **Space Key**: Restart game (when game is over)

### Game Rules
- Guide the snake to eat the red food
- Each food eaten increases your score by 10 points
- The snake grows longer with each food eaten
- Game ends if you:
  - Hit the walls
  - Hit yourself
  - Press ESC to return to menu

### Features
- **Score Tracking**: Your scores are saved automatically
- **High Scores**: View the top players' scores
- **Player Names**: Personalize your gaming experience
- **Modern UI**: Clean, responsive interface
- **Pause Function**: Take a break anytime with the P key

### Tips
- Plan your moves ahead to avoid getting trapped
- Use the grid lines to help with navigation
- Try to create space between the snake's head and body
- Watch out for the snake's growing length

## 🏆 High Scores
- View your best scores and compete with other players
- Access the high scores screen from the main menu or game over screen
- Scores are saved automatically when the game ends

## 🎯 Game Over Options
When your game ends, you can:
1. Play Again: Start a new game immediately
2. Main Menu: Return to the player name screen
3. High Scores: View the leaderboard

## 🧪 Testing

### Test Suite Overview
The game includes a comprehensive test suite covering all major components:

#### Model Tests
- `PointTest`: Coordinate system and point equality
- `SnakeTest`: Snake movement, growth, and collision detection
- `GameTest`: Game state management and scoring
- `FoodTest`: Food placement and randomization

#### UI Tests
- `SnakeGameAppTest`: Screen navigation and UI state
- `GameScreenTest`: Game controls and display
- `PlayerNameScreenTest`: Input validation and navigation
- `HighScoreScreenTest`: Score display and sorting

#### Database Tests
- `DatabaseManagerTest`: Score persistence and retrieval
- Uses Testcontainers for isolated database testing

### Running Tests

#### Run All Tests
```bash
mvn test
```

#### Run Specific Test Class
```bash
mvn test -Dtest=GameTest
```

#### Run Specific Test Method
```bash
mvn test -Dtest=GameTest#testScoreIncrease
```

### Test Coverage
The project uses JaCoCo for code coverage analysis:

1. Generate coverage report:
```bash
mvn clean test
```

2. View the report:
```bash
open target/site/jacoco/index.html
```

### Test Categories

#### Unit Tests
- Test individual components in isolation
- Mock external dependencies
- Fast execution

#### Integration Tests
- Test component interactions
- Use TestFX for JavaFX UI testing
- Database integration with Testcontainers

#### UI Tests
- Simulate user interactions
- Verify screen transitions
- Test keyboard controls

### Test Dependencies
- JUnit 5: Testing framework
- TestFX: JavaFX UI testing
- Mockito: Mocking framework
- Testcontainers: Database testing
- JaCoCo: Code coverage

### Troubleshooting Tests

If you encounter test failures, check the following:

#### JaCoCo and Java Version
- JaCoCo 0.8.11 has compatibility issues with Java 23 (class file version 67)
- Use Java 17 or lower for running tests with coverage, or use the following command to skip JaCoCo:
```bash
mvn test -Djacoco.skip=true
```

#### UI Tests
- For TestFX failures: Ensure JavaFX components have proper ID attributes or CSS classes
- For headless environments: Add `-Djava.awt.headless=true -Dtestfx.robot=glass -Dtestfx.headless=true` to test options
- UI tests may fail on macOS due to permissions; run in non-headless mode first
- TestFX requires the `testfx-monocle` dependency for headless testing
- When mocking JavaFX components, use `spy()` instead of `mock()` for Application classes

#### Database Tests
- Testcontainers requires Docker running on your machine
- PostgreSQL container may take time to initialize; increase timeouts if needed
- Ensure database credentials in test match container configuration
- Use the following command to run only model tests (avoiding database tests):
```bash
mvn test -Dtest="*Point*Test,*Snake*Test,*Game*Test,*Food*Test" -Djacoco.skip=true
```

#### Mocked Components
- If using `@Mock` annotations, ensure `MockitoExtension.class` is included in `@ExtendWith`
- Verify the behavior of mocked dependencies matches actual component behavior
- JavaFX `Application` class cannot be easily mocked; consider using interfaces for better testability

#### Test Isolation
- Each test should clean up resources to avoid affecting other tests
- Use `@BeforeEach` and `@AfterEach` to set up and tear down test environments
- Add the following to your `.gitignore` to avoid committing test reports:
```
target/
*.hprof
*.log
.DS_Store
.testcontainers*
```

### Known Issues

#### Java 23 Compatibility
- The project uses ByteBuddy via Mockito which officially supports up to Java 22
- When running with Java 23, you may see errors like:
```
Java 23 (67) is not supported by the current version of Byte Buddy which officially supports Java 22 (66)
```
- Solutions:
  1. Use Java 17 or 21 for testing: `export JAVA_HOME=/path/to/java17`
  2. Add VM property: `-Dnet.bytebuddy.experimental=true`
  3. Skip UI tests that use Mockito: `mvn test -Dtest="!*GameScreen*,!*SnakeGameApp*" -Djacoco.skip=true`

#### JavaFX Threading Issues
- Tests that involve JavaFX may fail with:
```
java.lang.IllegalStateException: Not on FX application thread; currentThread = main
```
- Solutions:
  1. Use `Platform.runLater()` for JavaFX-related code in tests
  2. Use TestFX's `FxRobot` for UI interaction
  3. Consider refactoring to separate UI logic from business logic for better testability

#### Database Testing
- The `DatabaseManagerTest` relies on H2 in-memory database
- Each test should clean up the database state to ensure isolation
- To run only database tests:
```bash
mvn test -Dtest="*DatabaseManagerTest" -Djacoco.skip=true
```

### Recommended Test Strategy

1. **Core Model Tests First**
   ```bash
   mvn test -Dtest="*Point*Test,*Snake*Test,*Game*Test,*Food*Test" -Djacoco.skip=true
   ```

2. **Database Tests Second**
   ```bash
   mvn test -Dtest="*DatabaseManagerTest" -Djacoco.skip=true
   ```

3. **UI Tests Last (may require specific setup)**
   ```bash
   mvn test -Dtest="*Screen*Test,*App*Test" -Djacoco.skip=true
   ```

4. **Track Test Coverage for Model Classes**
   ```bash
   mvn test -Dtest="*Point*Test,*Snake*Test,*Game*Test,*Food*Test"
   ```

### Using Maven Profiles

The project includes several Maven profiles to simplify running different test categories:

#### Model Tests
Tests only the core game logic classes:
```bash
mvn test -P model-tests
```

#### Database Tests
Tests only the database functionality:
```bash
mvn test -P db-tests
```

#### UI Tests
Tests the JavaFX UI components (may be skipped on Java 23+):
```bash
mvn test -P ui-tests
```

#### All Tests
Runs all tests with ByteBuddy experimental mode for Java 23+ compatibility:
```bash
mvn test -P all-tests
```

### Using the run.sh Script

For convenience, a `run.sh` script is provided that offers a simple interface for building, running, and testing the game:

```bash
# Make the script executable (one-time setup)
chmod +x run.sh

# Display help
./run.sh help

# Build the project
./run.sh build

# Run the game
./run.sh run

# Run all tests
./run.sh test

# Run specific test categories
./run.sh test-model
./run.sh test-db
./run.sh test-ui

# Generate test coverage report
./run.sh coverage
```

The script handles Java version differences automatically and provides clear output for each operation.

#### Windows Users

For Windows users, a PowerShell script `run.ps1` is provided with the same functionality:

```powershell
# Display help
.\run.ps1 help

# Build the project
.\run.ps1 build

# Run the game
.\run.ps1 run

# Run all tests
.\run.ps1 test

# Run specific test categories
.\run.ps1 test-model
.\run.ps1 test-db
.\run.ps1 test-ui

# Generate test coverage report
.\run.ps1 coverage
```

Note: You may need to set the PowerShell execution policy to allow running scripts:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Writing New Tests

When adding new tests:

1. **Model Tests**: Focus on business logic and state management
   ```java
   @Test
   void testSnakeGrowth() {
       Snake snake = new Snake(10, 10);
       int initialLength = snake.getBody().size();
       snake.grow();
       assertEquals(initialLength + 1, snake.getBody().size());
   }
   ```

2. **Database Tests**: Use `@BeforeEach` to ensure a clean database state
   ```java
   @BeforeEach
   void setup() {
       // Clear database tables
       try (Connection conn = dbManager.getConnection()) {
           conn.createStatement().execute("DELETE FROM player_scores");
       }
   }
   ```

3. **UI Tests**: Create interfaces for JavaFX dependencies to enable effective mocking
   ```java
   // Instead of directly using JavaFX classes
   public interface SceneManager {
       void switchToGameScreen();
       void switchToHighScoreScreen();
   }
   ```

## 🏗️ Architecture

### Core Components

#### UI Layer
- `SnakeGameApp`: Main application class that manages screen transitions and application lifecycle
- `PlayerNameScreen`: Handles player name input and initial game setup
- `GameScreen`: Main game interface, rendering and user input handling
- `HighScoreScreen`: Displays and manages high score leaderboard

#### Game Logic Layer
- `Game`: Core game engine managing game state, rules, and updates
- `Snake`: Represents the snake entity, handling movement and growth
- `Food`: Manages food placement and collision detection
- `Point`: Data structure for 2D coordinates
- `Direction`: Enum for snake movement directions

#### Data Layer
- `DatabaseManager`: Handles database operations and connection pooling
- `Score`: Data model for player scores

### Class Interactions

```
SnakeGameApp
    ↓
    ├── PlayerNameScreen
    │       ↓
    │       └── GameScreen
    │           ↓
    │           ├── Game
    │           │   ├── Snake
    │           │   │   └── Point
    │           │   └── Food
    │           │       └── Point
    │           │
    │           └── DatabaseManager
    │               └── Score
    └── HighScoreScreen
            ↓
            └── DatabaseManager
```

### Key Design Patterns
1. **MVC (Model-View-Controller)**
   - Model: `Game`, `Snake`, `Food`, `Score`
   - View: `GameScreen`, `PlayerNameScreen`, `HighScoreScreen`
   - Controller: `SnakeGameApp` and screen-specific logic

2. **Singleton**
   - `DatabaseManager`: Ensures single database connection pool

3. **Observer**
   - Game state changes trigger UI updates
   - Score changes update the display

### Data Flow
1. **Game Initialization**
   ```
   SnakeGameApp → PlayerNameScreen → GameScreen → Game.initialize()
   ```

2. **Game Loop**
   ```
   GameScreen (AnimationTimer)
   ↓
   Game.update()
   ↓
   Snake.move()
   ↓
   Collision Detection
   ↓
   UI Update
   ```

3. **Score Saving**
   ```
   Game (game over)
   ↓
   DatabaseManager.saveScore()
   ↓
   HighScoreScreen.refresh()
   ```

### Technical Details
- **JavaFX**: UI framework for modern, responsive interface
- **PostgreSQL**: Persistent storage for high scores
- **HikariCP**: Connection pooling for database efficiency
- **Maven**: Build and dependency management

### Extension Points
1. **Game Features**
   - Add new game modes in `Game` class
   - Implement power-ups through `Food` class extensions
   - Add difficulty levels via `Game` configuration

2. **UI Enhancements**
   - Create new screens by extending existing UI classes
   - Customize game appearance through CSS
   - Add animations using JavaFX animation APIs

3. **Data Management**
   - Implement alternative storage backends
   - Add player profiles and statistics
   - Create multiplayer functionality 