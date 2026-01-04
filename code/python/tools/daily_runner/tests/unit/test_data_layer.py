"""
Tests for the data layer (repositories and managers).

Test IDs:
- 3.T1: Config loads defaults when file missing
- 3.T2: Config persists changes correctly
- 3.T3: Team repository lists all teams in directory
- 3.T4: Team repository filters inactive members
- 3.T5: Team repository sorts alphabetically by display_name
- 3.T6: History enforces 2000 entry limit (FIFO)
- 3.T7: History atomic write survives interruption
- 3.T8: History handles corrupted file gracefully
- 3.T9: Recovery manager detects existing session
- 3.T10: Recovery manager auto-save triggers correctly
- 3.T11: Recovery manager clears file on completion
"""

import json
import time
from pathlib import Path
from typing import Any

import pytest

from src.core.models import (
    AppConfig,
    MeetingRecord,
    MeetingState,
    MeetingStatus,
    SessionRecovery,
)
from src.data.config_manager import ConfigManager
from src.data.history_repository import HistoryRepository
from src.data.recovery_manager import RecoveryManager
from src.data.team_repository import TeamNotFoundError, TeamRepository

# =============================================================================
# Test 3.T1-T2: Config Manager Tests
# =============================================================================


class TestConfigManagerDefaults:
    """Test 3.T1: Config loads defaults when file missing."""

    def test_load_creates_default_when_missing(self, temp_dir: Path) -> None:
        """Test that loading without a file creates defaults."""
        config_path = temp_dir / "config.json"
        manager = ConfigManager(config_path)

        config = manager.load()

        assert config.version == "1.0"
        assert config.timer.default_speaker_time_seconds == 180
        assert config.teams.default_team == "imagine_dragons"

    def test_load_saves_default_file(self, temp_dir: Path) -> None:
        """Test that loading without a file saves the defaults."""
        config_path = temp_dir / "config.json"
        manager = ConfigManager(config_path)

        manager.load()

        assert config_path.exists()
        data = json.loads(config_path.read_text())
        assert data["version"] == "1.0"

    def test_config_property_loads_automatically(self, temp_dir: Path) -> None:
        """Test that config property loads on first access."""
        config_path = temp_dir / "config.json"
        manager = ConfigManager(config_path)

        # Access via property
        config = manager.config

        assert config is not None
        assert config.timer.default_speaker_time_seconds == 180

    def test_create_default_returns_valid_config(self) -> None:
        """Test that create_default returns a valid AppConfig."""
        config = AppConfig.create_default()

        assert config.timer.default_speaker_time_seconds == 180
        assert config.timer.transition_time_seconds == 30
        assert config.alerts.warning_color == "#FFA500"


