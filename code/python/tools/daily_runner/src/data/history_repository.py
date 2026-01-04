"""
History repository for storing and querying meeting records.

This module manages meeting history with FIFO limiting and
atomic file writes for data safety.
"""

import json
import logging
from pathlib import Path

from filelock import FileLock

from src.core.models import HistoryFile, MeetingRecord

logger = logging.getLogger(__name__)


class HistoryRepository:
    """
    Repository for meeting history data.

    Handles persistence of meeting records with configurable
    maximum entries and atomic file operations.
    """

    DEFAULT_MAX_ENTRIES = 2000

    def __init__(
        self,
        team_id: str,
        data_dir: Path | None = None,
        max_entries: int | None = None,
    ) -> None:
        """
        Initialize the history repository.

        Args:
            team_id: Team identifier for the history file.
            data_dir: Directory for history files.
            max_entries: Maximum number of entries to keep.
        """
        self._team_id = team_id
        self._data_dir = data_dir or Path("data")
        self._max_entries = max_entries or self.DEFAULT_MAX_ENTRIES
        self._history: HistoryFile | None = None

        # Construct file path
        self._file_path = self._data_dir / f"history_{team_id}.json"
        self._lock_path = self._file_path.with_suffix(".lock")

    @property
    def file_path(self) -> Path:
        """Return the history file path."""
        return self._file_path

    @property
    def team_id(self) -> str:
        """Return the team ID."""
        return self._team_id

    @property
    def max_entries(self) -> int:
        """Return the maximum entries limit."""
        return self._max_entries

    def load(self) -> HistoryFile:
        """
        Load history from file or create empty.

        Returns:
            The loaded or empty HistoryFile.
        """
        if not self._file_path.exists():
            logger.info(f"History file not found, creating empty: {self._file_path}")
            self._history = HistoryFile()
            return self._history

        try:
            with FileLock(self._lock_path):
                data = json.loads(self._file_path.read_text())
                self._history = HistoryFile.model_validate(data)
                logger.debug(f"Loaded {len(self._history.entries)} history entries")
                return self._history
        except json.JSONDecodeError as e:
            logger.warning(f"Corrupted history file: {e}")
            return self._handle_corrupted_file()
        except Exception as e:
            logger.warning(f"Error loading history: {e}")
            return self._handle_corrupted_file()

    def _handle_corrupted_file(self) -> HistoryFile:
        """
        Handle corrupted history file by backing up and creating new.

        Returns:
            A new empty HistoryFile.
        """
        if self._file_path.exists():
            backup_path = self._file_path.with_suffix(".corrupted.json")
            try:
                self._file_path.rename(backup_path)
                logger.info(f"Backed up corrupted history to {backup_path}")
            except OSError as e:
                logger.error(f"Failed to backup corrupted history: {e}")

        self._history = HistoryFile()
        self._save()
        return self._history

    def _save(self) -> None:
        """
        Save history to file atomically.

        Uses temporary file and atomic rename for safety.
        """
        if self._history is None:
            return

        # Ensure directory exists
        self._data_dir.mkdir(parents=True, exist_ok=True)

        temp_path = self._file_path.with_suffix(".tmp")
        try:
            with FileLock(self._lock_path):
                data = self._history.model_dump(mode="json")
                temp_path.write_text(json.dumps(data, indent=2))
                temp_path.replace(self._file_path)
                logger.debug(f"Saved history with {len(self._history.entries)} entries")
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
            if temp_path.exists():
                temp_path.unlink()
            raise

    def save_entry(self, record: MeetingRecord) -> None:
        """
        Save a new meeting record.

        Automatically enforces the max entries limit.

        Args:
            record: The meeting record to save.
        """
        if self._history is None:
            self.load()

        assert self._history is not None
        self._history.add_entry(record, self._max_entries)
        self._save()
        logger.info(f"Saved meeting record: {record.id}")

    def get_entries(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
    ) -> list[MeetingRecord]:
        """
        Get meeting entries with optional filters.

        Args:
            start_date: Filter entries on or after this date (YYYY-MM-DD).
            end_date: Filter entries on or before this date (YYYY-MM-DD).
            limit: Maximum number of entries to return.

        Returns:
            List of matching meeting records.
        """
        if self._history is None:
            self.load()

        assert self._history is not None
        entries = self._history.get_entries_by_date_range(start_date, end_date)

        if limit:
            entries = entries[-limit:]

        return entries

    def get_latest(self, count: int = 1) -> list[MeetingRecord]:
        """
        Get the most recent meeting records.

        Args:
            count: Number of records to return.

        Returns:
            List of the most recent records.
        """
        if self._history is None:
            self.load()

        assert self._history is not None
        return self._history.entries[-count:] if self._history.entries else []

    def get_entry_count(self) -> int:
        """
        Get the total number of entries.

        Returns:
            Number of history entries.
        """
        if self._history is None:
            self.load()

        assert self._history is not None
        return len(self._history.entries)

    def clear(self) -> None:
        """Clear all history entries."""
        self._history = HistoryFile()
        self._save()
        logger.info("Cleared all history entries")

    def delete_file(self) -> None:
        """Delete the history file."""
        if self._file_path.exists():
            self._file_path.unlink()
            logger.info(f"Deleted history file: {self._file_path}")
        self._history = None
