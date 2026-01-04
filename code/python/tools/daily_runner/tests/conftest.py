"""
Pytest configuration and shared fixtures for the Daily Standup Timer tests.
"""

import json
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_config() -> dict[str, Any]:
    """Return a sample configuration dictionary."""
    return {
        "version": "1.0",
        "timer": {
            "default_speaker_time_seconds": 180,
            "transition_time_seconds": 30,
            "grace_period_seconds": 15,
            "warning_threshold_seconds": 30,
        },
        "alerts": {
            "warning_color": "#FFA500",
            "overtime_color": "#FF0000",
            "flash_on_overtime": True,
        },
        "history": {
            "file_path": "data/history_{team_id}.json",
            "max_entries": 2000,
        },
        "recovery": {
            "enabled": True,
            "auto_save_interval_seconds": 5,
            "file_path": "data/.session_recovery.json",
        },
        "ui": {
            "theme": "light",
            "show_avatars": False,
        },
        "teams": {
            "directory": "teams",
            "default_team": "imagine_dragons",
        },
        "default_order": "alphabetical",
    }


@pytest.fixture
def temp_config(temp_dir: Path, sample_config: dict[str, Any]) -> Path:
    """Create a temporary config file."""
    config_path = temp_dir / "config.json"
    config_path.write_text(json.dumps(sample_config, indent=2))
    return config_path


@pytest.fixture
def sample_team_data() -> dict[str, Any]:
    """Return sample team data."""
    return {
        "team": {
            "name": "Test Team",
            "emoji": "🧪",
            "group_manager": {"name": "Manager", "email": "manager@test.com"},
            "team_leader": {"name": "Leader", "email": "leader@test.com"},
        },
        "members": [
            {
                "id": "alice",
                "name": "Alice Anderson",
                "display_name": "Alice",
                "email": "alice@test.com",
                "github": "alice-dev",
                "role": "Developer",
                "specialization": ["frontend"],
                "daily_config": {"default_time_seconds": 180, "active": True},
            },
            {
                "id": "bob",
                "name": "Bob Brown",
                "display_name": "Bob",
                "email": "bob@test.com",
                "github": "bob-dev",
                "role": "Developer",
                "specialization": ["backend"],
                "daily_config": {"default_time_seconds": 180, "active": True},
            },
        ],
    }


@pytest.fixture
def temp_team_file(temp_dir: Path, sample_team_data: dict[str, Any]) -> Path:
    """Create a temporary team file."""
    teams_dir = temp_dir / "teams"
    teams_dir.mkdir(parents=True, exist_ok=True)
    team_path = teams_dir / "test_team.json"
    team_path.write_text(json.dumps(sample_team_data, indent=2))
    return team_path


@pytest.fixture
def temp_history_file(temp_dir: Path) -> Path:
    """Create a temporary empty history file."""
    data_dir = temp_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    history_path = data_dir / "history_test_team.json"
    history_path.write_text(json.dumps({"version": "1.0", "entries": []}, indent=2))
    return history_path


@pytest.fixture
def sample_meeting_record() -> dict[str, Any]:
    """Return a sample meeting record."""
    return {
        "id": "2026-01-04T09:00:00Z",
        "date": "2026-01-04",
        "start_time": "09:00:00",
        "end_time": "09:15:30",
        "total_duration_seconds": 930,
        "expected_duration_seconds": 1080,
        "status": "completed",
        "participants": [
            {
                "member_id": "alice",
                "display_name": "Alice",
                "status": "present",
                "allocated_time_seconds": 180,
                "actual_time_seconds": 165,
                "overtime_seconds": 0,
                "order_position": 1,
            },
            {
                "member_id": "bob",
                "display_name": "Bob",
                "status": "present",
                "allocated_time_seconds": 180,
                "actual_time_seconds": 195,
                "overtime_seconds": 15,
                "order_position": 2,
            },
        ],
        "notes": "",
    }
