# Snake Game Runner for Windows
# This script provides a simplified interface for building, running, and testing the Snake Game

# Check if Maven is installed
try {
    $mvnVersion = mvn --version
} catch {
    Write-Host "Maven is not installed. Please install Maven first." -ForegroundColor Red
    exit 1
}

# Print header
function Print-Header {
    Write-Host "======================================" -ForegroundColor Blue
    Write-Host "           Snake Game 🐍            " -ForegroundColor Blue
    Write-Host "======================================" -ForegroundColor Blue
}

# Print usage
function Print-Usage {
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 [option]" -ForegroundColor Green
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  build        - Build the project" -ForegroundColor Green
    Write-Host "  run          - Run the Snake game" -ForegroundColor Green
    Write-Host "  test         - Run all tests with appropriate settings for Java 23" -ForegroundColor Green
    Write-Host "  test-model   - Run only model tests" -ForegroundColor Green
    Write-Host "  test-db      - Run only database tests" -ForegroundColor Green
    Write-Host "  test-ui      - Run only UI tests" -ForegroundColor Green
    Write-Host "  coverage     - Generate test coverage report" -ForegroundColor Green
    Write-Host "  help         - Display this help message" -ForegroundColor Green
    Write-Host ""
}

# Build the project
function Build-Project {
    Write-Host "Building the project..." -ForegroundColor Blue
    mvn clean package -DskipTests
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Build successful!" -ForegroundColor Green
    } else {
        Write-Host "Build failed!" -ForegroundColor Red
        exit 1
    }
}

# Run the game
function Run-Game {
    Write-Host "Running the Snake game..." -ForegroundColor Blue
    mvn javafx:run
}

# Run all tests
function Run-AllTests {
    Write-Host "Running model tests..." -ForegroundColor Blue
    mvn test -P model-tests
    
    Write-Host "Running database tests..." -ForegroundColor Blue
    mvn test -P db-tests
    
    Write-Host "Running UI tests (may be skipped on Java 23+)..." -ForegroundColor Blue
    mvn test -P ui-tests
    
    Write-Host "All tests completed!" -ForegroundColor Green
}

# Run model tests
function Run-ModelTests {
    Write-Host "Running model tests..." -ForegroundColor Blue
    mvn test -P model-tests
}

# Run database tests
function Run-DatabaseTests {
    Write-Host "Running database tests..." -ForegroundColor Blue
    mvn test -P db-tests
}

# Run UI tests
function Run-UITests {
    Write-Host "Running UI tests (may be skipped on Java 23+)..." -ForegroundColor Blue
    mvn test -P ui-tests
}

# Generate coverage report
function Generate-Coverage {
    Write-Host "Generating test coverage report..." -ForegroundColor Blue
    
    # Check Java version
    $javaVersionOutput = java -version 2>&1
    $javaVersionString = $javaVersionOutput | Select-String -Pattern '\"(\d+)' | ForEach-Object { $_.Matches.Groups[1].Value }
    $javaVersion = [int]$javaVersionString
    
    if ($javaVersion -ge 23) {
        Write-Host "Warning: JaCoCo may have issues with Java 23+. Using model tests only." -ForegroundColor Yellow
        mvn clean test -Dtest="*Point*Test,*Snake*Test,*Game*Test,*Food*Test"
    } else {
        mvn clean test
    }
    
    Write-Host "Coverage report generated in target/site/jacoco/index.html" -ForegroundColor Green
    
    # Open the report
    Start-Process "target/site/jacoco/index.html"
}

# Main function
function Main {
    param (
        [string]$Option
    )
    
    Print-Header
    
    if ([string]::IsNullOrEmpty($Option)) {
        Print-Usage
        return
    }
    
    switch ($Option) {
        "build" { Build-Project }
        "run" { Run-Game }
        "test" { Run-AllTests }
        "test-model" { Run-ModelTests }
        "test-db" { Run-DatabaseTests }
        "test-ui" { Run-UITests }
        "coverage" { Generate-Coverage }
        "help" { Print-Usage }
        default {
            Write-Host "Unknown option: $Option" -ForegroundColor Red
            Print-Usage
            exit 1
        }
    }
}

# Execute main function with provided arguments
Main $args[0] 