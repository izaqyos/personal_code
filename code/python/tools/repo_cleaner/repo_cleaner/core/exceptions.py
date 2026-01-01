"""Custom exceptions for Repo Cleaner."""

from typing import Optional


class RepoCleanerError(Exception):
    """Base exception for all Repo Cleaner errors."""

    def __init__(self, message: str, details: Optional[str] = None) -> None:
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.details:
            return f"{self.message}\nDetails: {self.details}"
        return self.message


class SafetyCheckError(RepoCleanerError):
    """Raised when a safety check fails.
    
    Examples:
    - Directory is not a git repository (when require_git is True)
    - Insufficient disk space
    - Maximum delete size exceeded
    """

    pass


class ConfigurationError(RepoCleanerError):
    """Raised when configuration is invalid.
    
    Examples:
    - Invalid YAML syntax
    - Unknown configuration keys
    - Invalid pattern format
    """

    pass


class DetectionError(RepoCleanerError):
    """Raised when project detection fails.
    
    Examples:
    - Cannot read directory
    - Permission denied
    """

    pass


class CleanError(RepoCleanerError):
    """Raised when cleaning operation fails.
    
    Examples:
    - Cannot delete file/directory
    - Permission denied
    - File in use
    """

    def __init__(
        self,
        message: str,
        path: Optional[str] = None,
        details: Optional[str] = None,
    ) -> None:
        self.path = path
        super().__init__(message, details)

    def __str__(self) -> str:
        parts = [self.message]
        if self.path:
            parts.append(f"Path: {self.path}")
        if self.details:
            parts.append(f"Details: {self.details}")
        return "\n".join(parts)

