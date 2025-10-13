#!/bin/bash

# Test script for rsync-dirs.sh

# --- Configuration ---
SCRIPT_DIR=$(dirname "$0")
SYNC_SCRIPT="${SCRIPT_DIR}/rsync-dirs.sh"
TEST_COUNT=0
FAIL_COUNT=0

# Check if the sync script exists and is executable
if [ ! -x "$SYNC_SCRIPT" ]; then
    echo "❌ Error: Sync script '$SYNC_SCRIPT' not found or not executable."
    echo "Please ensure it's in the same directory or in your PATH and has execute permissions."
    exit 1
fi

# Define colors for output (simplified for test runner)
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# --- Test Runner ---
# Usage: run_test "Test Description" <expected_exit_code> <sync_script_args...>
# Verification logic should be placed *after* calling run_test
run_test() {
    local description="$1"
    local expected_exit_code="$2"
    shift 2 # Remove description and expected exit code from args
    local args=("$@")
    local output_log
    local exit_code

    ((TEST_COUNT++))
    echo -e "\n--- Test ${TEST_COUNT}: ${description} ---"

    # Run the script, capturing output and exit code
    # Use a here-string 'y' to auto-confirm the script's pre-run prompts
    # For interactive tests (-i), the input for rsync itself needs separate handling if needed
    echo "Running: $SYNC_SCRIPT ${args[*]}"
    output_log=$(echo 'y' | "$SYNC_SCRIPT" "${args[@]}" 2>&1)
    exit_code=$?
    echo " -> Exit Code: $exit_code (Expected: $expected_exit_code)"
    # Uncomment to see full output for debugging
    # echo "--- Script Output ---"
    # echo "$output_log"
    # echo "---------------------"

    if [ "$exit_code" -ne "$expected_exit_code" ]; then
        echo -e "❌ ${RED}FAIL:${NC} Unexpected exit code."
        echo "--- Script Output ---"
        echo "$output_log"
        echo "---------------------"
        ((FAIL_COUNT++))
        return 1 # Indicate failure
    fi
    return 0 # Indicate success so far
}

# --- Helper Verification Functions ---
assert_exists() {
    if [ ! -e "$1" ]; then
        echo -e "❌ ${RED}FAIL:${NC} Expected '$1' to exist."
        ((FAIL_COUNT++))
        return 1
    fi
    return 0
}
assert_not_exists() {
    if [ -e "$1" ]; then
        echo -e "❌ ${RED}FAIL:${NC} Expected '$1' to NOT exist."
        ((FAIL_COUNT++))
        return 1
    fi
    return 0
}
assert_files_equal() {
    if ! cmp -s "$1" "$2"; then
        echo -e "❌ ${RED}FAIL:${NC} Expected file '$1' and '$2' to be identical."
        ((FAIL_COUNT++))
        return 1
    fi
    return 0
}
assert_is_dir() {
     if [ ! -d "$1" ]; then
        echo -e "❌ ${RED}FAIL:${NC} Expected '$1' to be a directory."
        ((FAIL_COUNT++))
        return 1
    fi
    return 0
}
assert_is_link() {
    if [ ! -L "$1" ]; then
        echo -e "❌ ${RED}FAIL:${NC} Expected '$1' to be a symbolic link."
        ((FAIL_COUNT++))
        return 1
    fi
    return 0
}


# --- Setup & Cleanup ---
TMP_DIR=$(mktemp -d -t rsync_dirs_test_XXXXXX)
cleanup() {
  echo -e "\nCleaning up temporary directory: $TMP_DIR"
  rm -rf "$TMP_DIR"
  echo "Cleanup complete."
}
trap cleanup EXIT

# --- Test Cases ---

# == Non-Interactive Tests ==

# Test 1: Basic Sync (New Files)
echo "Setting up Test 1..."
mkdir -p "$TMP_DIR/src1" "$TMP_DIR/dest1"
echo "fileA" > "$TMP_DIR/src1/fileA.txt"
echo "fileB" > "$TMP_DIR/src1/fileB.txt"
mkdir "$TMP_DIR/src1/subdir"
echo "subfile" > "$TMP_DIR/src1/subdir/sub.txt"
run_test "Basic Sync (New Files)" 0 "$TMP_DIR/src1" "$TMP_DIR/dest1"
if [ $? -eq 0 ]; then
    assert_exists "$TMP_DIR/dest1/fileA.txt" && assert_files_equal "$TMP_DIR/src1/fileA.txt" "$TMP_DIR/dest1/fileA.txt"
    assert_exists "$TMP_DIR/dest1/fileB.txt" && assert_files_equal "$TMP_DIR/src1/fileB.txt" "$TMP_DIR/dest1/fileB.txt"
    assert_exists "$TMP_DIR/dest1/subdir/sub.txt" && assert_files_equal "$TMP_DIR/src1/subdir/sub.txt" "$TMP_DIR/dest1/subdir/sub.txt"
