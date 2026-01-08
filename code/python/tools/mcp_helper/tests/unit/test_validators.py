"""Unit tests for token validators."""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
import respx

from mcp_health.config.models import MCPServerConfig
from mcp_health.validators.atlassian import AtlassianValidator
from mcp_health.validators.base import TokenStatus, ValidationResult
from mcp_health.validators.github import GitHubValidator
from mcp_health.validators.slack import SlackValidator


class TestTokenStatus:
    """Tests for TokenStatus enum."""

    def test_is_healthy_valid(self) -> None:
        """Test that VALID status is healthy."""
        assert TokenStatus.VALID.is_healthy() is True

    def test_is_healthy_invalid(self) -> None:
        """Test that INVALID status is not healthy."""
        assert TokenStatus.INVALID.is_healthy() is False

    def test_needs_refresh_invalid(self) -> None:
        """Test that INVALID needs refresh."""
        assert TokenStatus.INVALID.needs_refresh() is True

    def test_needs_refresh_expired(self) -> None:
        """Test that EXPIRED needs refresh."""
        assert TokenStatus.EXPIRED.needs_refresh() is True

    def test_needs_refresh_valid(self) -> None:
        """Test that VALID doesn't need refresh."""
        assert TokenStatus.VALID.needs_refresh() is False


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_is_healthy(self) -> None:
        """Test is_healthy method."""
        result = ValidationResult(status=TokenStatus.VALID, message="OK")
        assert result.is_healthy() is True

    def test_needs_refresh(self) -> None:
        """Test needs_refresh method."""
        result = ValidationResult(status=TokenStatus.EXPIRED, message="Expired")
        assert result.needs_refresh() is True

    def test_default_values(self) -> None:
        """Test default field values."""
        result = ValidationResult(status=TokenStatus.VALID, message="OK")
        assert result.expires_at is None
        assert result.can_refresh is False
        assert result.refresh_instructions is None
        assert result.user_info == {}
        assert result.scopes == []


