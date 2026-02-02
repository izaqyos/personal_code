#!/bin/bash
# Wrapper script to run exercises with the virtual environment
# Usage: ./run.sh [arguments for run_exercises.py]

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: python3 -m venv venv && ./venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Run with venv python
exec "$VENV_PYTHON" "$SCRIPT_DIR/run_exercises.py" "$@"
