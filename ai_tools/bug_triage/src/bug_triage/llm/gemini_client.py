"""Gemini LLM client (optional extra; the SDK is imported lazily)."""

from __future__ import annotations

import json
import logging
import os
from typing import Any

from bug_triage.llm.base import LLMError

logger = logging.getLogger(__name__)


class GeminiClient:
    """Calls Gemini via google-genai; all failures surface as LLMError."""

    def __init__(self, model: str = "gemini-2.5-flash", api_key: str | None = None) -> None:
        self.model = model
        self.name = f"gemini:{model}"
        self._api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self._client: Any = None

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        if not self._api_key:
            raise LLMError("GEMINI_API_KEY not set (see .env.example)")
        try:
            from google import genai
        except ImportError as exc:
            raise LLMError("install the gemini extra: uv pip install -e '.[gemini]'") from exc
        try:
            self._client = genai.Client(api_key=self._api_key)
        except Exception as exc:
            raise LLMError(f"could not create Gemini client: {exc}") from exc
        return self._client

    def complete_json(self, system: str, user: str, schema: dict[str, Any]) -> dict[str, Any]:
        """Generate a JSON answer constrained by ``schema``."""
        client = self._get_client()
        try:
            response = client.models.generate_content(
                model=self.model,
                contents=user,
                config={
                    "system_instruction": system,
                    "response_mime_type": "application/json",
                    "response_schema": schema,
                    "temperature": 0,
                },
            )
            text = response.text
        except Exception as exc:
            raise LLMError(f"Gemini request failed: {exc}") from exc
        if not isinstance(text, str):
            raise LLMError("Gemini returned no text")
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise LLMError(f"Gemini returned non-JSON text: {text[:200]!r}") from exc
        if not isinstance(data, dict):
            raise LLMError("Gemini returned JSON that is not an object")
        return data
