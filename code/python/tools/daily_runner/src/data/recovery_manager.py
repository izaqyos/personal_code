"""
Recovery manager for session crash resilience.

This module handles saving and restoring meeting session state
to allow recovery after unexpected application termination.
"""

import contextlib
import json
import logging
import threading
from collections.abc import Callable
from pathlib import Path

from filelock import FileLock

from src.core.models import SessionRecovery

logger = logging.getLogger(__name__)


class RecoveryManager:
    """
    Manages session recovery for crash resilience.

    Provides automatic periodic saving of session state and
    methods to detect, restore, and clear recovery data.
    """

    DEFAULT_RECOVERY_PATH = Path("data/.session_recovery.json")
    DEFAULT_INTERVAL = 5  # seconds

    def __init__(
        self,
        recovery_path: Path | None = None,
        auto_save_interval: int | None = None,
    ) -> None:
        """
        Initialize the recovery manager.

        Args:
            recovery_path: Path for recovery file.
            auto_save_interval: Seconds between auto-saves.
        """
        self._recovery_path = recovery_path or self.DEFAULT_RECOVERY_PATH
        self._lock_path = self._recovery_path.with_suffix(".lock")
        self._interval = auto_save_interval or self.DEFAULT_INTERVAL

        self._session: SessionRecovery | None = None
        self._auto_save_thread: threading.Thread | None = None
        self._stop_auto_save = threading.Event()
        self._state_callback: Callable[[], SessionRecovery | None] | None = None

    @property
    def recovery_path(self) -> Path:
        """Return the recovery file path."""
        return self._recovery_path

    @property
    def auto_save_interval(self) -> int:
        """Return the auto-save interval in seconds."""
        return self._interval

    def has_recovery(self) -> bool:
        """
        Check if a recovery file exists.

        Returns:
            True if a valid recovery file exists.
        """
        if not self._recovery_path.exists():
            return False

        # Verify it's valid JSON
        try:
            data = json.loads(self._recovery_path.read_text())
            SessionRecovery.model_validate(data)
            return True
        except Exception:
            return False

    def load_recovery(self) -> SessionRecovery | None:
        """
        Load recovery data from file.

        Returns:
            The SessionRecovery or None if not found/invalid.
        """
        if not self._recovery_path.exists():
            logger.debug("No recovery file found")
            return None

        try:
            with FileLock(self._lock_path):
                data = json.loads(self._recovery_path.read_text())
                session = SessionRecovery.model_validate(data)
                self._session = session
                logger.info(f"Loaded recovery session: {session.session_id}")
                return session
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid recovery file JSON: {e}")
            self._cleanup_invalid_recovery()
            return None
        except Exception as e:
            logger.warning(f"Error loading recovery: {e}")
            self._cleanup_invalid_recovery()
            return None

    def _cleanup_invalid_recovery(self) -> None:
        """Remove invalid recovery file."""
        if self._recovery_path.exists():
            try:
                backup = self._recovery_path.with_suffix(".invalid.json")
                self._recovery_path.rename(backup)
                logger.info(f"Moved invalid recovery to {backup}")
            except OSError:
                with contextlib.suppress(OSError):
                    self._recovery_path.unlink()

    def save_recovery(self, session: SessionRecovery) -> None:
        """
        Save recovery state to file.

        Args:
            session: The session state to save.
        """
        # Ensure directory exists
        self._recovery_path.parent.mkdir(parents=True, exist_ok=True)

        session.update_timestamp()
        self._session = session

        temp_path = self._recovery_path.with_suffix(".tmp")
        try:
            with FileLock(self._lock_path):
                data = session.to_json_dict()
                temp_path.write_text(json.dumps(data, indent=2))
                temp_path.replace(self._recovery_path)
                logger.debug(f"Saved recovery state: {session.session_id}")
        except Exception as e:
            logger.error(f"Failed to save recovery: {e}")
            if temp_path.exists():
                temp_path.unlink()
            raise

    def clear_recovery(self) -> None:
        """Delete the recovery file."""
        self.stop_auto_save()

        if self._recovery_path.exists():
            try:
                with FileLock(self._lock_path):
                    self._recovery_path.unlink()
                    logger.info("Cleared recovery file")
            except OSError as e:
                logger.error(f"Failed to clear recovery file: {e}")

        self._session = None

    def start_auto_save(
        self,
        state_callback: Callable[[], SessionRecovery | None],
    ) -> None:
        """
        Start automatic periodic saving.

        Args:
            state_callback: Function that returns current session state.
        """
        if self._auto_save_thread is not None and self._auto_save_thread.is_alive():
            logger.warning("Auto-save already running")
            return

        self._state_callback = state_callback
        self._stop_auto_save.clear()

        self._auto_save_thread = threading.Thread(
            target=self._auto_save_loop,
            daemon=True,
            name="RecoveryAutoSave",
        )
        self._auto_save_thread.start()
        logger.info(f"Started auto-save with {self._interval}s interval")

    def _auto_save_loop(self) -> None:
        """Background thread loop for periodic saves."""
        while not self._stop_auto_save.wait(timeout=self._interval):
            if self._state_callback is None:
                continue

            try:
                session = self._state_callback()
                if session is not None:
                    self.save_recovery(session)
            except Exception as e:
                logger.error(f"Auto-save error: {e}")

    def stop_auto_save(self) -> None:
        """Stop the automatic saving thread."""
        if self._auto_save_thread is None:
            return

        self._stop_auto_save.set()

        if self._auto_save_thread.is_alive():
            self._auto_save_thread.join(timeout=2.0)

        self._auto_save_thread = None
        self._state_callback = None
        logger.info("Stopped auto-save")

    def is_auto_save_running(self) -> bool:
        """
        Check if auto-save is currently running.

        Returns:
            True if auto-save thread is active.
        """
        return (
            self._auto_save_thread is not None
            and self._auto_save_thread.is_alive()
        )

    def get_recovery_info(self) -> dict[str, str] | None:
        """
        Get summary info about existing recovery.

        Returns:
            Dictionary with session info or None if no recovery exists.
        """
        session = self.load_recovery()
        if session is None:
            return None

        completed_names = [s.member_id for s in session.completed_speakers]

        return {
            "session_id": session.session_id,
            "team_id": session.team_id,
            "started_at": session.started_at,
            "last_updated": session.last_updated,
            "current_speaker_index": str(session.current_speaker_index),
            "completed_speakers": ", ".join(completed_names) if completed_names else "None",
            "state": session.state.value,
        }
