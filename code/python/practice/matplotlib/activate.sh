#!/bin/bash
# Quick activation script for matplotlib practice exercises
# Usage: source activate.sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/venv/bin/activate"

echo "✅ Virtual environment activated!"
echo ""
echo "Quick commands:"
echo "  python run_exercises.py --list    # List all exercises"
echo "  python run_exercises.py 1         # Run exercise 1"
echo "  python ex01_basic_line_plots.py   # Run file directly"
echo ""
echo "💡 Tip: You can also use ./run.sh without activating:"
echo "  ./run.sh --list"
echo "  ./run.sh 1"
echo ""
