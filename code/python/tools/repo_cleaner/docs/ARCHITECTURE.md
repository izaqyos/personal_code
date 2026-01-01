# Repo Cleaner Architecture

## Overview

Repo Cleaner follows a modular, extensible architecture that separates concerns into distinct components:

```
┌─────────────────────────────────────────────────────────────┐
│                      CLI Entry Point                         │
│                   (repo_cleaner/main.py)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Core Orchestrator                         │
│              (repo_cleaner/core/cleaner.py)                 │
└──────────┬──────────────────────────────┬───────────────────┘
           │                              │
           ▼                              ▼
┌──────────────────────┐    ┌──────────────────────────────┐
│   Project Detector    │    │    Cleaner Engine            │
│ (detectors/__init__) │    │  (cleaners/__init__.py)      │
└──────────┬────────────┘    └──────────┬───────────────────┘
           │                            │
           ▼                            ▼
┌──────────────────────┐    ┌──────────────────────────────┐
│  Language Detectors  │    │  Language Cleaners            │
│  - Python detector   │    │  - PythonCleaner              │
│  - Node detector     │    │  - NodeCleaner                │
│  - Java detector     │    │  - JavaCleaner                │
│  - C/C++ detector    │    │  - CCppCleaner                │
│  - JS Framework      │    │  - FrameworkCleaner           │
└──────────────────────┘    └──────────────────────────────┘
```

## Design Principles

1. **Modularity**: Each language/framework has its own detector and cleaner module
2. **Extensibility**: Easy to add new language support via plugin-like architecture
3. **Safety First**: Dry-run by default, interactive confirmation, git-aware
4. **Configuration**: Sensible defaults with optional user overrides
5. **Cross-platform**: Works on Unix, macOS, and Windows

## Components

### 1. CLI Entry Point (`main.py`)

The CLI is built with Click and provides:
- Argument parsing and validation
- Logging configuration
- Error handling and exit codes

Key options:
- `--dry-run / -n`: Preview without deleting
- `--no-interactive / -y`: Skip confirmations
- `--config / -c`: Custom config file
- `--target / -t`: Target directory
- `--languages / -l`: Filter by languages
- `--exclude / -e`: Exclusion patterns

### 2. Core Orchestrator (`core/cleaner.py`)

The `RepoCleaner` class coordinates the entire workflow:

```python
class RepoCleaner:
    def detect_project_types(path: Path) -> Dict[str, DetectionResult]
    def validate_safety_checks(path: Path) -> None
    def get_cleaner_for_type(project_type: str) -> BaseCleaner
    def clean(path, languages, exclude_patterns) -> CleanSummary
```

Responsibilities:
- Orchestrate detection and cleaning
- Manage dry-run vs actual deletion
- Handle interactive confirmations
- Aggregate results from multiple cleaners

### 3. Detector System (`detectors/`)

Base interface:
```python
class BaseDetector(ABC):
    @property
    def name(self) -> str
    def detect(self, path: Path) -> bool
    def get_confidence(self, path: Path) -> float
    def get_indicators(self, path: Path) -> List[str]
    def full_detect(self, path: Path) -> DetectionResult
```

Detection strategy:
- Multi-pass detection (can detect multiple project types)
- Confidence scoring (0.0 to 1.0)
- Priority ordering (more specific frameworks first)

### 4. Cleaner System (`cleaners/`)

Base interface:
```python
class BaseCleaner(ABC):
    @property
    def name(self) -> str
    def get_patterns(self) -> List[Pattern]
    def find_items(path, exclude_patterns) -> List[CleanItem]
    def clean(path, dry_run, exclude_patterns) -> CleanResult
```

Pattern structure:
```python
@dataclass
class Pattern:
    name: str
    patterns: List[str]  # Glob patterns
    type: PatternType    # FILE, DIRECTORY, or BOTH
    description: str
    safe: bool = True
    requires_confirmation: bool = False
```

### 5. Configuration System (`config/`)

Configuration hierarchy (lowest to highest priority):
1. Built-in defaults (`defaults.py`)
2. User config file (`.repo_cleaner.yaml`)
3. CLI arguments

Config file format:
```yaml
exclude: []
languages:
  python:
    enabled: true
    additional_patterns: []
    exclude: []
safety:
  require_git: false
  min_free_space_mb: 100
  max_delete_size_mb: 0
```

### 6. Utilities (`utils/`)

- `filesystem.py`: Safe file operations, size calculation, pattern matching
- `git.py`: Repository detection, status checks
- `prompts.py`: Interactive confirmations, progress display, colorized output

## Data Flow

```
User Input (CLI)
    │
    ▼
Parse Arguments
    │
    ▼
Load Configuration (defaults + user config)
    │
    ▼
Initialize RepoCleaner
    │
    ▼
Validate Safety Checks
    │
    ▼
Detect Project Types (run all detectors)
    │
    ▼
Select Cleaners (based on detected types)
    │
    ▼
For each Cleaner:
    ├── Collect matching files/dirs
    ├── Calculate total size
    ├── Apply exclude patterns
    ├── (If interactive) Prompt for confirmation
    ├── (If dry-run) Display preview
    └── (If not dry-run) Delete items
    │
    ▼
Aggregate Results
    │
    ▼
Display Summary
    │
    ▼
Exit (with appropriate code)
```

## Error Handling

Custom exceptions:
- `RepoCleanerError`: Base exception
- `SafetyCheckError`: Git check failed, insufficient space
- `ConfigurationError`: Invalid config file
- `DetectionError`: Detector failure
- `CleanError`: Cleaner execution failure

Strategy:
- Fail fast on safety checks
- Continue on non-critical errors (log warnings)
- Clear error messages with suggestions

## Adding New Language Support

### 1. Create Detector

```python
# repo_cleaner/detectors/ruby.py
class RubyDetector(BaseDetector):
    @property
    def name(self) -> str:
        return "ruby"
    
    def detect(self, path: Path) -> bool:
        # Check for Gemfile, *.rb files, etc.
        pass
    
    def get_confidence(self, path: Path) -> float:
        # Return 0.0-1.0 based on indicators
        pass
```

### 2. Create Cleaner

```python
# repo_cleaner/cleaners/ruby.py
class RubyCleaner(BaseCleaner):
    @property
    def name(self) -> str:
        return "ruby"
    
    def get_patterns(self) -> List[Pattern]:
        return [
            Pattern(
                name="Bundler Gems",
                patterns=["vendor/bundle/**"],
                type=PatternType.DIRECTORY,
                description="Bundler gem cache",
            ),
            # More patterns...
        ]
```

### 3. Register in `__init__.py`

```python
# detectors/__init__.py
from repo_cleaner.detectors.ruby import RubyDetector
ALL_DETECTORS.append(RubyDetector())

# cleaners/__init__.py
from repo_cleaner.cleaners.ruby import RubyCleaner
CLEANER_REGISTRY["ruby"] = RubyCleaner
```

### 4. Add Default Patterns

```python
# config/defaults.py
DEFAULT_PATTERNS["ruby"] = [
    {
        "name": "Bundler Gems",
        "patterns": ["vendor/bundle/**"],
        "type": "directory",
        "description": "Bundler gem cache",
    },
]
```

## Testing Strategy

- **Unit Tests**: Individual detectors, cleaners, config parsing
- **Integration Tests**: Full workflow with fixture projects
- **Fixtures**: Realistic project structures for each language

Coverage targets:
- Unit tests: >90%
- Integration tests: All major workflows
- Edge cases: Empty dirs, symlinks, permissions

