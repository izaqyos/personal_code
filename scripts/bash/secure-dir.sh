#!/bin/bash

# === Documentation ===
# Script: secure-dir.sh
#
# Purpose:
#   Creates an encrypted APFS `.sparsebundle` disk image from the contents of an
#   existing source directory on macOS. It is designed to help migrate sensitive
#   data from a plain folder into a secure, password-protected container.
#   After successful creation and optional verification, it prompts the user to
#   delete the original source directory.
#
# How it Works:
#   1.  Argument Parsing: Parses command-line arguments for the source directory,
#       desired image size (in GB), output path for the `.sparsebundle`,
#       and an optional path to a verification script (`dir-diff.sh`).
#   2.  Input Validation:
#       - Ensures all mandatory arguments (`--source`, `--size`, `--output`) are provided.
#       - Checks that the source directory exists and is readable.
#       - Validates that the specified size is a positive number.
#       - Ensures the intended output path for the `.sparsebundle` does not already exist.
#       - If a verification script path is provided, checks that it exists and is executable.
#   3.  Password Handling: Securely prompts the user to enter and confirm a password.
#   4.  Confirmation: Displays parameters and asks for confirmation before creation.
#   5.  Image Creation: Executes `hdiutil create` using AES-256 encryption, APFS,
#       sparse bundle format, and the source folder content.
#   6.  Verification (Optional):
#       - If `--verify-script` is provided, attaches the new image.
#       - Runs the specified script (e.g., `dir-diff.sh`) to compare source and volume.
#       - Detaches the image. Exits on verification failure.
#   7.  Source Deletion:
#       - If creation/verification succeeds, prompts for confirmation before deleting
#         the original source directory using `rm -rf`.
#   8.  Completion: Reports success or failure.
#
# Parameters:
#   --source <path>       (Mandatory) Path to the existing source directory.
#   --size <GB>           (Mandatory) Max size of the disk image in gigabytes (e.g., `300`).
#   --output <path>       (Mandatory) Full path for the output `.sparsebundle` image bundle.
#   --verify-script <path> (Optional) Path to `dir-diff.sh` for verification.
#   -h, --help            Display usage information.
#
# Prerequisites:
#   - macOS operating system.
#   - `hdiutil` command-line tool (built-in).
#   - (Optional) The `dir-diff.sh` script (executable) if using `--verify-script`.
#   - (Optional) `xpath` command (often part of `xmllint`) for verification mount point parsing.
#
# Usage Example:
#   ./secure-dir.sh --source ~/.secrets --size 50 --output ~/Desktop/Secrets.sparsebundle --verify-script ./dir-diff.sh
#   ./secure-dir.sh --source /Volumes/Data/Photos --size 500 --output ~/SecurePhotos.sparsebundle
#
# Caveats:
#   - Original source deletion is permanent after confirmation.
#   - Script refuses to overwrite an existing output file.
#   - Lost passwords mean lost data. Use a strong, memorable password.
#   - Verification relies on the correctness of the `--verify-script`.
#   - Creation/verification of large directories can take time.
# === End Documentation ===

# --- Configuration & Color --- 
set -e # Exit immediately if a command exits with a non-zero status.
set -o pipefail # Causes a pipeline to return the exit status of the last command that errored

# Define colors for output (requires tput)
if command -v tput >/dev/null 2>&1 && [[ -t 1 ]]; then
  GREEN=$(tput setaf 2)
  RED=$(tput setaf 1)
  YELLOW=$(tput setaf 3)
  BOLD=$(tput bold)
  NC=$(tput sgr0) # No Color
else
  GREEN=""
  RED=""
  YELLOW=""
  BOLD=""
  NC=""
fi # --- Helper Functions --- 

echo_err() {
    echo -e "${RED}Error: $*${NC}" >&2
}

echo_warn() {
    echo -e "${YELLOW}Warning: $*${NC}" >&2
}

echo_info() {
    echo -e "${GREEN}$*${NC}"
}

