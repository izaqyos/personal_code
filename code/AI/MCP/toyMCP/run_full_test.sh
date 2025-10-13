#!/bin/bash

# This script orchestrates a full test run:
# 1. Cleans and starts the database.
# 2. Starts the server in the background.
# 3. Runs the test_server.sh script (containing curl tests).
# 4. Runs the agent framework tests.
# 5. Stops the server.
# 6. Optionally stops the database.

echo "### Orchestrator: Starting Full Test Run ###"

# 1. Clean and Start Database
echo "--- Performing Clean Docker Stop and Volume Removal ---"
docker compose down -v
if [ $? -ne 0 ]; then
  echo "ERROR: 'docker compose down -v' failed. Aborting."
  exit 1
fi

echo "--- Starting Fresh Database Container ---"
docker compose up -d db
if [ $? -ne 0 ]; then
  echo "ERROR: 'docker compose up -d db' failed. Aborting."
  exit 1
fi

# 2. Wait for DB
echo "--- Waiting 7 seconds for DB to initialize... ---"
sleep 7 # Increased wait time slightly for robustness

# 3. Start Server in Background
echo "--- Starting Node.js Server in background ---"
npm start & # Run npm start in the background
SERVER_PID=$! # Get the Process ID of the background npm start
echo "Server started in background with PID: $SERVER_PID"

# Trap EXIT signal to ensure server is killed even if script is interrupted
trap "echo '>>> Stopping background server (PID $SERVER_PID)...'; kill $SERVER_PID 2>/dev/null; wait $SERVER_PID 2>/dev/null; echo '>>> Server stopped.'; exit" EXIT SIGHUP SIGINT SIGQUIT SIGTERM

# 4. Wait for Server
echo "--- Waiting 5 seconds for server to initialize... ---"
sleep 5

# Check if server process is still running before testing
if ! ps -p $SERVER_PID > /dev/null; then
   echo "ERROR: Server process $SERVER_PID died unexpectedly after startup. Check server logs."
   # Trap will handle cleanup, just exit
   exit 1
fi
echo "Server process $SERVER_PID seems to be running."

# 5. Run MCP API Tests
echo "--- Running test_server.sh ---"
bash ./test_server.sh # Execute the curl test script
SERVER_TEST_EXIT_CODE=$?
echo "--- test_server.sh finished with exit code: $SERVER_TEST_EXIT_CODE ---"

# 6. Run Agent Framework Tests
echo "--- Running Agent Framework Tests ---"
# Save current directory
CURRENT_DIR=$(pwd)
# Change to agent-framework directory
cd agent-framework || { echo "ERROR: agent-framework directory not found"; exit 1; }

# Run agent framework tests (assuming they're run with a script or npm command)
# Check if run_tests.sh exists, otherwise use npm test
if [ -f "run_tests.sh" ]; then
  # Make sure it's executable
  chmod +x run_tests.sh
  ./run_tests.sh
  AGENT_TEST_EXIT_CODE=$?
else
  echo "Using npm test for agent framework tests"
  npm test
  AGENT_TEST_EXIT_CODE=$?
fi

# Change back to original directory
cd "$CURRENT_DIR"
echo "--- Agent Framework Tests finished with exit code: $AGENT_TEST_EXIT_CODE ---"

# 7. Stop Background Server (handled by trap)

# 8. Optionally Stop Database (uncomment if desired)
# echo "--- Stopping database container ---"
# docker compose down

# 9. Determine overall test success
echo "### Test Results Summary ###"
echo "Server Tests Exit Code: $SERVER_TEST_EXIT_CODE"
echo "Agent Framework Tests Exit Code: $AGENT_TEST_EXIT_CODE"

if [ $SERVER_TEST_EXIT_CODE -eq 0 ] && [ $AGENT_TEST_EXIT_CODE -eq 0 ]; then
  echo "### Orchestrator: Full Test Run PASSED ###"
  exit 0
else
  echo "### Orchestrator: Full Test Run FAILED ###"
  # Exit with non-zero code if either test suite failed
  exit 1
fi 