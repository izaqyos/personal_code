#!/bin/bash

# Bash script to sequentially test the toyMCP To-Do Server using HTTPie
# Uses piped JSON, checks responses with jq, and reports results.
#
# IMPORTANT: This script assumes the database is in a clean state (empty todos table)
#            when it starts, so that the first added item gets ID 1 and the second ID 2.
#            If the DB contains previous data, the remove steps [4] and [5] will likely fail.
#            To ensure a clean state, run: `docker compose down -v && docker compose up -d db`
#            before starting the server (`npm start`) and running this script.
#
# Requires: httpie, jq
#
# Assumes the server is running on http://127.0.0.1:3000
# Run this script using: bash test_server.sh

# --- Configuration ---
# BASE_URL="http://127.0.0.1:3000/rpc" # Base for API calls
API_BASE_URL="http://127.0.0.1:3000" # Base for all server URLs
RPC_ENDPOINT="$API_BASE_URL/rpc"
AUTH_ENDPOINT="$API_BASE_URL/auth/login"
HEADERS="Content-Type:application/json"
AUTH_TOKEN=""
PASSED_COUNT=0
FAILED_COUNT=0
TOTAL_TESTS=0

# --- Login Function ---
# Logs in the default user and exports the token
login_user() {
    echo -e "\n--- [0] Attempting Login ---"
    local login_payload='{"username": "testuser", "password": "password123"}'
    local login_response

    login_response=$(curl -s -X POST -H "$HEADERS" -d "$login_payload" "$AUTH_ENDPOINT")
    local login_curl_code=$?

    if [ $login_curl_code -ne 0 ]; then
        echo "FAILED: Login request failed with exit code $login_curl_code"
        echo "Response: $login_response"
        exit 1 # Cannot proceed without login
    fi

    # Check if login response contains a token using jq
    AUTH_TOKEN=$(echo "$login_response" | jq -r '.token // empty') # Extract token or empty string

    if [ -z "$AUTH_TOKEN" ]; then
        echo "FAILED: Login failed. Could not extract token from response."
        echo "Response:"
        echo "$login_response" | jq '.'
        exit 1 # Cannot proceed without token
    else
        echo "SUCCESS: Login successful. Token obtained."
        # Optionally print token: echo "Token: $AUTH_TOKEN"
    fi
}

