#!/bin/bash

# Test script for rust_cleaner.sh
# Comprehensive test suite covering all functionality and edge cases

# --- Configuration ---
SCRIPT_DIR=$(dirname "$0")
RUST_CLEANER_SCRIPT="${SCRIPT_DIR}/rust_cleaner.sh"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Colors for test output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Test Infrastructure ---
print_test_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

print_test_result() {
    local test_name="$1"
    local result="$2"
    TESTS_RUN=$((TESTS_RUN + 1))
    
    if [[ "$result" == "PASS" ]]; then
        echo -e "${GREEN}✓ PASS${NC}: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: $test_name"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_exit_code="${3:-0}"
    
    echo -e "\n${YELLOW}Running:${NC} $test_name"
    
    # Capture output and exit code
    local output
    local exit_code
    output=$(eval "$test_command" 2>&1)
    exit_code=$?
    
    if [[ $exit_code -eq $expected_exit_code ]]; then
        print_test_result "$test_name" "PASS"
        return 0
    else
        print_test_result "$test_name" "FAIL"
        echo "  Expected exit code: $expected_exit_code, Got: $exit_code"
        echo "  Output: $output"
        return 1
    fi
}

# Check if the rust cleaner script exists and is executable
if [ ! -x "$RUST_CLEANER_SCRIPT" ]; then
    echo -e "${RED}Error:${NC} Rust cleaner script '$RUST_CLEANER_SCRIPT' not found or not executable."
    echo "Please ensure it's in the same directory and has execute permissions."
    exit 1
fi

# Create temporary directories for testing
TEST_BASE_DIR=$(mktemp -d -t rust_cleaner_test_XXXXXX)
TEST_PROJECTS_DIR="$TEST_BASE_DIR/projects"
TEST_WORKSPACE_DIR="$TEST_BASE_DIR/workspace"
TEST_EMPTY_DIR="$TEST_BASE_DIR/empty"
TEST_INVALID_DIR="$TEST_BASE_DIR/nonexistent"

# --- Cleanup Function ---
cleanup() {
    echo -e "\n${YELLOW}Cleaning up temporary directories...${NC}"
    rm -rf "$TEST_BASE_DIR"
    echo "Cleanup complete."
}
trap cleanup EXIT

# --- Setup Test Environment ---
setup_test_environment() {
    print_test_header "Setting up test environment"
    
    mkdir -p "$TEST_PROJECTS_DIR"
    mkdir -p "$TEST_WORKSPACE_DIR"
    mkdir -p "$TEST_EMPTY_DIR"
    
    # Create a simple Cargo project
    local simple_project="$TEST_PROJECTS_DIR/simple_project"
    mkdir -p "$simple_project/src"
    cat > "$simple_project/Cargo.toml" << 'EOF'
[package]
name = "simple_project"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF
    echo 'fn main() { println!("Hello, world!"); }' > "$simple_project/src/main.rs"
    mkdir -p "$simple_project/target"
    echo "dummy build artifact" > "$simple_project/target/dummy_file"
    
    # Create a workspace with members
    local workspace_root="$TEST_WORKSPACE_DIR/my_workspace"
    mkdir -p "$workspace_root"
    cat > "$workspace_root/Cargo.toml" << 'EOF'
[workspace]
members = ["member1", "member2"]
resolver = "2"
EOF
    
    # Create workspace member 1
    local member1="$workspace_root/member1"
    mkdir -p "$member1/src"
    cat > "$member1/Cargo.toml" << 'EOF'
[package]
name = "member1"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF
    echo 'fn main() { println!("Member 1"); }' > "$member1/src/main.rs"
    mkdir -p "$member1/target"
    echo "member1 build artifact" > "$member1/target/dummy_file"
    
    # Create workspace member 2
    local member2="$workspace_root/member2"
    mkdir -p "$member2/src"
    cat > "$member2/Cargo.toml" << 'EOF'
[package]
name = "member2"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF
    echo 'fn main() { println!("Member 2"); }' > "$member2/src/main.rs"
    mkdir -p "$member2/target"
    echo "member2 build artifact" > "$member2/target/dummy_file"
    
    # Create a project with invalid Cargo.toml
    local invalid_project="$TEST_PROJECTS_DIR/invalid_project"
    mkdir -p "$invalid_project/src"
    echo "This is not a valid TOML file [[[" > "$invalid_project/Cargo.toml"
    echo 'fn main() { println!("Invalid project"); }' > "$invalid_project/src/main.rs"
    mkdir -p "$invalid_project/target"
    echo "invalid project build artifact" > "$invalid_project/target/dummy_file"
    
    # Create a project with no target directory
    local no_target_project="$TEST_PROJECTS_DIR/no_target_project"
    mkdir -p "$no_target_project/src"
    cat > "$no_target_project/Cargo.toml" << 'EOF'
[package]
name = "no_target_project"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF
    echo 'fn main() { println!("No target project"); }' > "$no_target_project/src/main.rs"
    
    # Create a nested project structure
    local nested_project="$TEST_PROJECTS_DIR/parent/nested_project"
    mkdir -p "$nested_project/src"
    cat > "$nested_project/Cargo.toml" << 'EOF'
[package]
name = "nested_project"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF
    echo 'fn main() { println!("Nested project"); }' > "$nested_project/src/main.rs"
    mkdir -p "$nested_project/target"
    echo "nested project build artifact" > "$nested_project/target/dummy_file"
    
    # Create a directory that looks like a project but isn't
    local fake_project="$TEST_PROJECTS_DIR/fake_project"
    mkdir -p "$fake_project/src"
    echo "This is not a Cargo.toml file" > "$fake_project/Cargo.txt"
    echo 'fn main() { println!("Fake project"); }' > "$fake_project/src/main.rs"
    
    echo -e "${GREEN}Test environment setup complete${NC}"
}

