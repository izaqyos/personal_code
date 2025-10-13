#!/opt/homebrew/bin/python3

import os
import time
from pathlib import Path

# Directories to check
backup_dirs = [
    "/Users/i500695/backups/",
    "/Users/i500695/Library/Mobile Documents/com~apple~CloudDocs/",
    "/Users/i500695/Library/CloudStorage/OneDrive-SAPSE/"
]

def get_files_sorted_by_mtime(directory):
    """Return a list of files in the directory, sorted by modification time (newest first)."""
    files = list(Path(directory).glob('*'))  # List all files
    files = [f for f in files if f.is_file()]  # Filter out only files
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)  # Sort by modification time
    return files

def delete_files(files_to_delete):
    """Delete the given list of files."""
    for file in files_to_delete:
        try:
            file.unlink()  # Deletes the file
            print(f"Deleted {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")

def cleanup_backup_files(n):
    """Main function to handle the backup cleanup logic."""
    for backup_dir in backup_dirs:
        if not os.path.exists(backup_dir):
            print(f"Directory {backup_dir} does not exist, skipping.")
            continue
        
        print(f"\nChecking directory: {backup_dir}")
        files = get_files_sorted_by_mtime(backup_dir)
        
        if len(files) <= n:
            print(f"Directory {backup_dir} has {len(files)} files, which is less than or equal to {n}. Nothing to delete.")
            continue
        
        files_to_keep = files[:n]  # Keep the n most recent files
        files_to_delete = files[n:]  # Files to potentially delete
        
        print('-'*80)
        print(f"\nThe following {len(files_to_delete)} files will be deleted from {backup_dir}:")
        for file in files_to_delete:
            print(f"- deleting {file} (Last modified: {time.ctime(file.stat().st_mtime)})")
        print('-'*80)
        print(f"\nThe following {len(files_to_keep)} files will be kept at {backup_dir}:")
        for file in files_to_keep:
            print(f"- keeping {file} (Last modified: {time.ctime(file.stat().st_mtime)})")
        print('-'*80)
        
        # Ask for user confirmation
        confirm = input("Do you want to delete these files? (y/n): ").strip().lower()
        if confirm == 'y':
            delete_files(files_to_delete)
        else:
            print(f"Skipping deletion in {backup_dir}.")

if __name__ == "__main__":
    # Accept number of files to keep as an argument
    n = int(input("Enter the number of recent files to keep: "))
    cleanup_backup_files(n)
