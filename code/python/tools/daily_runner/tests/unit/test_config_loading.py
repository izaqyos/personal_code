"""
Tests for configuration file loading.

Test ID: 1.T2 - Config file loads with defaults when missing
"""

import json
from pathlib import Path


class TestConfigFileLoading:
    """Test configuration file loading behavior."""

    def test_config_file_exists_in_project(self) -> None:
        """Test that config.json exists in the project root."""
        # Get the project root (relative to this test file)
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "config.json"

        assert config_path.exists(), f"config.json not found at {config_path}"

    def test_config_file_is_valid_json(self) -> None:
        """Test that config.json contains valid JSON."""
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "config.json"

        with open(config_path) as f:
            config = json.load(f)

        assert isinstance(config, dict)

    def test_config_has_required_sections(self) -> None:
        """Test that config.json has all required sections."""
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "config.json"

        with open(config_path) as f:
            config = json.load(f)

        required_sections = ["version", "timer", "alerts", "history", "recovery", "ui", "teams"]
        for section in required_sections:
            assert section in config, f"Missing required section: {section}"

    def test_config_timer_defaults(self) -> None:
        """Test that timer section has correct default values."""
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "config.json"

        with open(config_path) as f:
            config = json.load(f)

        timer = config["timer"]
        assert timer["default_speaker_time_seconds"] == 180
        assert timer["transition_time_seconds"] == 30
        assert timer["grace_period_seconds"] == 15
        assert timer["warning_threshold_seconds"] == 30

    def test_config_teams_default(self) -> None:
        """Test that default team is set to imagine_dragons."""
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "config.json"

        with open(config_path) as f:
            config = json.load(f)

        assert config["teams"]["default_team"] == "imagine_dragons"

    def test_config_history_max_entries(self) -> None:
        """Test that history max_entries is set to 2000."""
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "config.json"

        with open(config_path) as f:
            config = json.load(f)

        assert config["history"]["max_entries"] == 2000


class TestTeamFileLoading:
    """Test team file loading behavior."""

    def test_default_team_file_exists(self) -> None:
        """Test that the default team file exists."""
        project_root = Path(__file__).parent.parent.parent
        team_path = project_root / "teams" / "imagine_dragons.json"

        assert team_path.exists(), f"Default team file not found at {team_path}"

    def test_default_team_file_is_valid_json(self) -> None:
        """Test that the default team file contains valid JSON."""
        project_root = Path(__file__).parent.parent.parent
        team_path = project_root / "teams" / "imagine_dragons.json"

        with open(team_path) as f:
            team_data = json.load(f)

        assert isinstance(team_data, dict)

    def test_default_team_has_members(self) -> None:
        """Test that the default team has members defined."""
        project_root = Path(__file__).parent.parent.parent
        team_path = project_root / "teams" / "imagine_dragons.json"

        with open(team_path) as f:
            team_data = json.load(f)

        assert "members" in team_data
        assert len(team_data["members"]) == 6  # Chen, Miri, Muhe, Osher, Yair, Yocheved

    def test_default_team_members_have_required_fields(self) -> None:
        """Test that team members have all required fields."""
        project_root = Path(__file__).parent.parent.parent
        team_path = project_root / "teams" / "imagine_dragons.json"

        with open(team_path) as f:
            team_data = json.load(f)

        required_fields = ["id", "name", "display_name", "email", "daily_config"]
        for member in team_data["members"]:
            for field in required_fields:
                assert field in member, f"Member missing required field: {field}"

    def test_default_team_members_alphabetical_by_display_name(self) -> None:
        """Test that members are in expected alphabetical order."""
        project_root = Path(__file__).parent.parent.parent
        team_path = project_root / "teams" / "imagine_dragons.json"

        with open(team_path) as f:
            team_data = json.load(f)

        display_names = [m["display_name"] for m in team_data["members"]]
        expected_order = ["Chen", "Miri", "Muhe", "Osher", "Yair", "Yocheved"]
        assert display_names == expected_order
