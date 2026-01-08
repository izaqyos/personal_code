"""Base validator interface and common types."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING, TypeVar

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

if TYPE_CHECKING:
    from mcp_health.config.models import MCPServerConfig

logger = logging.getLogger(__name__)

T = TypeVar("T")


def with_retry(
    max_attempts: int = 3,
    min_wait: float = 0.5,
    max_wait: float = 5.0,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator factory for retrying network operations.

    Retries on httpx network errors with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts
        min_wait: Minimum wait between retries (seconds)
        max_wait: Maximum wait between retries (seconds)

    Returns:
        Decorator that adds retry behavior
    """
    return retry(
        retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException)),
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=min_wait, max=max_wait),
        reraise=True,
    )


class TokenStatus(Enum):
    """Status of a token after validation."""

    VALID = "valid"
    INVALID = "invalid"
    EXPIRED = "expired"
    EXPIRING_SOON = "expiring_soon"  # Token valid but expires within 24h
    MISSING = "missing"
    NETWORK_ERROR = "network_error"  # Distinct from unknown
    UNKNOWN = "unknown"

    def is_healthy(self) -> bool:
        """Check if the status indicates a healthy token."""
        return self in (TokenStatus.VALID, TokenStatus.EXPIRING_SOON)

    def needs_refresh(self) -> bool:
        """Check if the token needs to be refreshed."""
        return self in (TokenStatus.INVALID, TokenStatus.EXPIRED)

    def is_network_issue(self) -> bool:
        """Check if the status indicates a network problem."""
        return self == TokenStatus.NETWORK_ERROR


@dataclass
class ValidationResult:
    """Result of token validation.

    Attributes:
        status: The validation status
        message: Human-readable message about the result
        expires_at: When the token expires (if known)
        can_refresh: Whether the token can be auto-refreshed
        refresh_instructions: Instructions for manual refresh (if applicable)
        user_info: Additional user/account info from the validation
        scopes: Token scopes/permissions (if available)
        warning: Optional warning message (e.g., expiring soon)
    """

    status: TokenStatus
    message: str
    expires_at: datetime | None = None
    can_refresh: bool = False
    refresh_instructions: str | None = None
    user_info: dict[str, str] = field(default_factory=dict)
    scopes: list[str] = field(default_factory=list)
    warning: str | None = None

    def is_healthy(self) -> bool:
        """Check if the validation result indicates a healthy token."""
        return self.status.is_healthy()

    def needs_refresh(self) -> bool:
        """Check if the token needs to be refreshed."""
        return self.status.needs_refresh()

    def has_warning(self) -> bool:
        """Check if there's a warning to display."""
        return self.warning is not None or self.status == TokenStatus.EXPIRING_SOON


class BaseValidator(ABC):
    """Abstract base class for service-specific token validators.

    Subclasses must implement the validate() method to check tokens
    for their specific service.
    """

    # Service name for identification
    service_name: str = "unknown"

    # Shared timeout for all validators (can be overridden)
    TIMEOUT_SECONDS: float = 10.0

    # Retry configuration
    RETRY_MAX_ATTEMPTS: int = 3
    RETRY_MIN_WAIT: float = 0.5
    RETRY_MAX_WAIT: float = 5.0

    # Expiration warning threshold
    EXPIRATION_WARNING_HOURS: int = 24

    @abstractmethod
    async def validate(self, config: MCPServerConfig) -> ValidationResult:
        """Validate the token for this service.

        Args:
            config: The MCP server configuration containing the token

        Returns:
            ValidationResult with the status and details
        """
        pass

    def get_token_env_var(self) -> str:
        """Get the environment variable name for this service's token.

        Returns:
            The environment variable name
        """
        return ""

    def extract_token(self, config: MCPServerConfig) -> str | None:
        """Extract the token from the server config.

        Args:
            config: The MCP server configuration

        Returns:
            The token string or None if not found
        """
        env_var = self.get_token_env_var()
        if env_var:
            return config.get_env_var(env_var)
        return None

    def _create_error_result(
        self,
        status: TokenStatus,
        message: str,
        include_instructions: bool = True,
        can_refresh: bool = False,
    ) -> ValidationResult:
        """Create a standardized error result.

        Args:
            status: The token status
            message: Error message
            include_instructions: Whether to include refresh instructions
            can_refresh: Whether token can be auto-refreshed

        Returns:
            ValidationResult with appropriate fields
        """
        return ValidationResult(
            status=status,
            message=message,
            can_refresh=can_refresh,
            refresh_instructions=self._get_refresh_instructions() if include_instructions else None,
        )

    def _get_refresh_instructions(self) -> str:
        """Get refresh instructions for this service. Override in subclasses."""
        return "Please regenerate the token for this service."

    def _check_expiration_warning(self, expires_at: datetime | None) -> tuple[bool, str | None]:
        """Check if token is expiring soon.

        Args:
            expires_at: Token expiration datetime

        Returns:
            Tuple of (is_expiring_soon, warning_message)
        """
        if not expires_at:
            return False, None

        from datetime import timezone

        now = datetime.now(timezone.utc)
        # Ensure expires_at is timezone-aware
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        time_until_expiry = expires_at - now
        threshold = timedelta(hours=self.EXPIRATION_WARNING_HOURS)

        if timedelta(0) < time_until_expiry <= threshold:
            hours_left = time_until_expiry.total_seconds() / 3600
            return True, f"Token expires in {hours_left:.1f} hours"

        return False, None
