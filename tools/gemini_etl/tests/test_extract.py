import pytest

from gemini_etl.config import Source
from gemini_etl.extract import FileRef, walk_source


@pytest.fixture
def kb_source(fixtures_dir) -> Source:
    return Source(
        name="sample_kb",
        path=str(fixtures_dir / "sample_kb"),
        extensions=frozenset({".md"}),
    )


@pytest.fixture
def code_source(fixtures_dir) -> Source:
    return Source(
        name="sample_code",
        path=str(fixtures_dir / "sample_code"),
        extensions=frozenset({".py"}),
    )


def _rel_paths(refs: list[FileRef]) -> set[str]:
    return {r.rel_path for r in refs}


def test_walks_only_allowed_extensions(kb_source):
    refs = list(walk_source(kb_source))
    assert all(r.rel_path.endswith(".md") for r in refs)


def test_respects_gitignore_build_dir(kb_source):
    paths = _rel_paths(list(walk_source(kb_source)))
    assert not any("build/" in p for p in paths)


def test_skips_dot_git(kb_source):
    paths = _rel_paths(list(walk_source(kb_source)))
    assert not any(p.startswith(".git/") for p in paths)


def test_skips_empty_files(kb_source):
    paths = _rel_paths(list(walk_source(kb_source)))
    assert "notes/empty.md" not in paths


def test_skips_node_modules(code_source):
    paths = _rel_paths(list(walk_source(code_source)))
    assert not any("node_modules" in p for p in paths)


def test_yields_expected_kb_files(kb_source):
    paths = _rel_paths(list(walk_source(kb_source)))
    assert paths == {"notes/intro.md", "notes/algorithms/dp.md"}


def test_file_ref_has_sha256(kb_source):
    refs = list(walk_source(kb_source))
    intro = next(r for r in refs if r.rel_path == "notes/intro.md")
    assert len(intro.sha256) == 64  # sha256 hex


def test_size_guard(tmp_path):
    big = tmp_path / "big.md"
    big.write_bytes(b"x" * 1024)
    src = Source(name="t", path=str(tmp_path), extensions=frozenset({".md"}))
    refs = list(walk_source(src, max_file_size_bytes=512))
    assert refs == []


def test_source_name_preserved(kb_source):
    refs = list(walk_source(kb_source))
    assert all(r.source == "sample_kb" for r in refs)
