"""Shared fixtures (reused by all test modules)."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
import yaml

from bug_triage.kb import KnowledgeBase
from bug_triage.models import (
    Bug,
    Candidate,
    KnownIssueHit,
    SimilarBug,
    Tier1Result,
    TriageSuggestion,
)

TINY_TEAMS = [
    {"name": "Alpha", "members": ["Ada Quill", "Ben Hart"], "components": ["auth", "api"]},
    {"name": "Beta", "members": ["Cleo Marsh", "Dev Patel"], "components": ["ui"]},
]
TINY_COMPONENTS = [
    {
        "name": "auth",
        "owner_team": "Alpha",
        "default_assignee": "Ada Quill",
        "keywords": ["login", "password", "sso", "session"],
    },
    {
        "name": "api",
        "owner_team": "Alpha",
        "default_assignee": "Ben Hart",
        "keywords": ["endpoint", "token", "rate", "webhook"],
    },
    {
        "name": "ui",
        "owner_team": "Beta",
        "default_assignee": "Cleo Marsh",
        "keywords": ["button", "page", "layout", "render"],
    },
]
TINY_KIS = [
    {
        "id": "KI-001",
        "title": "Login loop with blocked cookies",
        "component": "auth",
        "symptoms": "login redirects forever when cookies are blocked",
        "workaround": "allow cookies",
        "status": "open",
    },
    {
        "id": "KI-002",
        "title": "Layout breaks on narrow screens",
        "component": "ui",
        "symptoms": "page layout overflows on narrow screens",
        "workaround": "widen window",
        "status": "wontfix",
    },
]
TINY_USE_CASES = [
    {"name": "Sign in", "description": "Users sign in.", "components": ["auth", "ui"]},
]


def _bug(
    i: int, title: str, desc: str, comp: str, team: str, who: str, **kw: Any
) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "id": f"BUG-{i}",
        "title": title,
        "description": desc,
        "logs": "",
        "component": comp,
        "team": team,
        "assignee": who,
        "severity": "medium",
        "duplicate_of": None,
        "known_issue": None,
    }
    rec.update(kw)
    return rec


TINY_HISTORY = [
    _bug(
        1,
        "Login fails with password",
        "login rejects a valid password",
        "auth",
        "Alpha",
        "Ada Quill",
    ),
    _bug(2, "SSO session expires", "sso session ends too early", "auth", "Alpha", "Ben Hart"),
    _bug(
        3,
        "Login loop",
        "login redirects forever when cookies blocked",
        "auth",
        "Alpha",
        "Ada Quill",
        known_issue="KI-001",
    ),
    _bug(
        4, "Endpoint returns 500", "api endpoint 500 on token refresh", "api", "Alpha", "Ben Hart"
    ),
    _bug(5, "Webhook rate limited", "webhook gets rate limit errors", "api", "Alpha", "Ben Hart"),
    _bug(6, "Button misaligned", "button misaligned on page", "ui", "Beta", "Cleo Marsh"),
    _bug(
        7,
        "Page layout overflow",
        "page layout overflows on narrow screens",
        "ui",
        "Beta",
        "Dev Patel",
        known_issue="KI-002",
    ),
    _bug(
        8,
        "Endpoint returns 500 again",
        "api endpoint 500 on token refresh",
        "api",
        "Alpha",
        "Ben Hart",
        duplicate_of="BUG-4",
    ),
]
TINY_EVAL = [
    _bug(1, "Cannot login", "login says wrong password", "auth", "Alpha", "Ada Quill"),
    _bug(
        2,
        "Token endpoint 500",
        "api endpoint 500 on token refresh",
        "api",
        "Alpha",
        "Ben Hart",
        duplicate_of="BUG-4",
    ),
    _bug(3, "Button not rendering", "button does not render on page", "ui", "Beta", "Cleo Marsh"),
]
for _i, _rec in enumerate(TINY_EVAL, start=1):
    _rec["id"] = f"EVAL-{_i:03d}"


def write_tiny_kb(path: Path) -> Path:
    """Write the minimal valid data set into path."""
    path.mkdir(parents=True, exist_ok=True)
    for name, key, items in (
        ("teams.yaml", "teams", TINY_TEAMS),
        ("components.yaml", "components", TINY_COMPONENTS),
        ("known_issues.yaml", "known_issues", TINY_KIS),
        ("use_cases.yaml", "use_cases", TINY_USE_CASES),
    ):
        (path / name).write_text(yaml.safe_dump({key: items}), encoding="utf-8")
    for name, rows in (("history.jsonl", TINY_HISTORY), ("eval.jsonl", TINY_EVAL)):
        (path / name).write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return path


@pytest.fixture(scope="session")
def kb() -> KnowledgeBase:
    """KnowledgeBase loaded from the real data/ directory."""
    return KnowledgeBase.load()


@pytest.fixture
def tiny_kb_dir(tmp_path: Path) -> Path:
    """Directory holding a minimal valid data set."""
    return write_tiny_kb(tmp_path / "tiny")


@pytest.fixture
def tiny_kb(tiny_kb_dir: Path) -> KnowledgeBase:
    """KnowledgeBase loaded from the tiny data set."""
    return KnowledgeBase.load(tiny_kb_dir)


@pytest.fixture
def sample_bug() -> Bug:
    """A generic incoming bug."""
    return Bug(
        id="NEW-1",
        title="Login page hangs after SSO redirect",
        description="After the SSO redirect the login page spins and times out.",
        logs="ERROR auth.sso callback timeout",
    )


@pytest.fixture
def make_tier1_result() -> Callable[..., Tier1Result]:
    """Factory for Tier1Result with overridable fields."""

    def factory(**overrides: Any) -> Tier1Result:
        data: dict[str, Any] = {
            "component_candidates": [
                Candidate(label="auth-sso", score=0.7),
                Candidate(label="web-ui", score=0.2),
                Candidate(label="mobile-app", score=0.1),
            ],
            "team": "Identity",
            "assignee": "Tobias Wren",
            "similar_bugs": [
                SimilarBug(
                    bug_id="BUG-1001",
                    title="Login loop",
                    score=0.5,
                    component="auth-sso",
                    assignee="Tobias Wren",
                )
            ],
            "known_issue_hits": [KnownIssueHit(id="KI-001", title="SSO login loops", score=0.3)],
            "duplicate_of": None,
            "known_issue": None,
            "elapsed_ms": 1.5,
        }
        data.update(overrides)
        return Tier1Result(**data)

    return factory


@pytest.fixture
def make_suggestion() -> Callable[..., TriageSuggestion]:
    """Factory for TriageSuggestion with overridable fields."""

    def factory(**overrides: Any) -> TriageSuggestion:
        data: dict[str, Any] = {
            "component": "auth-sso",
            "team": "Identity",
            "duplicate_of": None,
            "known_issue": None,
            "severity": "medium",
            "confidence": 0.8,
            "rationale": "matches SSO login symptoms",
        }
        data.update(overrides)
        return TriageSuggestion(**data)

    return factory


class FakeLLMClient:
    """Scripted LLMClient: returns dicts in order, raises Exception instances."""

    def __init__(self, responses: list[dict[str, Any] | Exception] | None = None) -> None:
        self.name = "fake"
        self.responses: list[dict[str, Any] | Exception] = list(responses or [])
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def complete_json(self, system: str, user: str, schema: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((system, user, schema))
        if not self.responses:
            raise RuntimeError("FakeLLMClient: no scripted responses left")
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


@pytest.fixture
def fake_llm() -> FakeLLMClient:
    """An empty FakeLLMClient; set .responses in the test."""
    return FakeLLMClient()
