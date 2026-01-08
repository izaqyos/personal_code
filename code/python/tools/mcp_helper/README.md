# MCP Health Check Tool

A Python CLI tool for monitoring MCP (Model Context Protocol) server health by validating tokens, testing connections, and managing token refresh flows.

## Features

- **Token Validation**: Validates tokens for GitHub, Slack, and Atlassian services via their respective APIs
- **MCP Protocol Testing**: Tests MCP server connections using the native MCP protocol
- **Hybrid Token Refresh**: 
  - Auto-refresh OAuth tokens (Atlassian)
  - User notifications for manual tokens (GitHub PAT, Slack Bot Token)
- **Rich Reporting**: Color-coded console output and JSON export for automation
- **Parallel Validation**: All servers validated concurrently for faster checks
- **Watch Mode**: Continuous monitoring with configurable intervals
- **Retry Logic**: Automatic retry with exponential backoff for transient network failures
- **Expiration Warnings**: Proactive alerts for tokens expiring within 24 hours
- **Server Filtering**: Check specific servers only with `--server` option

## Installation

### Using Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd mcp_helper

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate     # On Windows

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

### Quick Install (Without venv)

```bash
cd mcp_helper
pip install -e ".[dev]"
```

> **Note:** Using a virtual environment is strongly recommended to avoid dependency conflicts with other Python projects.

## Quick Start

```bash
# Run health check with default config location
mcp-health check

# Specify custom config file
mcp-health check --config /path/to/mcp-config.json

# Output as JSON
mcp-health check --format json

# Verbose output
mcp-health check -v

# Check specific server(s) only
mcp-health check --server github --server slack

# Continuous monitoring (watch mode)
mcp-health check --watch --interval 60

# Skip MCP protocol tests (token validation only)
mcp-health check --skip-mcp

# Auto-refresh expired OAuth tokens
mcp-health check --auto-refresh
```

## Configuration

The tool reads your MCP server configuration from:
1. `--config` flag (explicit path)
2. `~/.cursor/mcp.json` (default Cursor location)
3. `MCP_CONFIG_PATH` environment variable

### Example Configuration

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..."
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-...",
        "SLACK_TEAM_ID": "T..."
      }
    },
    "perimeter81-atlassian": {
      "command": "npx",
      "args": ["-y", "mcp-remote@0.1.30", "https://mcp.atlassian.com/v1/sse"],
      "env": {
        "MCP_REMOTE_CONFIG_DIR": "/path/to/.mcp-auth/mcp-remote-stable"
      }
    }
  }
}
```

## Health Check Output

```
MCP Server Health Check
========================

✓ github
  Token: Valid (expires: never)
  MCP Connection: Healthy
  
⚠ slack  
  Token: Invalid - token revoked
  Action Required: Regenerate bot token at https://api.slack.com/apps
  
✓ perimeter81-atlassian
  Token: Valid (expires: 2024-01-15 10:30:00)
  MCP Connection: Healthy
  OAuth: Auto-refreshable
```

## Supported Services

| Service | Token Type | Auto-Refresh | Validation Method |
|---------|-----------|--------------|-------------------|
| GitHub | PAT | No | `GET /user` |
| Slack | Bot Token | No | `POST auth.test` |
| Atlassian | OAuth 2.0 | Yes | Process detection + API fallback |

### Atlassian MCP Special Considerations

Atlassian MCP uses `mcp-remote` which manages OAuth tokens differently than other MCP servers:

- **MCP-Scoped Tokens**: Tokens work for MCP but not standard REST APIs
- **In-Memory Management**: Fresh tokens may not be immediately persisted to disk
- **Process-Based Validation**: `mcp-health` detects running `mcp-remote` processes as validation fallback
- **No Alternative**: `mcp-remote` is the official Atlassian-recommended proxy for desktop clients

**Why Claude Code works better:**
Claude Code has native MCP OAuth support and connects directly to Atlassian's cloud without needing `mcp-remote`. This eliminates token file synchronization issues entirely.

**If Atlassian tokens appear expired but MCP works in Cursor:**

1. **Toggle in Cursor**: Settings → MCP Servers → Toggle Atlassian OFF/ON (most reliable)
2. **Use mcp-health**: `mcp-health check --server perimeter81-atlassian --reauth`
3. **Use Claude Code**: For Atlassian-heavy workflows (no token issues)

See [ATLASSIAN_TOKEN_ISSUES.md](docs/ATLASSIAN_TOKEN_ISSUES.md) for detailed troubleshooting and architecture explanation.

## Development

### Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dev dependencies
pip install -e ".[dev]"
```

### Testing

The project maintains **88% test coverage** with 171 tests across unit and integration test suites.

