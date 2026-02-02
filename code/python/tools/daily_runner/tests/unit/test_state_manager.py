"""
Unit tests for the State Manager.

Test coverage for Phase 5:
- 5.T1: Valid state transitions succeed
- 5.T2: Invalid transitions raise exception
- 5.T3: All valid transitions covered (matrix test)
- 5.T4: Observers notified on state change
- 5.T5: Observer removal works correctly
- 5.T6: Speaker queue management (next, skip)
- 5.T7: Current speaker tracking accurate
- 5.T8: Absent member handling in queue
"""

import pytest

from src.core.models import MeetingState, TeamMember
from src.core.state_manager import (
    VALID_TRANSITIONS,
    InvalidStateTransitionError,
    SpeakerRecord,
    StateManager,
)

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def state_manager() -> StateManager:
    """Create a fresh state manager."""
    return StateManager()


@pytest.fixture
def sample_members() -> list[TeamMember]:
    """Create sample team members for testing."""
    return [
        TeamMember(
            id="alice",
            name="Alice Smith",
            display_name="Alice",
            email="alice@test.com",
        ),
        TeamMember(
            id="bob",
            name="Bob Jones",
            display_name="Bob",
            email="bob@test.com",
        ),
        TeamMember(
            id="charlie",
            name="Charlie Brown",
            display_name="Charlie",
            email="charlie@test.com",
        ),
    ]


# =============================================================================
# Test 5.T1: Valid State Transitions
# =============================================================================


class TestValidTransitions:
    """Test 5.T1: Valid state transitions succeed."""

    def test_idle_to_transition(self, state_manager: StateManager) -> None:
        """Can transition from IDLE to TRANSITION."""
        state_manager.transition_to(MeetingState.TRANSITION)
        assert state_manager.state == MeetingState.TRANSITION

    def test_idle_to_speaking(self, state_manager: StateManager) -> None:
        """Can transition from IDLE to SPEAKING (skip transition)."""
        state_manager.transition_to(MeetingState.SPEAKING)
        assert state_manager.state == MeetingState.SPEAKING

    def test_transition_to_speaking(self, state_manager: StateManager) -> None:
        """Can transition from TRANSITION to SPEAKING."""
        state_manager.transition_to(MeetingState.TRANSITION)
        state_manager.transition_to(MeetingState.SPEAKING)
        assert state_manager.state == MeetingState.SPEAKING

    def test_speaking_to_paused(self, state_manager: StateManager) -> None:
        """Can transition from SPEAKING to PAUSED."""
        state_manager.transition_to(MeetingState.SPEAKING)
        state_manager.transition_to(MeetingState.PAUSED)
        assert state_manager.state == MeetingState.PAUSED

    def test_paused_to_speaking(self, state_manager: StateManager) -> None:
        """Can transition from PAUSED back to SPEAKING."""
        state_manager.transition_to(MeetingState.SPEAKING)
        state_manager.transition_to(MeetingState.PAUSED)
        state_manager.transition_to(MeetingState.SPEAKING)
        assert state_manager.state == MeetingState.SPEAKING

    def test_speaking_to_grace(self, state_manager: StateManager) -> None:
        """Can transition from SPEAKING to GRACE."""
        state_manager.transition_to(MeetingState.SPEAKING)
        state_manager.transition_to(MeetingState.GRACE)
        assert state_manager.state == MeetingState.GRACE

    def test_grace_to_transition(self, state_manager: StateManager) -> None:
        """Can transition from GRACE to TRANSITION."""
        state_manager.transition_to(MeetingState.SPEAKING)
        state_manager.transition_to(MeetingState.GRACE)
        state_manager.transition_to(MeetingState.TRANSITION)
        assert state_manager.state == MeetingState.TRANSITION

    def test_speaking_to_completed(self, state_manager: StateManager) -> None:
        """Can transition from SPEAKING to COMPLETED."""
        state_manager.transition_to(MeetingState.SPEAKING)
        state_manager.transition_to(MeetingState.COMPLETED)
        assert state_manager.state == MeetingState.COMPLETED


# =============================================================================
# Test 5.T2: Invalid State Transitions
# =============================================================================


