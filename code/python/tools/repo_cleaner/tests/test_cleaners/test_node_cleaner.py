"""Tests for Node.js project cleaner."""

from pathlib import Path

import pytest

from repo_cleaner.cleaners.node import NodeCleaner


class TestNodeCleaner:
    """Tests for NodeCleaner."""
    
    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.cleaner = NodeCleaner()
    
    def test_name(self) -> None:
        """Test cleaner name."""
        assert self.cleaner.name == "node"
        assert self.cleaner.display_name == "Node.js"
    
    def test_patterns(self) -> None:
        """Test pattern definitions."""
        patterns = self.cleaner.get_patterns()
        assert len(patterns) > 0
        
        pattern_names = [p.name for p in patterns]
        assert "Node Modules" in pattern_names
        assert "Distribution Directory" in pattern_names
        assert "Build Output" in pattern_names
    
    def test_node_modules_requires_confirmation(self) -> None:
        """Test that node_modules pattern requires confirmation."""
        patterns = self.cleaner.get_patterns()
        nm_pattern = next(p for p in patterns if p.name == "Node Modules")
        assert nm_pattern.requires_confirmation is True
    
    def test_find_items_node_modules(self, node_project: Path) -> None:
        """Test finding node_modules."""
        items = self.cleaner.find_items(node_project)
        nm_items = [i for i in items if "node_modules" in str(i.path)]
        assert len(nm_items) > 0
    
    def test_find_items_dist(self, node_project: Path) -> None:
        """Test finding dist directory."""
        items = self.cleaner.find_items(node_project)
        dist_items = [i for i in items if "dist" in str(i.path)]
        assert len(dist_items) > 0
    
    def test_find_items_cache(self, node_project: Path) -> None:
        """Test finding .cache directory."""
        items = self.cleaner.find_items(node_project)
        cache_items = [i for i in items if ".cache" in str(i.path)]
        assert len(cache_items) > 0
    
    def test_clean_dry_run(self, node_project: Path) -> None:
        """Test dry run cleaning."""
        items_before = self.cleaner.find_items(node_project)
        assert len(items_before) > 0
        
        result = self.cleaner.clean(node_project, dry_run=True)
        
        assert result.dry_run is True
        assert len(result.items_cleaned) > 0
        
        # Nothing deleted
        items_after = self.cleaner.find_items(node_project)
        assert len(items_after) == len(items_before)
    
    def test_clean_actual(self, node_project: Path) -> None:
        """Test actual cleaning."""
        # Exclude node_modules to avoid size issues
        items_before = self.cleaner.find_items(
            node_project,
            exclude_patterns=["**/node_modules", "**/node_modules/**"]
        )
        
        result = self.cleaner.clean(
            node_project,
            dry_run=False,
            exclude_patterns=["**/node_modules", "**/node_modules/**"]
        )
        
        assert result.dry_run is False
        
        # Verify items were deleted
        items_after = self.cleaner.find_items(
            node_project,
            exclude_patterns=["**/node_modules", "**/node_modules/**"]
        )
        assert len(items_after) < len(items_before)

