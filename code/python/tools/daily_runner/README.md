# Daily Standup Timer

A Python application for managing daily standup meetings with configurable timers, meeting history tracking, and analytics.

## Features

- **Per-developer timers** with configurable time limits (default: 3 minutes)
- **Visual alerts** for warnings, overtime, and overflow states
- **Grace period** (15s) after timer expires with warning
- **Overflow period** (90s after grace) with bold red display for hard time limits
- **Two interface modes**: Streamlit UI and Interactive CLI
- **Meeting history** tracking with analytics
- **Inactivity timeout** auto-closes forgotten meetings after 5 minutes of no input (configurable)
- **Session recovery** for crash resilience
- **Multi-team support** with separate configurations

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Setup

```bash
# Clone the repository
cd daily_runner

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

## Usage

### Quick Start (Imagine Dragons Team)

```bash
# Launch daily standup (Streamlit UI)
python main.py --team imagine_dragons

# Launch daily standup (CLI mode)
python main.py --mode cli --team imagine_dragons

# View meeting history
python main.py --mode history --team imagine_dragons

# Launch with test config (faster timers for testing)
python main.py --config config.test.json --team imagine_dragons
```

### Streamlit UI Mode (Default)

```bash
python main.py
# or explicitly
python main.py --mode ui
```

### CLI Mode

```bash
python main.py --mode cli
```

### Specify Team

```bash
python main.py --team sample_team
```

### View Meeting History

```bash
# View last 30 days of meetings
python main.py --mode history

# View last 7 days, limit to 10 entries
python main.py --mode history --days 7 --limit 10

# View history for specific team
python main.py --mode history --team sample_team
```

### Using Installed Command

After `pip install -e .`, you can also use the installed command:

```bash
daily-timer --team sample_team
daily-timer --mode history
```

## Configuration

Configuration is stored in `config.json`. A test configuration (`config.test.json`) is also available with reduced timers for faster testing:

| Setting | Production | Test |
|---------|------------|------|
| Speaker time | 180s (3m) | 30s |
| Transition time | 30s | 5s |
| Grace period | 15s | 3s |
| Warning threshold | 30s | 5s |
| Overflow period | 90s | 10s |
| Inactivity timeout | 600s (10m) | 30s |
| Auto-save interval | 5s | 1s |
| Max history entries | 2000 | 100 |

### Default Configuration (`config.json`)

```json
{
  "timer": {
    "default_speaker_time_seconds": 180,
    "transition_time_seconds": 30,
    "grace_period_seconds": 15,
    "warning_threshold_seconds": 30,
    "overflow_period_seconds": 90,
    "inactivity_timeout_seconds": 600
  },
  "teams": {
    "directory": "teams",
    "default_team": "imagine_dragons"
  }
}
```

## Team Configuration

Team files are stored in the `teams/` directory as JSON files. A `sample_team.json` is provided as a template.

### Creating Your Own Team

1. Copy the sample team file:
   ```bash
   cp teams/sample_team.json teams/my_team.json
   ```

2. Edit `teams/my_team.json` with your team's information:
   ```json
   {
     "team": {
       "name": "My Team",
       "emoji": "🚀",
       "team_leader": {
         "name": "Team Lead Name",
         "email": "lead@example.com"
       }
     },
     "members": [
       {
         "id": "alice",
         "name": "Alice Anderson",
         "display_name": "Alice",
         "email": "alice@example.com",
         "github": "alice-dev",
         "role": "Developer",
         "specialization": ["frontend", "testing"],
         "daily_config": {
           "default_time_seconds": 180,
           "active": true
         }
       }
     ]
   }
   ```

3. Run with your team:
   ```bash
   python main.py --team my_team
   ```

**Note:** Team files (except `sample_team.json`) are gitignored to protect personal data.

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_package_structure.py
```

### Type Checking

```bash
mypy src/
```

### Linting

```bash
ruff check src/ tests/
```

### All Quality Checks

```bash
# Run all checks before committing
pytest --cov=src --cov-fail-under=80 && mypy src/ && ruff check src/ tests/
```

## Project Structure

```
daily_runner/
├── src/
│   ├── core/           # Business logic (timer, state machine, models)
│   ├── data/           # Data access (config, teams, history)
│   ├── services/       # Analytics service
│   ├── ui/             # Streamlit interface
│   └── cli/            # CLI interface
├── tests/
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── teams/              # Team configuration files
├── data/               # Generated data (history, recovery)
├── config.json         # Application configuration
└── main.py             # Entry point
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed version history.

## License

MIT License - See LICENSE file for details.

## Author

Yosi Izaq - Imagine Dragons Team Lead
