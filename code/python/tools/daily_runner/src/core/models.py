"""
Pydantic data models for the Daily Standup Timer application.

This module defines all data structures used throughout the application,
including team configuration, meeting records, application settings, and
session recovery data.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

# =============================================================================
# Enums
# =============================================================================


class ParticipantStatus(str, Enum):
    """Status of a participant in a meeting."""

    PRESENT = "present"
    ABSENT = "absent"
    SKIPPED = "skipped"


class MeetingStatus(str, Enum):
    """Status of a meeting."""

    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MeetingState(str, Enum):
    """State machine states for meeting flow."""

    IDLE = "idle"
    TRANSITION = "transition"
    SPEAKING = "speaking"
    PAUSED = "paused"
    GRACE = "grace"
    OVERFLOW = "overflow"
    COMPLETED = "completed"


# =============================================================================
# Team Models
# =============================================================================


class DailyConfig(BaseModel):
    """Per-member daily standup configuration."""

    model_config = ConfigDict(strict=True)

    default_time_seconds: int = Field(
        default=180,
        ge=30,
        le=600,
        description="Default speaking time in seconds (30-600)",
    )
    active: bool = Field(
        default=True,
        description="Whether member participates in dailies",
    )


class TeamMember(BaseModel):
    """A team member who participates in daily standups."""

    model_config = ConfigDict(strict=True)

    id: str = Field(
        ...,
        min_length=1,
        max_length=50,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="Unique identifier (lowercase, alphanumeric with underscores)",
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Full name",
    )
    display_name: str = Field(
        ...,
        min_length=1,
        max_length=30,
        description="Short display name for UI",
    )
    email: EmailStr = Field(
        ...,
        description="Email address",
    )
    github: str | None = Field(
        default=None,
        max_length=50,
        description="GitHub username",
    )
    role: str | None = Field(
        default=None,
        max_length=100,
        description="Role or title",
    )
    specialization: list[str] = Field(
        default_factory=list,
        description="Areas of expertise",
    )
    daily_config: DailyConfig = Field(
        default_factory=DailyConfig,
        description="Daily standup settings",
    )


class ManagerInfo(BaseModel):
    """Manager or leader information."""

    model_config = ConfigDict(strict=True)

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class TeamInfo(BaseModel):
    """Team metadata."""

    model_config = ConfigDict(strict=True)

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Team name",
    )
    emoji: str = Field(
        default="👥",
        max_length=10,
        description="Team emoji/icon",
    )
    group_manager: ManagerInfo | None = Field(
        default=None,
        description="Group manager info",
    )
    team_leader: ManagerInfo | None = Field(
        default=None,
        description="Team leader info",
    )


class TeamFile(BaseModel):
    """Root model for team JSON files."""

    model_config = ConfigDict(strict=True)

    team: TeamInfo = Field(..., description="Team metadata")
    members: list[TeamMember] = Field(
        ...,
        min_length=1,
        description="List of team members",
    )

    def get_active_members(self) -> list[TeamMember]:
        """Return only active team members."""
        return [m for m in self.members if m.daily_config.active]

    def get_member_by_id(self, member_id: str) -> TeamMember | None:
        """Find a member by their ID."""
        for member in self.members:
            if member.id == member_id:
                return member
        return None

    def get_sorted_members(self, by: str = "display_name") -> list[TeamMember]:
        """Return members sorted by the specified field."""
        active = self.get_active_members()
        if by == "display_name":
            return sorted(active, key=lambda m: m.display_name.lower())
        if by == "name":
            return sorted(active, key=lambda m: m.name.lower())
        if by == "id":
            return sorted(active, key=lambda m: m.id)
        return active


# =============================================================================
# Configuration Models
# =============================================================================


class TimerConfig(BaseModel):
    """Timer-related configuration."""

    model_config = ConfigDict(strict=True)

    default_speaker_time_seconds: int = Field(
        default=180,
        ge=30,
        le=600,
        description="Default time per speaker (30-600 seconds)",
    )
    transition_time_seconds: int = Field(
        default=30,
        ge=0,
        le=120,
        description="Time between speakers (0-120 seconds)",
    )
    grace_period_seconds: int = Field(
        default=15,
        ge=0,
        le=60,
        description="Grace period after time expires (0-60 seconds)",
    )
    warning_threshold_seconds: int = Field(
        default=30,
        ge=5,
        le=120,
        description="When to show warning (5-120 seconds before end)",
    )
    overflow_period_seconds: int = Field(
        default=90,
        ge=5,
        le=300,
        description="Overflow period after grace (5-300 seconds)",
    )


class AlertConfig(BaseModel):
    """Alert and notification configuration."""

    model_config = ConfigDict(strict=True)

    warning_color: str = Field(
        default="#FFA500",
        pattern=r"^#[0-9A-Fa-f]{6}$",
        description="Warning state color (hex)",
    )
    overtime_color: str = Field(
        default="#FF0000",
        pattern=r"^#[0-9A-Fa-f]{6}$",
        description="Overtime state color (hex)",
    )
    flash_on_overtime: bool = Field(
        default=True,
        description="Whether to flash display on overtime",
    )


class HistoryConfig(BaseModel):
    """History storage configuration."""

    model_config = ConfigDict(strict=True)

    file_path: str = Field(
        default="data/history_{team_id}.json",
        description="Path pattern for history files",
    )
    max_entries: int = Field(
        default=2000,
        ge=100,
        le=10000,
        description="Maximum history entries (100-10000)",
    )


class RecoveryConfig(BaseModel):
    """Session recovery configuration."""

    model_config = ConfigDict(strict=True)

    enabled: bool = Field(
        default=True,
        description="Whether session recovery is enabled",
    )
    auto_save_interval_seconds: int = Field(
        default=5,
        ge=1,
        le=60,
        description="Auto-save interval (1-60 seconds)",
    )
    file_path: str = Field(
        default="data/.session_recovery.json",
        description="Recovery file path",
    )


class UIConfig(BaseModel):
    """UI-related configuration."""

    model_config = ConfigDict(strict=True)

    theme: str = Field(
        default="light",
        pattern=r"^(light|dark)$",
        description="UI theme (light or dark)",
    )
    show_avatars: bool = Field(
        default=False,
        description="Whether to show member avatars",
    )


class TeamsConfig(BaseModel):
    """Teams directory configuration."""

    model_config = ConfigDict(strict=True)

    directory: str = Field(
        default="teams",
        description="Directory containing team JSON files",
    )
    default_team: str = Field(
        default="imagine_dragons",
        min_length=1,
        description="Default team ID to load",
    )


class AppConfig(BaseModel):
    """Root application configuration model."""

    model_config = ConfigDict(strict=True)

    version: str = Field(
        default="1.0",
        description="Configuration version",
    )
    timer: TimerConfig = Field(
        default_factory=TimerConfig,
        description="Timer settings",
    )
    alerts: AlertConfig = Field(
        default_factory=AlertConfig,
        description="Alert settings",
    )
    history: HistoryConfig = Field(
        default_factory=HistoryConfig,
        description="History settings",
    )
    recovery: RecoveryConfig = Field(
        default_factory=RecoveryConfig,
        description="Recovery settings",
    )
    ui: UIConfig = Field(
        default_factory=UIConfig,
        description="UI settings",
    )
    teams: TeamsConfig = Field(
        default_factory=TeamsConfig,
        description="Teams settings",
    )
    default_order: str = Field(
        default="alphabetical",
        pattern=r"^(alphabetical|custom)$",
        description="Default speaker order",
    )

    @classmethod
    def create_default(cls) -> "AppConfig":
        """Create a configuration with all default values."""
        return cls()


# =============================================================================
# Meeting History Models
# =============================================================================


class ParticipantRecord(BaseModel):
    """Record of a participant's time in a meeting."""

    model_config = ConfigDict(strict=False)  # Allow string-to-enum coercion for JSON loading

    member_id: str = Field(..., description="Team member ID")
    display_name: str = Field(..., description="Display name at time of meeting")
    status: ParticipantStatus = Field(..., description="Participation status")
    allocated_time_seconds: int = Field(
        ...,
        ge=0,
        description="Time allocated to this participant",
    )
    actual_time_seconds: float = Field(
        ...,
        ge=0,
        description="Actual time used",
    )
    overtime_seconds: float = Field(
        default=0,
        ge=0,
        description="Time over allocated limit",
    )
    order_position: int | None = Field(
        default=None,
        ge=1,
        description="Position in speaker order (1-indexed)",
    )