# --- Helper Function ---
# Runs a test case
# $1: Test number/ID (e.g., "[1]", "[E1]")
# $2: Test description
# $3: JSON payload to send (as a string)
# $4: jq expression to check for success (should evaluate to true on success) OR "expect_401" OR "expect_auth_failure"
# $5: Expected description (optional, for clarity in failure message)
run_test() {
    local test_id="$1"
    local description="$2"
    local payload="$3"
    local check_type="$4" # Renamed from jq_check for clarity
    local expected_desc="$5"
    local response
    local http_code # To store HTTP status code
    local auth_header
    local target_endpoint

    echo -e "\n--- $test_id $description ---"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    # Determine target endpoint and if auth header is needed
    if [[ "$test_id" == "[L1]" || "$test_id" == "[L2]" ]]; then
        target_endpoint=$AUTH_ENDPOINT
        # NO AUTH HEADER for login attempts
        response=$(curl -s -w "\\n%{http_code}" -X POST -H "$HEADERS" -d "$payload" "$target_endpoint")
    elif [[ "$test_id" == "[E8]" || "$test_id" == "[E9]" ]]; then
        target_endpoint=$RPC_ENDPOINT
        # NO AUTH HEADER for these specific unauthenticated tests
        response=$(echo "$payload" | curl -s -w "\\n%{http_code}" -X POST -H "$HEADERS" --data-binary @- "$target_endpoint")
    elif [[ "$test_id" == "[E6]" || "$test_id" == "[E7]" ]]; then
        # These error cases (invalid JSON, non-JSON-RPC) are sent to RPC endpoint without Auth
        # because the server should handle malformed requests irrespective of auth,
        # or they are testing specific parsing errors before auth logic.
        target_endpoint=$RPC_ENDPOINT
        response=$(echo "$payload" | curl -s -w "\\n%{http_code}" -X POST -H "$HEADERS" --data-binary @- "$target_endpoint")
    else
        # Default to RPC_ENDPOINT and use AUTH_TOKEN if available
        target_endpoint=$RPC_ENDPOINT
        if [ -n "$AUTH_TOKEN" ]; then
            auth_header="Authorization: Bearer $AUTH_TOKEN"
            response=$(echo "$payload" | curl -s -w "\\n%{http_code}" -X POST -H "$HEADERS" -H "$auth_header" --data-binary @- "$target_endpoint")
        else
            # This case should ideally not be hit for protected routes if AUTH_TOKEN is expected
            echo "WARNING: No AUTH_TOKEN for a test that might require it: $test_id"
            response=$(echo "$payload" | curl -s -w "\\n%{http_code}" -X POST -H "$HEADERS" --data-binary @- "$target_endpoint")
        fi
    fi
    local curl_exit_code=$?

    # Extract HTTP status code and response body
    http_code=$(echo "$response" | tail -n1)
    response_body=$(echo "$response" | sed '$d')


    if [ $curl_exit_code -ne 0 ]; then
        echo "FAILED: HTTP request failed with curl exit code $curl_exit_code"
        echo "Response Body:"
        echo "$response_body" # Show response body even on HTTP failure
        FAILED_COUNT=$((FAILED_COUNT + 1))
        return
    fi

    # Check based on check_type
    if [[ "$check_type" == "expect_401" ]]; then
        if [[ "$http_code" -eq 401 ]]; then
            echo "SUCCESS (Got HTTP 401 Unauthorized as expected)"
            echo "Response Body:"
            echo "$response_body" | jq '.' 2>/dev/null || echo "$response_body" # Pretty print if JSON, else raw
            PASSED_COUNT=$((PASSED_COUNT + 1))
        else
            echo "FAILED: Expected HTTP 401, got $http_code"
            echo "Response Body:"
            echo "$response_body" | jq '.' 2>/dev/null || echo "$response_body"
            FAILED_COUNT=$((FAILED_COUNT + 1))
        fi
        return
    elif [[ "$check_type" == "expect_auth_failure" ]]; then # For [L1] and [L2]
        if [[ "$http_code" -eq 401 ]]; then
            # Check if response_body contains the expected message
            echo "$response_body" | jq -e '.message | test("Incorrect username or password|Invalid credentials|Authentication failed"; "i")' > /dev/null 2>&1
            local jq_auth_check_exit_code=$?
            if [ $jq_auth_check_exit_code -eq 0 ]; then
                echo "SUCCESS (Got HTTP 401 and expected auth failure message)"
                echo "Response Body:"
                echo "$response_body" | jq '.'
                PASSED_COUNT=$((PASSED_COUNT + 1))
            else
                echo "FAILED: Got HTTP 401, but response body did not contain expected auth failure message."
                echo "Expected message like: 'Incorrect username or password' or 'Invalid credentials'"
                echo "Response Body:"
                echo "$response_body" | jq '.'
                FAILED_COUNT=$((FAILED_COUNT + 1))
            fi
        else
            echo "FAILED: Expected HTTP 401 for auth failure, got $http_code"
            echo "Response Body:"
            echo "$response_body" | jq '.' 2>/dev/null || echo "$response_body"
            FAILED_COUNT=$((FAILED_COUNT + 1))
        fi
        return
    fi

    # Standard jq check for JSON-RPC success (implies HTTP 200 for JSON-RPC)
    if [[ "$http_code" -ne 200 ]]; then
        echo "FAILED: Expected HTTP 200 for successful JSON-RPC, got $http_code"
        echo "Response Body:"
        echo "$response_body" | jq '.' 2>/dev/null || echo "$response_body"
        FAILED_COUNT=$((FAILED_COUNT + 1))
        return
    fi

    echo "$response_body" | jq -e "$check_type" > /dev/null 2>&1
    local jq_exit_code=$?

    if [ $jq_exit_code -eq 0 ]; then
        echo "SUCCESS"
        echo "Response Body:"
        echo "$response_body" | jq '.' # Pretty print JSON response on success
        PASSED_COUNT=$((PASSED_COUNT + 1))
    else
        echo "FAILED: Response JSON did not match expected criteria (HTTP 200)."
        if [ -n "$expected_desc" ]; then
            echo "       Expected JQ check: $check_type"
            echo "       Expected Description: $expected_desc"
        fi
        echo "Response Body:"
        echo "$response_body" | jq '.' # Pretty print JSON response on failure
        FAILED_COUNT=$((FAILED_COUNT + 1))
    fi
}

