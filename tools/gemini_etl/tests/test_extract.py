import pytest

from gemini_etl.config import Source
from gemini_etl.extract import FileRef, walk_source


@pytest.fixture
def kb_source(sample_kb_tree) -> Source:
    return Source(
        name="sample_kb",
        path=str(sample_kb_tree),
        extensions=frozenset({".md"}),
    )


@pytest.fixture
def code_source(sample_code_tree) -> Source:
    return Source(
        name="sample_code",
        path=str(sample_code_tree),
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


def test_skipped_files_exist_but_are_not_yielded(kb_source, sample_kb_tree):
    """Sanity check: the 'should-be-skipped' files DO exist on disk, so the
    walk_source assertions test real skip behavior, not file absence."""
    assert (sample_kb_tree / "build" / "skipme.md").is_file()
    assert (sample_kb_tree / ".git" / "HEAD").is_file()
    assert (sample_kb_tree / "notes" / "draft.tmp").is_file()
    assert (sample_kb_tree / "notes" / "empty.md").is_file()

    paths = {r.rel_path for r in walk_source(kb_source)}
    assert "build/skipme.md" not in paths
    assert ".git/HEAD" not in paths
    assert "notes/draft.tmp" not in paths
    assert "notes/empty.md" not in paths
