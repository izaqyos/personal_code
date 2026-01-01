"""Configuration schema validation for Repo Cleaner."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path

from repo_cleaner.core.exceptions import ConfigurationError


@dataclass
class LanguageConfig:
    """Configuration for a specific language cleaner.
    
    Attributes:
        enabled: Whether this language cleaner is enabled
        additional_patterns: Additional patterns to clean
        exclude: Patterns to exclude for this language
    """
    enabled: bool = True
    additional_patterns: List[Dict[str, Any]] = field(default_factory=list)
    exclude: List[str] = field(default_factory=list)


@dataclass
class SafetyConfig:
    """Safety configuration settings.
    
    Attributes:
        require_git: Require directory to be a git repository
        min_free_space_mb: Minimum free disk space in MB
        max_delete_size_mb: Maximum size to delete in MB (0 = no limit)
    """
    require_git: bool = False
    min_free_space_mb: int = 100
    max_delete_size_mb: int = 0


@dataclass
class ConfigSchema:
    """Complete configuration schema.
    
    Attributes:
        exclude: Global exclude patterns
        languages: Language-specific configurations
        safety: Safety settings
    """
    exclude: List[str] = field(default_factory=list)
    languages: Dict[str, LanguageConfig] = field(default_factory=dict)
    safety: SafetyConfig = field(default_factory=SafetyConfig)


def validate_pattern(pattern: Dict[str, Any]) -> bool:
    """Validate a pattern definition.
    
    Args:
        pattern: Pattern dictionary to validate
        
    Returns:
        True if valid
        
    Raises:
        ConfigurationError: If pattern is invalid
    """
    required_keys = ["name", "patterns", "type"]
    
    for key in required_keys:
        if key not in pattern:
            raise ConfigurationError(
                f"Pattern missing required key: {key}",
                details=f"Pattern: {pattern}",
            )
    
    if not isinstance(pattern["patterns"], list):
        raise ConfigurationError(
            f"Pattern 'patterns' must be a list",
            details=f"Got: {type(pattern['patterns']).__name__}",
        )
    
    valid_types = ["file", "directory", "both"]
    if pattern["type"] not in valid_types:
        raise ConfigurationError(
            f"Invalid pattern type: {pattern['type']}",
            details=f"Valid types: {valid_types}",
        )
    
    return True


def validate_config(config: Dict[str, Any]) -> ConfigSchema:
    """Validate and parse configuration dictionary.
    
    Args:
        config: Raw configuration dictionary
        
    Returns:
        Validated ConfigSchema object
        
    Raises:
        ConfigurationError: If configuration is invalid
    """
    try:
        # Parse exclude patterns
        exclude = config.get("exclude", [])
        if not isinstance(exclude, list):
            raise ConfigurationError("'exclude' must be a list of patterns")
        
        # Parse language configurations
        languages: Dict[str, LanguageConfig] = {}
        raw_languages = config.get("languages", {})
        
        if not isinstance(raw_languages, dict):
            raise ConfigurationError("'languages' must be a dictionary")
        
        for lang_name, lang_config in raw_languages.items():
            if lang_config is None:
                lang_config = {}
            
            if not isinstance(lang_config, dict):
                raise ConfigurationError(
                    f"Language config for '{lang_name}' must be a dictionary"
                )
            
            # Validate additional patterns
            additional_patterns = lang_config.get("additional_patterns", [])
            for pattern in additional_patterns:
                validate_pattern(pattern)
            
            languages[lang_name] = LanguageConfig(
                enabled=lang_config.get("enabled", True),
                additional_patterns=additional_patterns,
                exclude=lang_config.get("exclude", []),
            )
        
        # Parse safety settings
        raw_safety = config.get("safety", {})
        if not isinstance(raw_safety, dict):
            raise ConfigurationError("'safety' must be a dictionary")
        
        safety = SafetyConfig(
            require_git=raw_safety.get("require_git", False),
            min_free_space_mb=raw_safety.get("min_free_space_mb", 100),
            max_delete_size_mb=raw_safety.get("max_delete_size_mb", 0),
        )
        
        # Validate safety values
        if safety.min_free_space_mb < 0:
            raise ConfigurationError("'min_free_space_mb' must be non-negative")
        if safety.max_delete_size_mb < 0:
            raise ConfigurationError("'max_delete_size_mb' must be non-negative")
        
        return ConfigSchema(
            exclude=exclude,
            languages=languages,
            safety=safety,
        )
    
    except ConfigurationError:
        raise
    except Exception as e:
        raise ConfigurationError(
            "Failed to parse configuration",
            details=str(e),
        )


def get_default_schema() -> ConfigSchema:
    """Get a default configuration schema.
    
    Returns:
        ConfigSchema with default values
    """
    return ConfigSchema()

