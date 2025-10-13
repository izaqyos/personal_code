#!/bin/bash

# === Documentation ===
# Script: create-empty-vault.sh
#
# Purpose:
#   Creates a new, *empty*, encrypted APFS sparse disk image on macOS.
#   This provides a secure, password-protected location to store files,
#   which can be mounted like a regular volume when needed.
#
# How it Works:
#   1.  Argument Parsing: Parses command-line arguments for the desired image
#       size (in GB) and the output path for the `.sparseimage`.
#   2.  Input Validation:
#       - Ensures mandatory arguments (`--size`, `--output`) are provided.
#       - Validates that the specified size is a positive number.
#       - Ensures the intended output path for the `.sparseimage` does not
#         already exist to prevent accidental overwrites.
#   3.  Password Handling: Securely prompts the user to enter and confirm a
#       password for the encrypted image.
#   4.  Confirmation: Displays parameters and asks for confirmation before creation.
#   5.  Image Creation: Executes `hdiutil create` using AES-256 encryption, APFS,
#       and sparse format to create an empty image container.
#   6.  Completion: Reports success or failure.
#
# Parameters:
#   --size <GB>           (Mandatory) Max size of the disk image in gigabytes (e.g., `50`).
#   --output <path>       (Mandatory) Full path for the output `.sparseimage` image file.
#   -h, --help            Display usage information.
#
# Prerequisites:
#   - macOS operating system.
#   - `hdiutil` command-line tool (built-in).
#
# Usage Example:
#   ./create-empty-vault.sh --size 50 --output ~/Documents/MySecureData.sparseimage
#
# After Creation:
#   - Mount: `hdiutil attach ~/Documents/MySecureData.sparseimage` (prompts for password)
#   - Access: Volume appears in Finder and at `/Volumes/MySecureData` (or similar)
#   - Unmount: `hdiutil detach /Volumes/MySecureData` or Eject in Finder
#
# Caveats:
#   - Script refuses to overwrite an existing output file.
#   - Lost passwords mean lost data. Use a strong, memorable password.
#   - Uses sparse format which only consumes disk space as needed, up to the maximum size.
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
Usage: $0 --size <GB> --output <path> [-h|--help]

Creates a new, empty, encrypted sparse disk image.
See script comments for full documentation.

Mandatory arguments:
  --size <GB>           Maximum size of the disk image in gigabytes.
  --output <path>       Full path for the output sparse image file.

Optional arguments:
  -h, --help            Display this help message.
EOF
  exit 1
}

# --- Argument Parsing ---
IMAGE_SIZE_GB=""
OUTPUT_PATH=""

while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --size)
      IMAGE_SIZE_GB="$2"
      shift # past argument
      shift # past value
      ;;
    --output)
      OUTPUT_PATH="$2"
      shift # past argument
      shift # past value
      ;;
    -h|--help)
      usage
      ;;
    *)
      # Unknown option
      echo_err "Unknown option: $1"
      usage
      ;;
  esac
done

# --- Validation ---
if [[ -z "$IMAGE_SIZE_GB" || -z "$OUTPUT_PATH" ]]; then
  echo_err "Missing one or more mandatory arguments: --size, --output"
  usage
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

# Ensure output path ends with .sparseimage
if [[ "$OUTPUT_PATH" == *.sparsebundle ]]; then
    OUTPUT_PATH="${OUTPUT_PATH%.sparsebundle}.sparseimage"
    echo_info "Changed output format to .sparseimage for better encryption: $OUTPUT_PATH"
elif [[ "$OUTPUT_PATH" == *.dmg ]]; then
    OUTPUT_PATH="${OUTPUT_PATH%.dmg}.sparseimage"
    echo_info "Changed output format to .sparseimage for sparse allocation: $OUTPUT_PATH"
elif [[ "$OUTPUT_PATH" != *.sparseimage ]]; then
    echo_warn "Output path '$OUTPUT_PATH' does not end with .sparseimage. Appending it."
    OUTPUT_PATH="${OUTPUT_PATH}.sparseimage"
fi

if [[ -e "$OUTPUT_PATH" ]]; then
    echo_err "Corrected output path '$OUTPUT_PATH' already exists. Please remove it or choose a different path."
    exit 1
fi

# Derive volume name from output path
VOLUME_NAME=$(basename "$OUTPUT_PATH" .sparseimage)
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
echo "   Image Max Size:   ${IMAGE_SIZE_GB} GB"
echo "   Output Image:     $OUTPUT_PATH"
echo "   Volume Name:      $VOLUME_NAME"
echo "   Encryption:       AES-256 (full disk encryption)"
echo "   Format:           Sparse (only uses space as needed)"
echo "   Initial Content:  Empty"
echo "-----------------------------------------------------"
read -p "${BOLD}Proceed with empty image creation? (y/N): ${NC}" confirm
if [[ ! "$confirm" =~ ^[Yy]([Ee][Ss])?$ ]]; then
    echo "Operation cancelled by user."
    exit 0
fi

# --- Image Creation ---
echo "Creating empty encrypted sparse disk image..."
# Use -stdinpass to provide the password securely
# Use SPARSE format for efficient space usage
if ! printf "%s" "$PASSWORD" | hdiutil create \
    -encryption AES-256 \
    -size "${IMAGE_SIZE_GB}g" \
    -fs APFS \
    -volname "$VOLUME_NAME" \
    -stdinpass \
    -type SPARSE \
    "$OUTPUT_PATH"; then
    echo_err "Failed to create disk image."
    # Attempt to clean up potentially incomplete output file
    rm -f "$OUTPUT_PATH" > /dev/null 2>&1 || true
    exit 1
fi

echo_info "Empty encrypted sparse image created successfully: $OUTPUT_PATH"
echo_info "This image will only use disk space as needed, up to ${IMAGE_SIZE_GB}GB."
echo "You can now attach it using: hdiutil attach '$OUTPUT_PATH'"
exit 0 