# --- Login Step ---
login_user # Call login function to get the token

# --- Test Execution ---

# [1] Add 'Learn HTTPie' (Now requires auth)
payload_1='{"jsonrpc": "2.0", "method": "todo.add", "params": {"text": "Learn HTTPie"}, "id": 1}'
check_1='.error == null and .result.text == "Learn HTTPie"'
run_test "[1]" "Add 'Learn HTTPie' (Requires Auth)" "$payload_1" "$check_1" "'result' with correct text, no 'error'"

# [2] Add 'Test the server'
payload_2='{"jsonrpc": "2.0", "method": "todo.add", "params": {"text": "Test the server"}, "id": 2}'
check_2='.error == null and .result.text == "Test the server"'
run_test "[2]" "Add 'Test the server' (Expected ID: 2 if DB is clean)" "$payload_2" "$check_2" "'result' with correct text, no 'error'"

# [3] List all items
payload_3='{"jsonrpc": "2.0", "method": "todo.list", "id": 3}'
check_3='.error == null and (.result | length) >= 2' # Check at least 2 items if clean, just check for result array
run_test "[3]" "List all items (Should show items just added)" "$payload_3" "$check_3" "'result' is an array, no 'error'"

# [4] Remove the first item
payload_4='{"jsonrpc": "2.0", "method": "todo.remove", "params": {"id": 1}, "id": 4}'
check_4='.error == null and .result.id == 1'
run_test "[4]" "Remove the first item (Assumes ID 1 - requires clean DB start)" "$payload_4" "$check_4" "'result' with ID 1, no 'error'"

# [5] Remove the second item
payload_5='{"jsonrpc": "2.0", "method": "todo.remove", "params": {"id": 2}, "id": 5}'
check_5='.error == null and .result.id == 2'
run_test "[5]" "Remove the second item (Assumes ID 2 - requires clean DB start)" "$payload_5" "$check_5" "'result' with ID 2, no 'error'"

# [6] List items again
payload_6='{"jsonrpc": "2.0", "method": "todo.list", "id": 6}'
check_6='.error == null and (.result | length) == 0' # Expect empty array if remove worked
run_test "[6]" "List items again (Should be empty if DB started clean)" "$payload_6" "$check_6" "'result' is an empty array, no 'error'"

# [7] Call mcp.discover (Now requires auth)
payload_7='{"jsonrpc": "2.0", "method": "mcp.discover", "id": 7}'
check_7='.error == null and .result.name == "ToyMCP Todo Service" and (.result.methods | map(.name) | contains(["todo.list", "todo.add", "todo.remove", "mcp.discover"]))'
run_test "[7]" "Call mcp.discover (Requires Auth)" "$payload_7" "$check_7" "'result' with service info and all methods listed"

echo -e "\n--- Error Cases ---"

# [E1] Add item with missing 'text' parameter (Requires Auth)
payload_e1='{"jsonrpc": "2.0", "method": "todo.add", "params": {}, "id": 101}'
check_e1='.error.code == -32602'
run_test "[E1]" "Add item with missing 'text' parameter (Requires Auth)" "$payload_e1" "$check_e1" "'error' with code -32602"