#### Run All Tests

```bash
# Run all tests with coverage report
pytest

# Quick run (no coverage report)
pytest -q

# Verbose output
pytest -v
```

#### Coverage Requirements

All stages are gated by **>= 80% coverage**:

```bash
# Check overall coverage (must be >= 80%)
pytest --cov=src/mcp_health --cov-report=term --cov-fail-under=80

# Generate HTML coverage report
pytest --cov=src/mcp_health --cov-report=html
# Open htmlcov/index.html in browser

# Stage-specific coverage
pytest tests/unit/test_config.py --cov=src/mcp_health/config --cov-fail-under=80
pytest tests/unit/test_validators.py --cov=src/mcp_health/validators --cov-fail-under=80
pytest tests/unit/test_mcp_client.py --cov=src/mcp_health/mcp --cov-fail-under=80
pytest tests/unit/test_refresh.py --cov=src/mcp_health/refresh --cov-fail-under=80
```

#### Test Organization

```
tests/
├── conftest.py              # Shared fixtures
├── unit/                    # Unit tests (mocked external dependencies)
│   ├── test_config.py       # Config loading & validation
│   ├── test_validators.py  # Token validators (GitHub, Slack, Atlassian)
│   ├── test_mcp_client.py  # MCP protocol client & spawner
│   └── test_refresh.py     # OAuth refresh & notifications
└── integration/             # Integration tests (end-to-end flows)
    └── test_health_check.py # Full health check scenarios
```

#### Run Specific Tests

```bash
# Run single test file
pytest tests/unit/test_config.py

# Run specific test class
pytest tests/unit/test_validators.py::TestGitHubValidator

# Run specific test method
pytest tests/unit/test_validators.py::TestGitHubValidator::test_valid_token

# Run tests matching pattern
pytest -k "github"
```

### Code Quality

```bash
# Type checking with mypy
mypy src/ --ignore-missing-imports

# Linting with ruff
ruff check src/ tests/

# Auto-fix linting issues
ruff check --fix src/ tests/

# Format code
ruff format src/ tests/
```

### Current Test Coverage

| Module | Coverage | Tests |
|--------|----------|-------|
| `config/` | 94-100% | 35 tests |
| `validators/` | 88-100% | 43 tests |
| `mcp/` | 77-98% | 30 tests |
| `refresh/` | 92-100% | 28 tests |
| `reporting/` | 96% | 35 tests |
| **Overall** | **88%** | **171 tests** |

### Linting & Type Checking

The project uses **ruff** for linting and **mypy** for static type checking.

```bash
# Run ruff linting
ruff check src/ tests/

# Auto-fix linting issues
ruff check --fix src/ tests/

# Format code with ruff
ruff format src/ tests/

# Run mypy type checking
mypy src/ --ignore-missing-imports

# Run all checks
ruff check src/ tests/ && mypy src/ --ignore-missing-imports
```

#### Current Status

✅ **All checks passing:**
- ✓ Ruff: 0 errors, all code formatted
- ✓ Mypy: 0 errors, full type coverage
- ✓ Tests: 171/171 passing (88% coverage)

## Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, component diagrams, data flow |
| [TEST_PLAN.md](docs/TEST_PLAN.md) | Testing strategy and coverage requirements |
| [LEARNING_GUIDE.md](docs/LEARNING_GUIDE.md) | Python patterns & idioms used in this project |
| [MANUAL_TEST_PLAN.md](docs/MANUAL_TEST_PLAN.md) | Step-by-step smoke tests for manual QA |
| [CODE_REVIEW.md](docs/CODE_REVIEW.md) | Improvement suggestions and future enhancements |
| [ATLASSIAN_TOKEN_ISSUES.md](docs/ATLASSIAN_TOKEN_ISSUES.md) | Troubleshooting guide for Atlassian MCP token issues |
| [ARCHITECTURE_COMPARISON.md](docs/ARCHITECTURE_COMPARISON.md) | Why Claude Code works seamlessly vs Cursor with mcp-remote |

## Project Structure

```
mcp_helper/
├── src/mcp_health/
│   ├── cli.py           # Click-based CLI
│   ├── config/          # Configuration loading
│   ├── validators/      # Token validators
│   ├── mcp/             # MCP protocol client
│   ├── refresh/         # Token refresh logic
│   └── reporting/       # Report generation
├── tests/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
└── docs/                # Documentation
    ├── ARCHITECTURE.md
    ├── TEST_PLAN.md
    ├── LEARNING_GUIDE.md
    ├── MANUAL_TEST_PLAN.md
    └── CODE_REVIEW.md
```

## License

MIT

