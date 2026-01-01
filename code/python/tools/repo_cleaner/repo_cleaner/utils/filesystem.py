"""Filesystem utilities for safe file operations."""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Union
import fnmatch


def safe_delete(path: Path, follow_symlinks: bool = False) -> bool:
    """Safely delete a file or directory.
    
    Args:
        path: Path to file or directory to delete
        follow_symlinks: Whether to follow symlinks (default: False for safety)
        
    Returns:
        True if deletion was successful, False otherwise
    """
    try:
        path = Path(path)
        
        if not path.exists():
            return True  # Already gone
        
        # Handle symlinks
        if path.is_symlink():
            path.unlink()
            return True
        
        # Delete file
        if path.is_file():
            path.unlink()
            return True
        
        # Delete directory
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=False)
            return True
        
        return False
    except (OSError, PermissionError, shutil.Error):
        return False


def get_directory_size(path: Path, follow_symlinks: bool = False) -> int:
    """Calculate the total size of a directory.
    
    Args:
        path: Path to directory
        follow_symlinks: Whether to follow symlinks
        
    Returns:
        Total size in bytes
    """
    path = Path(path)
    
    if not path.is_dir():
        if path.is_file():
            try:
                return path.stat().st_size
            except OSError:
                return 0
        return 0
    
    total_size = 0
    try:
        for entry in path.glob("**/*"):
            if entry.is_symlink() and not follow_symlinks:
                continue
            if entry.is_file():
                try:
                    total_size += entry.stat().st_size
                except OSError:
                    pass  # Skip inaccessible files
    except (OSError, PermissionError):
        pass
    
    return total_size


def get_file_size(path: Path) -> int:
    """Get the size of a single file.
    
    Args:
        path: Path to file
        
    Returns:
        Size in bytes, or 0 if file doesn't exist or can't be accessed
    """
    try:
        return Path(path).stat().st_size
    except (OSError, PermissionError):
        return 0


def format_size(size_bytes: int) -> str:
    """Format a size in bytes to a human-readable string.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable size string (e.g., "1.5 MB")
    """
    if size_bytes < 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(size_bytes)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    return f"{size:.1f} {units[unit_index]}"


def match_patterns(
    path: Union[str, Path],
    patterns: List[str],
    root: Optional[Path] = None,
) -> bool:
    """Check if a path matches any of the given patterns.
    
    Args:
        path: Path to check
        patterns: List of glob patterns
        root: Optional root path for relative matching
        
    Returns:
        True if path matches any pattern
    """
    path = Path(path)
    path_str = str(path)
    
    # Also check relative path if root is provided
    relative_str = None
    if root:
        try:
            relative_str = str(path.relative_to(root))
        except ValueError:
            pass
    
    for pattern in patterns:
        # Try full path
        if fnmatch.fnmatch(path_str, pattern):
            return True
        
        # Try just the name
        if fnmatch.fnmatch(path.name, pattern):
            return True
        
        # Try relative path
        if relative_str and fnmatch.fnmatch(relative_str, pattern):
            return True
    
    return False


def count_items(path: Path, pattern: str = "**/*") -> int:
    """Count items matching a pattern.
    
    Args:
        path: Root path to search
        pattern: Glob pattern
        
    Returns:
        Number of matching items
    """
    try:
        return sum(1 for _ in Path(path).glob(pattern))
    except (OSError, PermissionError):
        return 0


def get_free_space(path: Path) -> int:
    """Get free disk space at the given path.
    
    Args:
        path: Path to check
        
    Returns:
        Free space in bytes
    """
    try:
        path = Path(path)
        if not path.exists():
            path = path.parent
        
        stat = os.statvfs(path)
        return stat.f_bavail * stat.f_frsize
    except (OSError, AttributeError):
        # AttributeError for Windows (statvfs not available)
        try:
            # Windows fallback
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(  # type: ignore
                ctypes.c_wchar_p(str(path)),
                None,
                None,
                ctypes.pointer(free_bytes),
            )
            return free_bytes.value
        except (OSError, AttributeError):
            return 0


def is_safe_path(path: Path, root: Path) -> bool:
    """Check if a path is safe to operate on (within root).
    
    Prevents directory traversal attacks and operations outside root.
    
    Args:
        path: Path to check
        root: Root directory that should contain path
        
    Returns:
        True if path is within root
    """
    try:
        path = Path(path).resolve()
        root = Path(root).resolve()
        return path == root or root in path.parents
    except (OSError, ValueError):
        return False

