"""Health report generation."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mcp_health.mcp.client import ConnectionResult, ConnectionStatus
from mcp_health.validators.base import TokenStatus, ValidationResult


class OverallStatus(Enum):
    """Overall health status for all servers."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

    def get_color(self) -> str:
        """Get color for this status."""
        colors = {
            OverallStatus.HEALTHY: "green",
            OverallStatus.DEGRADED: "yellow",
            OverallStatus.UNHEALTHY: "red",
        }
        return colors.get(self, "white")

    def get_symbol(self) -> str:
        """Get symbol for this status."""
        symbols = {
            OverallStatus.HEALTHY: "✓",
            OverallStatus.DEGRADED: "⚠",
            OverallStatus.UNHEALTHY: "✗",
        }
        return symbols.get(self, "?")


@dataclass
class ServerHealth:
    """Health status of a single server.

    Attributes:
        name: Server name
        token_result: Result of token validation
        connection_result: Result of MCP connection test
        refresh_attempted: Whether token refresh was attempted
        refresh_success: Whether refresh succeeded
        action_required: Action user needs to take
    """

    name: str
    token_result: ValidationResult | None = None
    connection_result: ConnectionResult | None = None
    refresh_attempted: bool = False
    refresh_success: bool = False
    action_required: str | None = None

    @property
    def is_healthy(self) -> bool:
        """Check if server is fully healthy."""
        token_ok = self.token_result is None or self.token_result.is_healthy()
        conn_ok = self.connection_result is None or self.connection_result.is_healthy()
        return token_ok and conn_ok

    @property
    def status(self) -> OverallStatus:
        """Get overall status for this server."""
        if self.is_healthy:
            return OverallStatus.HEALTHY
        elif self.token_result and self.token_result.status == TokenStatus.VALID:
            # Token OK but connection failed
            return OverallStatus.DEGRADED
        elif self.connection_result and self.connection_result.is_healthy():
            # Connection OK but token invalid
            return OverallStatus.DEGRADED
        return OverallStatus.UNHEALTHY


@dataclass
class HealthReport:
    """Complete health report for all servers.

    Attributes:
        servers: Dictionary of server name to health status
        timestamp: When the report was generated
        config_path: Path to the config file used
    """

    servers: dict[str, ServerHealth] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    config_path: str | None = None

    @property
    def overall_status(self) -> OverallStatus:
        """Get overall status across all servers."""
        if not self.servers:
            return OverallStatus.HEALTHY

        statuses = [s.status for s in self.servers.values()]

        if all(s == OverallStatus.HEALTHY for s in statuses):
            return OverallStatus.HEALTHY
        elif all(s == OverallStatus.UNHEALTHY for s in statuses):
            return OverallStatus.UNHEALTHY
        return OverallStatus.DEGRADED

    @property
    def healthy_count(self) -> int:
        """Count of healthy servers."""
        return sum(1 for s in self.servers.values() if s.is_healthy)

    @property
    def total_count(self) -> int:
        """Total number of servers."""
        return len(self.servers)

    def add_server(self, health: ServerHealth) -> None:
        """Add a server health entry."""
        self.servers[health.name] = health


