"""
State manager for meeting flow control.

This module implements a state machine with observer pattern
for managing meeting states and speaker queue.
"""

import logging
from collections.abc import Callable
from dataclasses import dataclass, field

from src.core.models import MeetingState, TeamMember

logger = logging.getLogger(__name__)

# Type alias for state change callbacks
StateObserver = Callable[[MeetingState, MeetingState], None]


class InvalidStateTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""

    pass


# Valid state transitions matrix
# Key: current state, Value: set of valid next states
VALID_TRANSITIONS: dict[MeetingState, set[MeetingState]] = {
    MeetingState.IDLE: {MeetingState.TRANSITION, MeetingState.SPEAKING},
    MeetingState.TRANSITION: {MeetingState.SPEAKING, MeetingState.PAUSED, MeetingState.COMPLETED},
    MeetingState.SPEAKING: {
        MeetingState.PAUSED,
        MeetingState.GRACE,
        MeetingState.TRANSITION,
        MeetingState.COMPLETED,
    },
    MeetingState.PAUSED: {
        MeetingState.SPEAKING,
        MeetingState.GRACE,
        MeetingState.OVERFLOW,
        MeetingState.TRANSITION,
        MeetingState.COMPLETED,
    },
    MeetingState.GRACE: {
        MeetingState.SPEAKING,
        MeetingState.PAUSED,
        MeetingState.OVERFLOW,
        MeetingState.TRANSITION,
        MeetingState.COMPLETED,
    },
    MeetingState.OVERFLOW: {
        MeetingState.SPEAKING,
        MeetingState.PAUSED,
        MeetingState.TRANSITION,
        MeetingState.COMPLETED,
    },
    MeetingState.COMPLETED: set(),  # Terminal state - no transitions out
}


@dataclass
class SpeakerRecord:
    """Record of a speaker's participation in the meeting."""

    member: TeamMember
    elapsed_seconds: float = 0.0
    is_absent: bool = False
    skipped: bool = False
    overtime_seconds: float = 0.0


@dataclass
class MeetingSnapshot:
    """Snapshot of current meeting state for observers."""

    state: MeetingState
    current_speaker_index: int
    total_speakers: int
    current_speaker: TeamMember | None
    elapsed_seconds: float
    speakers: list[SpeakerRecord] = field(default_factory=list)


