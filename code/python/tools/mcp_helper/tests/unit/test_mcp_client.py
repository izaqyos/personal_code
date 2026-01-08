"""Unit tests for MCP protocol client and server spawner."""

from __future__ import annotations

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mcp_health.config.models import MCPServerConfig
from mcp_health.mcp.client import (
    ConnectionResult,
    ConnectionStatus,
    MCPClient,
    MCPProtocolError,
)
from mcp_health.mcp.spawner import (
    MCPConnection,
    ServerSpawner,
    SpawnError,
)


class TestConnectionStatus:
    """Tests for ConnectionStatus enum."""

    def test_healthy_is_healthy(self) -> None:
        """Test that HEALTHY status is healthy."""
        assert ConnectionStatus.HEALTHY.is_healthy() is True

    def test_unhealthy_is_not_healthy(self) -> None:
        """Test that UNHEALTHY status is not healthy."""
        assert ConnectionStatus.UNHEALTHY.is_healthy() is False

    def test_timeout_is_not_healthy(self) -> None:
        """Test that TIMEOUT status is not healthy."""
        assert ConnectionStatus.TIMEOUT.is_healthy() is False

    def test_spawn_failed_is_not_healthy(self) -> None:
        """Test that SPAWN_FAILED status is not healthy."""
        assert ConnectionStatus.SPAWN_FAILED.is_healthy() is False


class TestConnectionResult:
    """Tests for ConnectionResult dataclass."""

    def test_is_healthy(self) -> None:
        """Test is_healthy method."""
        result = ConnectionResult(status=ConnectionStatus.HEALTHY, message="OK")
        assert result.is_healthy() is True

    def test_is_not_healthy(self) -> None:
        """Test is_healthy returns False for unhealthy."""
        result = ConnectionResult(status=ConnectionStatus.UNHEALTHY, message="Failed")
        assert result.is_healthy() is False

    def test_default_values(self) -> None:
        """Test default field values."""
        result = ConnectionResult(status=ConnectionStatus.HEALTHY, message="OK")
        assert result.resources == []
        assert result.capabilities == {}
        assert result.error_details is None


class TestSpawnError:
    """Tests for SpawnError exception."""

    def test_basic_error(self) -> None:
        """Test creating a basic SpawnError."""
        error = SpawnError("Failed to spawn")
        assert str(error) == "Failed to spawn"
        assert error.stderr is None

    def test_error_with_stderr(self) -> None:
        """Test SpawnError with stderr output."""
        error = SpawnError("Command failed", stderr="Error output")
        assert error.stderr == "Error output"


