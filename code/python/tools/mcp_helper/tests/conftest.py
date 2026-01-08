"""Shared test fixtures for MCP Health Check Tool."""

import json
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def sample_mcp_config() -> dict[str, Any]:
    """Full sample MCP configuration."""
    return {
        "mcpServers": {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_test123"},
            },
            "slack": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-slack"],
                "env": {"SLACK_BOT_TOKEN": "xoxb-test", "SLACK_TEAM_ID": "T123"},
            },
            "perimeter81-atlassian": {
                "command": "npx",
                "args": ["-y", "mcp-remote@0.1.30", "https://mcp.atlassian.com/v1/sse"],
                "env": {"MCP_REMOTE_CONFIG_DIR": "/tmp/.mcp-auth"},
            },
        }
    }


@pytest.fixture
def github_only_config() -> dict[str, Any]:
    """Config with only GitHub server."""
    return {
        "mcpServers": {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_testtoken"},
            }
        }
    }


@pytest.fixture
def minimal_config() -> dict[str, Any]:
    """Minimal valid config with just command and args."""
    return {
        "mcpServers": {
            "test-server": {
                "command": "echo",
                "args": ["hello"],
            }
        }
    }


@pytest.fixture
def temp_config_file(tmp_path: Path, sample_mcp_config: dict[str, Any]) -> Path:
    """Create a temporary config file with sample config."""
    config_path = tmp_path / "mcp.json"
    config_path.write_text(json.dumps(sample_mcp_config))
    return config_path


@pytest.fixture
def temp_minimal_config_file(tmp_path: Path, minimal_config: dict[str, Any]) -> Path:
    """Create a temporary config file with minimal config."""
    config_path = tmp_path / "mcp.json"
    config_path.write_text(json.dumps(minimal_config))
    return config_path


@pytest.fixture
def mock_atlassian_tokens(tmp_path: Path) -> Path:
    """Create mock Atlassian token file with valid (future) expiration."""
    token_dir = tmp_path / ".mcp-auth"
    token_dir.mkdir()
    tokens = {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_at": "2099-01-01T00:00:00Z",  # Far future - always valid
    }
    (token_dir / "tokens.json").write_text(json.dumps(tokens))
    return token_dir


@pytest.fixture
def mock_expired_atlassian_tokens(tmp_path: Path) -> Path:
    """Create mock expired Atlassian token file."""
    token_dir = tmp_path / ".mcp-auth-expired"
    token_dir.mkdir()
    tokens = {
        "access_token": "expired_access_token",
        "refresh_token": "valid_refresh_token",
        "expires_at": "2020-01-01T00:00:00Z",
    }
    (token_dir / "tokens.json").write_text(json.dumps(tokens))
    return token_dir