# [E2] Add item with invalid 'text' type
payload_e2='{"jsonrpc": "2.0", "method": "todo.add", "params": {"text": 123}, "id": 102}'
check_e2='.error.code == -32602'
run_test "[E2]" "Add item with invalid 'text' type" "$payload_e2" "$check_e2" "'error' with code -32602"

# [E3] Remove item with missing 'id' parameter
payload_e3='{"jsonrpc": "2.0", "method": "todo.remove", "params": {}, "id": 103}'
check_e3='.error.code == -32602'
run_test "[E3]" "Remove item with missing 'id' parameter" "$payload_e3" "$check_e3" "'error' with code -32602"

# [E4] Remove item with non-existent ID
payload_e4='{"jsonrpc": "2.0", "method": "todo.remove", "params": {"id": 99999}, "id": 104}'
check_e4='.error.code == 1001' # Custom Not Found code
run_test "[E4]" "Remove item with non-existent ID" "$payload_e4" "$check_e4" "'error' with code 1001"

# [E5] Call a non-existent method
payload_e5='{"jsonrpc": "2.0", "method": "invalid.method.name", "params": {}, "id": 105}'
check_e5='.error.code == -32601' # Method not found
run_test "[E5]" "Call a non-existent method" "$payload_e5" "$check_e5" "'error' with code -32601"

# [E6] Send invalid JSON (Should still work without auth as it's caught earlier)
payload_e6='{"jsonrpc": "2.0", "method": "foo", "params": "bar", "id": 1' # Missing closing brace
check_e6='.error.code == -32700'
run_test "[E6]" "Send invalid JSON (No Auth Needed)" "$payload_e6" "$check_e6" "'error' with code -32700"

# [E7] Send valid JSON but not a valid JSON-RPC request (Should still work without auth)
payload_e7='{"hello": "world", "foo": "bar"}'
run_test "[E7]" "Send valid JSON but not JSON-RPC (No Auth Needed)" "$payload_e7" "expect_401" "401 Unauthorized response"

# --- New Auth Test Cases ---
echo -e "\n--- Authentication Specific Tests ---"

# [L1] Failed login attempt (Wrong Password)
# This test now expects an HTTP 401 and a specific message from /auth/login
payload_l1='{"username": "testuser", "password": "wrongpassword"}'
run_test "[L1]" "Failed login (Wrong Password)" "$payload_l1" "expect_auth_failure" "HTTP 401 with auth failure message"

# [L2] Failed login attempt (Wrong Username)
# This test now expects an HTTP 401 and a specific message from /auth/login
payload_l2='{"username": "nonexistent", "password": "password123"}'
run_test "[L2]" "Failed login (Wrong Username)" "$payload_l2" "expect_auth_failure" "HTTP 401 with auth failure message"

# Clear token to test unauthenticated access
AUTH_TOKEN="" # This is correct for [E8] and [E9]

# [E8] Attempt mcp.discover without token
payload_e8='{"jsonrpc": "2.0", "method": "mcp.discover", "id": 108}'
run_test "[E8]" "Attempt mcp.discover (No Token)" "$payload_e8" "expect_401" "HTTP 401 Unauthorized response"

# [E9] Attempt todo.add without token
payload_e9='{"jsonrpc": "2.0", "method": "todo.add", "params": {"text": "No Auth"}, "id": 109}'
run_test "[E9]" "Attempt todo.add (No Token)" "$payload_e9" "expect_401" "HTTP 401 Unauthorized response"

# --- Final Report ---
echo -e "\n--- Testing Complete ---"
echo "=========================="
echo " TOTAL TESTS: $TOTAL_TESTS"
echo "      PASSED: $PASSED_COUNT"
echo "      FAILED: $FAILED_COUNT"
echo "=========================="

# Exit with non-zero status if any tests failed
if [ "$FAILED_COUNT" -ne 0 ]; then
    exit 1
fi

exit 0 