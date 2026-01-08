"""Unit tests for configuration loading and models."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from mcp_health.config import (
    ConfigLoader,
    ConfigNotFoundError,
    ConfigParseError,
    ConfigValidationError,
    MCPConfig,
    MCPServerConfig,
)


class TestMCPServerConfig:
    """Tests for MCPServerConfig model."""

    def test_valid_server_config(self) -> None:
        """Test creating a valid server config."""
        config = MCPServerConfig(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={"GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_test"},
        )
        assert config.command == "npx"
        assert config.args == ["-y", "@modelcontextprotocol/server-github"]
        assert config.env["GITHUB_PERSONAL_ACCESS_TOKEN"] == "ghp_test"

    def test_minimal_server_config(self) -> None:
        """Test creating config with only required fields."""
        config = MCPServerConfig(command="echo", args=["hello"])
        assert config.command == "echo"
        assert config.args == ["hello"]
        assert config.env == {}

    def test_default_empty_args(self) -> None:
        """Test that args defaults to empty list."""
        config = MCPServerConfig(command="test")
        assert config.args == []

    def test_default_empty_env(self) -> None:
        """Test that env defaults to empty dict."""
        config = MCPServerConfig(command="test", args=[])
        assert config.env == {}

    def test_get_env_var_exists(self) -> None:
        """Test getting an existing environment variable."""
        config = MCPServerConfig(command="test", env={"MY_TOKEN": "secret123"})
        assert config.get_env_var("MY_TOKEN") == "secret123"

    def test_get_env_var_missing(self) -> None:
        """Test getting a missing environment variable."""
        config = MCPServerConfig(command="test", env={})
        assert config.get_env_var("MISSING") is None

    def test_get_env_var_with_default(self) -> None:
        """Test getting a missing variable with default."""
        config = MCPServerConfig(command="test", env={})
        assert config.get_env_var("MISSING", "default_value") == "default_value"

    def test_has_env_var_true(self) -> None:
        """Test has_env_var returns True for existing var."""
        config = MCPServerConfig(command="test", env={"EXISTS": "yes"})
        assert config.has_env_var("EXISTS") is True

    def test_has_env_var_false(self) -> None:
        """Test has_env_var returns False for missing var."""
        config = MCPServerConfig(command="test", env={})
        assert config.has_env_var("MISSING") is False


class TestMCPConfig:
    """Tests for MCPConfig model."""

    def test_valid_config(self, sample_mcp_config: dict[str, Any]) -> None:
        """Test creating a valid MCP config."""
        config = MCPConfig.model_validate(sample_mcp_config)
        assert len(config) == 3
        assert "github" in config.server_names()
        assert "slack" in config.server_names()
        assert "perimeter81-atlassian" in config.server_names()

    def test_get_server_exists(self, sample_mcp_config: dict[str, Any]) -> None:
        """Test getting an existing server."""
        config = MCPConfig.model_validate(sample_mcp_config)
        github = config.get_server("github")
        assert github is not None
        assert github.command == "npx"

    def test_get_server_missing(self, sample_mcp_config: dict[str, Any]) -> None:
        """Test getting a non-existent server."""
        config = MCPConfig.model_validate(sample_mcp_config)
        assert config.get_server("nonexistent") is None

    def test_server_names(self, sample_mcp_config: dict[str, Any]) -> None:
        """Test getting all server names."""
        config = MCPConfig.model_validate(sample_mcp_config)
        names = config.server_names()
        assert sorted(names) == ["github", "perimeter81-atlassian", "slack"]

    def test_len(self, sample_mcp_config: dict[str, Any]) -> None:
        """Test __len__ returns number of servers."""
        config = MCPConfig.model_validate(sample_mcp_config)
        assert len(config) == 3

    def test_iter(self, sample_mcp_config: dict[str, Any]) -> None:
        """Test iterating over server configurations."""
        config = MCPConfig.model_validate(sample_mcp_config)
        items = list(config)
        assert len(items) == 3
        names = [name for name, _ in items]
        assert "github" in names

    def test_single_server_config(self, github_only_config: dict[str, Any]) -> None:
        """Test config with single server."""
        config = MCPConfig.model_validate(github_only_config)
        assert len(config) == 1
        assert config.server_names() == ["github"]

    def test_alias_mcp_servers(self) -> None:
        """Test that mcpServers alias works."""
        data = {"mcpServers": {"test": {"command": "echo", "args": []}}}
        config = MCPConfig.model_validate(data)
        assert len(config) == 1


class TestConfigLoader:
    """Tests for ConfigLoader."""

    def test_load_valid_config(self, temp_config_file: Path) -> None:
        """Test loading a valid config file."""
        loader = ConfigLoader()
        config = loader.load(temp_config_file)
        assert len(config) == 3
        assert config.get_server("github") is not None

    def test_load_minimal_config(self, temp_minimal_config_file: Path) -> None:
        """Test loading a minimal config file."""
        loader = ConfigLoader()
        config = loader.load(temp_minimal_config_file)
        assert len(config) == 1
        server = config.get_server("test-server")
        assert server is not None
        assert server.command == "echo"

    def test_load_missing_file(self, tmp_path: Path) -> None:
        """Test loading a non-existent file."""
        loader = ConfigLoader()
        missing_path = tmp_path / "nonexistent.json"
        with pytest.raises(ConfigNotFoundError) as exc_info:
            loader.load(missing_path)
        assert str(missing_path) in str(exc_info.value)

    def test_load_invalid_json(self, tmp_path: Path) -> None:
        """Test loading a file with invalid JSON."""
        invalid_path = tmp_path / "invalid.json"
        invalid_path.write_text("{ invalid json }")
        loader = ConfigLoader()
        with pytest.raises(ConfigParseError) as exc_info:
            loader.load(invalid_path)
        assert str(invalid_path) in str(exc_info.value)

    def test_load_missing_required_fields(self, tmp_path: Path) -> None:
        """Test loading config with missing required fields."""
        invalid_path = tmp_path / "missing_fields.json"
        # Missing 'command' field
        invalid_path.write_text(json.dumps({"mcpServers": {"test": {"args": ["hello"]}}}))
        loader = ConfigLoader()
        with pytest.raises(ConfigValidationError):
            loader.load(invalid_path)

    def test_load_empty_servers(self, tmp_path: Path) -> None:
        """Test loading config with empty servers dict."""
        empty_path = tmp_path / "empty.json"
        empty_path.write_text(json.dumps({"mcpServers": {}}))
        loader = ConfigLoader()
        config = loader.load(empty_path)
        assert len(config) == 0

    def test_load_from_string(self) -> None:
        """Test loading config from JSON string."""
        json_str = json.dumps({"mcpServers": {"test": {"command": "echo", "args": ["hello"]}}})
        loader = ConfigLoader()
        config = loader.load_from_string(json_str)
        assert len(config) == 1

    def test_load_from_string_invalid_json(self) -> None:
        """Test loading invalid JSON string."""
        loader = ConfigLoader()
        with pytest.raises(ConfigParseError):
            loader.load_from_string("{ not valid json }")

    def test_load_from_dict(self, sample_mcp_config: dict[str, Any]) -> None:
        """Test loading config from dictionary."""
        loader = ConfigLoader()
        config = loader.load_from_dict(sample_mcp_config)
        assert len(config) == 3

    def test_load_from_dict_invalid(self) -> None:
        """Test loading invalid dict."""
        loader = ConfigLoader()
        with pytest.raises(ConfigValidationError):
            loader.load_from_dict({"mcpServers": {"bad": {}}})

    def test_find_config_env_var(
        self, tmp_path: Path, sample_mcp_config: dict[str, Any], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test finding config via environment variable."""
        config_path = tmp_path / "custom_mcp.json"
        config_path.write_text(json.dumps(sample_mcp_config))
        monkeypatch.setenv("MCP_CONFIG_PATH", str(config_path))

        loader = ConfigLoader()
        found_path = loader.find_config()
        assert found_path == config_path

    def test_find_config_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test when no config is found."""
        # Clear env var and mock default paths
        monkeypatch.delenv("MCP_CONFIG_PATH", raising=False)

        loader = ConfigLoader()
        # Override default paths to non-existent ones
        loader.DEFAULT_CONFIG_PATHS = [Path("/nonexistent/path/mcp.json")]

        with pytest.raises(ConfigNotFoundError) as exc_info:
            loader.find_config()
        assert "Searched" in str(exc_info.value)

    def test_find_config_uses_env_before_default(
        self, tmp_path: Path, sample_mcp_config: dict[str, Any], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that env var takes priority over default paths."""
        # Create two config files
        env_config = tmp_path / "env_config.json"
        default_config = tmp_path / "default_config.json"

        env_config.write_text(json.dumps(sample_mcp_config))
        default_config.write_text(json.dumps({"mcpServers": {}}))

        monkeypatch.setenv("MCP_CONFIG_PATH", str(env_config))

        loader = ConfigLoader()
        loader.DEFAULT_CONFIG_PATHS = [default_config]

        found_path = loader.find_config()
        assert found_path == env_config

    def test_load_without_path_uses_find(
        self, tmp_path: Path, sample_mcp_config: dict[str, Any], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that load() without path uses find_config()."""
        config_path = tmp_path / "mcp.json"
        config_path.write_text(json.dumps(sample_mcp_config))
        monkeypatch.setenv("MCP_CONFIG_PATH", str(config_path))

        loader = ConfigLoader()
        config = loader.load()
        assert len(config) == 3


class TestConfigExceptions:
    """Tests for configuration exception classes."""

    def test_config_not_found_with_path(self) -> None:
        """Test ConfigNotFoundError with explicit path."""
        path = Path("/some/path/config.json")
        error = ConfigNotFoundError(path=path)
        assert str(path) in str(error)
        assert error.path == path

    def test_config_not_found_with_searched_paths(self) -> None:
        """Test ConfigNotFoundError with searched paths."""
        paths = [Path("/path1"), Path("/path2")]
        error = ConfigNotFoundError(searched_paths=paths)
        assert "Searched" in str(error)
        assert all(str(p) in str(error) for p in paths)

    def test_config_parse_error(self) -> None:
        """Test ConfigParseError message."""
        path = Path("/config.json")
        error = ConfigParseError(path, "Unexpected token")
        assert str(path) in str(error)
        assert "Unexpected token" in str(error)

    def test_config_validation_error(self) -> None:
        """Test ConfigValidationError message."""
        path = Path("/config.json")
        errors = [{"loc": ("mcpServers", "test"), "msg": "field required"}]
        error = ConfigValidationError(path, errors)
        assert str(path) in str(error)
        assert "field required" in str(error)