class TestMCPConnection:
    """Tests for MCPConnection dataclass."""

    @pytest.fixture
    def mock_process(self) -> MagicMock:
        """Create a mock process."""
        process = MagicMock()
        process.returncode = None
        return process

    @pytest.fixture
    def mock_config(self) -> MCPServerConfig:
        """Create a mock server config."""
        return MCPServerConfig(command="echo", args=["hello"])

    def test_is_alive_running(self, mock_process: MagicMock, mock_config: MCPServerConfig) -> None:
        """Test is_alive when process is running."""
        stdin = MagicMock()
        stdout = MagicMock()
        conn = MCPConnection(
            process=mock_process,
            stdin=stdin,
            stdout=stdout,
            server_name="test",
            config=mock_config,
        )
        assert conn.is_alive is True

    def test_is_alive_terminated(
        self, mock_process: MagicMock, mock_config: MCPServerConfig
    ) -> None:
        """Test is_alive when process has terminated."""
        mock_process.returncode = 0
        stdin = MagicMock()
        stdout = MagicMock()
        conn = MCPConnection(
            process=mock_process,
            stdin=stdin,
            stdout=stdout,
            server_name="test",
            config=mock_config,
        )
        assert conn.is_alive is False

    def test_is_alive_closed(self, mock_process: MagicMock, mock_config: MCPServerConfig) -> None:
        """Test is_alive when connection is closed."""
        stdin = MagicMock()
        stdout = MagicMock()
        conn = MCPConnection(
            process=mock_process,
            stdin=stdin,
            stdout=stdout,
            server_name="test",
            config=mock_config,
            _closed=True,
        )
        assert conn.is_alive is False

    @pytest.mark.asyncio
    async def test_close(self, mock_process: MagicMock, mock_config: MCPServerConfig) -> None:
        """Test closing a connection."""
        mock_process.terminate = MagicMock()
        mock_process.wait = AsyncMock(return_value=0)

        stdin = AsyncMock()
        stdin.close = MagicMock()
        stdin.wait_closed = AsyncMock()

        stdout = MagicMock()

        conn = MCPConnection(
            process=mock_process,
            stdin=stdin,
            stdout=stdout,
            server_name="test",
            config=mock_config,
        )

        await conn.close()

        assert conn._closed is True
        stdin.close.assert_called_once()
        mock_process.terminate.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_already_closed(
        self, mock_process: MagicMock, mock_config: MCPServerConfig
    ) -> None:
        """Test closing an already closed connection."""
        stdin = AsyncMock()
        stdout = MagicMock()

        conn = MCPConnection(
            process=mock_process,
            stdin=stdin,
            stdout=stdout,
            server_name="test",
            config=mock_config,
            _closed=True,
        )

        await conn.close()
        # Should not call terminate again
        mock_process.terminate.assert_not_called()

    @pytest.mark.asyncio
    async def test_close_process_already_exited(
        self, mock_process: MagicMock, mock_config: MCPServerConfig
    ) -> None:
        """Test closing when process already exited."""
        mock_process.returncode = 0  # Already exited
        mock_process.terminate = MagicMock()

        stdin = AsyncMock()
        stdin.close = MagicMock()
        stdin.wait_closed = AsyncMock()
        stdout = MagicMock()

        conn = MCPConnection(
            process=mock_process,
            stdin=stdin,
            stdout=stdout,
            server_name="test",
            config=mock_config,
        )

        await conn.close()
        # Terminate should not be called since process already exited
        mock_process.terminate.assert_not_called()


class TestServerSpawner:
    """Tests for ServerSpawner."""

    @pytest.fixture
    def spawner(self) -> ServerSpawner:
        """Create a spawner instance."""
        return ServerSpawner()

    @pytest.fixture
    def echo_config(self) -> MCPServerConfig:
        """Create a config that runs echo."""
        return MCPServerConfig(command="cat", args=[])

    @pytest.mark.asyncio
    async def test_spawn_command_not_found(self, spawner: ServerSpawner) -> None:
        """Test spawning with non-existent command."""
        config = MCPServerConfig(command="nonexistent_command_xyz", args=[])

        with pytest.raises(SpawnError) as exc_info:
            await spawner.spawn("test", config)

        assert "not found" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_spawn_timeout(self, spawner: ServerSpawner) -> None:
        """Test spawn timeout handling."""
        # This test simulates timeout by mocking
        config = MCPServerConfig(command="sleep", args=["100"])

        with patch("asyncio.create_subprocess_exec") as mock_create:
            # Make create_subprocess_exec hang
            async def slow_create(*args, **kwargs):
                await asyncio.sleep(10)
                raise Exception("Should not reach here")

            mock_create.side_effect = slow_create

            with pytest.raises(SpawnError) as exc_info:
                await spawner.spawn("test", config, timeout=0.1)

            assert "timeout" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_spawn_immediate_exit(self, spawner: ServerSpawner) -> None:
        """Test handling of process that exits immediately."""
        config = MCPServerConfig(command="false", args=[])  # false exits with code 1

        with pytest.raises(SpawnError) as exc_info:
            await spawner.spawn("test", config)

        assert "exited immediately" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_terminate(self, spawner: ServerSpawner) -> None:
        """Test terminating a connection."""
        mock_conn = MagicMock(spec=MCPConnection)
        mock_conn.close = AsyncMock()

        await spawner.terminate(mock_conn)

        mock_conn.close.assert_called_once()


