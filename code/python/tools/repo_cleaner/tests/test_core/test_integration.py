"""Integration tests for Repo Cleaner."""

from pathlib import Path

import pytest

from repo_cleaner.config.manager import ConfigManager
from repo_cleaner.core.cleaner import RepoCleaner


class TestIntegration:
    """End-to-end integration tests."""
    
    def test_full_workflow_python(self, python_project: Path) -> None:
        """Test full cleaning workflow for Python project."""
        # Create cleaner
        cleaner = RepoCleaner(
            dry_run=False,
            interactive=False,
            verbose=False,
        )
        
        # Verify artifacts exist before cleaning
        pycache = python_project / "src" / "__pycache__"
        pytest_cache = python_project / ".pytest_cache"
        mypy_cache = python_project / ".mypy_cache"
        
        assert pycache.exists()
        assert pytest_cache.exists()
        assert mypy_cache.exists()
        
        # Clean (excluding venv to avoid confirmation)
        summary = cleaner.clean(
            python_project,
            exclude_patterns=["venv/**", "venv"]
        )
        
        # Verify results
        assert summary.success
        assert "python" in summary.detected_types
        assert summary.total_size_cleaned > 0
        
        # Verify artifacts were deleted
        assert not pycache.exists()
        assert not pytest_cache.exists()
        assert not mypy_cache.exists()
        
        # Verify source files still exist
        assert (python_project / "src" / "main.py").exists()
        assert (python_project / "pyproject.toml").exists()
    
    def test_full_workflow_node(self, node_project: Path) -> None:
        """Test full cleaning workflow for Node.js project."""
        cleaner = RepoCleaner(
            dry_run=False,
            interactive=False,
        )
        
        # Verify artifacts exist
        dist = node_project / "dist"
        cache = node_project / ".cache"
        
        assert dist.exists()
        assert cache.exists()
        
        # Clean (excluding node_modules)
        summary = cleaner.clean(
            node_project,
            exclude_patterns=["**/node_modules", "**/node_modules/**"]
        )
        
        # Verify results
        assert summary.success
        assert "node" in summary.detected_types
        
        # Verify artifacts were deleted
        assert not dist.exists()
        assert not cache.exists()
        
        # Verify source files still exist
        assert (node_project / "src" / "index.js").exists()
        assert (node_project / "package.json").exists()
    
    def test_full_workflow_cpp(self, cpp_project: Path) -> None:
        """Test full cleaning workflow for C++ project."""
        cleaner = RepoCleaner(
            dry_run=False,
            interactive=False,
        )
        
        # Verify artifacts exist
        build = cpp_project / "build"
        
        assert build.exists()
        assert (build / "main.o").exists()
        
        # Clean
        summary = cleaner.clean(cpp_project)
        
        # Verify results
        assert summary.success
        assert "c_cpp" in summary.detected_types
        
        # Verify artifacts were deleted
        assert not (build / "main.o").exists()
        
        # Verify source files still exist
        assert (cpp_project / "main.cpp").exists()
        assert (cpp_project / "CMakeLists.txt").exists()
    
    def test_dry_run_preserves_files(self, python_project: Path) -> None:
        """Test that dry-run mode doesn't delete files."""
        cleaner = RepoCleaner(
            dry_run=True,
            interactive=False,
        )
        
        # Get initial state
        pycache = python_project / "src" / "__pycache__"
        assert pycache.exists()
        initial_size = sum(
            f.stat().st_size for f in pycache.rglob("*") if f.is_file()
        )
        
        # Dry run clean
        summary = cleaner.clean(python_project)
        
        assert summary.dry_run
        assert summary.total_size_found > 0
        
        # Verify files still exist
        assert pycache.exists()
        current_size = sum(
            f.stat().st_size for f in pycache.rglob("*") if f.is_file()
        )
        assert current_size == initial_size
    
    def test_mixed_project_detection(self, mixed_project: Path) -> None:
        """Test detection and cleaning of mixed project."""
        cleaner = RepoCleaner(
            dry_run=True,
            interactive=False,
        )
        
        # Detect project types
        detected = cleaner.detect_project_types(mixed_project)
        
        # Should detect multiple types
        assert len(detected) >= 1
        
        # Clean
        summary = cleaner.clean(mixed_project)
        
        assert summary.success
        assert len(summary.detected_types) >= 1
    
    def test_exclude_patterns_work(self, python_project: Path) -> None:
        """Test that exclude patterns prevent deletion."""
        cleaner = RepoCleaner(
            dry_run=False,
            interactive=False,
        )
        
        pycache = python_project / "src" / "__pycache__"
        assert pycache.exists()
        
        # Clean with exclusion for __pycache__
        summary = cleaner.clean(
            python_project,
            exclude_patterns=["**/__pycache__", "**/__pycache__/**", "venv/**"]
        )
        
        # __pycache__ should still exist
        assert pycache.exists()
    
    def test_language_filter(self, mixed_project: Path) -> None:
        """Test filtering by specific languages."""
        cleaner = RepoCleaner(
            dry_run=True,
            interactive=False,
        )
        
        # Only clean Python
        summary = cleaner.clean(
            mixed_project,
            languages=["python"]
        )
        
        assert summary.detected_types == ["python"]
        assert "python" in summary.results
        # Should not include node
        assert "node" not in summary.results
    
    def test_empty_project_handling(self, empty_dir: Path) -> None:
        """Test handling of empty project."""
        cleaner = RepoCleaner(
            dry_run=True,
            interactive=False,
        )
        
        summary = cleaner.clean(empty_dir)
        
        assert summary.success
        assert len(summary.detected_types) == 0
        assert summary.total_size_found == 0