class StateManager:
    """
    Manages meeting state with observer pattern.

    Tracks the current meeting state, speaker queue, and notifies
    registered observers when state changes occur.
    """

    def __init__(self) -> None:
        """Initialize the state manager."""
        self._state = MeetingState.IDLE
        self._observers: list[StateObserver] = []

        # Speaker tracking
        self._speaker_queue: list[TeamMember] = []
        self._current_index: int = -1
        self._speaker_records: dict[str, SpeakerRecord] = {}

    @property
    def state(self) -> MeetingState:
        """Return the current meeting state."""
        return self._state

    @property
    def speaker_queue(self) -> list[TeamMember]:
        """Return the current speaker queue."""
        return self._speaker_queue.copy()

    @property
    def current_speaker_index(self) -> int:
        """Return the current speaker index (-1 if not started)."""
        return self._current_index

    @property
    def current_speaker(self) -> TeamMember | None:
        """Return the current speaker or None."""
        if 0 <= self._current_index < len(self._speaker_queue):
            return self._speaker_queue[self._current_index]
        return None

    @property
    def total_speakers(self) -> int:
        """Return the total number of speakers in queue."""
        return len(self._speaker_queue)

    @property
    def remaining_speakers(self) -> int:
        """Return the number of speakers yet to speak."""
        if self._current_index < 0:
            return len(self._speaker_queue)
        return max(0, len(self._speaker_queue) - self._current_index - 1)

    @property
    def completed_speakers(self) -> list[SpeakerRecord]:
        """Return records of speakers who have completed."""
        return [
            record
            for record in self._speaker_records.values()
            if record.elapsed_seconds > 0 or record.skipped or record.is_absent
        ]

    def set_speaker_queue(self, members: list[TeamMember]) -> None:
        """
        Set the speaker queue for the meeting.

        Args:
            members: List of team members in speaking order.
        """
        self._speaker_queue = members.copy()
        self._current_index = -1
        self._speaker_records = {
            member.id: SpeakerRecord(member=member) for member in members
        }
        logger.debug(f"Speaker queue set with {len(members)} members")

    def reorder_speakers(self, new_order: list[str]) -> None:
        """
        Reorder the remaining speakers.

        Args:
            new_order: List of member IDs in new order.

        Raises:
            ValueError: If new_order contains invalid member IDs.
        """
        # Validate all IDs exist
        queue_ids = {m.id for m in self._speaker_queue}
        for member_id in new_order:
            if member_id not in queue_ids:
                raise ValueError(f"Unknown member ID: {member_id}")

        # Build new queue maintaining members not in new_order at original positions
        # For speakers before current, keep as-is
        # For current and after, apply new order
        completed_part = self._speaker_queue[: self._current_index + 1]

        # Get remaining members by new order
        remaining_members = []
        for member_id in new_order:
            for member in self._speaker_queue:
                if member.id == member_id and member.id not in {
                    m.id for m in completed_part
                }:
                    remaining_members.append(member)
                    break

        self._speaker_queue = completed_part + remaining_members
        logger.debug(f"Speakers reordered: {[m.id for m in self._speaker_queue]}")

    def advance_speaker(self) -> TeamMember | None:
        """
        Advance to the next speaker in the queue.

        Returns:
            The next speaker, or None if queue exhausted.
        """
        # Skip any absent members
        next_index = self._current_index + 1

        while next_index < len(self._speaker_queue):
            member = self._speaker_queue[next_index]
            record = self._speaker_records.get(member.id)

            if record and record.is_absent:
                next_index += 1
                continue

            self._current_index = next_index
            logger.debug(f"Advanced to speaker: {member.display_name}")
            return member

        # No more speakers
        self._current_index = len(self._speaker_queue)
        logger.debug("No more speakers in queue")
        return None

    def skip_current_speaker(self) -> None:
        """Mark the current speaker as skipped.

        Resets their elapsed time to 0 since they never spoke.
        """
        if self.current_speaker:
            record = self._speaker_records.get(self.current_speaker.id)
            if record:
                record.skipped = True
                record.elapsed_seconds = 0.0  # Never spoke
                record.overtime_seconds = 0.0
                logger.debug(f"Skipped speaker: {self.current_speaker.display_name}")

    def mark_absent(self, member_id: str) -> bool:
        """
        Mark a member as absent.

        Args:
            member_id: The ID of the member to mark absent.

        Returns:
            True if member was found and marked, False otherwise.
        """
        record = self._speaker_records.get(member_id)
        if record:
            record.is_absent = True
            logger.debug(f"Marked absent: {member_id}")
            return True
        return False

    def unmark_absent(self, member_id: str) -> bool:
        """
        Unmark a member as absent.

        Args:
            member_id: The ID of the member to unmark.

        Returns:
            True if member was found and unmarked, False otherwise.
        """
        record = self._speaker_records.get(member_id)
        if record:
            record.is_absent = False
            logger.debug(f"Unmarked absent: {member_id}")
            return True
        return False

    def get_active_speakers(self) -> list[TeamMember]:
        """Return speakers who are not marked absent."""
        return [
            member
            for member in self._speaker_queue
            if not self._speaker_records.get(member.id, SpeakerRecord(member=member)).is_absent
        ]

    def update_speaker_time(
        self,
        member_id: str,
        elapsed_seconds: float,
        overtime_seconds: float = 0.0,
    ) -> None:
        """
        Update the elapsed time for a speaker.

        Args:
            member_id: The speaker's ID.
            elapsed_seconds: Total elapsed time in seconds.
            overtime_seconds: Overtime amount in seconds.
        """
        record = self._speaker_records.get(member_id)
        if record:
            record.elapsed_seconds = elapsed_seconds
            record.overtime_seconds = overtime_seconds

    def get_speaker_record(self, member_id: str) -> SpeakerRecord | None:
        """
        Get the record for a specific speaker.

        Args:
            member_id: The speaker's ID.

        Returns:
            The SpeakerRecord or None if not found.
        """
        return self._speaker_records.get(member_id)

    def get_all_speaker_records(self) -> list[SpeakerRecord]:
        """Return all speaker records."""
        return list(self._speaker_records.values())

    def is_valid_transition(self, to_state: MeetingState) -> bool:
        """
        Check if a transition to the given state is valid.

        Args:
            to_state: The target state.

        Returns:
            True if the transition is valid.
        """
        valid_targets = VALID_TRANSITIONS.get(self._state, set())
        return to_state in valid_targets

    def transition_to(self, new_state: MeetingState) -> None:
        """
        Transition to a new state.

        Args:
            new_state: The target state.

        Raises:
            InvalidStateTransitionError: If the transition is not valid.
        """
        if not self.is_valid_transition(new_state):
            raise InvalidStateTransitionError(
                f"Cannot transition from {self._state.value} to {new_state.value}"
            )

        old_state = self._state
        self._state = new_state
        logger.info(f"STATE TRANSITION: {old_state.value} -> {new_state.value}")

        self._notify_observers(old_state, new_state)

    def add_observer(self, callback: StateObserver) -> None:
        """
        Register an observer for state changes.

        Args:
            callback: Function called with (old_state, new_state) on changes.
        """
        if callback not in self._observers:
            self._observers.append(callback)
            logger.debug(f"Added observer: {callback}")

    def remove_observer(self, callback: StateObserver) -> None:
        """
        Unregister an observer.

        Args:
            callback: The callback to remove.
        """
        if callback in self._observers:
            self._observers.remove(callback)
            logger.debug(f"Removed observer: {callback}")

    def _notify_observers(
        self, old_state: MeetingState, new_state: MeetingState
    ) -> None:
        """Notify all registered observers of a state change."""
        for observer in self._observers:
            try:
                observer(old_state, new_state)
            except Exception as e:
                logger.error(f"Observer error: {e}")

    def get_snapshot(self) -> MeetingSnapshot:
        """
        Get a snapshot of the current meeting state.

        Returns:
            A MeetingSnapshot with current state information.
        """
        current = self.current_speaker
        elapsed = 0.0
        if current:
            record = self._speaker_records.get(current.id)
            if record:
                elapsed = record.elapsed_seconds

        return MeetingSnapshot(
            state=self._state,
            current_speaker_index=self._current_index,
            total_speakers=len(self._speaker_queue),
            current_speaker=current,
            elapsed_seconds=elapsed,
            speakers=list(self._speaker_records.values()),
        )

    def reset(self) -> None:
        """Reset the state manager to initial state."""
        old_state = self._state
        self._state = MeetingState.IDLE
        self._speaker_queue = []
        self._current_index = -1
        self._speaker_records = {}

        if old_state != MeetingState.IDLE:
            self._notify_observers(old_state, MeetingState.IDLE)

        logger.debug("State manager reset")

    def has_more_speakers(self) -> bool:
        """Check if there are more speakers to process."""
        # Check remaining speakers after current index
        for i in range(self._current_index + 1, len(self._speaker_queue)):
            member = self._speaker_queue[i]
            record = self._speaker_records.get(member.id)
            if record and not record.is_absent:
                return True
        return False
