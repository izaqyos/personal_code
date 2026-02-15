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
from mcp_health.refresh.cooldown import ReauthCooldown
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
    "--skip-mcp/--with-mcp",
    default=True,
    help="Skip MCP protocol connection tests (default: skip)",
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
    "--force",
    is_flag=True,
    help="Bypass cooldown restrictions for --reauth",
)
@click.option(
    "--cooldown-status",
    is_flag=True,
    help="Show re-auth cooldown status",
)
@click.option(
    "--reset-cooldown",
    "reset_cooldown_server",
    default=None,
    help="Reset cooldown for a server (or 'all' for all servers)",
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
    force: bool,
    cooldown_status: bool,
    reset_cooldown_server: str | None,
    servers: tuple[str, ...],
    watch: bool,
    interval: int,
) -> None:
    """Run health check on all MCP servers."""
    cooldown = ReauthCooldown()

    # Handle cooldown status display
    if cooldown_status:
        console.print(cooldown.status_summary())
        return

    # Handle cooldown reset
    if reset_cooldown_server:
        server_to_reset = None if reset_cooldown_server.lower() == "all" else reset_cooldown_server
        reset_servers = cooldown.reset(server_to_reset)
        if reset_servers:
            console.print(f"[green]✓ Reset cooldown for:[/] {', '.join(reset_servers)}")
        else:
            console.print("[yellow]No cooldown data to reset.[/]")
        return

    asyncio.run(
        run_health_check(
            config_path=config,
            output_format=output_format,
            verbose=verbose,
            skip_mcp=skip_mcp,
            auto_refresh=auto_refresh,
            reauth=reauth,
            force_reauth=force,
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
    force_reauth: bool = False,
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
        force_reauth: Bypass cooldown restrictions for reauth
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
            force_reauth,
            interval,
        )
    else:
        report = await _run_single_check(
            servers_to_check,
            config_path,
            skip_mcp,
            auto_refresh,
            reauth,
            force_reauth,
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
    force_reauth: bool = False,
) -> HealthReport:
    """Run a single health check on all servers (in parallel).

    Args:
        servers: List of (name, config) tuples
        config_path: Path to config file
        skip_mcp: Skip MCP connection tests
        auto_refresh: Auto-refresh OAuth tokens
        reauth: Re-authenticate via OAuth if tokens are invalid
        force_reauth: Bypass cooldown restrictions for reauth

    Returns:
        HealthReport with all results
    """
    report = HealthReport(config_path=str(config_path) if config_path else None)

    # Validate tokens in parallel
    logger.debug("Starting parallel token validation for %d servers", len(servers))
    validation_tasks = [
        _validate_server(name, config, skip_mcp, auto_refresh, reauth, force_reauth)
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
    force_reauth: bool = False,
) -> ServerHealth:
    """Validate a single server.

    Args:
        server_name: Name of the server
        server_config: Server configuration
        skip_mcp: Skip MCP connection tests
        auto_refresh: Auto-refresh OAuth tokens
        reauth: Re-authenticate via OAuth if tokens are invalid
        force_reauth: Bypass cooldown restrictions for reauth

    Returns:
        ServerHealth with validation results
    """
    health = ServerHealth(name=server_name)
    refresher = OAuthRefresher()
    notifier = UserNotifier()
    cooldown = ReauthCooldown()

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
                    # Refresh failed due to invalid token, try re-auth with cooldown check
                    can_reauth, cooldown_reason = cooldown.can_reauth(server_name)
                    if can_reauth or force_reauth:
                        cooldown.record_attempt(server_name)
                        reauth_result = await refresher.reauth_atlassian(Path(config_dir))
                        if reauth_result.is_success():
                            health.token_result = await validator.validate(server_config)
                            health.refresh_success = True
                        else:
                            health.action_required = reauth_result.message
                    else:
                        health.action_required = f"Cooldown active: {cooldown_reason}"
                else:
                    health.action_required = refresh_result.message

            elif reauth and config_dir and "atlassian" in server_name.lower():
                # Direct reauth requested for Atlassian - check cooldown
                can_reauth, cooldown_reason = cooldown.can_reauth(server_name)
                if can_reauth or force_reauth:
                    cooldown.record_attempt(server_name)
                    reauth_result = await refresher.reauth_atlassian(Path(config_dir))
                    if reauth_result.is_success():
                        health.token_result = await validator.validate(server_config)
                        health.refresh_attempted = True
                        health.refresh_success = True
                    else:
                        health.action_required = reauth_result.message
                else:
                    health.action_required = f"Cooldown active: {cooldown_reason}"
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
    force_reauth: bool,
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
        force_reauth: Bypass cooldown restrictions for reauth
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
                force_reauth,
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


@main.command(name="wipe-reauth")
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, path_type=Path),
    help="Path to MCP config file",
)
@click.option(
    "--server",
    "-s",
    "server_name",
    default=None,
    help="Specific server to wipe (default: all Atlassian servers)",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Skip confirmation prompt AND bypass cooldown",
)
def wipe_reauth(config: Path | None, server_name: str | None, force: bool) -> None:
    """Completely wipe OAuth tokens and re-authenticate via browser.

    This is a nuclear option for when tokens are corrupted or in a bad state.
    It removes ALL OAuth-related files and triggers a fresh authentication.

    Note: Subject to cooldown restrictions unless --force is used.

    Example:
        mcp-health wipe-reauth -s perimeter81-atlassian
        mcp-health wipe-reauth -s perimeter81-atlassian --force
    """
    asyncio.run(run_wipe_reauth(config, server_name, force))


