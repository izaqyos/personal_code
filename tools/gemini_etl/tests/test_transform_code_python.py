import logging

from gemini_etl.transform.code_python import chunk_python


def _always_above(_t: str) -> int:
    return 999_999


def _always_below(_t: str) -> int:
    return 1


def test_short_file_is_one_chunk():
    src = "def foo():\n    return 1\n"
    chunks = chunk_python(
        text=src, source="personal_code", rel_path="m.py",
        token_limit=10_000, count_tokens=_always_below,
    )
    assert len(chunks) == 1
    assert "def foo()" in chunks[0].text


def test_oversize_file_splits_per_top_level_def():
    src = (
        "import os\n"
        "X = 1\n"
        "\n"
        "def alpha():\n    return 1\n"
        "\n"
        "def beta():\n    return 2\n"
    )
    chunks = chunk_python(
        text=src, source="personal_code", rel_path="m.py",
        token_limit=1, count_tokens=_always_above,
    )
    bodies = [c.text for c in chunks]
    # 1 module-prelude + 2 defs = 3 chunks.
    assert len(chunks) == 3
    assert any("import os" in b and "X = 1" in b for b in bodies)
    assert any("def alpha" in b and "def beta" not in b for b in bodies)
    assert any("def beta" in b and "def alpha" not in b for b in bodies)


def test_decorator_stays_attached_to_def():
    src = (
        "@decorator\n"
        "def thing():\n"
        "    \"\"\"docs.\"\"\"\n"
        "    return 1\n"
        "\n"
        "def other():\n"
        "    return 2\n"
    )
    chunks = chunk_python(
        text=src, source="personal_code", rel_path="m.py",
        token_limit=1, count_tokens=_always_above,
    )
    decorated = next(c for c in chunks if "def thing" in c.text)
    assert "@decorator" in decorated.text
    assert "docs." in decorated.text


def test_class_body_is_atomic_chunk():
    src = (
        "class Foo:\n"
        "    def bar(self):\n"
        "        return 1\n"
        "    def baz(self):\n"
        "        return 2\n"
    )
    chunks = chunk_python(
        text=src, source="personal_code", rel_path="m.py",
        token_limit=1, count_tokens=_always_above,
    )
    cls = next(c for c in chunks if "class Foo" in c.text)
    assert "def bar" in cls.text
    assert "def baz" in cls.text


def test_non_def_node_between_defs_keeps_source_order():
    """Module-level statements after a def must remain in source position."""
    src = (
        "def first():\n    return 1\n"
        "\n"
        "CONSTANT = 42\n"
        "\n"
        "def second():\n    return 2\n"
    )
    chunks = chunk_python(
        text=src, source="personal_code", rel_path="m.py",
        token_limit=1, count_tokens=_always_above,
    )
    bodies = [c.text for c in chunks]
    # Order: first(), CONSTANT, second()
    first_idx = next(i for i, b in enumerate(bodies) if "def first" in b)
    const_idx = next(i for i, b in enumerate(bodies) if "CONSTANT = 42" in b)
    second_idx = next(i for i, b in enumerate(bodies) if "def second" in b)
    assert first_idx < const_idx < second_idx


def test_oversize_def_logged_and_emitted_intact(caplog):
    """A single def larger than token_limit gets a warning but is still emitted as one chunk."""
    src = "def huge():\n" + ("    x = 1\n" * 50)

    def _huge_only(t: str) -> int:
        return 999_999 if "x = 1" in t else 1

    with caplog.at_level(logging.WARNING):
        chunks = chunk_python(
            text=src, source="personal_code", rel_path="m.py",
            token_limit=10, count_tokens=_huge_only,
        )

    assert len(chunks) == 1
    assert "oversize def" in caplog.text


def test_empty_file_returns_no_chunks_when_oversize():
    """Empty input under the oversize branch returns []."""
    chunks = chunk_python(
        text="", source="personal_code", rel_path="m.py",
        token_limit=1, count_tokens=_always_above,
    )
    assert chunks == []
