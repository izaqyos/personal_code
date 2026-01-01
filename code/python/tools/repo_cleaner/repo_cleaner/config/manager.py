"""Configuration manager for Repo Cleaner."""

from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml

from repo_cleaner.config.defaults import DEFAULT_PATTERNS, DEFAULT_SAFETY, DEFAULT_EXCLUDES
from repo_cleaner.config.schema import ConfigSchema, LanguageConfig, SafetyConfig, validate_config
from repo_cleaner.core.exceptions import ConfigurationError


# Default config file names (in order of priority)
CONFIG_FILE_NAMES = [
    ".repo_cleaner.yaml",
    ".repo_cleaner.yml",
    ".repo-cleaner.yaml",
    ".repo-cleaner.yml",
    "repo_cleaner.yaml",
    "repo_cleaner.yml",
]


class ConfigManager:
    """Manager for loading and merging configurations.
    
    The configuration is loaded from:
    1. Built-in defaults (lowest priority)
    2. User config file (if found)
    3. CLI arguments (highest priority)
    """
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        target_dir: Optional[Path] = None,
    ) -> None:
        """Initialize the configuration manager.
        
        Args:
            config_path: Explicit path to config file
            target_dir: Target directory to search for config
        """
        self.config_path = config_path
        self.target_dir = target_dir or Path.cwd()
        self._config: Optional[ConfigSchema] = None
        self._raw_config: Dict[str, Any] = {}
    
    def load(self) -> ConfigSchema:
        """Load and merge all configurations.
        
        Returns:
            Merged ConfigSchema
            
        Raises:
            ConfigurationError: If config file is invalid
        """
        # Start with defaults
        self._raw_config = self._get_default_config()
        
        # Try to load user config
        user_config = self._load_user_config()
        if user_config:
            self._raw_config = self._merge_configs(self._raw_config, user_config)
        
        # Validate and create schema
        self._config = validate_config(self._raw_config)
        return self._config
    
    @property
    def config(self) -> ConfigSchema:
        """Get the loaded configuration.
        
        Returns:
            ConfigSchema (loads if not already loaded)
        """
        if self._config is None:
            self.load()
        return self._config  # type: ignore
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration as dictionary.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "exclude": list(DEFAULT_EXCLUDES),
            "languages": {
                lang: {"enabled": True, "additional_patterns": [], "exclude": []}
                for lang in DEFAULT_PATTERNS.keys()
            },
            "safety": dict(DEFAULT_SAFETY),
        }
    
    def _load_user_config(self) -> Optional[Dict[str, Any]]:
        """Load user configuration file.
        
        Returns:
            User configuration dictionary, or None if not found
            
        Raises:
            ConfigurationError: If config file exists but is invalid
        """
        config_file = self._find_config_file()
        
        if config_file is None:
            return None
        
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            
            if config is None:
                return {}
            
            if not isinstance(config, dict):
                raise ConfigurationError(
                    f"Config file must be a YAML dictionary",
                    details=f"File: {config_file}",
                )
            
            return config
        
        except yaml.YAMLError as e:
            raise ConfigurationError(
                f"Invalid YAML in config file",
                details=f"File: {config_file}\nError: {e}",
            )
        except OSError as e:
            raise ConfigurationError(
                f"Cannot read config file",
                details=f"File: {config_file}\nError: {e}",
            )
    
    def _find_config_file(self) -> Optional[Path]:
        """Find the configuration file.
        
        Searches in order:
        1. Explicit config_path (if provided)
        2. Target directory
        3. Parent directories up to home
        
        Returns:
            Path to config file, or None if not found
        """
        # Check explicit path first
        if self.config_path:
            path = Path(self.config_path)
            if path.is_file():
                return path
            raise ConfigurationError(
                f"Config file not found: {self.config_path}"
            )
        
        # Search in target directory and parents
        search_dirs = [self.target_dir]
        
        # Add parent directories (but not above home)
        home = Path.home()
        current = self.target_dir
        while current != current.parent:
            current = current.parent
            if current == home:
                search_dirs.append(current)
                break
            search_dirs.append(current)
        
        # Search for config files
        for directory in search_dirs:
            for filename in CONFIG_FILE_NAMES:
                config_path = directory / filename
                if config_path.is_file():
                    return config_path
        
        return None
    
    def _merge_configs(
        self,
        base: Dict[str, Any],
        override: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Deep merge two configuration dictionaries.
        
        Args:
            base: Base configuration
            override: Configuration to merge on top
            
        Returns:
            Merged configuration
        """
        result = dict(base)
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            elif key in result and isinstance(result[key], list) and isinstance(value, list):
                # For lists, we extend rather than replace (for exclude patterns)
                if key == "exclude":
                    result[key] = list(set(result[key] + value))
                else:
                    result[key] = value
            else:
                result[key] = value
        
        return result
    
    def get_patterns_for_language(self, language: str) -> List[Dict[str, Any]]:
        """Get all patterns for a language (defaults + additional).
        
        Args:
            language: Language name
            
        Returns:
            List of pattern definitions
        """
        patterns = list(DEFAULT_PATTERNS.get(language, []))
        
        # Add additional patterns from config
        if self._config and language in self._config.languages:
            lang_config = self._config.languages[language]
            patterns.extend(lang_config.additional_patterns)
        
        return patterns
    
    def get_exclude_patterns(self, language: Optional[str] = None) -> List[str]:
        """Get exclude patterns for a language.
        
        Args:
            language: Optional language name for language-specific excludes
            
        Returns:
            List of exclude patterns
        """
        patterns = list(self.config.exclude)
        
        if language and language in self.config.languages:
            patterns.extend(self.config.languages[language].exclude)
        
        return patterns
    
    def is_language_enabled(self, language: str) -> bool:
        """Check if a language is enabled.
        
        Args:
            language: Language name
            
        Returns:
            True if enabled
        """
        if language not in self.config.languages:
            return True  # Default to enabled
        return self.config.languages[language].enabled
    
    def get_safety_config(self) -> SafetyConfig:
        """Get safety configuration.
        
        Returns:
            SafetyConfig object
        """
        return self.config.safety