async def run_wipe_reauth(
    config_path: Path | None,
    server_name: str | None,
    force: bool,
) -> None:
    """Run the wipe and re-authentication flow.

    Args:
        config_path: Path to config file
        server_name: Specific server name or None for all Atlassian servers
        force: Skip confirmation prompt AND bypass cooldown
    """
    loader = ConfigLoader()
    refresher = OAuthRefresher()
    cooldown = ReauthCooldown()

    # Check cooldown unless force is used
    if not force and server_name:
        can_reauth, cooldown_reason = cooldown.can_reauth(server_name)
        if not can_reauth:
            console.print(f"[red]Cooldown active:[/] {cooldown_reason}")
            console.print("[dim]Use --force to bypass cooldown restrictions.[/]")
            raise SystemExit(1)

    try:
        mcp_config = loader.load(config_path)
    except ConfigError as e:
        console.print(f"[red]Error loading config:[/] {e}")
        raise SystemExit(1) from e

    # Find Atlassian servers with OAuth config
    atlassian_servers: list[tuple[str, Path]] = []
    for name, server_config in mcp_config:
        is_atlassian = "atlassian" in name.lower() or "jira" in name.lower()
        config_dir = server_config.get_env_var("MCP_REMOTE_CONFIG_DIR")

        if config_dir and is_atlassian:
            if server_name is None or name == server_name:
                atlassian_servers.append((name, Path(config_dir)))

    if not atlassian_servers:
        if server_name:
            console.print(f"[red]Server not found or not an OAuth server:[/] {server_name}")
            console.print("\nAvailable OAuth servers:")
            for name, server_config in mcp_config:
                if server_config.get_env_var("MCP_REMOTE_CONFIG_DIR"):
                    console.print(f"  - {name}")
        else:
            console.print("[yellow]No Atlassian OAuth servers found in config.[/]")
        raise SystemExit(1)

    # Show what will be wiped
    console.print("\n[bold red]⚠️  WIPE AND RE-AUTHENTICATE[/]\n")
    console.print("This will completely remove all OAuth tokens and force re-authentication.\n")
    console.print("[bold]Servers to wipe:[/]")
    for name, config_dir in atlassian_servers:
        console.print(f"  • [cyan]{name}[/]")
        console.print(f"    Config dir: [dim]{config_dir}[/]")

    console.print("\n[bold]Files to remove:[/]")
    console.print("  • Token files (*_tokens.json)")
    console.print("  • Client registration (*_client_info.json)")
    console.print("  • PKCE verifiers (*_code_verifier.txt)")
    console.print("  • Lock files (*_lock.json)")

    # Confirm unless --force
    if not force:
        console.print("")
        if not click.confirm("Proceed with wipe and re-authentication?", default=False):
            console.print("[yellow]Cancelled.[/]")
            raise SystemExit(0)

    # Wipe tokens for each server
    console.print("\n[bold]Wiping tokens...[/]")
    for name, config_dir in atlassian_servers:
        console.print(f"\n  [{name}]")
        removed_files = refresher.wipe_all_tokens(config_dir)
        if removed_files:
            for f in removed_files:
                console.print(f"    [red]✗[/] Removed: [dim]{f}[/]")
        else:
            console.print("    [dim]No token files found[/]")

    # Re-authenticate
    console.print("\n[bold]Starting re-authentication...[/]")
    console.print("[dim]A browser will open for you to log in to Atlassian.[/]\n")

    for name, config_dir in atlassian_servers:
        console.print(f"[bold cyan]Re-authenticating {name}...[/]")
        # Record the reauth attempt
        cooldown.record_attempt(name)
        result = await refresher.reauth_atlassian(config_dir)

        if result.is_success():
            console.print(f"[green]✓ {result.message}[/]")
        else:
            console.print(f"[red]✗ {result.message}[/]")
            console.print("\n[yellow]Manual steps if re-auth failed:[/]")
            console.print("  1. Open Cursor Settings → MCP Servers")
            console.print("  2. Toggle OFF the Atlassian MCP server")
            console.print("  3. Toggle it back ON")
            console.print("  4. Complete OAuth in browser when prompted")
            raise SystemExit(1)

    console.print("\n[green bold]✓ Re-authentication complete![/]")
    console.print("\n[dim]Note: You may need to toggle the MCP server in Cursor Settings")
    console.print("if Cursor doesn't pick up the new tokens automatically.[/]")


