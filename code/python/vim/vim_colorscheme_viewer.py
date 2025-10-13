#!/usr/bin/env python3
import os
import subprocess
import tempfile
from pathlib import Path

def get_installed_colorschemes():
    """
    Gets a list of installed Vim colorschemes, prioritizing ~/.vim.
    """

    colorschemes = []

    # Prioritize ~/.vim and other custom directories
    custom_colorscheme_dirs = [
        os.path.expanduser("~/.vim/colors"),
        os.path.expanduser("~/.config/nvim/colors"),  # For Neovim users
        # Add any other custom directories here
    ]

    for colors_dir in custom_colorscheme_dirs:
        if os.path.exists(colors_dir):
            for filename in os.listdir(colors_dir):
                if filename.endswith(".vim"):
                    colorscheme_name = filename[:-4]  # Remove .vim extension
                    colorschemes.append(colorscheme_name)

    # If no colorschemes found in custom dirs, check MacVim's runtime (optional)
    if not colorschemes:
        print("No colorschemes found in custom directories. Checking MacVim runtime...")
        vimruntime = "/Applications/MacVim.app/Contents/Resources/vim/runtime"  # You can make this configurable if needed
        if os.path.exists(vimruntime):
            colors_dir = os.path.join(vimruntime, "colors")
            if os.path.exists(colors_dir):
                for filename in os.listdir(colors_dir):
                    if filename.endswith(".vim"):
                        colorscheme_name = filename[:-4]
                        colorschemes.append(colorscheme_name)

    return colorschemes


def create_temp_vimrc(colorscheme):
    """Creates a temporary .vimrc file with the specified colorscheme."""
    temp_vimrc = tempfile.NamedTemporaryFile(mode="w", delete=False, prefix="temp_vimrc_")
    temp_vimrc.write(f"colorscheme {colorscheme}\n")
    temp_vimrc.write("set background=dark\n")  # You can adjust this if needed
    temp_vimrc.write("syntax on\n")
    temp_vimrc.close()
    return temp_vimrc.name

def open_vim_with_colorscheme(filepath, temp_vimrc_path):
    """Opens Vim with the specified file and temporary .vimrc."""
    try:
        subprocess.run(
            ["vim", "-u", temp_vimrc_path, filepath],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error opening Vim: {e}")

def display_colorschemes(filepath):
    """Displays different Vim colorschemes for the given file."""
    colorschemes = get_installed_colorschemes()

    if not colorschemes:
        print("No Vim colorschemes found.")
        return

    for colorscheme in colorschemes:
        print(f"Displaying colorscheme: {colorscheme}")
        temp_vimrc_path = create_temp_vimrc(colorscheme)
        open_vim_with_colorscheme(filepath, temp_vimrc_path)
        os.unlink(temp_vimrc_path)  # Clean up the temporary .vimrc

        # Ask the user if they want to continue
        user_input = input("Press Enter to continue to the next colorscheme (or type 'q' to quit): ")
        if user_input.lower() == 'q':
            break

def main():
    """Main function to run the colorscheme visualizer."""
    filepath_input = input("Enter the path to the file you want to open in Vim: ")
    filepath = Path(filepath_input)

    if filepath.is_absolute():
        # filepath already absolute. Nothing to do.
        pass
    elif str(filepath).startswith("~"):
        # relative path with home directory
        filepath = Path.home() / str(filepath)[2:]
    else:
        # relative path, make it absolute
        filepath = Path.cwd() / filepath

    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return

    display_colorschemes(str(filepath))

if __name__ == "__main__":
    main()