class TestInvalidTransitions:
    """Test 5.T2: Invalid transitions raise exception."""

    def test_idle_to_paused_invalid(self, state_manager: StateManager) -> None:
        """Cannot transition from IDLE to PAUSED."""
        with pytest.raises(InvalidStateTransitionError):
            state_manager.transition_to(MeetingState.PAUSED)

    def test_idle_to_grace_invalid(self, state_manager: StateManager) -> None:
        """Cannot transition from IDLE to GRACE."""
        with pytest.raises(InvalidStateTransitionError):
            state_manager.transition_to(MeetingState.GRACE)

    def test_idle_to_completed_invalid(self, state_manager: StateManager) -> None:
        """Cannot transition from IDLE to COMPLETED."""
        with pytest.raises(InvalidStateTransitionError):
            state_manager.transition_to(MeetingState.COMPLETED)

    def test_completed_to_any_invalid(self, state_manager: StateManager) -> None:
        """Cannot transition out of COMPLETED state."""
        state_manager.transition_to(MeetingState.SPEAKING)
        state_manager.transition_to(MeetingState.COMPLETED)

        for target in MeetingState:
            if target != MeetingState.COMPLETED:
                with pytest.raises(InvalidStateTransitionError):
                    state_manager.transition_to(target)

    def test_transition_to_idle_invalid(self, state_manager: StateManager) -> None:
        """Cannot transition back to IDLE (except via reset)."""
        state_manager.transition_to(MeetingState.SPEAKING)

        with pytest.raises(InvalidStateTransitionError):
            state_manager.transition_to(MeetingState.IDLE)

    def test_error_message_contains_states(self, state_manager: StateManager) -> None:
        """Error message should include state names."""
        try:
            state_manager.transition_to(MeetingState.GRACE)
        except InvalidStateTransitionError as e:
            assert "idle" in str(e).lower()
            assert "grace" in str(e).lower()


# =============================================================================
# Test 5.T3: All Valid Transitions (Matrix Test)
# =============================================================================


class TestTransitionMatrix:
    """Test 5.T3: All valid transitions covered."""

    def test_all_valid_transitions_work(self) -> None:
        """Every transition in VALID_TRANSITIONS should succeed."""
        for from_state, valid_targets in VALID_TRANSITIONS.items():
            for to_state in valid_targets:
                # Create fresh manager for each test
                sm = StateManager()

                # Get to from_state first
                if from_state != MeetingState.IDLE:
                    self._navigate_to_state(sm, from_state)

                # Now test the transition
                sm.transition_to(to_state)
                assert sm.state == to_state

    def test_all_invalid_transitions_fail(self) -> None:
        """Every transition NOT in VALID_TRANSITIONS should fail."""
        all_states = set(MeetingState)

        for from_state, valid_targets in VALID_TRANSITIONS.items():
            invalid_targets = all_states - valid_targets - {from_state}

            for to_state in invalid_targets:
                sm = StateManager()

                # Get to from_state first
                if from_state != MeetingState.IDLE:
                    self._navigate_to_state(sm, from_state)

                # This transition should fail
                with pytest.raises(InvalidStateTransitionError):
                    sm.transition_to(to_state)

    def _navigate_to_state(self, sm: StateManager, target: MeetingState) -> None:
        """Helper to navigate to a specific state."""
        paths = {
            MeetingState.TRANSITION: [MeetingState.TRANSITION],
            MeetingState.SPEAKING: [MeetingState.SPEAKING],
            MeetingState.PAUSED: [MeetingState.SPEAKING, MeetingState.PAUSED],
            MeetingState.GRACE: [MeetingState.SPEAKING, MeetingState.GRACE],
            MeetingState.OVERFLOW: [MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW],
            MeetingState.COMPLETED: [MeetingState.SPEAKING, MeetingState.COMPLETED],
        }
        for state in paths.get(target, []):
            sm.transition_to(state)

    def test_is_valid_transition_method(self, state_manager: StateManager) -> None:
        """is_valid_transition should match VALID_TRANSITIONS."""
        assert state_manager.is_valid_transition(MeetingState.TRANSITION) is True
        assert state_manager.is_valid_transition(MeetingState.SPEAKING) is True
        assert state_manager.is_valid_transition(MeetingState.PAUSED) is False
        assert state_manager.is_valid_transition(MeetingState.GRACE) is False


# =============================================================================
# Test 5.T4: Observer Notification
# =============================================================================


