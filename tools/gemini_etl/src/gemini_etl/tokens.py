"""Token counting with a per-process cache.

The default underlying counter calls Gemini's ``count_tokens`` API. Tests and
chunkers receive the counter via dependency injection so the SDK never
appears in the transform layer.
"""
from __future__ import annotations

from typing import Any, Callable, Protocol


class TokenCounter(Protocol):
    def count(self, text: str) -> int: ...


class CachedTokenCounter:
    """In-memory cached token counter; implements the ``TokenCounter`` Protocol.

    Wraps an underlying ``Callable[[str], int]`` and memoizes its results in a
    per-instance ``dict``. Cache is keyed by string equality, not identity.
    """
    def __init__(self, underlying: Callable[[str], int]) -> None:
        self._underlying = underlying
        self._cache: dict[str, int] = {}

    def count(self, text: str) -> int:
        if text not in self._cache:
            self._cache[text] = self._underlying(text)
        return self._cache[text]


def gemini_token_counter(client: Any, model: str = "gemini-2.5-flash") -> Callable[[str], int]:
    """Build an underlying counter backed by the live Gemini API.

    Note: API surface for ``count_tokens`` is verified at runtime; if the
    google-genai version installed differs, adjust the call here. This is the
    only place SDK-shape leaks into the transform path.
    """
    def _count(text: str) -> int:
        result = client.models.count_tokens(model=model, contents=text)
        for attr in ("total_tokens", "totalTokens"):
            val = getattr(result, attr, None)
            if val is not None:
                return int(val)
        raise AttributeError(
            f"count_tokens result has neither 'total_tokens' nor 'totalTokens'; "
            f"got: {result!r}"
        )
    return _count
