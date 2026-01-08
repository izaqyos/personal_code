"""Unit tests for token refresh and user notification."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import httpx
import pytest
import respx

from mcp_health.refresh.notifier import RefreshNotification, ServiceType, UserNotifier
from mcp_health.refresh.oauth import OAuthRefresher, RefreshResult, RefreshStatus


class TestRefreshStatus:
    """Tests for RefreshStatus enum."""

    def test_success_status(self) -> None:
        """Test SUCCESS status exists."""
        assert RefreshStatus.SUCCESS.value == "success"

    def test_failed_status(self) -> None:
        """Test FAILED status exists."""
        assert RefreshStatus.FAILED.value == "failed"


class TestRefreshResult:
    """Tests for RefreshResult dataclass."""

    def test_is_success_true(self) -> None:
        """Test is_success when status is SUCCESS."""
        result = RefreshResult(status=RefreshStatus.SUCCESS, message="OK")
        assert result.is_success() is True

    def test_is_success_false(self) -> None:
        """Test is_success when status is not SUCCESS."""
        result = RefreshResult(status=RefreshStatus.FAILED, message="Failed")
        assert result.is_success() is False

    def test_default_values(self) -> None:
        """Test default field values."""
        result = RefreshResult(status=RefreshStatus.SUCCESS, message="OK")
        assert result.new_access_token is None
        assert result.new_expires_at is None

    def test_with_token(self) -> None:
        """Test result with new token."""
        now = datetime.now(timezone.utc)
        result = RefreshResult(
            status=RefreshStatus.SUCCESS,
            message="Refreshed",
            new_access_token="new_token",
            new_expires_at=now,
        )
        assert result.new_access_token == "new_token"
        assert result.new_expires_at == now


class TestOAuthRefresher:
    """Tests for OAuthRefresher."""

    @pytest.fixture
    def refresher(self) -> OAuthRefresher:
        """Create a refresher instance."""
        return OAuthRefresher()

    @pytest.fixture
    def token_dir(self, tmp_path: Path) -> Path:
        """Create a token directory with valid tokens."""
        token_dir = tmp_path / ".mcp-auth"
        token_dir.mkdir()
        tokens = {
            "access_token": "old_access_token",
            "refresh_token": "valid_refresh_token",
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "expires_at": "2020-01-01T00:00:00Z",
        }
        (token_dir / "tokens.json").write_text(json.dumps(tokens))
        return token_dir

    @pytest.fixture
    def token_dir_no_refresh(self, tmp_path: Path) -> Path:
        """Create a token directory without refresh token."""
        token_dir = tmp_path / ".mcp-auth-no-refresh"
        token_dir.mkdir()
        tokens = {
            "access_token": "old_access_token",
            "expires_at": "2020-01-01T00:00:00Z",
        }
        (token_dir / "tokens.json").write_text(json.dumps(tokens))
        return token_dir

    @pytest.fixture
    def token_dir_subdir(self, tmp_path: Path) -> Path:
        """Create a token directory with tokens in subdirectory."""
        token_dir = tmp_path / ".mcp-auth-subdir"
        token_dir.mkdir()
        subdir = token_dir / "server-hash"
        subdir.mkdir()
        tokens = {
            "access_token": "old_access_token",
            "refresh_token": "valid_refresh_token",
        }
        (subdir / "tokens.json").write_text(json.dumps(tokens))
        return token_dir

    @pytest.mark.asyncio
    @respx.mock
    async def test_refresh_success(self, refresher: OAuthRefresher, token_dir: Path) -> None:
        """Test successful token refresh."""
        respx.post("https://auth.atlassian.com/oauth/token").mock(
            return_value=httpx.Response(
                200,
                json={
                    "access_token": "new_access_token",
                    "refresh_token": "new_refresh_token",
                    "expires_in": 3600,
                    "token_type": "Bearer",
                },
            )
        )

        result = await refresher.refresh_atlassian(token_dir)

        assert result.status == RefreshStatus.SUCCESS
        assert result.new_access_token == "new_access_token"
        assert result.new_expires_at is not None

        # Verify token file was updated
        token_path = token_dir / "tokens.json"
        updated_tokens = json.loads(token_path.read_text())
        assert updated_tokens["access_token"] == "new_access_token"
        assert updated_tokens["refresh_token"] == "new_refresh_token"

    @pytest.mark.asyncio
    async def test_refresh_no_token_file(self, refresher: OAuthRefresher, tmp_path: Path) -> None:
        """Test refresh when token file doesn't exist."""
        missing_dir = tmp_path / "missing"
        missing_dir.mkdir()

        result = await refresher.refresh_atlassian(missing_dir)

        assert result.status == RefreshStatus.NO_TOKEN

    @pytest.mark.asyncio
    async def test_refresh_no_refresh_token(
        self, refresher: OAuthRefresher, token_dir_no_refresh: Path
    ) -> None:
        """Test refresh when no refresh_token in file."""
        result = await refresher.refresh_atlassian(token_dir_no_refresh)

        assert result.status == RefreshStatus.NO_REFRESH_TOKEN

    @pytest.mark.asyncio
    @respx.mock
    async def test_refresh_api_error(self, refresher: OAuthRefresher, token_dir: Path) -> None:
        """Test refresh when API returns error."""
        respx.post("https://auth.atlassian.com/oauth/token").mock(
            return_value=httpx.Response(
                400,
                json={
                    "error": "invalid_grant",
                    "error_description": "Refresh token expired",
                },
            )
        )

        result = await refresher.refresh_atlassian(token_dir)

        assert result.status == RefreshStatus.FAILED
        assert "invalid_grant" in result.message

    @pytest.mark.asyncio
    @respx.mock
    async def test_refresh_network_timeout(
        self, refresher: OAuthRefresher, token_dir: Path
    ) -> None:
        """Test refresh with network timeout."""
        respx.post("https://auth.atlassian.com/oauth/token").mock(
            side_effect=httpx.TimeoutException("Timeout")
        )

        result = await refresher.refresh_atlassian(token_dir)

        assert result.status == RefreshStatus.NETWORK_ERROR
        assert "timeout" in result.message.lower()

    @pytest.mark.asyncio
    @respx.mock
    async def test_refresh_network_error(self, refresher: OAuthRefresher, token_dir: Path) -> None:
        """Test refresh with network error."""
        respx.post("https://auth.atlassian.com/oauth/token").mock(
            side_effect=httpx.RequestError("Connection failed")
        )

        result = await refresher.refresh_atlassian(token_dir)

        assert result.status == RefreshStatus.NETWORK_ERROR

    @pytest.mark.asyncio
    @respx.mock
    async def test_refresh_tokens_in_subdirectory(
        self, refresher: OAuthRefresher, token_dir_subdir: Path
    ) -> None:
        """Test refresh with tokens in subdirectory."""
        respx.post("https://auth.atlassian.com/oauth/token").mock(
            return_value=httpx.Response(
                200,
                json={
                    "access_token": "new_token",
                    "expires_in": 3600,
                },
            )
        )

        result = await refresher.refresh_atlassian(token_dir_subdir)

        assert result.status == RefreshStatus.SUCCESS

    @pytest.mark.asyncio
    async def test_refresh_nonexistent_directory(
        self, refresher: OAuthRefresher, tmp_path: Path
    ) -> None:
        """Test refresh with non-existent directory."""
        result = await refresher.refresh_atlassian(tmp_path / "nonexistent")

        assert result.status == RefreshStatus.NO_TOKEN

    @pytest.mark.asyncio
    @respx.mock
    async def test_refresh_api_error_no_json(
        self, refresher: OAuthRefresher, token_dir: Path
    ) -> None:
        """Test refresh when API returns non-JSON error."""
        respx.post("https://auth.atlassian.com/oauth/token").mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )

        result = await refresher.refresh_atlassian(token_dir)

        assert result.status == RefreshStatus.FAILED
        assert "500" in result.message

    def test_load_tokens_invalid_json(self, refresher: OAuthRefresher, tmp_path: Path) -> None:
        """Test loading tokens with invalid JSON."""
        token_dir = tmp_path / "invalid"
        token_dir.mkdir()
        (token_dir / "tokens.json").write_text("not valid json")

        tokens, path = refresher._load_tokens(token_dir)
        assert tokens is None


