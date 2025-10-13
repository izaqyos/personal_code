Remove old backup files 

prompt: I have a script that creates backup files at three locations. 1. /Users/i500695/backups/ 2.  /Users/i500695/Library/Mobile Documents/com~apple~CloudDocs/  3. /Users/i500695/Library/CloudStorage/OneDrive-SAPSE . help me create a python script that accepts an argument n - for number of files to keep. The script then keeps the n most recent files. Then it prints the rest of the files and ask for confirmation whether its ok to delete them. If the input is y for yes then the remaining, older, files are deleted

Response:
Here’s how we can approach this task step-by-step:

Plan:

	1.	Function to List Files:
	•	For each of the three directories, gather all files.
	•	Sort them by modification time.
	2.	Keep Most Recent Files:
	•	Keep the most recent n files and separate the rest for potential deletion.
	3.	Display Files to Delete:
	•	Print the older files that are subject to deletion and ask the user for confirmation.
	4.	Delete Files:
	•	If the user confirms, delete the older files.
	5.	Error Handling:
	•	Handle any potential errors (e.g., permissions issues, file not found).

Pseudocode:

	1.	Define the directories in a list.
	2.	Create a function to list and sort files in each directory.
	3.	Prompt the user for confirmation on which files to delete.
	4.	Delete the files if the user confirms.

Full Python Script:

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
        
        print(f"\nThe following {len(files_to_delete)} files will be deleted from {backup_dir}:")
        for file in files_to_delete:
            print(f"- {file} (Last modified: {time.ctime(file.stat().st_mtime)})")
        
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

How It Works:

	1.	get_files_sorted_by_mtime(directory):
	•	Lists all files in the given directory and sorts them by modification time, with the newest files first.
	2.	cleanup_backup_files(n):
	•	Loops through the list of backup directories.
	•	Checks if each directory exists and gathers the files.
	•	If the number of files is greater than n, it displays the older files and asks for confirmation to delete them.
	•	Deletes files if the user confirms.
	3.	delete_files(files_to_delete):
	•	Deletes the specified list of files, with error handling for file deletion errors.

Next Steps:

a. Would you like to add more specific logging or error handling to make the script more robust?

b. Should I help create a test suite to ensure this script handles different edge cases, like empty directories or permission errors?
