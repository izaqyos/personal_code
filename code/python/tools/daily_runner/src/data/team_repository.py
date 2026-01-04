"""
Team repository for managing team member data.

This module provides access to team configuration files,
including listing available teams and loading team members.
"""

import json
import logging
from pathlib import Path

from src.core.models import TeamFile, TeamMember

logger = logging.getLogger(__name__)


class TeamNotFoundError(Exception):
    """Raised when a requested team does not exist."""

    pass


class TeamRepository:
    """
    Repository for accessing team data.

    Handles loading team files from the teams directory and
    provides methods for querying team members.
    """

    def __init__(self, teams_dir: Path | None = None) -> None:
        """
        Initialize the team repository.

        Args:
            teams_dir: Path to teams directory. Uses default if not provided.
        """
        self._teams_dir = teams_dir or Path("teams")
        self._cache: dict[str, TeamFile] = {}

    @property
    def teams_dir(self) -> Path:
        """Return the teams directory path."""
        return self._teams_dir

    def list_teams(self) -> list[str]:
        """
        List all available team IDs.

        Returns:
            List of team IDs (filenames without .json extension).
        """
        if not self._teams_dir.exists():
            logger.warning(f"Teams directory not found: {self._teams_dir}")
            return []

        teams = []
        for path in self._teams_dir.glob("*.json"):
            team_id = path.stem
            teams.append(team_id)

        return sorted(teams)

    def load_team(self, team_id: str, use_cache: bool = True) -> TeamFile:
        """
        Load a team by ID.

        Args:
            team_id: The team identifier (filename without .json).
            use_cache: Whether to use cached data if available.

        Returns:
            The loaded TeamFile.

        Raises:
            TeamNotFoundError: If the team file doesn't exist.
            ValueError: If the team file is invalid.
        """
        if use_cache and team_id in self._cache:
            return self._cache[team_id]

        team_path = self._teams_dir / f"{team_id}.json"

        if not team_path.exists():
            raise TeamNotFoundError(f"Team not found: {team_id}")

        try:
            data = json.loads(team_path.read_text())
            team = TeamFile.model_validate(data)
            self._cache[team_id] = team
            logger.debug(f"Loaded team: {team_id}")
            return team
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in team file {team_id}: {e}") from e
        except Exception as e:
            raise ValueError(f"Error loading team {team_id}: {e}") from e

    def get_team_name(self, team_id: str) -> str:
        """
        Get the display name of a team.

        Args:
            team_id: The team identifier.

        Returns:
            The team's display name.
        """
        team = self.load_team(team_id)
        return team.team.name

    def get_active_members(self, team_id: str) -> list[TeamMember]:
        """
        Get active members of a team.

        Args:
            team_id: The team identifier.

        Returns:
            List of active team members.
        """
        team = self.load_team(team_id)
        return team.get_active_members()

    def get_member_by_id(self, team_id: str, member_id: str) -> TeamMember | None:
        """
        Find a specific member in a team.

        Args:
            team_id: The team identifier.
            member_id: The member identifier.

        Returns:
            The TeamMember or None if not found.
        """
        team = self.load_team(team_id)
        return team.get_member_by_id(member_id)

    def get_sorted_members(
        self,
        team_id: str,
        order: str = "display_name",
        active_only: bool = True,
    ) -> list[TeamMember]:
        """
        Get members sorted by the specified field.

        Args:
            team_id: The team identifier.
            order: Sort field ("display_name", "name", or "id").
            active_only: Whether to include only active members.

        Returns:
            Sorted list of team members.
        """
        team = self.load_team(team_id)
        members = team.get_active_members() if active_only else team.members

        if order == "display_name":
            return sorted(members, key=lambda m: m.display_name.lower())
        if order == "name":
            return sorted(members, key=lambda m: m.name.lower())
        if order == "id":
            return sorted(members, key=lambda m: m.id)

        return members

    def get_member_ids(self, team_id: str, active_only: bool = True) -> list[str]:
        """
        Get list of member IDs for a team.

        Args:
            team_id: The team identifier.
            active_only: Whether to include only active members.

        Returns:
            List of member IDs.
        """
        members = self.get_sorted_members(team_id, active_only=active_only)
        return [m.id for m in members]

    def clear_cache(self) -> None:
        """Clear the team cache."""
        self._cache.clear()

    def team_exists(self, team_id: str) -> bool:
        """
        Check if a team exists.

        Args:
            team_id: The team identifier.

        Returns:
            True if the team file exists.
        """
        team_path = self._teams_dir / f"{team_id}.json"
        return team_path.exists()