class MeetingRecord(BaseModel):
    """Record of a completed meeting."""

    model_config = ConfigDict(strict=False)  # Allow string-to-enum coercion for JSON loading

    id: str = Field(..., description="Unique meeting ID (ISO timestamp)")
    date: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Meeting date (YYYY-MM-DD)",
    )
    start_time: str = Field(
        ...,
        pattern=r"^\d{2}:\d{2}:\d{2}$",
        description="Start time (HH:MM:SS)",
    )
    end_time: str = Field(
        ...,
        pattern=r"^\d{2}:\d{2}:\d{2}$",
        description="End time (HH:MM:SS)",
    )
    total_duration_seconds: float = Field(
        ...,
        ge=0,
        description="Total meeting duration",
    )
    expected_duration_seconds: int = Field(
        ...,
        ge=0,
        description="Expected duration based on participants",
    )
    status: MeetingStatus = Field(..., description="Meeting completion status")
    participants: list[ParticipantRecord] = Field(
        default_factory=list,
        description="Participant records",
    )
    notes: str = Field(
        default="",
        max_length=1000,
        description="Optional meeting notes",
    )
    team_id: str = Field(
        default="",
        description="Team ID for this meeting",
    )

    @field_validator("id")
    @classmethod
    def validate_id_format(cls, v: str) -> str:
        """Validate that ID looks like an ISO timestamp."""
        # Allow flexible ISO-like formats
        if not v or len(v) < 10:
            raise ValueError("ID must be a valid timestamp string")
        return v

    def get_total_overtime(self) -> float:
        """Calculate total overtime across all participants."""
        return sum(p.overtime_seconds for p in self.participants)

    def get_present_count(self) -> int:
        """Count participants who were present."""
        return sum(1 for p in self.participants if p.status == ParticipantStatus.PRESENT)

    def get_absent_count(self) -> int:
        """Count participants who were absent."""
        return sum(1 for p in self.participants if p.status == ParticipantStatus.ABSENT)


