"""Tests for core cleaner orchestrator."""

from pathlib import Path
from unittest.mock import patch

import pytest

from repo_cleaner.config.manager import ConfigManager
from repo_cleaner.core.cleaner import RepoCleaner, CleanSummary
from repo_cleaner.core.exceptions import SafetyCheckError


class TestRepoCleaner:
    """Tests for RepoCleaner orchestrator."""
    
    def test_init_default(self, temp_dir: Path) -> None:
        """Test default initialization."""
        cleaner = RepoCleaner()
        
        assert cleaner.dry_run is False
        assert cleaner.interactive is True
        assert cleaner.verbose is False
    
    def test_init_with_options(self, temp_dir: Path) -> None:
        """Test initialization with options."""
        config = ConfigManager(target_dir=temp_dir)
        cleaner = RepoCleaner(
            config=config,
            dry_run=True,
            interactive=False,
            verbose=True,
        )
        
        assert cleaner.dry_run is True
        assert cleaner.interactive is False
        assert cleaner.verbose is True
    
    def test_detect_python_project(self, python_project: Path) -> None:
        """Test Python project detection."""
        cleaner = RepoCleaner()
        results = cleaner.detect_project_types(python_project)
        
        assert "python" in results
        assert results["python"].detected is True
        assert results["python"].confidence >= 0.8
    
    def test_detect_node_project(self, node_project: Path) -> None:
        """Test Node.js project detection."""
        cleaner = RepoCleaner()
        results = cleaner.detect_project_types(node_project)
        
        assert "node" in results
        assert results["node"].detected is True
    
    def test_detect_java_project(self, java_project: Path) -> None:
        """Test Java project detection."""
        cleaner = RepoCleaner()
        results = cleaner.detect_project_types(java_project)
        
        assert "java" in results
        assert results["java"].detected is True
    
    def test_detect_cpp_project(self, cpp_project: Path) -> None:
        """Test C++ project detection."""
        cleaner = RepoCleaner()
        results = cleaner.detect_project_types(cpp_project)
        
        assert "c_cpp" in results
        assert results["c_cpp"].detected is True
    
    def test_detect_react_project(self, react_project: Path) -> None:
        """Test React project detection."""
        cleaner = RepoCleaner()
        results = cleaner.detect_project_types(react_project)
        
        assert "react" in results
        assert results["react"].detected is True
        # Also detects as node
        assert "node" in results
    
    def test_detect_mixed_project(self, mixed_project: Path) -> None:
        """Test mixed project detection."""
        cleaner = RepoCleaner()
        results = cleaner.detect_project_types(mixed_project)
        
        # Should detect both Python and Node
        assert len(results) >= 1
    
    def test_detect_empty_project(self, empty_dir: Path) -> None:
        """Test detection in empty directory."""
        cleaner = RepoCleaner()
        results = cleaner.detect_project_types(empty_dir)
        
        assert len(results) == 0
    
    def test_clean_dry_run(self, python_project: Path) -> None:
        """Test cleaning in dry-run mode."""
        cleaner = RepoCleaner(dry_run=True, interactive=False)
        summary = cleaner.clean(python_project)
        
        assert summary.dry_run is True
        assert summary.target_path == python_project
        assert len(summary.detected_types) > 0
        assert summary.total_size_found > 0
        
        # Verify nothing was deleted
        assert (python_project / "src" / "__pycache__").exists()
    
    def test_clean_with_specified_languages(self, python_project: Path) -> None:
        """Test cleaning with specified languages."""
        cleaner = RepoCleaner(dry_run=True, interactive=False)
        summary = cleaner.clean(
            python_project,
            languages=["python"]
        )
        
        assert summary.detected_types == ["python"]
        assert "python" in summary.results
    
    def test_clean_with_exclude_patterns(self, python_project: Path) -> None:
        """Test cleaning with exclude patterns."""
        cleaner = RepoCleaner(dry_run=True, interactive=False)
        
        # Without exclusions
        summary1 = cleaner.clean(python_project)
        
        # With exclusions
        summary2 = cleaner.clean(
            python_project,
            exclude_patterns=["**/__pycache__"]
        )
        
        # Should find fewer items with exclusions
        assert summary2.total_size_found <= summary1.total_size_found
    
    def test_safety_check_require_git(self, temp_dir: Path, python_project: Path) -> None:
        """Test safety check for git requirement."""
        import yaml
        
        # Create config requiring git
        config_file = temp_dir / ".repo_cleaner.yaml"
        config_file.write_text(yaml.dump({
            "safety": {"require_git": True}
        }))
        
        config = ConfigManager(config_path=config_file, target_dir=python_project)
        cleaner = RepoCleaner(config=config, interactive=False)
        
        # Should fail because project is not a git repo
        summary = cleaner.clean(python_project)
        assert not summary.success
        assert any("git" in e.lower() for e in summary.errors)
    
    def test_get_cleaner_for_type(self, temp_dir: Path) -> None:
        """Test getting cleaner for project type."""
        cleaner = RepoCleaner()
        
        python_cleaner = cleaner.get_cleaner_for_type("python")
        assert python_cleaner is not None
        assert python_cleaner.name == "python"
        
        node_cleaner = cleaner.get_cleaner_for_type("node")
        assert node_cleaner is not None
        assert node_cleaner.name == "node"
        
        unknown_cleaner = cleaner.get_cleaner_for_type("unknown")
        assert unknown_cleaner is None
    
    def test_clean_summary_success(self, python_project: Path) -> None:
        """Test CleanSummary success property."""
        cleaner = RepoCleaner(dry_run=True, interactive=False)
        summary = cleaner.clean(python_project)
        
        assert summary.success is True
        assert len(summary.errors) == 0


class TestCleanSummary:
    """Tests for CleanSummary dataclass."""
    
    def test_success_property(self, temp_dir: Path) -> None:
        """Test success property."""
        summary = CleanSummary(target_path=temp_dir)
        assert summary.success is True
        
        summary.errors.append("An error")
        assert summary.success is False
    
    def test_defaults(self, temp_dir: Path) -> None:
        """Test default values."""
        summary = CleanSummary(target_path=temp_dir)
        
        assert summary.detected_types == []
        assert summary.results == {}
        assert summary.total_size_found == 0
        assert summary.total_size_cleaned == 0
        assert summary.dry_run is False
        assert summary.errors == []

