"""CLI for MCP Health Check tool."""

from __future__ import annotations

import asyncio
import logging
import time
from pathlib import Path

import click
from rich.console import Console

from mcp_health.config import ConfigError, ConfigLoader
from mcp_health.config.models import MCPServerConfig
from mcp_health.mcp.client import MCPClient
from mcp_health.refresh.notifier import ServiceType, UserNotifier
from mcp_health.refresh.oauth import OAuthRefresher
from mcp_health.reporting.report import (
    HealthReport,
    ReportGenerator,
    ServerHealth,
)
from mcp_health.validators.atlassian import AtlassianValidator
from mcp_health.validators.base import BaseValidator
from mcp_health.validators.github import GitHubValidator
from mcp_health.validators.slack import SlackValidator

console = Console()
logger = logging.getLogger(__name__)


def get_validator_for_server(server_name: str) -> BaseValidator | None:
    """Get the appropriate validator for a server name.

    Args:
        server_name: Name of the server

    Returns:
        Validator instance or None if unknown
    """
    validators = {
        "github": GitHubValidator(),
        "slack": SlackValidator(),
    }
    # Check for Atlassian variants
    if "atlassian" in server_name.lower() or "jira" in server_name.lower():
        return AtlassianValidator()
    return validators.get(server_name.lower())


def get_service_type(server_name: str) -> ServiceType:
    """Get service type from server name.

    Args:
        server_name: Name of the server

    Returns:
        ServiceType enum
    """
    name_lower = server_name.lower()
    if "github" in name_lower:
        return ServiceType.GITHUB
    elif "slack" in name_lower:
        return ServiceType.SLACK
    elif "atlassian" in name_lower or "jira" in name_lower:
        return ServiceType.ATLASSIAN
    return ServiceType.UNKNOWN


@click.group()
@click.version_option(version="0.1.0")
def main() -> None:
    """MCP Health Check - Monitor your MCP server connections."""
    pass


@main.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, path_type=Path),
    help="Path to MCP config file",
)
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["console", "json"]),
    default="console",
    help="Output format",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show verbose output",
)
@click.option(
    "--skip-mcp",
    is_flag=True,
    help="Skip MCP protocol connection tests",
)
@click.option(
    "--auto-refresh",
    is_flag=True,
    help="Automatically refresh OAuth tokens if expired",
)
@click.option(
    "--reauth",
    is_flag=True,
    help="Re-authenticate via OAuth if tokens are invalid (opens browser)",
)
@click.option(
    "--server",
    "-s",
    "servers",
    multiple=True,
    help="Check specific server(s) only (can be repeated)",
)
@click.option(
    "--watch",
    "-w",
    is_flag=True,
    help="Continuously monitor servers",
)
@click.option(
    "--interval",
    "-i",
    default=60,
    type=int,
    help="Watch interval in seconds (default: 60)",
)
def check(
    config: Path | None,
    output_format: str,
    verbose: bool,
    skip_mcp: bool,
    auto_refresh: bool,
    reauth: bool,
    servers: tuple[str, ...],
    watch: bool,
    interval: int,
) -> None:
    """Run health check on all MCP servers."""
    asyncio.run(
        run_health_check(
            config_path=config,
            output_format=output_format,
            verbose=verbose,
            skip_mcp=skip_mcp,
            auto_refresh=auto_refresh,
            reauth=reauth,
            filter_servers=list(servers) if servers else None,
            watch=watch,
            interval=interval,
        )
    )


