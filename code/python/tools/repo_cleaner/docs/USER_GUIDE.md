# Repo Cleaner User Guide

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Command Line Options](#command-line-options)
4. [Configuration](#configuration)
5. [Supported Languages](#supported-languages)
6. [Common Use Cases](#common-use-cases)
7. [Safety Features](#safety-features)
8. [Troubleshooting](#troubleshooting)

## Installation

### From Source

```bash
git clone https://github.com/repo-cleaner/repo-cleaner.git
cd repo-cleaner
pip install -e .
```

### With Optional Dependencies

```bash
# With color support
pip install -e ".[color]"

# With progress bars
pip install -e ".[progress]"

# All optional features
pip install -e ".[all]"
```

## Basic Usage

### Preview Mode (Dry Run)

Always start with a dry run to see what would be cleaned:

```bash
repo-cleaner -n
```

This shows all files and directories that would be deleted without actually deleting anything.

### Interactive Mode (Default)

Run without flags for interactive mode:

```bash
repo-cleaner
```

You'll be prompted to confirm before any deletion.

### Force Mode (Non-Interactive)

For scripting or CI/CD pipelines:

```bash
repo-cleaner -f
```

This skips all confirmations (but respects exclude patterns).

## Command Line Options

### Target Directory

```bash
# Clean current directory (default)
repo-cleaner

# Clean specific directory
repo-cleaner -t /path/to/project

# Clean multiple projects (run multiple times)
repo-cleaner -t ~/projects/app1
repo-cleaner -t ~/projects/app2
```

### Language Filter

```bash
# Clean only Python artifacts
repo-cleaner -l python

# Clean multiple languages
repo-cleaner -l python,node,java

# List available languages
repo-cleaner --list-languages
```

### Exclude Patterns

```bash
# Exclude specific directories
repo-cleaner -e "vendor/**"

# Multiple exclusions
repo-cleaner -e "vendor/**" -e "important_build/**" -e "*.important"

# Exclude node_modules from deletion
repo-cleaner -e "**/node_modules" -e "**/node_modules/**"
```

### Verbosity

```bash
# Verbose output (shows all indicators and details)
repo-cleaner -v

# Quiet mode (only errors)
repo-cleaner -q
```

## Configuration

### Configuration File Location

Repo Cleaner looks for configuration in this order:

1. Explicit path via `--config`
2. `.repo_cleaner.yaml` in target directory
3. `.repo_cleaner.yaml` in parent directories (up to home)

### Configuration Format

```yaml
# .repo_cleaner.yaml

# Global patterns to exclude from all cleaners
exclude:
  - "**/important_build/"
  - "vendor/**"
  - "third_party/**"

# Per-language configuration
languages:
  python:
    enabled: true
    # Additional patterns specific to your project
    additional_patterns:
      - name: "Custom Cache"
        patterns: ["my_cache/**"]
        type: "directory"
        description: "Project-specific cache"
    # Exclude from Python cleaning
    exclude:
      - "special_venv/**"

  node:
    enabled: true
    exclude: []

  java:
    enabled: true
    exclude: []

  c_cpp:
    enabled: true
    exclude: []

  react:
    enabled: true
    exclude: []

  angular:
    enabled: true
    exclude: []

  vue:
    enabled: true
    exclude: []

# Safety settings
safety:
  # Require directory to be a git repository
  require_git: false
  
  # Minimum free disk space (MB) before cleaning
  min_free_space_mb: 100
  
  # Maximum total size to delete (MB), 0 = no limit
  max_delete_size_mb: 0
```

### Disabling Languages

```yaml
languages:
  python:
    enabled: true
  node:
    enabled: false  # Won't clean node_modules, dist, etc.
```

## Supported Languages

### Python

**Automatically cleaned:**
- `__pycache__/` directories
- `*.pyc`, `*.pyo`, `*.pyd` files
- `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`
- `*.egg-info/` directories
- `dist/`, `build/` directories
- `.tox/`, `.coverage`, `htmlcov/`

**Requires confirmation:**
- `venv/`, `.venv/`, `env/` (virtual environments)

### Node.js

**Automatically cleaned:**
- `dist/`, `build/`, `out/` directories
- `.cache/`, `.parcel-cache/`
- `npm-debug.log*`, `yarn-*.log*`
- `coverage/`, `.nyc_output/`
- `*.tsbuildinfo`

**Requires confirmation:**
- `node_modules/` directories

### Java

**Automatically cleaned:**
- `target/` (Maven)
- `build/`, `out/` (Gradle)
- `*.class` files
- `.gradle/` cache

### C/C++

**Automatically cleaned:**
- `*.o`, `*.obj` object files
- `*.a`, `*.lib` static libraries
- `build/`, `cmake-build-*/` directories
- CMake cache files
- `*.dSYM/`, `*.pdb` debug symbols

**Requires confirmation:**
- `*.so`, `*.dylib`, `*.dll` shared libraries
- `*.exe` executables

### JavaScript Frameworks

**React:**
- `.next/` (Next.js)
- `build/` (Create React App)
- `.cache/` (Gatsby)

**Angular:**
- `dist/`
- `.angular/`

**Vue.js:**
- `dist/`
- `.nuxt/`, `.vite/`

## Common Use Cases

### Clean a Python Project

```bash
cd ~/projects/my-python-app
repo-cleaner -n  # Preview first
repo-cleaner     # Clean interactively
```

### Clean Before Committing

```bash
# Clean and see what space was freed
repo-cleaner -v

# Then commit
git add .
git commit -m "Clean build artifacts"
```

### Clean Monorepo

```bash
# Auto-detect all project types
repo-cleaner -t ~/monorepo

# Or clean specific subdirectories
repo-cleaner -t ~/monorepo/backend -l python
repo-cleaner -t ~/monorepo/frontend -l node,react
```

### CI/CD Pipeline

```bash
# Force mode, specific languages
repo-cleaner -f -l python,node

# With custom exclusions
repo-cleaner -f -e "deployment/**" -e "scripts/**"
```

### Clean Without Deleting Dependencies

```bash
# Keep node_modules but clean build artifacts
repo-cleaner -e "**/node_modules" -e "**/node_modules/**"

# Keep virtual environments
repo-cleaner -e "venv/**" -e ".venv/**"
```

### Disk Space Recovery

```bash
# Find large projects to clean
repo-cleaner -n -t ~/projects | grep "Total:"

# Clean the largest offenders
repo-cleaner -t ~/projects/big-app
```

## Safety Features

### Dry Run Mode

Always use dry run (`-n`) first to preview changes:

```bash
repo-cleaner -n
```

### Interactive Confirmation

By default, you'll be asked to confirm before deletion:

```
Clean 15 Python items (293.7 KB)? [y/N]:
```

### Require Git Repository

In your config, require the target to be a git repository:

```yaml
safety:
  require_git: true
```

### Confirmation for Dangerous Items

Some items always require confirmation:
- Virtual environments (`venv/`, `.venv/`)
- `node_modules/` directories
- Shared libraries (`.so`, `.dll`, `.dylib`)
- Executables (`.exe`)

## Troubleshooting

### "No project types detected"

This means no recognizable project files were found. Check:
- You're in the correct directory
- Project has standard structure (e.g., `package.json`, `pyproject.toml`)
- Try specifying languages manually: `repo-cleaner -l python`

### "Target directory is not a git repository"

If you have `require_git: true` in config:
- Initialize a git repo: `git init`
- Or set `require_git: false` in config
- Or use: `repo-cleaner -c /path/to/config/without/git/requirement.yaml`

### Files Not Being Cleaned

Check if they're excluded:
- Global excludes in config
- Language-specific excludes
- CLI `-e` patterns

Use verbose mode to see what's happening:
```bash
repo-cleaner -v
```

### Permission Errors

Some files may not be deletable due to permissions. Errors will be shown but other files will still be cleaned.

### Large Repositories

For very large repos, consider:
- Cleaning specific languages: `repo-cleaner -l python`
- Excluding large directories: `repo-cleaner -e "large_data/**"`
- Using force mode for speed: `repo-cleaner -f`