class TestConfigManagerPersistence:
    """Test 3.T2: Config persists changes correctly."""

    def test_save_persists_to_file(self, temp_dir: Path) -> None:
        """Test that save writes config to file."""
        config_path = temp_dir / "config.json"
        manager = ConfigManager(config_path)
        manager.load()

        manager.save()

        assert config_path.exists()

    def test_set_and_save_persists_changes(self, temp_dir: Path) -> None:
        """Test that set + save persists configuration changes."""
        config_path = temp_dir / "config.json"
        manager = ConfigManager(config_path)
        manager.load()

        manager.set("timer.default_speaker_time_seconds", 240)
        manager.save()

        # Reload and verify
        manager2 = ConfigManager(config_path)
        config = manager2.load()
        assert config.timer.default_speaker_time_seconds == 240

    def test_get_returns_correct_value(self, temp_dir: Path) -> None:
        """Test that get returns correct nested values."""
        config_path = temp_dir / "config.json"
        manager = ConfigManager(config_path)
        manager.load()

        value = manager.get("timer.default_speaker_time_seconds")

        assert value == 180

    def test_get_returns_default_for_missing_key(self, temp_dir: Path) -> None:
        """Test that get returns default for missing keys."""
        config_path = temp_dir / "config.json"
        manager = ConfigManager(config_path)
        manager.load()

        value = manager.get("nonexistent.key", default="fallback")

        assert value == "fallback"

    def test_set_raises_for_invalid_key(self, temp_dir: Path) -> None:
        """Test that set raises ValueError for invalid keys."""
        config_path = temp_dir / "config.json"
        manager = ConfigManager(config_path)
        manager.load()

        with pytest.raises(ValueError):
            manager.set("invalid.key.path", "value")

    def test_reload_reads_from_file(self, temp_dir: Path) -> None:
        """Test that reload reads fresh data from file."""
        config_path = temp_dir / "config.json"
        manager = ConfigManager(config_path)
        manager.load()

        # Modify file directly
        data = json.loads(config_path.read_text())
        data["timer"]["default_speaker_time_seconds"] = 300
        config_path.write_text(json.dumps(data))

        # Reload
        config = manager.reload()

        assert config.timer.default_speaker_time_seconds == 300

    def test_handles_corrupted_config(self, temp_dir: Path) -> None:
        """Test that corrupted config is handled gracefully."""
        config_path = temp_dir / "config.json"
        config_path.write_text("invalid json {{{")

        manager = ConfigManager(config_path)
        config = manager.load()

        # Should return defaults
        assert config.timer.default_speaker_time_seconds == 180
        # Corrupted file should be backed up
        assert (temp_dir / "config.corrupted.json").exists()

    def test_reset_to_defaults(self, temp_dir: Path) -> None:
        """Test resetting config to defaults."""
        config_path = temp_dir / "config.json"
        manager = ConfigManager(config_path)
        manager.load()

        # Modify a value
        manager.set("timer.default_speaker_time_seconds", 300)
        manager.save()
        assert manager.config.timer.default_speaker_time_seconds == 300

        # Reset to defaults
        config = manager.reset_to_defaults()

        assert config.timer.default_speaker_time_seconds == 180

        # Verify file was updated
        manager2 = ConfigManager(config_path)
        assert manager2.load().timer.default_speaker_time_seconds == 180


# =============================================================================
# Test 3.T3-T5: Team Repository Tests
# =============================================================================


class TestTeamRepositoryListTeams:
    """Test 3.T3: Team repository lists all teams in directory."""

    def test_list_teams_returns_all_teams(self, temp_dir: Path) -> None:
        """Test listing all teams in directory."""
        teams_dir = temp_dir / "teams"
        teams_dir.mkdir()

        # Create team files
        for name in ["alpha", "beta", "gamma"]:
            (teams_dir / f"{name}.json").write_text(
                json.dumps(self._minimal_team(name))
            )

        repo = TeamRepository(teams_dir)
        teams = repo.list_teams()

        assert sorted(teams) == ["alpha", "beta", "gamma"]

    def test_list_teams_empty_directory(self, temp_dir: Path) -> None:
        """Test listing teams in empty directory."""
        teams_dir = temp_dir / "teams"
        teams_dir.mkdir()

        repo = TeamRepository(teams_dir)
        teams = repo.list_teams()

        assert teams == []

    def test_list_teams_missing_directory(self, temp_dir: Path) -> None:
        """Test listing teams when directory doesn't exist."""
        repo = TeamRepository(temp_dir / "nonexistent")
        teams = repo.list_teams()

        assert teams == []

    def _minimal_team(self, name: str) -> dict[str, Any]:
        """Create minimal team data."""
        return {
            "team": {"name": name, "emoji": "🧪"},
            "members": [
                {
                    "id": "member1",
                    "name": "Member One",
                    "display_name": "Member",
                    "email": "member@test.com",
                    "daily_config": {"default_time_seconds": 180, "active": True},
                }
            ],
        }


