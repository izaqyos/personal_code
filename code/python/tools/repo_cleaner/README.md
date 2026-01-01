# Repo Cleaner

A powerful Python CLI tool for cleaning build artifacts, cache directories, and generated files across multiple programming languages and frameworks.

## Features

- **Multi-language Support**: Python, Node.js, Java, C/C++, React, Angular, Vue.js
- **Auto-detection**: Automatically detects project types in your repository
- **Safe Defaults**: Dry-run mode, interactive confirmations, git-aware operations
- **Configurable**: Optional YAML configuration for custom patterns and exclusions
- **Cross-platform**: Works on Linux, macOS, and Windows

## Installation

```bash
# From PyPI (when published)
pip install repo-cleaner

# From source
git clone https://github.com/repo-cleaner/repo-cleaner.git
cd repo-cleaner
pip install -e .
```

## Quick Start

```bash
# Clean current directory (interactive mode)
repo-cleaner

# Dry run - preview what would be cleaned
repo-cleaner -n

# Clean specific directory
repo-cleaner -t ~/projects/myapp

# Force mode (skip all confirmations)
repo-cleaner -f

# Clean only specific languages
repo-cleaner -l python,node

# Exclude patterns
repo-cleaner -e "vendor/**" -e "custom_build/**"

# Monorepo support (scans recursively)
repo-cleaner -t ~/monorepo -n          # Preview all projects
repo-cleaner -t ~/monorepo -f          # Clean all without prompts
repo-cleaner -t ~/monorepo --rescan    # Force fresh project scan

# View cleanup history
repo-cleaner --history
```

## CLI Options

| Option | Short | Description |
|--------|-------|-------------|
| `--target` | `-t` | Target directory to clean (default: current directory) |
| `--dry-run` | `-n` | Preview changes without deleting anything |
| `--force` | `-f` | Skip all confirmation prompts (non-interactive mode) |
| `--config` | `-c` | Path to configuration file |
| `--languages` | `-l` | Comma-separated list of languages to clean |
| `--exclude` | `-e` | Patterns to exclude (can be specified multiple times) |
| `--rescan` | | Force fresh project scan (ignore cached layout) |
| `--detailed-report` | | Include item details in cleanup report |
| `--history` | | Show cleanup history and exit |
| `--verbose` | `-v` | Show verbose output |
| `--quiet` | `-q` | Suppress non-error output |
| `--list-languages` | | List available language cleaners |
| `--version` | | Show version and exit |

## Monorepo Support

Repo Cleaner automatically handles monorepos with multiple projects in subdirectories:

- **Recursive scanning**: Finds all projects at any depth
- **Per-project confirmation**: Asks for each project (unless `-f` used)
- **Layout caching**: Caches scan results for 24 hours (use `--rescan` to refresh)
- **History tracking**: Saves last 1000 cleanup reports

### Monorepo Workflow

```bash
# First, preview what will be cleaned
repo-cleaner -t ~/monorepo -n

# This will show:
# - All detected projects
# - Project types (Python, Node, etc.)
# - What would be cleaned in each

# Then clean with per-project prompts
repo-cleaner -t ~/monorepo

# Or clean everything without prompts
repo-cleaner -t ~/monorepo -f
```

### Data Storage

Repo Cleaner stores data in `~/.config/repo_cleaner/`:

```
~/.config/repo_cleaner/
├── history.json         # Cleanup history (last 1000 entries)
└── layouts/
    └── *.json           # Cached project layouts (24h expiry)
```

## Supported Languages

### Python
- `__pycache__/` directories
- `*.pyc`, `*.pyo`, `*.pyd` files
- `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`
- `*.egg-info/` directories
- `dist/`, `build/` directories
- Virtual environments (`venv/`, `.venv/`) - requires confirmation
- Coverage data (`.coverage`, `htmlcov/`)

### Node.js
- `node_modules/` - requires confirmation
- `dist/`, `build/`, `out/` directories
- `.next/`, `.nuxt/`, `.cache/`
- NPM/Yarn log files
- Coverage reports

### Java
- `target/` (Maven)
- `build/`, `out/` (Gradle)
- `*.class` files
- `.gradle/` cache

### C/C++
- `*.o`, `*.obj` object files
- `*.a`, `*.lib` static libraries
- `*.so`, `*.dylib`, `*.dll` shared libraries - requires confirmation
- `build/`, `cmake-build-*/` directories
- CMake cache files
- Debug symbols

### React
- `.next/` (Next.js)
- `build/` (Create React App)
- `.cache/` (Gatsby)

### Angular
- `dist/` build output
- `.angular/` cache

### Vue.js
- `dist/` build output
- `.nuxt/`, `.vite/` directories

## Configuration

Create a `.repo_cleaner.yaml` file in your project root:

```yaml
# Global exclude patterns
exclude:
  - "**/important_build/"
  - "vendor/**"

# Language-specific settings
languages:
  python:
    enabled: true
    exclude:
      - "special_cache/**"
  node:
    enabled: true
    additional_patterns:
      - name: "Custom Cache"
        patterns: ["custom_cache/**"]
        type: "directory"
        description: "Custom cache directory"

# Safety settings
safety:
  require_git: false      # Require directory to be a git repository
  min_free_space_mb: 100  # Minimum free disk space in MB
  max_delete_size_mb: 0   # Maximum size to delete (0 = no limit)
```

## Examples

### Clean a Python project

```bash
$ repo-cleaner -t ~/projects/myapp -l python -n

============================================================
  Repo Cleaner v0.1.0
  Target: /home/user/projects/myapp
  Mode: DRY RUN (no files will be deleted)
============================================================

ℹ Detected project types: python

Python items to clean:
  [DIR ] src/__pycache__ (45.2 KB)
  [DIR ] tests/__pycache__ (12.8 KB)
  [DIR ] .pytest_cache (1.2 KB)
  [DIR ] .mypy_cache (234.5 KB)
  Total: 4 items, 293.7 KB

============================================================
⚠ DRY RUN - No files were actually deleted
✓ Cleaning complete! Freed 293.7 KB from 4 items
============================================================
```

### Clean a Node.js project

```bash
$ repo-cleaner -t ~/projects/webapp -l node -e "**/node_modules"

# Cleans dist/, .cache/, .next/ etc. but preserves node_modules
```

### Clean everything in a monorepo

```bash
$ repo-cleaner -t ~/projects/monorepo -f

# Auto-detects all project types and cleans without prompts
```

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/repo-cleaner/repo-cleaner.git
cd repo-cleaner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=repo_cleaner --cov-report=html

# Run specific test file
pytest tests/test_detectors/test_python_detector.py
```

### Code Quality

```bash
# Lint with ruff
ruff check .

# Type check with mypy
mypy repo_cleaner

# Format code
ruff format .
```

## Architecture

The project follows a modular architecture:

```
repo_cleaner/
├── core/           # Orchestrator and exceptions
├── detectors/      # Language detection modules
├── cleaners/       # Language cleaning modules
├── config/         # Configuration management
└── utils/          # Filesystem, git, and prompt utilities
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Changelog

### v0.1.0

- Initial release
- Support for Python, Node.js, Java, C/C++, React, Angular, Vue.js
- Dry-run and interactive modes
- Configuration file support
- Comprehensive test suite

