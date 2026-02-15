"""Re-authentication cooldown management to prevent auth storms."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class CooldownStatus:
    """Status of cooldown for a specific server.

    Attributes:
        server: Server name
        can_reauth: Whether re-auth is currently allowed
        reason: Human-readable reason if blocked
        last_attempt: Timestamp of last re-auth attempt
        attempts_in_window: Number of attempts in the current hour window
        seconds_until_allowed: Seconds until re-auth is allowed (0 if allowed)
    """

    server: str
    can_reauth: bool
    reason: str
    last_attempt: datetime | None = None
    attempts_in_window: int = 0
    seconds_until_allowed: int = 0


@dataclass
class ServerCooldownData:
    """Cooldown data for a single server."""

    attempts: list[datetime] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary for JSON storage."""
        return {
            "attempts": [a.isoformat() for a in self.attempts],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ServerCooldownData":
        """Deserialize from dictionary."""
        attempts = []
        for a in data.get("attempts", []):
            try:
                attempts.append(datetime.fromisoformat(a))
            except (ValueError, TypeError):
                continue
        return cls(attempts=attempts)


class ReauthCooldown:
    """Track re-auth attempts and enforce cooldowns to prevent auth storms.

    Prevents repeated browser authentication popups by enforcing:
    - Minimum interval between attempts (default: 5 minutes)
    - Maximum attempts per hour (default: 3)

    Data is persisted to a JSON file for cross-session tracking.

    Example:
        cooldown = ReauthCooldown()

        # Check if reauth is allowed
        status = cooldown.check("perimeter81-atlassian")
        if status.can_reauth:
            # Perform reauth...
            cooldown.record_attempt("perimeter81-atlassian")
        else:
            print(f"Cooldown active: {status.reason}")

        # Reset cooldown after manual fix
        cooldown.reset("perimeter81-atlassian")
    """

    DEFAULT_COOLDOWN_FILE = Path.home() / ".mcp-auth" / ".reauth-cooldown.json"
    MIN_INTERVAL_SECONDS = 300  # 5 minutes
    MAX_ATTEMPTS_PER_HOUR = 3
    WINDOW_SECONDS = 3600  # 1 hour

    def __init__(
        self,
        cooldown_file: Path | None = None,
        min_interval_seconds: int | None = None,
        max_attempts_per_hour: int | None = None,
    ):
        """Initialize the cooldown tracker.

        Args:
            cooldown_file: Path to cooldown data file (default: ~/.mcp-auth/.reauth-cooldown.json)
            min_interval_seconds: Minimum seconds between attempts (default: 300)
            max_attempts_per_hour: Maximum attempts per hour (default: 3)
        """
        self.cooldown_file = cooldown_file or self.DEFAULT_COOLDOWN_FILE
        self.min_interval = min_interval_seconds or self.MIN_INTERVAL_SECONDS
        self.max_attempts = max_attempts_per_hour or self.MAX_ATTEMPTS_PER_HOUR
        self._data: dict[str, ServerCooldownData] = {}
        self._load()

    def _load(self) -> None:
        """Load cooldown data from file."""
        if not self.cooldown_file.exists():
            self._data = {}
            return

        try:
            raw = json.loads(self.cooldown_file.read_text())
            self._data = {}
            for server, server_data in raw.get("servers", {}).items():
                self._data[server] = ServerCooldownData.from_dict(server_data)
        except (json.JSONDecodeError, OSError, KeyError):
            self._data = {}

    def _save(self) -> None:
        """Save cooldown data to file."""
        # Ensure parent directory exists
        self.cooldown_file.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": 1,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "servers": {
                server: server_data.to_dict() for server, server_data in self._data.items()
            },
        }

        try:
            self.cooldown_file.write_text(json.dumps(data, indent=2))
        except OSError:
            # Silently fail - cooldown still works in memory
            pass

    def _prune_old_attempts(self, server: str) -> None:
        """Remove attempts older than the tracking window.

        Args:
            server: Server name
        """
        if server not in self._data:
            return

        now = datetime.now(timezone.utc)
        cutoff = now.replace(microsecond=0)
        from datetime import timedelta

        cutoff = cutoff - timedelta(seconds=self.WINDOW_SECONDS)

        self._data[server].attempts = [
            a for a in self._data[server].attempts if a > cutoff
        ]

    def check(self, server: str) -> CooldownStatus:
        """Check if re-auth is allowed for a server.

        Args:
            server: Server name to check

        Returns:
            CooldownStatus with allowed status and reason
        """
        now = datetime.now(timezone.utc)
        self._prune_old_attempts(server)

        # No history = allowed
        if server not in self._data or not self._data[server].attempts:
            return CooldownStatus(
                server=server,
                can_reauth=True,
                reason="No recent attempts",
                attempts_in_window=0,
            )

        attempts = self._data[server].attempts
        last_attempt = max(attempts)
        attempts_count = len(attempts)

        # Check max attempts per hour
        if attempts_count >= self.max_attempts:
            return CooldownStatus(
                server=server,
                can_reauth=False,
                reason=f"Maximum {self.max_attempts} attempts per hour reached. Try manual recovery.",
                last_attempt=last_attempt,
                attempts_in_window=attempts_count,
                seconds_until_allowed=self.WINDOW_SECONDS,  # Wait for oldest to expire
            )

        # Check minimum interval
        seconds_since_last = (now - last_attempt).total_seconds()
        if seconds_since_last < self.min_interval:
            remaining = int(self.min_interval - seconds_since_last)
            minutes = remaining // 60
            seconds = remaining % 60
            return CooldownStatus(
                server=server,
                can_reauth=False,
                reason=f"Cooldown active. Wait {minutes}m {seconds}s before next attempt.",
                last_attempt=last_attempt,
                attempts_in_window=attempts_count,
                seconds_until_allowed=remaining,
            )

        # Allowed
        return CooldownStatus(
            server=server,
            can_reauth=True,
            reason="Cooldown expired",
            last_attempt=last_attempt,
            attempts_in_window=attempts_count,
        )

    def can_reauth(self, server: str) -> tuple[bool, str]:
        """Convenience method to check if re-auth is allowed.

        Args:
            server: Server name to check

        Returns:
            Tuple of (allowed, reason)
        """
        status = self.check(server)
        return status.can_reauth, status.reason

    def record_attempt(self, server: str) -> None:
        """Record a re-auth attempt for a server.

        Args:
            server: Server name
        """
        now = datetime.now(timezone.utc)

        if server not in self._data:
            self._data[server] = ServerCooldownData()

        self._data[server].attempts.append(now)
        self._prune_old_attempts(server)
        self._save()

    def reset(self, server: str | None = None) -> list[str]:
        """Reset cooldown for a server or all servers.

        Args:
            server: Server name to reset, or None to reset all

        Returns:
            List of servers that were reset
        """
        reset_servers: list[str] = []

        if server is None:
            reset_servers = list(self._data.keys())
            self._data = {}
        elif server in self._data:
            reset_servers = [server]
            del self._data[server]

        self._save()
        return reset_servers

    def status(self) -> dict[str, CooldownStatus]:
        """Get cooldown status for all tracked servers.

        Returns:
            Dictionary mapping server names to their CooldownStatus
        """
        result: dict[str, CooldownStatus] = {}
        for server in self._data:
            result[server] = self.check(server)
        return result

    def status_summary(self) -> str:
        """Get a human-readable summary of all cooldown states.

        Returns:
            Multi-line summary string
        """
        statuses = self.status()

        if not statuses:
            return "No cooldown data. Re-auth has not been attempted recently."

        lines = ["Cooldown Status:"]
        for server, status in statuses.items():
            if status.can_reauth:
                state = "✓ allowed"
            else:
                state = f"✗ blocked ({status.seconds_until_allowed}s remaining)"

            attempts = status.attempts_in_window
            lines.append(f"  {server}: {state} [{attempts}/{self.max_attempts} attempts/hr]")

        return "\n".join(lines)
