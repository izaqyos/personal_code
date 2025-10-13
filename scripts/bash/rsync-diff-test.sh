#!/bin/bash

# Test script for rsync-diff.sh

# --- Configuration ---
# Assuming rsync-diff.sh is in the same directory or in PATH
SCRIPT_DIR=$(dirname "$0")
DIFF_SCRIPT="${SCRIPT_DIR}/rsync-diff.sh"
# Alternative: DIFF_SCRIPT="rsync-diff.sh" # If it's in PATH

# Check if the diff script exists and is executable
if [ ! -x "$DIFF_SCRIPT" ]; then
    echo "Error: Diff script '$DIFF_SCRIPT' not found or not executable."
    echo "Please ensure it's in the same directory or in your PATH and has execute permissions."
    exit 1
fi

# Create temporary directories
TEST_SOURCE=$(mktemp -d -t rsync_diff_test_source_XXXXXX)
TEST_DEST=$(mktemp -d -t rsync_diff_test_dest_XXXXXX)

# --- Cleanup Function ---
cleanup() {
  echo "Cleaning up temporary directories..."
  rm -rf "$TEST_SOURCE" "$TEST_DEST"
  echo "Cleanup complete."
}
# Register the cleanup function to run on script exit (normal or error)
trap cleanup EXIT

# --- Populate Test Directories ---
echo "Setting up test directories..."

# 1. Identical file
echo "Identical content" > "$TEST_SOURCE/common_file.txt"
echo "Identical content" > "$TEST_DEST/common_file.txt"

# 2. File only in source
echo "This file is only in the source" > "$TEST_SOURCE/only_in_source.txt"

# 3. File only in destination
echo "This file is only in the destination" > "$TEST_DEST/only_in_dest.txt"

# 4. Different content
echo "Source content" > "$TEST_SOURCE/diff_content.txt"
echo "Destination content" > "$TEST_DEST/diff_content.txt"

# 5. Different permissions
echo "Permissions test" > "$TEST_SOURCE/diff_perms.txt"
echo "Permissions test" > "$TEST_DEST/diff_perms.txt"
chmod 755 "$TEST_SOURCE/diff_perms.txt" # Executable in source
chmod 644 "$TEST_DEST/diff_perms.txt" # Not executable in dest

# 6. Subdirectory only in source
mkdir "$TEST_SOURCE/subdir_source"
echo "File inside source-only subdir" > "$TEST_SOURCE/subdir_source/file.txt"

# 7. Subdirectory only in destination
mkdir "$TEST_DEST/subdir_dest"
echo "File inside dest-only subdir" > "$TEST_DEST/subdir_dest/file.txt"

# 8. Empty directory only in source
mkdir "$TEST_SOURCE/empty_dir_source"

# 9. Empty directory only in destination
mkdir "$TEST_DEST/empty_dir_dest"

# 10. Identical subdirectory structure + content
mkdir "$TEST_SOURCE/common_subdir"
mkdir "$TEST_DEST/common_subdir"
echo "Nested identical file" > "$TEST_SOURCE/common_subdir/nested_common.txt"
echo "Nested identical file" > "$TEST_DEST/common_subdir/nested_common.txt"

# 11. Subdirectory with different content within
mkdir "$TEST_SOURCE/diff_subdir"
mkdir "$TEST_DEST/diff_subdir"
echo "Source nested" > "$TEST_SOURCE/diff_subdir/nested_diff.txt"
echo "Dest nested" > "$TEST_DEST/diff_subdir/nested_diff.txt"


echo "Test setup complete."
echo "Source Tree:"
find "$TEST_SOURCE" -ls
echo "---------------------"
echo "Destination Tree:"
find "$TEST_DEST" -ls
echo "---------------------"


# --- Run the Diff Script ---
echo "Running $DIFF_SCRIPT..."
echo "Command: $DIFF_SCRIPT \"$TEST_SOURCE\" \"$TEST_DEST\""
echo "--------------------- Output ---------------------"

# Execute the script and capture output
OUTPUT=$("$DIFF_SCRIPT" "$TEST_SOURCE" "$TEST_DEST")
EXIT_CODE=$?

echo "$OUTPUT" # Print the output for manual inspection

echo "--------------------------------------------------"
echo "Script finished with exit code: $EXIT_CODE"
echo "--------------------------------------------------"

# --- Basic Verification (Optional but Recommended) ---
# Check if the output contains expected markers. This is a basic check.
# A more robust test suite would parse the output more precisely.
echo "Performing basic output checks..."
checks_passed=true

# Check for file only in source
if ! echo "$OUTPUT" | grep -q "\[+\] Only in Source:.*only_in_source.txt"; then
    echo "Check FAILED: Expected '[+] Only in Source:' for only_in_source.txt"
    checks_passed=false
fi

# Check for directory only in source
if ! echo "$OUTPUT" | grep -q "\[+\] Only in Source:.*subdir_source (Directory)"; then
    echo "Check FAILED: Expected '[+] Only in Source:' for subdir_source"
    checks_passed=false
fi

# Check for file only in dest
if ! echo "$OUTPUT" | grep -q "\[-\] Only in Dest:.*only_in_dest.txt"; then
    echo "Check FAILED: Expected '[-] Only in Dest:' for only_in_dest.txt"
    checks_passed=false
fi

# Check for directory only in dest
if ! echo "$OUTPUT" | grep -q "\[-\] Only in Dest:.*subdir_dest"; then
    echo "Check FAILED: Expected '[-] Only in Dest:' for subdir_dest"
    checks_passed=false
fi

# Check for different content
if ! echo "$OUTPUT" | grep -q "\[~\] Different:.*diff_content.txt"; then
    echo "Check FAILED: Expected '[~] Different:' for diff_content.txt"
    checks_passed=false
fi

# Check for different permissions (might also show as size/time depending on rsync version/filesystem)
# We look for the file marked as different. The exact code (like '.f...p....') might vary.
if ! echo "$OUTPUT" | grep -q "\[~\] Different:.*diff_perms.txt"; then
    echo "Check FAILED: Expected '[~] Different:' for diff_perms.txt (permissions)"
    checks_passed=false
fi

# Check for file difference within subdir
if ! echo "$OUTPUT" | grep -q "\[~\] Different:.*diff_subdir/nested_diff.txt"; then
    echo "Check FAILED: Expected '[~] Different:' for diff_subdir/nested_diff.txt"
    checks_passed=false
fi

# Check final status message
if ! echo "$OUTPUT" | grep -q "Comparison finished. Differences found."; then
     echo "Check FAILED: Expected 'Comparison finished. Differences found.' message."
     checks_passed=false
fi


echo "--------------------------------------------------"
if [ "$checks_passed" = true ]; then
    echo "Basic checks PASSED."
    # Exit code 0 already handled by trap
else
    echo "Basic checks FAILED."
    exit 1 # Indicate test failure
fi

# Cleanup happens automatically via trap EXIT 