class ReportGenerator:
    """Generates health reports in various formats.

    Example:
        generator = ReportGenerator()
        generator.generate_console(report)
        json_output = generator.generate_json(report)
    """

    def __init__(self, console: Console | None = None):
        """Initialize the generator.

        Args:
            console: Optional Rich console instance
        """
        self.console = console or Console()

    def generate_console(self, report: HealthReport, verbose: bool = False) -> None:
        """Generate console output with Rich formatting.

        Args:
            report: The health report to display
            verbose: Whether to show verbose output
        """
        # Header
        status = report.overall_status
        title = Text(f"MCP Server Health Check ({report.healthy_count}/{report.total_count})")
        title.stylize(f"bold {status.get_color()}")

        self.console.print()
        self.console.print(Panel(title, expand=False))
        self.console.print()

        # Server table
        table = Table(show_header=True, header_style="bold")
        table.add_column("Server", style="cyan")
        table.add_column("Token Status")
        table.add_column("Connection")
        table.add_column("Action Required")

        for name, health in report.servers.items():
            token_status = self._format_token_status(health.token_result)
            conn_status = self._format_connection_status(health.connection_result)
            action = health.action_required or ""

            table.add_row(name, token_status, conn_status, action)

        self.console.print(table)
        self.console.print()

        # Show actions required if any
        actions = [
            (name, h.action_required) for name, h in report.servers.items() if h.action_required
        ]
        if actions:
            self.console.print("[bold yellow]Actions Required:[/]")
            for name, action in actions:
                self.console.print(f"  • [cyan]{name}[/]: {action}")
            self.console.print()

        # Verbose output
        if verbose:
            self._print_verbose(report)

    def _format_token_status(self, result: ValidationResult | None) -> Text:
        """Format token validation result for display."""
        if result is None:
            return Text("Not checked", style="dim")

        status_styles = {
            TokenStatus.VALID: ("✓ Valid", "green"),
            TokenStatus.EXPIRING_SOON: ("⚠ Expiring Soon", "yellow"),
            TokenStatus.INVALID: ("✗ Invalid", "red"),
            TokenStatus.EXPIRED: ("⚠ Expired", "yellow"),
            TokenStatus.MISSING: ("✗ Missing", "red"),
            TokenStatus.NETWORK_ERROR: ("⚠ Network Error", "yellow"),
            TokenStatus.UNKNOWN: ("? Unknown", "dim"),
        }

        text, style = status_styles.get(result.status, (result.status.value, "white"))
        formatted = Text(text, style=style)

        # Append warning if present
        if result.warning:
            formatted.append(f" ({result.warning})", style="dim")

        return formatted

    def _format_connection_status(self, result: ConnectionResult | None) -> Text:
        """Format connection result for display."""
        if result is None:
            return Text("Not tested", style="dim")

        status_styles = {
            ConnectionStatus.HEALTHY: ("✓ Healthy", "green"),
            ConnectionStatus.UNHEALTHY: ("✗ Unhealthy", "red"),
            ConnectionStatus.TIMEOUT: ("⚠ Timeout", "yellow"),
            ConnectionStatus.SPAWN_FAILED: ("✗ Spawn Failed", "red"),
            ConnectionStatus.PROTOCOL_ERROR: ("✗ Protocol Error", "red"),
        }

        text, style = status_styles.get(result.status, (result.status.value, "white"))
        return Text(text, style=style)

    def _print_verbose(self, report: HealthReport) -> None:
        """Print verbose details."""
        self.console.print("[bold]Detailed Results:[/]")
        for name, health in report.servers.items():
            self.console.print(f"\n[cyan]{name}[/]:")
            if health.token_result:
                self.console.print(f"  Token: {health.token_result.message}")
                if health.token_result.user_info:
                    for k, v in health.token_result.user_info.items():
                        if v:
                            self.console.print(f"    {k}: {v}")
            if health.connection_result:
                self.console.print(f"  Connection: {health.connection_result.message}")
                if health.connection_result.resources:
                    self.console.print(f"    Resources: {len(health.connection_result.resources)}")

    def generate_json(self, report: HealthReport) -> str:
        """Generate JSON output.

        Args:
            report: The health report

        Returns:
            JSON string representation
        """
        data = self._report_to_dict(report)
        return json.dumps(data, indent=2, default=str)

    def _report_to_dict(self, report: HealthReport) -> dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "timestamp": report.timestamp.isoformat(),
            "config_path": report.config_path,
            "overall_status": report.overall_status.value,
            "healthy_count": report.healthy_count,
            "total_count": report.total_count,
            "servers": {
                name: self._server_health_to_dict(health) for name, health in report.servers.items()
            },
        }

    def _server_health_to_dict(self, health: ServerHealth) -> dict[str, Any]:
        """Convert server health to dictionary."""
        result: dict[str, Any] = {
            "status": health.status.value,
            "is_healthy": health.is_healthy,
        }

        if health.token_result:
            result["token"] = {
                "status": health.token_result.status.value,
                "message": health.token_result.message,
                "can_refresh": health.token_result.can_refresh,
                "user_info": health.token_result.user_info,
            }
            if health.token_result.expires_at:
                result["token"]["expires_at"] = health.token_result.expires_at.isoformat()
            if health.token_result.warning:
                result["token"]["warning"] = health.token_result.warning

        if health.connection_result:
            result["connection"] = {
                "status": health.connection_result.status.value,
                "message": health.connection_result.message,
                "resource_count": len(health.connection_result.resources),
            }

        if health.action_required:
            result["action_required"] = health.action_required

        if health.refresh_attempted:
            result["refresh_attempted"] = True
            result["refresh_success"] = health.refresh_success

        return result