class TestTeamRepositoryFiltering:
    """Test 3.T4: Team repository filters inactive members."""

    def test_get_active_members_excludes_inactive(self, temp_dir: Path) -> None:
        """Test that inactive members are excluded."""
        teams_dir = temp_dir / "teams"
        teams_dir.mkdir()

        team_data = {
            "team": {"name": "Test", "emoji": "🧪"},
            "members": [
                {
                    "id": "active1",
                    "name": "Active One",
                    "display_name": "Active",
                    "email": "active@test.com",
                    "daily_config": {"default_time_seconds": 180, "active": True},
                },
                {
                    "id": "inactive1",
                    "name": "Inactive One",
                    "display_name": "Inactive",
                    "email": "inactive@test.com",
                    "daily_config": {"default_time_seconds": 180, "active": False},
                },
            ],
        }
        (teams_dir / "test.json").write_text(json.dumps(team_data))

        repo = TeamRepository(teams_dir)
        active = repo.get_active_members("test")

        assert len(active) == 1
        assert active[0].id == "active1"

    def test_get_member_by_id_finds_member(self, temp_dir: Path) -> None:
        """Test finding a specific member by ID."""
        teams_dir = temp_dir / "teams"
        teams_dir.mkdir()

        team_data = {
            "team": {"name": "Test", "emoji": "🧪"},
            "members": [
                {
                    "id": "alice",
                    "name": "Alice",
                    "display_name": "Alice",
                    "email": "alice@test.com",
                    "daily_config": {"default_time_seconds": 180, "active": True},
                },
            ],
        }
        (teams_dir / "test.json").write_text(json.dumps(team_data))

        repo = TeamRepository(teams_dir)
        member = repo.get_member_by_id("test", "alice")

        assert member is not None
        assert member.name == "Alice"

    def test_get_member_by_id_returns_none_for_missing(
        self, temp_dir: Path
    ) -> None:
        """Test that missing member returns None."""
        teams_dir = temp_dir / "teams"
        teams_dir.mkdir()

        team_data = {
            "team": {"name": "Test", "emoji": "🧪"},
            "members": [
                {
                    "id": "alice",
                    "name": "Alice",
                    "display_name": "Alice",
                    "email": "alice@test.com",
                    "daily_config": {"default_time_seconds": 180, "active": True},
                },
            ],
        }
        (teams_dir / "test.json").write_text(json.dumps(team_data))

        repo = TeamRepository(teams_dir)
        member = repo.get_member_by_id("test", "unknown")

        assert member is None


class TestTeamRepositorySorting:
    """Test 3.T5: Team repository sorts alphabetically by display_name."""

    def test_get_sorted_members_alphabetical(self, temp_dir: Path) -> None:
        """Test sorting members alphabetically."""
        teams_dir = temp_dir / "teams"
        teams_dir.mkdir()

        team_data = {
            "team": {"name": "Test", "emoji": "🧪"},
            "members": [
                {
                    "id": "charlie",
                    "name": "Charlie",
                    "display_name": "Charlie",
                    "email": "c@test.com",
                    "daily_config": {"default_time_seconds": 180, "active": True},
                },
                {
                    "id": "alice",
                    "name": "Alice",
                    "display_name": "Alice",
                    "email": "a@test.com",
                    "daily_config": {"default_time_seconds": 180, "active": True},
                },
                {
                    "id": "bob",
                    "name": "Bob",
                    "display_name": "Bob",
                    "email": "b@test.com",
                    "daily_config": {"default_time_seconds": 180, "active": True},
                },
            ],
        }
        (teams_dir / "test.json").write_text(json.dumps(team_data))

        repo = TeamRepository(teams_dir)
        members = repo.get_sorted_members("test", order="display_name")

        names = [m.display_name for m in members]
        assert names == ["Alice", "Bob", "Charlie"]

    def test_load_team_raises_for_missing(self, temp_dir: Path) -> None:
        """Test that loading missing team raises error."""
        teams_dir = temp_dir / "teams"
        teams_dir.mkdir()

        repo = TeamRepository(teams_dir)

        with pytest.raises(TeamNotFoundError):
            repo.load_team("nonexistent")

    def test_team_exists_check(self, temp_dir: Path) -> None:
        """Test team existence check."""
        teams_dir = temp_dir / "teams"
        teams_dir.mkdir()

        team_data = {
            "team": {"name": "Test", "emoji": "🧪"},
            "members": [
                {
                    "id": "alice",
                    "name": "Alice",
                    "display_name": "Alice",
                    "email": "a@test.com",
                    "daily_config": {"default_time_seconds": 180, "active": True},
                },
            ],
        }
        (teams_dir / "exists.json").write_text(json.dumps(team_data))

        repo = TeamRepository(teams_dir)

        assert repo.team_exists("exists") is True
        assert repo.team_exists("missing") is False

    def test_get_team_name(self, temp_dir: Path) -> None:
        """Test getting team display name."""
        teams_dir = temp_dir / "teams"
        teams_dir.mkdir()

        team_data = {
            "team": {"name": "Awesome Team", "emoji": "🚀"},
            "members": [
                {
                    "id": "alice",
                    "name": "Alice",
                    "display_name": "Alice",
                    "email": "a@test.com",
                    "daily_config": {"default_time_seconds": 180, "active": True},
                },
            ],
        }
        (teams_dir / "awesome.json").write_text(json.dumps(team_data))

        repo = TeamRepository(teams_dir)
        name = repo.get_team_name("awesome")

        assert name == "Awesome Team"

    def test_get_member_ids(self, temp_dir: Path) -> None:
        """Test getting list of member IDs."""
        teams_dir = temp_dir / "teams"
        teams_dir.mkdir()

        team_data = {
            "team": {"name": "Test", "emoji": "🧪"},
            "members": [
                {
                    "id": "bob",
                    "name": "Bob",
                    "display_name": "Bob",
                    "email": "b@test.com",
                    "daily_config": {"default_time_seconds": 180, "active": True},
                },
                {
                    "id": "alice",
                    "name": "Alice",
                    "display_name": "Alice",
                    "email": "a@test.com",
                    "daily_config": {"default_time_seconds": 180, "active": True},
                },
            ],
        }
        (teams_dir / "test.json").write_text(json.dumps(team_data))

        repo = TeamRepository(teams_dir)
        ids = repo.get_member_ids("test")

        # Should be sorted alphabetically by display_name
        assert ids == ["alice", "bob"]

    def test_clear_cache(self, temp_dir: Path) -> None:
        """Test clearing team cache."""
        teams_dir = temp_dir / "teams"
        teams_dir.mkdir()

        team_data: dict[str, Any] = {
            "team": {"name": "Test", "emoji": "🧪"},
            "members": [
                {
                    "id": "alice",
                    "name": "Alice",
                    "display_name": "Alice",
                    "email": "a@test.com",
                    "daily_config": {"default_time_seconds": 180, "active": True},
                },
            ],
        }
        (teams_dir / "test.json").write_text(json.dumps(team_data))

        repo = TeamRepository(teams_dir)
        repo.load_team("test")

        # Modify file
        team_data["team"]["name"] = "Modified Team"
        (teams_dir / "test.json").write_text(json.dumps(team_data))

        # Should still return cached value
        assert repo.get_team_name("test") == "Test"

        # After clear, should return new value
        repo.clear_cache()
        assert repo.get_team_name("test") == "Modified Team"


