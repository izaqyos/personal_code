"""Cleaner modules for removing build artifacts."""

from repo_cleaner.cleaners.base import BaseCleaner, Pattern, PatternType, CleanResult
from repo_cleaner.cleaners.python import PythonCleaner
from repo_cleaner.cleaners.node import NodeCleaner
from repo_cleaner.cleaners.java import JavaCleaner
from repo_cleaner.cleaners.c_cpp import CCppCleaner
from repo_cleaner.cleaners.js_frameworks import (
    ReactCleaner,
    AngularCleaner,
    VueCleaner,
)

# Mapping from detector names to cleaners
CLEANER_REGISTRY = {
    "python": PythonCleaner,
    "node": NodeCleaner,
    "java": JavaCleaner,
    "c_cpp": CCppCleaner,
    "react": ReactCleaner,
    "angular": AngularCleaner,
    "vue": VueCleaner,
}

__all__ = [
    "BaseCleaner",
    "Pattern",
    "PatternType",
    "CleanResult",
    "PythonCleaner",
    "NodeCleaner",
    "JavaCleaner",
    "CCppCleaner",
    "ReactCleaner",
    "AngularCleaner",
    "VueCleaner",
    "CLEANER_REGISTRY",
]

