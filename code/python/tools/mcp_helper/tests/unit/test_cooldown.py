"""Unit tests for re-auth cooldown mechanism."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from mcp_health.refresh.cooldown import CooldownStatus, ReauthCooldown, ServerCooldownData


class TestServerCooldownData:
    """Tests for ServerCooldownData dataclass."""

    def test_default_values(self) -> None:
        """Test default field values."""
        data = ServerCooldownData()
        assert data.attempts == []

    def test_to_dict(self) -> None:
        """Test serialization to dict."""
        now = datetime.now(timezone.utc)
        data = ServerCooldownData(attempts=[now])
        result = data.to_dict()

        assert "attempts" in result
        assert len(result["attempts"]) == 1
        assert result["attempts"][0] == now.isoformat()

    def test_from_dict(self) -> None:
        """Test deserialization from dict."""
        now = datetime.now(timezone.utc)
        raw = {"attempts": [now.isoformat()]}
        data = ServerCooldownData.from_dict(raw)

        assert len(data.attempts) == 1
        # Compare without microseconds due to ISO format precision
        assert data.attempts[0].replace(microsecond=0) == now.replace(microsecond=0)

    def test_from_dict_invalid(self) -> None:
        """Test deserialization with invalid data."""
        raw = {"attempts": ["not-a-date", None, ""]}
        data = ServerCooldownData.from_dict(raw)

        assert data.attempts == []

    def test_from_dict_empty(self) -> None:
        """Test deserialization from empty dict."""
        data = ServerCooldownData.from_dict({})
        assert data.attempts == []


class TestCooldownStatus:
    """Tests for CooldownStatus dataclass."""

    def test_allowed_status(self) -> None:
        """Test allowed cooldown status."""
        status = CooldownStatus(
            server="test",
            can_reauth=True,
            reason="No recent attempts",
        )
        assert status.can_reauth is True
        assert status.seconds_until_allowed == 0

    def test_blocked_status(self) -> None:
        """Test blocked cooldown status."""
        status = CooldownStatus(
            server="test",
            can_reauth=False,
            reason="Cooldown active",
            seconds_until_allowed=180,
        )
        assert status.can_reauth is False
        assert status.seconds_until_allowed == 180


class TestReauthCooldown:
    """Tests for ReauthCooldown class."""

    @pytest.fixture
    def cooldown_file(self, tmp_path: Path) -> Path:
        """Create a temporary cooldown file path."""
        return tmp_path / ".mcp-auth" / ".reauth-cooldown.json"

    @pytest.fixture
    def cooldown(self, cooldown_file: Path) -> ReauthCooldown:
        """Create a cooldown instance with temporary file."""
        return ReauthCooldown(cooldown_file=cooldown_file)

    def test_init_defaults(self, cooldown: ReauthCooldown) -> None:
        """Test default initialization."""
        assert cooldown.min_interval == 300  # 5 minutes
        assert cooldown.max_attempts == 3

    def test_init_custom_values(self, tmp_path: Path) -> None:
        """Test custom initialization values."""
        cooldown = ReauthCooldown(
            cooldown_file=tmp_path / "custom.json",
            min_interval_seconds=60,
            max_attempts_per_hour=5,
        )
        assert cooldown.min_interval == 60
        assert cooldown.max_attempts == 5

    def test_check_no_history(self, cooldown: ReauthCooldown) -> None:
        """Test check with no history allows reauth."""
        status = cooldown.check("test-server")

        assert status.server == "test-server"
        assert status.can_reauth is True
        assert status.attempts_in_window == 0

    def test_record_attempt(self, cooldown: ReauthCooldown) -> None:
        """Test recording an attempt."""
        cooldown.record_attempt("test-server")
        status = cooldown.check("test-server")

        assert status.attempts_in_window == 1

    def test_min_interval_enforcement(self, cooldown: ReauthCooldown) -> None:
        """Test minimum interval is enforced."""
        cooldown.record_attempt("test-server")
        status = cooldown.check("test-server")

        # Should be blocked immediately after recording
        assert status.can_reauth is False
        assert status.seconds_until_allowed > 0
        assert "wait" in status.reason.lower()

    def test_max_attempts_enforcement(self, tmp_path: Path) -> None:
        """Test max attempts per hour is enforced."""
        # Create cooldown with short interval for testing
        cooldown = ReauthCooldown(
            cooldown_file=tmp_path / "test.json",
            min_interval_seconds=1,  # Very short for testing
            max_attempts_per_hour=3,
        )

        # Record 3 attempts with enough time between
        now = datetime.now(timezone.utc)
        cooldown._data["test-server"] = ServerCooldownData(
            attempts=[
                now - timedelta(seconds=10),
                now - timedelta(seconds=8),
                now - timedelta(seconds=6),
            ]
        )

        status = cooldown.check("test-server")

        assert status.can_reauth is False
        assert status.attempts_in_window == 3
        assert "maximum" in status.reason.lower()

    def test_cooldown_expiry(self, tmp_path: Path) -> None:
        """Test cooldown expires after interval."""
        cooldown = ReauthCooldown(
            cooldown_file=tmp_path / "test.json",
            min_interval_seconds=60,
        )

        # Record an attempt 2 minutes ago (should be expired)
        old_time = datetime.now(timezone.utc) - timedelta(minutes=2)
        cooldown._data["test-server"] = ServerCooldownData(attempts=[old_time])

        status = cooldown.check("test-server")

        assert status.can_reauth is True
        assert status.reason == "Cooldown expired"

    def test_reset_single_server(self, cooldown: ReauthCooldown) -> None:
        """Test resetting cooldown for a single server."""
        cooldown.record_attempt("server-a")
        cooldown.record_attempt("server-b")

        reset_servers = cooldown.reset("server-a")

        assert reset_servers == ["server-a"]
        assert cooldown.check("server-a").attempts_in_window == 0
        assert cooldown.check("server-b").attempts_in_window == 1

    def test_reset_all_servers(self, cooldown: ReauthCooldown) -> None:
        """Test resetting cooldown for all servers."""
        cooldown.record_attempt("server-a")
        cooldown.record_attempt("server-b")

        reset_servers = cooldown.reset(None)

        assert set(reset_servers) == {"server-a", "server-b"}
        assert cooldown.check("server-a").attempts_in_window == 0
        assert cooldown.check("server-b").attempts_in_window == 0

    def test_reset_nonexistent(self, cooldown: ReauthCooldown) -> None:
        """Test resetting nonexistent server."""
        reset_servers = cooldown.reset("nonexistent")

        assert reset_servers == []

    def test_can_reauth_convenience(self, cooldown: ReauthCooldown) -> None:
        """Test can_reauth convenience method."""
        allowed, reason = cooldown.can_reauth("test-server")

        assert allowed is True
        assert isinstance(reason, str)

    def test_status_all_servers(self, cooldown: ReauthCooldown) -> None:
        """Test getting status for all servers."""
        cooldown.record_attempt("server-a")
        cooldown.record_attempt("server-b")

        statuses = cooldown.status()

        assert "server-a" in statuses
        assert "server-b" in statuses
        assert statuses["server-a"].server == "server-a"

    def test_status_summary(self, cooldown: ReauthCooldown) -> None:
        """Test human-readable status summary."""
        cooldown.record_attempt("test-server")

        summary = cooldown.status_summary()

        assert "test-server" in summary
        assert "blocked" in summary.lower() or "allowed" in summary.lower()

    def test_status_summary_empty(self, cooldown: ReauthCooldown) -> None:
        """Test status summary with no data."""
        summary = cooldown.status_summary()

        assert "no cooldown data" in summary.lower()

    def test_persistence_save(self, cooldown: ReauthCooldown, cooldown_file: Path) -> None:
        """Test data is saved to file."""
        cooldown.record_attempt("test-server")

        assert cooldown_file.exists()
        data = json.loads(cooldown_file.read_text())
        assert "servers" in data
        assert "test-server" in data["servers"]

    def test_persistence_load(self, cooldown_file: Path) -> None:
        """Test data is loaded from file."""
        # Create a cooldown file manually
        now = datetime.now(timezone.utc)
        cooldown_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": 1,
            "servers": {
                "test-server": {
                    "attempts": [now.isoformat()],
                }
            },
        }
        cooldown_file.write_text(json.dumps(data))

        # Load cooldown and verify
        cooldown = ReauthCooldown(cooldown_file=cooldown_file)
        status = cooldown.check("test-server")

        assert status.attempts_in_window == 1

    def test_persistence_invalid_json(self, cooldown_file: Path) -> None:
        """Test handling of invalid JSON in cooldown file."""
        cooldown_file.parent.mkdir(parents=True, exist_ok=True)
        cooldown_file.write_text("not valid json")

        # Should not raise, just start with empty data
        cooldown = ReauthCooldown(cooldown_file=cooldown_file)
        status = cooldown.check("test-server")

        assert status.can_reauth is True

    def test_prune_old_attempts(self, tmp_path: Path) -> None:
        """Test old attempts are pruned from history."""
        cooldown = ReauthCooldown(cooldown_file=tmp_path / "test.json")

        # Add attempts: 2 old (>1hr), 1 recent
        now = datetime.now(timezone.utc)
        cooldown._data["test-server"] = ServerCooldownData(
            attempts=[
                now - timedelta(hours=2),  # Should be pruned
                now - timedelta(hours=1, minutes=30),  # Should be pruned
                now - timedelta(minutes=30),  # Should remain
            ]
        )

        # Trigger prune via check
        status = cooldown.check("test-server")

        assert status.attempts_in_window == 1

    def test_multiple_servers_independent(self, cooldown: ReauthCooldown) -> None:
        """Test cooldowns for different servers are independent."""
        cooldown.record_attempt("server-a")

        status_a = cooldown.check("server-a")
        status_b = cooldown.check("server-b")

        assert status_a.can_reauth is False
        assert status_b.can_reauth is True

    def test_concurrent_attempts(self, cooldown: ReauthCooldown) -> None:
        """Test handling of rapid concurrent attempts."""
        # Rapidly record multiple attempts
        for _ in range(5):
            cooldown.record_attempt("test-server")

        status = cooldown.check("test-server")

        # Should have all attempts recorded (5 > max_attempts=3)
        assert status.can_reauth is False
        assert status.attempts_in_window == 5
