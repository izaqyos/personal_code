#!/bin/bash

# Colors for better output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==============================${NC}"
echo -e "${BLUE}   toyMCP Test Runner        ${NC}"
echo -e "${BLUE}==============================${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo -e "${RED}Error: Docker is not running.${NC}"
  echo -e "${YELLOW}Please start Docker first.${NC}"
  exit 1
fi

# Start the database if it's not running
if ! docker ps | grep -q "toymcp_db"; then
  echo -e "${YELLOW}Database container not running. Starting it now...${NC}"
  docker compose up -d db
  
  # Give some time for the database to initialize
  echo -e "${BLUE}Waiting for database to initialize...${NC}"
  sleep 5
fi

# Default to running all tests
TEST_PATH=""

# Process arguments
if [ "$1" == "unit" ]; then
  TEST_PATH="--testPathPattern=unit_tests"
  echo -e "${BLUE}Running unit tests only${NC}"
elif [ "$1" == "integration" ]; then
  TEST_PATH="--testPathPattern=integration_tests"
  echo -e "${BLUE}Running integration tests only${NC}"
  echo -e "${YELLOW}Note: Integration tests require a running database${NC}"
else
  echo -e "${BLUE}Running all tests${NC}"
fi

# Run the tests
echo -e "${BLUE}Starting tests...${NC}"
npm test -- $TEST_PATH

# Check result
if [ $? -eq 0 ]; then
  echo -e "${GREEN}✓ Tests passed successfully!${NC}"
else
  echo -e "${RED}✗ Tests failed.${NC}"
  echo -e "${YELLOW}See test output above for details.${NC}"
  echo -e "${YELLOW}For help fixing common test failures, see TESTING.md${NC}"
fi 