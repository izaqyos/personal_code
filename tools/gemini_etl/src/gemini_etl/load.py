"""Gemini File Search Store loader: bootstrap + upload + delete with retry."""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

log = logging.getLogger(__name__)

_RATE_LIMIT_RE = re.compile(r"\b(429|503|rate|quota|unavailable)\b", re.IGNORECASE)


def _is_retryable(exc: BaseException) -> bool:
    return bool(_RATE_LIMIT_RE.search(str(exc)))


@dataclass(frozen=True)
class UploadResult:
    document_id: str


class Loader:
    def __init__(
        self,
        *,
        client: Any,
        store_display_name: str,
        max_attempts: int = 5,
        retry_min_seconds: float = 1.0,
    ) -> None:
        self._client = client
        self._store_display_name = store_display_name
        self._store_name: str | None = None
        # Typed Any: tenacity's retry() returns Callable[[WrappedFn], WrappedFn]
        # which is a TypeVar-bound type not readily expressible under mypy --strict
        # without importing tenacity's internal WrappedFn TypeVar.
        self._retry: Any = retry(
            retry=retry_if_exception(_is_retryable),
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=retry_min_seconds, min=retry_min_seconds, max=8),
            reraise=True,
        )

    def ensure_store(self) -> str:
        """Return the store resource name, creating it if it does not exist."""
        if self._store_name is not None:
            return self._store_name
        for store in self._client.file_search_stores.list():
            if store.display_name == self._store_display_name:
                name: str = store.name
                self._store_name = name
                return name
        new_store = self._client.file_search_stores.create(
            display_name=self._store_display_name
        )
        new_name: str = new_store.name
        self._store_name = new_name
        return new_name

    def upload(self, *, path: Path, display_name: str) -> UploadResult:
        """Upload the file at ``path`` and create a store document.

        ``display_name`` should be ``{source}/{rel_path}`` so duplicates can
        be reconciled by ``find_document_by_display_name``."""
        assert self._store_name is not None, "call ensure_store() first"

        @self._retry
        def _do() -> str:
            uploaded = self._client.files.upload(file=str(path))
            doc = self._client.file_search_stores.documents.create(
                parent=self._store_name,
                config={"display_name": display_name, "file": uploaded.name},
            )
            return doc.name  # type: ignore[no-any-return]

        return UploadResult(document_id=_do())

    def delete_document(self, document_id: str) -> None:
        """Delete a document from the store by its resource name."""

        @self._retry
        def _do() -> None:
            self._client.file_search_stores.documents.delete(name=document_id)

        _do()

    def find_document_by_display_name(self, display_name: str) -> str | None:
        """Return the resource name of the first document matching ``display_name``.

        Used to reconcile orphans after a crashed run."""
        assert self._store_name is not None, "call ensure_store() first"
        for doc in self._client.file_search_stores.documents.list(
            parent=self._store_name
        ):
            if doc.display_name == display_name:
                return doc.name  # type: ignore[no-any-return]
        return None
