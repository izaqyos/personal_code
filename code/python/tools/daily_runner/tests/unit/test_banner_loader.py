"""Tests for schedule_loader."""

import json
from pathlib import Path

import pytest

from src.banner.errors import MalformedScheduleError, MissingScheduleError
from src.banner.schedule_loader import load_schedules


VALID_DATA = {
    "team_members": {"yocheved": "U07ANSFF3EX"},
    "rotation_schedule": {
        "26.Q2.1": {
            "champion": "yocheved",
            "dr": "2026-04-26",
            "go_nogo": "2026-04-30",
            "prod": "2026-05-03",
        },
    },
    "dod_schedule": {"2026-04-12": "chen"},
}


class TestLoadSchedules:
    def test_loads_valid_file(self, tmp_path: Path) -> None:
        path = tmp_path / "schedules.json"
        path.write_text(json.dumps(VALID_DATA))

        result = load_schedules(path)

        assert "26.Q2.1" in result.rotation_schedule
        assert result.rotation_schedule["26.Q2.1"].champion == "yocheved"

    def test_missing_file_raises(self, tmp_path: Path) -> None:
        path = tmp_path / "does_not_exist.json"

        with pytest.raises(MissingScheduleError) as exc_info:
            load_schedules(path)

        assert str(path) in exc_info.value.path

    def test_empty_path_raises(self) -> None:
        """Path("") normalizes to Path(".") which is not a file → MissingScheduleError."""
        with pytest.raises(MissingScheduleError):
            load_schedules(Path(""))

    def test_invalid_json_raises_malformed(self, tmp_path: Path) -> None:
        path = tmp_path / "schedules.json"
        path.write_text("{not valid json")

        with pytest.raises(MalformedScheduleError) as exc_info:
            load_schedules(path)

        assert "json" in exc_info.value.reason.lower()

    def test_missing_required_key_raises_malformed(self, tmp_path: Path) -> None:
        path = tmp_path / "schedules.json"
        path.write_text(json.dumps({"team_members": {}, "dod_schedule": {}}))

        with pytest.raises(MalformedScheduleError):
            load_schedules(path)

    def test_validation_error_is_compact(self, tmp_path: Path) -> None:
        """ValidationError reason should be a one-liner, not pydantic's full multi-line output."""
        path = tmp_path / "schedules.json"
        # Missing rotation_schedule + bad dod_schedule key shape (multiple errors).
        path.write_text(json.dumps({"team_members": {}, "dod_schedule": {"not-a-date": "x"}}))

        with pytest.raises(MalformedScheduleError) as exc_info:
            load_schedules(path)

        assert "\n" not in exc_info.value.reason
        assert "https://" not in exc_info.value.reason  # no pydantic doc URL

    def test_path_with_tilde_expands(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("HOME", str(tmp_path))
        target = tmp_path / "schedules.json"
        target.write_text(json.dumps(VALID_DATA))

        result = load_schedules(Path("~/schedules.json"))

        assert "26.Q2.1" in result.rotation_schedule