# --- Test Cases ---

test_input_validation() {
    print_test_header "Input Validation Tests"
    
    # Test 1: No arguments
    run_test "No arguments provided" \
        "'$RUST_CLEANER_SCRIPT'" \
        1
    
    # Test 2: Empty string argument
    run_test "Empty string argument" \
        "'$RUST_CLEANER_SCRIPT' ''" \
        1
    
    # Test 3: Non-existent directory
    run_test "Non-existent directory" \
        "'$RUST_CLEANER_SCRIPT' '$TEST_INVALID_DIR'" \
        1
    
    # Test 4: File instead of directory
    local test_file="$TEST_BASE_DIR/test_file.txt"
    echo "test content" > "$test_file"
    run_test "File instead of directory" \
        "'$RUST_CLEANER_SCRIPT' '$test_file'" \
        1
}

test_cargo_availability() {
    print_test_header "Cargo Availability Tests"
    
    # Test with cargo available (should pass if cargo is installed)
    run_test "Cargo available - empty directory" \
        "'$RUST_CLEANER_SCRIPT' '$TEST_EMPTY_DIR'" \
        0
}

test_project_detection() {
    print_test_header "Project Detection Tests"
    
    # Test 1: Directory with no Cargo projects
    run_test "Empty directory scan" \
        "'$RUST_CLEANER_SCRIPT' '$TEST_EMPTY_DIR'" \
        0
    
    # Test 2: Directory with valid projects
    run_test "Valid projects scan" \
        "'$RUST_CLEANER_SCRIPT' '$TEST_PROJECTS_DIR'" \
        0
    
    # Test 3: Nested project detection
    run_test "Nested project detection" \
        "'$RUST_CLEANER_SCRIPT' '$TEST_PROJECTS_DIR/parent'" \
        0
}

test_workspace_handling() {
    print_test_header "Workspace Handling Tests"
    
    # Test workspace detection and member skipping
    run_test "Workspace with members" \
        "'$RUST_CLEANER_SCRIPT' '$TEST_WORKSPACE_DIR'" \
        0
}

test_cleaning_functionality() {
    print_test_header "Cleaning Functionality Tests"
    
    # Test cleaning valid projects
    run_test "Clean valid projects" \
        "'$RUST_CLEANER_SCRIPT' '$TEST_PROJECTS_DIR'" \
        0
    
    # Test cleaning projects with invalid Cargo.toml
    run_test "Clean projects with invalid Cargo.toml" \
        "'$RUST_CLEANER_SCRIPT' '$TEST_PROJECTS_DIR/invalid_project'" \
        1
}

test_edge_cases() {
    print_test_header "Edge Case Tests"
    
    # Test 1: Relative path handling
    local current_dir=$(pwd)
    local absolute_script=$(realpath "$RUST_CLEANER_SCRIPT")
    cd "$TEST_BASE_DIR"
    run_test "Relative path handling" \
        "'$absolute_script' './projects'" \
        0
    cd "$current_dir"
    
    # Test 2: Path with spaces
    local space_dir="$TEST_BASE_DIR/dir with spaces"
    mkdir -p "$space_dir"
    run_test "Path with spaces" \
        "'$RUST_CLEANER_SCRIPT' '$space_dir'" \
        0
    
    # Test 3: Symlink handling
    local symlink_dir="$TEST_BASE_DIR/symlink_test"
    mkdir -p "$symlink_dir"
    ln -s "$TEST_PROJECTS_DIR/simple_project" "$symlink_dir/symlink_project"
    run_test "Symlink handling" \
        "'$RUST_CLEANER_SCRIPT' '$symlink_dir'" \
        0
    
    # Test 4: Very deep directory structure
    local deep_dir="$TEST_BASE_DIR/a/b/c/d/e/f/g/h/i/j"
    mkdir -p "$deep_dir"
    run_test "Deep directory structure" \
        "'$RUST_CLEANER_SCRIPT' '$deep_dir'" \
        0
}