async def run_health_check(
    config_path: Path | None,
    output_format: str,
    verbose: bool,
    skip_mcp: bool,
    auto_refresh: bool,
    reauth: bool = False,
    filter_servers: list[str] | None = None,
    watch: bool = False,
    interval: int = 60,
) -> None:
    """Run the health check asynchronously.

    Args:
        config_path: Path to config file
        output_format: Output format (console/json)
        verbose: Verbose output
        skip_mcp: Skip MCP connection tests
        auto_refresh: Auto-refresh OAuth tokens
        reauth: Re-authenticate via OAuth if tokens are invalid
        filter_servers: Optional list of server names to check
        watch: Enable continuous monitoring
        interval: Interval between checks in watch mode
    """
    loader = ConfigLoader()
    generator = ReportGenerator(console)

    try:
        mcp_config = loader.load(config_path)
    except ConfigError as e:
        console.print(f"[red]Error loading config:[/] {e}")
        raise SystemExit(1) from e

    # Filter servers if specified
    servers_to_check: list[tuple[str, MCPServerConfig]] = []
    for server_name, server_config in mcp_config:
        if filter_servers is None or server_name in filter_servers:
            servers_to_check.append((server_name, server_config))

    if filter_servers and not servers_to_check:
        console.print(f"[red]No matching servers found:[/] {', '.join(filter_servers)}")
        console.print("Available servers: " + ", ".join(mcp_config.server_names()))
        raise SystemExit(1)

    if watch:
        await _run_watch_mode(
            servers_to_check,
            config_path,
            generator,
            verbose,
            skip_mcp,
            auto_refresh,
            reauth,
            interval,
        )
    else:
        report = await _run_single_check(
            servers_to_check,
            config_path,
            skip_mcp,
            auto_refresh,
            reauth,
        )
        # Generate output
        if output_format == "json":
            console.print(generator.generate_json(report))
        else:
            generator.generate_console(report, verbose=verbose)

        # Exit with appropriate code
        if report.overall_status.value == "unhealthy":
            raise SystemExit(1)


async def _run_single_check(
    servers: list[tuple[str, MCPServerConfig]],
    config_path: Path | None,
    skip_mcp: bool,
    auto_refresh: bool,
    reauth: bool = False,
) -> HealthReport:
    """Run a single health check on all servers (in parallel).

    Args:
        servers: List of (name, config) tuples
        config_path: Path to config file
        skip_mcp: Skip MCP connection tests
        auto_refresh: Auto-refresh OAuth tokens
        reauth: Re-authenticate via OAuth if tokens are invalid

    Returns:
        HealthReport with all results
    """
    report = HealthReport(config_path=str(config_path) if config_path else None)

    # Validate tokens in parallel
    logger.debug("Starting parallel token validation for %d servers", len(servers))
    validation_tasks = [
        _validate_server(name, config, skip_mcp, auto_refresh, reauth)
        for name, config in servers
    ]
    results = await asyncio.gather(*validation_tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, Exception):
            logger.error("Validation failed: %s", result)
            continue
        if isinstance(result, ServerHealth):
            report.add_server(result)

    return report


async def _validate_server(
    server_name: str,
    server_config: MCPServerConfig,
    skip_mcp: bool,
    auto_refresh: bool,
    reauth: bool = False,
) -> ServerHealth:
    """Validate a single server.

    Args:
        server_name: Name of the server
        server_config: Server configuration
        skip_mcp: Skip MCP connection tests
        auto_refresh: Auto-refresh OAuth tokens
        reauth: Re-authenticate via OAuth if tokens are invalid

    Returns:
        ServerHealth with validation results
    """
    health = ServerHealth(name=server_name)
    refresher = OAuthRefresher()
    notifier = UserNotifier()

    # Validate token
    validator = get_validator_for_server(server_name)
    if validator:
        health.token_result = await validator.validate(server_config)

        # Handle token refresh/reauth
        if health.token_result.needs_refresh():
            config_dir = server_config.get_env_var("MCP_REMOTE_CONFIG_DIR")

            if health.token_result.can_refresh and auto_refresh and config_dir:
                # Try auto-refresh for OAuth tokens
                refresh_result = await refresher.refresh_atlassian(Path(config_dir))
                health.refresh_attempted = True
                health.refresh_success = refresh_result.is_success()

                if refresh_result.is_success():
                    # Re-validate with new token
                    health.token_result = await validator.validate(server_config)
                elif refresh_result.needs_reauth() and reauth and config_dir:
                    # Refresh failed due to invalid token, try re-auth
                    reauth_result = await refresher.reauth_atlassian(Path(config_dir))
                    if reauth_result.is_success():
                        health.token_result = await validator.validate(server_config)
                        health.refresh_success = True
                    else:
                        health.action_required = reauth_result.message
                else:
                    health.action_required = refresh_result.message

            elif reauth and config_dir and "atlassian" in server_name.lower():
                # Direct reauth requested for Atlassian
                reauth_result = await refresher.reauth_atlassian(Path(config_dir))
                if reauth_result.is_success():
                    health.token_result = await validator.validate(server_config)
                    health.refresh_attempted = True
                    health.refresh_success = True
                else:
                    health.action_required = reauth_result.message
            else:
                # Notify user for manual refresh
                service_type = get_service_type(server_name)
                notification = notifier.notify(service_type)
                health.action_required = notification.title

    # Test MCP connection
    if not skip_mcp and (health.token_result is None or health.token_result.is_healthy()):
        mcp_client = MCPClient()
        health.connection_result = await mcp_client.health_check(server_name, server_config)

    return health


