"""OAuth token refresh and re-authentication for Atlassian."""

from __future__ import annotations

import asyncio
import contextlib
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

import httpx


class RefreshStatus(Enum):
    """Status of a token refresh attempt."""

    SUCCESS = "success"
    FAILED = "failed"
    NO_TOKEN = "no_token"
    NO_REFRESH_TOKEN = "no_refresh_token"
    NETWORK_ERROR = "network_error"
    INVALID_REFRESH_TOKEN = "invalid_refresh_token"
    REAUTH_REQUIRED = "reauth_required"


class ReauthStatus(Enum):
    """Status of a re-authentication attempt."""

    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
    NPX_NOT_FOUND = "npx_not_found"


@dataclass
class RefreshResult:
    """Result of a token refresh attempt.

    Attributes:
        status: The refresh status
        message: Human-readable message
        new_access_token: New access token if successful
        new_expires_at: Expiration time of new token
    """

    status: RefreshStatus
    message: str
    new_access_token: str | None = None
    new_expires_at: datetime | None = None

    def is_success(self) -> bool:
        """Check if refresh was successful."""
        return self.status == RefreshStatus.SUCCESS

    def needs_reauth(self) -> bool:
        """Check if re-authentication is required."""
        return self.status in (
            RefreshStatus.NO_TOKEN,
            RefreshStatus.INVALID_REFRESH_TOKEN,
            RefreshStatus.REAUTH_REQUIRED,
        )


@dataclass
class ReauthResult:
    """Result of a re-authentication attempt.

    Attributes:
        status: The reauth status
        message: Human-readable message
    """

    status: ReauthStatus
    message: str

    def is_success(self) -> bool:
        """Check if reauth was successful."""
        return self.status == ReauthStatus.SUCCESS


