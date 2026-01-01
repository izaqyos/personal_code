# Installation Guide

## Quick Setup (macOS)

The easiest way to set up Repo Cleaner on macOS:

```bash
cd /Users/yosii/work/git/personal_code/code/python/tools/repo_cleaner
./setup.sh
```

This will:
1. Create a virtual environment in `venv/`
2. Install all dependencies
3. Install repo-cleaner in development mode

## Manual Setup

If you prefer to set up manually:

### 1. Create Virtual Environment

```bash
cd /Users/yosii/work/git/personal_code/code/python/tools/repo_cleaner
python3 -m venv venv
```

### 2. Activate Virtual Environment

```bash
source venv/bin/activate
```

You should see `(venv)` in your prompt.

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -e .
```

### 4. Verify Installation

```bash
repo-cleaner --version
repo-cleaner --help
```

## Usage

### Activate Environment

Every time you want to use repo-cleaner, activate the virtual environment first:

```bash
cd /Users/yosii/work/git/personal_code/code/python/tools/repo_cleaner
source venv/bin/activate
```

### Run Commands

```bash
# Show help
repo-cleaner --help

# Dry run (preview)
repo-cleaner -n

# Clean current directory
repo-cleaner

# Clean specific directory
repo-cleaner -t ~/projects/myapp

# Force mode (no prompts)
repo-cleaner -f

# Clean only Python
repo-cleaner -l python
```

### Deactivate Environment

When done:

```bash
deactivate
```

## Alternative: Using pipx (Recommended for System-wide Install)

If you want to use repo-cleaner system-wide without activating a venv each time:

```bash
# Install pipx if not already installed
brew install pipx
pipx ensurepath

# Install repo-cleaner
cd /Users/yosii/work/git/personal_code/code/python/tools/repo_cleaner
pipx install -e .

# Now you can use it from anywhere
repo-cleaner --help
```

## Troubleshooting

### "command not found: pip"

Use `pip3` instead of `pip`:
```bash
pip3 install -e .
```

### "externally-managed-environment"

This is macOS protecting the system Python. Use one of these solutions:

**Option 1: Virtual Environment (Recommended)**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

**Option 2: pipx (For system-wide install)**
```bash
brew install pipx
pipx install -e .
```

**Option 3: --user flag (Not recommended)**
```bash
pip3 install --user -e .
```

### "ModuleNotFoundError: No module named 'click'"

You're trying to run the script directly without installing dependencies. Use one of:

**Option 1: Install in venv (Recommended)**
```bash
./setup.sh
source venv/bin/activate
repo-cleaner
```

**Option 2: Install dependencies manually**
```bash
python3 -m venv venv
source venv/bin/activate
pip install click pyyaml
python3 -m repo_cleaner.main
```

### Running from Source Without Install

If you want to run without installing:

```bash
# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install click pyyaml

# Run as module
python3 -m repo_cleaner.main --help

# Or run script directly
python3 repo_cleaner/main.py --help
```

## Development Setup

For development with all tools:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check .

# Type check
mypy repo_cleaner
```

