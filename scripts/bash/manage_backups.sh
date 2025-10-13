#!/bin/bash

# --- Configuration ---
# Add all your backup locations to this array.
BACKUP_DIRS=(
    "$HOME/backups"
    "$HOME/Library/Mobile Documents/com~apple~CloudDocs"
    "$HOME/Library/CloudStorage/OneDrive-SAPSE"
)

# --- Helper Function ---

# This function finds and sorts backup files for a SINGLE directory.
# It's called by the list and delete functions.
# Argument: $1 - The directory to search in.
# Output: A sorted list of "YYYYMMDD /path/to/file.tar.bz2"
get_sorted_backups_for_dir() {
    local search_dir="$1"
    # -maxdepth 1 prevents find from going into subdirectories.
    find "$search_dir" -maxdepth 1 -type f -name "*.tar.bz2" -print0 | while IFS= read -r -d '' file; do
        local filename
        filename=$(basename "$file")
        
        # Parse date and convert to 20YYMMDD for sorting.
        local date_str
        date_str=$(echo "$filename" | awk -F'[_.]' '{
            if (NF > 4) {
                day=$(NF-4); month=$(NF-3); year=$(NF-2);
                if (year ~ /^[0-9]{2}$/ && month ~ /^[0-9]{2}$/ && day ~ /^[0-9]{2}$/) {
                    printf "20%s%s%s\n", year, month, day
                }
            }
        }')
        
        if [[ -n "$date_str" ]]; then
            echo "$date_str $file"
        fi
    done | sort -nr # Sort newest first.
}

# --- Script Actions ---

# List the 'n' newest files from EACH backup location.
list_backups() {
    local num_files=${1:-10}
    echo "🔍 Listing the ${num_files} most recent backups from each location:"
    echo "=================================================="

    for dir in "${BACKUP_DIRS[@]}"; do
        echo "--- Location: $dir ---"
        if [ ! -d "$dir" ] || [ ! -r "$dir" ]; then
            echo "Warning: Directory not found or not readable."
        else
            local files_found
            files_found=$(get_sorted_backups_for_dir "$dir" | head -n "$num_files" | cut -d' ' -f2-)
            
            if [ -n "$files_found" ]; then
                echo "$files_found"
            else
                echo "No matching backup files found here."
            fi
        fi
        echo # Add a blank line for readability
    done
    echo "=================================================="
}

# Delete the 'n' oldest files from EACH backup location.
delete_backups() {
    local num_files=${1:-10}

    if ! [[ "$num_files" =~ ^[1-9][0-9]*$ ]]; then
        echo "❌ Error: Please provide a valid positive number of files to delete."
        exit 1
    fi

    echo "🗑️ Finding the ${num_files} oldest files from EACH location..."
    
    local all_files_to_delete=""

    # Loop through each directory to find the oldest files within it.
    for dir in "${BACKUP_DIRS[@]}"; do
        if [ -d "$dir" ] && [ -r "$dir" ]; then
            local oldest_in_dir
            # Use `tail` to get the oldest files from the sorted list for this dir.
            oldest_in_dir=$(get_sorted_backups_for_dir "$dir" | tail -n "$num_files" | cut -d' ' -f2-)
            
            if [ -n "$oldest_in_dir" ]; then
                all_files_to_delete+="$oldest_in_dir"$'\n'
            fi
        fi
    done

    # Trim trailing newline
    all_files_to_delete=$(echo "$all_files_to_delete" | sed '/^$/d')

    if [ -z "$all_files_to_delete" ]; then
        echo "✅ No matching backup files were found to delete."
        exit 0
    fi

    echo "The following files will be PERMANENTLY DELETED:"
    echo "--------------------------------------------------"
    echo "$all_files_to_delete"
    echo "--------------------------------------------------"

    read -p "Are you sure you want to delete these files? (y/N) " confirm
    if [[ "$confirm" =~ ^[yY]([eE][sS])?$ ]]; then
        echo "🔥 Deleting files..."
        echo "$all_files_to_delete" | while IFS= read -r file; do
            rm -v "$file"
        done
        echo "✅ Deletion complete."
    else
        echo "🚫 Deletion cancelled."
    fi
}

# --- Main Logic ---
ACTION=${1:-list}
NUM_FILES=${2}

case "$ACTION" in
    list)
        list_backups "$NUM_FILES"
        ;;
    delete)
        delete_backups "$NUM_FILES"
        ;;
    *)
        echo "Usage: $(basename "$0") [action] [number]"
        echo ""
        echo "Actions:"
        echo "  list [n]      Lists the 'n' newest files from each location (default: 10)."
        echo "  delete [n]    Deletes the 'n' oldest files from each location (default: 10)."
        exit 1
        ;;
esac
