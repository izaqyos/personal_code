"""Git-related utilities for Repo Cleaner."""

import subprocess
from pathlib import Path
from typing import Optional


def is_git_repository(path: Path) -> bool:
    """Check if the given path is within a git repository.
    
    Args:
        path: Path to check
        
    Returns:
        True if path is in a git repository
    """
    path = Path(path)
    
    # Check for .git directory
    if (path / ".git").is_dir():
        return True
    
    # Check parent directories
    for parent in path.parents:
        if (parent / ".git").is_dir():
            return True
    
    # Try git command as fallback
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return False


def get_git_root(path: Path) -> Optional[Path]:
    """Get the root directory of the git repository.
    
    Args:
        path: Path within the repository
        
    Returns:
        Path to git root, or None if not in a git repository
    """
    path = Path(path)
    
    # Check for .git directory
    if (path / ".git").is_dir():
        return path
    
    # Check parent directories
    for parent in path.parents:
        if (parent / ".git").is_dir():
            return parent
    
    # Try git command
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return Path(result.stdout.strip())
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass
    
    return None


def is_git_dirty(path: Path) -> bool:
    """Check if the git repository has uncommitted changes.
    
    Args:
        path: Path within the repository
        
    Returns:
        True if there are uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        # If output is not empty, there are changes
        return bool(result.stdout.strip())
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        # If we can't determine, assume not dirty
        return False


def is_ignored_by_git(path: Path, check_path: Path) -> bool:
    """Check if a path is ignored by git.
    
    Args:
        path: Path to git repository
        check_path: Path to check if ignored
        
    Returns:
        True if the path is ignored by git
    """
    try:
        result = subprocess.run(
            ["git", "check-ignore", "-q", str(check_path)],
            cwd=path,
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return False


def get_git_status_summary(path: Path) -> dict:
    """Get a summary of git repository status.
    
    Args:
        path: Path to git repository
        
    Returns:
        Dictionary with status information
    """
    status = {
        "is_repo": False,
        "root": None,
        "is_dirty": False,
        "branch": None,
        "uncommitted_changes": 0,
    }
    
    if not is_git_repository(path):
        return status
    
    status["is_repo"] = True
    status["root"] = get_git_root(path)
    status["is_dirty"] = is_git_dirty(path)
    
    # Get branch name
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            status["branch"] = result.stdout.strip() or "HEAD"
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass
    
    # Count uncommitted changes
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            lines = [l for l in result.stdout.strip().split("\n") if l]
            status["uncommitted_changes"] = len(lines)
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass
    
    return status

