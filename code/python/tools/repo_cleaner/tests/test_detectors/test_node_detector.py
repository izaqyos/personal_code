"""Tests for Node.js project detector."""

import json
from pathlib import Path

import pytest

from repo_cleaner.detectors.node import NodeDetector


class TestNodeDetector:
    """Tests for NodeDetector."""
    
    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.detector = NodeDetector()
    
    def test_name(self) -> None:
        """Test detector name."""
        assert self.detector.name == "node"
        assert self.detector.display_name == "Node.js"
    
    def test_detect_package_json(self, temp_dir: Path) -> None:
        """Test detection with package.json."""
        (temp_dir / "package.json").write_text('{"name": "test"}')
        assert self.detector.detect(temp_dir) is True
    
    def test_detect_package_lock(self, temp_dir: Path) -> None:
        """Test detection with package-lock.json."""
        (temp_dir / "package-lock.json").write_text('{"lockfileVersion": 2}')
        assert self.detector.detect(temp_dir) is True
    
    def test_detect_yarn_lock(self, temp_dir: Path) -> None:
        """Test detection with yarn.lock."""
        (temp_dir / "yarn.lock").write_text("# yarn lockfile")
        assert self.detector.detect(temp_dir) is True
    
    def test_detect_node_modules(self, temp_dir: Path) -> None:
        """Test detection with node_modules directory."""
        (temp_dir / "node_modules").mkdir()
        assert self.detector.detect(temp_dir) is True
    
    def test_no_detect_empty(self, temp_dir: Path) -> None:
        """Test no detection in empty directory."""
        assert self.detector.detect(temp_dir) is False
    
    def test_confidence_package_json(self, temp_dir: Path) -> None:
        """Test confidence with package.json."""
        (temp_dir / "package.json").write_text('{"name": "test"}')
        confidence = self.detector.get_confidence(temp_dir)
        assert confidence >= 0.9
    
    def test_confidence_with_dependencies(self, temp_dir: Path) -> None:
        """Test confidence with dependencies."""
        (temp_dir / "package.json").write_text(json.dumps({
            "name": "test",
            "dependencies": {"express": "^4.0.0"},
            "scripts": {"start": "node index.js"}
        }))
        confidence = self.detector.get_confidence(temp_dir)
        assert confidence >= 0.95
    
    def test_package_manager_detection(self, temp_dir: Path) -> None:
        """Test package manager detection."""
        (temp_dir / "package.json").write_text('{"name": "test"}')
        
        # No lock file - unknown
        assert self.detector.get_package_manager(temp_dir) == "unknown"
        
        # NPM
        (temp_dir / "package-lock.json").write_text("{}")
        assert self.detector.get_package_manager(temp_dir) == "npm"
        
        # Yarn takes precedence
        (temp_dir / "yarn.lock").write_text("")
        assert self.detector.get_package_manager(temp_dir) == "yarn"
        
        # pnpm takes precedence
        (temp_dir / "pnpm-lock.yaml").write_text("")
        assert self.detector.get_package_manager(temp_dir) == "pnpm"
    
    def test_indicators(self, node_project: Path) -> None:
        """Test indicator detection."""
        indicators = self.detector.get_indicators(node_project)
        assert len(indicators) > 0
        assert any("package.json" in i for i in indicators)
    
    def test_full_detect(self, node_project: Path) -> None:
        """Test full detection result."""
        result = self.detector.full_detect(node_project)
        assert result.detected is True
        assert result.confidence >= 0.9
        assert result.detector_name == "node"

