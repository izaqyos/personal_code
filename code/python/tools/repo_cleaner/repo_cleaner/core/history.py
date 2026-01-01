"""History manager for tracking cleanup operations."""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from repo_cleaner.core.layout import get_config_dir
from repo_cleaner.core.logger import get_logger

logger = get_logger()


# History file location
HISTORY_FILE = get_config_dir() / "history.json"

# Maximum number of history entries
MAX_HISTORY_ENTRIES = 1000


@dataclass
class CleanedItem:
    """Record of a single cleaned item.
    
    Attributes:
        path: Path that was cleaned
        size: Size in bytes
        is_directory: Whether it was a directory
        pattern_name: Name of the pattern that matched
    """
    path: str
    size: int
    is_directory: bool
    pattern_name: str
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "CleanedItem":
        return cls(**data)


@dataclass
class ProjectCleanReport:
    """Report for a single project cleanup.
    
    Attributes:
        path: Project path
        relative_path: Path relative to scan root
        project_types: Types detected
        items_cleaned: Number of items cleaned
        size_cleaned: Total size cleaned in bytes
        items: Detailed list of items (if detailed report)
        errors: Any errors encountered
    """
    path: str
    relative_path: str
    project_types: List[str]
    items_cleaned: int = 0
    size_cleaned: int = 0
    items: List[CleanedItem] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self, include_items: bool = False) -> dict:
        data = {
            "path": self.path,
            "relative_path": self.relative_path,
            "project_types": self.project_types,
            "items_cleaned": self.items_cleaned,
            "size_cleaned": self.size_cleaned,
            "errors": self.errors,
        }
        if include_items:
            data["items"] = [i.to_dict() for i in self.items]
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProjectCleanReport":
        items = [CleanedItem.from_dict(i) for i in data.get("items", [])]
        return cls(
            path=data["path"],
            relative_path=data["relative_path"],
            project_types=data["project_types"],
            items_cleaned=data.get("items_cleaned", 0),
            size_cleaned=data.get("size_cleaned", 0),
            items=items,
            errors=data.get("errors", []),
        )


@dataclass
class CleanupReport:
    """Complete report for a cleanup operation.
    
    Attributes:
        id: Unique report ID
        timestamp: When the cleanup occurred
        root_path: Root path that was cleaned
        total_projects: Number of projects cleaned
        total_items: Total items cleaned
        total_size: Total size cleaned in bytes
        project_reports: Per-project reports
        dry_run: Whether this was a dry run
        duration_seconds: How long the cleanup took
        errors: Global errors
    """
    id: str
    timestamp: str
    root_path: str
    total_projects: int = 0
    total_items: int = 0
    total_size: int = 0
    project_reports: List[ProjectCleanReport] = field(default_factory=list)
    dry_run: bool = False
    duration_seconds: float = 0.0
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self, include_items: bool = False) -> dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "root_path": self.root_path,
            "total_projects": self.total_projects,
            "total_items": self.total_items,
            "total_size": self.total_size,
            "project_reports": [p.to_dict(include_items) for p in self.project_reports],
            "dry_run": self.dry_run,
            "duration_seconds": self.duration_seconds,
            "errors": self.errors,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CleanupReport":
        project_reports = [
            ProjectCleanReport.from_dict(p)
            for p in data.get("project_reports", [])
        ]
        return cls(
            id=data["id"],
            timestamp=data["timestamp"],
            root_path=data["root_path"],
            total_projects=data.get("total_projects", 0),
            total_items=data.get("total_items", 0),
            total_size=data.get("total_size", 0),
            project_reports=project_reports,
            dry_run=data.get("dry_run", False),
            duration_seconds=data.get("duration_seconds", 0.0),
            errors=data.get("errors", []),
        )
    
    @property
    def success(self) -> bool:
        """Return True if no errors occurred."""
        return len(self.errors) == 0 and all(
            len(p.errors) == 0 for p in self.project_reports
        )
    
    def get_summary_by_language(self) -> Dict[str, Dict[str, int]]:
        """Get summary broken down by language.
        
        Returns:
            Dict mapping language to {items, size}
        """
        summary: Dict[str, Dict[str, int]] = {}
        
        for report in self.project_reports:
            for lang in report.project_types:
                if lang not in summary:
                    summary[lang] = {"items": 0, "size": 0, "projects": 0}
                summary[lang]["items"] += report.items_cleaned
                summary[lang]["size"] += report.size_cleaned
                summary[lang]["projects"] += 1
        
        return summary


def generate_report_id() -> str:
    """Generate a unique report ID.
    
    Returns:
        Report ID in format: YYYYMMDD_HHMMSS_XXXX
    """
    import random
    import string
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"{timestamp}_{suffix}"


