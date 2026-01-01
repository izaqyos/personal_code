"""Configuration management for Repo Cleaner."""

from repo_cleaner.config.manager import ConfigManager
from repo_cleaner.config.defaults import DEFAULT_PATTERNS
from repo_cleaner.config.schema import ConfigSchema, validate_config

__all__ = [
    "ConfigManager",
    "DEFAULT_PATTERNS",
    "ConfigSchema",
    "validate_config",
]

