"""User notification for manual token refresh."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ServiceType(Enum):
    """Type of service requiring token refresh."""

    GITHUB = "github"
    SLACK = "slack"
    ATLASSIAN = "atlassian"
    UNKNOWN = "unknown"


@dataclass
class RefreshNotification:
    """Notification for user about token refresh requirement.

    Attributes:
        service: The service requiring refresh
        title: Short title for the notification
        message: Detailed message with instructions
        url: URL to visit for token generation
        steps: Step-by-step instructions
    """

    service: ServiceType
    title: str
    message: str
    url: str
    steps: list[str]

    def format_console(self) -> str:
        """Format notification for console output.

        Returns:
            Formatted string for terminal display
        """
        lines = [
            f"⚠️  {self.title}",
            "",
            self.message,
            "",
            f"URL: {self.url}",
            "",
            "Steps:",
        ]
        for i, step in enumerate(self.steps, 1):
            lines.append(f"  {i}. {step}")
        return "\n".join(lines)


class UserNotifier:
    """Generates notifications for manual token refresh.

    For tokens that cannot be auto-refreshed (PATs, bot tokens),
    this class generates user-friendly instructions for regeneration.

    Example:
        notifier = UserNotifier()
        notification = notifier.notify(ServiceType.GITHUB)
        print(notification.format_console())
    """

    def notify(self, service: ServiceType) -> RefreshNotification:
        """Generate notification for a service.

        Args:
            service: The service type

        Returns:
            RefreshNotification with instructions
        """
        if service == ServiceType.GITHUB:
            return self.notify_github()
        elif service == ServiceType.SLACK:
            return self.notify_slack()
        elif service == ServiceType.ATLASSIAN:
            return self.notify_atlassian()
        else:
            return self._unknown_service(service)

    def notify_github(self) -> RefreshNotification:
        """Generate GitHub PAT refresh notification.

        Returns:
            RefreshNotification for GitHub
        """
        return RefreshNotification(
            service=ServiceType.GITHUB,
            title="GitHub Personal Access Token Expired",
            message=(
                "Your GitHub Personal Access Token (PAT) has expired or is invalid. "
                "PATs cannot be auto-refreshed and must be regenerated manually."
            ),
            url="https://github.com/settings/tokens",
            steps=[
                "Go to GitHub Settings → Developer settings → Personal access tokens",
                "Click 'Generate new token' (or regenerate existing)",
                "Select required scopes: repo, read:user (minimum)",
                "Copy the new token",
                "Update GITHUB_PERSONAL_ACCESS_TOKEN in your MCP config",
                "Restart Cursor to apply changes",
            ],
        )

    def notify_slack(self) -> RefreshNotification:
        """Generate Slack bot token refresh notification.

        Returns:
            RefreshNotification for Slack
        """
        return RefreshNotification(
            service=ServiceType.SLACK,
            title="Slack Bot Token Invalid",
            message=(
                "Your Slack Bot Token is invalid, revoked, or expired. "
                "Bot tokens must be regenerated through the Slack App settings."
            ),
            url="https://api.slack.com/apps",
            steps=[
                "Go to api.slack.com/apps and select your app",
                "Navigate to 'OAuth & Permissions'",
                "Click 'Reinstall to Workspace' to generate new tokens",
                "Copy the 'Bot User OAuth Token' (starts with xoxb-)",
                "Update SLACK_BOT_TOKEN in your MCP config",
                "Restart Cursor to apply changes",
            ],
        )

    def notify_atlassian(self) -> RefreshNotification:
        """Generate Atlassian OAuth refresh notification.

        This is used when auto-refresh fails.

        Returns:
            RefreshNotification for Atlassian
        """
        return RefreshNotification(
            service=ServiceType.ATLASSIAN,
            title="Atlassian OAuth Token Refresh Failed",
            message=(
                "Failed to auto-refresh your Atlassian OAuth token. "
                "The easiest fix is to toggle the MCP server in Cursor."
            ),
            url="https://mcp.atlassian.com",
            steps=[
                "Open Cursor Settings → MCP Servers",
                "Toggle OFF the Atlassian MCP server",
                "Toggle it back ON",
                "Complete OAuth in browser when prompted",
                "Or run: mcp-health check --server perimeter81-atlassian --reauth",
            ],
        )

    def _unknown_service(self, service: ServiceType) -> RefreshNotification:
        """Generate notification for unknown service.

        Args:
            service: The unknown service type

        Returns:
            Generic RefreshNotification
        """
        return RefreshNotification(
            service=service,
            title=f"Token Refresh Required: {service.value}",
            message=(
                f"The token for {service.value} needs to be refreshed. "
                "Please check the service documentation for instructions."
            ),
            url="",
            steps=[
                "Check the service's documentation",
                "Generate or refresh the required token",
                "Update your MCP configuration",
                "Restart Cursor",
            ],
        )

    def get_instructions(self, service: ServiceType) -> str:
        """Get formatted instructions as a string.

        Convenience method for getting just the text instructions.

        Args:
            service: The service type

        Returns:
            Formatted instruction string
        """
        notification = self.notify(service)
        return notification.format_console()