class TestGitHubValidator:
    """Tests for GitHubValidator."""

    @pytest.fixture
    def validator(self) -> GitHubValidator:
        """Create a validator instance."""
        return GitHubValidator()

    @pytest.fixture
    def github_config(self) -> MCPServerConfig:
        """Create a config with GitHub token."""
        return MCPServerConfig(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={"GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_testtoken123"},
        )

    @pytest.fixture
    def github_config_no_token(self) -> MCPServerConfig:
        """Create a config without GitHub token."""
        return MCPServerConfig(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={},
        )

    @pytest.mark.asyncio
    @respx.mock
    async def test_valid_token(
        self, validator: GitHubValidator, github_config: MCPServerConfig
    ) -> None:
        """Test validation of a valid token."""
        respx.get("https://api.github.com/user").mock(
            return_value=httpx.Response(
                200,
                json={"login": "testuser", "name": "Test User", "email": "test@example.com"},
                headers={"X-OAuth-Scopes": "repo, read:user"},
            )
        )

        result = await validator.validate(github_config)

        assert result.status == TokenStatus.VALID
        assert "testuser" in result.message
        assert result.user_info["login"] == "testuser"
        assert "repo" in result.scopes

    @pytest.mark.asyncio
    @respx.mock
    async def test_invalid_token(
        self, validator: GitHubValidator, github_config: MCPServerConfig
    ) -> None:
        """Test validation of an invalid token."""
        respx.get("https://api.github.com/user").mock(
            return_value=httpx.Response(401, json={"message": "Bad credentials"})
        )

        result = await validator.validate(github_config)

        assert result.status == TokenStatus.INVALID
        assert "invalid" in result.message.lower()
        assert result.refresh_instructions is not None

    @pytest.mark.asyncio
    @respx.mock
    async def test_expired_token(
        self, validator: GitHubValidator, github_config: MCPServerConfig
    ) -> None:
        """Test validation of an expired token."""
        respx.get("https://api.github.com/user").mock(
            return_value=httpx.Response(401, json={"message": "Token has expired"})
        )

        result = await validator.validate(github_config)

        assert result.status == TokenStatus.EXPIRED
        assert result.refresh_instructions is not None

    @pytest.mark.asyncio
    async def test_missing_token(
        self, validator: GitHubValidator, github_config_no_token: MCPServerConfig
    ) -> None:
        """Test validation when token is missing."""
        result = await validator.validate(github_config_no_token)

        assert result.status == TokenStatus.MISSING
        assert "GITHUB_PERSONAL_ACCESS_TOKEN" in result.message
        assert result.refresh_instructions is not None

    @pytest.mark.asyncio
    @respx.mock
    async def test_rate_limited(
        self, validator: GitHubValidator, github_config: MCPServerConfig
    ) -> None:
        """Test validation when rate limited."""
        respx.get("https://api.github.com/user").mock(
            return_value=httpx.Response(403, json={"message": "API rate limit exceeded"})
        )

        result = await validator.validate(github_config)

        assert result.status == TokenStatus.UNKNOWN
        assert "rate limit" in result.message.lower()

    @pytest.mark.asyncio
    @respx.mock
    async def test_network_timeout(
        self, validator: GitHubValidator, github_config: MCPServerConfig
    ) -> None:
        """Test handling of network timeout."""
        respx.get("https://api.github.com/user").mock(side_effect=httpx.TimeoutException("Timeout"))

        result = await validator.validate(github_config)

        assert result.status == TokenStatus.NETWORK_ERROR
        assert "timed out" in result.message.lower()

    @pytest.mark.asyncio
    @respx.mock
    async def test_network_error(
        self, validator: GitHubValidator, github_config: MCPServerConfig
    ) -> None:
        """Test handling of network error."""
        respx.get("https://api.github.com/user").mock(
            side_effect=httpx.RequestError("Connection failed")
        )

        result = await validator.validate(github_config)

        assert result.status == TokenStatus.NETWORK_ERROR
        assert "network error" in result.message.lower()

    @pytest.mark.asyncio
    @respx.mock
    async def test_forbidden_other(
        self, validator: GitHubValidator, github_config: MCPServerConfig
    ) -> None:
        """Test handling of 403 that's not rate limiting."""
        respx.get("https://api.github.com/user").mock(
            return_value=httpx.Response(403, json={"message": "Access denied"})
        )

        result = await validator.validate(github_config)

        assert result.status == TokenStatus.INVALID

    @pytest.mark.asyncio
    @respx.mock
    async def test_unexpected_status(
        self, validator: GitHubValidator, github_config: MCPServerConfig
    ) -> None:
        """Test handling of unexpected status code."""
        respx.get("https://api.github.com/user").mock(
            return_value=httpx.Response(500, json={"message": "Server error"})
        )

        result = await validator.validate(github_config)

        assert result.status == TokenStatus.UNKNOWN

    def test_service_name(self, validator: GitHubValidator) -> None:
        """Test service name attribute."""
        assert validator.service_name == "github"

    def test_get_token_env_var(self, validator: GitHubValidator) -> None:
        """Test token environment variable name."""
        assert validator.get_token_env_var() == "GITHUB_PERSONAL_ACCESS_TOKEN"


