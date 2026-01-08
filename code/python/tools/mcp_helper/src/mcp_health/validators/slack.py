"""Slack token validator."""

from __future__ import annotations

import logging
from typing import Any

import httpx
from tenacity import RetryError

from mcp_health.config.models import MCPServerConfig
from mcp_health.validators.base import (
    BaseValidator,
    TokenStatus,
    ValidationResult,
    with_retry,
)

logger = logging.getLogger(__name__)


class SlackValidator(BaseValidator):
    """Validates Slack Bot Tokens.

    Uses the Slack auth.test API to validate the bot token.
    Bot tokens cannot be auto-refreshed; users must regenerate them manually.
    """

    service_name = "slack"
    SLACK_API_URL = "https://slack.com/api"
    TOKEN_ENV_VAR = "SLACK_BOT_TOKEN"
    # Uses TIMEOUT_SECONDS from BaseValidator

    def get_token_env_var(self) -> str:
        """Get the environment variable name for Slack token."""
        return self.TOKEN_ENV_VAR

    async def validate(self, config: MCPServerConfig) -> ValidationResult:
        """Validate the Slack bot token.

        Args:
            config: The MCP server configuration

        Returns:
            ValidationResult with token status
        """
        logger.debug("Validating Slack token")
        token = self.extract_token(config)

        if not token:
            logger.info("Slack token missing")
            return self._create_error_result(
                TokenStatus.MISSING,
                f"Slack bot token not found in {self.TOKEN_ENV_VAR}",
            )

        # Validate token format
        if not self._is_valid_token_format(token):
            logger.info("Slack token has invalid format")
            return self._create_error_result(
                TokenStatus.INVALID,
                "Invalid Slack token format (expected xoxb-... for bot tokens)",
            )

        result = await self._validate_token(token)
        logger.info("Slack validation result: %s", result.status.value)
        return result

    def _is_valid_token_format(self, token: str) -> bool:
        """Check if the token has a valid Slack format.

        Args:
            token: The token to check

        Returns:
            True if format is valid
        """
        # Bot tokens start with xoxb-
        # User tokens start with xoxp-
        # App tokens start with xapp-
        valid_prefixes = ("xoxb-", "xoxp-", "xapp-")
        return token.startswith(valid_prefixes)

    async def _validate_token(self, token: str) -> ValidationResult:
        """Make API call to validate the token.

        Args:
            token: The Slack token to validate

        Returns:
            ValidationResult with validation details
        """
        try:
            response = await self._make_request(token)
            data: dict[str, Any] = response.json()

            if data.get("ok"):
                return self._handle_success(data)
            else:
                return self._handle_error(data)

        except RetryError as e:
            logger.warning("Slack API failed after retries: %s", e.last_attempt.exception())
            return ValidationResult(
                status=TokenStatus.NETWORK_ERROR,
                message=f"Network error after {self.RETRY_MAX_ATTEMPTS} attempts",
                can_refresh=False,
            )
        except httpx.TimeoutException:
            logger.warning("Slack API request timed out")
            return ValidationResult(
                status=TokenStatus.NETWORK_ERROR,
                message="Request timed out while validating Slack token",
                can_refresh=False,
            )
        except httpx.RequestError as e:
            logger.warning("Slack API network error: %s", e)
            return ValidationResult(
                status=TokenStatus.NETWORK_ERROR,
                message=f"Network error while validating Slack token: {e}",
                can_refresh=False,
            )

    @with_retry(max_attempts=3, min_wait=0.5, max_wait=5.0)
    async def _make_request(self, token: str) -> httpx.Response:
        """Make the API request with retry logic.

        Args:
            token: The Slack token

        Returns:
            HTTP response
        """
        async with httpx.AsyncClient(timeout=self.TIMEOUT_SECONDS) as client:
            return await client.post(
                f"{self.SLACK_API_URL}/auth.test",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
            )

    def _handle_success(self, data: dict[str, Any]) -> ValidationResult:
        """Handle successful validation response.

        Args:
            data: The successful API response data

        Returns:
            ValidationResult with user/team info
        """
        return ValidationResult(
            status=TokenStatus.VALID,
            message=f"Token valid for team: {data.get('team', 'unknown')}",
            can_refresh=False,
            user_info={
                "team": data.get("team", ""),
                "team_id": data.get("team_id", ""),
                "user": data.get("user", ""),
                "user_id": data.get("user_id", ""),
                "bot_id": data.get("bot_id", ""),
            },
        )

    def _handle_error(self, data: dict[str, Any]) -> ValidationResult:
        """Handle error response from Slack API.

        Args:
            data: The error response data

        Returns:
            ValidationResult with appropriate status
        """
        error = data.get("error", "unknown_error")

        # Map Slack error codes to our status
        error_mapping = {
            "invalid_auth": (TokenStatus.INVALID, "Invalid authentication token"),
            "not_authed": (TokenStatus.MISSING, "No authentication token provided"),
            "token_revoked": (TokenStatus.INVALID, "Token has been revoked"),
            "token_expired": (TokenStatus.EXPIRED, "Token has expired"),
            "account_inactive": (TokenStatus.INVALID, "Account is inactive"),
            "team_access_not_granted": (
                TokenStatus.INVALID,
                "Team access has not been granted",
            ),
        }

        status, message = error_mapping.get(
            error, (TokenStatus.UNKNOWN, f"Slack API error: {error}")
        )

        return ValidationResult(
            status=status,
            message=message,
            can_refresh=False,
            refresh_instructions=self._get_refresh_instructions()
            if status != TokenStatus.UNKNOWN
            else None,
        )

    def _get_refresh_instructions(self) -> str:
        """Get instructions for refreshing the Slack token."""
        return (
            "To regenerate your Slack Bot Token:\n"
            "1. Go to https://api.slack.com/apps\n"
            "2. Select your app\n"
            "3. Navigate to 'OAuth & Permissions'\n"
            "4. Click 'Reinstall to Workspace' or create new token\n"
            "5. Copy the 'Bot User OAuth Token' (xoxb-...)\n"
            "6. Update SLACK_BOT_TOKEN in your MCP config"
        )