class TestObserverNotification:
    """Test 5.T4: Observers notified on state change."""

    def test_observer_called_on_transition(self, state_manager: StateManager) -> None:
        """Observer should be called when state changes."""
        notifications: list[tuple[MeetingState, MeetingState]] = []

        def observer(old: MeetingState, new: MeetingState) -> None:
            notifications.append((old, new))

        state_manager.add_observer(observer)
        state_manager.transition_to(MeetingState.SPEAKING)

        assert len(notifications) == 1
        assert notifications[0] == (MeetingState.IDLE, MeetingState.SPEAKING)

    def test_multiple_observers_all_notified(
        self, state_manager: StateManager
    ) -> None:
        """All observers should be notified."""
        notifications1: list[MeetingState] = []
        notifications2: list[MeetingState] = []

        state_manager.add_observer(lambda _o, n: notifications1.append(n))
        state_manager.add_observer(lambda _o, n: notifications2.append(n))

        state_manager.transition_to(MeetingState.SPEAKING)

        assert len(notifications1) == 1
        assert len(notifications2) == 1

    def test_observer_receives_correct_states(
        self, state_manager: StateManager
    ) -> None:
        """Observer receives old and new state correctly."""
        transitions: list[tuple[MeetingState, MeetingState]] = []

        state_manager.add_observer(lambda o, n: transitions.append((o, n)))

        state_manager.transition_to(MeetingState.SPEAKING)
        state_manager.transition_to(MeetingState.PAUSED)
        state_manager.transition_to(MeetingState.SPEAKING)

        assert transitions == [
            (MeetingState.IDLE, MeetingState.SPEAKING),
            (MeetingState.SPEAKING, MeetingState.PAUSED),
            (MeetingState.PAUSED, MeetingState.SPEAKING),
        ]

    def test_observer_error_does_not_stop_others(
        self, state_manager: StateManager
    ) -> None:
        """One observer's error should not prevent others from being notified."""
        notifications: list[MeetingState] = []

        def bad_observer(o: MeetingState, n: MeetingState) -> None:
            raise ValueError("Observer error")

        def good_observer(o: MeetingState, n: MeetingState) -> None:
            notifications.append(n)

        state_manager.add_observer(bad_observer)
        state_manager.add_observer(good_observer)

        # Should not raise
        state_manager.transition_to(MeetingState.SPEAKING)

        # Good observer should still have been called
        assert len(notifications) == 1

    def test_observer_not_added_twice(self, state_manager: StateManager) -> None:
        """Same observer should not be added twice."""
        count = 0

        def observer(o: MeetingState, n: MeetingState) -> None:
            nonlocal count
            count += 1

        state_manager.add_observer(observer)
        state_manager.add_observer(observer)  # Same observer again

        state_manager.transition_to(MeetingState.SPEAKING)

        assert count == 1  # Only called once


# =============================================================================
# Test 5.T5: Observer Removal
# =============================================================================


class TestObserverRemoval:
    """Test 5.T5: Observer removal works correctly."""

    def test_removed_observer_not_called(self, state_manager: StateManager) -> None:
        """Removed observer should not be called."""
        notifications: list[MeetingState] = []

        def observer(o: MeetingState, n: MeetingState) -> None:
            notifications.append(n)

        state_manager.add_observer(observer)
        state_manager.transition_to(MeetingState.SPEAKING)

        assert len(notifications) == 1

        state_manager.remove_observer(observer)
        state_manager.transition_to(MeetingState.PAUSED)

        # Should still be 1, not 2
        assert len(notifications) == 1

    def test_remove_nonexistent_observer_safe(
        self, state_manager: StateManager
    ) -> None:
        """Removing a non-existent observer should not raise."""

        def observer(o: MeetingState, n: MeetingState) -> None:
            pass

        # Should not raise
        state_manager.remove_observer(observer)

    def test_remaining_observers_still_work(
        self, state_manager: StateManager
    ) -> None:
        """After removal, remaining observers should still work."""
        notifications1: list[MeetingState] = []
        notifications2: list[MeetingState] = []

        def observer1(o: MeetingState, n: MeetingState) -> None:
            notifications1.append(n)

        def observer2(o: MeetingState, n: MeetingState) -> None:
            notifications2.append(n)

        state_manager.add_observer(observer1)
        state_manager.add_observer(observer2)

        state_manager.remove_observer(observer1)
        state_manager.transition_to(MeetingState.SPEAKING)

        assert len(notifications1) == 0  # Removed
        assert len(notifications2) == 1  # Still active


# =============================================================================
# Test 5.T6: Speaker Queue Management
# =============================================================================