class TestSlackValidator:
    """Tests for SlackValidator."""

    @pytest.fixture
    def validator(self) -> SlackValidator:
        """Create a validator instance."""
        return SlackValidator()

    @pytest.fixture
    def slack_config(self) -> MCPServerConfig:
        """Create a config with Slack token."""
        return MCPServerConfig(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-slack"],
            env={"SLACK_BOT_TOKEN": "xoxb-test-token", "SLACK_TEAM_ID": "T123"},
        )

    @pytest.fixture
    def slack_config_no_token(self) -> MCPServerConfig:
        """Create a config without Slack token."""
        return MCPServerConfig(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-slack"],
            env={"SLACK_TEAM_ID": "T123"},
        )

    @pytest.fixture
    def slack_config_bad_format(self) -> MCPServerConfig:
        """Create a config with invalid token format."""
        return MCPServerConfig(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-slack"],
            env={"SLACK_BOT_TOKEN": "invalid-token-format"},
        )

    @pytest.mark.asyncio
    @respx.mock
    async def test_valid_token(
        self, validator: SlackValidator, slack_config: MCPServerConfig
    ) -> None:
        """Test validation of a valid token."""
        respx.post("https://slack.com/api/auth.test").mock(
            return_value=httpx.Response(
                200,
                json={
                    "ok": True,
                    "team": "Test Team",
                    "team_id": "T123",
                    "user": "bot",
                    "user_id": "U123",
                    "bot_id": "B123",
                },
            )
        )

        result = await validator.validate(slack_config)

        assert result.status == TokenStatus.VALID
        assert "Test Team" in result.message
        assert result.user_info["team"] == "Test Team"

    @pytest.mark.asyncio
    @respx.mock
    async def test_invalid_token(
        self, validator: SlackValidator, slack_config: MCPServerConfig
    ) -> None:
        """Test validation of an invalid token."""
        respx.post("https://slack.com/api/auth.test").mock(
            return_value=httpx.Response(200, json={"ok": False, "error": "invalid_auth"})
        )

        result = await validator.validate(slack_config)

        assert result.status == TokenStatus.INVALID
        assert result.refresh_instructions is not None

    @pytest.mark.asyncio
    @respx.mock
    async def test_revoked_token(
        self, validator: SlackValidator, slack_config: MCPServerConfig
    ) -> None:
        """Test validation of a revoked token."""
        respx.post("https://slack.com/api/auth.test").mock(
            return_value=httpx.Response(200, json={"ok": False, "error": "token_revoked"})
        )

        result = await validator.validate(slack_config)

        assert result.status == TokenStatus.INVALID
        assert "revoked" in result.message.lower()

    @pytest.mark.asyncio
    @respx.mock
    async def test_expired_token(
        self, validator: SlackValidator, slack_config: MCPServerConfig
    ) -> None:
        """Test validation of an expired token."""
        respx.post("https://slack.com/api/auth.test").mock(
            return_value=httpx.Response(200, json={"ok": False, "error": "token_expired"})
        )

        result = await validator.validate(slack_config)

        assert result.status == TokenStatus.EXPIRED

    @pytest.mark.asyncio
    async def test_missing_token(
        self, validator: SlackValidator, slack_config_no_token: MCPServerConfig
    ) -> None:
        """Test validation when token is missing."""
        result = await validator.validate(slack_config_no_token)

        assert result.status == TokenStatus.MISSING
        assert "SLACK_BOT_TOKEN" in result.message

    @pytest.mark.asyncio
    async def test_invalid_token_format(
        self, validator: SlackValidator, slack_config_bad_format: MCPServerConfig
    ) -> None:
        """Test validation with invalid token format."""
        result = await validator.validate(slack_config_bad_format)

        assert result.status == TokenStatus.INVALID
        assert "format" in result.message.lower()

    @pytest.mark.asyncio
    @respx.mock
    async def test_network_timeout(
        self, validator: SlackValidator, slack_config: MCPServerConfig
    ) -> None:
        """Test handling of network timeout."""
        respx.post("https://slack.com/api/auth.test").mock(
            side_effect=httpx.TimeoutException("Timeout")
        )

        result = await validator.validate(slack_config)

        assert result.status == TokenStatus.NETWORK_ERROR
        assert "timed out" in result.message.lower()

    @pytest.mark.asyncio
    @respx.mock
    async def test_network_error(
        self, validator: SlackValidator, slack_config: MCPServerConfig
    ) -> None:
        """Test handling of network error."""
        respx.post("https://slack.com/api/auth.test").mock(
            side_effect=httpx.RequestError("Connection failed")
        )

        result = await validator.validate(slack_config)

        assert result.status == TokenStatus.NETWORK_ERROR

    @pytest.mark.asyncio
    @respx.mock
    async def test_unknown_error(
        self, validator: SlackValidator, slack_config: MCPServerConfig
    ) -> None:
        """Test handling of unknown Slack error."""
        respx.post("https://slack.com/api/auth.test").mock(
            return_value=httpx.Response(200, json={"ok": False, "error": "some_new_error"})
        )

        result = await validator.validate(slack_config)

        assert result.status == TokenStatus.UNKNOWN

    def test_service_name(self, validator: SlackValidator) -> None:
        """Test service name attribute."""
        assert validator.service_name == "slack"

    def test_valid_token_formats(self, validator: SlackValidator) -> None:
        """Test _is_valid_token_format for various formats."""
        assert validator._is_valid_token_format("xoxb-12345") is True
        assert validator._is_valid_token_format("xoxp-12345") is True
        assert validator._is_valid_token_format("xapp-12345") is True
        assert validator._is_valid_token_format("invalid") is False


