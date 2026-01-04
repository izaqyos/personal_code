"""
Configuration manager for loading and persisting application settings.

This module handles reading and writing the config.json file,
providing default values when the file is missing or corrupted.
"""

import json
import logging
from pathlib import Path
from typing import Any

from filelock import FileLock

from src.core.models import AppConfig

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Manages application configuration with file persistence.

    Provides methods to load, save, and access configuration values.
    Uses file locking for safe concurrent access.
    """

    DEFAULT_CONFIG_PATH = Path("config.json")

    def __init__(self, config_path: Path | None = None) -> None:
        """
        Initialize the config manager.

        Args:
            config_path: Path to config file. Uses default if not provided.
        """
        self._config_path = config_path or self.DEFAULT_CONFIG_PATH
        self._lock_path = self._config_path.with_suffix(".lock")
        self._config: AppConfig | None = None

    @property
    def config_path(self) -> Path:
        """Return the configuration file path."""
        return self._config_path

    @property
    def config(self) -> AppConfig:
        """
        Return the current configuration, loading if necessary.

        Returns:
            The application configuration.
        """
        if self._config is None:
            self._config = self.load()
        return self._config

    def load(self) -> AppConfig:
        """
        Load configuration from file or create defaults.

        If the config file doesn't exist or is invalid, creates
        a new config with default values and saves it.

        Returns:
            The loaded or default configuration.
        """
        if not self._config_path.exists():
            logger.info(f"Config file not found at {self._config_path}, creating defaults")
            config = AppConfig.create_default()
            self._config = config
            self.save()
            return config

        try:
            with FileLock(self._lock_path):
                data = json.loads(self._config_path.read_text())
                config = AppConfig.model_validate(data)
                self._config = config
                logger.debug(f"Loaded config from {self._config_path}")
                return config
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid JSON in config file: {e}, using defaults")
            return self._handle_corrupted_config()
        except Exception as e:
            logger.warning(f"Error loading config: {e}, using defaults")
            return self._handle_corrupted_config()

    def _handle_corrupted_config(self) -> AppConfig:
        """
        Handle corrupted config by backing up and creating new defaults.

        Returns:
            A new default configuration.
        """
        if self._config_path.exists():
            backup_path = self._config_path.with_suffix(".corrupted.json")
            try:
                self._config_path.rename(backup_path)
                logger.info(f"Backed up corrupted config to {backup_path}")
            except OSError as e:
                logger.error(f"Failed to backup corrupted config: {e}")

        config = AppConfig.create_default()
        self._config = config
        self.save()
        return config

    def save(self) -> None:
        """
        Save current configuration to file atomically.

        Uses a temporary file and atomic rename for safety.
        """
        if self._config is None:
            logger.warning("No config to save")
            return

        # Ensure parent directory exists
        self._config_path.parent.mkdir(parents=True, exist_ok=True)

        temp_path = self._config_path.with_suffix(".tmp")
        try:
            with FileLock(self._lock_path):
                # Write to temp file first
                data = self._config.model_dump(mode="json")
                temp_path.write_text(json.dumps(data, indent=2))
                # Atomic rename
                temp_path.replace(self._config_path)
                logger.debug(f"Saved config to {self._config_path}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            # Clean up temp file if it exists
            if temp_path.exists():
                temp_path.unlink()
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by dot-notation key.

        Args:
            key: Dot-notation key (e.g., "timer.default_speaker_time_seconds")
            default: Default value if key not found.

        Returns:
            The configuration value or default.
        """
        config = self.config
        obj: Any = config

        for part in key.split("."):
            if hasattr(obj, part):
                obj = getattr(obj, part)
            elif isinstance(obj, dict) and part in obj:
                obj = obj[part]
            else:
                return default
        return obj

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value by dot-notation key.

        Note: This modifies the in-memory config. Call save() to persist.

        Args:
            key: Dot-notation key (e.g., "timer.default_speaker_time_seconds")
            value: The value to set.

        Raises:
            ValueError: If the key path is invalid.
        """
        config = self.config
        parts = key.split(".")

        # Navigate to parent object
        obj: Any = config
        for part in parts[:-1]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                raise ValueError(f"Invalid config key: {key}")

        # Set the final attribute
        final_key = parts[-1]
        if hasattr(obj, final_key):
            setattr(obj, final_key, value)
        else:
            raise ValueError(f"Invalid config key: {key}")

    def reload(self) -> AppConfig:
        """
        Force reload configuration from file.

        Returns:
            The reloaded configuration.
        """
        self._config = None
        return self.load()

    def reset_to_defaults(self) -> AppConfig:
        """
        Reset configuration to default values.

        Returns:
            The default configuration.
        """
        self._config = AppConfig.create_default()
        self.save()
        return self._config
