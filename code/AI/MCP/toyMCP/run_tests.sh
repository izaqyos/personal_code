#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==============================${NC}"
echo -e "${BLUE}   toyMCP Test Runner        ${NC}"
echo -e "${BLUE}==============================${NC}"

# Ensure the database container is running
echo -e "${BLUE}Ensuring database container is running...${NC}"
docker compose up -d db

# Wait a moment for the database to initialize if it just started
echo -e "${BLUE}Waiting for database to initialize...${NC}"
sleep 5

# Check environment
node scripts/check_test_env.js
if [ $? -ne 0 ]; then
  echo -e "${RED}Environment check failed. Please address the issues above.${NC}"
  exit 1
fi

# Run tests with proper arguments
if [ "$1" == "unit" ]; then
  echo -e "${BLUE}Running unit tests...${NC}"
  npm test -- --testPathPattern=unit_tests
elif [ "$1" == "integration" ]; then
  echo -e "${BLUE}Running integration tests...${NC}"
  npm test -- --testPathPattern=integration_tests
else
  echo -e "${BLUE}Running all tests...${NC}"
  npm test
fi

# Check the test result
if [ $? -eq 0 ]; then
  echo -e "${GREEN}✓ All tests passed!${NC}"
else
  echo -e "${RED}✗ Some tests failed.${NC}"
  echo -e "${YELLOW}===========================================${NC}"
  echo -e "${YELLOW}Common test failures and how to fix them:${NC}"
  echo -e "${YELLOW}===========================================${NC}"
  echo -e "${YELLOW}1. Database connection issues:${NC}"
  echo -e "   - Make sure Docker is running"
  echo -e "   - Start the database with: docker compose up -d db"
  echo -e "${YELLOW}2. Authentication token issues:${NC}"
  echo -e "   - Check test user credentials"
  echo -e "${YELLOW}3. SQL statement mismatches:${NC}"
  echo -e "   - Update tests if schema has changed"
  echo -e "${YELLOW}4. Error handling test failures:${NC}"
  echo -e "   - May need to bypass authentication for error tests"
  echo -e "${YELLOW}===========================================${NC}"
fi 