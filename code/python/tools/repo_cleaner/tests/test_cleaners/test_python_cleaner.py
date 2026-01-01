"""Tests for Python project cleaner."""

from pathlib import Path

import pytest

from repo_cleaner.cleaners.python import PythonCleaner
from repo_cleaner.cleaners.base import PatternType


class TestPythonCleaner:
    """Tests for PythonCleaner."""
    
    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.cleaner = PythonCleaner()
    
    def test_name(self) -> None:
        """Test cleaner name."""
        assert self.cleaner.name == "python"
        assert self.cleaner.display_name == "Python"
    
    def test_patterns(self) -> None:
        """Test pattern definitions."""
        patterns = self.cleaner.get_patterns()
        assert len(patterns) > 0
        
        # Check for essential patterns
        pattern_names = [p.name for p in patterns]
        assert "Python Cache" in pattern_names
        assert "Compiled Python Files" in pattern_names
        assert "Pytest Cache" in pattern_names
        assert "Virtual Environments" in pattern_names
    
    def test_venv_requires_confirmation(self) -> None:
        """Test that venv pattern requires confirmation."""
        patterns = self.cleaner.get_patterns()
        venv_pattern = next(p for p in patterns if p.name == "Virtual Environments")
        assert venv_pattern.requires_confirmation is True
        assert venv_pattern.safe is False
    
    def test_find_items_pycache(self, python_project: Path) -> None:
        """Test finding __pycache__ directories."""
        items = self.cleaner.find_items(python_project)
        pycache_items = [i for i in items if "__pycache__" in str(i.path)]
        assert len(pycache_items) > 0
        assert all(i.is_directory for i in pycache_items)
    
    def test_find_items_pytest_cache(self, python_project: Path) -> None:
        """Test finding .pytest_cache directory."""
        items = self.cleaner.find_items(python_project)
        pytest_items = [i for i in items if ".pytest_cache" in str(i.path)]
        assert len(pytest_items) > 0
    
    def test_find_items_mypy_cache(self, python_project: Path) -> None:
        """Test finding .mypy_cache directory."""
        items = self.cleaner.find_items(python_project)
        mypy_items = [i for i in items if ".mypy_cache" in str(i.path)]
        assert len(mypy_items) > 0
    
    def test_find_items_with_exclusions(self, python_project: Path) -> None:
        """Test finding items with exclusions."""
        all_items = self.cleaner.find_items(python_project)
        
        # Exclude __pycache__
        excluded_items = self.cleaner.find_items(
            python_project,
            exclude_patterns=["**/__pycache__"]
        )
        
        assert len(excluded_items) < len(all_items)
        assert not any("__pycache__" in str(i.path) for i in excluded_items)
    
    def test_clean_dry_run(self, python_project: Path) -> None:
        """Test dry run cleaning."""
        # Get initial items
        items_before = self.cleaner.find_items(python_project)
        assert len(items_before) > 0
        
        # Dry run clean
        result = self.cleaner.clean(python_project, dry_run=True)
        
        assert result.dry_run is True
        assert result.cleaner_name == "python"
        assert len(result.items_cleaned) > 0
        assert result.total_size_cleaned > 0
        
        # Verify nothing was actually deleted
        items_after = self.cleaner.find_items(python_project)
        assert len(items_after) == len(items_before)
    
    def test_clean_actual(self, python_project: Path) -> None:
        """Test actual cleaning."""
        # Exclude venv to avoid confirmation issues
        items_before = self.cleaner.find_items(
            python_project,
            exclude_patterns=["venv/**", "venv"]
        )
        assert len(items_before) > 0
        
        # Actual clean
        result = self.cleaner.clean(
            python_project,
            dry_run=False,
            exclude_patterns=["venv/**", "venv"]
        )
        
        assert result.dry_run is False
        assert result.cleaner_name == "python"
        assert len(result.items_cleaned) > 0
        
        # Verify items were deleted
        items_after = self.cleaner.find_items(
            python_project,
            exclude_patterns=["venv/**", "venv"]
        )
        assert len(items_after) < len(items_before)
    
    def test_clean_empty_project(self, empty_dir: Path) -> None:
        """Test cleaning empty project."""
        result = self.cleaner.clean(empty_dir, dry_run=True)
        
        assert result.cleaner_name == "python"
        assert len(result.items_found) == 0
        assert len(result.items_cleaned) == 0
        assert result.total_size_cleaned == 0
    
    def test_clean_result_properties(self, python_project: Path) -> None:
        """Test CleanResult properties."""
        result = self.cleaner.clean(
            python_project,
            dry_run=True,
            exclude_patterns=["venv/**"]
        )
        
        assert result.items_count == len(result.items_found)
        assert result.cleaned_count == len(result.items_cleaned)
        assert result.success is True  # No errors in dry run

