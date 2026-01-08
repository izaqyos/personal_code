"""Integration tests for end-to-end health check flow."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from click.testing import CliRunner
from rich.console import Console

from mcp_health.cli import get_service_type, get_validator_for_server, main, run_health_check
from mcp_health.mcp.client import ConnectionResult, ConnectionStatus
from mcp_health.refresh.notifier import ServiceType
from mcp_health.reporting.report import (
    HealthReport,
    OverallStatus,
    ReportGenerator,
    ServerHealth,
)
from mcp_health.validators.base import TokenStatus, ValidationResult


class TestOverallStatus:
    """Tests for OverallStatus enum."""

    def test_get_color(self) -> None:
        """Test color mapping."""
        assert OverallStatus.HEALTHY.get_color() == "green"
        assert OverallStatus.DEGRADED.get_color() == "yellow"
        assert OverallStatus.UNHEALTHY.get_color() == "red"

    def test_get_symbol(self) -> None:
        """Test symbol mapping."""
        assert OverallStatus.HEALTHY.get_symbol() == "✓"
        assert OverallStatus.DEGRADED.get_symbol() == "⚠"
        assert OverallStatus.UNHEALTHY.get_symbol() == "✗"


class TestServerHealth:
    """Tests for ServerHealth dataclass."""

    def test_is_healthy_true(self) -> None:
        """Test is_healthy when everything is OK."""
        health = ServerHealth(
            name="test",
            token_result=ValidationResult(status=TokenStatus.VALID, message="OK"),
            connection_result=ConnectionResult(status=ConnectionStatus.HEALTHY, message="OK"),
        )
        assert health.is_healthy is True

    def test_is_healthy_token_invalid(self) -> None:
        """Test is_healthy when token is invalid."""
        health = ServerHealth(
            name="test",
            token_result=ValidationResult(status=TokenStatus.INVALID, message="Bad"),
        )
        assert health.is_healthy is False

    def test_is_healthy_connection_failed(self) -> None:
        """Test is_healthy when connection failed."""
        health = ServerHealth(
            name="test",
            token_result=ValidationResult(status=TokenStatus.VALID, message="OK"),
            connection_result=ConnectionResult(status=ConnectionStatus.UNHEALTHY, message="Failed"),
        )
        assert health.is_healthy is False

    def test_status_healthy(self) -> None:
        """Test status property for healthy server."""
        health = ServerHealth(
            name="test",
            token_result=ValidationResult(status=TokenStatus.VALID, message="OK"),
            connection_result=ConnectionResult(status=ConnectionStatus.HEALTHY, message="OK"),
        )
        assert health.status == OverallStatus.HEALTHY

    def test_status_degraded_connection_only(self) -> None:
        """Test status when only connection failed."""
        health = ServerHealth(
            name="test",
            token_result=ValidationResult(status=TokenStatus.VALID, message="OK"),
            connection_result=ConnectionResult(status=ConnectionStatus.UNHEALTHY, message="Failed"),
        )
        assert health.status == OverallStatus.DEGRADED

    def test_status_unhealthy(self) -> None:
        """Test status when both token and connection failed."""
        health = ServerHealth(
            name="test",
            token_result=ValidationResult(status=TokenStatus.INVALID, message="Bad"),
            connection_result=ConnectionResult(status=ConnectionStatus.UNHEALTHY, message="Failed"),
        )
        assert health.status == OverallStatus.UNHEALTHY


class TestHealthReport:
    """Tests for HealthReport dataclass."""

    def test_overall_status_all_healthy(self) -> None:
        """Test overall status when all servers are healthy."""
        report = HealthReport()
        report.add_server(
            ServerHealth(
                name="github",
                token_result=ValidationResult(status=TokenStatus.VALID, message="OK"),
            )
        )
        report.add_server(
            ServerHealth(
                name="slack",
                token_result=ValidationResult(status=TokenStatus.VALID, message="OK"),
            )
        )
        assert report.overall_status == OverallStatus.HEALTHY

    def test_overall_status_mixed(self) -> None:
        """Test overall status with mixed health."""
        report = HealthReport()
        report.add_server(
            ServerHealth(
                name="github",
                token_result=ValidationResult(status=TokenStatus.VALID, message="OK"),
            )
        )
        report.add_server(
            ServerHealth(
                name="slack",
                token_result=ValidationResult(status=TokenStatus.INVALID, message="Bad"),
            )
        )
        assert report.overall_status == OverallStatus.DEGRADED

    def test_overall_status_all_unhealthy(self) -> None:
        """Test overall status when all servers are unhealthy."""
        report = HealthReport()
        report.add_server(
            ServerHealth(
                name="github",
                token_result=ValidationResult(status=TokenStatus.INVALID, message="Bad"),
            )
        )
        report.add_server(
            ServerHealth(
                name="slack",
                token_result=ValidationResult(status=TokenStatus.INVALID, message="Bad"),
            )
        )
        assert report.overall_status == OverallStatus.UNHEALTHY

    def test_counts(self) -> None:
        """Test healthy_count and total_count."""
        report = HealthReport()
        report.add_server(
            ServerHealth(
                name="github",
                token_result=ValidationResult(status=TokenStatus.VALID, message="OK"),
            )
        )
        report.add_server(
            ServerHealth(
                name="slack",
                token_result=ValidationResult(status=TokenStatus.INVALID, message="Bad"),
            )
        )
        assert report.healthy_count == 1
        assert report.total_count == 2


class TestReportGenerator:
    """Tests for ReportGenerator."""

    @pytest.fixture
    def generator(self) -> ReportGenerator:
        """Create a generator with captured console."""
        console = Console(file=StringIO(), force_terminal=True)
        return ReportGenerator(console=console)

    @pytest.fixture
    def sample_report(self) -> HealthReport:
        """Create a sample report."""
        report = HealthReport()
        report.add_server(
            ServerHealth(
                name="github",
                token_result=ValidationResult(
                    status=TokenStatus.VALID,
                    message="Token valid",
                    user_info={"login": "testuser"},
                ),
                connection_result=ConnectionResult(
                    status=ConnectionStatus.HEALTHY,
                    message="OK",
                    resources=[{"name": "test"}],
                ),
            )
        )
        report.add_server(
            ServerHealth(
                name="slack",
                token_result=ValidationResult(
                    status=TokenStatus.INVALID,
                    message="Invalid token",
                ),
                action_required="Regenerate token",
            )
        )
        return report

    def test_generate_json(self, generator: ReportGenerator, sample_report: HealthReport) -> None:
        """Test JSON output generation."""
        output = generator.generate_json(sample_report)
        data = json.loads(output)

        assert "servers" in data
        assert "github" in data["servers"]
        assert "slack" in data["servers"]
        assert data["overall_status"] == "degraded"

    def test_generate_json_server_details(
        self, generator: ReportGenerator, sample_report: HealthReport
    ) -> None:
        """Test JSON output includes server details."""
        output = generator.generate_json(sample_report)
        data = json.loads(output)

        github = data["servers"]["github"]
        assert github["token"]["status"] == "valid"
        assert github["connection"]["status"] == "healthy"
        assert github["is_healthy"] is True

        slack = data["servers"]["slack"]
        assert slack["token"]["status"] == "invalid"
        assert slack["action_required"] == "Regenerate token"

    def test_generate_console(
        self, generator: ReportGenerator, sample_report: HealthReport
    ) -> None:
        """Test console output generation doesn't raise."""
        # Just verify it doesn't crash
        generator.generate_console(sample_report)

    def test_generate_console_verbose(
        self, generator: ReportGenerator, sample_report: HealthReport
    ) -> None:
        """Test verbose console output."""
        generator.generate_console(sample_report, verbose=True)


