"""Ollama (local) LLM client using the /api/chat endpoint with structured output."""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

from bug_triage.llm.base import LLMError

logger = logging.getLogger(__name__)


class OllamaClient:
    """Calls a local Ollama server; all failures surface as LLMError."""

    def __init__(
        self,
        model: str = "gemma4:12b",
        base_url: str = "http://localhost:11434",
        timeout: float = 120.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.transport = transport
        self.name = f"ollama:{model}"

    def complete_json(self, system: str, user: str, schema: dict[str, Any]) -> dict[str, Any]:
        """POST a chat request constrained by ``schema`` and parse the JSON reply."""
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "format": schema,
            "stream": False,
            # Thinking models (gemma4) combined with a format schema stall for minutes.
            "think": False,
            "options": {"temperature": 0},
        }
        url = f"{self.base_url}/api/chat"
        try:
            with httpx.Client(transport=self.transport, timeout=self.timeout) as http:
                resp = http.post(url, json=body)
                resp.raise_for_status()
                payload = resp.json()
        except httpx.ConnectError as exc:
            raise LLMError(
                f"Ollama not reachable at {self.base_url}; is `ollama serve` running?"
            ) from exc
        except httpx.TimeoutException as exc:
            raise LLMError(f"Ollama timed out after {self.timeout}s ({self.model})") from exc
        except httpx.HTTPStatusError as exc:
            raise LLMError(
                f"Ollama returned HTTP {exc.response.status_code}: {exc.response.text[:200]}"
            ) from exc
        except (httpx.HTTPError, ValueError) as exc:
            raise LLMError(f"Ollama request failed: {exc}") from exc
        return _parse_content(payload)


def _parse_content(payload: object) -> dict[str, Any]:
    try:
        content = payload["message"]["content"]  # type: ignore[index]
    except (KeyError, TypeError) as exc:
        raise LLMError("Ollama response has no message.content") from exc
    if not isinstance(content, str):
        raise LLMError("Ollama message.content is not a string")
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise LLMError(f"Ollama returned non-JSON content: {content[:200]!r}") from exc
    if not isinstance(data, dict):
        raise LLMError("Ollama returned JSON that is not an object")
    return data
