"""
Meeting manager for orchestrating daily standup meetings.

This module coordinates the timer, state machine, and data repositories
to manage the complete lifecycle of a standup meeting.
"""

import logging
import uuid
from collections.abc import Callable
from datetime import datetime

from src.core.constants import MAX_MEETING_DURATION_SECONDS, SESSION_ID_LENGTH
from src.core.models import (
    AppConfig,
    CompletedSpeakerRecord,
    MeetingRecord,
    MeetingState,
    MeetingStatus,
    ParticipantRecord,
    ParticipantStatus,
    SessionRecovery,
    TeamMember,
)
from src.core.state_manager import StateManager, SpeakerRecord
from src.core.timer_engine import TimerEngine
from src.data.history_repository import HistoryRepository
from src.data.recovery_manager import RecoveryManager
from src.data.team_repository import TeamRepository

logger = logging.getLogger(__name__)

# Type alias for meeting event callbacks
MeetingObserver = Callable[[str, dict[str, object]], None]


class MeetingManager:
    """
    Orchestrates daily standup meeting flow.

    Coordinates timer, state machine, and repositories to manage
    the complete meeting lifecycle including speaker transitions,
    pauses, and recovery.
    """

    def __init__(
        self,
        team_repo: TeamRepository,
        config: AppConfig,
        history_repo: HistoryRepository,
        recovery_mgr: RecoveryManager,
    ) -> None:
        """
        Initialize the meeting manager.

        Args:
            team_repo: Repository for team data.
            config: Application configuration.
            history_repo: Repository for meeting history.
            recovery_mgr: Manager for crash recovery.
        """
        self._team_repo = team_repo
        self._config = config
        self._history_repo = history_repo
        self._recovery_mgr = recovery_mgr

        # Core components
        self._state_manager = StateManager()
        self._speaker_timer: TimerEngine | None = None
        self._transition_timer: TimerEngine | None = None
        self._meeting_timer: TimerEngine | None = None

        # Meeting metadata
        self._session_id: str | None = None
        self._team_id: str | None = None
        self._started_at: datetime | None = None

        # Observers
        self._observers: list[MeetingObserver] = []

        # Grace period tracking
        self._in_grace_period = False
        self._grace_notified = False

        # Overflow period tracking
        self._in_overflow_period = False
        self._overflow_notified = False

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def state(self) -> MeetingState:
        """Return the current meeting state."""
        return self._state_manager.state

    @property
    def is_active(self) -> bool:
        """Check if a meeting is currently active."""
        return self._state_manager.state not in (
            MeetingState.IDLE,
            MeetingState.COMPLETED,
        )

    @property
    def session_id(self) -> str | None:
        """Return the current session ID."""
        return self._session_id

    @property
    def team_id(self) -> str | None:
        """Return the current team ID."""
        return self._team_id

    @property
    def current_speaker(self) -> TeamMember | None:
        """Return the current speaker."""
        return self._state_manager.current_speaker

    @property
    def speaker_queue(self) -> list[TeamMember]:
        """Return the speaker queue."""
        return self._state_manager.speaker_queue

    @property
    def current_speaker_index(self) -> int:
        """Return the current speaker index."""
        return self._state_manager.current_speaker_index

    @property
    def total_speakers(self) -> int:
        """Return the total number of speakers."""
        return self._state_manager.total_speakers

    @property
    def remaining_speakers(self) -> int:
        """Return the number of remaining speakers."""
        return self._state_manager.remaining_speakers

    @property
    def speaker_time_remaining(self) -> float:
        """Return remaining time for current speaker in seconds (negative when overtime)."""
        if self._speaker_timer is None:
            return 0.0
        return self._speaker_timer.remaining_seconds  # Allow negative for overtime display

    @property
    def speaker_time_elapsed(self) -> float:
        """Return elapsed time for current speaker in seconds."""
        if self._speaker_timer is None:
            return 0.0
        return self._speaker_timer.elapsed_seconds

    @property
    def transition_time_remaining(self) -> float:
        """Return remaining transition time in seconds."""
        if self._transition_timer is None:
            return 0.0
        return max(0.0, self._transition_timer.remaining_seconds)

    @property
    def meeting_elapsed(self) -> float:
        """Return total meeting elapsed time in seconds."""
        if self._meeting_timer is None:
            return 0.0
        return self._meeting_timer.elapsed_seconds

    @property
    def is_overtime(self) -> bool:
        """Check if current speaker is in overtime."""
        if self._speaker_timer is None:
            return False
        return self._speaker_timer.is_overtime

    @property
    def overtime_seconds(self) -> float:
        """Return overtime amount for current speaker."""
        if self._speaker_timer is None:
            return 0.0
        return self._speaker_timer.overtime_seconds

    def get_all_speaker_records(self) -> list[SpeakerRecord]:
        """
        Get all speaker records for the current meeting.

        Returns:
            List of SpeakerRecord objects with timing information.
        """
        return self._state_manager.get_all_speaker_records()

    @property
    def transition_time_seconds(self) -> int:
        """Return configured transition time in seconds."""
        return self._config.timer.transition_time_seconds

    @property
    def default_speaker_time_seconds(self) -> int:
        """Return default speaker time in seconds."""
        return self._config.timer.default_speaker_time_seconds

    # =========================================================================
    # Meeting Lifecycle
    # =========================================================================

    def start_meeting(
        self,
        team_id: str | None = None,
        speaker_order: list[str] | None = None,
    ) -> None:
        """
        Start a new meeting.

        Args:
            team_id: Team identifier. Uses default if not provided.
            speaker_order: Optional custom speaker order (list of member IDs).

        Raises:
            RuntimeError: If a meeting is already in progress.
            ValueError: If team not found or no active members.
        """
        if self.is_active:
            raise RuntimeError("A meeting is already in progress")

        # Determine team
        team_id = team_id or self._config.teams.default_team
        if not team_id:
            raise ValueError("No team specified and no default configured")

        # Load team members
        members = self._team_repo.get_active_members(team_id)
        if not members:
            raise ValueError(f"No active members in team: {team_id}")

        # Apply custom order if provided
        if speaker_order:
            ordered_members = []
            for member_id in speaker_order:
                member = self._team_repo.get_member_by_id(team_id, member_id)
                if member and member in members:
                    ordered_members.append(member)
            members = ordered_members if ordered_members else members

        # Initialize session
        self._session_id = str(uuid.uuid4())[:SESSION_ID_LENGTH]
        self._team_id = team_id
        self._started_at = datetime.now()
        self._in_grace_period = False
        self._grace_notified = False
        self._in_overflow_period = False
        self._overflow_notified = False

        # Setup state manager
        self._state_manager.reset()
        self._state_manager.set_speaker_queue(members)

        # Initialize meeting timer
        self._meeting_timer = TimerEngine(duration_seconds=MAX_MEETING_DURATION_SECONDS)
        self._meeting_timer.start()

        # Start recovery auto-save
        self._recovery_mgr.start_auto_save(self._get_recovery_state)

        # Advance to first speaker and start transition
        self._state_manager.advance_speaker()
        self._start_transition()

        logger.info(f"Meeting started: {self._session_id} with {len(members)} speakers")
        self._notify_observers("meeting_started", {"team_id": team_id})

    def end_meeting(self, save_history: bool = True) -> MeetingRecord | None:
        """
        End the current meeting.

        Args:
            save_history: Whether to save the meeting to history.

        Returns:
            The meeting record if saved, None otherwise.
        """
        if not self.is_active and self._state_manager.state != MeetingState.COMPLETED:
            logger.warning("No active meeting to end")
            return None

        # Stop all timers
        self._stop_all_timers()

        # Update final speaker time if applicable
        self._finalize_current_speaker()

        # Build meeting record
        record = self._build_meeting_record()

        # Save to history
        if save_history and record:
            self._history_repo.save_entry(record)
            logger.info(f"Meeting record saved: {record.id}")

        # Clear recovery
        self._recovery_mgr.clear_recovery()

        # Transition to completed
        if self._state_manager.state != MeetingState.COMPLETED:
            self._state_manager.transition_to(MeetingState.COMPLETED)

        logger.info(f"Meeting ended: {self._session_id}")
        self._notify_observers("meeting_ended", {"record_id": record.id if record else None})

        # Reset session data
        self._session_id = None
        self._team_id = None
        self._started_at = None

        return record

    # =========================================================================
    # Speaker Control
    # =========================================================================

    def next_speaker(self) -> TeamMember | None:
        """
        Advance to the next speaker.

        Returns:
            The next speaker, or None if meeting complete.
        """
        if not self.is_active:
            return None

        # Finalize current speaker's time
        self._finalize_current_speaker()

        # Advance queue
        next_member = self._state_manager.advance_speaker()

        if next_member is None:
            # No more speakers - end meeting
            self.end_meeting()
            return None

        # Start transition period
        self._start_transition()

        logger.debug(f"Next speaker: {next_member.display_name}")
        return next_member

    def skip_speaker(self) -> TeamMember | None:
        """
        Skip the current speaker and move to next.

        Returns:
            The next speaker, or None if meeting complete.
        """
        if not self.is_active:
            return None

        current = self.current_speaker
        if current:
            self._state_manager.skip_current_speaker()
            logger.info(f"Skipped speaker: {current.display_name}")
            self._notify_observers("speaker_skipped", {"member_id": current.id})

        return self.next_speaker()

    def mark_absent(self, member_id: str) -> bool:
        """
        Mark a member as absent.

        Args:
            member_id: The member ID to mark absent.

        Returns:
            True if marked successfully.
        """
        result = self._state_manager.mark_absent(member_id)
        if result:
            self._notify_observers("member_absent", {"member_id": member_id})

            # If current speaker is now absent, advance
            if self.current_speaker and self.current_speaker.id == member_id:
                self.next_speaker()

        return result

    def unmark_absent(self, member_id: str) -> bool:
        """
        Unmark a member as absent.

        Args:
            member_id: The member ID to unmark.

        Returns:
            True if unmarked successfully.
        """
        return self._state_manager.unmark_absent(member_id)

    def reorder_speakers(self, new_order: list[str]) -> None:
        """
        Reorder the remaining speakers.

        Args:
            new_order: List of member IDs in new order.
        """
        self._state_manager.reorder_speakers(new_order)
        self._notify_observers("speakers_reordered", {"new_order": new_order})

    # =========================================================================
    # Timer Control
    # =========================================================================

    def pause(self) -> None:
        """Pause the meeting and all timers."""
        if self._state_manager.state not in (MeetingState.SPEAKING, MeetingState.GRACE, MeetingState.OVERFLOW):
            logger.warning(f"Cannot pause in state: {self._state_manager.state}")
            return

        # Pause speaker timer
        if self._speaker_timer and self._speaker_timer.is_running:
            self._speaker_timer.pause()

        # Pause meeting timer
        if self._meeting_timer and self._meeting_timer.is_running:
            self._meeting_timer.pause()

        self._state_manager.transition_to(MeetingState.PAUSED)
        self._notify_observers("meeting_paused", {})

    def resume(self) -> None:
        """Resume the meeting from pause."""
        if self._state_manager.state != MeetingState.PAUSED:
            logger.warning("Meeting is not paused")
            return

        # Resume timers
        if self._speaker_timer and self._speaker_timer.is_paused:
            self._speaker_timer.resume()

        if self._meeting_timer and self._meeting_timer.is_paused:
            self._meeting_timer.resume()

        # Return to appropriate state
        if self._in_overflow_period:
            self._state_manager.transition_to(MeetingState.OVERFLOW)
        elif self._in_grace_period:
            self._state_manager.transition_to(MeetingState.GRACE)
        else:
            self._state_manager.transition_to(MeetingState.SPEAKING)

        self._notify_observers("meeting_resumed", {})

    def add_time(self, seconds: int) -> None:
        """
        Add time to the current speaker.

        Args:
            seconds: Seconds to add (can be negative).
        """
        if self._speaker_timer is None:
            return

        try:
            self._speaker_timer.add_time(seconds)
            self._notify_observers("time_added", {"seconds": seconds})

            # Reset grace period if we added time and were in overtime
            if seconds > 0 and self._in_grace_period:
                self._in_grace_period = False
                self._grace_notified = False
                if self._state_manager.state == MeetingState.GRACE:
                    self._state_manager.transition_to(MeetingState.SPEAKING)

        except ValueError as e:
            logger.warning(f"Cannot add time: {e}")

    # =========================================================================
    # Transition and Grace Period
    # =========================================================================

    def _start_transition(self) -> None:
        """Start the transition period before a speaker."""
        transition_seconds = self._config.timer.transition_time_seconds
        if self._speaker_timer:
            # Clear previous speaker timer so elapsed doesn't leak into queue display.
            self._speaker_timer.stop()
            self._speaker_timer = None

        if transition_seconds > 0:
            self._transition_timer = TimerEngine(duration_seconds=transition_seconds)
            self._transition_timer.start()

            # Only transition if not already in transition state
            if self._state_manager.state != MeetingState.TRANSITION:
                self._state_manager.transition_to(MeetingState.TRANSITION)

            self._notify_observers("transition_started", {
                "next_speaker": self.current_speaker.display_name if self.current_speaker else None
            })
        else:
            # No transition period - go directly to speaking
            self._start_speaking()

    def start_speaking(self) -> None:
        """
        Start the speaking period for current speaker.

        Call this after transition period completes.
        """
        self._start_speaking()

    def _start_speaking(self) -> None:
        """Internal: Start the speaking timer for current speaker."""
        if self.current_speaker is None:
            return

        # Stop transition timer if running
        if self._transition_timer and self._transition_timer.is_running:
            self._transition_timer.stop()

        # Get speaker's configured time
        speaker_time = self._config.timer.default_speaker_time_seconds
        if self.current_speaker.daily_config:
            speaker_time = self.current_speaker.daily_config.default_time_seconds

        # Create and start speaker timer
        self._speaker_timer = TimerEngine(duration_seconds=speaker_time)
        self._speaker_timer.start()

        self._in_grace_period = False
        self._grace_notified = False
        self._in_overflow_period = False
        self._overflow_notified = False

        if self._state_manager.state != MeetingState.SPEAKING:
            self._state_manager.transition_to(MeetingState.SPEAKING)

        self._notify_observers("speaking_started", {
            "speaker": self.current_speaker.display_name,
            "duration": speaker_time,
        })

    def check_grace_period(self) -> bool:
        """
        Check if grace period should be triggered.

        Returns:
            True if in grace period.
        """
        if self._speaker_timer is None:
            logger.debug("check_grace_period: no speaker timer")
            return False

        overtime = self._speaker_timer.overtime_seconds
        is_overtime = self._speaker_timer.is_overtime
        current_state = self._state_manager.state

        if is_overtime and not self._in_grace_period:
            self._in_grace_period = True
            logger.info(f"Entering grace period at overtime={overtime:.1f}s")

            if current_state == MeetingState.SPEAKING:
                logger.info(f"Transitioning from SPEAKING to GRACE")
                self._state_manager.transition_to(MeetingState.GRACE)

            if not self._grace_notified:
                self._grace_notified = True
                self._notify_observers("grace_period_started", {
                    "overtime": overtime
                })

        # Check for overflow period (after grace period threshold)
        self.check_overflow_period()

        return self._in_grace_period

    def check_overflow_period(self) -> bool:
        """
        Check if overflow period should be triggered.

        Overflow occurs after grace_period + overflow_period seconds of overtime.

        Returns:
            True if in overflow period.
        """
        if self._speaker_timer is None:
            logger.debug("check_overflow_period: no speaker timer")
            return False

        grace_limit = self._config.timer.grace_period_seconds
        overflow_period = self._config.timer.overflow_period_seconds
        overflow_threshold = grace_limit + overflow_period
        overtime = self._speaker_timer.overtime_seconds
        is_overtime = self._speaker_timer.is_overtime
        current_state = self._state_manager.state

        if (
            is_overtime
            and overtime >= overflow_threshold
            and not self._in_overflow_period
        ):
            self._in_overflow_period = True
            logger.info(
                f"Entering overflow period at overtime={overtime:.1f}s "
                f"(threshold was {overflow_threshold}s)"
            )

            if current_state in (MeetingState.GRACE, MeetingState.SPEAKING):
                logger.info(f"Transitioning from {current_state.value} to OVERFLOW")
                self._state_manager.transition_to(MeetingState.OVERFLOW)

            if not self._overflow_notified:
                self._overflow_notified = True
                self._notify_observers("overflow_period_started", {
                    "overtime": overtime
                })

        return self._in_overflow_period

    def should_auto_advance(self) -> bool:
        """
        Check if we should auto-advance to next speaker.

        Returns:
            True if grace period exceeded.
        """
        if not self._in_grace_period or self._speaker_timer is None:
            return False

        grace_limit = self._config.timer.grace_period_seconds
        return self._speaker_timer.overtime_seconds >= grace_limit

    # =========================================================================
    # Recovery
    # =========================================================================

    def check_recovery(self) -> bool:
        """
        Check if a recovery session exists.

        Returns:
            True if recovery data is available.
        """
        return self._recovery_mgr.has_recovery()

    def get_recovery_info(self) -> dict[str, str] | None:
        """
        Get information about the recovery session.

        Returns:
            Dictionary with recovery info or None.
        """
        return self._recovery_mgr.get_recovery_info()

    def restore_session(self) -> bool:
        """
        Restore a previous session from recovery.

        Returns:
            True if restoration successful.
        """
        recovery = self._recovery_mgr.load_recovery()
        if recovery is None:
            return False

        try:
            # Restore session metadata
            self._session_id = recovery.session_id
            self._team_id = recovery.team_id
            self._started_at = datetime.fromisoformat(recovery.started_at)

            # Load team members
            members = self._team_repo.get_active_members(recovery.team_id)
            if not members:
                logger.error(f"No active members for team: {recovery.team_id}")
                return False

            # Setup state manager
            self._state_manager.reset()
            self._state_manager.set_speaker_queue(members)

            # Restore completed speakers
            for completed in recovery.completed_speakers:
                self._state_manager.update_speaker_time(
                    completed.member_id,
                    completed.actual_time_seconds,
                    0.0,  # Overtime not stored in recovery
                )

            # Advance to current position
            for _ in range(recovery.current_speaker_index + 1):
                self._state_manager.advance_speaker()

            # Restore meeting timer
            self._meeting_timer = TimerEngine(duration_seconds=MAX_MEETING_DURATION_SECONDS)
            self._meeting_timer.start()

            # Restore speaker timer with remaining time
            if self.current_speaker:
                speaker_time = self._config.timer.default_speaker_time_seconds
                if self.current_speaker.daily_config:
                    speaker_time = self.current_speaker.daily_config.default_time_seconds

                elapsed = recovery.current_speaker_elapsed_seconds
                remaining = speaker_time - elapsed
                self._speaker_timer = TimerEngine(duration_seconds=max(1, int(speaker_time)))
                self._speaker_timer.start()

                # Adjust for elapsed time
                if remaining < speaker_time:
                    self._speaker_timer.add_time(-int(speaker_time - remaining))

            # Restore state
            self._state_manager.transition_to(recovery.state)

            # Restart auto-save
            self._recovery_mgr.start_auto_save(self._get_recovery_state)

            logger.info(f"Session restored: {self._session_id}")
            self._notify_observers("session_restored", {"session_id": self._session_id})
            return True

        except Exception as e:
            logger.error(f"Failed to restore session: {e}")
            self.discard_recovery()
            return False

    def discard_recovery(self) -> None:
        """Discard the recovery data and start fresh."""
        self._recovery_mgr.clear_recovery()
        self._state_manager.reset()
        logger.info("Recovery data discarded")

    def _get_recovery_state(self) -> SessionRecovery | None:
        """Build current session state for recovery."""
        if not self.is_active or self._session_id is None:
            return None

        completed: list[CompletedSpeakerRecord] = []
        for record in self._state_manager.completed_speakers:
            completed.append(CompletedSpeakerRecord(
                member_id=record.member.id,
                actual_time_seconds=record.elapsed_seconds,
            ))

        # Build speaker order list
        speaker_order = [m.id for m in self._state_manager.speaker_queue]

        # Get absent members
        absent_members = [
            r.member.id
            for r in self._state_manager.get_all_speaker_records()
            if r.is_absent
        ]

        return SessionRecovery(
            session_id=self._session_id,
            team_id=self._team_id or "",
            started_at=self._started_at.isoformat() if self._started_at else "",
            last_updated=datetime.now().isoformat(),
            global_elapsed_seconds=self.meeting_elapsed,
            current_speaker_index=max(0, self._state_manager.current_speaker_index),
            speaker_order=speaker_order,
            completed_speakers=completed,
            current_speaker_elapsed_seconds=self.speaker_time_elapsed,
            is_in_transition=self._state_manager.state == MeetingState.TRANSITION,
            is_paused=self._state_manager.state == MeetingState.PAUSED,
            absent_members=absent_members,
            state=self._state_manager.state,
        )

    # =========================================================================
    # Observers
    # =========================================================================

    def add_observer(self, callback: MeetingObserver) -> None:
        """Register an observer for meeting events."""
        if callback not in self._observers:
            self._observers.append(callback)

    def remove_observer(self, callback: MeetingObserver) -> None:
        """Unregister an observer."""
        if callback in self._observers:
            self._observers.remove(callback)

    def _notify_observers(self, event: str, data: dict[str, object]) -> None:
        """Notify all observers of an event."""
        for observer in self._observers:
            try:
                observer(event, data)
            except Exception as e:
                logger.error(f"Observer error: {e}")

    # =========================================================================
    # Internal Helpers
    # =========================================================================

    def _stop_all_timers(self) -> None:
        """Stop all running timers."""
        if self._speaker_timer and self._speaker_timer.is_running:
            self._speaker_timer.stop()
        if self._transition_timer and self._transition_timer.is_running:
            self._transition_timer.stop()
        if self._meeting_timer and self._meeting_timer.is_running:
            self._meeting_timer.stop()

        self._recovery_mgr.stop_auto_save()

    def _finalize_current_speaker(self) -> None:
        """Save current speaker's final time.

        Note: Skipped speakers are not finalized with timer values since
        they never actually spoke. The skip_current_speaker() method
        resets their time to 0.
        """
        if self.current_speaker and self._speaker_timer:
            # Don't overwrite time for skipped speakers - they never spoke
            record = self._state_manager.get_speaker_record(self.current_speaker.id)
            if record and record.skipped:
                return

            self._state_manager.update_speaker_time(
                self.current_speaker.id,
                self._speaker_timer.elapsed_seconds,
                self._speaker_timer.overtime_seconds,
            )

    def _build_meeting_record(self) -> MeetingRecord | None:
        """Build a meeting record from current state."""
        if self._started_at is None or self._team_id is None:
            return None

        ended_at = datetime.now()

        # Build participant records
        participants = []
        position = 1
        total_expected = 0

        for record in self._state_manager.get_all_speaker_records():
            if record.is_absent:
                status = ParticipantStatus.ABSENT
            elif record.skipped:
                status = ParticipantStatus.SKIPPED
            else:
                status = ParticipantStatus.PRESENT

            # Get allocated time from member config
            allocated = self._config.timer.default_speaker_time_seconds
            if record.member.daily_config:
                allocated = record.member.daily_config.default_time_seconds

            if not record.is_absent:
                total_expected += allocated

            participants.append(ParticipantRecord(
                member_id=record.member.id,
                display_name=record.member.display_name,
                status=status,
                allocated_time_seconds=allocated,
                actual_time_seconds=record.elapsed_seconds,
                overtime_seconds=record.overtime_seconds,
                order_position=position,
            ))
            position += 1

        return MeetingRecord(
            id=self._started_at.strftime("%Y-%m-%dT%H:%M:%S"),
            date=self._started_at.strftime("%Y-%m-%d"),
            start_time=self._started_at.strftime("%H:%M:%S"),
            end_time=ended_at.strftime("%H:%M:%S"),
            total_duration_seconds=self.meeting_elapsed,
            expected_duration_seconds=total_expected,
            status=MeetingStatus.COMPLETED,
            participants=participants,
            team_id=self._team_id,
        )
