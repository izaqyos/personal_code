"""Tests for monorepo scanning and cleaning."""

import json
from pathlib import Path

import pytest

from repo_cleaner.core.scanner import MonorepoScanner, ScanLayout, DetectedProject
from repo_cleaner.core.layout import LayoutManager, get_layout_path
from repo_cleaner.core.history import HistoryManager, CleanupReport, generate_report_id
from repo_cleaner.core.monorepo_cleaner import MonorepoCleaner


class TestMonorepoScanner:
    """Tests for MonorepoScanner."""
    
    def test_scan_empty_directory(self, temp_dir: Path) -> None:
        """Test scanning empty directory."""
        scanner = MonorepoScanner()
        layout = scanner.scan(temp_dir)
        
        assert layout.root_path == str(temp_dir)
        assert layout.total_projects == 0
        assert len(layout.projects) == 0
    
    def test_scan_single_project(self, python_project: Path) -> None:
        """Test scanning single project."""
        scanner = MonorepoScanner()
        layout = scanner.scan(python_project)
        
        assert layout.total_projects >= 1
        assert "python" in layout.languages_found
    
    def test_scan_monorepo(self, mixed_project: Path) -> None:
        """Test scanning monorepo with multiple projects."""
        scanner = MonorepoScanner()
        layout = scanner.scan(mixed_project)
        
        # Should find projects in subdirectories
        assert layout.total_projects >= 1
    
    def test_scan_with_language_filter(self, mixed_project: Path) -> None:
        """Test scanning with language filter."""
        # Only scan for Python
        scanner = MonorepoScanner(enabled_languages=["python"])
        layout = scanner.scan(mixed_project)
        
        # Should only find Python projects
        for project in layout.projects:
            assert "python" in project.project_types or len(project.project_types) == 0
    
    def test_scan_max_depth(self, temp_dir: Path) -> None:
        """Test max depth limit."""
        # Create deeply nested project
        deep_path = temp_dir / "a" / "b" / "c" / "d" / "e"
        deep_path.mkdir(parents=True)
        (deep_path / "pyproject.toml").write_text("[project]")
        
        # Scan with low max depth
        scanner = MonorepoScanner(max_depth=2)
        layout = scanner.scan(temp_dir)
        
        # Should not find the deep project
        deep_paths = [p for p in layout.projects if "e" in p.relative_path]
        assert len(deep_paths) == 0
    
    def test_detected_project_to_dict(self) -> None:
        """Test DetectedProject serialization."""
        project = DetectedProject(
            path="/test/path",
            relative_path="path",
            project_types=["python"],
            confidence={"python": 0.9},
            indicators={"python": ["Found pyproject.toml"]},
            depth=1,
        )
        
        data = project.to_dict()
        restored = DetectedProject.from_dict(data)
        
        assert restored.path == project.path
        assert restored.project_types == project.project_types
        assert restored.confidence == project.confidence
    
    def test_scan_layout_to_dict(self, python_project: Path) -> None:
        """Test ScanLayout serialization."""
        scanner = MonorepoScanner()
        layout = scanner.scan(python_project)
        
        data = layout.to_dict()
        restored = ScanLayout.from_dict(data)
        
        assert restored.root_path == layout.root_path
        assert restored.total_projects == layout.total_projects
        assert len(restored.projects) == len(layout.projects)


class TestLayoutManager:
    """Tests for LayoutManager."""
    
    def test_save_and_load_layout(self, python_project: Path, temp_dir: Path) -> None:
        """Test saving and loading layout."""
        scanner = MonorepoScanner()
        layout = scanner.scan(python_project)
        
        manager = LayoutManager()
        manager.save_layout(layout)
        
        loaded = manager.load_layout(python_project)
        
        assert loaded is not None
        assert loaded.root_path == layout.root_path
        assert loaded.total_projects == layout.total_projects
    
    def test_load_nonexistent_layout(self, temp_dir: Path) -> None:
        """Test loading non-existent layout."""
        manager = LayoutManager()
        loaded = manager.load_layout(temp_dir / "nonexistent")
        
        assert loaded is None
    
    def test_delete_layout(self, python_project: Path) -> None:
        """Test deleting layout."""
        scanner = MonorepoScanner()
        layout = scanner.scan(python_project)
        
        manager = LayoutManager()
        manager.save_layout(layout)
        
        # Verify it exists
        assert manager.load_layout(python_project) is not None
        
        # Delete
        result = manager.delete_layout(python_project)
        assert result is True
        
        # Verify deleted
        assert manager.load_layout(python_project) is None