class TestServiceType:
    """Tests for ServiceType enum."""

    def test_github_type(self) -> None:
        """Test GITHUB service type."""
        assert ServiceType.GITHUB.value == "github"

    def test_slack_type(self) -> None:
        """Test SLACK service type."""
        assert ServiceType.SLACK.value == "slack"

    def test_atlassian_type(self) -> None:
        """Test ATLASSIAN service type."""
        assert ServiceType.ATLASSIAN.value == "atlassian"


class TestRefreshNotification:
    """Tests for RefreshNotification dataclass."""

    def test_format_console(self) -> None:
        """Test console formatting."""
        notification = RefreshNotification(
            service=ServiceType.GITHUB,
            title="Test Title",
            message="Test message",
            url="https://example.com",
            steps=["Step 1", "Step 2"],
        )

        output = notification.format_console()

        assert "Test Title" in output
        assert "Test message" in output
        assert "https://example.com" in output
        assert "Step 1" in output
        assert "Step 2" in output


class TestUserNotifier:
    """Tests for UserNotifier."""

    @pytest.fixture
    def notifier(self) -> UserNotifier:
        """Create a notifier instance."""
        return UserNotifier()

    def test_notify_github(self, notifier: UserNotifier) -> None:
        """Test GitHub notification generation."""
        notification = notifier.notify(ServiceType.GITHUB)

        assert notification.service == ServiceType.GITHUB
        assert "GitHub" in notification.title
        assert "github.com" in notification.url
        assert len(notification.steps) > 0

    def test_notify_slack(self, notifier: UserNotifier) -> None:
        """Test Slack notification generation."""
        notification = notifier.notify(ServiceType.SLACK)

        assert notification.service == ServiceType.SLACK
        assert "Slack" in notification.title
        assert "slack.com" in notification.url
        assert len(notification.steps) > 0

    def test_notify_atlassian(self, notifier: UserNotifier) -> None:
        """Test Atlassian notification generation."""
        notification = notifier.notify(ServiceType.ATLASSIAN)

        assert notification.service == ServiceType.ATLASSIAN
        assert "Atlassian" in notification.title
        assert len(notification.steps) > 0

    def test_notify_unknown(self, notifier: UserNotifier) -> None:
        """Test unknown service notification."""
        notification = notifier.notify(ServiceType.UNKNOWN)

        assert notification.service == ServiceType.UNKNOWN
        assert "documentation" in notification.message.lower()

    def test_notify_github_method(self, notifier: UserNotifier) -> None:
        """Test notify_github direct method."""
        notification = notifier.notify_github()

        assert notification.service == ServiceType.GITHUB
        assert "PAT" in notification.message or "Personal Access Token" in notification.message

    def test_notify_slack_method(self, notifier: UserNotifier) -> None:
        """Test notify_slack direct method."""
        notification = notifier.notify_slack()

        assert notification.service == ServiceType.SLACK
        assert "Bot Token" in notification.message or "bot" in notification.message.lower()

    def test_notify_atlassian_method(self, notifier: UserNotifier) -> None:
        """Test notify_atlassian direct method."""
        notification = notifier.notify_atlassian()

        assert notification.service == ServiceType.ATLASSIAN
        assert "OAuth" in notification.message

    def test_get_instructions(self, notifier: UserNotifier) -> None:
        """Test get_instructions convenience method."""
        instructions = notifier.get_instructions(ServiceType.GITHUB)

        assert isinstance(instructions, str)
        assert "GitHub" in instructions
        assert "Step" in instructions or "1." in instructions