class TestMCPClient:
    """Tests for MCPClient."""

    @pytest.fixture
    def mock_spawner(self) -> MagicMock:
        """Create a mock spawner."""
        return MagicMock(spec=ServerSpawner)

    @pytest.fixture
    def client(self, mock_spawner: MagicMock) -> MCPClient:
        """Create a client with mock spawner."""
        return MCPClient(spawner=mock_spawner)

    @pytest.fixture
    def test_config(self) -> MCPServerConfig:
        """Create a test config."""
        return MCPServerConfig(command="test", args=[])

    @pytest.mark.asyncio
    async def test_health_check_healthy(
        self, client: MCPClient, mock_spawner: MagicMock, test_config: MCPServerConfig
    ) -> None:
        """Test health check with healthy server."""
        # Mock connection
        mock_conn = MagicMock(spec=MCPConnection)
        mock_conn.is_alive = True
        mock_conn.stdin = MagicMock()
        mock_conn.stdin.write = MagicMock()
        mock_conn.stdin.drain = AsyncMock()
        mock_conn.stdout = MagicMock()

        # Mock responses
        init_response = (
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "result": {"capabilities": {"resources": True}},
                }
            ).encode()
            + b"\n"
        )
        resources_response = (
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "result": {"resources": [{"name": "test", "uri": "test://uri"}]},
                }
            ).encode()
            + b"\n"
        )

        mock_conn.stdout.readline = AsyncMock(side_effect=[init_response, resources_response])

        mock_spawner.spawn = AsyncMock(return_value=mock_conn)
        mock_spawner.terminate = AsyncMock()

        result = await client.health_check("test-server", test_config)

        assert result.status == ConnectionStatus.HEALTHY
        assert len(result.resources) == 1
        mock_spawner.terminate.assert_called_once()

    @pytest.mark.asyncio
    async def test_health_check_spawn_failed(
        self, client: MCPClient, mock_spawner: MagicMock, test_config: MCPServerConfig
    ) -> None:
        """Test health check when spawn fails."""
        mock_spawner.spawn = AsyncMock(side_effect=SpawnError("Failed to spawn"))
        mock_spawner.terminate = AsyncMock()

        result = await client.health_check("test-server", test_config)

        assert result.status == ConnectionStatus.SPAWN_FAILED
        assert "spawn" in result.message.lower()

    @pytest.mark.asyncio
    async def test_health_check_timeout(
        self, client: MCPClient, mock_spawner: MagicMock, test_config: MCPServerConfig
    ) -> None:
        """Test health check with timeout."""
        mock_conn = MagicMock(spec=MCPConnection)
        mock_conn.is_alive = True
        mock_conn.stdin = MagicMock()
        mock_conn.stdin.write = MagicMock()
        mock_conn.stdin.drain = AsyncMock()
        mock_conn.stdout = MagicMock()
        mock_conn.stdout.readline = AsyncMock(side_effect=asyncio.TimeoutError())

        mock_spawner.spawn = AsyncMock(return_value=mock_conn)
        mock_spawner.terminate = AsyncMock()

        result = await client.health_check("test-server", test_config, timeout=0.1)

        assert result.status == ConnectionStatus.TIMEOUT

    @pytest.mark.asyncio
    async def test_health_check_protocol_error(
        self, client: MCPClient, mock_spawner: MagicMock, test_config: MCPServerConfig
    ) -> None:
        """Test health check with protocol error."""
        mock_conn = MagicMock(spec=MCPConnection)
        mock_conn.is_alive = True
        mock_conn.stdin = MagicMock()
        mock_conn.stdin.write = MagicMock()
        mock_conn.stdin.drain = AsyncMock()
        mock_conn.stdout = MagicMock()

        # Return error response
        error_response = (
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "error": {"code": -32600, "message": "Invalid Request"},
                }
            ).encode()
            + b"\n"
        )
        mock_conn.stdout.readline = AsyncMock(return_value=error_response)

        mock_spawner.spawn = AsyncMock(return_value=mock_conn)
        mock_spawner.terminate = AsyncMock()

        result = await client.health_check("test-server", test_config)

        assert result.status == ConnectionStatus.PROTOCOL_ERROR

    @pytest.mark.asyncio
    async def test_health_check_invalid_json(
        self, client: MCPClient, mock_spawner: MagicMock, test_config: MCPServerConfig
    ) -> None:
        """Test health check with invalid JSON response."""
        mock_conn = MagicMock(spec=MCPConnection)
        mock_conn.is_alive = True
        mock_conn.stdin = MagicMock()
        mock_conn.stdin.write = MagicMock()
        mock_conn.stdin.drain = AsyncMock()
        mock_conn.stdout = MagicMock()
        mock_conn.stdout.readline = AsyncMock(return_value=b"not valid json\n")

        mock_spawner.spawn = AsyncMock(return_value=mock_conn)
        mock_spawner.terminate = AsyncMock()

        result = await client.health_check("test-server", test_config)

        assert result.status == ConnectionStatus.PROTOCOL_ERROR

    @pytest.mark.asyncio
    async def test_health_check_empty_response(
        self, client: MCPClient, mock_spawner: MagicMock, test_config: MCPServerConfig
    ) -> None:
        """Test health check with empty response."""
        mock_conn = MagicMock(spec=MCPConnection)
        mock_conn.is_alive = True
        mock_conn.stdin = MagicMock()
        mock_conn.stdin.write = MagicMock()
        mock_conn.stdin.drain = AsyncMock()
        mock_conn.stdout = MagicMock()
        mock_conn.stdout.readline = AsyncMock(return_value=b"")

        mock_spawner.spawn = AsyncMock(return_value=mock_conn)
        mock_spawner.terminate = AsyncMock()

        result = await client.health_check("test-server", test_config)

        assert result.status == ConnectionStatus.PROTOCOL_ERROR

    @pytest.mark.asyncio
    async def test_health_check_connection_not_alive(
        self, client: MCPClient, mock_spawner: MagicMock, test_config: MCPServerConfig
    ) -> None:
        """Test health check when connection dies."""
        mock_conn = MagicMock(spec=MCPConnection)
        mock_conn.is_alive = False  # Connection died
        mock_conn.stdin = MagicMock()
        mock_conn.stdin.write = MagicMock()
        mock_conn.stdin.drain = AsyncMock()
        mock_conn.stdout = MagicMock()

        mock_spawner.spawn = AsyncMock(return_value=mock_conn)
        mock_spawner.terminate = AsyncMock()

        result = await client.health_check("test-server", test_config)

        assert result.status == ConnectionStatus.PROTOCOL_ERROR
        assert "not alive" in result.message.lower()

    @pytest.mark.asyncio
    async def test_health_check_unexpected_error(
        self, client: MCPClient, mock_spawner: MagicMock, test_config: MCPServerConfig
    ) -> None:
        """Test health check with unexpected error."""
        mock_conn = MagicMock(spec=MCPConnection)
        mock_conn.is_alive = True
        mock_conn.stdin = MagicMock()
        mock_conn.stdin.write = MagicMock(side_effect=RuntimeError("Unexpected"))
        mock_conn.stdin.drain = AsyncMock()

        mock_spawner.spawn = AsyncMock(return_value=mock_conn)
        mock_spawner.terminate = AsyncMock()

        result = await client.health_check("test-server", test_config)

        assert result.status == ConnectionStatus.UNHEALTHY

    def test_create_request(self, client: MCPClient) -> None:
        """Test creating JSON-RPC request."""
        request = client._create_request("test/method", {"key": "value"})

        assert request["jsonrpc"] == "2.0"
        assert request["method"] == "test/method"
        assert request["params"] == {"key": "value"}
        assert "id" in request

    def test_create_request_increments_id(self, client: MCPClient) -> None:
        """Test that request IDs increment."""
        request1 = client._create_request("method1", {})
        request2 = client._create_request("method2", {})

        assert request2["id"] > request1["id"]


class TestMCPProtocolError:
    """Tests for MCPProtocolError."""

    def test_error_message(self) -> None:
        """Test creating protocol error."""
        error = MCPProtocolError("Invalid message")
        assert str(error) == "Invalid message"