class TestHistoryManager:
    """Tests for HistoryManager."""
    
    def test_add_and_get_report(self, temp_dir: Path) -> None:
        """Test adding and retrieving report."""
        history_file = temp_dir / "history.json"
        manager = HistoryManager(history_file=history_file)
        
        report = CleanupReport(
            id=generate_report_id(),
            timestamp="2024-01-01T12:00:00",
            root_path="/test/path",
            total_projects=5,
            total_items=100,
            total_size=1024 * 1024,
        )
        
        manager.add_report(report)
        
        reports = manager.get_history()
        assert len(reports) == 1
        assert reports[0].id == report.id
    
    def test_max_entries_limit(self, temp_dir: Path) -> None:
        """Test that history respects max entries."""
        history_file = temp_dir / "history.json"
        manager = HistoryManager(history_file=history_file, max_entries=5)
        
        # Add 10 reports
        for i in range(10):
            report = CleanupReport(
                id=f"report_{i}",
                timestamp=f"2024-01-0{i+1}T12:00:00",
                root_path="/test/path",
            )
            manager.add_report(report)
        
        # Should only have 5
        reports = manager.get_history()
        assert len(reports) == 5
        
        # Should have the newest ones
        assert "report_9" in [r.id for r in reports]
        assert "report_0" not in [r.id for r in reports]
    
    def test_get_report_by_id(self, temp_dir: Path) -> None:
        """Test getting report by ID."""
        history_file = temp_dir / "history.json"
        manager = HistoryManager(history_file=history_file)
        
        report = CleanupReport(
            id="test_id_123",
            timestamp="2024-01-01T12:00:00",
            root_path="/test/path",
        )
        manager.add_report(report)
        
        found = manager.get_report("test_id_123")
        assert found is not None
        assert found.id == "test_id_123"
        
        not_found = manager.get_report("nonexistent")
        assert not_found is None
    
    def test_get_stats(self, temp_dir: Path) -> None:
        """Test getting statistics."""
        history_file = temp_dir / "history.json"
        manager = HistoryManager(history_file=history_file)
        
        # Add some reports
        for i, dry_run in enumerate([True, False, False]):
            report = CleanupReport(
                id=f"report_{i}",
                timestamp=f"2024-01-0{i+1}T12:00:00",
                root_path="/test/path",
                total_items=10,
                total_size=1024,
                dry_run=dry_run,
            )
            manager.add_report(report)
        
        stats = manager.get_stats()
        assert stats["total_cleanups"] == 3
        assert stats["dry_runs"] == 1
        assert stats["actual_cleanups"] == 2
        assert stats["total_items_cleaned"] == 30
    
    def test_clear_history(self, temp_dir: Path) -> None:
        """Test clearing history."""
        history_file = temp_dir / "history.json"
        manager = HistoryManager(history_file=history_file)
        
        # Add some reports
        for i in range(5):
            report = CleanupReport(
                id=f"report_{i}",
                timestamp="2024-01-01T12:00:00",
                root_path="/test/path",
            )
            manager.add_report(report)
        
        # Clear
        count = manager.clear_history()
        assert count == 5
        
        # Verify empty
        reports = manager.get_history()
        assert len(reports) == 0


class TestMonorepoCleaner:
    """Tests for MonorepoCleaner."""
    
    def test_clean_dry_run(self, python_project: Path) -> None:
        """Test dry run cleaning."""
        cleaner = MonorepoCleaner(
            dry_run=True,
            force=True,  # Skip prompts for testing
        )
        
        report = cleaner.clean(python_project)
        
        assert report.dry_run is True
        assert report.total_projects >= 0
    
    def test_clean_with_language_filter(self, mixed_project: Path) -> None:
        """Test cleaning with language filter."""
        cleaner = MonorepoCleaner(
            dry_run=True,
            force=True,
        )
        
        report = cleaner.clean(mixed_project, languages=["python"])
        
        assert report.dry_run is True
        # All cleaned projects should be Python
        for proj_report in report.project_reports:
            if proj_report.items_cleaned > 0:
                assert "python" in proj_report.project_types
    
    def test_report_saved_to_history(self, python_project: Path, temp_dir: Path) -> None:
        """Test that reports are saved to history."""
        cleaner = MonorepoCleaner(
            dry_run=True,
            force=True,
        )
        
        report = cleaner.clean(python_project)
        
        # Check history
        history = cleaner.history_manager.get_history()
        assert len(history) >= 1
        assert history[0].id == report.id

