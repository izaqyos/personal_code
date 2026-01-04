"""
Unit tests for the Timer Engine.

Test coverage for Phase 4:
- 4.T1: Timer counts down correctly over 10 seconds
- 4.T2: Timer accuracy < 100ms drift over 60 seconds
- 4.T3: Pause freezes elapsed time
- 4.T4: Resume continues accurately after pause
- 4.T5: Multiple pause/resume cycles maintain accuracy
- 4.T6: Add time extends remaining correctly
- 4.T7: Overtime detected when remaining < 0
- 4.T8: Reset restores initial state
- 4.T9: Cannot start already running timer
- 4.T10: Cannot resume non-paused timer
"""

import time

import pytest

from src.core.timer_engine import TimerEngine, TimerState

# =============================================================================
# Test 4.T1: Timer Countdown
# =============================================================================


class TestTimerCountdown:
    """Test 4.T1: Timer counts down correctly."""

    def test_initial_state(self) -> None:
        """Timer should start in IDLE state with correct duration."""
        timer = TimerEngine(180)

        assert timer.state == TimerState.IDLE
        assert timer.is_idle is True
        assert timer.is_running is False
        assert timer.is_paused is False
        assert timer.initial_duration == 180
        assert timer.duration == 180.0
        assert timer.elapsed_seconds == 0.0
        assert timer.remaining_seconds == 180.0

    def test_countdown_over_short_period(self) -> None:
        """Timer should count down correctly over a short period."""
        timer = TimerEngine(10)
        timer.start()

        assert timer.is_running is True
        assert timer.state == TimerState.RUNNING

        # Wait a short time
        time.sleep(0.1)

        elapsed = timer.elapsed_seconds
        remaining = timer.remaining_seconds

        # Elapsed should be approximately 0.1 seconds (with tolerance)
        assert 0.08 <= elapsed <= 0.15
        # Remaining should be duration minus elapsed
        assert abs(remaining - (10.0 - elapsed)) < 0.01

    def test_countdown_tracks_time(self) -> None:
        """Timer should track elapsed time accurately."""
        timer = TimerEngine(60)
        timer.start()

        time.sleep(0.2)
        elapsed1 = timer.elapsed_seconds

        time.sleep(0.1)
        elapsed2 = timer.elapsed_seconds

        # Second reading should be greater
        assert elapsed2 > elapsed1
        # Difference should be approximately 0.1 seconds
        assert 0.08 <= (elapsed2 - elapsed1) <= 0.15


# =============================================================================
# Test 4.T2: Timer Accuracy
# =============================================================================


class TestTimerAccuracy:
    """Test 4.T2: Timer accuracy < 100ms drift."""

    def test_accuracy_over_1_second(self) -> None:
        """Timer should maintain accuracy over 1 second."""
        timer = TimerEngine(60)
        timer.start()

        time.sleep(1.0)
        elapsed = timer.elapsed_seconds

        # Should be within 100ms of expected
        assert abs(elapsed - 1.0) < 0.1

    def test_monotonic_time_used(self) -> None:
        """Timer should use monotonic time (not wall clock)."""
        timer = TimerEngine(60)
        timer.start()

        # Multiple readings should be monotonically increasing
        readings = []
        for _ in range(5):
            readings.append(timer.elapsed_seconds)
            time.sleep(0.05)

        for i in range(1, len(readings)):
            assert readings[i] >= readings[i - 1]


# =============================================================================
# Test 4.T3: Pause Behavior
# =============================================================================


class TestTimerPause:
    """Test 4.T3: Pause freezes elapsed time."""

    def test_pause_freezes_time(self) -> None:
        """Pausing should freeze the elapsed time."""
        timer = TimerEngine(60)
        timer.start()
        time.sleep(0.1)

        timer.pause()
        paused_elapsed = timer.elapsed_seconds

        assert timer.is_paused is True
        assert timer.state == TimerState.PAUSED

        # Wait while paused
        time.sleep(0.2)

        # Elapsed should not have changed
        assert abs(timer.elapsed_seconds - paused_elapsed) < 0.01

    def test_pause_preserves_remaining(self) -> None:
        """Pausing should preserve remaining time."""
        timer = TimerEngine(60)
        timer.start()
        time.sleep(0.1)

        timer.pause()
        paused_remaining = timer.remaining_seconds

        time.sleep(0.2)

        # Remaining should not have changed
        assert abs(timer.remaining_seconds - paused_remaining) < 0.01