class TestAtlassianValidator:
    """Tests for AtlassianValidator."""

    @pytest.fixture
    def validator(self) -> AtlassianValidator:
        """Create a validator instance."""
        return AtlassianValidator()

    @pytest.fixture
    def atlassian_config(self, mock_atlassian_tokens: Path) -> MCPServerConfig:
        """Create a config with Atlassian token directory."""
        return MCPServerConfig(
            command="npx",
            args=["-y", "mcp-remote@0.1.30", "https://mcp.atlassian.com/v1/sse"],
            env={"MCP_REMOTE_CONFIG_DIR": str(mock_atlassian_tokens)},
        )

    @pytest.fixture
    def atlassian_config_no_dir(self) -> MCPServerConfig:
        """Create a config without token directory."""
        return MCPServerConfig(
            command="npx",
            args=["-y", "mcp-remote@0.1.30"],
            env={},
        )

    @pytest.fixture
    def atlassian_config_missing_file(self, tmp_path: Path) -> MCPServerConfig:
        """Create a config with empty token directory."""
        empty_dir = tmp_path / "empty-mcp-auth"
        empty_dir.mkdir()
        return MCPServerConfig(
            command="npx",
            args=["-y", "mcp-remote@0.1.30"],
            env={"MCP_REMOTE_CONFIG_DIR": str(empty_dir)},
        )

    @pytest.mark.asyncio
    @respx.mock
    async def test_valid_token(
        self, validator: AtlassianValidator, atlassian_config: MCPServerConfig
    ) -> None:
        """Test validation of a valid token."""
        respx.get("https://api.atlassian.com/me").mock(
            return_value=httpx.Response(
                200,
                json={
                    "account_id": "123456",
                    "email": "test@example.com",
                    "name": "Test User",
                },
            )
        )

        result = await validator.validate(atlassian_config)

        assert result.status == TokenStatus.VALID
        assert "test@example.com" in result.message
        assert result.can_refresh is True  # Has refresh_token

    @pytest.mark.asyncio
    @respx.mock
    async def test_expired_token_api(
        self, validator: AtlassianValidator, atlassian_config: MCPServerConfig
    ) -> None:
        """Test validation when API returns 401."""
        respx.get("https://api.atlassian.com/me").mock(
            return_value=httpx.Response(401, json={"message": "Unauthorized"})
        )

        result = await validator.validate(atlassian_config)

        assert result.status == TokenStatus.EXPIRED
        assert result.can_refresh is True

    @pytest.mark.asyncio
    async def test_missing_config_dir(
        self, validator: AtlassianValidator, atlassian_config_no_dir: MCPServerConfig
    ) -> None:
        """Test validation when config dir is missing."""
        result = await validator.validate(atlassian_config_no_dir)

        assert result.status == TokenStatus.MISSING
        assert "MCP_REMOTE_CONFIG_DIR" in result.message

    @pytest.mark.asyncio
    async def test_missing_token_file(
        self, validator: AtlassianValidator, atlassian_config_missing_file: MCPServerConfig
    ) -> None:
        """Test validation when token file is missing."""
        result = await validator.validate(atlassian_config_missing_file)

        assert result.status == TokenStatus.MISSING

    @pytest.mark.asyncio
    async def test_expired_token_from_file(
        self, validator: AtlassianValidator, mock_expired_atlassian_tokens: Path
    ) -> None:
        """Test validation when token is expired based on file data."""
        config = MCPServerConfig(
            command="npx",
            args=["-y", "mcp-remote@0.1.30"],
            env={"MCP_REMOTE_CONFIG_DIR": str(mock_expired_atlassian_tokens)},
        )

        result = await validator.validate(config)

        assert result.status == TokenStatus.EXPIRED
        assert result.can_refresh is True

    @pytest.mark.asyncio
    @respx.mock
    async def test_network_timeout(
        self, validator: AtlassianValidator, atlassian_config: MCPServerConfig
    ) -> None:
        """Test handling of network timeout."""
        respx.get("https://api.atlassian.com/me").mock(
            side_effect=httpx.TimeoutException("Timeout")
        )

        result = await validator.validate(atlassian_config)

        assert result.status == TokenStatus.NETWORK_ERROR

    @pytest.mark.asyncio
    @respx.mock
    async def test_network_error(
        self, validator: AtlassianValidator, atlassian_config: MCPServerConfig
    ) -> None:
        """Test handling of network error."""
        respx.get("https://api.atlassian.com/me").mock(
            side_effect=httpx.RequestError("Connection failed")
        )

        result = await validator.validate(atlassian_config)

        assert result.status == TokenStatus.NETWORK_ERROR

    @pytest.mark.asyncio
    @respx.mock
    async def test_unexpected_status(
        self, validator: AtlassianValidator, atlassian_config: MCPServerConfig
    ) -> None:
        """Test handling of unexpected status code."""
        respx.get("https://api.atlassian.com/me").mock(
            return_value=httpx.Response(500, json={"message": "Server error"})
        )

        result = await validator.validate(atlassian_config)

        assert result.status == TokenStatus.UNKNOWN

    def test_service_name(self, validator: AtlassianValidator) -> None:
        """Test service name attribute."""
        assert validator.service_name == "atlassian"

    def test_load_tokens_from_subdirectory(
        self, validator: AtlassianValidator, tmp_path: Path
    ) -> None:
        """Test loading tokens from subdirectory."""
        config_dir = tmp_path / "mcp-auth"
        config_dir.mkdir()
        subdir = config_dir / "server-hash"
        subdir.mkdir()
        (subdir / "tokens.json").write_text(json.dumps({"access_token": "test"}))

        tokens, token_path = validator._load_tokens(config_dir)
        assert tokens is not None
        assert tokens["access_token"] == "test"

    def test_parse_expiration_iso(self, validator: AtlassianValidator) -> None:
        """Test parsing ISO format expiration."""
        tokens = {"expires_at": "2024-01-15T10:30:00Z"}
        expires = validator._parse_expiration(tokens)
        assert expires is not None
        assert expires.year == 2024

    def test_parse_expiration_invalid(self, validator: AtlassianValidator) -> None:
        """Test parsing invalid expiration format."""
        tokens = {"expires_at": "not-a-date"}
        expires = validator._parse_expiration(tokens)
        assert expires is None

    @pytest.mark.asyncio
    async def test_missing_access_token(
        self, validator: AtlassianValidator, tmp_path: Path
    ) -> None:
        """Test when tokens file exists but has no access_token."""
        token_dir = tmp_path / "no-access"
        token_dir.mkdir()
        (token_dir / "tokens.json").write_text(json.dumps({"refresh_token": "refresh"}))

        config = MCPServerConfig(
            command="npx",
            args=[],
            env={"MCP_REMOTE_CONFIG_DIR": str(token_dir)},
        )

        result = await validator.validate(config)
        assert result.status == TokenStatus.MISSING
        assert result.can_refresh is True  # Has refresh_token
