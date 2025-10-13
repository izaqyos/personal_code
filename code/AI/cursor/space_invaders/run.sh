#!/bin/bash

# Space Invaders game runner script
# Provides a shell interface to run the game, tests, and get help

# Function to display usage
show_usage() {
    echo "Usage: ./run.sh [command]"
    echo
    echo "Commands:"
    echo "  game    - Run the Space Invaders game"
    echo "  test    - Run the game's test suite"
    echo "  help    - Show help information"
    echo "  clean   - Clean Python cache files"
    echo "  setup   - Set up the conda environment"
    echo
    echo "If no command is provided, 'help' will be shown."
}

# Function to clean Python cache files
clean_cache() {
    echo "Cleaning Python cache files..."
    find . -type d -name "__pycache__" -exec rm -r {} +
    find . -type f -name "*.pyc" -delete
    echo "Cache cleaned!"
}

# Function to set up conda environment
setup_environment() {
    echo "Setting up conda environment..."
    conda create -n space_invaders python=3.11 numpy -y
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate space_invaders
    pip install pygame
    echo "Environment setup complete!"
}

# Function to check if we're in the correct conda environment
check_environment() {
    # Initialize conda for shell script
    source "$(conda info --base)/etc/profile.d/conda.sh"
    
    if [[ "$CONDA_DEFAULT_ENV" != "space_invaders" ]]; then
        echo "Activating space_invaders environment..."
        if ! conda activate space_invaders; then
            echo "Error: Could not activate space_invaders environment"
            echo "Please run './run.sh setup' first to create the environment"
            exit 1
        fi
    fi
}

# Function to check if required packages are installed
check_packages() {
    if ! python -c "import pygame" 2>/dev/null; then
        echo "Installing required packages..."
        pip install pygame
    fi
}

# Check if conda is available
check_conda() {
    if ! command -v conda &> /dev/null; then
        echo "Error: conda is not installed or not in PATH"
        echo "Please install conda first: https://docs.conda.io/en/latest/miniconda.html"
        exit 1
    fi
}

# Main script logic
if [ $# -eq 0 ]; then
    show_usage
    exit 0
fi

case "$1" in
    "game")
        check_conda
        check_environment
        check_packages
        python run.py game
        ;;
    "test")
        check_conda
        check_environment
        check_packages
        python run.py test
        ;;
    "help")
        python run.py help
        ;;
    "clean")
        clean_cache
        ;;
    "setup")
        check_conda
        setup_environment
        ;;
    *)
        echo "Error: Unknown command '$1'"
        show_usage
        exit 1
        ;;
esac 