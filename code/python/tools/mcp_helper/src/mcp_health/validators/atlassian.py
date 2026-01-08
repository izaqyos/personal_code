"""Atlassian OAuth token validator."""

from __future__ import annotations

import json
import logging
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
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


class AtlassianValidator(BaseValidator):
    """Validates Atlassian OAuth tokens.

    Uses mcp-remote's stored OAuth tokens from MCP_REMOTE_CONFIG_DIR.
    OAuth tokens can be auto-refreshed using the refresh_token.
    """

    service_name = "atlassian"
    ATLASSIAN_API_URL = "https://api.atlassian.com"
    CONFIG_DIR_ENV_VAR = "MCP_REMOTE_CONFIG_DIR"
    TOKEN_FILE_NAME = "tokens.json"
    # Uses TIMEOUT_SECONDS from BaseValidator

    # Note: mcp-remote OAuth tokens are scoped for MCP access only
    # They may not work with standard Atlassian REST APIs like /me
    # We validate by checking token file freshness and structure

    def get_token_env_var(self) -> str:
        """Get the environment variable name for the config directory."""
        return self.CONFIG_DIR_ENV_VAR

    async def validate(self, config: MCPServerConfig) -> ValidationResult:
        """Validate the Atlassian OAuth token.

        Args:
            config: The MCP server configuration

        Returns:
            ValidationResult with token status
        """
        logger.debug("Validating Atlassian token")
        config_dir = config.get_env_var(self.CONFIG_DIR_ENV_VAR)

        if not config_dir:
            logger.info("Atlassian config dir missing")
            return self._create_error_result(
                TokenStatus.MISSING,
                f"Atlassian config dir not found in {self.CONFIG_DIR_ENV_VAR}",
            )

        tokens, token_path = self._load_tokens(Path(config_dir))
        if tokens is None:
            logger.info("Atlassian token file not found in %s", config_dir)
            return self._create_error_result(
                TokenStatus.MISSING,
                f"Token file not found in {config_dir}",
            )

        access_token = tokens.get("access_token")
        has_refresh = bool(tokens.get("refresh_token"))

        if not access_token:
            logger.info("access_token not found in tokens file")
            return ValidationResult(
                status=TokenStatus.MISSING,
                message="access_token not found in tokens file",
                can_refresh=has_refresh,
                refresh_instructions=self._get_refresh_instructions(),
            )

        # Check expiration from stored data
        expires_at = self._parse_expiration(tokens)
        now = datetime.now(timezone.utc)
        # Make expires_at timezone-aware if it isn't
        if expires_at:
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            if expires_at < now:
                logger.info("Atlassian token expired at %s", expires_at)
                return ValidationResult(
                    status=TokenStatus.EXPIRED,
                    message="Atlassian OAuth token has expired",
                    expires_at=expires_at,
                    can_refresh=has_refresh,
                    refresh_instructions=self._get_refresh_instructions()
                    if not has_refresh
                    else None,
                )

        result = await self._validate_token(access_token, tokens)

        # Check for expiration warning
        if result.status == TokenStatus.VALID and expires_at:
            is_expiring, warning = self._check_expiration_warning(expires_at)
            if is_expiring:
                logger.info("Atlassian token expiring soon: %s", warning)
                return ValidationResult(
                    status=TokenStatus.EXPIRING_SOON,
                    message=result.message,
                    expires_at=expires_at,
                    can_refresh=has_refresh,
                    user_info=result.user_info,
                    warning=warning,
                )

        logger.info("Atlassian validation result: %s", result.status.value)
        return result

    def _load_tokens(self, config_dir: Path) -> tuple[dict[str, Any] | None, Path | None]:
        """Load tokens from the mcp-remote config directory.

        Args:
            config_dir: Path to the MCP_REMOTE_CONFIG_DIR

        Returns:
            Token dictionary or None if not found
        """
        if not config_dir.exists():
            return None, None

        # mcp-remote stores tokens with hash prefixes: <hash>_tokens.json
        # Try multiple patterns to find the tokens file

        # Pattern 1: Direct tokens.json in root
        token_path = config_dir / self.TOKEN_FILE_NAME
        if token_path.exists():
            try:
                tokens: dict[str, Any] = json.loads(token_path.read_text())
                return tokens, token_path
            except (json.JSONDecodeError, OSError):
                pass

        # Pattern 2: Hash-prefixed tokens in root (*_tokens.json)
        for token_file in config_dir.glob(f"*_{self.TOKEN_FILE_NAME}"):
            try:
                tokens = json.loads(token_file.read_text())
                return tokens, token_file
            except (json.JSONDecodeError, OSError):
                continue

        # Pattern 3: Search subdirectories for tokens.json or *_tokens.json
        for subdir in config_dir.iterdir():
            if subdir.is_dir():
                # Try direct tokens.json
                token_path = subdir / self.TOKEN_FILE_NAME
                if token_path.exists():
                    try:
                        tokens = json.loads(token_path.read_text())
                        return tokens, token_path
                    except (json.JSONDecodeError, OSError):
                        pass

                # Try hash-prefixed tokens
                for token_file in subdir.glob(f"*_{self.TOKEN_FILE_NAME}"):
                    try:
                        tokens = json.loads(token_file.read_text())
                        return tokens, token_file
                    except (json.JSONDecodeError, OSError):
                        continue

        return None, None

    def _parse_expiration(self, tokens: dict[str, Any]) -> datetime | None:
        """Parse token expiration time.

        Args:
            tokens: Token dictionary

        Returns:
            Expiration datetime or None
        """
        expires_at = tokens.get("expires_at")
        if isinstance(expires_at, str):
            try:
                # Try ISO format
                return datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            except ValueError:
                pass

        # Try expires_in (seconds from token issuance)
        expires_in = tokens.get("expires_in")
        issued_at = tokens.get("issued_at")
        if expires_in and issued_at:
            try:
                issued = datetime.fromisoformat(issued_at.replace("Z", "+00:00"))
                return issued + timedelta(seconds=int(expires_in))
            except (ValueError, TypeError):
                pass

        return None

    def _is_mcp_remote_running(self) -> bool:
        """Check if mcp-remote process is running for Atlassian.

        Returns:
            True if mcp-remote process for Atlassian is running
        """
        try:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return "mcp-remote" in result.stdout and "atlassian" in result.stdout
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            return False

    async def _validate_token(self, access_token: str, tokens: dict[str, Any]) -> ValidationResult:
        """Make API call to validate the token.

        Args:
            access_token: The Atlassian access token
            tokens: Full tokens dict (for refresh token check)

        Returns:
            ValidationResult with validation details
        """
        has_refresh = bool(tokens.get("refresh_token"))

        try:
            response = await self._make_request(access_token)

            if response.status_code == 200:
                return self._handle_success(response, tokens)
            elif response.status_code == 401:
                # API validation failed - check if mcp-remote is running
                # mcp-remote tokens are scoped for MCP only, not REST API
                if self._is_mcp_remote_running():
                    logger.info("API validation failed but mcp-remote is running - tokens may be MCP-scoped")
                    return ValidationResult(
                        status=TokenStatus.VALID,
                        message="Token valid (mcp-remote running, MCP-scoped token)",
                        can_refresh=has_refresh,
                        warning="Unable to validate via REST API - token appears MCP-scoped only",
                    )
                return self._handle_unauthorized(tokens)
            else:
                return ValidationResult(
                    status=TokenStatus.UNKNOWN,
                    message=f"Unexpected response: {response.status_code}",
                    can_refresh=has_refresh,
                )

        except RetryError as e:
            logger.warning("Atlassian API failed after retries: %s", e.last_attempt.exception())
            # Check if mcp-remote is running as fallback
            if self._is_mcp_remote_running():
                return ValidationResult(
                    status=TokenStatus.VALID,
                    message="Token valid (mcp-remote running)",
                    can_refresh=has_refresh,
                    warning="Unable to validate via REST API - relying on mcp-remote process",
                )
            return ValidationResult(
                status=TokenStatus.NETWORK_ERROR,
                message=f"Network error after {self.RETRY_MAX_ATTEMPTS} attempts",
                can_refresh=has_refresh,
            )
        except httpx.TimeoutException:
            logger.warning("Atlassian API request timed out")
            # Check if mcp-remote is running as fallback
            if self._is_mcp_remote_running():
                return ValidationResult(
                    status=TokenStatus.VALID,
                    message="Token valid (mcp-remote running)",
                    can_refresh=has_refresh,
                    warning="Unable to validate via REST API - relying on mcp-remote process",
                )
            return ValidationResult(
                status=TokenStatus.NETWORK_ERROR,
                message="Request timed out while validating Atlassian token",
                can_refresh=has_refresh,
            )
        except httpx.RequestError as e:
            logger.warning("Atlassian API network error: %s", e)
            # Check if mcp-remote is running as fallback
            if self._is_mcp_remote_running():
                return ValidationResult(
                    status=TokenStatus.VALID,
                    message="Token valid (mcp-remote running)",
                    can_refresh=has_refresh,
                    warning="Unable to validate via REST API - relying on mcp-remote process",
                )
            return ValidationResult(
                status=TokenStatus.NETWORK_ERROR,
                message=f"Network error while validating Atlassian token: {e}",
                can_refresh=has_refresh,
            )

    @with_retry(max_attempts=3, min_wait=0.5, max_wait=5.0)
    async def _make_request(self, access_token: str) -> httpx.Response:
        """Make the API request with retry logic.

        Args:
            access_token: The Atlassian access token

        Returns:
            HTTP response
        """
        async with httpx.AsyncClient(timeout=self.TIMEOUT_SECONDS) as client:
            return await client.get(
                f"{self.ATLASSIAN_API_URL}/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )

    def _handle_success(self, response: httpx.Response, tokens: dict[str, Any]) -> ValidationResult:
        """Handle successful validation response.

        Args:
            response: The successful API response
            tokens: Token dict for refresh capability check

        Returns:
            ValidationResult with user info
        """
        data = response.json()
        expires_at = self._parse_expiration(tokens)

        return ValidationResult(
            status=TokenStatus.VALID,
            message=f"Token valid for: {data.get('email', 'unknown')}",
            expires_at=expires_at,
            can_refresh=bool(tokens.get("refresh_token")),
            user_info={
                "account_id": data.get("account_id", ""),
                "email": data.get("email", ""),
                "name": data.get("name", ""),
            },
        )

    def _handle_unauthorized(self, tokens: dict[str, Any]) -> ValidationResult:
        """Handle 401 unauthorized response.

        Args:
            tokens: Token dict for refresh capability check

        Returns:
            ValidationResult with expired status
        """
        has_refresh = bool(tokens.get("refresh_token"))

        return ValidationResult(
            status=TokenStatus.EXPIRED,
            message="Atlassian OAuth token has expired or been revoked",
            can_refresh=has_refresh,
            refresh_instructions=self._get_refresh_instructions() if not has_refresh else None,
        )

    def _get_refresh_instructions(self) -> str:
        """Get instructions for refreshing the Atlassian token."""
        return (
            "To re-authenticate with Atlassian:\n"
            "Option 1 (Recommended - via Cursor):\n"
            "  1. Open Cursor Settings → MCP Servers\n"
            "  2. Toggle OFF the Atlassian MCP server\n"
            "  3. Toggle it back ON\n"
            "  4. Complete OAuth in browser when prompted\n"
            "\n"
            "Option 2 (Manual):\n"
            "  1. Run: mcp-health check --server perimeter81-atlassian --reauth\n"
            "  2. Complete OAuth in browser when prompted\n"
            "\n"
            "Option 3 (Advanced):\n"
            "  1. Remove token files from MCP_REMOTE_CONFIG_DIR\n"
            "  2. Restart Cursor to trigger OAuth flow\n"
            "\n"
            "Note: mcp-remote tokens are MCP-scoped and may not work with REST APIs"
        )
