# MCP Health Check Tool - Test Plan

## Overview

This document outlines the testing strategy for the MCP Health Check Tool. All stages are gated by **>= 80% code coverage**.

## Testing Pyramid

```
                    ┌───────────────┐
                    │  Integration  │  ← End-to-end health check flows
                    │    Tests      │
                    └───────────────┘
               ┌─────────────────────────┐
               │      Unit Tests         │  ← Individual components
               │   (mocked external)     │
               └─────────────────────────┘
          ┌───────────────────────────────────┐
          │        Static Analysis            │  ← mypy, ruff
          └───────────────────────────────────┘
```

## Test Coverage Requirements

| Stage | Module | Coverage Gate |
|-------|--------|---------------|
| 1 | `config/` | >= 80% |
| 2 | `validators/` | >= 80% |
| 3 | `mcp/` | >= 80% |
| 4 | `refresh/` | >= 80% |
| 5 | All + CLI | >= 80% |

## Stage 1: Configuration Tests

### `tests/unit/test_config.py`

#### Test Cases: ConfigLoader

| Test | Description | Expected |
|------|-------------|----------|
| `test_load_valid_config` | Load well-formed JSON | Returns MCPConfig |
| `test_load_missing_file` | File doesn't exist | Raises ConfigNotFoundError |
| `test_load_invalid_json` | Malformed JSON | Raises ConfigParseError |
| `test_load_missing_required_fields` | Missing `command` | Raises ValidationError |
| `test_find_config_default_location` | No explicit path | Finds ~/.cursor/mcp.json |
| `test_find_config_env_var` | MCP_CONFIG_PATH set | Uses env path |
| `test_load_with_empty_env` | Server with no env vars | Returns config with empty dict |

#### Test Cases: Models

| Test | Description | Expected |
|------|-------------|----------|
| `test_mcp_server_config_validation` | Valid server config | Model validates |
| `test_mcp_server_config_defaults` | Missing optional fields | Defaults applied |
| `test_mcp_config_multiple_servers` | Multiple server entries | All parsed correctly |

### Fixtures

```python
@pytest.fixture
def valid_config_json():
    return {
        "mcpServers": {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_test"}
            }
        }
    }

@pytest.fixture
def temp_config_file(tmp_path, valid_config_json):
    config_path = tmp_path / "mcp.json"
    config_path.write_text(json.dumps(valid_config_json))
    return config_path
```

## Stage 2: Validator Tests

### `tests/unit/test_validators.py`

#### Mocking Strategy

All external API calls are mocked using `respx`:

```python
@pytest.fixture
def mock_github_api():
    with respx.mock:
        yield respx
```

#### Test Cases: GitHubValidator

| Test | Description | Mock Response | Expected |
|------|-------------|---------------|----------|
| `test_valid_token` | Token works | 200 + user data | TokenStatus.VALID |
| `test_invalid_token` | Bad token | 401 | TokenStatus.INVALID |
| `test_expired_token` | Token expired | 401 + expired message | TokenStatus.EXPIRED |
| `test_missing_token` | No token in env | N/A | TokenStatus.MISSING |
| `test_rate_limited` | Too many requests | 403 | TokenStatus.UNKNOWN |
| `test_network_error` | Connection failed | Timeout | TokenStatus.UNKNOWN |

#### Test Cases: SlackValidator

| Test | Description | Mock Response | Expected |
|------|-------------|---------------|----------|
| `test_valid_token` | Token works | `{"ok": true}` | TokenStatus.VALID |
| `test_invalid_token` | Bad token | `{"ok": false, "error": "invalid_auth"}` | TokenStatus.INVALID |
| `test_revoked_token` | Token revoked | `{"ok": false, "error": "token_revoked"}` | TokenStatus.INVALID |
| `test_missing_token` | No token in env | N/A | TokenStatus.MISSING |

#### Test Cases: AtlassianValidator

| Test | Description | Mock Response | Expected |
|------|-------------|---------------|----------|
| `test_valid_token` | Token works | 200 + user data | TokenStatus.VALID |
| `test_expired_token` | Token expired | 401 | TokenStatus.EXPIRED |
| `test_missing_config_dir` | No MCP_REMOTE_CONFIG_DIR | N/A | TokenStatus.MISSING |
| `test_missing_token_file` | Config dir exists but no tokens | N/A | TokenStatus.MISSING |
| `test_can_refresh` | Has refresh_token | 200 | ValidationResult.can_refresh = True |

## Stage 3: MCP Protocol Tests

### `tests/unit/test_mcp_client.py`

#### Mocking Strategy

MCP server processes are mocked using `pytest-mock`:

```python
@pytest.fixture
def mock_subprocess(mocker):
    mock_proc = mocker.MagicMock()
    mock_proc.stdin = asyncio.StreamWriter(...)
    mock_proc.stdout = asyncio.StreamReader(...)
    mocker.patch('asyncio.create_subprocess_exec', return_value=mock_proc)
    return mock_proc
```

#### Test Cases: ServerSpawner

| Test | Description | Expected |
|------|-------------|----------|
| `test_spawn_success` | Valid command | Returns MCPConnection |
| `test_spawn_command_not_found` | Invalid command | Raises SpawnError |
| `test_spawn_timeout` | Process hangs | Raises TimeoutError |
| `test_terminate_clean` | Normal shutdown | Process terminated |
| `test_terminate_force` | Process won't stop | SIGKILL sent |

