"""MCP server process spawner."""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp_health.config.models import MCPServerConfig


class SpawnError(Exception):
    """Failed to spawn MCP server process."""

    def __init__(self, message: str, stderr: str | None = None):
        self.stderr = stderr
        super().__init__(message)


@dataclass
class MCPConnection:
    """Represents a connection to a spawned MCP server.

    Attributes:
        process: The asyncio subprocess
        stdin: Writer for sending messages
        stdout: Reader for receiving messages
        server_name: Name of the server for identification
        config: Original server configuration
    """

    process: asyncio.subprocess.Process
    stdin: asyncio.StreamWriter
    stdout: asyncio.StreamReader
    server_name: str
    config: MCPServerConfig
    _closed: bool = field(default=False, repr=False)

    @property
    def is_alive(self) -> bool:
        """Check if the process is still running."""
        return self.process.returncode is None and not self._closed

    async def close(self) -> None:
        """Close the connection and terminate the process."""
        if self._closed:
            return
        self._closed = True
        try:
            self.stdin.close()
            await self.stdin.wait_closed()
        except Exception:
            pass
        await self._terminate_process()

    async def _terminate_process(self) -> None:
        """Terminate the process, forcefully if needed."""
        if self.process.returncode is not None:
            return

        self.process.terminate()
        try:
            await asyncio.wait_for(self.process.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            self.process.kill()
            await self.process.wait()


class ServerSpawner:
    """Spawns and manages MCP server subprocesses.

    Example:
        spawner = ServerSpawner()
        connection = await spawner.spawn("github", config)
        # ... use connection ...
        await spawner.terminate(connection)
    """

    DEFAULT_TIMEOUT = 30.0

    async def spawn(
        self,
        server_name: str,
        config: MCPServerConfig,
        timeout: float | None = None,
    ) -> MCPConnection:
        """Spawn an MCP server subprocess.

        Args:
            server_name: Name to identify this server
            config: Server configuration with command and args
            timeout: Spawn timeout in seconds

        Returns:
            MCPConnection for communicating with the server

        Raises:
            SpawnError: If the process fails to start
        """
        timeout = timeout or self.DEFAULT_TIMEOUT

        # Build environment with config env vars
        env = os.environ.copy()
        env.update(config.env)

        cmd = [config.command, *config.args]

        try:
            process = await asyncio.wait_for(
                asyncio.create_subprocess_exec(
                    *cmd,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    env=env,
                ),
                timeout=timeout,
            )
        except asyncio.TimeoutError as e:
            raise SpawnError(
                f"Timeout while spawning {server_name}: command took > {timeout}s"
            ) from e
        except FileNotFoundError as e:
            raise SpawnError(f"Command not found for {server_name}: {config.command}") from e
        except OSError as e:
            raise SpawnError(f"Failed to spawn {server_name}: {e}") from e

        if process.stdin is None or process.stdout is None:
            if process.returncode is None:
                process.kill()
            raise SpawnError(f"Failed to get stdin/stdout for {server_name}")

        # Check if process immediately exited (bad command, etc.)
        # Give it a tiny moment to fail if it's going to
        await asyncio.sleep(0.1)
        if process.returncode is not None:
            stderr = ""
            if process.stderr:
                stderr_bytes = await process.stderr.read()
                stderr = stderr_bytes.decode("utf-8", errors="replace")
            raise SpawnError(
                f"Process {server_name} exited immediately with code {process.returncode}",
                stderr=stderr,
            )

        # Create StreamWriter wrapper for stdin
        # Note: process.stdin is already a StreamWriter in Python 3.8+
        stdin_writer = process.stdin

        return MCPConnection(
            process=process,
            stdin=stdin_writer,
            stdout=process.stdout,
            server_name=server_name,
            config=config,
        )

    async def terminate(self, connection: MCPConnection) -> None:
        """Terminate an MCP server connection.

        Args:
            connection: The connection to terminate
        """
        await connection.close()
