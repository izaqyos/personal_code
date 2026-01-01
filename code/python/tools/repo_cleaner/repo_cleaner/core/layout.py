"""Layout manager for caching scan results."""

import hashlib
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from repo_cleaner.core.scanner import ScanLayout
from repo_cleaner.core.logger import get_logger

logger = get_logger()


# Default config directory
DEFAULT_CONFIG_DIR = Path.home() / ".config" / "repo_cleaner"
LAYOUTS_DIR = DEFAULT_CONFIG_DIR / "layouts"

# Cache expiry time in hours
CACHE_EXPIRY_HOURS = 24


def get_config_dir() -> Path:
    """Get or create the config directory.
    
    Returns:
        Path to config directory
    """
    config_dir = DEFAULT_CONFIG_DIR
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_layouts_dir() -> Path:
    """Get or create the layouts directory.
    
    Returns:
        Path to layouts directory
    """
    layouts_dir = LAYOUTS_DIR
    layouts_dir.mkdir(parents=True, exist_ok=True)
    return layouts_dir


def get_layout_hash(path: Path) -> str:
    """Generate a hash for a path to use as layout filename.
    
    Args:
        path: Path to hash
        
    Returns:
        SHA256 hash of the path (first 16 chars)
    """
    path_str = str(Path(path).resolve())
    return hashlib.sha256(path_str.encode()).hexdigest()[:16]


def get_layout_path(root_path: Path) -> Path:
    """Get the path where a layout would be stored.
    
    Args:
        root_path: Root path of the scan
        
    Returns:
        Path to the layout JSON file
    """
    layout_hash = get_layout_hash(root_path)
    return get_layouts_dir() / f"{layout_hash}.json"


class LayoutManager:
    """Manages saving and loading of scan layouts.
    
    Layouts are cached in ~/.config/repo_cleaner/layouts/ with
    a 24-hour expiry time.
    """
    
    def __init__(self, cache_expiry_hours: int = CACHE_EXPIRY_HOURS) -> None:
        """Initialize the layout manager.
        
        Args:
            cache_expiry_hours: Hours before cache expires
        """
        self.cache_expiry_hours = cache_expiry_hours
        self.layouts_dir = get_layouts_dir()
    
    def save_layout(self, layout: ScanLayout) -> Path:
        """Save a scan layout to cache.
        
        Args:
            layout: Layout to save
            
        Returns:
            Path where layout was saved
        """
        layout_path = get_layout_path(Path(layout.root_path))
        
        try:
            with open(layout_path, "w", encoding="utf-8") as f:
                json.dump(layout.to_dict(), f, indent=2)
            
            logger.debug(f"Saved layout to {layout_path}")
            return layout_path
        except OSError as e:
            logger.warning(f"Failed to save layout: {e}")
            raise
    
    def load_layout(self, root_path: Path) -> Optional[ScanLayout]:
        """Load a cached layout if it exists and is not expired.
        
        Args:
            root_path: Root path of the scan
            
        Returns:
            ScanLayout if valid cache exists, None otherwise
        """
        layout_path = get_layout_path(root_path)
        
        if not layout_path.exists():
            logger.debug(f"No cached layout found at {layout_path}")
            return None
        
        # Check if expired
        if self._is_expired(layout_path):
            logger.debug(f"Layout cache expired: {layout_path}")
            return None
        
        try:
            with open(layout_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            layout = ScanLayout.from_dict(data)
            
            # Verify the root path matches
            if str(Path(layout.root_path).resolve()) != str(Path(root_path).resolve()):
                logger.warning("Layout root path mismatch, ignoring cache")
                return None
            
            logger.debug(f"Loaded layout from cache: {layout_path}")
            return layout
        except (json.JSONDecodeError, KeyError, OSError) as e:
            logger.warning(f"Failed to load cached layout: {e}")
            return None
    
    def _is_expired(self, layout_path: Path) -> bool:
        """Check if a cached layout is expired.
        
        Args:
            layout_path: Path to layout file
            
        Returns:
            True if expired
        """
        try:
            mtime = datetime.fromtimestamp(layout_path.stat().st_mtime)
            expiry = mtime + timedelta(hours=self.cache_expiry_hours)
            return datetime.now() > expiry
        except OSError:
            return True
    
    def get_cache_age(self, root_path: Path) -> Optional[timedelta]:
        """Get the age of a cached layout.
        
        Args:
            root_path: Root path of the scan
            
        Returns:
            Age as timedelta, or None if no cache
        """
        layout_path = get_layout_path(root_path)
        
        if not layout_path.exists():
            return None
        
        try:
            mtime = datetime.fromtimestamp(layout_path.stat().st_mtime)
            return datetime.now() - mtime
        except OSError:
            return None
    
    def delete_layout(self, root_path: Path) -> bool:
        """Delete a cached layout.
        
        Args:
            root_path: Root path of the scan
            
        Returns:
            True if deleted successfully
        """
        layout_path = get_layout_path(root_path)
        
        try:
            if layout_path.exists():
                layout_path.unlink()
                logger.debug(f"Deleted layout: {layout_path}")
                return True
            return False
        except OSError as e:
            logger.warning(f"Failed to delete layout: {e}")
            return False
    
    def clear_all_layouts(self) -> int:
        """Clear all cached layouts.
        
        Returns:
            Number of layouts deleted
        """
        count = 0
        try:
            for layout_file in self.layouts_dir.glob("*.json"):
                layout_file.unlink()
                count += 1
            logger.info(f"Cleared {count} cached layouts")
        except OSError as e:
            logger.warning(f"Error clearing layouts: {e}")
        return count
    
    def list_cached_layouts(self) -> list:
        """List all cached layouts with metadata.
        
        Returns:
            List of dicts with layout info
        """
        layouts = []
        
        try:
            for layout_file in self.layouts_dir.glob("*.json"):
                try:
                    with open(layout_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    mtime = datetime.fromtimestamp(layout_file.stat().st_mtime)
                    age = datetime.now() - mtime
                    expired = age > timedelta(hours=self.cache_expiry_hours)
                    
                    layouts.append({
                        "file": str(layout_file),
                        "root_path": data.get("root_path", "unknown"),
                        "scan_time": data.get("scan_time", "unknown"),
                        "total_projects": data.get("total_projects", 0),
                        "age_hours": age.total_seconds() / 3600,
                        "expired": expired,
                    })
                except (json.JSONDecodeError, OSError):
                    continue
        except OSError:
            pass
        
        return layouts