async def _run_watch_mode(
    servers: list[tuple[str, MCPServerConfig]],
    config_path: Path | None,
    generator: ReportGenerator,
    verbose: bool,
    skip_mcp: bool,
    auto_refresh: bool,
    reauth: bool,
    interval: int,
) -> None:
    """Run continuous monitoring mode.

    Args:
        servers: List of (name, config) tuples
        config_path: Path to config file
        generator: Report generator
        verbose: Verbose output
        skip_mcp: Skip MCP connection tests
        auto_refresh: Auto-refresh OAuth tokens
        reauth: Re-authenticate via OAuth if tokens are invalid
        interval: Seconds between checks
    """
    console.print(f"[bold]Watch mode enabled[/] - checking every {interval}s")
    console.print("Press Ctrl+C to stop\n")

    try:
        while True:
            # Clear screen for fresh output
            console.clear()
            console.print(f"[dim]Last check: {time.strftime('%Y-%m-%d %H:%M:%S')}[/]")
            console.print(f"[dim]Next check in {interval}s (Ctrl+C to stop)[/]\n")

            report = await _run_single_check(
                servers,
                config_path,
                skip_mcp,
                auto_refresh,
                reauth,
            )
            generator.generate_console(report, verbose=verbose)

            await asyncio.sleep(interval)
    except KeyboardInterrupt:
        console.print("\n[yellow]Watch mode stopped[/]")


@main.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, path_type=Path),
    help="Path to MCP config file",
)
def list_servers(config: Path | None) -> None:
    """List all configured MCP servers."""
    loader = ConfigLoader()

    try:
        mcp_config = loader.load(config)
    except ConfigError as e:
        console.print(f"[red]Error loading config:[/] {e}")
        raise SystemExit(1) from e

    console.print("\n[bold]Configured MCP Servers:[/]\n")
    for server_name, server_config in mcp_config:
        console.print(f"  [cyan]{server_name}[/]")
        console.print(f"    Command: {server_config.command}")
        console.print(f"    Args: {' '.join(server_config.args)}")
        if server_config.env:
            env_keys = list(server_config.env.keys())
            console.print(f"    Env vars: {', '.join(env_keys)}")
        console.print()


@main.command()
@click.argument("server_name")
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, path_type=Path),
    help="Path to MCP config file",
)
def refresh(server_name: str, config: Path | None) -> None:
    """Attempt to refresh token for a specific server."""
    asyncio.run(run_refresh(server_name, config))


async def run_refresh(server_name: str, config_path: Path | None) -> None:
    """Run token refresh for a server.

    Args:
        server_name: Name of the server
        config_path: Path to config file
    """
    loader = ConfigLoader()

    try:
        mcp_config = loader.load(config_path)
    except ConfigError as e:
        console.print(f"[red]Error loading config:[/] {e}")
        raise SystemExit(1) from e

    server_config = mcp_config.get_server(server_name)
    if not server_config:
        console.print(f"[red]Server not found:[/] {server_name}")
        raise SystemExit(1)

    # Check if this is an OAuth-refreshable server
    config_dir = server_config.get_env_var("MCP_REMOTE_CONFIG_DIR")
    if config_dir:
        refresher = OAuthRefresher()
        console.print(f"Attempting to refresh OAuth token for [cyan]{server_name}[/]...")
        result = await refresher.refresh_atlassian(Path(config_dir))

        if result.is_success():
            console.print("[green]✓ Token refreshed successfully[/]")
            if result.new_expires_at:
                console.print(f"  New expiration: {result.new_expires_at}")
        else:
            console.print(f"[red]✗ Refresh failed:[/] {result.message}")
            raise SystemExit(1)
    else:
        # Show manual refresh instructions
        notifier = UserNotifier()
        service_type = get_service_type(server_name)
        instructions = notifier.get_instructions(service_type)
        console.print(f"\n[yellow]{server_name} uses a non-refreshable token.[/]\n")
        console.print(instructions)


if __name__ == "__main__":
    main()
