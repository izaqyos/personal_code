#!/opt/homebrew/bin/python3
import os
import shutil
import argparse
from datetime import datetime

def move_recent_files(source_dir, target_dir, num_files):
    """Moves the n most recent files from source_dir to target_dir."""

    # Ensure directories exist and are accessible
    if not os.path.isdir(source_dir):
        raise FileNotFoundError(f"Source directory not found: {source_dir}")
    if not os.path.isdir(target_dir):
        raise FileNotFoundError(f"Target directory not found: {target_dir}")
    os.makedirs(target_dir, exist_ok=True)  # Create target dir if it doesn't exist

    # Get files and their modification times
    file_times = [(os.path.join(source_dir, f), os.path.getmtime(os.path.join(source_dir, f)))
                  for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

    # Sort by modification time (most recent first)
    file_times.sort(key=lambda x: x[1], reverse=True)

    # Move the n most recent files
    for i in range(min(num_files, len(file_times))):
        source_path = file_times[i][0]
        filename = os.path.basename(source_path)
        print(f"Moving: {filename}")
        target_path = os.path.join(target_dir, filename)
        
        # Handle potential file name conflicts
        base_name, extension = os.path.splitext(filename)
        counter = 1
        while os.path.exists(target_path):
            target_path = os.path.join(target_dir, f"{base_name}_{counter}{extension}")
            counter += 1

        shutil.move(source_path, target_path)
        print(f"Moved: {source_path} -> {target_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move recent files from source to target.")
    parser.add_argument("source_dir", help="Path to the source directory")
    parser.add_argument("target_dir", help="Path to the target directory")
    parser.add_argument("num_files", type=int, help="Number of files to move")
    args = parser.parse_args()

    move_recent_files(args.source_dir, args.target_dir, args.num_files)