# =============================================================================
# Test 3.T6-T8: History Repository Tests
# =============================================================================


class TestHistoryRepositoryLimit:
    """Test 3.T6: History enforces 2000 entry limit (FIFO)."""

    def test_enforces_max_entries_limit(self, temp_dir: Path) -> None:
        """Test that history enforces max entries with FIFO."""
        repo = HistoryRepository("test", data_dir=temp_dir, max_entries=10)
        repo.load()

        # Add more than limit
        for i in range(15):
            record = MeetingRecord(
                id=f"meeting-{i:03d}",
                date=f"2026-01-{(i % 28) + 1:02d}",
                start_time="09:00:00",
                end_time="09:15:00",
                total_duration_seconds=900,
                expected_duration_seconds=900,
                status=MeetingStatus.COMPLETED,
            )
            repo.save_entry(record)

        # Should only have 10 entries (the last 10)
        entries = repo.get_entries()
        assert len(entries) == 10
        assert entries[0].id == "meeting-005"
        assert entries[-1].id == "meeting-014"

    def test_get_entries_with_date_filter(self, temp_dir: Path) -> None:
        """Test filtering entries by date range."""
        repo = HistoryRepository("test", data_dir=temp_dir)
        repo.load()

        dates = ["2026-01-01", "2026-01-05", "2026-01-10", "2026-01-15"]
        for i, date in enumerate(dates):
            record = MeetingRecord(
                id=f"2026-01-{(i+1):02d}T09:00:00",
                date=date,
                start_time="09:00:00",
                end_time="09:15:00",
                total_duration_seconds=900,
                expected_duration_seconds=900,
                status=MeetingStatus.COMPLETED,
            )
            repo.save_entry(record)

        entries = repo.get_entries(start_date="2026-01-03", end_date="2026-01-12")

        assert len(entries) == 2
        assert entries[0].date == "2026-01-05"
        assert entries[1].date == "2026-01-10"

    def test_get_latest_entries(self, temp_dir: Path) -> None:
        """Test getting the most recent entries."""
        repo = HistoryRepository("test", data_dir=temp_dir)
        repo.load()

        for i in range(5):
            record = MeetingRecord(
                id=f"2026-01-{(i+1):02d}T09:00:00",
                date=f"2026-01-{(i+1):02d}",
                start_time="09:00:00",
                end_time="09:15:00",
                total_duration_seconds=900,
                expected_duration_seconds=900,
                status=MeetingStatus.COMPLETED,
            )
            repo.save_entry(record)

        latest = repo.get_latest(count=2)

        assert len(latest) == 2
        assert latest[-1].date == "2026-01-05"

    def test_get_entry_count(self, temp_dir: Path) -> None:
        """Test getting entry count."""
        repo = HistoryRepository("test", data_dir=temp_dir)
        repo.load()

        assert repo.get_entry_count() == 0

        record = MeetingRecord(
            id="2026-01-01T09:00:00",
            date="2026-01-01",
            start_time="09:00:00",
            end_time="09:15:00",
            total_duration_seconds=900,
            expected_duration_seconds=900,
            status=MeetingStatus.COMPLETED,
        )
        repo.save_entry(record)

        assert repo.get_entry_count() == 1