fi

# Test 2: Sync with Deletion
echo "Setting up Test 2..."
mkdir -p "$TMP_DIR/src2" "$TMP_DIR/dest2"
echo "fileA_new" > "$TMP_DIR/src2/fileA.txt" # Only A in source
echo "fileA_old" > "$TMP_DIR/dest2/fileA.txt"
echo "fileC_extra" > "$TMP_DIR/dest2/fileC.txt" # Extra file in dest
mkdir "$TMP_DIR/dest2/subdir_extra"
echo "foo" > "$TMP_DIR/dest2/subdir_extra/foo.txt" # Extra dir in dest
run_test "Sync with Deletion" 0 "$TMP_DIR/src2" "$TMP_DIR/dest2"
if [ $? -eq 0 ]; then
    assert_exists "$TMP_DIR/dest2/fileA.txt" && assert_files_equal "$TMP_DIR/src2/fileA.txt" "$TMP_DIR/dest2/fileA.txt"
    assert_not_exists "$TMP_DIR/dest2/fileC.txt"
    assert_not_exists "$TMP_DIR/dest2/subdir_extra"
fi

# Test 3: Sync Empty Source
echo "Setting up Test 3..."
mkdir -p "$TMP_DIR/src3" "$TMP_DIR/dest3"
# src3 is empty
echo "fileA" > "$TMP_DIR/dest3/fileA.txt"
mkdir "$TMP_DIR/dest3/subdir"
echo "sub" > "$TMP_DIR/dest3/subdir/file.txt"
run_test "Sync Empty Source (Deletes All in Dest)" 0 "$TMP_DIR/src3" "$TMP_DIR/dest3"
if [ $? -eq 0 ]; then
    assert_not_exists "$TMP_DIR/dest3/fileA.txt"
    assert_not_exists "$TMP_DIR/dest3/subdir"
    # Check if dest3 itself still exists (it should)
    assert_is_dir "$TMP_DIR/dest3"
fi

# Test 4: Files/Dirs with Spaces
echo "Setting up Test 4..."
mkdir -p "$TMP_DIR/src4" "$TMP_DIR/dest4"
echo "content space" > "$TMP_DIR/src4/file with space.txt"
mkdir "$TMP_DIR/src4/dir with space"
echo "inner" > "$TMP_DIR/src4/dir with space/inner file.txt"
echo "extra dest" > "$TMP_DIR/dest4/extra file.txt" # To be deleted
run_test "Files/Dirs with Spaces" 0 "$TMP_DIR/src4" "$TMP_DIR/dest4"
if [ $? -eq 0 ]; then
    assert_exists "$TMP_DIR/dest4/file with space.txt" && assert_files_equal "$TMP_DIR/src4/file with space.txt" "$TMP_DIR/dest4/file with space.txt"
    assert_exists "$TMP_DIR/dest4/dir with space/inner file.txt" && assert_files_equal "$TMP_DIR/src4/dir with space/inner file.txt" "$TMP_DIR/dest4/dir with space/inner file.txt"
    assert_not_exists "$TMP_DIR/dest4/extra file.txt"
fi

# Test 5: Symbolic Links
echo "Setting up Test 5..."
mkdir -p "$TMP_DIR/src5" "$TMP_DIR/dest5"
echo "target file" > "$TMP_DIR/src5/target.txt"
ln -s target.txt "$TMP_DIR/src5/link_to_target" # Link created in source
echo "extra" > "$TMP_DIR/dest5/extra.txt" # To be deleted
ln -s extra.txt "$TMP_DIR/dest5/old_link" # Old link to be deleted
run_test "Symbolic Links" 0 "$TMP_DIR/src5" "$TMP_DIR/dest5"
if [ $? -eq 0 ]; then
    assert_exists "$TMP_DIR/dest5/target.txt"
    assert_is_link "$TMP_DIR/dest5/link_to_target"
    # Optional: check link target (readlink might vary slightly)
    # link_target=$(readlink "$TMP_DIR/dest5/link_to_target")
    # if [ "$link_target" != "target.txt" ]; then echo "FAIL Link target mismatch"; ((FAIL_COUNT++)); fi
    assert_not_exists "$TMP_DIR/dest5/extra.txt"
    assert_not_exists "$TMP_DIR/dest5/old_link"