class OAuthRefresher:
    """Handles OAuth token refresh for services that support it.

    Currently supports:
    - Atlassian (via mcp-remote stored tokens)

    Example:
        refresher = OAuthRefresher()
        result = await refresher.refresh_atlassian(Path("/path/to/.mcp-auth"))
        if result.is_success():
            print(f"New token: {result.new_access_token}")
    """

    ATLASSIAN_TOKEN_URL = "https://auth.atlassian.com/oauth/token"
    TOKEN_FILE_NAME = "tokens.json"
    TIMEOUT_SECONDS = 30.0

    # mcp-remote configuration
    MCP_REMOTE_PACKAGE = "mcp-remote@0.1.30"
    ATLASSIAN_SSE_URL = "https://mcp.atlassian.com/v1/sse"
    REAUTH_TIMEOUT_SECONDS = 120  # 2 minutes for user to complete OAuth

    async def reauth_atlassian(
        self,
        config_dir: Path,
        server_url: str | None = None,
        timeout: int | None = None,
    ) -> ReauthResult:
        """Trigger re-authentication for Atlassian via mcp-remote.

        Spawns `npx mcp-remote` which opens a browser for OAuth authentication.
        Waits for the user to complete the OAuth flow and save new tokens.

        Args:
            config_dir: Path to MCP_REMOTE_CONFIG_DIR
            server_url: Atlassian SSE URL (default: mcp.atlassian.com)
            timeout: Timeout in seconds to wait for auth completion

        Returns:
            ReauthResult with status and message
        """
        # Check if npx is available
        npx_path = shutil.which("npx")
        if not npx_path:
            return ReauthResult(
                status=ReauthStatus.NPX_NOT_FOUND,
                message="npx not found in PATH. Install Node.js to use mcp-remote.",
            )

        # Use defaults
        if server_url is None:
            server_url = self.ATLASSIAN_SSE_URL
        if timeout is None:
            timeout = self.REAUTH_TIMEOUT_SECONDS

        # Clear existing stale tokens to force fresh OAuth
        self._clear_stale_tokens(config_dir)

        # Build command
        cmd = [
            npx_path,
            "-y",
            self.MCP_REMOTE_PACKAGE,
            server_url,
            "--config-dir",
            str(config_dir),
        ]

        print("\n🔐 Starting Atlassian OAuth re-authentication...")
        print("   A browser will open for you to log in to Atlassian.")
        print(f"   Waiting up to {timeout} seconds for completion...\n")

        try:
            # Run mcp-remote - it will open browser for OAuth
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            # Wait for process with timeout
            # mcp-remote will exit after saving tokens or on error
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return ReauthResult(
                    status=ReauthStatus.TIMEOUT,
                    message=f"OAuth timed out after {timeout}s. Please try again.",
                )

            # Check if tokens were created
            tokens, _ = self._load_tokens(config_dir)
            if tokens and tokens.get("access_token"):
                return ReauthResult(
                    status=ReauthStatus.SUCCESS,
                    message="Successfully re-authenticated with Atlassian!",
                )
            else:
                error_msg = stderr.decode() if stderr else "Unknown error"
                return ReauthResult(
                    status=ReauthStatus.FAILED,
                    message=f"OAuth failed: {error_msg}",
                )

        except FileNotFoundError:
            return ReauthResult(
                status=ReauthStatus.NPX_NOT_FOUND,
                message="npx not found. Install Node.js to use mcp-remote.",
            )
        except Exception as e:
            return ReauthResult(
                status=ReauthStatus.FAILED,
                message=f"Re-authentication failed: {e}",
            )

    def _clear_stale_tokens(self, config_dir: Path) -> None:
        """Clear stale token files to force fresh OAuth.

        Args:
            config_dir: Path to config directory
        """
        if not config_dir.exists():
            return

        # Remove token files (but keep client_info.json for client registration)
        patterns = ["*_tokens.json", "*_code_verifier.txt", "*_lock.json"]
        for pattern in patterns:
            for file_path in config_dir.glob(pattern):
                with contextlib.suppress(OSError):
                    file_path.unlink()

        # Also check subdirectories
        for subdir in config_dir.iterdir():
            if subdir.is_dir():
                for pattern in patterns:
                    for file_path in subdir.glob(pattern):
                        with contextlib.suppress(OSError):
                            file_path.unlink()

    async def refresh_atlassian(self, config_dir: Path) -> RefreshResult:
        """Refresh Atlassian OAuth tokens.

        Reads tokens from the mcp-remote config directory, uses the
        refresh_token to get new tokens, and writes them back.

        Args:
            config_dir: Path to MCP_REMOTE_CONFIG_DIR

        Returns:
            RefreshResult with status and new tokens if successful
        """
        # Load existing tokens
        tokens, token_path = self._load_tokens(config_dir)
        if tokens is None:
            return RefreshResult(
                status=RefreshStatus.NO_TOKEN,
                message=f"Token file not found in {config_dir}",
            )

        refresh_token = tokens.get("refresh_token")
        if not refresh_token:
            return RefreshResult(
                status=RefreshStatus.NO_REFRESH_TOKEN,
                message="No refresh_token found in token file",
            )

        # Get client credentials from tokens file if available
        client_id = tokens.get("client_id")
        client_secret = tokens.get("client_secret")

        # Perform refresh
        return await self._do_refresh(
            refresh_token,
            client_id,
            client_secret,
            token_path,
        )

    def _load_tokens(self, config_dir: Path) -> tuple[dict[str, Any] | None, Path | None]:
        """Load tokens from config directory.

        Args:
            config_dir: Path to config directory

        Returns:
            Tuple of (tokens dict, token file path) or (None, None)
        """
        if not config_dir.exists():
            return None, None

        # mcp-remote stores tokens with hash prefixes: <hash>_tokens.json
        # Try multiple patterns to find the tokens file

        # Pattern 1: Direct tokens.json in root
        token_path = config_dir / self.TOKEN_FILE_NAME
        if token_path.exists():
            try:
                return json.loads(token_path.read_text()), token_path
            except (json.JSONDecodeError, OSError):
                pass

        # Pattern 2: Hash-prefixed tokens in root (*_tokens.json)
        for token_file in config_dir.glob(f"*_{self.TOKEN_FILE_NAME}"):
            try:
                return json.loads(token_file.read_text()), token_file
            except (json.JSONDecodeError, OSError):
                continue

        # Pattern 3: Search subdirectories for tokens.json or *_tokens.json
        for subdir in config_dir.iterdir():
            if subdir.is_dir():
                # Try direct tokens.json
                token_path = subdir / self.TOKEN_FILE_NAME
                if token_path.exists():
                    try:
                        return json.loads(token_path.read_text()), token_path
                    except (json.JSONDecodeError, OSError):
                        pass

                # Try hash-prefixed tokens
                for token_file in subdir.glob(f"*_{self.TOKEN_FILE_NAME}"):
                    try:
                        return json.loads(token_file.read_text()), token_file
                    except (json.JSONDecodeError, OSError):
                        continue

        return None, None

    async def _do_refresh(
        self,
        refresh_token: str,
        client_id: str | None,
        client_secret: str | None,
        token_path: Path | None,
    ) -> RefreshResult:
        """Perform the OAuth refresh request.

        Args:
            refresh_token: The refresh token
            client_id: OAuth client ID (if available)
            client_secret: OAuth client secret (if available)
            token_path: Path to write updated tokens

        Returns:
            RefreshResult with new tokens if successful
        """
        # Build refresh request
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        if client_id:
            data["client_id"] = client_id
        if client_secret:
            data["client_secret"] = client_secret

        try:
            async with httpx.AsyncClient(timeout=self.TIMEOUT_SECONDS) as client:
                response = await client.post(
                    self.ATLASSIAN_TOKEN_URL,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )

                if response.status_code == 200:
                    return self._handle_success(response, token_path)
                else:
                    return self._handle_error(response)

        except httpx.TimeoutException:
            return RefreshResult(
                status=RefreshStatus.NETWORK_ERROR,
                message="Timeout while refreshing token",
            )
        except httpx.RequestError as e:
            return RefreshResult(
                status=RefreshStatus.NETWORK_ERROR,
                message=f"Network error: {e}",
            )

    def _handle_success(self, response: httpx.Response, token_path: Path | None) -> RefreshResult:
        """Handle successful token refresh.

        Args:
            response: The successful API response
            token_path: Path to write updated tokens

        Returns:
            RefreshResult with new tokens
        """
        data = response.json()
        new_access_token = data.get("access_token")
        new_refresh_token = data.get("refresh_token")
        expires_in = data.get("expires_in", 3600)

        # Calculate expiration time
        now = datetime.now(timezone.utc)
        expires_at = now.replace(microsecond=0)
        if expires_in:
            from datetime import timedelta

            expires_at = now + timedelta(seconds=int(expires_in))

        # Write updated tokens
        if token_path and new_access_token:
            self._write_tokens(
                token_path,
                new_access_token,
                new_refresh_token,
                expires_at,
            )

        return RefreshResult(
            status=RefreshStatus.SUCCESS,
            message="Token refreshed successfully",
            new_access_token=new_access_token,
            new_expires_at=expires_at,
        )

    def _handle_error(self, response: httpx.Response) -> RefreshResult:
        """Handle failed token refresh.

        Args:
            response: The error API response

        Returns:
            RefreshResult with failure details
        """
        status = RefreshStatus.FAILED
        try:
            data = response.json()
            error = data.get("error", "unknown")
            description = data.get("error_description", "").lower()
            message = f"Refresh failed: {error}"
            if description:
                message += f" - {data.get('error_description', '')}"

            # Detect invalid refresh token errors that require re-authentication
            invalid_token_indicators = [
                "invalid",
                "expired",
                "revoked",
                "unauthorized_client",
                "invalid_grant",
            ]
            if any(ind in error.lower() or ind in description for ind in invalid_token_indicators):
                status = RefreshStatus.INVALID_REFRESH_TOKEN

        except Exception:
            message = f"Refresh failed with status {response.status_code}"

        return RefreshResult(
            status=status,
            message=message,
        )

    def _write_tokens(
        self,
        token_path: Path,
        access_token: str,
        refresh_token: str | None,
        expires_at: datetime,
    ) -> None:
        """Write updated tokens to file.

        Args:
            token_path: Path to token file
            access_token: New access token
            refresh_token: New refresh token (if rotated)
            expires_at: Token expiration time
        """
        try:
            # Load existing tokens to preserve other fields
            existing = {}
            if token_path.exists():
                try:  # noqa: SIM105
                    existing = json.loads(token_path.read_text())
                except Exception:
                    pass

            # Update with new values
            existing["access_token"] = access_token
            if refresh_token:
                existing["refresh_token"] = refresh_token
            existing["expires_at"] = expires_at.isoformat()
            existing["refreshed_at"] = datetime.now(timezone.utc).isoformat()

            token_path.write_text(json.dumps(existing, indent=2))
        except OSError:
            # Silently fail - token is still valid in memory
            pass
