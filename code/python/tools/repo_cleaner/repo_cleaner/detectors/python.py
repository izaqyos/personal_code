"""Python project detector."""

from pathlib import Path
from typing import List

from repo_cleaner.detectors.base import BaseDetector


class PythonDetector(BaseDetector):
    """Detector for Python projects.
    
    Identifies Python projects by looking for:
    - pyproject.toml
    - setup.py
    - setup.cfg
    - requirements.txt
    - Pipfile
    - *.py files
    - __init__.py files
    """
    
    # Indicator files and their confidence weights
    INDICATORS = {
        "pyproject.toml": 0.9,
        "setup.py": 0.9,
        "setup.cfg": 0.8,
        "requirements.txt": 0.7,
        "Pipfile": 0.7,
        "Pipfile.lock": 0.6,
        "poetry.lock": 0.7,
        "tox.ini": 0.6,
        "pytest.ini": 0.5,
        ".python-version": 0.5,
    }
    
    @property
    def name(self) -> str:
        """Return detector name."""
        return "python"
    
    @property
    def display_name(self) -> str:
        """Return display name."""
        return "Python"
    
    def detect(self, path: Path) -> bool:
        """Check if this is a Python project.
        
        Args:
            path: Path to check
            
        Returns:
            True if Python project detected
        """
        path = Path(path)
        
        # Check for indicator files
        for indicator in self.INDICATORS.keys():
            if self._has_file(path, indicator):
                return True
        
        # Check for Python files
        if self._has_files_with_extension(path, ".py", recursive=False):
            return True
        
        # Check for __pycache__ directories
        if self._has_directory(path, "__pycache__"):
            return True
        
        # Check for venv/env directories with pyvenv.cfg
        for venv_dir in ["venv", "env", ".venv", ".env"]:
            if (path / venv_dir / "pyvenv.cfg").is_file():
                return True
        
        return False
    
    def get_confidence(self, path: Path) -> float:
        """Calculate confidence score.
        
        Args:
            path: Path to project
            
        Returns:
            Confidence score 0.0 to 1.0
        """
        path = Path(path)
        max_confidence = 0.0
        
        # Check indicator files
        for indicator, weight in self.INDICATORS.items():
            if self._has_file(path, indicator):
                max_confidence = max(max_confidence, weight)
        
        # Boost confidence if multiple indicators found
        indicator_count = sum(
            1 for indicator in self.INDICATORS.keys()
            if self._has_file(path, indicator)
        )
        
        if indicator_count >= 3:
            max_confidence = min(1.0, max_confidence + 0.1)
        
        # Check for Python files
        py_count = self._count_files_with_extension(path, ".py", recursive=True)
        if py_count > 10:
            max_confidence = max(max_confidence, 0.8)
        elif py_count > 0:
            max_confidence = max(max_confidence, 0.5)
        
        return max_confidence
    
    def get_indicators(self, path: Path) -> List[str]:
        """Get list of detected indicators.
        
        Args:
            path: Path to project
            
        Returns:
            List of indicator descriptions
        """
        path = Path(path)
        indicators = []
        
        for indicator in self.INDICATORS.keys():
            if self._has_file(path, indicator):
                indicators.append(f"Found {indicator}")
        
        py_count = self._count_files_with_extension(path, ".py", recursive=True)
        if py_count > 0:
            indicators.append(f"Found {py_count} Python files")
        
        # Check for virtual environments
        for venv_dir in ["venv", "env", ".venv", ".env"]:
            if (path / venv_dir / "pyvenv.cfg").is_file():
                indicators.append(f"Found virtual environment: {venv_dir}")
        
        # Check for __pycache__
        if self._has_directory(path, "__pycache__"):
            indicators.append("Found __pycache__ directory")
        
        return indicators

