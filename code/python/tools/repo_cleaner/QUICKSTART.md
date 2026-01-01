# Quick Start Guide

## Setup (One-time)

Run the setup script:

```bash
cd /Users/yosii/work/git/personal_code/code/python/tools/repo_cleaner
./setup.sh
```

This creates a virtual environment and installs all dependencies.

## Daily Usage

### 1. Activate the environment

```bash
cd /Users/yosii/work/git/personal_code/code/python/tools/repo_cleaner
source venv/bin/activate
```

You'll see `(venv)` in your prompt.

### 2. Run repo-cleaner

```bash
# Preview what would be cleaned (safe)
repo-cleaner -n

# Clean current directory (interactive)
repo-cleaner

# Clean specific directory
repo-cleaner -t ~/projects/myapp

# Force mode (no prompts)
repo-cleaner -f

# Clean only Python artifacts
repo-cleaner -l python

# Clean Python and Node
repo-cleaner -l python,node
```

### 3. Monorepo Support

```bash
# Scan and preview a monorepo
repo-cleaner -t ~/monorepo -n

# Clean with per-project prompts
repo-cleaner -t ~/monorepo

# Clean all without prompts
repo-cleaner -t ~/monorepo -f

# Force rescan (ignore cached layout)
repo-cleaner -t ~/monorepo --rescan

# View cleanup history
repo-cleaner --history
```

### 4. Deactivate when done

```bash
deactivate
```

## Common Commands

```bash
# See all options
repo-cleaner --help

# List supported languages
repo-cleaner --list-languages

# Dry run with verbose output
repo-cleaner -n -v

# Clean excluding certain directories
repo-cleaner -e "vendor/**" -e "important_build/**"

# View recent cleanup history
repo-cleaner --history

# Version info
repo-cleaner --version
```

## How Monorepo Cleaning Works

1. **Scan**: Recursively finds all projects in subdirectories
2. **Cache**: Saves layout to `~/.config/repo_cleaner/layouts/` (24h cache)
3. **Confirm**: Asks per-project (unless `-f` flag used)
4. **Clean**: Iteratively cleans each project
5. **Report**: Saves report to `~/.config/repo_cleaner/history.json`

## Troubleshooting

If you get "command not found: repo-cleaner", make sure:
1. You activated the venv: `source venv/bin/activate`
2. You ran the setup: `./setup.sh`

If setup fails, see [INSTALL.md](INSTALL.md) for detailed instructions.

