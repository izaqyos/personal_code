"""Tests for configuration manager."""

from pathlib import Path

import pytest
import yaml

from repo_cleaner.config.manager import ConfigManager
from repo_cleaner.config.schema import ConfigSchema
from repo_cleaner.core.exceptions import ConfigurationError


class TestConfigManager:
    """Tests for ConfigManager."""
    
    def test_default_config(self, temp_dir: Path) -> None:
        """Test loading default configuration."""
        manager = ConfigManager(target_dir=temp_dir)
        config = manager.load()
        
        assert isinstance(config, ConfigSchema)
        assert config.safety.require_git is False
        assert config.safety.min_free_space_mb >= 0
    
    def test_load_user_config(self, temp_dir: Path) -> None:
        """Test loading user configuration file."""
        # Create config file
        config_file = temp_dir / ".repo_cleaner.yaml"
        config_file.write_text(yaml.dump({
            "exclude": ["vendor/**"],
            "safety": {
                "require_git": True,
                "min_free_space_mb": 500
            }
        }))
        
        manager = ConfigManager(target_dir=temp_dir)
        config = manager.load()
        
        assert "vendor/**" in config.exclude
        assert config.safety.require_git is True
        assert config.safety.min_free_space_mb == 500
    
    def test_explicit_config_path(self, temp_dir: Path) -> None:
        """Test loading config from explicit path."""
        config_file = temp_dir / "custom_config.yaml"
        config_file.write_text(yaml.dump({
            "safety": {"require_git": True}
        }))
        
        manager = ConfigManager(config_path=config_file)
        config = manager.load()
        
        assert config.safety.require_git is True
    
    def test_invalid_config_path(self, temp_dir: Path) -> None:
        """Test error when config path doesn't exist."""
        manager = ConfigManager(
            config_path=temp_dir / "nonexistent.yaml"
        )
        
        with pytest.raises(ConfigurationError):
            manager.load()
    
    def test_invalid_yaml(self, temp_dir: Path) -> None:
        """Test error with invalid YAML."""
        config_file = temp_dir / ".repo_cleaner.yaml"
        config_file.write_text("invalid: yaml: content: [")
        
        manager = ConfigManager(target_dir=temp_dir)
        
        with pytest.raises(ConfigurationError):
            manager.load()
    
    def test_language_enabled(self, temp_dir: Path) -> None:
        """Test checking if language is enabled."""
        config_file = temp_dir / ".repo_cleaner.yaml"
        config_file.write_text(yaml.dump({
            "languages": {
                "python": {"enabled": True},
                "node": {"enabled": False}
            }
        }))
        
        manager = ConfigManager(target_dir=temp_dir)
        manager.load()
        
        assert manager.is_language_enabled("python") is True
        assert manager.is_language_enabled("node") is False
        # Unknown language defaults to enabled
        assert manager.is_language_enabled("unknown") is True
    
    def test_get_exclude_patterns(self, temp_dir: Path) -> None:
        """Test getting exclude patterns."""
        config_file = temp_dir / ".repo_cleaner.yaml"
        config_file.write_text(yaml.dump({
            "exclude": ["vendor/**"],
            "languages": {
                "python": {"exclude": ["custom_cache/**"]}
            }
        }))
        
        manager = ConfigManager(target_dir=temp_dir)
        manager.load()
        
        # Global excludes
        global_excludes = manager.get_exclude_patterns()
        assert "vendor/**" in global_excludes
        
        # Language-specific excludes
        python_excludes = manager.get_exclude_patterns("python")
        assert "vendor/**" in python_excludes
        assert "custom_cache/**" in python_excludes
    
    def test_get_patterns_for_language(self, temp_dir: Path) -> None:
        """Test getting patterns for a language."""
        manager = ConfigManager(target_dir=temp_dir)
        manager.load()
        
        python_patterns = manager.get_patterns_for_language("python")
        assert len(python_patterns) > 0
        
        # Unknown language returns empty
        unknown_patterns = manager.get_patterns_for_language("unknown")
        assert len(unknown_patterns) == 0
    
    def test_safety_config(self, temp_dir: Path) -> None:
        """Test getting safety configuration."""
        config_file = temp_dir / ".repo_cleaner.yaml"
        config_file.write_text(yaml.dump({
            "safety": {
                "require_git": True,
                "min_free_space_mb": 1000,
                "max_delete_size_mb": 5000
            }
        }))
        
        manager = ConfigManager(target_dir=temp_dir)
        manager.load()
        
        safety = manager.get_safety_config()
        assert safety.require_git is True
        assert safety.min_free_space_mb == 1000
        assert safety.max_delete_size_mb == 5000
    
    def test_config_search_parent_dirs(self, temp_dir: Path) -> None:
        """Test config file search in parent directories."""
        # Create subdirectory
        subdir = temp_dir / "projects" / "myproject"
        subdir.mkdir(parents=True)
        
        # Create config in parent
        config_file = temp_dir / ".repo_cleaner.yaml"
        config_file.write_text(yaml.dump({
            "safety": {"require_git": True}
        }))
        
        # Search from subdirectory
        manager = ConfigManager(target_dir=subdir)
        config = manager.load()
        
        # Should find config from parent
        assert config.safety.require_git is True

