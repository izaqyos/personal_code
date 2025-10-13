#!/bin/bash

# Test script for dir-diff.sh

# --- Configuration ---
# Assuming dir-diff.sh is in the same directory or in PATH
SCRIPT_DIR=$(dirname "$0")
DIFF_SCRIPT="${SCRIPT_DIR}/dir-diff.sh"

# Check if the diff script exists and is executable
if [ ! -x "$DIFF_SCRIPT" ]; then
    echo "Error: Diff script '$DIFF_SCRIPT' not found or not executable."
    echo "Please ensure it's in the same directory or in your PATH and has execute permissions."
    exit 1
fi

# Create temporary directories
TEST_SOURCE=$(mktemp -d -t dir_diff_test_source_XXXXXX)
TEST_DEST=$(mktemp -d -t dir_diff_test_dest_XXXXXX)

# --- Cleanup Function ---
cleanup() {
  echo "Cleaning up temporary directories..."
  rm -rf "$TEST_SOURCE" "$TEST_DEST"
  echo "Cleanup complete."
}
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

# 5. Different permissions (Content identical - diff -r --brief likely won't report difference)
echo "Permissions test" > "$TEST_SOURCE/diff_perms.txt"
echo "Permissions test" > "$TEST_DEST/diff_perms.txt"
chmod 755 "$TEST_SOURCE/diff_perms.txt"
chmod 644 "$TEST_DEST/diff_perms.txt"

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

# 12. File in source, Directory in dest
echo "File content" > "$TEST_SOURCE/file_vs_dir"
mkdir "$TEST_DEST/file_vs_dir"
echo "Content in dest dir" > "$TEST_DEST/file_vs_dir/inner_file"

# 13. Directory in source, File in dest
mkdir "$TEST_SOURCE/dir_vs_file"
echo "Content in source dir" > "$TEST_SOURCE/dir_vs_file/inner_file"
echo "File content" > "$TEST_DEST/dir_vs_file"

# 14. Symlink only in source (pointing to a file)
ln -s common_file.txt "$TEST_SOURCE/link_only_source"

# 15. Symlink only in dest (pointing to a file)
ln -s common_file.txt "$TEST_DEST/link_only_dest"

# 16. Symlinks pointing to different targets
ln -s only_in_source.txt "$TEST_SOURCE/link_diff_target"
ln -s only_in_dest.txt "$TEST_DEST/link_diff_target" # Points to different file

# 17. Symlink in source, File in dest
ln -s common_file.txt "$TEST_SOURCE/link_vs_file"
echo "Actual file" > "$TEST_DEST/link_vs_file"

# 18. File with spaces
echo "File with spaces" > "$TEST_SOURCE/file with spaces.txt"
echo "File with spaces" > "$TEST_DEST/file with spaces.txt" # Identical

# 19. File with spaces (different)
echo "Source spaces" > "$TEST_SOURCE/diff file with spaces.txt"
echo "Dest spaces" > "$TEST_DEST/diff file with spaces.txt" # Different

# 20. Empty file only in source
touch "$TEST_SOURCE/empty_file_source.txt"

# 21. Empty file only in dest
touch "$TEST_DEST/empty_file_dest.txt"

# 22. Empty file vs non-empty file
touch "$TEST_SOURCE/empty_vs_not.txt"
echo "Not empty" > "$TEST_DEST/empty_vs_not.txt"


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
# Capture exit code *after* command substitution
EXIT_CODE=$?

echo "$OUTPUT" # Print the output for manual inspection

echo "--------------------------------------------------"
echo "Script finished with exit code: $EXIT_CODE"
echo "--------------------------------------------------"

# --- Verification ---
echo "Performing output checks..."
checks_passed=true

# Expect diff to exit with 1 (differences found)
if [ "$EXIT_CODE" -ne 1 ]; then
    echo "Check FAILED: Expected exit code 1 (differences found), but got $EXIT_CODE."
    checks_passed=false
fi

# Check for file only in source
if ! echo "$OUTPUT" | grep -q "\[+\] Only in Source:.*only_in_source.txt"; then
    echo "Check FAILED: Expected '[+] Only in Source:' for only_in_source.txt"
    checks_passed=false
fi

# Check for directory only in source
if ! echo "$OUTPUT" | grep -q "\[+\] Only in Source:.*subdir_source"; then
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

# Check for file difference within subdir
if ! echo "$OUTPUT" | grep -q "\[~\] Different:.*diff_subdir/nested_diff.txt"; then
    echo "Check FAILED: Expected '[~] Different:' for diff_subdir/nested_diff.txt"
    checks_passed=false
fi