@main.command()
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be killed without actually killing",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Kill processes without confirmation",
)
def cleanup(dry_run: bool, force: bool) -> None:
    """Kill stale mcp-remote processes causing auth popup spam.

    Use when you see multiple browser tabs opening for Atlassian OAuth,
    "localhost refused to connect" errors, or excessive auth prompts.

    Example:
        mcp-health cleanup         # Interactive cleanup
        mcp-health cleanup --force # Skip confirmation
        mcp-health cleanup --dry-run  # Preview only
    """
    import subprocess

    console.print("\n[bold]MCP Process Cleanup[/]\n")

    # Find mcp-remote processes
    try:
        result = subprocess.run(
            ["pgrep", "-f", "mcp-remote"],
            capture_output=True,
            text=True,
        )
        pids = result.stdout.strip().split("\n") if result.stdout.strip() else []
    except FileNotFoundError:
        # pgrep not available, try ps approach
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True,
            text=True,
        )
        lines = [line for line in result.stdout.split("\n") if "mcp-remote" in line and "grep" not in line]
        pids = [line.split()[1] for line in lines if line]

    if not pids:
        console.print("[green]✓ No stale mcp-remote processes found.[/]")
        console.print("[dim]Everything looks clean![/]")
        return

    # Get process details
    console.print(f"[yellow]Found {len(pids)} mcp-remote process(es):[/]\n")
    
    try:
        ps_result = subprocess.run(
            ["ps", "-p", ",".join(pids), "-o", "pid,etime,command"],
            capture_output=True,
            text=True,
        )
        if ps_result.stdout:
            for line in ps_result.stdout.strip().split("\n"):
                if "PID" in line:
                    console.print(f"  [dim]{line}[/]")
                else:
                    console.print(f"  {line[:100]}{'...' if len(line) > 100 else ''}")
    except Exception:
        for pid in pids:
            console.print(f"  PID: {pid}")

    console.print("")

    if dry_run:
        console.print("[yellow]Dry run - no processes killed.[/]")
        console.print("[dim]Run without --dry-run to kill these processes.[/]")
        return

    # Confirm unless --force
    if not force:
        if not click.confirm("Kill all mcp-remote processes?", default=True):
            console.print("[yellow]Cancelled.[/]")
            return

    # Kill processes
    try:
        result = subprocess.run(
            ["pkill", "-f", "mcp-remote"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            console.print(f"[green]✓ Killed {len(pids)} mcp-remote process(es).[/]")
        else:
            # pkill returns 1 if no processes found (already killed)
            console.print("[green]✓ Processes terminated.[/]")
    except FileNotFoundError:
        # pkill not available, use kill
        for pid in pids:
            try:
                subprocess.run(["kill", pid], check=True)
            except subprocess.CalledProcessError:
                pass
        console.print(f"[green]✓ Killed {len(pids)} mcp-remote process(es).[/]")

    console.print("\n[bold]Next steps:[/]")
    console.print("  1. Your next MCP call will spawn fresh processes")
    console.print("  2. You'll get a one-time browser auth prompt")
    console.print("  3. Subsequent calls will use cached tokens")
    console.print("\n[dim]Tip: Run 'mcp-health check' to verify MCP servers are working.[/]")


@main.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, path_type=Path),
    help="Path to MCP config file",
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output as JSON",
)
def status(config: Path | None, output_json: bool) -> None:
    """Quick one-liner status: server health + cooldown state.

    Designed for agents to call frequently without side effects.

    Example:
        mcp-health status
        mcp-health status --json
    """
    asyncio.run(run_status(config, output_json))


