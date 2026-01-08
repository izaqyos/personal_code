"""Data models for MCP configuration."""

from __future__ import annotations

from pydantic import BaseModel, Field


class MCPServerConfig(BaseModel):
    """Configuration for a single MCP server.

    Attributes:
        command: The command to run (e.g., 'npx')
        args: List of arguments for the command
        env: Environment variables to set for the server process
    """

    command: str = Field(..., description="Command to execute the MCP server")
    args: list[str] = Field(default_factory=list, description="Arguments for the command")
    env: dict[str, str] = Field(
        default_factory=dict, description="Environment variables for the server"
    )

    def get_env_var(self, key: str, default: str | None = None) -> str | None:
        """Get an environment variable from the config.

        Args:
            key: The environment variable name
            default: Default value if not found

        Returns:
            The environment variable value or default
        """
        return self.env.get(key, default)

    def has_env_var(self, key: str) -> bool:
        """Check if an environment variable exists in the config.

        Args:
            key: The environment variable name

        Returns:
            True if the variable exists
        """
        return key in self.env


class MCPConfig(BaseModel):
    """Root configuration containing all MCP servers.

    Attributes:
        mcp_servers: Dictionary mapping server names to their configurations
    """

    mcp_servers: dict[str, MCPServerConfig] = Field(
        ..., alias="mcpServers", description="Map of server names to configurations"
    )

    model_config = {"populate_by_name": True}

    def get_server(self, name: str) -> MCPServerConfig | None:
        """Get a server configuration by name.

        Args:
            name: The server name

        Returns:
            The server configuration or None if not found
        """
        return self.mcp_servers.get(name)

    def server_names(self) -> list[str]:
        """Get list of all server names.

        Returns:
            List of server names
        """
        return list(self.mcp_servers.keys())

    def __len__(self) -> int:
        """Return the number of configured servers."""
        return len(self.mcp_servers)

    def __iter__(self):  # type: ignore[no-untyped-def]
        """Iterate over server name and config pairs."""
        return iter(self.mcp_servers.items())
