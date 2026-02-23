"""
Tests for Pydantic data models.

Test IDs:
- 2.T1: Valid team member model creation
- 2.T2: Invalid team member rejected (missing required fields)
- 2.T3: Config model with defaults
- 2.T4: Meeting record serialization round-trip
- 2.T5: Session recovery model validation
"""

import json

import pytest
from pydantic import ValidationError

from src.core.models import (
    AlertConfig,
    AppConfig,
    CompletedSpeakerRecord,
    DailyConfig,
    HistoryConfig,
    HistoryFile,
    ManagerInfo,
    MeetingRecord,
    MeetingState,
    MeetingStatus,
    ParticipantRecord,
    ParticipantStatus,
    RecoveryConfig,
    SessionRecovery,
    TeamFile,
    TeamInfo,
    TeamMember,
    TeamsConfig,
    TimerConfig,
    UIConfig,
)

# =============================================================================
# Test 2.T1: Valid team member model creation
# =============================================================================


class TestTeamMemberCreation:
    """Test valid TeamMember model creation."""

    def test_create_minimal_team_member(self) -> None:
        """Test creating a team member with minimal required fields."""
        member = TeamMember(
            id="alice",
            name="Alice Anderson",
            display_name="Alice",
            email="alice@example.com",
        )
        assert member.id == "alice"
        assert member.name == "Alice Anderson"
        assert member.display_name == "Alice"
        assert member.email == "alice@example.com"

    def test_create_full_team_member(self) -> None:
        """Test creating a team member with all fields."""
        member = TeamMember(
            id="bob",
            name="Bob Brown",
            display_name="Bob",
            email="bob@example.com",
            github="bob-dev",
            role="Senior Developer",
            specialization=["backend", "database"],
            daily_config=DailyConfig(default_time_seconds=240, active=True),
        )
        assert member.github == "bob-dev"
        assert member.role == "Senior Developer"
        assert member.specialization == ["backend", "database"]
        assert member.daily_config.default_time_seconds == 240

    def test_team_member_default_daily_config(self) -> None:
        """Test that DailyConfig has correct defaults."""
        member = TeamMember(
            id="carol",
            name="Carol Clark",
            display_name="Carol",
            email="carol@example.com",
        )
        assert member.daily_config.default_time_seconds == 180
        assert member.daily_config.active is True

    def test_daily_config_custom_values(self) -> None:
        """Test DailyConfig with custom values."""
        config = DailyConfig(default_time_seconds=300, active=False)
        assert config.default_time_seconds == 300
        assert config.active is False


class TestTeamFileModel:
    """Test TeamFile model and methods."""

    @pytest.fixture
    def sample_team_file(self) -> TeamFile:
        """Create a sample TeamFile for testing."""
        return TeamFile(
            team=TeamInfo(
                name="Test Team",
                emoji="🧪",
                group_manager=ManagerInfo(name="Manager", email="mgr@test.com"),
                team_leader=ManagerInfo(name="Leader", email="lead@test.com"),
            ),
            members=[
                TeamMember(
                    id="alice",
                    name="Alice Anderson",
                    display_name="Alice",
                    email="alice@test.com",
                    daily_config=DailyConfig(active=True),
                ),
                TeamMember(
                    id="bob",
                    name="Bob Brown",
                    display_name="Bob",
                    email="bob@test.com",
                    daily_config=DailyConfig(active=True),
                ),
                TeamMember(
                    id="carol",
                    name="Carol Clark",
                    display_name="Carol",
                    email="carol@test.com",
                    daily_config=DailyConfig(active=False),
                ),
            ],
        )

    def test_get_active_members(self, sample_team_file: TeamFile) -> None:
        """Test filtering active members."""
        active = sample_team_file.get_active_members()
        assert len(active) == 2
        assert all(m.daily_config.active for m in active)

    def test_get_member_by_id(self, sample_team_file: TeamFile) -> None:
        """Test finding member by ID."""
        member = sample_team_file.get_member_by_id("alice")
        assert member is not None
        assert member.display_name == "Alice"

    def test_get_member_by_id_not_found(self, sample_team_file: TeamFile) -> None:
        """Test finding non-existent member."""
        member = sample_team_file.get_member_by_id("unknown")
        assert member is None

    def test_get_sorted_members_by_display_name(self, sample_team_file: TeamFile) -> None:
        """Test sorting members by display name."""
        sorted_members = sample_team_file.get_sorted_members("display_name")
        names = [m.display_name for m in sorted_members]
        assert names == ["Alice", "Bob"]  # Carol is inactive

    def test_get_sorted_members_by_id(self, sample_team_file: TeamFile) -> None:
        """Test sorting members by ID."""
        sorted_members = sample_team_file.get_sorted_members("id")
        ids = [m.id for m in sorted_members]
        assert ids == ["alice", "bob"]