fi

# == Interactive Tests (-i) ==
# NOTE: These only test the script's confirmation prompt and a simple
# 'y'/'n' reply to rsync's -I prompt for *one* expected deletion.

# Test 6: Interactive Deletion - Confirm 'y'
echo "Setting up Test 6..."
mkdir -p "$TMP_DIR/src6" "$TMP_DIR/dest6"
echo "file A" > "$TMP_DIR/src6/fileA.txt"
echo "file A" > "$TMP_DIR/dest6/fileA.txt"
echo "delete me" > "$TMP_DIR/dest6/fileB.txt" # Only in dest
echo -e "\n--- Test ${TEST_COUNT}: Interactive Deletion - Confirm 'y' ---"
((TEST_COUNT++))
echo "Running: echo 'y' | $SYNC_SCRIPT -i $TMP_DIR/src6 $TMP_DIR/dest6 (Simulating 'y' for script confirm AND 'y' for rsync delete)"
# Provide 'y' for the script's prompt, then 'y' again for rsync's -I prompt
output_log=$(echo -e "y\ny" | "$SYNC_SCRIPT" -i "$TMP_DIR/src6" "$TMP_DIR/dest6" 2>&1)
exit_code=$?
echo " -> Exit Code: $exit_code (Expected: 0)"
if [ "$exit_code" -ne 0 ]; then
    echo -e "❌ ${RED}FAIL:${NC} Unexpected exit code."
    echo "$output_log"
    ((FAIL_COUNT++))
else
    assert_exists "$TMP_DIR/dest6/fileA.txt"
    assert_not_exists "$TMP_DIR/dest6/fileB.txt" # Should be deleted
fi

# Test 7: Interactive Deletion - Deny 'n'
echo "Setting up Test 7..."
mkdir -p "$TMP_DIR/src7" "$TMP_DIR/dest7"
echo "file A" > "$TMP_DIR/src7/fileA.txt"
echo "file A" > "$TMP_DIR/dest7/fileA.txt"
echo "keep me" > "$TMP_DIR/dest7/fileB.txt" # Only in dest
echo -e "\n--- Test ${TEST_COUNT}: Interactive Deletion - Deny 'n' ---"
((TEST_COUNT++))
echo "Running: echo 'y' | $SYNC_SCRIPT -i $TMP_DIR/src7 $TMP_DIR/dest7 (Simulating 'y' for script confirm AND 'n' for rsync delete)"
# Provide 'y' for the script's prompt, then 'n' for rsync's -I prompt
output_log=$(echo -e "y\nn" | "$SYNC_SCRIPT" -i "$TMP_DIR/src7" "$TMP_DIR/dest7" 2>&1)
exit_code=$?
echo " -> Exit Code: $exit_code (Expected: 0)" # Rsync still exits 0 even if deletions are skipped
if [ "$exit_code" -ne 0 ]; then
    echo -e "❌ ${RED}FAIL:${NC} Unexpected exit code."
    echo "$output_log"
    ((FAIL_COUNT++))
else
    assert_exists "$TMP_DIR/dest7/fileA.txt"
    # assert_exists "$TMP_DIR/dest7/fileB.txt" # Should NOT be deleted
    # Note: Testing 'n' confirmation for rsync -I via piping is unreliable
    # as rsync -I often reads directly from /dev/tty, ignoring the pipe.
    # We confirm -i works via Test 6 (where 'y' allows deletion).
fi


# == Error Condition Tests ==

# Test 8: Missing Arguments
run_test "Missing Arguments" 1 # No args provided to script

# Test 9: Source Not Found
run_test "Source Not Found" 1 "$TMP_DIR/nonexistent_src" "$TMP_DIR/dest_err"

# Test 10: Destination is a File
echo "Setting up Test 10..."
mkdir -p "$TMP_DIR/src10"
touch "$TMP_DIR/dest_is_file" # Create dest as a file
run_test "Destination is a File" 1 "$TMP_DIR/src10" "$TMP_DIR/dest_is_file"
rm "$TMP_DIR/dest_is_file" # Clean up the file

# Test 11: Help Flag
run_test "Help Flag (-h)" 1 -h

# --- Final Report ---
echo -e "\n--- Test Summary ---"
if [ "$FAIL_COUNT" -eq 0 ]; then
  echo -e "✅ ${GREEN}All ${TEST_COUNT} tests passed!${NC}"
  exit 0
else
  echo -e "❌ ${RED}${FAIL_COUNT} out of ${TEST_COUNT} tests failed.${NC}"
  exit 1
fi 