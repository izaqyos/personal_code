"""SQLite manifest tracking per-file SHA + Gemini doc IDs.

Thread-safe: a single ``Manifest`` instance can be shared across worker
threads — writes are serialized by an internal lock and the connection is
opened with ``check_same_thread=False``."""
from __future__ import annotations

import enum
import sqlite3
import threading
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterator


class FileState(enum.Enum):
    NEW = "new"
    CHANGED = "changed"
    UNCHANGED = "unchanged"


@dataclass(frozen=True)
class ManifestRow:
    source: str
    rel_path: str
    sha256: str
    display_name: str
    document_id: str | None
    uploaded_at: str | None = None


_SCHEMA = """
CREATE TABLE IF NOT EXISTS files (
  source       TEXT NOT NULL,
  rel_path     TEXT NOT NULL,
  sha256       TEXT NOT NULL,
  display_name TEXT NOT NULL,
  document_id  TEXT,
  uploaded_at  TEXT NOT NULL,
  PRIMARY KEY (source, rel_path)
);
"""


class Manifest:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._lock = threading.Lock()
        with self._lock:
            self._conn.executescript(_SCHEMA)
            self._conn.commit()

    def classify(self, source: str, rel_path: str, sha256: str) -> FileState:
        """Return whether a file is NEW, CHANGED, or UNCHANGED relative to the manifest.

        Note: ``classify`` followed by ``upsert`` is not atomic. If two threads
        race on the same ``(source, rel_path)``, the result may be stale.
        Callers must ensure no concurrent writer for the same key between the
        two calls."""
        row = self.get(source, rel_path)
        if row is None:
            return FileState.NEW
        return FileState.UNCHANGED if row.sha256 == sha256 else FileState.CHANGED

    def get(self, source: str, rel_path: str) -> ManifestRow | None:
        with self._lock:
            cur = self._conn.execute(
                "SELECT source, rel_path, sha256, display_name, document_id, uploaded_at "
                "FROM files WHERE source = ? AND rel_path = ?",
                (source, rel_path),
            )
            r = cur.fetchone()
        return ManifestRow(*r) if r else None

    def upsert(self, row: ManifestRow) -> None:
        """Insert or update a manifest row.

        If ``row.uploaded_at`` is None, the current UTC timestamp is
        substituted before writing. The DB enforces NOT NULL on the column,
        so rows returned by ``get()`` always have a non-None ``uploaded_at``."""
        uploaded_at = row.uploaded_at or datetime.now(UTC).isoformat()
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO files (source, rel_path, sha256, display_name, document_id, uploaded_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(source, rel_path) DO UPDATE SET
                    sha256 = excluded.sha256,
                    display_name = excluded.display_name,
                    document_id = excluded.document_id,
                    uploaded_at = excluded.uploaded_at
                """,
                (row.source, row.rel_path, row.sha256, row.display_name,
                 row.document_id, uploaded_at),
            )
            self._conn.commit()

    def delete(self, source: str, rel_path: str) -> None:
        with self._lock:
            self._conn.execute(
                "DELETE FROM files WHERE source = ? AND rel_path = ?",
                (source, rel_path),
            )
            self._conn.commit()

    def deleted_rows(self, live_set: set[tuple[str, str]]) -> Iterator[ManifestRow]:
        """Yield manifest rows whose ``(source, rel_path)`` is not in ``live_set``.

        The snapshot is taken atomically under the lock; the generator yields
        outside the lock so consumers may take their time without blocking
        writers."""
        with self._lock:
            rows = list(self._conn.execute(
                "SELECT source, rel_path, sha256, display_name, document_id, uploaded_at FROM files"
            ))
        for r in rows:
            if (r[0], r[1]) not in live_set:
                yield ManifestRow(*r)

    def summary(self) -> dict[str, int]:
        with self._lock:
            return {
                source: count
                for source, count in self._conn.execute(
                    "SELECT source, COUNT(*) FROM files GROUP BY source"
                )
            }

    def close(self) -> None:
        """Close the underlying SQLite connection.

        After ``close()`` is called, no other methods may be called on this
        instance — they will raise ``sqlite3.ProgrammingError``."""
        with self._lock:
            self._conn.close()
