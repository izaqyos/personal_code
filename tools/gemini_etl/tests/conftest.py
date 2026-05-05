"""Shared pytest fixtures for gemini_etl tests."""
from collections.abc import Callable
from pathlib import Path

import pytest



@pytest.fixture
def fake_count_tokens() -> Callable[[str], int]:
    """Deterministic stand-in for Gemini's count_tokens API."""
    def _count(text: str) -> int:
        # Roughly char/4 — matches Gemini's order-of-magnitude.
        return max(1, len(text) // 4)
    return _count


@pytest.fixture
def sample_kb_tree(tmp_path: Path) -> Path:
    """Build a deterministic sample_kb tree under tmp_path.

    Includes both files that SHOULD be yielded by walk_source and files that
    MUST be skipped (gitignored, .git/, empty, wrong extension). Built
    programmatically so the 'should-be-skipped' files are guaranteed to exist
    at test time, even in CI from a clean checkout."""
    root = tmp_path / "sample_kb"
    (root / "notes" / "algorithms").mkdir(parents=True)
    (root / "build").mkdir()
    (root / ".git").mkdir()

    (root / ".gitignore").write_text("build/\n*.tmp\ncustom_output/\n", encoding="utf-8")

    # SHOULD be yielded
    (root / "notes" / "intro.md").write_text("# Hello\nbody\n", encoding="utf-8")
    (root / "notes" / "algorithms" / "dp.md").write_text("# DP\n", encoding="utf-8")

    # MUST be skipped
    (root / "build" / "skipme.md").write_text("noise\n", encoding="utf-8")
    (root / "notes" / "empty.md").write_text("", encoding="utf-8")
    (root / "notes" / "draft.tmp").write_text("tmp\n", encoding="utf-8")
    (root / ".git" / "HEAD").write_text("in dot-git\n", encoding="utf-8")

    (root / "custom_output").mkdir()
    (root / "custom_output" / "ignored.md").write_text("noise\n", encoding="utf-8")

    return root


@pytest.fixture
def sample_code_tree(tmp_path: Path) -> Path:
    """Build a deterministic sample_code tree under tmp_path."""
    root = tmp_path / "sample_code"
    (root / "src").mkdir(parents=True)
    (root / "node_modules").mkdir()

    (root / "src" / "foo.py").write_text("def foo():\n    return 1\n", encoding="utf-8")
    (root / "node_modules" / "x.py").write_text("noise\n", encoding="utf-8")

    return root