class HistoryManager:
    """Manages cleanup history with JSON storage.
    
    Stores the last 1000 cleanup reports, automatically
    removing oldest entries when limit is exceeded.
    """
    
    def __init__(
        self,
        history_file: Optional[Path] = None,
        max_entries: int = MAX_HISTORY_ENTRIES,
    ) -> None:
        """Initialize the history manager.
        
        Args:
            history_file: Path to history file (default: ~/.config/repo_cleaner/history.json)
            max_entries: Maximum number of entries to keep
        """
        self.history_file = history_file or HISTORY_FILE
        self.max_entries = max_entries
        
        # Ensure parent directory exists
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_history(self) -> List[dict]:
        """Load history from file.
        
        Returns:
            List of history entry dicts
        """
        if not self.history_file.exists():
            return []
        
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Failed to load history: {e}")
            return []
    
    def _save_history(self, history: List[dict]) -> None:
        """Save history to file.
        
        Args:
            history: List of history entry dicts
        """
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except OSError as e:
            logger.warning(f"Failed to save history: {e}")
    
    def add_report(self, report: CleanupReport, detailed: bool = False) -> None:
        """Add a cleanup report to history.
        
        Args:
            report: Report to add
            detailed: Whether to include detailed item list
        """
        history = self._load_history()
        
        # Add new entry
        history.append(report.to_dict(include_items=detailed))
        
        # Trim to max entries (remove oldest)
        if len(history) > self.max_entries:
            history = history[-self.max_entries:]
        
        self._save_history(history)
        logger.debug(f"Added report {report.id} to history")
    
    def get_history(
        self,
        limit: Optional[int] = None,
        root_path: Optional[str] = None,
    ) -> List[CleanupReport]:
        """Get cleanup history.
        
        Args:
            limit: Maximum number of entries to return
            root_path: Filter by root path
            
        Returns:
            List of CleanupReport objects (newest first)
        """
        history = self._load_history()
        
        # Filter by root path if specified
        if root_path:
            root_path_resolved = str(Path(root_path).resolve())
            history = [
                h for h in history
                if str(Path(h.get("root_path", "")).resolve()) == root_path_resolved
            ]
        
        # Sort by timestamp (newest first)
        history.sort(key=lambda h: h.get("timestamp", ""), reverse=True)
        
        # Apply limit
        if limit:
            history = history[:limit]
        
        return [CleanupReport.from_dict(h) for h in history]
    
    def get_report(self, report_id: str) -> Optional[CleanupReport]:
        """Get a specific report by ID.
        
        Args:
            report_id: Report ID to find
            
        Returns:
            CleanupReport or None if not found
        """
        history = self._load_history()
        
        for entry in history:
            if entry.get("id") == report_id:
                return CleanupReport.from_dict(entry)
        
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get overall statistics from history.
        
        Returns:
            Dict with statistics
        """
        history = self._load_history()
        
        if not history:
            return {
                "total_cleanups": 0,
                "total_items_cleaned": 0,
                "total_size_cleaned": 0,
                "dry_runs": 0,
                "actual_cleanups": 0,
            }
        
        return {
            "total_cleanups": len(history),
            "total_items_cleaned": sum(h.get("total_items", 0) for h in history),
            "total_size_cleaned": sum(h.get("total_size", 0) for h in history),
            "dry_runs": sum(1 for h in history if h.get("dry_run", False)),
            "actual_cleanups": sum(1 for h in history if not h.get("dry_run", False)),
        }
    
    def clear_history(self) -> int:
        """Clear all history.
        
        Returns:
            Number of entries cleared
        """
        history = self._load_history()
        count = len(history)
        self._save_history([])
        logger.info(f"Cleared {count} history entries")
        return count
    
    def print_history(self, limit: int = 10) -> None:
        """Print recent history to console.
        
        Args:
            limit: Number of entries to show
        """
        from repo_cleaner.utils.filesystem import format_size
        from repo_cleaner.utils.prompts import print_info
        
        reports = self.get_history(limit=limit)
        
        if not reports:
            print_info("No cleanup history found.")
            return
        
        print()
        print("=" * 60)
        print(f"  Recent Cleanup History (last {len(reports)})")
        print("=" * 60)
        print()
        
        for report in reports:
            mode = "[DRY RUN]" if report.dry_run else "[CLEANED]"
            size = format_size(report.total_size)
            time = report.timestamp[:19]  # Trim microseconds
            
            print(f"{mode} {time}")
            print(f"  Path: {report.root_path}")
            print(f"  Projects: {report.total_projects}, Items: {report.total_items}, Size: {size}")
            print()

