"""
Daily Standup Timer - A timer application for managing daily standup meetings.

This package provides both a Streamlit UI and CLI interface for running
timed daily standup meetings with configurable speaker times, transition
periods, and meeting history tracking.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("daily-standup-timer")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

__author__ = "Yosi Izaq"
