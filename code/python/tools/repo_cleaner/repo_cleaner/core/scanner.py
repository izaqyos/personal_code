"""Recursive project scanner for monorepo support."""

import hashlib
import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

from repo_cleaner.detectors import ALL_DETECTORS
from repo_cleaner.detectors.base import DetectionResult
from repo_cleaner.core.logger import get_logger

logger = get_logger()


@dataclass
class DetectedProject:
    """Represents a detected project within a monorepo.
    
    Attributes:
        path: Absolute path to the project directory
        relative_path: Path relative to the scan root
        project_types: List of detected project types
        detections: Detection results per type
        depth: Directory depth from scan root
    """
    path: str
    relative_path: str
    project_types: List[str]
    confidence: Dict[str, float] = field(default_factory=dict)
    indicators: Dict[str, List[str]] = field(default_factory=dict)
    depth: int = 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "path": self.path,
            "relative_path": self.relative_path,
            "project_types": self.project_types,
            "confidence": self.confidence,
            "indicators": self.indicators,
            "depth": self.depth,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "DetectedProject":
        """Create from dictionary."""
        return cls(
            path=data["path"],
            relative_path=data["relative_path"],
            project_types=data["project_types"],
            confidence=data.get("confidence", {}),
            indicators=data.get("indicators", {}),
            depth=data.get("depth", 0),
        )


@dataclass
class ScanLayout:
    """Layout of all detected projects in a monorepo.
    
    Attributes:
        root_path: Absolute path to the scan root
        scan_time: When the scan was performed
        projects: List of detected projects
        total_projects: Number of projects found
        languages_found: Set of languages detected
        max_depth: Maximum directory depth scanned
    """
    root_path: str
    scan_time: str
    projects: List[DetectedProject] = field(default_factory=list)
    total_projects: int = 0
    languages_found: List[str] = field(default_factory=list)
    max_depth: int = 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "root_path": self.root_path,
            "scan_time": self.scan_time,
            "projects": [p.to_dict() for p in self.projects],
            "total_projects": self.total_projects,
            "languages_found": self.languages_found,
            "max_depth": self.max_depth,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ScanLayout":
        """Create from dictionary."""
        return cls(
            root_path=data["root_path"],
            scan_time=data["scan_time"],
            projects=[DetectedProject.from_dict(p) for p in data.get("projects", [])],
            total_projects=data.get("total_projects", 0),
            languages_found=data.get("languages_found", []),
            max_depth=data.get("max_depth", 0),
        )
    
    def get_projects_by_language(self, language: str) -> List[DetectedProject]:
        """Get all projects of a specific language."""
        return [p for p in self.projects if language in p.project_types]
    
    def get_summary(self) -> Dict[str, int]:
        """Get summary of projects by language."""
        summary: Dict[str, int] = {}
        for project in self.projects:
            for lang in project.project_types:
                summary[lang] = summary.get(lang, 0) + 1
        return summary


# Directories to skip during scanning
SKIP_DIRECTORIES = {
    ".git",
    ".svn",
    ".hg",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    ".nox",
    "venv",
    ".venv",
    "env",
    ".env",
    "dist",
    "build",
    "target",
    ".next",
    ".nuxt",
    ".angular",
    "vendor",
    ".gradle",
    ".idea",
    ".vscode",
}