# =============================================================================
# Test 2.T2: Invalid team member rejected
# =============================================================================


class TestTeamMemberValidation:
    """Test TeamMember validation rules."""

    def test_reject_missing_required_field(self) -> None:
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TeamMember(
                id="test",
                name="Test",
                # missing display_name and email
            )  # type: ignore[call-arg]
        errors = exc_info.value.errors()
        error_fields = {e["loc"][0] for e in errors}
        assert "display_name" in error_fields
        assert "email" in error_fields

    def test_reject_invalid_email(self) -> None:
        """Test that invalid email format is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            TeamMember(
                id="test",
                name="Test User",
                display_name="Test",
                email="not-an-email",
            )
        assert any("email" in str(e["loc"]) for e in exc_info.value.errors())

    def test_reject_invalid_id_format(self) -> None:
        """Test that invalid ID format is rejected."""
        with pytest.raises(ValidationError):
            TeamMember(
                id="123invalid",  # Must start with letter
                name="Test User",
                display_name="Test",
                email="test@example.com",
            )

    def test_reject_id_with_uppercase(self) -> None:
        """Test that uppercase ID is rejected."""
        with pytest.raises(ValidationError):
            TeamMember(
                id="TestUser",  # Must be lowercase
                name="Test User",
                display_name="Test",
                email="test@example.com",
            )

    def test_reject_empty_id(self) -> None:
        """Test that empty ID is rejected."""
        with pytest.raises(ValidationError):
            TeamMember(
                id="",
                name="Test User",
                display_name="Test",
                email="test@example.com",
            )

    def test_reject_time_too_short(self) -> None:
        """Test that speaking time below minimum is rejected."""
        with pytest.raises(ValidationError):
            DailyConfig(default_time_seconds=10)  # Minimum is 30

    def test_reject_time_too_long(self) -> None:
        """Test that speaking time above maximum is rejected."""
        with pytest.raises(ValidationError):
            DailyConfig(default_time_seconds=1000)  # Maximum is 600

    def test_reject_empty_team_members(self) -> None:
        """Test that TeamFile requires at least one member."""
        with pytest.raises(ValidationError):
            TeamFile(
                team=TeamInfo(name="Empty Team"),
                members=[],  # Must have at least 1 member
            )


# =============================================================================
# Test 2.T3: Config model with defaults
# =============================================================================


class TestConfigModels:
    """Test configuration model defaults."""

    def test_timer_config_defaults(self) -> None:
        """Test TimerConfig default values."""
        config = TimerConfig()
        assert config.default_speaker_time_seconds == 180
        assert config.transition_time_seconds == 30
        assert config.grace_period_seconds == 15
        assert config.warning_threshold_seconds == 30

    def test_alert_config_defaults(self) -> None:
        """Test AlertConfig default values."""
        config = AlertConfig()
        assert config.warning_color == "#FFA500"
        assert config.overtime_color == "#FF0000"
        assert config.flash_on_overtime is True

    def test_history_config_defaults(self) -> None:
        """Test HistoryConfig default values."""
        config = HistoryConfig()
        assert config.max_entries == 2000
        assert "{team_id}" in config.file_path

    def test_recovery_config_defaults(self) -> None:
        """Test RecoveryConfig default values."""
        config = RecoveryConfig()
        assert config.enabled is True
        assert config.auto_save_interval_seconds == 5

    def test_ui_config_defaults(self) -> None:
        """Test UIConfig default values."""
        config = UIConfig()
        assert config.theme == "light"
        assert config.show_avatars is False

    def test_teams_config_defaults(self) -> None:
        """Test TeamsConfig default values."""
        config = TeamsConfig()
        assert config.directory == "teams"
        assert config.default_team == "imagine_dragons"

    def test_app_config_create_default(self) -> None:
        """Test creating AppConfig with all defaults."""
        config = AppConfig.create_default()
        assert config.version == "1.0"
        assert config.timer.default_speaker_time_seconds == 180
        assert config.teams.default_team == "imagine_dragons"
        assert config.default_order == "alphabetical"

    def test_app_config_custom_values(self) -> None:
        """Test AppConfig with custom values."""
        config = AppConfig(
            timer=TimerConfig(default_speaker_time_seconds=240),
            teams=TeamsConfig(default_team="other_team"),
        )
        assert config.timer.default_speaker_time_seconds == 240
        assert config.teams.default_team == "other_team"

    def test_reject_invalid_color_format(self) -> None:
        """Test that invalid color format is rejected."""
        with pytest.raises(ValidationError):
            AlertConfig(warning_color="orange")  # Must be hex format

    def test_reject_invalid_theme(self) -> None:
        """Test that invalid theme is rejected."""
        with pytest.raises(ValidationError):
            UIConfig(theme="blue")  # Must be "light" or "dark"


# =============================================================================
# Test 2.T4: Meeting record serialization round-trip
# =============================================================================


class TestMeetingRecordSerialization:
    """Test MeetingRecord serialization and deserialization."""

    @pytest.fixture
    def sample_meeting_record(self) -> MeetingRecord:
        """Create a sample meeting record."""
        return MeetingRecord(
            id="2026-01-04T09:00:00",
            date="2026-01-04",
            start_time="09:00:00",
            end_time="09:18:45",
            total_duration_seconds=1125,
            expected_duration_seconds=1230,
            status=MeetingStatus.COMPLETED,
            team_id="test_team",
            participants=[
                ParticipantRecord(
                    member_id="alice",
                    display_name="Alice",
                    status=ParticipantStatus.PRESENT,
                    allocated_time_seconds=180,
                    actual_time_seconds=165.5,
                    overtime_seconds=0,
                    order_position=1,
                ),
                ParticipantRecord(
                    member_id="bob",
                    display_name="Bob",
                    status=ParticipantStatus.PRESENT,
                    allocated_time_seconds=180,
                    actual_time_seconds=195.0,
                    overtime_seconds=15.0,
                    order_position=2,
                ),
                ParticipantRecord(
                    member_id="carol",
                    display_name="Carol",
                    status=ParticipantStatus.ABSENT,
                    allocated_time_seconds=0,
                    actual_time_seconds=0,
                    overtime_seconds=0,
                    order_position=None,
                ),
            ],
            notes="Test meeting",
        )

    def test_serialize_to_json(self, sample_meeting_record: MeetingRecord) -> None:
        """Test serialization to JSON."""
        json_str = sample_meeting_record.model_dump_json()
        data = json.loads(json_str)

        assert data["id"] == "2026-01-04T09:00:00"
        assert data["status"] == "completed"
        assert len(data["participants"]) == 3

    def test_deserialize_from_json(self, sample_meeting_record: MeetingRecord) -> None:
        """Test deserialization from JSON."""
        json_str = sample_meeting_record.model_dump_json()
        restored = MeetingRecord.model_validate_json(json_str)

        assert restored.id == sample_meeting_record.id
        assert restored.status == sample_meeting_record.status
        assert len(restored.participants) == len(sample_meeting_record.participants)

    def test_round_trip_preserves_data(self, sample_meeting_record: MeetingRecord) -> None:
        """Test that serialization round-trip preserves all data."""
        json_str = sample_meeting_record.model_dump_json()
        restored = MeetingRecord.model_validate_json(json_str)

        assert restored == sample_meeting_record

    def test_get_total_overtime(self, sample_meeting_record: MeetingRecord) -> None:
        """Test calculating total overtime."""
        overtime = sample_meeting_record.get_total_overtime()
        assert overtime == 15.0

    def test_get_present_count(self, sample_meeting_record: MeetingRecord) -> None:
        """Test counting present participants."""
        count = sample_meeting_record.get_present_count()
        assert count == 2

    def test_get_absent_count(self, sample_meeting_record: MeetingRecord) -> None:
        """Test counting absent participants."""
        count = sample_meeting_record.get_absent_count()
        assert count == 1


class TestHistoryFile:
    """Test HistoryFile model and methods."""

    def test_add_entry_within_limit(self) -> None:
        """Test adding entries within the limit."""
        history = HistoryFile()
        record = MeetingRecord(
            id="2026-01-04T09:00:00",
            date="2026-01-04",
            start_time="09:00:00",
            end_time="09:15:00",
            total_duration_seconds=900,
            expected_duration_seconds=900,
            status=MeetingStatus.COMPLETED,
        )
        history.add_entry(record)
        assert len(history.entries) == 1

    def test_add_entry_enforces_limit(self) -> None:
        """Test that add_entry enforces max_entries limit."""
        history = HistoryFile()

        # Add more than the limit
        for i in range(105):
            record = MeetingRecord(
                id=f"2026-01-{i:02d}T09:00:00",
                date=f"2026-01-{(i % 28) + 1:02d}",
                start_time="09:00:00",
                end_time="09:15:00",
                total_duration_seconds=900,
                expected_duration_seconds=900,
                status=MeetingStatus.COMPLETED,
            )
            history.add_entry(record, max_entries=100)

        assert len(history.entries) == 100
        # Should keep the latest entries
        assert history.entries[0].id == "2026-01-05T09:00:00"

    def test_get_entries_by_date_range(self) -> None:
        """Test filtering entries by date range."""
        history = HistoryFile(
            entries=[
                MeetingRecord(
                    id="2026-01-01T09:00:00",
                    date="2026-01-01",
                    start_time="09:00:00",
                    end_time="09:15:00",
                    total_duration_seconds=900,
                    expected_duration_seconds=900,
                    status=MeetingStatus.COMPLETED,
                ),
                MeetingRecord(
                    id="2026-01-05T09:00:00",
                    date="2026-01-05",
                    start_time="09:00:00",
                    end_time="09:15:00",
                    total_duration_seconds=900,
                    expected_duration_seconds=900,
                    status=MeetingStatus.COMPLETED,
                ),
                MeetingRecord(
                    id="2026-01-10T09:00:00",
                    date="2026-01-10",
                    start_time="09:00:00",
                    end_time="09:15:00",
                    total_duration_seconds=900,
                    expected_duration_seconds=900,
                    status=MeetingStatus.COMPLETED,
                ),
            ]
        )

        filtered = history.get_entries_by_date_range("2026-01-03", "2026-01-07")
        assert len(filtered) == 1
        assert filtered[0].date == "2026-01-05"


# =============================================================================
# Test 2.T5: Session recovery model validation
# =============================================================================


class TestSessionRecovery:
    """Test SessionRecovery model and methods."""

    def test_create_new_session(self) -> None:
        """Test creating a new recovery session."""
        session = SessionRecovery.create_new(
            team_id="test_team",
            speaker_order=["alice", "bob", "carol"],
        )

        assert session.team_id == "test_team"
        assert session.speaker_order == ["alice", "bob", "carol"]
        assert session.global_elapsed_seconds == 0
        assert session.current_speaker_index == 0
        assert session.state == MeetingState.IDLE
        assert session.is_paused is False

    def test_update_timestamp(self) -> None:
        """Test updating the timestamp."""
        session = SessionRecovery.create_new(
            team_id="test_team",
            speaker_order=["alice"],
        )
        original = session.last_updated

        # Small delay to ensure timestamp changes
        import time

        time.sleep(0.01)
        session.update_timestamp()

        assert session.last_updated != original

    def test_to_json_dict(self) -> None:
        """Test conversion to JSON dictionary."""
        session = SessionRecovery.create_new(
            team_id="test_team",
            speaker_order=["alice", "bob"],
        )
        session.completed_speakers = [
            CompletedSpeakerRecord(member_id="alice", actual_time_seconds=175.5)
        ]

        data = session.to_json_dict()

        assert isinstance(data, dict)
        assert data["team_id"] == "test_team"
        assert data["speaker_order"] == ["alice", "bob"]
        assert len(data["completed_speakers"]) == 1

    def test_from_json_dict(self) -> None:
        """Test creation from JSON dictionary."""
        session = SessionRecovery.create_new(
            team_id="test_team",
            speaker_order=["alice", "bob"],
        )
        session.global_elapsed_seconds = 300.5
        session.current_speaker_index = 1
        session.state = MeetingState.SPEAKING

        data = session.to_json_dict()
        restored = SessionRecovery.from_json_dict(data)

        assert restored.team_id == session.team_id
        assert restored.global_elapsed_seconds == 300.5
        assert restored.current_speaker_index == 1
        assert restored.state == MeetingState.SPEAKING

    def test_round_trip_serialization(self) -> None:
        """Test full serialization round-trip."""
        session = SessionRecovery.create_new(
            team_id="imagine_dragons",
            speaker_order=["chen", "miri", "muhe", "osher", "yair", "yocheved"],
        )
        session.global_elapsed_seconds = 450.25
        session.current_speaker_index = 2
        session.completed_speakers = [
            CompletedSpeakerRecord(member_id="chen", actual_time_seconds=165.0),
            CompletedSpeakerRecord(member_id="miri", actual_time_seconds=180.0),
        ]
        session.current_speaker_elapsed_seconds = 45.25
        session.absent_members = ["yocheved"]
        session.state = MeetingState.SPEAKING

        # Serialize to JSON string
        json_str = json.dumps(session.to_json_dict())

        # Deserialize back
        data = json.loads(json_str)
        restored = SessionRecovery.from_json_dict(data)

        assert restored.team_id == "imagine_dragons"
        assert restored.global_elapsed_seconds == 450.25
        assert len(restored.completed_speakers) == 2
        assert restored.absent_members == ["yocheved"]

    def test_reject_invalid_state(self) -> None:
        """Test that invalid state is rejected."""
        with pytest.raises(ValidationError):
            SessionRecovery(
                session_id="test",
                team_id="test",
                started_at="2026-01-04T09:00:00",
                last_updated="2026-01-04T09:00:00",
                global_elapsed_seconds=0,
                current_speaker_index=0,
                speaker_order=["alice"],
                state="invalid_state",  # type: ignore[arg-type]
            )

    def test_reject_negative_elapsed_time(self) -> None:
        """Test that negative elapsed time is rejected."""
        with pytest.raises(ValidationError):
            SessionRecovery(
                session_id="test",
                team_id="test",
                started_at="2026-01-04T09:00:00",
                last_updated="2026-01-04T09:00:00",
                global_elapsed_seconds=-10,  # Must be >= 0
                current_speaker_index=0,
                speaker_order=["alice"],
            )


# =============================================================================
# Enum Tests
# =============================================================================


class TestEnums:
    """Test enum values."""

    def test_participant_status_values(self) -> None:
        """Test ParticipantStatus enum values."""
        assert ParticipantStatus.PRESENT.value == "present"
        assert ParticipantStatus.ABSENT.value == "absent"
        assert ParticipantStatus.SKIPPED.value == "skipped"

    def test_meeting_status_values(self) -> None:
        """Test MeetingStatus enum values."""
        assert MeetingStatus.IN_PROGRESS.value == "in_progress"
        assert MeetingStatus.COMPLETED.value == "completed"
        assert MeetingStatus.CANCELLED.value == "cancelled"

    def test_meeting_state_values(self) -> None:
        """Test MeetingState enum values."""
        assert MeetingState.IDLE.value == "idle"
        assert MeetingState.TRANSITION.value == "transition"
        assert MeetingState.SPEAKING.value == "speaking"
        assert MeetingState.PAUSED.value == "paused"
        assert MeetingState.GRACE.value == "grace"
        assert MeetingState.OVERFLOW.value == "overflow"
        assert MeetingState.COMPLETED.value == "completed"


# =============================================================================
# Inactivity Timeout Config Tests
# =============================================================================


class TestInactivityTimeoutConfig:
    """Tests for inactivity_timeout_seconds in TimerConfig."""

    def test_timer_config_default_inactivity_timeout(self) -> None:
        """TimerConfig should default to 300s inactivity timeout."""
        config = TimerConfig()
        assert config.inactivity_timeout_seconds == 300

    def test_timer_config_custom_inactivity_timeout(self) -> None:
        """TimerConfig should accept custom inactivity timeout."""
        config = TimerConfig(inactivity_timeout_seconds=600)
        assert config.inactivity_timeout_seconds == 600

    def test_timer_config_inactivity_timeout_minimum(self) -> None:
        """TimerConfig should reject inactivity timeout below 60s."""
        with pytest.raises(ValidationError):
            TimerConfig(inactivity_timeout_seconds=30)

    def test_timer_config_inactivity_timeout_maximum(self) -> None:
        """TimerConfig should reject inactivity timeout above 1800s."""
        with pytest.raises(ValidationError):
            TimerConfig(inactivity_timeout_seconds=3600)
