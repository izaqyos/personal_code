"""Base detector interface for project type detection."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class DetectionResult:
    """Result of project type detection.
    
    Attributes:
        detected: Whether the project type was detected
        confidence: Confidence score from 0.0 to 1.0
        detector_name: Name of the detector that produced this result
        indicators: List of indicators that led to detection
        message: Optional message with additional details
    """
    
    detected: bool
    confidence: float
    detector_name: str
    indicators: List[str] = field(default_factory=list)
    message: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Validate confidence is in valid range."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")


class BaseDetector(ABC):
    """Abstract base class for project type detectors.
    
    Each detector is responsible for identifying if a directory contains
    a specific type of project (e.g., Python, Node.js, Java).
    
    Subclasses must implement:
        - name: Property returning the detector name
        - detect(): Method to check if project type matches
        - get_confidence(): Method to return confidence score
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the detector name (e.g., 'python', 'node', 'java').
        
        This name is used to identify the detector and match with cleaners.
        """
        pass
    
    @property
    def display_name(self) -> str:
        """Return a human-readable display name.
        
        Can be overridden by subclasses for prettier output.
        """
        return self.name.replace("_", " ").title()
    
    @abstractmethod
    def detect(self, path: Path) -> bool:
        """Check if the project type matches this detector.
        
        Args:
            path: Path to the project directory
            
        Returns:
            True if the project type is detected, False otherwise
        """
        pass
    
    @abstractmethod
    def get_confidence(self, path: Path) -> float:
        """Return a confidence score for the detection.
        
        The confidence score indicates how certain the detector is that
        the project matches this type. Used when multiple detectors match.
        
        Args:
            path: Path to the project directory
            
        Returns:
            Confidence score from 0.0 (no match) to 1.0 (certain match)
        """
        pass
    
    def get_indicators(self, path: Path) -> List[str]:
        """Return a list of indicators that led to detection.
        
        This is useful for debugging and informing users why a project
        type was detected.
        
        Args:
            path: Path to the project directory
            
        Returns:
            List of indicator descriptions (e.g., "Found package.json")
        """
        return []
    
    def full_detect(self, path: Path) -> DetectionResult:
        """Perform full detection and return detailed result.
        
        Args:
            path: Path to the project directory
            
        Returns:
            DetectionResult with all detection information
        """
        detected = self.detect(path)
        confidence = self.get_confidence(path) if detected else 0.0
        indicators = self.get_indicators(path) if detected else []
        
        return DetectionResult(
            detected=detected,
            confidence=confidence,
            detector_name=self.name,
            indicators=indicators,
        )
    
    def _has_file(self, path: Path, filename: str) -> bool:
        """Check if a file exists in the directory.
        
        Args:
            path: Directory path
            filename: Name of file to check
            
        Returns:
            True if file exists
        """
        return (path / filename).is_file()
    
    def _has_directory(self, path: Path, dirname: str) -> bool:
        """Check if a directory exists.
        
        Args:
            path: Parent directory path
            dirname: Name of directory to check
            
        Returns:
            True if directory exists
        """
        return (path / dirname).is_dir()
    
    def _has_files_with_extension(self, path: Path, extension: str, recursive: bool = False) -> bool:
        """Check if files with given extension exist.
        
        Args:
            path: Directory path
            extension: File extension (e.g., '.py', '.java')
            recursive: Whether to search recursively
            
        Returns:
            True if at least one matching file exists
        """
        if not extension.startswith("."):
            extension = f".{extension}"
        
        pattern = f"**/*{extension}" if recursive else f"*{extension}"
        
        try:
            return any(path.glob(pattern))
        except (OSError, PermissionError):
            return False
    
    def _count_files_with_extension(self, path: Path, extension: str, recursive: bool = True) -> int:
        """Count files with given extension.
        
        Args:
            path: Directory path
            extension: File extension (e.g., '.py', '.java')
            recursive: Whether to search recursively
            
        Returns:
            Number of matching files
        """
        if not extension.startswith("."):
            extension = f".{extension}"
        
        pattern = f"**/*{extension}" if recursive else f"*{extension}"
        
        try:
            return sum(1 for _ in path.glob(pattern))
        except (OSError, PermissionError):
            return 0

