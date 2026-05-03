"""Shared pytest fixtures for gemini_etl tests."""
from collections.abc import Callable
from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def fake_count_tokens() -> Callable[[str], int]:
    """Deterministic stand-in for Gemini's count_tokens API."""
    def _count(text: str) -> int:
        # Roughly char/4 — matches Gemini's order-of-magnitude.
        return max(1, len(text) // 4)
    return _count
