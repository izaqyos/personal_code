from gemini_etl.transform import chunk_file


def _below(_t: str) -> int:
    return 1


def test_dispatches_md_to_markdown():
    chunks = chunk_file(
        text="# h\nbody\n", ext=".md",
        source="s", rel_path="x.md",
        token_limit=10_000, count_tokens=_below,
    )
    assert len(chunks) == 1
    assert "[Type: .md]" in chunks[0].text


def test_dispatches_py_to_python():
    chunks = chunk_file(
        text="def f(): return 1\n", ext=".py",
        source="s", rel_path="m.py",
        token_limit=10_000, count_tokens=_below,
    )
    assert "[Type: .py]" in chunks[0].text


def test_dispatches_js_to_generic():
    chunks = chunk_file(
        text="function f(){}", ext=".js",
        source="s", rel_path="x.js",
        token_limit=10_000, count_tokens=_below,
    )
    assert "[Type: .js]" in chunks[0].text


def test_unknown_extension_raises():
    import pytest
    with pytest.raises(ValueError):
        chunk_file(
            text="x", ext=".xyz",
            source="s", rel_path="x.xyz",
            token_limit=10_000, count_tokens=_below,
        )