class HistoryFile(BaseModel):
    """Root model for history JSON files."""

    model_config = ConfigDict(strict=False)  # Allow string-to-enum coercion for JSON loading

    version: str = Field(default="1.0", description="History file version")
    entries: list[MeetingRecord] = Field(
        default_factory=list,
        description="Meeting history entries",
    )

    def add_entry(self, record: MeetingRecord, max_entries: int = 2000) -> None:
        """Add a meeting record, enforcing max entries limit."""
        self.entries.append(record)
        if len(self.entries) > max_entries:
            # Remove oldest entries (FIFO)
            self.entries = self.entries[-max_entries:]

    def get_entries_by_date_range(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[MeetingRecord]:
        """Filter entries by date range."""
        filtered = self.entries
        if start_date:
            filtered = [e for e in filtered if e.date >= start_date]
        if end_date:
            filtered = [e for e in filtered if e.date <= end_date]
        return filtered


# =============================================================================
# Session Recovery Models
# =============================================================================


class CompletedSpeakerRecord(BaseModel):
    """Record of a speaker who has completed their turn."""

    model_config = ConfigDict(strict=True)

    member_id: str = Field(..., description="Team member ID")
    actual_time_seconds: float = Field(..., ge=0, description="Time used")


class SessionRecovery(BaseModel):
    """Session state for crash recovery."""

    # Not strict to allow enum deserialization from strings
    model_config = ConfigDict(strict=False, use_enum_values=False)

    session_id: str = Field(..., description="Session ID (ISO timestamp)")
    team_id: str = Field(..., description="Team ID for this session")
    started_at: str = Field(..., description="Session start timestamp")
    last_updated: str = Field(..., description="Last update timestamp")
    global_elapsed_seconds: float = Field(
        ...,
        ge=0,
        description="Total elapsed time",
    )
    current_speaker_index: int = Field(
        ...,
        ge=0,
        description="Index of current speaker in queue",
    )
    speaker_order: list[str] = Field(
        ...,
        description="Ordered list of member IDs",
    )
    completed_speakers: list[CompletedSpeakerRecord] = Field(
        default_factory=list,
        description="Speakers who have finished",
    )
    current_speaker_elapsed_seconds: float = Field(
        default=0,
        ge=0,
        description="Current speaker's elapsed time",
    )
    is_in_transition: bool = Field(
        default=False,
        description="Whether in transition period",
    )
    is_paused: bool = Field(
        default=False,
        description="Whether meeting is paused",
    )
    absent_members: list[str] = Field(
        default_factory=list,
        description="Member IDs marked as absent",
    )
    state: MeetingState = Field(
        default=MeetingState.IDLE,
        description="Current meeting state",
    )

    @classmethod
    def create_new(
        cls,
        team_id: str,
        speaker_order: list[str],
    ) -> "SessionRecovery":
        """Create a new recovery session."""
        now = datetime.now().isoformat()
        return cls(
            session_id=now,
            team_id=team_id,
            started_at=now,
            last_updated=now,
            global_elapsed_seconds=0,
            current_speaker_index=0,
            speaker_order=speaker_order,
            completed_speakers=[],
            current_speaker_elapsed_seconds=0,
            is_in_transition=False,
            is_paused=False,
            absent_members=[],
            state=MeetingState.IDLE,
        )

    def update_timestamp(self) -> None:
        """Update the last_updated timestamp."""
        self.last_updated = datetime.now().isoformat()

    def to_json_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return self.model_dump(mode="json")

    @classmethod
    def from_json_dict(cls, data: dict[str, Any]) -> "SessionRecovery":
        """Create instance from JSON dictionary."""
        return cls.model_validate(data)
