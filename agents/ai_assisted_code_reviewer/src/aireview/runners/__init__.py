"""LLM runners: take the bundle, return raw finding dicts (untrusted)."""

from __future__ import annotations

import json
import re

FENCE_RE = re.compile(r"```(?:json)?\s*\n(.*?)\n```", re.DOTALL)


class RunnerError(RuntimeError):
    pass


def extract_findings(text: str) -> list:
    """Pull the findings array out of free-form model output.

    Accepts a ```json fence (last parseable one wins), a bare object, or a bare array.
    Objects must carry a "findings" list.
    """
    candidates = [m.group(1) for m in FENCE_RE.finditer(text)][::-1]
    stripped = text.strip()
    candidates.append(stripped)
    for opener, closer in (("{", "}"), ("[", "]")):
        a, b = stripped.find(opener), stripped.rfind(closer)
        if a != -1 and b > a:
            candidates.append(stripped[a : b + 1])
    for c in candidates:
        try:
            data = json.loads(c)
        except (json.JSONDecodeError, ValueError):
            continue
        if isinstance(data, dict) and isinstance(data.get("findings"), list):
            return data["findings"]
        if isinstance(data, list):
            return data
    raise RunnerError("no findings JSON found in model output")


def get_runner(name: str, cfg: dict, mock_response: str | None = None):
    if name == "claude":
        from .claude import ClaudeRunner

        return ClaudeRunner(cfg["claude"])
    if name == "mock":
        from .mock import MockRunner

        if not mock_response:
            raise RunnerError("--mock-response is required for the mock runner")
        return MockRunner(mock_response)
    raise RunnerError(f"unknown runner {name!r}")