# =============================================================================
# Test 4.T4: Resume Behavior
# =============================================================================


class TestTimerResume:
    """Test 4.T4: Resume continues accurately after pause."""

    def test_resume_continues_from_pause(self) -> None:
        """Resuming should continue from where it was paused."""
        timer = TimerEngine(60)
        timer.start()
        time.sleep(0.1)

        timer.pause()
        paused_elapsed = timer.elapsed_seconds

        time.sleep(0.1)  # Time passes while paused

        timer.resume()
        resumed_elapsed = timer.elapsed_seconds

        assert timer.is_running is True
        # Should be approximately the same as when paused
        assert abs(resumed_elapsed - paused_elapsed) < 0.02

    def test_resume_continues_counting(self) -> None:
        """After resume, time should continue counting."""
        timer = TimerEngine(60)
        timer.start()
        time.sleep(0.1)

        timer.pause()
        time.sleep(0.1)
        timer.resume()

        resumed_elapsed = timer.elapsed_seconds
        time.sleep(0.1)
        new_elapsed = timer.elapsed_seconds

        # Should have counted more time after resume
        assert new_elapsed > resumed_elapsed
        assert 0.08 <= (new_elapsed - resumed_elapsed) <= 0.15


# =============================================================================
# Test 4.T5: Multiple Pause/Resume Cycles
# =============================================================================


class TestMultiplePauseResume:
    """Test 4.T5: Multiple pause/resume cycles maintain accuracy."""

    def test_multiple_cycles_accurate(self) -> None:
        """Multiple pause/resume cycles should maintain timing accuracy."""
        timer = TimerEngine(60)
        timer.start()

        total_running_time = 0.0

        for _ in range(3):
            time.sleep(0.1)
            total_running_time += 0.1
            timer.pause()
            time.sleep(0.05)  # Paused time shouldn't count
            timer.resume()

        time.sleep(0.1)
        total_running_time += 0.1

        elapsed = timer.elapsed_seconds

        # Should be approximately equal to total running time
        assert abs(elapsed - total_running_time) < 0.15

    def test_pause_resume_does_not_drift(self) -> None:
        """Timer should not drift across pause/resume cycles."""
        timer = TimerEngine(60)
        timer.start()

        # Run for 0.1s, pause, run for 0.1s, pause, run for 0.1s
        time.sleep(0.1)
        timer.pause()
        time.sleep(0.5)  # Long pause
        timer.resume()
        time.sleep(0.1)
        timer.pause()
        time.sleep(0.5)  # Another long pause
        timer.resume()
        time.sleep(0.1)

        elapsed = timer.elapsed_seconds

        # Total should be ~0.3s, not ~1.3s
        assert elapsed < 0.5


# =============================================================================
# Test 4.T6: Add Time
# =============================================================================


class TestAddTime:
    """Test 4.T6: Add time extends remaining correctly."""

    def test_add_time_extends_duration(self) -> None:
        """Adding time should extend the duration."""
        timer = TimerEngine(60)
        timer.start()

        initial_duration = timer.duration
        timer.add_time(30)

        assert timer.duration == initial_duration + 30
        assert timer.duration == 90.0

    def test_add_time_extends_remaining(self) -> None:
        """Adding time should extend remaining time."""
        timer = TimerEngine(60)
        timer.start()
        time.sleep(0.1)

        remaining_before = timer.remaining_seconds
        timer.add_time(30)
        remaining_after = timer.remaining_seconds

        # Remaining should have increased by ~30 seconds
        assert abs((remaining_after - remaining_before) - 30) < 0.05

    def test_add_negative_time(self) -> None:
        """Adding negative time should reduce duration."""
        timer = TimerEngine(60)
        timer.add_time(-10)

        assert timer.duration == 50.0

    def test_add_time_cannot_go_below_zero(self) -> None:
        """Cannot reduce duration to zero or below."""
        timer = TimerEngine(60)

        with pytest.raises(ValueError, match="below zero"):
            timer.add_time(-60)

        with pytest.raises(ValueError, match="below zero"):
            timer.add_time(-100)


