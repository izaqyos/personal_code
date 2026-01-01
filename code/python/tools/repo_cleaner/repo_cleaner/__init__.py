"""Repo Cleaner - A tool for cleaning build artifacts across multiple programming languages."""

__version__ = "0.1.0"
__author__ = "Repo Cleaner Contributors"

from repo_cleaner.core.cleaner import RepoCleaner
from repo_cleaner.core.exceptions import RepoCleanerError

__all__ = ["RepoCleaner", "RepoCleanerError", "__version__"]

