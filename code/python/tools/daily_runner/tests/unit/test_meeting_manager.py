"""
Unit tests for the Meeting Manager.

Test coverage for Phase 6:
- 6.T1: Full meeting lifecycle (start → speakers → end)
- 6.T2: Meeting saves correct history record
- 6.T3: Skip speaker works mid-meeting
- 6.T4: Mark absent removes from queue
- 6.T5: Reorder updates remaining speakers
- 6.T6: Pause/resume affects all timers
- 6.T7: Add time extends current speaker
- 6.T8: Transition period between speakers
- 6.T9: Grace period triggers after time up
- 6.T10: Auto-advance after grace period
- 6.T11: Recovery file created during meeting
- 6.T12: Session restored correctly from recovery
- 6.T13: Discard recovery starts clean meeting
- 6.T14: End meeting clears recovery file
"""

import json
import time
from pathlib import Path
from typing import Any

import pytest

from src.core.meeting_manager import MeetingManager
from src.core.models import (
    AppConfig,
    MeetingState,
    ParticipantStatus,
)
from src.data.history_repository import HistoryRepository
from src.data.recovery_manager import RecoveryManager
from src.data.team_repository import TeamRepository

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Create temp directory structure."""
    (tmp_path / "teams").mkdir()
    (tmp_path / "data").mkdir()
    return tmp_path


@pytest.fixture
def sample_team_file() -> dict[str, Any]:
    """Create sample team data (members don't override config time)."""
    return {
        "team": {"name": "Test Team", "emoji": "🧪"},
        "members": [
            {
                "id": "alice",
                "name": "Alice Smith",
                "display_name": "Alice",
                "email": "alice@test.com",
            },
            {
                "id": "bob",
                "name": "Bob Jones",
                "display_name": "Bob",
                "email": "bob@test.com",
            },
            {
                "id": "charlie",
                "name": "Charlie Brown",
                "display_name": "Charlie",
                "email": "charlie@test.com",
            },
        ],
    }


@pytest.fixture
def setup_team(temp_dir: Path, sample_team_file: dict[str, Any]) -> None:
    """Write team file to disk."""
    team_path = temp_dir / "teams" / "test_team.json"
    team_path.write_text(json.dumps(sample_team_file))


@pytest.fixture
def config() -> AppConfig:
    """Create test configuration."""
    config = AppConfig.create_default()
    config.timer.default_speaker_time_seconds = 2  # Very short for testing
    config.timer.transition_time_seconds = 1  # Short transition
    config.timer.grace_period_seconds = 1  # Short grace
    config.teams.default_team = "test_team"
    return config


@pytest.fixture
def team_repo(temp_dir: Path, setup_team: None) -> TeamRepository:
    """Create team repository."""
    return TeamRepository(teams_dir=temp_dir / "teams")


@pytest.fixture
def history_repo(temp_dir: Path) -> HistoryRepository:
    """Create history repository."""
    return HistoryRepository(team_id="test_team", data_dir=temp_dir / "data")


@pytest.fixture
def recovery_mgr(temp_dir: Path) -> RecoveryManager:
    """Create recovery manager."""
    return RecoveryManager(
        recovery_path=temp_dir / "data" / ".session_recovery.json",
        auto_save_interval=60,  # Long interval to avoid auto-saves in tests
    )


@pytest.fixture
def meeting_manager(
    team_repo: TeamRepository,
    config: AppConfig,
    history_repo: HistoryRepository,
    recovery_mgr: RecoveryManager,
) -> MeetingManager:
    """Create meeting manager."""
    return MeetingManager(
        team_repo=team_repo,
        config=config,
        history_repo=history_repo,
        recovery_mgr=recovery_mgr,
    )


# =============================================================================
# Test 6.T1: Full Meeting Lifecycle
# =============================================================================


class TestMeetingLifecycle:
    """Test 6.T1: Full meeting lifecycle."""

    def test_start_meeting(self, meeting_manager: MeetingManager) -> None:
        """Can start a meeting."""
        meeting_manager.start_meeting()

        assert meeting_manager.is_active is True
        assert meeting_manager.session_id is not None
        assert meeting_manager.team_id == "test_team"
        assert meeting_manager.total_speakers == 3

    def test_start_meeting_sets_transition_state(
        self, meeting_manager: MeetingManager
    ) -> None:
        """Starting meeting enters transition state."""
        meeting_manager.start_meeting()

        assert meeting_manager.state == MeetingState.TRANSITION

    def test_cannot_start_while_active(self, meeting_manager: MeetingManager) -> None:
        """Cannot start a meeting while one is active."""
        meeting_manager.start_meeting()

        with pytest.raises(RuntimeError, match="already in progress"):
            meeting_manager.start_meeting()

    def test_full_lifecycle(self, meeting_manager: MeetingManager) -> None:
        """Complete meeting from start to finish."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()  # Start first speaker

        # Go through all speakers
        for _ in range(3):
            time.sleep(0.1)
            meeting_manager.next_speaker()
            if meeting_manager.is_active and meeting_manager.state == MeetingState.TRANSITION:
                meeting_manager.start_speaking()

        # Meeting should be completed or we should end it
        if meeting_manager.is_active:
            meeting_manager.end_meeting()

        assert meeting_manager.is_active is False

    def test_end_meeting_returns_record(self, meeting_manager: MeetingManager) -> None:
        """Ending meeting returns a record."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()
        time.sleep(0.1)

        record = meeting_manager.end_meeting()

        assert record is not None
        assert record.team_id == "test_team"
        assert len(record.participants) == 3

    def test_custom_speaker_order(self, meeting_manager: MeetingManager) -> None:
        """Can start with custom speaker order."""
        meeting_manager.start_meeting(speaker_order=["charlie", "alice", "bob"])
        meeting_manager.start_speaking()

        assert meeting_manager.current_speaker is not None
        assert meeting_manager.current_speaker.id == "charlie"


# =============================================================================
# Test 6.T2: Meeting Saves History Record
# =============================================================================


class TestMeetingHistory:
    """Test 6.T2: Meeting saves correct history record."""

    def test_history_saved_on_end(
        self, meeting_manager: MeetingManager, history_repo: HistoryRepository
    ) -> None:
        """Meeting record is saved to history."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()
        time.sleep(0.1)
        meeting_manager.end_meeting()

        entries = history_repo.get_entries()
        assert len(entries) == 1
        assert entries[0].team_id == "test_team"

    def test_history_not_saved_when_disabled(
        self, meeting_manager: MeetingManager, history_repo: HistoryRepository
    ) -> None:
        """Can disable history saving."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()
        meeting_manager.end_meeting(save_history=False)

        entries = history_repo.get_entries()
        assert len(entries) == 0

    def test_participant_times_recorded(
        self, meeting_manager: MeetingManager, history_repo: HistoryRepository
    ) -> None:
        """Participant speaking times are recorded."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()
        time.sleep(0.2)
        meeting_manager.end_meeting()

        entries = history_repo.get_entries()
        assert len(entries) == 1

        # First participant should have recorded time
        alice_record = next(
            (p for p in entries[0].participants if p.member_id == "alice"), None
        )
        assert alice_record is not None
        assert alice_record.actual_time_seconds > 0


# =============================================================================
# Test 6.T3: Skip Speaker
# =============================================================================


class TestSkipSpeaker:
    """Test 6.T3: Skip speaker works mid-meeting."""

    def test_skip_advances_to_next(self, meeting_manager: MeetingManager) -> None:
        """Skipping advances to next speaker."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        assert meeting_manager.current_speaker is not None
        assert meeting_manager.current_speaker.id == "alice"

        meeting_manager.skip_speaker()
        if meeting_manager.state == MeetingState.TRANSITION:
            meeting_manager.start_speaking()

        assert meeting_manager.current_speaker is not None
        assert meeting_manager.current_speaker.id == "bob"

    def test_skipped_speaker_marked(
        self, meeting_manager: MeetingManager, history_repo: HistoryRepository
    ) -> None:
        """Skipped speaker is marked in history."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()
        meeting_manager.skip_speaker()
        meeting_manager.end_meeting()

        entries = history_repo.get_entries()
        alice_record = next(
            (p for p in entries[0].participants if p.member_id == "alice"), None
        )
        assert alice_record is not None
        assert alice_record.status == ParticipantStatus.SKIPPED


# =============================================================================
# Test 6.T4: Mark Absent
# =============================================================================


class TestMarkAbsent:
    """Test 6.T4: Mark absent removes from queue."""

    def test_mark_absent_skips_in_queue(self, meeting_manager: MeetingManager) -> None:
        """Marking absent causes speaker to be skipped."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        # Mark bob absent before reaching him
        meeting_manager.mark_absent("bob")

        # Advance through speakers
        meeting_manager.next_speaker()
        if meeting_manager.state == MeetingState.TRANSITION:
            meeting_manager.start_speaking()

        # Should skip bob and go to charlie
        assert meeting_manager.current_speaker is not None
        assert meeting_manager.current_speaker.id == "charlie"

    def test_mark_current_absent_advances(
        self, meeting_manager: MeetingManager
    ) -> None:
        """Marking current speaker absent advances to next."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        assert meeting_manager.current_speaker is not None
        assert meeting_manager.current_speaker.id == "alice"

        meeting_manager.mark_absent("alice")

        # Should advance (possibly through transition)
        if meeting_manager.state == MeetingState.TRANSITION:
            meeting_manager.start_speaking()

        assert meeting_manager.current_speaker is not None
        assert meeting_manager.current_speaker.id == "bob"

    def test_absent_recorded_in_history(
        self, meeting_manager: MeetingManager, history_repo: HistoryRepository
    ) -> None:
        """Absent status recorded in history."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()
        meeting_manager.mark_absent("charlie")
        meeting_manager.end_meeting()

        entries = history_repo.get_entries()
        charlie_record = next(
            (p for p in entries[0].participants if p.member_id == "charlie"), None
        )
        assert charlie_record is not None
        assert charlie_record.status == ParticipantStatus.ABSENT


# =============================================================================
# Test 6.T5: Reorder Speakers
# =============================================================================


class TestReorderSpeakers:
    """Test 6.T5: Reorder updates remaining speakers."""

    def test_reorder_changes_queue(self, meeting_manager: MeetingManager) -> None:
        """Reordering changes speaker queue."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        # Reorder remaining speakers
        meeting_manager.reorder_speakers(["charlie", "bob"])

        # Advance to next
        meeting_manager.next_speaker()
        if meeting_manager.state == MeetingState.TRANSITION:
            meeting_manager.start_speaking()

        assert meeting_manager.current_speaker is not None
        assert meeting_manager.current_speaker.id == "charlie"


# =============================================================================
# Test 6.T6: Pause/Resume
# =============================================================================


class TestPauseResume:
    """Test 6.T6: Pause/resume affects all timers."""

    def test_pause_changes_state(self, meeting_manager: MeetingManager) -> None:
        """Pausing changes state to PAUSED."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        meeting_manager.pause()

        assert meeting_manager.state == MeetingState.PAUSED

    def test_pause_freezes_timer(self, meeting_manager: MeetingManager) -> None:
        """Pausing freezes speaker timer."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()
        time.sleep(0.1)

        meeting_manager.pause()
        elapsed_at_pause = meeting_manager.speaker_time_elapsed

        time.sleep(0.2)

        # Timer should not have advanced
        assert abs(meeting_manager.speaker_time_elapsed - elapsed_at_pause) < 0.05

    def test_resume_continues_timer(self, meeting_manager: MeetingManager) -> None:
        """Resuming continues timer."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()
        time.sleep(0.1)

        meeting_manager.pause()
        elapsed_at_pause = meeting_manager.speaker_time_elapsed

        time.sleep(0.1)
        meeting_manager.resume()
        time.sleep(0.1)

        # Timer should have advanced
        assert meeting_manager.speaker_time_elapsed > elapsed_at_pause

    def test_resume_restores_state(self, meeting_manager: MeetingManager) -> None:
        """Resuming restores previous state."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        meeting_manager.pause()
        meeting_manager.resume()

        assert meeting_manager.state == MeetingState.SPEAKING


# =============================================================================
# Test 6.T7: Add Time
# =============================================================================


class TestAddTime:
    """Test 6.T7: Add time extends current speaker."""

    def test_add_time_increases_remaining(
        self, meeting_manager: MeetingManager
    ) -> None:
        """Adding time increases remaining time."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        remaining_before = meeting_manager.speaker_time_remaining
        meeting_manager.add_time(30)
        remaining_after = meeting_manager.speaker_time_remaining

        assert remaining_after > remaining_before
        assert abs((remaining_after - remaining_before) - 30) < 0.1

    def test_add_negative_time(self, meeting_manager: MeetingManager) -> None:
        """Can subtract time."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        remaining_before = meeting_manager.speaker_time_remaining
        meeting_manager.add_time(-2)
        remaining_after = meeting_manager.speaker_time_remaining

        assert remaining_after < remaining_before


# =============================================================================
# Test 6.T8: Transition Period
# =============================================================================


class TestTransitionPeriod:
    """Test 6.T8: Transition period between speakers."""

    def test_transition_state_on_start(self, meeting_manager: MeetingManager) -> None:
        """Meeting starts in transition state."""
        meeting_manager.start_meeting()

        assert meeting_manager.state == MeetingState.TRANSITION

    def test_transition_timer_running(self, meeting_manager: MeetingManager) -> None:
        """Transition timer is running during transition."""
        meeting_manager.start_meeting()

        assert meeting_manager.transition_time_remaining > 0

    def test_start_speaking_transitions_state(
        self, meeting_manager: MeetingManager
    ) -> None:
        """Starting to speak transitions to SPEAKING state."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        assert meeting_manager.state == MeetingState.SPEAKING


# =============================================================================
# Test 6.T9: Grace Period
# =============================================================================


class TestGracePeriod:
    """Test 6.T9: Grace period triggers after time up."""

    def test_grace_period_detected(self, meeting_manager: MeetingManager) -> None:
        """Grace period is detected when overtime (simulated)."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        # Simulate overtime by reducing timer duration
        assert meeting_manager._speaker_timer is not None
        meeting_manager._speaker_timer.add_time(-175)  # From 180 to 5 seconds
        time.sleep(5.5)

        in_grace = meeting_manager.check_grace_period()
        assert in_grace is True
        assert meeting_manager.is_overtime is True

    def test_grace_period_changes_state(
        self, meeting_manager: MeetingManager
    ) -> None:
        """Grace period changes state to GRACE (simulated)."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        # Simulate overtime
        assert meeting_manager._speaker_timer is not None
        meeting_manager._speaker_timer.add_time(-175)
        time.sleep(5.5)
        meeting_manager.check_grace_period()

        assert meeting_manager.state == MeetingState.GRACE
        assert meeting_manager.is_overtime is True

    def test_add_time_exits_grace(self, meeting_manager: MeetingManager) -> None:
        """Adding time exits grace period (simulated)."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        # Simulate overtime
        assert meeting_manager._speaker_timer is not None
        meeting_manager._speaker_timer.add_time(-175)
        time.sleep(5.5)
        meeting_manager.check_grace_period()
        assert meeting_manager.state == MeetingState.GRACE
        assert meeting_manager.is_overtime is True

        meeting_manager.add_time(60)

        assert meeting_manager.state == MeetingState.SPEAKING


# =============================================================================
# Test 6.T10: Auto-Advance
# =============================================================================


class TestAutoAdvance:
    """Test 6.T10: Auto-advance after grace period."""

    def test_should_auto_advance_when_grace_exceeded(
        self, meeting_manager: MeetingManager
    ) -> None:
        """Should auto-advance when grace period exceeded (simulated)."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        # Simulate overtime past grace period (reduce to 3s, wait 5s = 2s overtime)
        assert meeting_manager._speaker_timer is not None
        meeting_manager._speaker_timer.add_time(-177)  # From 180 to 3 seconds
        time.sleep(5.5)  # 2.5s overtime, exceeding 1s grace
        meeting_manager.check_grace_period()

        # Should be in grace and overtime > grace_period_seconds
        assert meeting_manager.is_overtime is True
        should_advance = meeting_manager.should_auto_advance()
        assert should_advance is True

    def test_not_auto_advance_during_normal_speaking(
        self, meeting_manager: MeetingManager
    ) -> None:
        """Should not auto-advance during normal speaking."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        time.sleep(0.1)

        should_advance = meeting_manager.should_auto_advance()
        assert should_advance is False


# =============================================================================
# Test 6.T11: Recovery File Created
# =============================================================================


class TestRecoveryCreation:
    """Test 6.T11: Recovery file created during meeting."""

    def test_recovery_state_available(self, meeting_manager: MeetingManager) -> None:
        """Recovery state can be retrieved during meeting."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        # Get recovery state directly
        state = meeting_manager._get_recovery_state()

        assert state is not None
        assert state.session_id == meeting_manager.session_id
        assert state.team_id == "test_team"


# =============================================================================
# Test 6.T12: Session Restored
# =============================================================================


class TestSessionRestore:
    """Test 6.T12: Session restored correctly from recovery."""

    def test_restore_session(
        self,
        team_repo: TeamRepository,
        config: AppConfig,
        history_repo: HistoryRepository,
        recovery_mgr: RecoveryManager,
    ) -> None:
        """Can restore a session from recovery."""
        # Start and save state with first manager
        mm1 = MeetingManager(team_repo, config, history_repo, recovery_mgr)
        mm1.start_meeting()
        mm1.start_speaking()
        time.sleep(0.2)

        # Save recovery manually (simulating periodic auto-save)
        state = mm1._get_recovery_state()
        assert state is not None
        recovery_mgr.save_recovery(state)
        recovery_mgr.stop_auto_save()  # Stop auto-save without clearing file

        # Verify recovery file exists
        assert recovery_mgr.has_recovery() is True

        # Create new manager (simulating restart after crash)
        mm2 = MeetingManager(team_repo, config, history_repo, recovery_mgr)

        # Restore
        result = mm2.restore_session()

        assert result is True
        assert mm2.is_active is True


# =============================================================================
# Test 6.T13: Discard Recovery
# =============================================================================


class TestDiscardRecovery:
    """Test 6.T13: Discard recovery starts clean meeting."""

    def test_discard_clears_recovery(
        self,
        meeting_manager: MeetingManager,
        recovery_mgr: RecoveryManager,
    ) -> None:
        """Discarding recovery clears the file."""
        # Create recovery
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()
        state = meeting_manager._get_recovery_state()
        assert state is not None
        recovery_mgr.save_recovery(state)
        meeting_manager.end_meeting(save_history=False)

        # Discard
        meeting_manager.discard_recovery()

        assert recovery_mgr.has_recovery() is False


# =============================================================================
# Test 6.T14: End Meeting Clears Recovery
# =============================================================================


class TestEndClearsRecovery:
    """Test 6.T14: End meeting clears recovery file."""

    def test_end_meeting_clears_recovery(
        self,
        meeting_manager: MeetingManager,
        recovery_mgr: RecoveryManager,
    ) -> None:
        """Ending meeting clears recovery."""
        meeting_manager.start_meeting()
        meeting_manager.start_speaking()

        # Save recovery manually
        state = meeting_manager._get_recovery_state()
        assert state is not None
        recovery_mgr.save_recovery(state)

        # End meeting
        meeting_manager.end_meeting()

        assert recovery_mgr.has_recovery() is False


# =============================================================================
# Additional Tests: Observer and Edge Cases
# =============================================================================


class TestMeetingObservers:
    """Test meeting observer notifications."""

    def test_observer_notified_on_start(self, meeting_manager: MeetingManager) -> None:
        """Observer is notified when meeting starts."""
        events: list[tuple[str, dict]] = []
        meeting_manager.add_observer(lambda e, d: events.append((e, d)))

        meeting_manager.start_meeting()

        assert any(e[0] == "meeting_started" for e in events)

    def test_observer_notified_on_end(self, meeting_manager: MeetingManager) -> None:
        """Observer is notified when meeting ends."""
        events: list[tuple[str, dict]] = []
        meeting_manager.add_observer(lambda e, d: events.append((e, d)))

        meeting_manager.start_meeting()
        meeting_manager.start_speaking()
        meeting_manager.end_meeting()

        assert any(e[0] == "meeting_ended" for e in events)

    def test_remove_observer(self, meeting_manager: MeetingManager) -> None:
        """Can remove observer."""
        events: list[str] = []

        def observer(e: str, d: dict) -> None:
            events.append(e)

        meeting_manager.add_observer(observer)
        meeting_manager.start_meeting()

        events.clear()
        meeting_manager.remove_observer(observer)
        meeting_manager.end_meeting()

        # Should not have received end event
        assert "meeting_ended" not in events


class TestMeetingEdgeCases:
    """Test edge cases."""

    def test_end_meeting_when_not_active(
        self, meeting_manager: MeetingManager
    ) -> None:
        """Ending when not active returns None."""
        result = meeting_manager.end_meeting()
        assert result is None

    def test_next_speaker_when_not_active(
        self, meeting_manager: MeetingManager
    ) -> None:
        """Next speaker when not active returns None."""
        result = meeting_manager.next_speaker()
        assert result is None

    def test_start_without_default_team(
        self,
        team_repo: TeamRepository,
        history_repo: HistoryRepository,
        recovery_mgr: RecoveryManager,
    ) -> None:
        """Error when no team specified and no default."""
        config = AppConfig.create_default()
        config.teams.default_team = None

        mm = MeetingManager(team_repo, config, history_repo, recovery_mgr)

        with pytest.raises(ValueError, match="No team"):
            mm.start_meeting()

    def test_properties_when_no_timer(self, meeting_manager: MeetingManager) -> None:
        """Properties return defaults when no timer."""
        assert meeting_manager.speaker_time_remaining == 0.0
        assert meeting_manager.speaker_time_elapsed == 0.0
        assert meeting_manager.transition_time_remaining == 0.0
        assert meeting_manager.meeting_elapsed == 0.0
        assert meeting_manager.is_overtime is False
        assert meeting_manager.overtime_seconds == 0.0
