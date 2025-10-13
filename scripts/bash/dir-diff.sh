#!/bin/bash

# --- Script Explanation ---
# Purpose:
#   Compares the contents of two directories (source and destination) using diff -r
#   and reports the differences found. It highlights files/directories that are:
#     [+] Only in the source directory.
#     [-] Only in the destination directory.
#     [~] Present in both, but differ in content.
# Note: This script primarily detects content differences. Attribute-only
#       differences (like permissions) might not be reported if content is identical.
#
# How it Works:
#   1. Argument Handling: Validates input arguments (two directories must be provided).
#   2. diff Execution: Runs `diff -r --brief source dest` to compare directories recursively.
#      `--brief` reports only whether files differ, not the actual differences.
#   3. Output Parsing: Processes the output of `diff`:
#      - Lines starting "Only in <source>" are marked [+].
#      - Lines starting "Only in <dest>" are marked [-].
#      - Lines starting "Files ... and ... differ" are marked [~].
#   4. Formatting: Prints results with colors and symbols.

# --- Configuration ---
# Define colors for output (requires tput)
if command -v tput >/dev/null 2>&1 && [[ -t 1 ]]; then
  GREEN=$(tput setaf 2)
  RED=$(tput setaf 1)
  YELLOW=$(tput setaf 3)
  BLUE=$(tput setaf 4)
  NC=$(tput sgr0) # No Color
else
  # No color support or not a TTY
  GREEN=""
  RED=""
  YELLOW=""
  BLUE=""
  NC=""
fi

# --- Functions ---
usage() {
  echo "Usage: $0 <source_directory> <destination_directory>"
  echo "Compares two directories using 'diff -r --brief' and prints differences."
  exit 1
}

# --- Argument Handling ---
if [ "$#" -ne 2 ]; then
  usage
fi

SOURCE_DIR="$1"
DEST_DIR="$2"

# Validate directories exist
if [ ! -d "$SOURCE_DIR" ]; then
  echo "${RED}Error: Source directory '$SOURCE_DIR' not found.${NC}"
  exit 1
fi
if [ ! -d "$DEST_DIR" ]; then
  echo "${RED}Error: Destination directory '$DEST_DIR' not found.${NC}"
  exit 1
fi

# --- Main Logic ---
echo "Comparing directories using 'diff -r --brief':"
echo " -> Source:      ${YELLOW}${SOURCE_DIR}${NC}"
echo " -> Destination: ${YELLOW}${DEST_DIR}${NC}"
echo "-------------------------------------------"

changes_found=0
# Run diff and process its output line by line
# We ignore stderr for common subdirectories messages, exit code handles errors
diff_output=$(diff -r --brief "$SOURCE_DIR" "$DEST_DIR" 2>/dev/null)
diff_exit_code=$?

# diff exits with 0=identical, 1=different, >1=error
if [ $diff_exit_code -gt 1 ]; then
    echo "${RED}Error running diff command (exit code: $diff_exit_code).${NC}"
    # Attempt to run without redirection to see error
    diff -r --brief "$SOURCE_DIR" "$DEST_DIR"
    exit $diff_exit_code
elif [ $diff_exit_code -eq 1 ]; then
    changes_found=1
    echo "$diff_output" | while IFS= read -r line; do
        # Handles "Only in <dir>: <filename>"
        if [[ "$line" == "Only in "* ]]; then
            # Extract directory and filename part
            # dir_part: "Only in <dir>"
            # filename_part: " <filename>" (with leading space)
            dir_part=$(echo "$line" | cut -d ":" -f 1)
            filename_part=$(echo "$line" | cut -d ":" -f 2- | sed 's/^ //') # Remove leading space

            # Check which directory it was found in
            if [[ "$dir_part" == "Only in ${SOURCE_DIR}"* ]]; then
                printf "%s[+] Only in Source:%s %s\n" "$GREEN" "$NC" "$filename_part"
            elif [[ "$dir_part" == "Only in ${DEST_DIR}"* ]]; then
                printf "%s[-] Only in Dest:  %s %s\n" "$RED" "$NC" "$filename_part"
            else
                 printf "${YELLOW}[?] Unknown 'Only in' line: %s${NC}\n" "$line"
            fi
        # Handles "Files <file1> and <file2> differ" and various type mismatches like:
        # "File <file1> is a directory while file <file2> is a regular file"
        # "File <file1> is a symbolic link while file <file2> is a regular file"
        elif [[ "$line" == "Files "* ]] || [[ "$line" == "File "* ]]; then
            # Attempt to extract the first full file path mentioned in the line.
            # Works by: splitting by " and " (taking first part), then splitting by " is a " (taking first part),
            # then removing the leading "Files " or "File " and potential quotes.
            file1_path=$(echo "$line" | awk -F' and ' '{print $1}' | awk -F' is a ' '{print $1}' | sed -E "s/^(Files|File) ('?)//; s/('?)$//")

            # Remove the base source directory path using parameter expansion to get the relative name.
            # ${string#prefix} removes the shortest matching prefix.
            rel_filename="${file1_path#$SOURCE_DIR/}"

            # Check if extraction worked (got a non-empty filename that's different from the original line)
            if [[ -n "$rel_filename" && "$file1_path" != "$rel_filename" ]]; then # Check extraction worked
                 type=""
                 # Add a generic note if the line indicates a type mismatch
                 if [[ "$line" == *" is a directory"* || "$line" == *" is a symbolic link"* || "$line" == *" while file "* ]]; then
                     type=" (Type mismatch or content differs)"
                 fi
                 printf "%s[~] Different:     %s %s%s\n" "$BLUE" "$NC" "$rel_filename" "$type"
            else
                 # Fallback if parsing failed
                 printf "${YELLOW}[?] Failed to parse diff line: %s${NC}\n" "$line"
            fi
        elif [[ "$line" == "Common subdirectories:"* ]]; then
            continue # Ignore common subdirs line
        elif [[ -n "$line" ]]; then # Report any other non-empty, non-matching lines
             printf "${YELLOW}[?] Unknown diff line: %s${NC}\n" "$line"
        fi
    done
fi


echo "-------------------------------------------"
if [ $changes_found -eq 0 ]; then
    echo "${GREEN}[OK] Directories appear identical.${NC}"
else
    echo "Comparison finished. Differences found."
    echo "${GREEN}[+] = Only in Source${NC}"
    echo "${RED}[-] = Only in Destination${NC}"
    echo "${BLUE}[~] = Exists in both, but differs (content/structure)${NC}"
fi

# Exit with diff's code (0=same, 1=diff, >1=error)
exit $diff_exit_code 