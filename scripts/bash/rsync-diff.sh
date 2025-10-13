#!/bin/bash

# --- Script Explanation ---
# Purpose:
#   Compares the contents of two directories (source and destination) using rsync
#   and reports the differences found. It highlights files/directories that are:
#     [+] Only in the source directory.
#     [-] Only in the destination directory.
#     [~] Present in both, but differ in content or attributes (size, mod time, etc.).
#
# How it Works:
#   1. Argument Handling: Validates input arguments (two directories must be provided).
#   2. Path Normalization: Ensures source and destination paths end with '/' for
#      rsync to compare directory *contents*.
#   3. rsync Dry Run: Executes `rsync -nia --delete source/ dest/`.
#      - `-n` (dry-run): Simulates the sync without changing files.
#      - `-i` (itemize-changes): Generates detailed output codes for differences.
#      - `-a` (archive): Recursively compares files preserving attributes.
#      - `--delete`: Reports files present only in the destination.
#   4. awk Parsing: The output of rsync is piped to `awk`. The awk script:
#      - Parses the itemized change codes from rsync.
#      - Formats the output with colors (if supported) and symbols ([+], [-], [~]).
#      - Provides a summary at the end.
#   5. Exit Status: Checks rsync's exit code for potential errors during comparison.
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
  echo "Compares two directories using rsync and prints differences."
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

# --- Ensure trailing slashes for rsync content comparison ---
# This tells rsync to compare the *contents* of the directories
[[ "$SOURCE_DIR" != */ ]] && SOURCE_DIR="${SOURCE_DIR}/"
[[ "$DEST_DIR" != */ ]] && DEST_DIR="${DEST_DIR}/"

# --- Main Logic ---
echo "Comparing directories:"
echo " -> Source:      ${YELLOW}${SOURCE_DIR}${NC}"
echo " -> Destination: ${YELLOW}${DEST_DIR}${NC}"
echo "-------------------------------------------"

# Use awk to parse the rsync output
# rsync options:
# -n: dry-run
# -i: itemize changes
# -a: archive mode (recursive, preserves attrs)
# -c: checksum comparison
# --delete: report files only in destination
rsync -niac --delete "$SOURCE_DIR" "$DEST_DIR" | \
awk -v G="$GREEN" -v R="$RED" -v Y="$YELLOW" -v B="$BLUE" -v NC="$NC" '
BEGIN {
    changes_found = 0; # Flag to track if any differences were reported
}
{
    # Skip blank lines or lines that are just "." (current dir)
    if ($0 ~ /^ *$/ || $0 ~ /^\.$/) {
        next;
    }

    # Extract the change code (e.g., "<f+++++++++,"cd+++++++++") and the filename
    change_code = substr($1, 1, 2); # First two chars are most significant
    # Awk is 1-based indexing for fields; $1 is code, $2 onwards is filename
    # Reconstruct filename which might contain spaces
    filename = "";
    for (i = 2; i <= NF; i++) {
        filename = filename (i > 2 ? " " : "") $i;
    }

    # Interpret the change codes
    # See `man rsync` under "--itemize-changes" for full details

    # Files/Dirs/Links only in SOURCE (would be sent to DEST)
    # <f = file, <d = directory, <L = symlink
    if (change_code ~ /^<[fdL]/) {
        type = "File";
        if (substr($1, 2, 1) == "d") type = "Directory";
        if (substr($1, 2, 1) == "L") type = "Symlink";
        printf "%s[+] Only in Source:%s %s (%s)\n", G, NC, filename, type;
        changes_found = 1;
    }
    # Files/Dirs only in DESTINATION (would be deleted from DEST)
    else if ($1 == "*deleting") {
        # $1 is "*deleting", filename starts from $2
        printf "%s[-] Only in Dest:  %s %s\n", R, NC, filename;
        changes_found = 1;
    }
    # Files/Dirs/Links present in both, but DIFFERENT
    # c = different checksum (file content) or different metadata (dirs/links)
    # t/T = modification time is different
    # s = size is different
    # p = permissions are different
    # o = owner is different
    # g = group is different
    # etc.
    # We group all these as "Different" for simplicity
    else if (substr($1, 1, 1) == "c" || # Checksum differs (files), or metadata (dirs)
             substr($1, 1, 1) ~ /[.>]f.[cstpgol]/ || # File attrs differ (size, time, perms etc)
             substr($1, 1, 1) ~ /[.>]d.[cstpgol]/ || # Dir attrs differ
             substr($1, 1, 1) ~ /[.>]L.[cstpgol]/ )  # Link attrs differ
    {
         # Heuristic to determine type if possible from 2nd char
        type = "?";
        if (substr($1, 2, 1) == "f") type = "File";
        if (substr($1, 2, 1) == "d") type = "Directory";
        if (substr($1, 2, 1) == "L") type = "Symlink";
        printf "%s[~] Different:     %s %s (%s) [%s]\n", B, NC, filename, type, $1; # Show rsync code for detail
        changes_found = 1;
    }
    # Optionally catch unhandled lines for debugging:
    # else {
    #    print "[?] Unknown/Ignored:", $0;
    # }
}
END {
    print "-------------------------------------------";
    if (changes_found == 0) {
        print G "[OK] Directories appear identical." NC;
    } else {
        print "Comparison finished. Differences found.";
        print G "[+] = Only in Source" NC;
        print R "[-] = Only in Destination" NC;
        print B "[~] = Exists in both, but differs (content/attributes)" NC;
    }
}'

# Check rsync exit code (optional, but good practice)
rsync_exit_code=$?
if [ $rsync_exit_code -ne 0 ]; then
    echo "${YELLOW}Warning: rsync exited with status ${rsync_exit_code}. There might have been errors during comparison.${NC}"
fi

exit 0 # Exit successfully