# =============================================================================
# Test 4.T7: Overtime Detection
# =============================================================================


class TestOvertime:
    """Test 4.T7: Overtime detected when remaining < 0."""

    def test_overtime_not_initially(self) -> None:
        """Timer should not be in overtime initially."""
        timer = TimerEngine(60)
        timer.start()

        assert timer.is_overtime is False
        assert timer.overtime_seconds == 0.0

    def test_overtime_detected_after_duration(self) -> None:
        """Timer should detect overtime after duration exceeded."""
        timer = TimerEngine(1)  # 1 second timer
        timer.start()

        time.sleep(1.2)  # Wait for overtime

        assert timer.is_overtime is True
        assert timer.overtime_seconds > 0
        assert timer.remaining_seconds < 0

    def test_overtime_seconds_calculated(self) -> None:
        """Overtime seconds should be calculated correctly."""
        timer = TimerEngine(1)
        timer.start()

        time.sleep(1.3)

        # Should be approximately 0.3 seconds overtime
        assert 0.2 <= timer.overtime_seconds <= 0.5

    def test_remaining_negative_in_overtime(self) -> None:
        """Remaining should be negative during overtime."""
        timer = TimerEngine(1)
        timer.start()

        time.sleep(1.2)

        remaining = timer.remaining_seconds
        assert remaining < 0
        # Use approximate comparison due to floating point timing
        assert abs(abs(remaining) - timer.overtime_seconds) < 0.01


# =============================================================================
# Test 4.T8: Reset
# =============================================================================


class TestTimerReset:
    """Test 4.T8: Reset restores initial state."""

    def test_reset_restores_state(self) -> None:
        """Reset should restore timer to initial state."""
        timer = TimerEngine(60)
        timer.start()
        time.sleep(0.1)
        timer.pause()

        timer.reset()

        assert timer.state == TimerState.IDLE
        assert timer.is_idle is True
        assert timer.elapsed_seconds == 0.0
        assert timer.remaining_seconds == 60.0
        assert timer.duration == 60.0

    def test_reset_allows_restart(self) -> None:
        """After reset, timer can be started again."""
        timer = TimerEngine(60)
        timer.start()
        time.sleep(0.1)
        timer.stop()

        timer.reset()
        timer.start()

        assert timer.is_running is True
        time.sleep(0.1)
        assert timer.elapsed_seconds > 0

    def test_reset_with_new_duration(self) -> None:
        """Reset can set a new duration."""
        timer = TimerEngine(60)
        timer.start()
        time.sleep(0.1)

        timer.reset(new_duration=120)

        assert timer.initial_duration == 120
        assert timer.duration == 120.0
        assert timer.remaining_seconds == 120.0

    def test_reset_invalid_duration(self) -> None:
        """Reset with invalid duration should raise error."""
        timer = TimerEngine(60)

        with pytest.raises(ValueError, match="positive"):
            timer.reset(new_duration=0)

        with pytest.raises(ValueError, match="positive"):
            timer.reset(new_duration=-10)


# =============================================================================
# Test 4.T9: Cannot Start Already Running
# =============================================================================


class TestCannotStartRunning:
    """Test 4.T9: Cannot start already running timer."""

    def test_start_when_running_raises(self) -> None:
        """Starting a running timer should raise error."""
        timer = TimerEngine(60)
        timer.start()

        with pytest.raises(RuntimeError, match="already running"):
            timer.start()

    def test_start_when_paused_raises(self) -> None:
        """Starting a paused timer should raise error (use resume)."""
        timer = TimerEngine(60)
        timer.start()
        timer.pause()

        with pytest.raises(RuntimeError, match="paused"):
            timer.start()