# Check for file vs dir conflict (diff should report this)
# Note: diff's exact message might vary slightly across versions/OS
if ! echo "$OUTPUT" | grep -q "\[~\] Different:.*file_vs_dir"; then
    # Allow for alternative reporting if the basic [~] check fails
    if ! (echo "$OUTPUT" | grep -q "File .*file_vs_dir is a regular file" && echo "$OUTPUT" | grep -q "File .*file_vs_dir is a directory"); then
        echo "Check FAILED: Expected difference report for file_vs_dir (File vs Dir)"
        checks_passed=false
    fi
fi
if ! echo "$OUTPUT" | grep -q "\[~\] Different:.*dir_vs_file"; then
     if ! (echo "$OUTPUT" | grep -q "File .*dir_vs_file is a directory" && echo "$OUTPUT" | grep -q "File .*dir_vs_file is a regular file"); then
        echo "Check FAILED: Expected difference report for dir_vs_file (Dir vs File)"
        checks_passed=false
    fi
fi

# Check for link only in source
if ! echo "$OUTPUT" | grep -q "\[+\] Only in Source:.*link_only_source"; then
    echo "Check FAILED: Expected '[+] Only in Source:' for link_only_source"
    checks_passed=false
fi

# Check for link only in dest
if ! echo "$OUTPUT" | grep -q "\[-\] Only in Dest:.*link_only_dest"; then
    echo "Check FAILED: Expected '[-] Only in Dest:' for link_only_dest"
    checks_passed=false
fi

# Check for links with different targets
if ! echo "$OUTPUT" | grep -q "\[~\] Different:.*link_diff_target"; then
    echo "Check FAILED: Expected '[~] Different:' for link_diff_target"
    checks_passed=false
fi

# Check for link vs file
if ! echo "$OUTPUT" | grep -q "\[~\] Different:.*link_vs_file"; then
     if ! (echo "$OUTPUT" | grep -q "File .*link_vs_file is a symbolic link" && echo "$OUTPUT" | grep -q "File .*link_vs_file is a regular file"); then
        echo "Check FAILED: Expected difference report for link_vs_file (Link vs File)"
        checks_passed=false
    fi
fi

# Check that identical file with spaces is NOT listed
# Need precise grep to avoid matching 'diff file with spaces.txt'
if echo "$OUTPUT" | grep -Eq "(\[.\].*:\s+|\[~\].*:\s+)'?file with spaces\.txt'?$"; then
    echo "Check FAILED: Did NOT expect 'file with spaces.txt' to be listed in differences."
    checks_passed=false
fi

# Check that different file with spaces IS listed
if ! echo "$OUTPUT" | grep -q "\[~\] Different:.*diff file with spaces.txt"; then
    echo "Check FAILED: Expected '[~] Different:' for 'diff file with spaces.txt'"
    checks_passed=false
fi

# Check for empty file only in source
if ! echo "$OUTPUT" | grep -q "\[+\] Only in Source:.*empty_file_source.txt"; then
    echo "Check FAILED: Expected '[+] Only in Source:' for empty_file_source.txt"
    checks_passed=false
fi

# Check for empty file only in dest
if ! echo "$OUTPUT" | grep -q "\[-\] Only in Dest:.*empty_file_dest.txt"; then
    echo "Check FAILED: Expected '[-] Only in Dest:' for empty_file_dest.txt"
    checks_passed=false
fi

# Check for empty vs non-empty file
if ! echo "$OUTPUT" | grep -q "\[~\] Different:.*empty_vs_not.txt"; then
    echo "Check FAILED: Expected '[~] Different:' for empty_vs_not.txt"
    checks_passed=false
fi

# Reinstate checks for unique directories themselves (just not their contents)
if ! echo "$OUTPUT" | grep -q "\[+\] Only in Source:.*subdir_source"; then
    echo "Check FAILED: Expected '[+] Only in Source:' for subdir_source (directory itself)"
    checks_passed=false
fi
if ! echo "$OUTPUT" | grep -q "\[-\] Only in Dest:.*subdir_dest"; then
    echo "Check FAILED: Expected '[-] Only in Dest:' for subdir_dest (directory itself)"
    checks_passed=false
fi

# Check that identical file is NOT listed
if echo "$OUTPUT" | grep -q "common_file.txt"; then
    echo "Check FAILED: Did NOT expect common_file.txt to be listed in differences."
    checks_passed=false
fi

# Check that permissions-only difference file is NOT listed (diff -r --brief limitation)
if echo "$OUTPUT" | grep -q "diff_perms.txt"; then
    echo "Check FAILED: Did NOT expect diff_perms.txt to be listed (diff -r --brief limitation)."
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
else
    echo "Basic checks FAILED."
    # Exit with a different code to signal test failure
    exit 2
fi

# Exit code 0 if checks passed (cleanup runs via trap)
exit 0 