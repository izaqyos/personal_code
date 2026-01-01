"""Base cleaner interface for removing build artifacts."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional, Set
import fnmatch


class PatternType(Enum):
    """Type of pattern to match."""
    
    FILE = "file"
    DIRECTORY = "directory"
    BOTH = "both"


@dataclass
class Pattern:
    """Definition of a pattern to clean.
    
    Attributes:
        name: Human-readable name for this pattern
        patterns: List of glob patterns to match
        type: Type of items to match (FILE, DIRECTORY, or BOTH)
        description: Description of what this pattern matches
        safe: Whether this pattern is safe to delete without confirmation
        requires_confirmation: Whether to always ask for confirmation
    """
    
    name: str
    patterns: List[str]
    type: PatternType
    description: str
    safe: bool = True
    requires_confirmation: bool = False


@dataclass
class CleanItem:
    """An item (file or directory) to be cleaned.
    
    Attributes:
        path: Path to the item
        size: Size in bytes
        is_directory: Whether this is a directory
        pattern_name: Name of the pattern that matched
    """
    
    path: Path
    size: int
    is_directory: bool
    pattern_name: str


@dataclass
class CleanResult:
    """Result of a cleaning operation.
    
    Attributes:
        cleaner_name: Name of the cleaner that produced this result
        items_found: List of items found for cleaning
        items_cleaned: List of items that were cleaned
        items_skipped: List of items that were skipped
        items_failed: List of items that failed to clean
        total_size_found: Total size of items found
        total_size_cleaned: Total size of items cleaned
        dry_run: Whether this was a dry run
        errors: List of error messages
    """
    
    cleaner_name: str
    items_found: List[CleanItem] = field(default_factory=list)
    items_cleaned: List[CleanItem] = field(default_factory=list)
    items_skipped: List[CleanItem] = field(default_factory=list)
    items_failed: List[CleanItem] = field(default_factory=list)
    total_size_found: int = 0
    total_size_cleaned: int = 0
    dry_run: bool = False
    errors: List[str] = field(default_factory=list)
    
    @property
    def success(self) -> bool:
        """Return True if no errors occurred."""
        return len(self.errors) == 0 and len(self.items_failed) == 0
    
    @property
    def items_count(self) -> int:
        """Return total number of items found."""
        return len(self.items_found)
    
    @property
    def cleaned_count(self) -> int:
        """Return number of items cleaned."""
        return len(self.items_cleaned)


class BaseCleaner(ABC):
    """Abstract base class for language-specific cleaners.
    
    Each cleaner is responsible for finding and removing build artifacts
    for a specific project type.
    
    Subclasses must implement:
        - name: Property returning the cleaner name
        - get_patterns(): Method returning list of patterns to clean
        - clean(): Method to execute the cleaning operation
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the cleaner name (e.g., 'python', 'node').
        
        This should match the corresponding detector name.
        """
        pass
    
    @property
    def display_name(self) -> str:
        """Return a human-readable display name."""
        return self.name.replace("_", " ").title()
    
    @abstractmethod
    def get_patterns(self) -> List[Pattern]:
        """Return list of patterns to clean.
        
        Returns:
            List of Pattern objects defining what to clean
        """
        pass
    
    def find_items(
        self,
        path: Path,
        exclude_patterns: Optional[List[str]] = None,
    ) -> List[CleanItem]:
        """Find all items matching the cleaner patterns.
        
        Args:
            path: Root path to search
            exclude_patterns: Optional list of patterns to exclude
            
        Returns:
            List of CleanItem objects to be cleaned
        """
        items: List[CleanItem] = []
        seen_paths: Set[Path] = set()
        exclude_patterns = exclude_patterns or []
        
        for pattern in self.get_patterns():
            for glob_pattern in pattern.patterns:
                found = self._find_matching_items(
                    path, glob_pattern, pattern, exclude_patterns, seen_paths
                )
                items.extend(found)
        
        return items
    
    def _find_matching_items(
        self,
        root: Path,
        glob_pattern: str,
        pattern: Pattern,
        exclude_patterns: List[str],
        seen_paths: Set[Path],
    ) -> List[CleanItem]:
        """Find items matching a single glob pattern.
        
        Args:
            root: Root path to search
            glob_pattern: Glob pattern to match
            pattern: Pattern definition
            exclude_patterns: Patterns to exclude
            seen_paths: Set of already seen paths (to avoid duplicates)
            
        Returns:
            List of matching CleanItem objects
        """
        items: List[CleanItem] = []
        
        try:
            for item_path in root.glob(glob_pattern):
                # Skip if already seen
                if item_path in seen_paths:
                    continue
                
                # Check type match
                if pattern.type == PatternType.FILE and item_path.is_dir():
                    continue
                if pattern.type == PatternType.DIRECTORY and item_path.is_file():
                    continue
                
                # Check exclusions
                if self._is_excluded(item_path, root, exclude_patterns):
                    continue
                
                seen_paths.add(item_path)
                
                # Calculate size
                size = self._get_item_size(item_path)
                
                items.append(CleanItem(
                    path=item_path,
                    size=size,
                    is_directory=item_path.is_dir(),
                    pattern_name=pattern.name,
                ))
        except (OSError, PermissionError):
            pass  # Skip inaccessible paths
        
        return items
    
    def _is_excluded(
        self,
        item_path: Path,
        root: Path,
        exclude_patterns: List[str],
    ) -> bool:
        """Check if a path should be excluded.
        
        Args:
            item_path: Path to check
            root: Root path for relative matching
            exclude_patterns: List of exclusion patterns
            
        Returns:
            True if the path should be excluded
        """
        try:
            relative_path = item_path.relative_to(root)
        except ValueError:
            relative_path = item_path
        
        relative_str = str(relative_path)
        
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(relative_str, pattern):
                return True
            if fnmatch.fnmatch(str(item_path), pattern):
                return True
        
        return False
    
    def _get_item_size(self, path: Path) -> int:
        """Get the size of a file or directory.
        
        Args:
            path: Path to file or directory
            
        Returns:
            Size in bytes
        """
        try:
            if path.is_file():
                return path.stat().st_size
            elif path.is_dir():
                return sum(
                    f.stat().st_size
                    for f in path.glob("**/*")
                    if f.is_file()
                )
        except (OSError, PermissionError):
            pass
        return 0
    
    def clean(
        self,
        path: Path,
        dry_run: bool = False,
        exclude_patterns: Optional[List[str]] = None,
    ) -> CleanResult:
        """Execute the cleaning operation.
        
        Args:
            path: Root path to clean
            dry_run: If True, only report what would be cleaned
            exclude_patterns: Optional list of patterns to exclude
            
        Returns:
            CleanResult with details of the operation
        """
        from repo_cleaner.utils.filesystem import safe_delete
        
        result = CleanResult(
            cleaner_name=self.name,
            dry_run=dry_run,
        )
        
        # Find all items
        items = self.find_items(path, exclude_patterns)
        result.items_found = items
        result.total_size_found = sum(item.size for item in items)
        
        if dry_run:
            # In dry-run mode, all items are "cleaned" (for reporting)
            result.items_cleaned = items
            result.total_size_cleaned = result.total_size_found
            return result
        
        # Actually delete items
        for item in items:
            try:
                success = safe_delete(item.path)
                if success:
                    result.items_cleaned.append(item)
                    result.total_size_cleaned += item.size
                else:
                    result.items_failed.append(item)
                    result.errors.append(f"Failed to delete: {item.path}")
            except Exception as e:
                result.items_failed.append(item)
                result.errors.append(f"Error deleting {item.path}: {e}")
        
        return result