# =============================================================================
# Test 4.T10: Cannot Resume Non-Paused
# =============================================================================


class TestCannotResumeNonPaused:
    """Test 4.T10: Cannot resume non-paused timer."""

    def test_resume_when_idle_raises(self) -> None:
        """Resuming an idle timer should raise error."""
        timer = TimerEngine(60)

        with pytest.raises(RuntimeError, match="not paused"):
            timer.resume()

    def test_resume_when_running_raises(self) -> None:
        """Resuming a running timer should raise error."""
        timer = TimerEngine(60)
        timer.start()

        with pytest.raises(RuntimeError, match="not paused"):
            timer.resume()

    def test_resume_when_stopped_raises(self) -> None:
        """Resuming a stopped timer should raise error."""
        timer = TimerEngine(60)
        timer.start()
        timer.stop()

        with pytest.raises(RuntimeError, match="not paused"):
            timer.resume()


# =============================================================================
# Additional Tests: Edge Cases and Utilities
# =============================================================================


class TestTimerEdgeCases:
    """Additional edge case tests."""

    def test_invalid_duration_raises(self) -> None:
        """Creating timer with invalid duration should raise error."""
        with pytest.raises(ValueError, match="positive"):
            TimerEngine(0)

        with pytest.raises(ValueError, match="positive"):
            TimerEngine(-10)

    def test_pause_when_not_running_raises(self) -> None:
        """Pausing when not running should raise error."""
        timer = TimerEngine(60)

        with pytest.raises(RuntimeError, match="not running"):
            timer.pause()

    def test_stop_captures_elapsed(self) -> None:
        """Stopping should capture final elapsed time."""
        timer = TimerEngine(60)
        timer.start()
        time.sleep(0.1)

        timer.stop()
        stopped_elapsed = timer.elapsed_seconds

        time.sleep(0.1)

        # Elapsed should not change after stop
        assert abs(timer.elapsed_seconds - stopped_elapsed) < 0.01
        assert timer.is_stopped is True

    def test_stop_from_paused(self) -> None:
        """Can stop from paused state."""
        timer = TimerEngine(60)
        timer.start()
        time.sleep(0.1)
        timer.pause()
        paused_elapsed = timer.elapsed_seconds

        timer.stop()

        assert timer.is_stopped is True
        assert abs(timer.elapsed_seconds - paused_elapsed) < 0.01


class TestTimerFormatting:
    """Test timer formatting methods."""

    def test_format_remaining(self) -> None:
        """Test remaining time formatting."""
        timer = TimerEngine(125)  # 2:05

        formatted = timer.format_remaining()
        assert formatted == "02:05"

    def test_format_remaining_overtime(self) -> None:
        """Test overtime formatting with negative sign."""
        timer = TimerEngine(1)
        timer.start()
        time.sleep(1.1)

        formatted = timer.format_remaining()
        assert formatted.startswith("-")

    def test_format_elapsed(self) -> None:
        """Test elapsed time formatting."""
        timer = TimerEngine(60)
        timer.start()
        time.sleep(0.1)

        formatted = timer.format_elapsed()
        assert formatted == "00:00"  # Less than 1 second

    def test_get_progress(self) -> None:
        """Test progress calculation."""
        timer = TimerEngine(10)
        timer.start()

        # Initially ~0%
        assert timer.get_progress() < 0.1

        time.sleep(0.5)

        # After 0.5s of 10s timer, should be ~5%
        progress = timer.get_progress()
        assert 0.03 <= progress <= 0.08

    def test_progress_over_100_in_overtime(self) -> None:
        """Progress should exceed 1.0 in overtime."""
        timer = TimerEngine(1)
        timer.start()
        time.sleep(1.2)

        progress = timer.get_progress()
        assert progress > 1.0