usage() {
  cat << EOF
Usage: $0 --source <path> --size <GB> --output <path> [--verify-script <path>] [-h|--help]

Creates an encrypted .sparsebundle disk image from a source directory.
See script comments for full documentation.

Mandatory arguments:
  --source <path>       Path to the existing source directory.
  --size <GB>           Maximum size of the disk image in gigabytes.
  --output <path>       Full path for the output .sparsebundle image bundle.

Optional arguments:
  --verify-script <path> Path to a script (like dir-diff.sh) to verify contents after creation.
  -h, --help            Display this help message.
EOF
  exit 1
}

# --- Argument Parsing --- 
SOURCE_DIR=""
IMAGE_SIZE_GB=""
OUTPUT_PATH=""
VERIFY_SCRIPT=""

# Use getopt for more robust parsing
# Check if getopt is available and supports long options (GNU version usually)
if ! getopt --test > /dev/null ; then echo_err "Enhanced getopt not available. Cannot parse options."; exit 1; fi
TEMP=$(getopt -o h --long help,source:,size:,output:,verify-script: -n '$0' -- "$@")
if [ $? != 0 ] ; then echo_err "Terminating... failed to parse options." ; usage ; fi

# Note the quotes around \"$TEMP\": they are essential!
eval set -- "$TEMP"

while true; do
  case "$1" in
    --source )
      SOURCE_DIR="$2"; shift 2 ;;
    --size )
      IMAGE_SIZE_GB="$2"; shift 2 ;;
    --output )
      OUTPUT_PATH="$2"; shift 2 ;;
    --verify-script )
      VERIFY_SCRIPT="$2"; shift 2 ;;
    -h | --help )
      usage; exit 0 ;;
    -- ) shift; break ;; # End of options
    * ) echo_err "Internal error!"; exit 1 ;; 
 esac
done

# --- Validation --- 
if [[ -z "$SOURCE_DIR" || -z "$IMAGE_SIZE_GB" || -z "$OUTPUT_PATH" ]]; then
  echo_err "Missing one or more mandatory arguments: --source, --size, --output"
  usage
fi

# Resolve ~ in source path
SOURCE_DIR="$(cd "$(dirname "$SOURCE_DIR")"; pwd)/$(basename "$SOURCE_DIR")"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo_err "Source directory '$SOURCE_DIR' not found or is not a directory."
  exit 1
fi

if ! [[ "$IMAGE_SIZE_GB" =~ ^[1-9][0-9]*$ ]]; then
    echo_err "Image size '$IMAGE_SIZE_GB' must be a positive integer."
    exit 1
fi

# Resolve ~ in output path
OUTPUT_DIR=$(dirname "$OUTPUT_PATH")
OUTPUT_BASE=$(basename "$OUTPUT_PATH")
if [[ "$OUTPUT_DIR" == "~"* ]]; then
    OUTPUT_DIR="$HOME/${OUTPUT_DIR#\~}"
fi
if [[ ! -d "$OUTPUT_DIR" ]]; then
    echo "Output directory '$OUTPUT_DIR' does not exist. Attempting to create it..."
    if ! mkdir -p "$OUTPUT_DIR"; then
        echo_err "Failed to create output directory '$OUTPUT_DIR'."
        exit 1
    fi
    echo_info "Output directory created."
fi
OUTPUT_PATH="$(cd "$OUTPUT_DIR"; pwd)/$OUTPUT_BASE"


if [[ -e "$OUTPUT_PATH" ]]; then
  echo_err "Output path '$OUTPUT_PATH' already exists. Please remove it or choose a different path."
  exit 1
fi

# Ensure output path ends with .sparsebundle
if [[ "$OUTPUT_PATH" != *.sparsebundle ]]; then
    echo_warn "Output path '$OUTPUT_PATH' does not end with .sparsebundle. Appending it."
    OUTPUT_PATH="${OUTPUT_PATH}.sparsebundle"
    if [[ -e "$OUTPUT_PATH" ]]; then
        echo_err "Corrected output path '$OUTPUT_PATH' already exists. Please remove it or choose a different path."
        exit 1
    fi