class TestCLIHelpers:
    """Tests for CLI helper functions."""

    def test_get_validator_for_github(self) -> None:
        """Test getting GitHub validator."""
        from mcp_health.validators.github import GitHubValidator

        validator = get_validator_for_server("github")
        assert isinstance(validator, GitHubValidator)

    def test_get_validator_for_slack(self) -> None:
        """Test getting Slack validator."""
        from mcp_health.validators.slack import SlackValidator

        validator = get_validator_for_server("slack")
        assert isinstance(validator, SlackValidator)

    def test_get_validator_for_atlassian(self) -> None:
        """Test getting Atlassian validator."""
        from mcp_health.validators.atlassian import AtlassianValidator

        validator = get_validator_for_server("perimeter81-atlassian")
        assert isinstance(validator, AtlassianValidator)

    def test_get_validator_unknown(self) -> None:
        """Test getting validator for unknown server."""
        validator = get_validator_for_server("unknown-server")
        assert validator is None

    def test_get_service_type_github(self) -> None:
        """Test getting service type for GitHub."""
        assert get_service_type("github") == ServiceType.GITHUB

    def test_get_service_type_slack(self) -> None:
        """Test getting service type for Slack."""
        assert get_service_type("slack") == ServiceType.SLACK

    def test_get_service_type_atlassian(self) -> None:
        """Test getting service type for Atlassian variants."""
        assert get_service_type("perimeter81-atlassian") == ServiceType.ATLASSIAN
        assert get_service_type("jira-server") == ServiceType.ATLASSIAN

    def test_get_service_type_unknown(self) -> None:
        """Test getting service type for unknown."""
        assert get_service_type("mystery-server") == ServiceType.UNKNOWN


