"""Tests for OllamaClient (no network; httpx.MockTransport)."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

from bug_triage.llm.base import LLMError
from bug_triage.llm.ollama_client import OllamaClient

SCHEMA = {"type": "object", "properties": {"a": {"type": "integer"}}}


def _client(handler: Any, **kw: Any) -> OllamaClient:
    return OllamaClient(transport=httpx.MockTransport(handler), **kw)


def _ok(content: Any) -> Any:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"message": {"role": "assistant", "content": content}})

    return handler


def test_success_and_name() -> None:
    c = _client(_ok('{"a": 1}'))
    assert c.name == "ollama:gemma4:12b"
    assert c.complete_json("s", "u", SCHEMA) == {"a": 1}


def test_request_shape() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"message": {"content": "{}"}})

    _client(handler, model="m", base_url="http://h:1/").complete_json("SYS", "USR", SCHEMA)
    req = seen[0]
    assert str(req.url) == "http://h:1/api/chat"
    body = json.loads(req.content)
    assert body["model"] == "m"
    assert body["format"] == SCHEMA
    assert body["stream"] is False
    assert body["options"] == {"temperature": 0}
    assert body["think"] is False
    assert body["messages"] == [
        {"role": "system", "content": "SYS"},
        {"role": "user", "content": "USR"},
    ]


def test_non_2xx() -> None:
    c = _client(lambda r: httpx.Response(500, text="boom"))
    with pytest.raises(LLMError, match="HTTP 500"):
        c.complete_json("s", "u", SCHEMA)


def test_connect_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused")

    with pytest.raises(LLMError, match="ollama serve"):
        _client(handler).complete_json("s", "u", SCHEMA)


def test_timeout() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("slow")

    with pytest.raises(LLMError, match="timed out"):
        _client(handler).complete_json("s", "u", SCHEMA)


def test_other_http_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadError("reset")

    with pytest.raises(LLMError, match="request failed"):
        _client(handler).complete_json("s", "u", SCHEMA)


def test_response_not_json() -> None:
    c = _client(lambda r: httpx.Response(200, text="<html>"))
    with pytest.raises(LLMError, match="request failed"):
        c.complete_json("s", "u", SCHEMA)


def test_non_json_content() -> None:
    with pytest.raises(LLMError, match="non-JSON"):
        _client(_ok("not json")).complete_json("s", "u", SCHEMA)


def test_array_content() -> None:
    with pytest.raises(LLMError, match="not an object"):
        _client(_ok("[1, 2]")).complete_json("s", "u", SCHEMA)


def test_missing_message() -> None:
    c = _client(lambda r: httpx.Response(200, json={"done": True}))
    with pytest.raises(LLMError, match="no message"):
        c.complete_json("s", "u", SCHEMA)


def test_payload_not_dict() -> None:
    c = _client(lambda r: httpx.Response(200, json=[1]))
    with pytest.raises(LLMError, match="no message"):
        c.complete_json("s", "u", SCHEMA)


def test_content_not_string() -> None:
    with pytest.raises(LLMError, match="not a string"):
        _client(_ok(5)).complete_json("s", "u", SCHEMA)
