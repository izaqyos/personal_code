"""Mock runner: replays a canned model response from disk (tests, offline demo)."""

from __future__ import annotations

from pathlib import Path

from . import extract_findings


class MockRunner:
    def __init__(self, response_path: str):
        self.path = Path(response_path)
        self.last_bundle: str | None = None

    def review(self, bundle: str, repo: Path) -> list:
        self.last_bundle = bundle
        return extract_findings(self.path.read_text())
