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

    return colorschemes

def create_temp_vimrc(colorschemes, current_group):
    """
    Creates a temporary .vimrc file to open nine split windows, each with a different colorscheme from the current group.
    """
    temp_vimrc = tempfile.NamedTemporaryFile(mode="w", delete=False, prefix="temp_vimrc_")

    # Vim commands to split the window and set colorschemes
    vimrc_content = f"""
    set background=dark
    syntax on
    set laststatus=0 " Hide status bar for cleaner look
    set noruler " Hide ruler
    set number " Show line number
    set cursorline " Highlight current line
    set nofoldenable " Disable folding

    " Open 9 windows
    vsplit
    vsplit
    wincmd h " Move to the left window
    split
    split
    wincmd j " Move to the bottom window
    vsplit
    vsplit
    wincmd h " Move to the left window
    split
    split
    wincmd k " Move to the top window

    " Display colorscheme names as messages
    echo "Colorschemes in this group: {", ".join(current_group)}"

    " Set colorschemes in each window (up to 9)
    """
    for i, colorscheme in enumerate(current_group):
      vimrc_content += f"""
          exe {i+1} . "wincmd w" " Move to window {i+1}
          silent! colorscheme {colorscheme}
          sleep 50m " Introduce a small delay
          """

    temp_vimrc.write(vimrc_content)
    temp_vimrc.close()
    return temp_vimrc.name

def open_vim_with_colorschemes(filepath, temp_vimrc_path):
    """Opens Vim with the specified file and temporary .vimrc."""
    try:
        subprocess.run(
            ["vim", "-u", temp_vimrc_path, filepath],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error opening Vim: {e}")

def main():
    """Main function to run the colorscheme visualizer."""
    filepath_input = input("Enter the path to the file you want to open in Vim: ")
    filepath = Path(filepath_input)

    if filepath.is_absolute():
        pass
    elif str(filepath).startswith("~"):
        filepath = Path.home() / str(filepath)[2:]
    else:
        filepath = Path.cwd() / filepath

    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return

    colorschemes = get_installed_colorschemes()

    if not colorschemes:
        print("No Vim colorschemes found.")
        return

    # Iterate in groups of 9
    for i in range(0, len(colorschemes), 9):
        current_group = colorschemes[i:i+9]
        print(f"Displaying colorschemes: {', '.join(current_group)}")

        temp_vimrc_path = create_temp_vimrc(colorschemes, current_group)
        open_vim_with_colorschemes(str(filepath), temp_vimrc_path)
        os.unlink(temp_vimrc_path)  # Clean up the temporary .vimrc

        # Ask the user if they want to continue
        user_input = input("Press Enter to continue to the next group (or type 'q' to quit): ")
        if user_input.lower() == 'q':
            break

if __name__ == "__main__":
    main()