class TestHistoryRepositoryAtomicWrite:
    """Test 3.T7: History atomic write survives interruption."""

    def test_save_creates_valid_file(self, temp_dir: Path) -> None:
        """Test that save creates a valid JSON file."""
        repo = HistoryRepository("test", data_dir=temp_dir)
        repo.load()

        record = MeetingRecord(
            id="meeting-001",
            date="2026-01-04",
            start_time="09:00:00",
            end_time="09:15:00",
            total_duration_seconds=900,
            expected_duration_seconds=900,
            status=MeetingStatus.COMPLETED,
        )
        repo.save_entry(record)

        # Read file directly
        file_path = temp_dir / "history_test.json"
        data = json.loads(file_path.read_text())
        assert "entries" in data
        assert len(data["entries"]) == 1

    def test_no_temp_file_after_save(self, temp_dir: Path) -> None:
        """Test that temp file is cleaned up after save."""
        repo = HistoryRepository("test", data_dir=temp_dir)
        repo.load()

        record = MeetingRecord(
            id="meeting-001",
            date="2026-01-04",
            start_time="09:00:00",
            end_time="09:15:00",
            total_duration_seconds=900,
            expected_duration_seconds=900,
            status=MeetingStatus.COMPLETED,
        )
        repo.save_entry(record)

        # Check no temp file exists
        temp_file = temp_dir / "history_test.tmp"
        assert not temp_file.exists()


class TestHistoryRepositoryCorruption:
    """Test 3.T8: History handles corrupted file gracefully."""

    def test_handles_corrupted_json(self, temp_dir: Path) -> None:
        """Test that corrupted JSON is handled gracefully."""
        history_path = temp_dir / "history_test.json"
        history_path.write_text("invalid json {{{")

        repo = HistoryRepository("test", data_dir=temp_dir)
        repo.load()

        # Should return empty history
        entries = repo.get_entries()
        assert entries == []

        # Corrupted file should be backed up
        assert (temp_dir / "history_test.corrupted.json").exists()

    def test_handles_invalid_schema(self, temp_dir: Path) -> None:
        """Test that invalid schema is handled gracefully."""
        history_path = temp_dir / "history_test.json"
        history_path.write_text(json.dumps({"invalid": "schema"}))

        repo = HistoryRepository("test", data_dir=temp_dir)
        repo.load()

        # Should return empty history
        entries = repo.get_entries()
        assert entries == []


# =============================================================================
# Test 3.T9-T11: Recovery Manager Tests
# =============================================================================


