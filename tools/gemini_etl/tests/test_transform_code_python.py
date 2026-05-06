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
