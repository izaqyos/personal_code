from gemini_etl.transform.code_generic import chunk_generic


def _below(_t: str) -> int:
    return 1


def _above(_t: str) -> int:
    return 999_999


def test_short_js_is_single_chunk():
    src = "function foo() { return 1; }\n"
    chunks = chunk_generic(
        text=src, source="personal_code", rel_path="x.js", ext=".js",
        token_limit=10_000, count_tokens=_below,
    )
    assert len(chunks) == 1
    assert "function foo" in chunks[0].text


def test_oversize_js_splits_on_top_level_function():
    src = (
        "function alpha() {\n  return 1;\n}\n"
        "function beta() {\n  return 2;\n}\n"
    )
    chunks = chunk_generic(
        text=src, source="personal_code", rel_path="x.js", ext=".js",
        token_limit=1, count_tokens=_above,
    )
    assert len(chunks) >= 2
    bodies = [c.text for c in chunks]
    assert any("alpha" in b and "beta" not in b for b in bodies)
    assert any("beta" in b and "alpha" not in b for b in bodies)


def test_oversize_bash_splits_on_function_keyword():
    src = (
        "function foo() {\n  echo a\n}\n"
        "function bar() {\n  echo b\n}\n"
    )
    chunks = chunk_generic(
        text=src, source="personal_code", rel_path="x.bash", ext=".bash",
        token_limit=1, count_tokens=_above,
    )
    assert len(chunks) >= 2


def test_oversize_chunk_falls_back_to_token_window():
    # One huge "function" that the regex can't split below threshold.
    src = "function huge() {\n" + ("  x = 1;\n" * 200) + "}\n"
    chunks = chunk_generic(
        text=src, source="personal_code", rel_path="x.js", ext=".js",
        token_limit=50,
        count_tokens=lambda t: max(1, len(t) // 4),
    )
    assert len(chunks) >= 2
    # All chunks should be under threshold (give some slack for boundaries).
    for c in chunks:
        assert len(c.text) // 4 < 200
