"""LLM client protocol shared by the judge and its backends."""

from __future__ import annotations

from typing import Any, Protocol


class LLMError(Exception):
    """Raised when an LLM backend fails or returns unusable output."""


class LLMClient(Protocol):
    """Anything that can answer a prompt with a JSON object."""

    name: str

    def complete_json(self, system: str, user: str, schema: dict[str, Any]) -> dict[str, Any]:
        """Return the model's answer as a JSON object matching ``schema``."""
        ...
