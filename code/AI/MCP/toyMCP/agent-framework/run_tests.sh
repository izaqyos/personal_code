#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Get current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

# Set log file path
LOG_FILE="$DIR/agent_tests.log"
echo "Test log will be saved to: $LOG_FILE"

# Function to log messages to both console and log file
log() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

# Original script starts here
log "${BLUE}$(date)${NC}"
log "${BLUE}========================================${NC}"
log "${BLUE}= Agent Framework Test Runner         =${NC}"
log "${BLUE}========================================${NC}"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    log "${RED}Error: npm is not installed${NC}"
    exit 1
fi

# Function to run tests
run_tests() {
    log "${BLUE}Running $1 tests...${NC}"
    npm test -- --config=jest.config.js --testPathPattern=$1 $2 2>&1 | tee -a "$LOG_FILE"
    
    TEST_EXIT=${PIPESTATUS[0]}
    if [ $TEST_EXIT -eq 0 ]; then
        log "${GREEN}$1 tests completed successfully.${NC}"
        return 0
    else
        log "${RED}$1 tests failed.${NC}"
        return 1
    fi
}

# Check if .env file exists, create from template if not
if [ ! -f ".env" ]; then
    log "${YELLOW}Warning: .env file not found. Creating from .env-example${NC}"
    if [ -f ".env-example" ]; then
        cp .env-example .env
        log "${YELLOW}Please update .env with your actual credentials.${NC}"
    else
        log "${RED}Error: .env-example file not found${NC}"
        exit 1
    fi
fi

# Build TypeScript first
log "${BLUE}Building TypeScript code...${NC}"
npm run build 2>&1 | tee -a "$LOG_FILE"

BUILD_EXIT=${PIPESTATUS[0]}
if [ $BUILD_EXIT -ne 0 ]; then
    log "${RED}Build failed. Cannot run tests.${NC}"
    exit 1
fi

# Default to running all tests if no arguments are provided
if [ $# -eq 0 ]; then
    log "${BLUE}Running all tests...${NC}"
    npm test -- --config=jest.config.js 2>&1 | tee -a "$LOG_FILE"
    TEST_EXIT=${PIPESTATUS[0]}
    
    log "${BLUE}========================================${NC}"
    log "${BLUE}= Agent Framework Test Run Complete    =${NC}"
    if [ $TEST_EXIT -eq 0 ]; then
        log "${GREEN}= All tests passed!               =${NC}"
    else
        log "${RED}= Some tests failed.               =${NC}"
    fi
    log "${BLUE}= Exit Code: $TEST_EXIT               =${NC}"
    log "${BLUE}========================================${NC}"
    exit $TEST_EXIT
fi

# Process arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --unit)
            run_tests "unit"
            UNIT_EXIT=$?
            shift
            ;;
        --integration)
            log "${YELLOW}Note: Integration tests require a running MCP server${NC}"
            run_tests "integration" "--env RUN_INTEGRATION_TESTS=true"
            INTEGRATION_EXIT=$?
            shift
            ;;
        --coverage)
            log "${BLUE}Generating test coverage report...${NC}"
            npm test -- --config=jest.config.js --coverage 2>&1 | tee -a "$LOG_FILE"
            COVERAGE_EXIT=${PIPESTATUS[0]}
            if [ $COVERAGE_EXIT -eq 0 ]; then
                log "${GREEN}Coverage report generated successfully.${NC}"
                log "${BLUE}Open 'coverage/lcov-report/index.html' in your browser to view the report.${NC}"
            else
                log "${RED}Failed to generate coverage report.${NC}"
                exit 1
            fi
            shift
            ;;
        *)
            log "${YELLOW}Unknown option: $1${NC}"
            log "Usage: $0 [--unit] [--integration] [--coverage]"
            exit 1
            ;;
    esac
done

# Determine exit code based on which tests were run
log "${BLUE}========================================${NC}"
log "${BLUE}= Agent Framework Test Run Complete    =${NC}"

if [ -n "$UNIT_EXIT" ] && [ -n "$INTEGRATION_EXIT" ]; then
    # Both tests were run
    if [ $UNIT_EXIT -eq 0 ] && [ $INTEGRATION_EXIT -eq 0 ]; then
        log "${GREEN}= All tests passed!               =${NC}"
        FINAL_EXIT=0
    else
        log "${RED}= Some tests failed.               =${NC}"
        FINAL_EXIT=1
    fi
elif [ -n "$UNIT_EXIT" ]; then
    # Only unit tests were run
    if [ $UNIT_EXIT -eq 0 ]; then
        log "${GREEN}= Unit tests passed!              =${NC}"
    else
        log "${RED}= Unit tests failed.              =${NC}"
    fi
    FINAL_EXIT=$UNIT_EXIT
elif [ -n "$INTEGRATION_EXIT" ]; then
    # Only integration tests were run
    if [ $INTEGRATION_EXIT -eq 0 ]; then
        log "${GREEN}= Integration tests passed!       =${NC}"
    else
        log "${RED}= Integration tests failed.       =${NC}"
    fi
    FINAL_EXIT=$INTEGRATION_EXIT
fi

log "${BLUE}= Exit Code: $FINAL_EXIT               =${NC}"
log "${BLUE}========================================${NC}"
exit $FINAL_EXIT 