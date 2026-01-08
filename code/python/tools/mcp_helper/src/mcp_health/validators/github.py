"""GitHub token validator."""

from __future__ import annotations

import logging

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


class GitHubValidator(BaseValidator):
    """Validates GitHub Personal Access Tokens (PATs).

    Uses the GitHub API /user endpoint to validate the token.
    PATs cannot be auto-refreshed; users must regenerate them manually.
    """

    service_name = "github"
    GITHUB_API_URL = "https://api.github.com"
    TOKEN_ENV_VAR = "GITHUB_PERSONAL_ACCESS_TOKEN"
    # Uses TIMEOUT_SECONDS from BaseValidator

    def get_token_env_var(self) -> str:
        """Get the environment variable name for GitHub token."""
        return self.TOKEN_ENV_VAR

    async def validate(self, config: MCPServerConfig) -> ValidationResult:
        """Validate the GitHub PAT.

        Args:
            config: The MCP server configuration

        Returns:
            ValidationResult with token status
        """
        logger.debug("Validating GitHub token")
        token = self.extract_token(config)

        if not token:
            logger.info("GitHub token missing")
            return self._create_error_result(
                TokenStatus.MISSING,
                f"GitHub token not found in {self.TOKEN_ENV_VAR}",
            )

        result = await self._validate_token(token)
        logger.info("GitHub validation result: %s", result.status.value)
        return result

    async def _validate_token(self, token: str) -> ValidationResult:
        """Make API call to validate the token.

        Args:
            token: The GitHub PAT to validate

        Returns:
            ValidationResult with validation details
        """
        try:
            response = await self._make_request(token)

            if response.status_code == 200:
                return self._handle_success(response)
            elif response.status_code == 401:
                return self._handle_unauthorized(response)
            elif response.status_code == 403:
                return self._handle_forbidden(response)
            else:
                return ValidationResult(
                    status=TokenStatus.UNKNOWN,
                    message=f"Unexpected response: {response.status_code}",
                    can_refresh=False,
                )

        except RetryError as e:
            # All retries exhausted
            logger.warning("GitHub API failed after retries: %s", e.last_attempt.exception())
            return ValidationResult(
                status=TokenStatus.NETWORK_ERROR,
                message=f"Network error after {self.RETRY_MAX_ATTEMPTS} attempts",
                can_refresh=False,
            )
        except httpx.TimeoutException:
            logger.warning("GitHub API request timed out")
            return ValidationResult(
                status=TokenStatus.NETWORK_ERROR,
                message="Request timed out while validating GitHub token",
                can_refresh=False,
            )
        except httpx.RequestError as e:
            logger.warning("GitHub API network error: %s", e)
            return ValidationResult(
                status=TokenStatus.NETWORK_ERROR,
                message=f"Network error while validating GitHub token: {e}",
                can_refresh=False,
            )

    @with_retry(max_attempts=3, min_wait=0.5, max_wait=5.0)
    async def _make_request(self, token: str) -> httpx.Response:
        """Make the API request with retry logic.

        Args:
            token: The GitHub PAT

        Returns:
            HTTP response
        """
        async with httpx.AsyncClient(timeout=self.TIMEOUT_SECONDS) as client:
            return await client.get(
                f"{self.GITHUB_API_URL}/user",
                headers={
                    "Authorization": f"token {token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
            )

    def _handle_success(self, response: httpx.Response) -> ValidationResult:
        """Handle successful validation response.

        Args:
            response: The successful API response

        Returns:
            ValidationResult with user info
        """
        data = response.json()
        scopes = self._parse_scopes(response)

        return ValidationResult(
            status=TokenStatus.VALID,
            message=f"Token valid for user: {data.get('login', 'unknown')}",
            can_refresh=False,
            user_info={
                "login": data.get("login", ""),
                "name": data.get("name", ""),
                "email": data.get("email", ""),
            },
            scopes=scopes,
        )

    def _handle_unauthorized(self, response: httpx.Response) -> ValidationResult:
        """Handle 401 unauthorized response.

        Args:
            response: The 401 response

        Returns:
            ValidationResult with invalid/expired status
        """
        # Check if token is expired vs just invalid
        data = response.json() if response.text else {}
        message = data.get("message", "Bad credentials")

        if "expired" in message.lower():
            return ValidationResult(
                status=TokenStatus.EXPIRED,
                message="GitHub token has expired",
                can_refresh=False,
                refresh_instructions=self._get_refresh_instructions(),
            )

        return ValidationResult(
            status=TokenStatus.INVALID,
            message=f"GitHub token is invalid: {message}",
            can_refresh=False,
            refresh_instructions=self._get_refresh_instructions(),
        )

    def _handle_forbidden(self, response: httpx.Response) -> ValidationResult:
        """Handle 403 forbidden response (rate limit, etc.).

        Args:
            response: The 403 response

        Returns:
            ValidationResult with appropriate status
        """
        data = response.json() if response.text else {}
        message = data.get("message", "Forbidden")

        # Check for rate limiting
        if "rate limit" in message.lower():
            return ValidationResult(
                status=TokenStatus.UNKNOWN,
                message="Rate limited - unable to validate token",
                can_refresh=False,
            )

        return ValidationResult(
            status=TokenStatus.INVALID,
            message=f"Access forbidden: {message}",
            can_refresh=False,
            refresh_instructions=self._get_refresh_instructions(),
        )

    def _parse_scopes(self, response: httpx.Response) -> list[str]:
        """Parse OAuth scopes from response headers.

        Args:
            response: The API response

        Returns:
            List of scope strings
        """
        scopes_header = response.headers.get("X-OAuth-Scopes", "")
        if scopes_header:
            return [s.strip() for s in scopes_header.split(",") if s.strip()]
        return []

    def _get_refresh_instructions(self) -> str:
        """Get instructions for refreshing the GitHub token."""
        return (
            "To regenerate your GitHub PAT:\n"
            "1. Go to https://github.com/settings/tokens\n"
            "2. Click 'Generate new token' or regenerate existing\n"
            "3. Select required scopes (repo, read:user minimum)\n"
            "4. Update GITHUB_PERSONAL_ACCESS_TOKEN in your MCP config"
        )