async def run_status(config_path: Path | None, output_json: bool) -> None:
    """Run the quick status check.

    Args:
        config_path: Path to config file
        output_json: Output as JSON
    """
    import json as json_module

    loader = ConfigLoader()
    cooldown = ReauthCooldown()

    try:
        mcp_config = loader.load(config_path)
    except ConfigError as e:
        if output_json:
            console.print(json_module.dumps({"error": str(e)}))
        else:
            console.print(f"[red]Error loading config:[/] {e}")
        raise SystemExit(1) from e

    # Quick health check - just token validation, no MCP spawn
    results: dict[str, dict] = {}
    for server_name, server_config in mcp_config:
        validator = get_validator_for_server(server_name)
        if validator:
            token_result = await validator.validate(server_config)
            results[server_name] = {
                "token_status": token_result.status.value,
                "healthy": token_result.is_healthy(),
            }
        else:
            results[server_name] = {
                "token_status": "unknown",
                "healthy": None,
            }

    # Get cooldown status
    cooldown_data = cooldown.status()
    cooldown_results: dict[str, dict] = {}
    for server, cd_status in cooldown_data.items():
        cooldown_results[server] = {
            "can_reauth": cd_status.can_reauth,
            "attempts_in_window": cd_status.attempts_in_window,
            "seconds_until_allowed": cd_status.seconds_until_allowed,
        }

    if output_json:
        output = {
            "servers": results,
            "cooldown": cooldown_results,
        }
        console.print(json_module.dumps(output, indent=2))
    else:
        # One-liner format
        parts = []
        all_healthy = True
        for name, data in results.items():
            status_icon = "✓" if data["healthy"] else "✗"
            parts.append(f"{name}: {status_icon}")
            if not data["healthy"]:
                all_healthy = False

        overall = "[green]HEALTHY[/]" if all_healthy else "[red]UNHEALTHY[/]"
        console.print(f"MCP Status: {overall} | " + " | ".join(parts))

        # Show cooldown if any
        if cooldown_results:
            cd_parts = []
            for server, cd in cooldown_results.items():
                if cd["can_reauth"]:
                    cd_parts.append(f"{server}: ok")
                else:
                    cd_parts.append(f"{server}: wait {cd['seconds_until_allowed']}s")
            console.print(f"[dim]Cooldown: {' | '.join(cd_parts)}[/]")


if __name__ == "__main__":
    main()