class TestRecoveryManagerDetection:
    """Test 3.T9: Recovery manager detects existing session."""

    def test_has_recovery_returns_true_when_exists(self, temp_dir: Path) -> None:
        """Test detection of existing recovery file."""
        recovery_path = temp_dir / "recovery.json"
        session = SessionRecovery.create_new("test", ["alice", "bob"])
        recovery_path.write_text(json.dumps(session.to_json_dict()))

        manager = RecoveryManager(recovery_path)

        assert manager.has_recovery() is True

    def test_has_recovery_returns_false_when_missing(
        self, temp_dir: Path
    ) -> None:
        """Test detection when no recovery file."""
        recovery_path = temp_dir / "recovery.json"
        manager = RecoveryManager(recovery_path)

        assert manager.has_recovery() is False

    def test_has_recovery_returns_false_for_invalid(self, temp_dir: Path) -> None:
        """Test that invalid file returns False."""
        recovery_path = temp_dir / "recovery.json"
        recovery_path.write_text("invalid json")

        manager = RecoveryManager(recovery_path)

        assert manager.has_recovery() is False

    def test_load_recovery_returns_session(self, temp_dir: Path) -> None:
        """Test loading existing recovery session."""
        recovery_path = temp_dir / "recovery.json"
        session = SessionRecovery.create_new("test", ["alice", "bob"])
        session.global_elapsed_seconds = 300
        recovery_path.write_text(json.dumps(session.to_json_dict()))

        manager = RecoveryManager(recovery_path)
        loaded = manager.load_recovery()

        assert loaded is not None
        assert loaded.team_id == "test"
        assert loaded.global_elapsed_seconds == 300


class TestRecoveryManagerAutoSave:
    """Test 3.T10: Recovery manager auto-save triggers correctly."""

    def test_auto_save_calls_callback(self, temp_dir: Path) -> None:
        """Test that auto-save calls the state callback."""
        recovery_path = temp_dir / "recovery.json"
        manager = RecoveryManager(recovery_path, auto_save_interval=1)

        call_count = 0
        session = SessionRecovery.create_new("test", ["alice"])

        def callback() -> SessionRecovery:
            nonlocal call_count
            call_count += 1
            return session

        manager.start_auto_save(callback)

        # Wait for at least one auto-save
        time.sleep(1.5)

        manager.stop_auto_save()

        assert call_count >= 1
        assert recovery_path.exists()

    def test_auto_save_can_be_stopped(self, temp_dir: Path) -> None:
        """Test that auto-save can be stopped."""
        recovery_path = temp_dir / "recovery.json"
        manager = RecoveryManager(recovery_path, auto_save_interval=1)

        session = SessionRecovery.create_new("test", ["alice"])
        manager.start_auto_save(lambda: session)

        assert manager.is_auto_save_running() is True

        manager.stop_auto_save()

        assert manager.is_auto_save_running() is False


class TestRecoveryManagerClear:
    """Test 3.T11: Recovery manager clears file on completion."""

    def test_clear_deletes_file(self, temp_dir: Path) -> None:
        """Test that clear removes the recovery file."""
        recovery_path = temp_dir / "recovery.json"
        session = SessionRecovery.create_new("test", ["alice"])
        recovery_path.write_text(json.dumps(session.to_json_dict()))

        manager = RecoveryManager(recovery_path)
        manager.clear_recovery()

        assert not recovery_path.exists()

    def test_clear_stops_auto_save(self, temp_dir: Path) -> None:
        """Test that clear stops auto-save if running."""
        recovery_path = temp_dir / "recovery.json"
        manager = RecoveryManager(recovery_path, auto_save_interval=1)

        session = SessionRecovery.create_new("test", ["alice"])
        manager.start_auto_save(lambda: session)

        assert manager.is_auto_save_running() is True

        manager.clear_recovery()

        assert manager.is_auto_save_running() is False

    def test_save_and_load_round_trip(self, temp_dir: Path) -> None:
        """Test save and load round trip."""
        recovery_path = temp_dir / "recovery.json"
        manager = RecoveryManager(recovery_path)

        session = SessionRecovery.create_new("test_team", ["alice", "bob", "carol"])
        session.global_elapsed_seconds = 450
        session.current_speaker_index = 1
        session.state = MeetingState.SPEAKING

        manager.save_recovery(session)
        loaded = manager.load_recovery()

        assert loaded is not None
        assert loaded.team_id == "test_team"
        assert loaded.global_elapsed_seconds == 450
        assert loaded.current_speaker_index == 1

    def test_get_recovery_info(self, temp_dir: Path) -> None:
        """Test getting recovery summary info."""
        recovery_path = temp_dir / "recovery.json"
        manager = RecoveryManager(recovery_path)

        session = SessionRecovery.create_new("test_team", ["alice", "bob"])
        manager.save_recovery(session)

        info = manager.get_recovery_info()

        assert info is not None
        assert info["team_id"] == "test_team"
        assert info["state"] == "idle"
