"""MCP protocol client for health checking."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

from mcp_health.mcp.spawner import MCPConnection, ServerSpawner, SpawnError

if TYPE_CHECKING:
    from mcp_health.config.models import MCPServerConfig


class ConnectionStatus(Enum):
    """Status of an MCP server connection."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    TIMEOUT = "timeout"
    SPAWN_FAILED = "spawn_failed"
    PROTOCOL_ERROR = "protocol_error"

    def is_healthy(self) -> bool:
        """Check if the status indicates a healthy connection."""
        return self == ConnectionStatus.HEALTHY


class MCPProtocolError(Exception):
    """Error in MCP protocol communication."""

    pass


@dataclass
class ConnectionResult:
    """Result of a connection health check.

    Attributes:
        status: The connection status
        message: Human-readable description
        resources: List of resources if available
        capabilities: Server capabilities if available
        error_details: Error details if failed
    """

    status: ConnectionStatus
    message: str
    resources: list[dict[str, Any]] = field(default_factory=list)
    capabilities: dict[str, Any] = field(default_factory=dict)
    error_details: str | None = None

    def is_healthy(self) -> bool:
        """Check if the result indicates a healthy connection."""
        return self.status.is_healthy()


class MCPClient:
    """Client for communicating with MCP servers.

    Implements the MCP protocol for health checking purposes:
    - Initialize handshake
    - List resources to verify connectivity

    Example:
        client = MCPClient()
        result = await client.health_check("github", config)
        if result.is_healthy():
            print(f"Server has {len(result.resources)} resources")
    """

    DEFAULT_TIMEOUT = 30.0
    PROTOCOL_VERSION = "2024-11-05"

    def __init__(self, spawner: ServerSpawner | None = None):
        """Initialize the MCP client.

        Args:
            spawner: Optional custom spawner instance
        """
        self._spawner = spawner or ServerSpawner()
        self._message_id = 0

    async def health_check(
        self,
        server_name: str,
        config: MCPServerConfig,
        timeout: float | None = None,
    ) -> ConnectionResult:
        """Perform a full health check on an MCP server.

        Spawns the server, initializes the connection, lists resources,
        and then terminates the connection.

        Args:
            server_name: Name to identify this server
            config: Server configuration
            timeout: Overall timeout for the health check

        Returns:
            ConnectionResult with status and details
        """
        timeout = timeout or self.DEFAULT_TIMEOUT
        connection: MCPConnection | None = None

        try:
            # Spawn the server
            connection = await self._spawner.spawn(server_name, config, timeout=timeout)

            # Initialize
            init_result = await self._initialize(connection, timeout)
            if not init_result:
                return ConnectionResult(
                    status=ConnectionStatus.PROTOCOL_ERROR,
                    message="Failed to initialize MCP connection",
                    error_details="Server did not respond to initialize request",
                )

            # List resources to verify full connectivity
            resources = await self._list_resources(connection, timeout)

            return ConnectionResult(
                status=ConnectionStatus.HEALTHY,
                message=f"Server healthy with {len(resources)} resources",
                resources=resources,
                capabilities=init_result.get("capabilities", {}),
            )

        except SpawnError as e:
            return ConnectionResult(
                status=ConnectionStatus.SPAWN_FAILED,
                message=f"Failed to spawn server: {e}",
                error_details=e.stderr,
            )
        except asyncio.TimeoutError:
            return ConnectionResult(
                status=ConnectionStatus.TIMEOUT,
                message=f"Health check timed out after {timeout}s",
            )
        except MCPProtocolError as e:
            return ConnectionResult(
                status=ConnectionStatus.PROTOCOL_ERROR,
                message=str(e),
            )
        except Exception as e:
            return ConnectionResult(
                status=ConnectionStatus.UNHEALTHY,
                message=f"Unexpected error: {e}",
                error_details=str(e),
            )
        finally:
            if connection:
                await self._spawner.terminate(connection)

    async def _initialize(self, connection: MCPConnection, timeout: float) -> dict[str, Any] | None:
        """Send initialize request and wait for response.

        Args:
            connection: Active MCP connection
            timeout: Timeout for the request

        Returns:
            Initialize result or None if failed
        """
        request = self._create_request(
            "initialize",
            {
                "protocolVersion": self.PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {
                    "name": "mcp-health",
                    "version": "0.1.0",
                },
            },
        )

        response = await self._send_request(connection, request, timeout)
        return response.get("result") if response else None

    async def _list_resources(
        self, connection: MCPConnection, timeout: float
    ) -> list[dict[str, Any]]:
        """List resources from the server.

        Args:
            connection: Active MCP connection
            timeout: Timeout for the request

        Returns:
            List of resource objects
        """
        request = self._create_request("resources/list", {})
        response = await self._send_request(connection, request, timeout)

        if response and "result" in response:
            resources: list[dict[str, Any]] = response["result"].get("resources", [])
            return resources
        return []

    def _create_request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        """Create a JSON-RPC request.

        Args:
            method: The method name
            params: Method parameters

        Returns:
            JSON-RPC request object
        """
        self._message_id += 1
        return {
            "jsonrpc": "2.0",
            "id": self._message_id,
            "method": method,
            "params": params,
        }

    async def _send_request(
        self,
        connection: MCPConnection,
        request: dict[str, Any],
        timeout: float,
    ) -> dict[str, Any] | None:
        """Send a request and wait for response.

        Args:
            connection: Active MCP connection
            request: JSON-RPC request
            timeout: Timeout for the request

        Returns:
            Response object or None if failed

        Raises:
            MCPProtocolError: If protocol error occurs
        """
        if not connection.is_alive:
            raise MCPProtocolError("Connection is not alive")

        # Send request
        message = json.dumps(request) + "\n"
        connection.stdin.write(message.encode("utf-8"))
        await connection.stdin.drain()

        # Read response
        try:
            line = await asyncio.wait_for(connection.stdout.readline(), timeout=timeout)
            if not line:
                return None

            response: dict[str, Any] = json.loads(line.decode("utf-8"))

            if "error" in response:
                error = response["error"]
                raise MCPProtocolError(
                    f"MCP error {error.get('code', 'unknown')}: {error.get('message', 'unknown')}"
                )

            return response
        except json.JSONDecodeError as e:
            raise MCPProtocolError(f"Invalid JSON response: {e}") from e
        except asyncio.TimeoutError:
            raise
