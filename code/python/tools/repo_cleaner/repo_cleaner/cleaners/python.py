"""Python project cleaner."""

from typing import List

from repo_cleaner.cleaners.base import BaseCleaner, Pattern, PatternType


class PythonCleaner(BaseCleaner):
    """Cleaner for Python project artifacts.
    
    Cleans:
    - __pycache__ directories
    - *.pyc, *.pyo, *.pyd files
    - .pytest_cache, .mypy_cache, .ruff_cache
    - *.egg-info directories
    - dist/, build/ directories
    - Virtual environments (with confirmation)
    - Coverage data
    """
    
    @property
    def name(self) -> str:
        """Return cleaner name."""
        return "python"
    
    @property
    def display_name(self) -> str:
        """Return display name."""
        return "Python"
    
    def get_patterns(self) -> List[Pattern]:
        """Return list of patterns to clean."""
        return [
            Pattern(
                name="Python Cache",
                patterns=["**/__pycache__"],
                type=PatternType.DIRECTORY,
                description="Python bytecode cache directories",
                safe=True,
            ),
            Pattern(
                name="Compiled Python Files",
                patterns=["**/*.pyc", "**/*.pyo", "**/*.pyd"],
                type=PatternType.FILE,
                description="Compiled Python files",
                safe=True,
            ),
            Pattern(
                name="Pytest Cache",
                patterns=["**/.pytest_cache"],
                type=PatternType.DIRECTORY,
                description="Pytest cache directories",
                safe=True,
            ),
            Pattern(
                name="MyPy Cache",
                patterns=["**/.mypy_cache"],
                type=PatternType.DIRECTORY,
                description="MyPy type checking cache",
                safe=True,
            ),
            Pattern(
                name="Ruff Cache",
                patterns=["**/.ruff_cache"],
                type=PatternType.DIRECTORY,
                description="Ruff linter cache",
                safe=True,
            ),
            Pattern(
                name="Egg Info",
                patterns=["**/*.egg-info"],
                type=PatternType.DIRECTORY,
                description="Python egg metadata",
                safe=True,
            ),
            Pattern(
                name="Distribution Directory",
                patterns=["dist"],
                type=PatternType.DIRECTORY,
                description="Python distribution directory",
                safe=True,
            ),
            Pattern(
                name="Build Directory",
                patterns=["build"],
                type=PatternType.DIRECTORY,
                description="Python build directory",
                safe=True,
            ),
            Pattern(
                name="Egg Files",
                patterns=["**/*.egg"],
                type=PatternType.FILE,
                description="Python egg packages",
                safe=True,
            ),
            Pattern(
                name="Tox Environments",
                patterns=[".tox"],
                type=PatternType.DIRECTORY,
                description="Tox testing environments",
                safe=True,
            ),
            Pattern(
                name="Coverage Data",
                patterns=[".coverage", "coverage.xml"],
                type=PatternType.FILE,
                description="Code coverage data files",
                safe=True,
            ),
            Pattern(
                name="Coverage HTML Report",
                patterns=["htmlcov"],
                type=PatternType.DIRECTORY,
                description="HTML coverage report",
                safe=True,
            ),
            Pattern(
                name="Nox Environments",
                patterns=[".nox"],
                type=PatternType.DIRECTORY,
                description="Nox testing environments",
                safe=True,
            ),
            Pattern(
                name="Hypothesis Cache",
                patterns=[".hypothesis"],
                type=PatternType.DIRECTORY,
                description="Hypothesis testing cache",
                safe=True,
            ),
            Pattern(
                name="Virtual Environments",
                patterns=["venv", "env", ".venv", ".env"],
                type=PatternType.DIRECTORY,
                description="Python virtual environments",
                safe=False,
                requires_confirmation=True,
            ),
        ]

