"""Detector modules for identifying project types."""

from repo_cleaner.detectors.base import BaseDetector, DetectionResult
from repo_cleaner.detectors.python import PythonDetector
from repo_cleaner.detectors.node import NodeDetector
from repo_cleaner.detectors.java import JavaDetector
from repo_cleaner.detectors.c_cpp import CCppDetector
from repo_cleaner.detectors.js_frameworks import (
    ReactDetector,
    AngularDetector,
    VueDetector,
)

# Registry of all available detectors (order matters - more specific first)
ALL_DETECTORS = [
    ReactDetector(),
    AngularDetector(),
    VueDetector(),
    PythonDetector(),
    NodeDetector(),
    JavaDetector(),
    CCppDetector(),
]

__all__ = [
    "BaseDetector",
    "DetectionResult",
    "PythonDetector",
    "NodeDetector",
    "JavaDetector",
    "CCppDetector",
    "ReactDetector",
    "AngularDetector",
    "VueDetector",
    "ALL_DETECTORS",
]