fi

if [[ -n "$VERIFY_SCRIPT" ]]; then
    # Resolve ~ in verify script path
    if [[ "$VERIFY_SCRIPT" == "~"* ]]; then
        VERIFY_SCRIPT="$HOME/${VERIFY_SCRIPT#\~}"
    fi
    if [[ ! -x "$VERIFY_SCRIPT" ]]; then
        echo_err "Verification script '$VERIFY_SCRIPT' not found or not executable."
        exit 1
    fi
    # Check for xpath command needed for verification
    if ! command -v xpath > /dev/null; then
        echo_err "Verification requires the 'xpath' command (usually from xmllint). Please install it."
        echo_warn "Proceeding without verification enabled."
        VERIFY_SCRIPT=""
    fi
fi

# Derive volume name from output path
VOLUME_NAME=$(basename "$OUTPUT_PATH" .sparsebundle)
if [[ -z "$VOLUME_NAME" ]]; then
    echo_err "Could not derive volume name from output path '$OUTPUT_PATH'."
    exit 1
fi

# --- Password Handling --- 
PASSWORD=""
PASSWORD_CONFIRM=""

echo "Please enter a password for the new encrypted image '$VOLUME_NAME'."
while [[ -z "$PASSWORD" ]]; do
    read -s -p "Password: " PASSWORD
    echo
    if [[ -z "$PASSWORD" ]]; then
        echo_warn "Password cannot be empty."
    fi
done

while [[ -z "$PASSWORD_CONFIRM" ]]; do
    read -s -p "Confirm Password: " PASSWORD_CONFIRM
    echo
    if [[ -z "$PASSWORD_CONFIRM" ]]; then
        echo_warn "Confirmation password cannot be empty."
    fi
done

if [[ "$PASSWORD" != "$PASSWORD_CONFIRM" ]]; then
    echo_err "Passwords do not match."
    exit 1
fi
echo_info "Password confirmed."

# --- Confirmation --- 
echo
echo "-----------------------------------------------------"
echo " ${BOLD}Parameters Summary:${NC}"
echo "   Source Directory: $SOURCE_DIR"
echo "   Image Max Size:   ${IMAGE_SIZE_GB} GB"
echo "   Output Image:     $OUTPUT_PATH"
echo "   Volume Name:      $VOLUME_NAME"
echo "   Encryption:       AES-256"
if [[ -n "$VERIFY_SCRIPT" ]]; then
    echo "   Verification:     ${GREEN}Enabled${NC} (using $VERIFY_SCRIPT)"
else
    echo "   Verification:     ${YELLOW}Disabled${NC}"
fi
echo "-----------------------------------------------------"
read -p "${BOLD}Proceed with image creation? (y/N): ${NC}" confirm
if [[ ! "$confirm" =~ ^[Yy]([Ee][Ss])?$ ]]; then
    echo "Operation cancelled by user."
    exit 0
fi

# --- Image Creation --- 
echo "Creating encrypted sparse bundle image... (This may take time for large sources)"
# Use -stdinpass to provide the password securely
if ! echo "$PASSWORD" | hdiutil create -encryption AES-256 -size "${IMAGE_SIZE_GB}g" -fs APFS -type SPARSEBUNDLE -volname "$VOLUME_NAME" -srcfolder "$SOURCE_DIR" -stdinpass "$OUTPUT_PATH"; then
    echo_err "Failed to create disk image."
    # Attempt to clean up potentially incomplete output file
    rm -rf "$OUTPUT_PATH" > /dev/null 2>&1 || true
    exit 1
fi
echo_info "Disk image created successfully: $OUTPUT_PATH"

# --- Verification (Optional) --- 
MOUNT_POINT=""
VERIFICATION_PASSED=1 # Default to true (passed) if verification is skipped