#### Test Cases: MCPClient

| Test | Description | Mock Response | Expected |
|------|-------------|---------------|----------|
| `test_initialize_success` | Server responds | `{"result": {...}}` | True |
| `test_initialize_failure` | Server errors | `{"error": {...}}` | False |
| `test_list_resources_success` | Has resources | `{"result": {"resources": [...]}}` | List of resources |
| `test_list_resources_empty` | No resources | `{"result": {"resources": []}}` | Empty list |
| `test_health_check_full_flow` | Complete check | Valid responses | ConnectionStatus.HEALTHY |
| `test_health_check_spawn_failure` | Can't spawn | SpawnError | ConnectionStatus.UNHEALTHY |
| `test_health_check_protocol_error` | Bad MCP response | Invalid JSON | ConnectionStatus.UNHEALTHY |

## Stage 4: Refresh Layer Tests

### `tests/unit/test_refresh.py`

#### Test Cases: OAuthRefresher

| Test | Description | Mock Response | Expected |
|------|-------------|---------------|----------|
| `test_refresh_atlassian_success` | Valid refresh | 200 + new tokens | RefreshResult.SUCCESS |
| `test_refresh_atlassian_expired_refresh` | Refresh token expired | 400 | RefreshResult.FAILED |
| `test_refresh_atlassian_no_token_file` | Missing tokens.json | N/A | RefreshResult.NO_TOKEN |
| `test_token_file_updated` | After refresh | N/A | New tokens written |

#### Test Cases: UserNotifier

| Test | Description | Expected |
|------|-------------|----------|
| `test_github_instructions` | GitHub PAT expired | Contains GitHub URL |
| `test_slack_instructions` | Slack token invalid | Contains Slack URL |
| `test_instructions_format` | All notifiers | Clear actionable steps |

## Stage 5: Integration Tests

### `tests/integration/test_health_check.py`

#### End-to-End Scenarios

| Test | Description | Setup | Expected |
|------|-------------|-------|----------|
| `test_all_healthy` | All servers pass | Mock all APIs healthy | Overall status: HEALTHY |
| `test_one_unhealthy` | One server fails | Mock one API failure | Overall status: DEGRADED |
| `test_all_unhealthy` | All servers fail | Mock all APIs fail | Overall status: UNHEALTHY |
| `test_refresh_triggered` | Expired OAuth | Mock expired + refresh | Token refreshed |
| `test_notify_triggered` | Expired PAT | Mock expired PAT | Notification shown |

#### CLI Tests

| Test | Description | Expected |
|------|-------------|----------|
| `test_cli_check_command` | `mcp-health check` | Runs without error |
| `test_cli_config_option` | `--config path` | Uses specified config |
| `test_cli_json_output` | `--format json` | Valid JSON output |
| `test_cli_verbose` | `-v` flag | More detailed output |
| `test_cli_missing_config` | No config found | Clear error message |

## Test Fixtures

### `tests/conftest.py`

```python
import pytest
import json
from pathlib import Path

@pytest.fixture
def sample_mcp_config():
    """Full sample MCP configuration"""
    return {
        "mcpServers": {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_test123"}
            },
            "slack": {
                "command": "npx", 
                "args": ["-y", "@modelcontextprotocol/server-slack"],
                "env": {"SLACK_BOT_TOKEN": "xoxb-test", "SLACK_TEAM_ID": "T123"}
            },
            "perimeter81-atlassian": {
                "command": "npx",
                "args": ["-y", "mcp-remote@0.1.30", "https://mcp.atlassian.com/v1/sse"],
                "env": {"MCP_REMOTE_CONFIG_DIR": "/tmp/.mcp-auth"}
            }
        }
    }

@pytest.fixture
def mock_atlassian_tokens(tmp_path):
    """Create mock Atlassian token file"""
    token_dir = tmp_path / ".mcp-auth"
    token_dir.mkdir()
    tokens = {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_at": "2024-01-01T00:00:00Z"
    }
    (token_dir / "tokens.json").write_text(json.dumps(tokens))
    return token_dir
```

## Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific stage
pytest tests/unit/test_config.py

# Run with verbose output
pytest -v

# Run and generate HTML coverage report
pytest --cov-report=html

# Check coverage without failing
pytest --cov-fail-under=0
```

## Coverage Gates

Each stage must pass before proceeding:

```bash
# Stage 1: Config
pytest tests/unit/test_config.py --cov=src/mcp_health/config --cov-fail-under=80

# Stage 2: Validators
pytest tests/unit/test_validators.py --cov=src/mcp_health/validators --cov-fail-under=80

# Stage 3: MCP
pytest tests/unit/test_mcp_client.py --cov=src/mcp_health/mcp --cov-fail-under=80

# Stage 4: Refresh
pytest tests/unit/test_refresh.py --cov=src/mcp_health/refresh --cov-fail-under=80

# Stage 5: Full
pytest --cov-fail-under=80
```

## Mocking Guidelines

1. **External APIs**: Always mock, never call real endpoints
2. **File System**: Use `tmp_path` fixture
3. **Subprocesses**: Mock with `pytest-mock`
4. **Time**: Use `freezegun` for time-dependent tests
5. **Environment Variables**: Use `monkeypatch`