class TestSpeakerQueueManagement:
    """Test 5.T6: Speaker queue management (next, skip)."""

    def test_set_speaker_queue(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Can set the speaker queue."""
        state_manager.set_speaker_queue(sample_members)

        assert state_manager.total_speakers == 3
        assert state_manager.current_speaker_index == -1
        assert state_manager.current_speaker is None

    def test_advance_speaker(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Can advance through speakers."""
        state_manager.set_speaker_queue(sample_members)

        speaker1 = state_manager.advance_speaker()
        assert speaker1 is not None
        assert speaker1.id == "alice"
        assert state_manager.current_speaker_index == 0

        speaker2 = state_manager.advance_speaker()
        assert speaker2 is not None
        assert speaker2.id == "bob"
        assert state_manager.current_speaker_index == 1

    def test_advance_past_end_returns_none(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Advancing past end returns None."""
        state_manager.set_speaker_queue(sample_members)

        state_manager.advance_speaker()  # alice
        state_manager.advance_speaker()  # bob
        state_manager.advance_speaker()  # charlie

        result = state_manager.advance_speaker()  # past end
        assert result is None

    def test_skip_current_speaker(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Can skip the current speaker."""
        state_manager.set_speaker_queue(sample_members)
        state_manager.advance_speaker()

        state_manager.skip_current_speaker()

        record = state_manager.get_speaker_record("alice")
        assert record is not None
        assert record.skipped is True

    def test_reorder_speakers(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Can reorder remaining speakers."""
        state_manager.set_speaker_queue(sample_members)
        state_manager.advance_speaker()  # Now on alice

        # Reorder bob and charlie
        state_manager.reorder_speakers(["charlie", "bob"])

        # Advance to see new order
        state_manager.advance_speaker()
        assert state_manager.current_speaker is not None
        assert state_manager.current_speaker.id == "charlie"

    def test_reorder_invalid_id_raises(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Reorder with invalid ID should raise."""
        state_manager.set_speaker_queue(sample_members)

        with pytest.raises(ValueError, match="Unknown member"):
            state_manager.reorder_speakers(["alice", "invalid_id"])

    def test_remaining_speakers_count(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Remaining speakers count is accurate."""
        state_manager.set_speaker_queue(sample_members)

        assert state_manager.remaining_speakers == 3

        state_manager.advance_speaker()
        assert state_manager.remaining_speakers == 2

        state_manager.advance_speaker()
        assert state_manager.remaining_speakers == 1

        state_manager.advance_speaker()
        assert state_manager.remaining_speakers == 0


# =============================================================================
# Test 5.T7: Current Speaker Tracking
# =============================================================================


class TestCurrentSpeakerTracking:
    """Test 5.T7: Current speaker tracking accurate."""

    def test_current_speaker_property(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Current speaker property returns correct member."""
        state_manager.set_speaker_queue(sample_members)

        assert state_manager.current_speaker is None

        state_manager.advance_speaker()
        assert state_manager.current_speaker is not None
        assert state_manager.current_speaker.id == "alice"

    def test_update_speaker_time(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Can update speaker elapsed time."""
        state_manager.set_speaker_queue(sample_members)
        state_manager.advance_speaker()

        state_manager.update_speaker_time("alice", 120.5, 30.5)

        record = state_manager.get_speaker_record("alice")
        assert record is not None
        assert record.elapsed_seconds == 120.5
        assert record.overtime_seconds == 30.5

    def test_completed_speakers_list(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Completed speakers list is accurate."""
        state_manager.set_speaker_queue(sample_members)

        state_manager.advance_speaker()
        state_manager.update_speaker_time("alice", 180.0)
        state_manager.advance_speaker()
        state_manager.skip_current_speaker()  # bob skipped

        completed = state_manager.completed_speakers
        assert len(completed) == 2
        assert any(r.member.id == "alice" for r in completed)
        assert any(r.member.id == "bob" for r in completed)

    def test_speaker_queue_is_copy(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """speaker_queue property returns a copy."""
        state_manager.set_speaker_queue(sample_members)

        queue = state_manager.speaker_queue
        queue.clear()  # Modify the returned list

        # Original should be unaffected
        assert state_manager.total_speakers == 3

    def test_get_all_speaker_records(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Can get all speaker records."""
        state_manager.set_speaker_queue(sample_members)

        records = state_manager.get_all_speaker_records()
        assert len(records) == 3

    def test_get_snapshot(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Snapshot contains correct information."""
        state_manager.set_speaker_queue(sample_members)
        state_manager.transition_to(MeetingState.SPEAKING)
        state_manager.advance_speaker()
        state_manager.update_speaker_time("alice", 60.0)

        snapshot = state_manager.get_snapshot()

        assert snapshot.state == MeetingState.SPEAKING
        assert snapshot.current_speaker_index == 0
        assert snapshot.total_speakers == 3
        assert snapshot.current_speaker is not None
        assert snapshot.current_speaker.id == "alice"
        assert snapshot.elapsed_seconds == 60.0


# =============================================================================
# Test 5.T8: Absent Member Handling
# =============================================================================


class TestAbsentMemberHandling:
    """Test 5.T8: Absent member handling in queue."""

    def test_mark_absent(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Can mark a member as absent."""
        state_manager.set_speaker_queue(sample_members)

        result = state_manager.mark_absent("bob")
        assert result is True

        record = state_manager.get_speaker_record("bob")
        assert record is not None
        assert record.is_absent is True

    def test_mark_absent_invalid_id(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Marking invalid ID returns False."""
        state_manager.set_speaker_queue(sample_members)

        result = state_manager.mark_absent("nonexistent")
        assert result is False

    def test_advance_skips_absent(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Advancing skips absent members."""
        state_manager.set_speaker_queue(sample_members)
        state_manager.mark_absent("alice")

        speaker = state_manager.advance_speaker()
        assert speaker is not None
        assert speaker.id == "bob"  # Skipped alice

    def test_advance_skips_multiple_absent(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Advancing skips multiple consecutive absent members."""
        state_manager.set_speaker_queue(sample_members)
        state_manager.mark_absent("alice")
        state_manager.mark_absent("bob")

        speaker = state_manager.advance_speaker()
        assert speaker is not None
        assert speaker.id == "charlie"

    def test_unmark_absent(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Can unmark a member as absent."""
        state_manager.set_speaker_queue(sample_members)
        state_manager.mark_absent("bob")
        state_manager.unmark_absent("bob")

        record = state_manager.get_speaker_record("bob")
        assert record is not None
        assert record.is_absent is False

    def test_get_active_speakers(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Get active speakers excludes absent."""
        state_manager.set_speaker_queue(sample_members)
        state_manager.mark_absent("bob")

        active = state_manager.get_active_speakers()
        assert len(active) == 2
        assert all(m.id != "bob" for m in active)

    def test_has_more_speakers_excludes_absent(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """has_more_speakers considers absent status."""
        state_manager.set_speaker_queue(sample_members)
        state_manager.mark_absent("bob")
        state_manager.mark_absent("charlie")

        state_manager.advance_speaker()  # alice

        assert state_manager.has_more_speakers() is False

    def test_all_absent_returns_none(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Advancing when all are absent returns None."""
        state_manager.set_speaker_queue(sample_members)
        state_manager.mark_absent("alice")
        state_manager.mark_absent("bob")
        state_manager.mark_absent("charlie")

        speaker = state_manager.advance_speaker()
        assert speaker is None


# =============================================================================
# Additional Tests: Reset and Edge Cases
# =============================================================================


class TestResetAndEdgeCases:
    """Additional tests for reset and edge cases."""

    def test_reset_clears_state(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Reset clears all state."""
        state_manager.set_speaker_queue(sample_members)
        state_manager.transition_to(MeetingState.SPEAKING)
        state_manager.advance_speaker()

        state_manager.reset()

        assert state_manager.state == MeetingState.IDLE
        assert state_manager.total_speakers == 0
        assert state_manager.current_speaker_index == -1
        assert state_manager.current_speaker is None

    def test_reset_notifies_observers(
        self, state_manager: StateManager
    ) -> None:
        """Reset notifies observers of state change."""
        notifications: list[tuple[MeetingState, MeetingState]] = []

        state_manager.add_observer(lambda o, n: notifications.append((o, n)))
        state_manager.transition_to(MeetingState.SPEAKING)

        notifications.clear()
        state_manager.reset()

        assert len(notifications) == 1
        assert notifications[0] == (MeetingState.SPEAKING, MeetingState.IDLE)

    def test_reset_from_idle_no_notification(
        self, state_manager: StateManager
    ) -> None:
        """Reset from IDLE doesn't notify (no change)."""
        notifications: list[MeetingState] = []

        state_manager.add_observer(lambda _o, n: notifications.append(n))
        state_manager.reset()

        assert len(notifications) == 0

    def test_initial_state_is_idle(self, state_manager: StateManager) -> None:
        """Initial state should be IDLE."""
        assert state_manager.state == MeetingState.IDLE
        assert state_manager.current_speaker_index == -1
        assert state_manager.total_speakers == 0

    def test_speaker_record_dataclass(self, sample_members: list[TeamMember]) -> None:
        """SpeakerRecord has correct defaults."""
        record = SpeakerRecord(member=sample_members[0])

        assert record.elapsed_seconds == 0.0
        assert record.is_absent is False
        assert record.skipped is False
        assert record.overtime_seconds == 0.0


# =============================================================================
# Bug Fix Tests: Skip Speaker Edge Cases
# =============================================================================


class TestSkipSpeakerEdgeCases:
    """Test skip speaker edge cases including bug fix for elapsed time reset.

    Bug: When a speaker is skipped, their elapsed_seconds should be 0,
    not the timer value from the previous speaker.
    """

    def test_skip_resets_elapsed_time_to_zero(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """BUG FIX: Skipped speaker's elapsed time should be 0.

        Scenario: User spoke for 4:08, then skipped Chen to Guy.
        Chen's time should be 0, not 4:08+.
        """
        state_manager.set_speaker_queue(sample_members)

        # First speaker (alice) speaks for 4:08
        state_manager.advance_speaker()
        state_manager.update_speaker_time("alice", 248.0, 0.0)  # 4:08

        # Advance to second speaker (bob)
        state_manager.advance_speaker()

        # User skips bob before he speaks
        state_manager.skip_current_speaker()

        # Bob's time should be 0, not alice's time
        record = state_manager.get_speaker_record("bob")
        assert record is not None
        assert record.skipped is True
        assert record.elapsed_seconds == 0.0
        assert record.overtime_seconds == 0.0

    def test_skip_resets_overtime_to_zero(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Skipped speaker's overtime should be 0."""
        state_manager.set_speaker_queue(sample_members)
        state_manager.advance_speaker()

        # Even if someone set time before skip (edge case)
        state_manager.update_speaker_time("alice", 300.0, 120.0)  # 5 min with 2 min overtime

        # Skip alice - times should reset
        state_manager.skip_current_speaker()

        record = state_manager.get_speaker_record("alice")
        assert record is not None
        assert record.skipped is True
        assert record.elapsed_seconds == 0.0
        assert record.overtime_seconds == 0.0

    def test_skip_speaker_not_in_queue_noop(
        self, state_manager: StateManager
    ) -> None:
        """Skipping when no current speaker does nothing (no crash)."""
        # No queue set
        state_manager.skip_current_speaker()  # Should not raise

        # With empty queue
        state_manager.set_speaker_queue([])
        state_manager.skip_current_speaker()  # Should not raise

    def test_skip_multiple_speakers_consecutively(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Multiple consecutive skips should all have 0 elapsed time."""
        state_manager.set_speaker_queue(sample_members)

        # Start with alice who speaks
        state_manager.advance_speaker()
        state_manager.update_speaker_time("alice", 180.0, 0.0)

        # Advance to bob
        state_manager.advance_speaker()

        # Skip bob
        state_manager.skip_current_speaker()

        # Advance to charlie
        state_manager.advance_speaker()

        # Skip charlie too
        state_manager.skip_current_speaker()

        # Both skipped speakers should have 0 time
        bob_record = state_manager.get_speaker_record("bob")
        charlie_record = state_manager.get_speaker_record("charlie")

        assert bob_record is not None and bob_record.elapsed_seconds == 0.0
        assert charlie_record is not None and charlie_record.elapsed_seconds == 0.0

        # Alice who actually spoke should have her time
        alice_record = state_manager.get_speaker_record("alice")
        assert alice_record is not None and alice_record.elapsed_seconds == 180.0

    def test_completed_speakers_includes_skipped(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """Completed speakers list includes skipped speakers."""
        state_manager.set_speaker_queue(sample_members)
        state_manager.advance_speaker()

        state_manager.skip_current_speaker()

        completed = state_manager.completed_speakers
        assert len(completed) == 1
        assert completed[0].skipped is True

    def test_skip_after_time_was_recorded(
        self, state_manager: StateManager, sample_members: list[TeamMember]
    ) -> None:
        """If time was somehow recorded before skip, skip resets it."""
        state_manager.set_speaker_queue(sample_members)
        state_manager.advance_speaker()

        # Time recorded (maybe speaker timer update before skip)
        state_manager.update_speaker_time("alice", 100.0, 10.0)

        # Then skipped - should reset
        state_manager.skip_current_speaker()

        record = state_manager.get_speaker_record("alice")
        assert record is not None
        assert record.elapsed_seconds == 0.0
        assert record.overtime_seconds == 0.0