class TestCLICommands:
    """Tests for CLI commands."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create CLI test runner."""
        return CliRunner()

    def test_main_help(self, runner: CliRunner) -> None:
        """Test main --help."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "MCP Health Check" in result.output

    def test_check_help(self, runner: CliRunner) -> None:
        """Test check --help."""
        result = runner.invoke(main, ["check", "--help"])
        assert result.exit_code == 0
        assert "--config" in result.output

    def test_list_servers_help(self, runner: CliRunner) -> None:
        """Test list-servers --help."""
        result = runner.invoke(main, ["list-servers", "--help"])
        assert result.exit_code == 0

    def test_refresh_help(self, runner: CliRunner) -> None:
        """Test refresh --help."""
        result = runner.invoke(main, ["refresh", "--help"])
        assert result.exit_code == 0

    def test_check_missing_config(self, runner: CliRunner) -> None:
        """Test check with missing config file."""
        result = runner.invoke(main, ["check", "--config", "/nonexistent/config.json"])
        assert result.exit_code != 0

    def test_list_servers_with_config(self, runner: CliRunner, temp_config_file: Path) -> None:
        """Test list-servers with valid config."""
        result = runner.invoke(main, ["list-servers", "--config", str(temp_config_file)])
        assert result.exit_code == 0
        assert "github" in result.output

    @pytest.mark.asyncio
    async def test_run_health_check_all_healthy(
        self, temp_config_file: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test health check with all healthy servers."""
        # Mock validators to return healthy
        mock_validate = AsyncMock(
            return_value=ValidationResult(status=TokenStatus.VALID, message="OK")
        )
        monkeypatch.setattr("mcp_health.validators.github.GitHubValidator.validate", mock_validate)
        monkeypatch.setattr("mcp_health.validators.slack.SlackValidator.validate", mock_validate)
        monkeypatch.setattr(
            "mcp_health.validators.atlassian.AtlassianValidator.validate", mock_validate
        )

        # Run with skip-mcp to avoid spawning processes
        await run_health_check(
            config_path=temp_config_file,
            output_format="console",
            verbose=False,
            skip_mcp=True,
            auto_refresh=False,
        )


class TestReportFormatting:
    """Tests for report formatting edge cases."""

    def test_format_token_status_all_types(self) -> None:
        """Test formatting all token status types."""
        generator = ReportGenerator()

        for status in TokenStatus:
            result = ValidationResult(status=status, message="test")
            formatted = generator._format_token_status(result)
            assert formatted is not None

    def test_format_connection_status_all_types(self) -> None:
        """Test formatting all connection status types."""
        generator = ReportGenerator()

        for status in ConnectionStatus:
            result = ConnectionResult(status=status, message="test")
            formatted = generator._format_connection_status(result)
            assert formatted is not None

    def test_format_none_results(self) -> None:
        """Test formatting None results."""
        generator = ReportGenerator()

        token_text = generator._format_token_status(None)
        assert "Not checked" in str(token_text)

        conn_text = generator._format_connection_status(None)
        assert "Not tested" in str(conn_text)

    def test_server_health_to_dict_with_refresh(self) -> None:
        """Test server health dict with refresh info."""
        generator = ReportGenerator()
        health = ServerHealth(
            name="test",
            token_result=ValidationResult(
                status=TokenStatus.VALID,
                message="OK",
                expires_at=datetime.now(timezone.utc),
            ),
            refresh_attempted=True,
            refresh_success=True,
        )

        result = generator._server_health_to_dict(health)
        assert result["refresh_attempted"] is True
        assert result["refresh_success"] is True
        assert "expires_at" in result["token"]
