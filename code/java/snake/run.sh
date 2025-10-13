#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Maven is installed
if ! command -v mvn &> /dev/null; then
    echo -e "${RED}Maven is not installed. Please install Maven first.${NC}"
    exit 1
fi

# Print header
print_header() {
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}           Snake Game 🐍            ${NC}"
    echo -e "${BLUE}======================================${NC}"
}

# Print usage
print_usage() {
    echo -e "${YELLOW}Usage:${NC}"
    echo -e "  ${GREEN}./run.sh${NC} [option]"
    echo
    echo -e "${YELLOW}Options:${NC}"
    echo -e "  ${GREEN}build${NC}        - Build the project"
    echo -e "  ${GREEN}run${NC}          - Run the Snake game"
    echo -e "  ${GREEN}test${NC}         - Run all tests with appropriate settings for Java 23"
    echo -e "  ${GREEN}test-model${NC}   - Run only model tests"
    echo -e "  ${GREEN}test-db${NC}      - Run only database tests"
    echo -e "  ${GREEN}test-ui${NC}      - Run only UI tests"
    echo -e "  ${GREEN}coverage${NC}     - Generate test coverage report"
    echo -e "  ${GREEN}help${NC}         - Display this help message"
    echo
}

# Build the project
build_project() {
    echo -e "${BLUE}Building the project...${NC}"
    mvn clean package -DskipTests
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Build successful!${NC}"
    else
        echo -e "${RED}Build failed!${NC}"
        exit 1
    fi
}

# Run the game
run_game() {
    echo -e "${BLUE}Running the Snake game...${NC}"
    mvn javafx:run
}

# Run all tests
run_all_tests() {
    echo -e "${BLUE}Running model tests...${NC}"
    mvn test -P model-tests
    
    echo -e "${BLUE}Running database tests...${NC}"
    mvn test -P db-tests
    
    echo -e "${BLUE}Running UI tests (may be skipped on Java 23+)...${NC}"
    mvn test -P ui-tests
    
    echo -e "${GREEN}All tests completed!${NC}"
}

# Run model tests
run_model_tests() {
    echo -e "${BLUE}Running model tests...${NC}"
    mvn test -P model-tests
}

# Run database tests
run_db_tests() {
    echo -e "${BLUE}Running database tests...${NC}"
    mvn test -P db-tests
}

# Run UI tests
run_ui_tests() {
    echo -e "${BLUE}Running UI tests (may be skipped on Java 23+)...${NC}"
    mvn test -P ui-tests
}

# Generate coverage report
generate_coverage() {
    echo -e "${BLUE}Generating test coverage report...${NC}"
    
    # Check Java version
    java_version=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}' | cut -d'.' -f1)
    
    if [ "$java_version" -ge 23 ]; then
        echo -e "${YELLOW}Warning: JaCoCo may have issues with Java 23+. Using model tests only.${NC}"
        mvn clean test -Dtest="*Point*Test,*Snake*Test,*Game*Test,*Food*Test"
    else
        mvn clean test
    fi
    
    echo -e "${GREEN}Coverage report generated in target/site/jacoco/index.html${NC}"
    
    # Open the report if possible
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open target/site/jacoco/index.html
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open target/site/jacoco/index.html 2>/dev/null
    elif [[ "$OSTYPE" == "msys" ]]; then
        start target/site/jacoco/index.html
    fi
}

# Main function
main() {
    print_header
    
    if [ $# -eq 0 ]; then
        print_usage
        exit 0
    fi
    
    case "$1" in
        build)
            build_project
            ;;
        run)
            run_game
            ;;
        test)
            run_all_tests
            ;;
        test-model)
            run_model_tests
            ;;
        test-db)
            run_db_tests
            ;;
        test-ui)
            run_ui_tests
            ;;
        coverage)
            generate_coverage
            ;;
        help)
            print_usage
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            print_usage
            exit 1
            ;;
    esac
}

# Execute main function
main "$@" 