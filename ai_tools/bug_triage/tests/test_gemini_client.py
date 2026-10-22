"""Tests for GeminiClient (SDK faked; no network)."""

from __future__ import annotations

import sys
import types
from typing import Any

import pytest

from bug_triage.llm.base import LLMError
from bug_triage.llm.gemini_client import GeminiClient

SCHEMA = {"type": "object"}


class _Models:
    def __init__(self, text: Any, error: Exception | None) -> None:
        self.text = text
        self.error = error
        self.kwargs: dict[str, Any] = {}

    def generate_content(self, **kwargs: Any) -> Any:
        self.kwargs = kwargs
        if self.error:
            raise self.error
        return types.SimpleNamespace(text=self.text)


def _install_fake(
    monkeypatch: pytest.MonkeyPatch,
    text: Any = '{"x": 1}',
    error: Exception | None = None,
    client_error: Exception | None = None,
) -> dict[str, Any]:
    state: dict[str, Any] = {}

    class Client:
        def __init__(self, api_key: str) -> None:
            if client_error:
                raise client_error
            state["api_key"] = api_key
            self.models = _Models(text, error)
            state["models"] = self.models

    google = types.ModuleType("google")
    genai = types.ModuleType("google.genai")
    genai.Client = Client  # type: ignore[attr-defined]
    google.genai = genai  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "google", google)
    monkeypatch.setitem(sys.modules, "google.genai", genai)
    return state


def test_key_from_arg_and_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    state = _install_fake(monkeypatch)
    c = GeminiClient(api_key="k1")
    assert c.name == "gemini:gemini-2.5-flash"
    assert c.complete_json("SYS", "USR", SCHEMA) == {"x": 1}
    assert c.complete_json("SYS", "USR", SCHEMA) == {"x": 1}  # client reused
    assert state["api_key"] == "k1"
    kw = state["models"].kwargs
    assert kw["model"] == "gemini-2.5-flash"
    assert kw["contents"] == "USR"
    assert kw["config"] == {
        "system_instruction": "SYS",
        "response_mime_type": "application/json",
        "response_schema": SCHEMA,
        "temperature": 0,
    }


def test_key_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "envkey")
    state = _install_fake(monkeypatch)
    GeminiClient().complete_json("s", "u", SCHEMA)
    assert state["api_key"] == "envkey"


def test_missing_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(LLMError, match="GEMINI_API_KEY not set"):
        GeminiClient().complete_json("s", "u", SCHEMA)


def test_import_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "google", None)
    monkeypatch.setitem(sys.modules, "google.genai", None)
    with pytest.raises(LLMError, match="gemini extra"):
        GeminiClient(api_key="k").complete_json("s", "u", SCHEMA)


def test_client_creation_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake(monkeypatch, client_error=RuntimeError("bad key"))
    with pytest.raises(LLMError, match="could not create"):
        GeminiClient(api_key="k").complete_json("s", "u", SCHEMA)


def test_sdk_error(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake(monkeypatch, error=RuntimeError("quota"))
    with pytest.raises(LLMError, match="quota"):
        GeminiClient(api_key="k").complete_json("s", "u", SCHEMA)


def test_bad_json(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake(monkeypatch, text="nope")
    with pytest.raises(LLMError, match="non-JSON"):
        GeminiClient(api_key="k").complete_json("s", "u", SCHEMA)


def test_json_not_object(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake(monkeypatch, text="[1]")
    with pytest.raises(LLMError, match="not an object"):
        GeminiClient(api_key="k").complete_json("s", "u", SCHEMA)


def test_no_text(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake(monkeypatch, text=None)
    with pytest.raises(LLMError, match="no text"):
        GeminiClient(api_key="k").complete_json("s", "u", SCHEMA)
