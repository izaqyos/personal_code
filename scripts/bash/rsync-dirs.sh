#!/bin/bash

# Purpose: Synchronizes the destination directory to match the source directory using rsync.
#          Files/dirs in the destination that are not in the source will be deleted.
# Direction: Source -> Destination ONLY. To sync Destination -> Source, swap the arguments.

# --- Configuration ---
INTERACTIVE_MODE=0 # Default: 0 (false), run non-interactively

# Define colors for output (requires tput)
if command -v tput >/dev/null 2>&1 && [[ -t 1 ]]; then
  GREEN=$(tput setaf 2)
  RED=$(tput setaf 1)
  YELLOW=$(tput setaf 3)
  BLUE=$(tput setaf 4)
  BOLD=$(tput bold)
  NC=$(tput sgr0) # No Color
else
  # No color support or not a TTY
  GREEN=""
  RED=""
  YELLOW=""
  BLUE=""
  BOLD=""
  NC=""
fi

# --- Functions ---
usage() {
  echo "Usage: $0 [-i | --interactive] <source_directory> <destination_directory>"
  echo ""
  echo "Synchronizes the destination directory to match the source directory using rsync."
  echo "Direction is ALWAYS source -> destination."
  echo "To sync destination -> source, swap the directory arguments."
  echo "Files in the destination that are not in the source will be deleted."
  echo ""
  echo "Options:"
  echo "  -i, --interactive   Prompt before deleting files in the destination."
  echo "  -h, --help          Display this help message."
  exit 1
}

# --- Argument Parsing ---
# Use a loop to handle options potentially mixed with positional arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -i|--interactive)
      INTERACTIVE_MODE=1
      shift # past argument
      ;;
    -h|--help)
      usage
      ;;
    *)
      # Assume it's the source or destination directory if not an option
      # Break the loop once we hit the first non-option argument
      # This handles cases like: script.sh dir1 -i dir2 (which is bad practice but might happen)
      # A more robust solution uses getopt, but this is common for simpler scripts.
      if [[ -z "$SOURCE_DIR" ]]; then
        SOURCE_DIR="$1"
      elif [[ -z "$DEST_DIR" ]]; then
        DEST_DIR="$1"
      else
        echo "${RED}Error: Unexpected argument '$1'${NC}"
        usage
      fi
      shift # past argument
      ;;
  esac
done

# --- Validation ---
if [ -z "$SOURCE_DIR" ] || [ -z "$DEST_DIR" ]; then
  # Directly call usage, it implies arguments were missing.
  usage
fi

# Validate directories exist
if [ ! -d "$SOURCE_DIR" ]; then
  echo "${RED}Error: Source directory '$SOURCE_DIR' not found.${NC}"
  exit 1
fi
# Destination directory doesn't strictly *need* to exist beforehand,
# rsync can create it. But we check if it exists *and* is not a directory.
if [ -e "$DEST_DIR" ] && [ ! -d "$DEST_DIR" ]; then
   echo "${RED}Error: Destination '$DEST_DIR' exists but is not a directory.${NC}"
   exit 1
fi


# --- Ensure trailing slash on source for content sync ---
# This tells rsync to sync the *contents* of the source directory
# into the destination directory. Without it, it would create
# source_directory *inside* destination_directory if it didn't exist.
[[ "$SOURCE_DIR" != */ ]] && SOURCE_DIR="${SOURCE_DIR}/"

# --- Prepare rsync command ---
RSYNC_CMD="rsync"
# -a: archive mode (recursive, preserves permissions, times, owner, group, links, devices)
# -v: verbose (shows files being transferred/deleted)
# -c: checksum comparison (forces content check, potentially slower but more robust)
# --delete: delete files on the destination that are not in the source
RSYNC_OPTIONS="-avc --delete"

echo "-------------------------------------------"
echo "Starting synchronization:"
echo " -> ${BOLD}Source:${NC}      ${YELLOW}${SOURCE_DIR}${NC}"
echo " -> ${BOLD}Destination:${NC} ${YELLOW}${DEST_DIR}${NC}"

if [ "$INTERACTIVE_MODE" -eq 1 ]; then
  # -I or --interactive: Ask user confirmation before deleting files on the receiving side.
  # Note: This specifically prompts for DELETIONS caused by --delete.
  # It does NOT prompt before overwriting existing files that have changed.
  RSYNC_OPTIONS+=" -I" # Add interactive flag
  echo " -> ${BOLD}Mode:${NC}        ${BLUE}Interactive (will prompt before deletions)${NC}"
  echo "-------------------------------------------"
  echo "Running rsync interactively. You will be asked to confirm deletions."
  echo "Type 'y' or 'yes' to confirm, 'n' or 'no' to skip a deletion."
  # Add a final confirmation before starting interactive mode
  read -p "Proceed with interactive sync? (y/N): " confirm
  # Default to No if user just presses Enter
  if [[ ! "$confirm" =~ ^[Yy]([Ee][Ss])?$ ]]; then
      echo "Sync cancelled by user."
      exit 0
  fi
else
  echo " -> ${BOLD}Mode:${NC}        ${GREEN}Non-Interactive (automatic sync)${NC}"
  echo "-------------------------------------------"
  # Add a final confirmation before starting non-interactive mode
  read -p "${BOLD}${RED}WARNING:${NC} This will automatically modify '${DEST_DIR}' to match '${SOURCE_DIR}', including deletions. Proceed? (y/N): " confirm
  # Default to No if user just presses Enter
  if [[ ! "$confirm" =~ ^[Yy]([Ee][Ss])?$ ]]; then
      echo "Sync cancelled by user."
      exit 0
  fi
fi

# --- Execute rsync ---
echo "Running: $RSYNC_CMD $RSYNC_OPTIONS \"$SOURCE_DIR\" \"$DEST_DIR\""
echo "-------------------------------------------"

# Execute the command
# Using eval allows the shell to correctly parse the options string, including any flags
# added conditionally (like -I). In this script, the variables are controlled internally,
# making eval relatively safe. An alternative for more complex cases is using arrays.
eval "$RSYNC_CMD $RSYNC_OPTIONS \"$SOURCE_DIR\" \"$DEST_DIR\""

# Capture exit code
rsync_exit_code=$?

echo "-------------------------------------------"
if [ $rsync_exit_code -eq 0 ]; then
  echo "${GREEN}[SUCCESS] Synchronization completed.${NC}"
else
  echo "${RED}[ERROR] rsync exited with status ${rsync_exit_code}. Please check the output above for errors.${NC}"
fi
echo "-------------------------------------------"

exit $rsync_exit_code