test_output_functions() {
    print_test_header "Output Function Tests"
    
    # Test that output contains expected sections
    local output
    output=$("$RUST_CLEANER_SCRIPT" "$TEST_PROJECTS_DIR" 2>&1)
    
    if echo "$output" | grep -q "CLEANUP REPORT"; then
        print_test_result "Output contains cleanup report" "PASS"
    else
        print_test_result "Output contains cleanup report" "FAIL"
    fi
    
    if echo "$output" | grep -q "Total Cargo projects found"; then
        print_test_result "Output contains project count" "PASS"
    else
        print_test_result "Output contains project count" "FAIL"
    fi
    
    if echo "$output" | grep -q "Successfully cleaned"; then
        print_test_result "Output contains success count" "PASS"
    else
        print_test_result "Output contains success count" "FAIL"
    fi
}

test_concurrent_access() {
    print_test_header "Concurrent Access Tests"
    
    # Test running multiple instances simultaneously
    local pid1 pid2
    "$RUST_CLEANER_SCRIPT" "$TEST_PROJECTS_DIR" >/dev/null 2>&1 &
    pid1=$!
    "$RUST_CLEANER_SCRIPT" "$TEST_PROJECTS_DIR" >/dev/null 2>&1 &
    pid2=$!
    
    wait $pid1
    local exit1=$?
    wait $pid2
    local exit2=$?
    
    if [[ $exit1 -eq 0 && $exit2 -eq 0 ]]; then
        print_test_result "Concurrent execution" "PASS"
    else
        print_test_result "Concurrent execution" "FAIL"
    fi
}

test_performance() {
    print_test_header "Performance Tests"
    
    # Create a larger test structure
    local perf_dir="$TEST_BASE_DIR/performance_test"
    mkdir -p "$perf_dir"
    
    # Create 50 small projects
    for i in {1..50}; do
        local project_dir="$perf_dir/project_$i"
        mkdir -p "$project_dir/src"
        cat > "$project_dir/Cargo.toml" << EOF
[package]
name = "project_$i"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF
        echo "fn main() { println!(\"Project $i\"); }" > "$project_dir/src/main.rs"
        mkdir -p "$project_dir/target"
        echo "build artifact $i" > "$project_dir/target/dummy_file"
    done
    
    # Time the execution
    local start_time=$(date +%s)
    "$RUST_CLEANER_SCRIPT" "$perf_dir" >/dev/null 2>&1
    local exit_code=$?
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    if [[ $exit_code -eq 0 && $duration -lt 30 ]]; then
        print_test_result "Performance test (50 projects in <30s)" "PASS"
    else
        print_test_result "Performance test (50 projects in <30s)" "FAIL"
        echo "  Duration: ${duration}s, Exit code: $exit_code"
    fi
}

# --- Main Test Execution ---
main() {
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}    Rust Cleaner Test Suite${NC}"
    echo -e "${BLUE}======================================${NC}"
    
    # Setup
    setup_test_environment
    
    # Run all test suites
    test_input_validation
    test_cargo_availability
    test_project_detection
    test_workspace_handling
    test_cleaning_functionality
    test_edge_cases
    test_output_functions
    test_concurrent_access
    test_performance
    
    # Final Report
    echo -e "\n${BLUE}======================================${NC}"
    echo -e "${BLUE}           TEST RESULTS${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo -e "Total tests run: ${TESTS_RUN}"
    echo -e "${GREEN}Tests passed: ${TESTS_PASSED}${NC}"
    echo -e "${RED}Tests failed: ${TESTS_FAILED}${NC}"
    
    if [[ $TESTS_FAILED -eq 0 ]]; then
        echo -e "\n${GREEN}🎉 ALL TESTS PASSED! 100% success rate${NC}"
        exit 0
    else
        echo -e "\n${RED}❌ Some tests failed${NC}"
        local success_rate=$((TESTS_PASSED * 100 / TESTS_RUN))
        echo -e "Success rate: ${success_rate}%"
        exit 1
    fi
}

# Run the main function
main "$@"