if [[ -n "$VERIFY_SCRIPT" ]]; then
    echo "Attempting to attach image for verification..."
    # Use -mountrandom /tmp to avoid polluting /Volumes and handle name conflicts
    # Capture the plist output
    MOUNT_INFO_PLIST=$(hdiutil attach "$OUTPUT_PATH" -mountrandom /tmp -nobrowse -plist)
    attach_exit_code=$?
    if [ $attach_exit_code -ne 0 ]; then
        echo_err "Failed to attach disk image '$OUTPUT_PATH' for verification (exit code $attach_exit_code)."
        exit 1
    fi

    # Extract mount point using xpath on the plist output
    # Requires xmllint or similar xpath tool to be installed
    # Using simple grep/sed fallback if xpath fails or isn't installed
    if command -v xpath > /dev/null; then
         MOUNT_POINT=$(echo "$MOUNT_INFO_PLIST" | xpath -e "//dict/key[.='mount-point']/following-sibling::string[1]/text()" - 2>/dev/null)
    fi
    # Fallback or if xpath yielded nothing
    if [[ -z "$MOUNT_POINT" ]]; then
        MOUNT_POINT=$(echo "$MOUNT_INFO_PLIST" | grep -A1 -E '<key>mount-point</key>' | grep -E '<string>.*</string>' | sed -E 's/.*<string>(.*)<\/string>/\1/')
    fi

    if [[ -z "$MOUNT_POINT" || ! -d "$MOUNT_POINT" ]]; then
        echo_err "Could not determine mount point after attaching image '$OUTPUT_PATH'. Cannot verify."
        # Attempt cleanup using device path if possible
        DEV_PATH=$(echo "$MOUNT_INFO_PLIST" | grep -A1 -E '<key>dev-entry</key>' | grep -E '<string>.*</string>' | sed -E 's/.*<string>(.*)<\/string>/\1/')
        [[ -n "$DEV_PATH" ]] && hdiutil detach "$DEV_PATH" -force >/dev/null 2>&1 || true 
       exit 1
    fi
    echo_info "Image mounted for verification at: $MOUNT_POINT"

    echo "Running verification script: $VERIFY_SCRIPT \"$SOURCE_DIR\" \"$MOUNT_POINT\""
    if "$VERIFY_SCRIPT" "$SOURCE_DIR" "$MOUNT_POINT"; then
        echo_info "Verification script indicates source and image contents are identical."
        VERIFICATION_PASSED=1
    else
        echo_err "Verification script indicates differences between source and image contents (exit code $?)."
        VERIFICATION_PASSED=0
    fi

    echo "Detaching verification volume..."
    if ! hdiutil detach "$MOUNT_POINT" -force; then
        echo_warn "Could not cleanly detach verification volume '$MOUNT_POINT'. You may need to force eject it manually via Finder or Disk Utility."
        # Don't exit here, but warn the user
    fi

    if [ $VERIFICATION_PASSED -eq 0 ]; then
        echo_err "Verification failed. The original source directory '$SOURCE_DIR' will NOT be deleted."
        exit 1
    fi
fi # End verification block

# --- Source Deletion --- 
echo
echo_warn "The encrypted image has been created${VERIFICATION_PASSED:+ and verified}."
read -p "${BOLD}${RED}WARNING:${NC} Delete the original source directory '$SOURCE_DIR' permanently? (y/N): " del_confirm
if [[ "$del_confirm" =~ ^[Yy]([Ee][Ss])?$ ]]; then
    echo "Deleting original source directory: $SOURCE_DIR ..."
    if rm -rf "$SOURCE_DIR"; then
        echo_info "Original source directory deleted."
    else
        echo_err "Failed to delete original source directory '$SOURCE_DIR'. Please delete it manually."
        exit 1 # Exit with error if deletion fails
    fi
else
    echo "Original source directory '$SOURCE_DIR' was NOT deleted."
fi

echo
echo_info "Operation completed successfully."
exit 0 