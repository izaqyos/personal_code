"""Configuration loader for MCP Health Check."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from mcp_health.config.models import MCPConfig


class ConfigError(Exception):
    """Base exception for configuration errors."""

    pass


class ConfigNotFoundError(ConfigError):
    """Configuration file not found."""

    def __init__(self, path: Path | None = None, searched_paths: list[Path] | None = None):
        self.path = path
        self.searched_paths = searched_paths or []
        if path:
            message = f"Configuration file not found: {path}"
        else:
            paths_str = ", ".join(str(p) for p in self.searched_paths)
            message = f"Configuration file not found. Searched: {paths_str}"
        super().__init__(message)


class ConfigParseError(ConfigError):
    """Configuration file could not be parsed."""

    def __init__(self, path: Path, error: str):
        self.path = path
        self.error = error
        super().__init__(f"Failed to parse configuration at {path}: {error}")


class ConfigValidationError(ConfigError):
    """Configuration validation failed."""

    def __init__(self, path: Path, errors: list[dict[str, Any]]):
        self.path = path
        self.errors = errors
        error_messages = "; ".join(
            f"{e.get('loc', 'unknown')}: {e.get('msg', 'unknown error')}" for e in errors
        )
        super().__init__(f"Configuration validation failed at {path}: {error_messages}")


class ConfigLoader:
    """Loads and validates MCP configuration files.

    The loader searches for configuration in the following order:
    1. Explicit path provided to load()
    2. MCP_CONFIG_PATH environment variable
    3. ~/.cursor/mcp.json (default Cursor location)

    Example:
        loader = ConfigLoader()
        config = loader.load()  # Auto-discovers config

        # Or with explicit path
        config = loader.load(Path("/path/to/mcp.json"))
    """

    DEFAULT_CONFIG_PATHS = [
        Path.home() / ".cursor" / "mcp.json",
    ]
    ENV_VAR_NAME = "MCP_CONFIG_PATH"

    def find_config(self) -> Path:
        """Find the configuration file in default locations.

        Searches in order:
        1. MCP_CONFIG_PATH environment variable
        2. Default paths (~/.cursor/mcp.json)

        Returns:
            Path to the configuration file

        Raises:
            ConfigNotFoundError: If no configuration file is found
        """
        searched_paths: list[Path] = []

        # Check environment variable first
        env_path = os.environ.get(self.ENV_VAR_NAME)
        if env_path:
            path = Path(env_path)
            searched_paths.append(path)
            if path.exists():
                return path

        # Check default paths
        for default_path in self.DEFAULT_CONFIG_PATHS:
            searched_paths.append(default_path)
            if default_path.exists():
                return default_path

        raise ConfigNotFoundError(searched_paths=searched_paths)

    def load(self, path: Path | None = None) -> MCPConfig:
        """Load and validate MCP configuration.

        Args:
            path: Optional explicit path to config file. If not provided,
                  will search default locations.

        Returns:
            Validated MCPConfig object

        Raises:
            ConfigNotFoundError: If configuration file not found
            ConfigParseError: If JSON parsing fails
            ConfigValidationError: If configuration validation fails
        """
        if path is None:
            path = self.find_config()
        elif not path.exists():
            raise ConfigNotFoundError(path=path)

        return self._load_from_path(path)

    def load_from_string(self, content: str, source: str = "<string>") -> MCPConfig:
        """Load configuration from a JSON string.

        Args:
            content: JSON string containing configuration
            source: Source identifier for error messages

        Returns:
            Validated MCPConfig object

        Raises:
            ConfigParseError: If JSON parsing fails
            ConfigValidationError: If configuration validation fails
        """
        source_path = Path(source)
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ConfigParseError(source_path, str(e)) from e

        return self._validate_config(data, source_path)

    def load_from_dict(self, data: dict[str, Any], source: str = "<dict>") -> MCPConfig:
        """Load configuration from a dictionary.

        Args:
            data: Dictionary containing configuration
            source: Source identifier for error messages

        Returns:
            Validated MCPConfig object

        Raises:
            ConfigValidationError: If configuration validation fails
        """
        return self._validate_config(data, Path(source))

    def _load_from_path(self, path: Path) -> MCPConfig:
        """Load configuration from a file path.

        Args:
            path: Path to the configuration file

        Returns:
            Validated MCPConfig object
        """
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as e:
            raise ConfigParseError(path, f"Failed to read file: {e}") from e

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ConfigParseError(path, str(e)) from e

        return self._validate_config(data, path)

    def _validate_config(self, data: dict[str, Any], path: Path) -> MCPConfig:
        """Validate configuration data using Pydantic.

        Args:
            data: Configuration dictionary
            path: Source path for error messages

        Returns:
            Validated MCPConfig object
        """
        try:
            return MCPConfig.model_validate(data)
        except ValidationError as e:
            raise ConfigValidationError(path, e.errors()) from e  # type: ignore[arg-type]