class MonorepoScanner:
    """Recursive scanner for detecting projects in a monorepo.
    
    Scans directories recursively to find all projects, building
    a layout of the repository structure.
    """
    
    def __init__(
        self,
        max_depth: int = 10,
        skip_dirs: Optional[Set[str]] = None,
        enabled_languages: Optional[List[str]] = None,
    ) -> None:
        """Initialize the scanner.
        
        Args:
            max_depth: Maximum directory depth to scan
            skip_dirs: Additional directories to skip
            enabled_languages: Only detect these languages (None = all)
        """
        self.max_depth = max_depth
        self.skip_dirs = SKIP_DIRECTORIES.copy()
        if skip_dirs:
            self.skip_dirs.update(skip_dirs)
        self.enabled_languages = enabled_languages
        
        # Filter detectors if languages specified
        if enabled_languages:
            self.detectors = [
                d for d in ALL_DETECTORS
                if d.name in enabled_languages
            ]
        else:
            self.detectors = ALL_DETECTORS
    
    def scan(self, root_path: Path) -> ScanLayout:
        """Scan a directory recursively for projects.
        
        Args:
            root_path: Root directory to scan
            
        Returns:
            ScanLayout with all detected projects
        """
        root_path = Path(root_path).resolve()
        
        layout = ScanLayout(
            root_path=str(root_path),
            scan_time=datetime.now().isoformat(),
        )
        
        # Track which paths we've already detected projects in
        detected_paths: Set[Path] = set()
        all_languages: Set[str] = set()
        
        # Scan recursively
        self._scan_directory(
            root_path,
            root_path,
            0,
            layout.projects,
            detected_paths,
            all_languages,
        )
        
        # Update layout metadata
        layout.total_projects = len(layout.projects)
        layout.languages_found = sorted(all_languages)
        layout.max_depth = max((p.depth for p in layout.projects), default=0)
        
        return layout
    
    def _scan_directory(
        self,
        current_path: Path,
        root_path: Path,
        depth: int,
        projects: List[DetectedProject],
        detected_paths: Set[Path],
        all_languages: Set[str],
    ) -> None:
        """Recursively scan a directory.
        
        Args:
            current_path: Current directory being scanned
            root_path: Root directory of the scan
            depth: Current depth from root
            projects: List to append detected projects to
            detected_paths: Set of paths already detected
            all_languages: Set of all languages found
        """
        if depth > self.max_depth:
            return
        
        # Skip if already detected a project here
        if current_path in detected_paths:
            return
        
        # Detect project types at this location
        detected_types: List[str] = []
        confidence: Dict[str, float] = {}
        indicators: Dict[str, List[str]] = {}
        
        for detector in self.detectors:
            try:
                result = detector.full_detect(current_path)
                if result.detected and result.confidence >= 0.5:
                    detected_types.append(detector.name)
                    confidence[detector.name] = result.confidence
                    indicators[detector.name] = result.indicators
                    all_languages.add(detector.name)
            except Exception as e:
                logger.debug(f"Detector {detector.name} failed at {current_path}: {e}")
        
        # If we found projects here, add them
        if detected_types:
            try:
                relative_path = current_path.relative_to(root_path)
            except ValueError:
                relative_path = current_path
            
            project = DetectedProject(
                path=str(current_path),
                relative_path=str(relative_path) if str(relative_path) != "." else ".",
                project_types=detected_types,
                confidence=confidence,
                indicators=indicators,
                depth=depth,
            )
            projects.append(project)
            detected_paths.add(current_path)
        
        # Continue scanning subdirectories
        try:
            for entry in current_path.iterdir():
                if not entry.is_dir():
                    continue
                
                # Skip certain directories
                if entry.name in self.skip_dirs:
                    continue
                
                # Skip hidden directories (except .git which we already skip)
                if entry.name.startswith(".") and entry.name not in {".github", ".gitlab"}:
                    continue
                
                # Recurse
                self._scan_directory(
                    entry,
                    root_path,
                    depth + 1,
                    projects,
                    detected_paths,
                    all_languages,
                )
        except PermissionError:
            logger.debug(f"Permission denied: {current_path}")
        except OSError as e:
            logger.debug(f"Error scanning {current_path}: {e}")
    
    def print_layout(self, layout: ScanLayout) -> None:
        """Print a human-readable layout summary.
        
        Args:
            layout: Layout to print
        """
        from repo_cleaner.utils.prompts import print_info, print_success
        
        print()
        print("=" * 60)
        print(f"  Monorepo Scan Results")
        print(f"  Root: {layout.root_path}")
        print(f"  Scanned: {layout.scan_time[:19]}")
        print("=" * 60)
        print()
        
        if not layout.projects:
            print_info("No projects detected.")
            return
        
        # Summary by language
        summary = layout.get_summary()
        print_info(f"Found {layout.total_projects} projects in {len(summary)} languages:")
        for lang, count in sorted(summary.items()):
            print(f"  - {lang}: {count} project(s)")
        print()
        
        # Project list
        print("Projects:")
        print("-" * 60)
        for project in sorted(layout.projects, key=lambda p: p.relative_path):
            path_display = project.relative_path if project.relative_path != "." else "(root)"
            types_display = ", ".join(project.project_types)
            print(f"  {path_display}")
            print(f"    Types: {types_display}")
        print("-" * 60)
        print()

