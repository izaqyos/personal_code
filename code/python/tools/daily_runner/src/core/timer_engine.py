"""
Timer engine for accurate countdown timing.

This module provides a high-precision timer using monotonic time
to prevent drift and ensure accurate time tracking for speakers.
"""

import logging
import time
from enum import Enum

logger = logging.getLogger(__name__)


class TimerState(Enum):
    """Possible states for the timer."""

    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


class TimerEngine:
    """
    High-precision countdown timer with pause/resume support.

    Uses time.monotonic() for drift-resistant timing that is
    not affected by system clock changes.
    """

    def __init__(self, duration_seconds: int) -> None:
        """
        Initialize the timer.

        Args:
            duration_seconds: Total time for the countdown in seconds.

        Raises:
            ValueError: If duration is not positive.
        """
        if duration_seconds <= 0:
            raise ValueError("Duration must be positive")

        self._initial_duration = duration_seconds
        self._duration = float(duration_seconds)
        self._state = TimerState.IDLE

        # Time tracking using monotonic clock
        self._start_time: float | None = None
        self._pause_time: float | None = None
        self._accumulated_elapsed: float = 0.0

    @property
    def initial_duration(self) -> int:
        """Return the original duration in seconds."""
        return self._initial_duration

    @property
    def duration(self) -> float:
        """Return the current total duration (may include added time)."""
        return self._duration

    @property
    def state(self) -> TimerState:
        """Return the current timer state."""
        return self._state

    @property
    def is_running(self) -> bool:
        """Check if the timer is currently running."""
        return self._state == TimerState.RUNNING

    @property
    def is_paused(self) -> bool:
        """Check if the timer is currently paused."""
        return self._state == TimerState.PAUSED

    @property
    def is_idle(self) -> bool:
        """Check if the timer has not been started."""
        return self._state == TimerState.IDLE

    @property
    def is_stopped(self) -> bool:
        """Check if the timer has been stopped."""
        return self._state == TimerState.STOPPED

    @property
    def elapsed_seconds(self) -> float:
        """
        Return the total elapsed time in seconds.

        Accounts for pause periods and uses monotonic time.
        """
        if self._state == TimerState.IDLE:
            return 0.0

        if self._state == TimerState.PAUSED or self._state == TimerState.STOPPED:
            return self._accumulated_elapsed

        if self._start_time is None:
            return 0.0

        current_elapsed = time.monotonic() - self._start_time
        return self._accumulated_elapsed + current_elapsed

    @property
    def remaining_seconds(self) -> float:
        """
        Return the remaining time in seconds.

        Returns negative values when in overtime.
        """
        return self._duration - self.elapsed_seconds

    @property
    def is_overtime(self) -> bool:
        """Check if the timer has exceeded the allocated time."""
        return self.remaining_seconds < 0

    @property
    def overtime_seconds(self) -> float:
        """
        Return the overtime amount in seconds.

        Returns 0.0 if not in overtime.
        """
        if not self.is_overtime:
            return 0.0
        return abs(self.remaining_seconds)

    def start(self) -> None:
        """
        Start the timer countdown.

        Raises:
            RuntimeError: If timer is already running.
        """
        if self._state == TimerState.RUNNING:
            raise RuntimeError("Timer is already running")

        if self._state == TimerState.PAUSED:
            raise RuntimeError("Timer is paused, use resume() instead")

        self._state = TimerState.RUNNING
        self._start_time = time.monotonic()
        self._accumulated_elapsed = 0.0
        logger.debug(f"Timer started: {self._duration}s")

    def pause(self) -> None:
        """
        Pause the timer.

        Raises:
            RuntimeError: If timer is not running.
        """
        if self._state != TimerState.RUNNING:
            raise RuntimeError("Timer is not running")

        if self._start_time is not None:
            current_elapsed = time.monotonic() - self._start_time
            self._accumulated_elapsed += current_elapsed

        self._pause_time = time.monotonic()
        self._state = TimerState.PAUSED
        logger.debug(f"Timer paused at {self._accumulated_elapsed:.2f}s")

    def resume(self) -> None:
        """
        Resume the timer from pause.

        Raises:
            RuntimeError: If timer is not paused.
        """
        if self._state != TimerState.PAUSED:
            raise RuntimeError("Timer is not paused")

        self._start_time = time.monotonic()
        self._pause_time = None
        self._state = TimerState.RUNNING
        logger.debug(f"Timer resumed, accumulated: {self._accumulated_elapsed:.2f}s")

    def stop(self) -> None:
        """
        Stop the timer permanently.

        The timer cannot be resumed after stopping.
        """
        if self._state == TimerState.RUNNING and self._start_time is not None:
            current_elapsed = time.monotonic() - self._start_time
            self._accumulated_elapsed += current_elapsed

        self._state = TimerState.STOPPED
        self._start_time = None
        self._pause_time = None
        logger.debug(f"Timer stopped at {self._accumulated_elapsed:.2f}s")

    def reset(self, new_duration: int | None = None) -> None:
        """
        Reset the timer to initial state.

        Args:
            new_duration: Optional new duration. Uses initial if not provided.
        """
        if new_duration is not None:
            if new_duration <= 0:
                raise ValueError("Duration must be positive")
            self._initial_duration = new_duration
            self._duration = float(new_duration)
        else:
            self._duration = float(self._initial_duration)

        self._state = TimerState.IDLE
        self._start_time = None
        self._pause_time = None
        self._accumulated_elapsed = 0.0
        logger.debug(f"Timer reset to {self._duration}s")

    def add_time(self, seconds: int) -> None:
        """
        Add (or subtract) time from the timer.

        Args:
            seconds: Seconds to add. Can be negative to subtract.

        Raises:
            ValueError: If resulting duration would be non-positive.
        """
        new_duration = self._duration + seconds
        if new_duration <= 0:
            raise ValueError("Cannot reduce duration below zero")

        self._duration = new_duration
        logger.debug(f"Timer adjusted by {seconds}s, new duration: {self._duration}s")

    def get_progress(self) -> float:
        """
        Return the progress as a percentage (0.0 to 1.0+).

        Values over 1.0 indicate overtime.
        """
        if self._duration <= 0:
            return 1.0
        return self.elapsed_seconds / self._duration

    def format_remaining(self) -> str:
        """
        Format the remaining time as MM:SS.

        Negative times are shown with a leading minus sign.
        """
        remaining = self.remaining_seconds
        is_negative = remaining < 0
        abs_remaining = abs(remaining)

        minutes = int(abs_remaining // 60)
        seconds = int(abs_remaining % 60)

        if is_negative:
            return f"-{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"

    def format_elapsed(self) -> str:
        """Format the elapsed time as MM:SS."""
        elapsed = self.elapsed_seconds
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        return f"{minutes:02d}:{seconds:02d}"
