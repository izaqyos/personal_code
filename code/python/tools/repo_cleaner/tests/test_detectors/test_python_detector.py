"""Tests for Python project detector."""

from pathlib import Path

import pytest

from repo_cleaner.detectors.python import PythonDetector


class TestPythonDetector:
    """Tests for PythonDetector."""
    
    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.detector = PythonDetector()
    
    def test_name(self) -> None:
        """Test detector name."""
        assert self.detector.name == "python"
        assert self.detector.display_name == "Python"
    
    def test_detect_pyproject_toml(self, temp_dir: Path) -> None:
        """Test detection with pyproject.toml."""
        (temp_dir / "pyproject.toml").write_text("[project]\nname = 'test'")
        assert self.detector.detect(temp_dir) is True
    
    def test_detect_setup_py(self, temp_dir: Path) -> None:
        """Test detection with setup.py."""
        (temp_dir / "setup.py").write_text("from setuptools import setup\nsetup()")
        assert self.detector.detect(temp_dir) is True
    
    def test_detect_requirements_txt(self, temp_dir: Path) -> None:
        """Test detection with requirements.txt."""
        (temp_dir / "requirements.txt").write_text("requests>=2.0")
        assert self.detector.detect(temp_dir) is True
    
    def test_detect_pipfile(self, temp_dir: Path) -> None:
        """Test detection with Pipfile."""
        (temp_dir / "Pipfile").write_text("[packages]\nrequests = '*'")
        assert self.detector.detect(temp_dir) is True
    
    def test_detect_python_files(self, temp_dir: Path) -> None:
        """Test detection with .py files."""
        (temp_dir / "main.py").write_text("print('hello')")
        assert self.detector.detect(temp_dir) is True
    
    def test_detect_pycache(self, temp_dir: Path) -> None:
        """Test detection with __pycache__ directory."""
        (temp_dir / "__pycache__").mkdir()
        assert self.detector.detect(temp_dir) is True
    
    def test_detect_venv(self, temp_dir: Path) -> None:
        """Test detection with virtual environment."""
        venv = temp_dir / "venv"
        venv.mkdir()
        (venv / "pyvenv.cfg").write_text("home = /usr/bin")
        assert self.detector.detect(temp_dir) is True
    
    def test_no_detect_empty(self, temp_dir: Path) -> None:
        """Test no detection in empty directory."""
        assert self.detector.detect(temp_dir) is False
    
    def test_no_detect_other_project(self, temp_dir: Path) -> None:
        """Test no detection in non-Python project."""
        (temp_dir / "package.json").write_text('{"name": "test"}')
        (temp_dir / "index.js").write_text("console.log('hello');")
        assert self.detector.detect(temp_dir) is False
    
    def test_confidence_pyproject(self, temp_dir: Path) -> None:
        """Test confidence with pyproject.toml."""
        (temp_dir / "pyproject.toml").write_text("[project]\nname = 'test'")
        confidence = self.detector.get_confidence(temp_dir)
        assert confidence >= 0.9
    
    def test_confidence_multiple_indicators(self, temp_dir: Path) -> None:
        """Test confidence with multiple indicators."""
        (temp_dir / "pyproject.toml").write_text("[project]")
        (temp_dir / "requirements.txt").write_text("requests")
        (temp_dir / "setup.py").write_text("from setuptools import setup")
        confidence = self.detector.get_confidence(temp_dir)
        # Should boost confidence with multiple indicators
        assert confidence >= 0.9
    
    def test_confidence_only_py_files(self, temp_dir: Path) -> None:
        """Test confidence with only Python files."""
        for i in range(15):
            (temp_dir / f"module_{i}.py").write_text(f"# Module {i}")
        confidence = self.detector.get_confidence(temp_dir)
        # Many Python files should give decent confidence
        assert confidence >= 0.7
    
    def test_indicators(self, python_project: Path) -> None:
        """Test indicator detection."""
        indicators = self.detector.get_indicators(python_project)
        assert len(indicators) > 0
        # Should find pyproject.toml and requirements.txt
        assert any("pyproject.toml" in i for i in indicators)
        assert any("requirements.txt" in i for i in indicators)
    
    def test_full_detect(self, python_project: Path) -> None:
        """Test full detection result."""
        result = self.detector.full_detect(python_project)
        assert result.detected is True
        assert result.confidence >= 0.8
        assert result.detector_name == "python"
        assert len(result.indicators) > 0

