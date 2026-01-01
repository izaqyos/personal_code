#!/bin/bash
# Setup script for Repo Cleaner on macOS

set -e

echo "Setting up Repo Cleaner..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "Error: Please run this script from the repo_cleaner directory"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install the package in editable mode
echo "Installing repo-cleaner in development mode..."
pip install -e .

echo ""
echo "✓ Setup complete!"
echo ""
echo "To use repo-cleaner:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the tool:"
echo "     repo-cleaner --help"
echo "     repo-cleaner -n  # dry run"
echo ""
echo "  3. When done, deactivate:"
echo "     deactivate"

