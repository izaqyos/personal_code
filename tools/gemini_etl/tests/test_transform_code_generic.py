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


def test_unknown_ext_uses_window_fallback():
    """Unknown extension (no pattern in _PATTERNS) falls back to window chunks
    and returns ALL windows, not just the first."""
    src = "x" * 2000
    chunks = chunk_generic(
        text=src, source="s", rel_path="f.rs", ext=".rs",
        token_limit=100,
        count_tokens=lambda t: max(1, len(t) // 4),
    )
    assert len(chunks) >= 2


def test_preamble_before_first_def_is_kept():
    """Content before the first regex match (license header, etc.) must be
    preserved as its own chunk, not silently dropped."""
    src = "// Copyright 2024 yosi\n\nfunction main() {\n  return 0;\n}\n"
    chunks = chunk_generic(
        text=src, source="s", rel_path="f.js", ext=".js",
        token_limit=1, count_tokens=_above,
    )
    assert any("Copyright" in c.text for c in chunks)


def test_c_regex_does_not_match_control_flow_at_col_zero():
    """Negative lookahead must keep for/if/while/switch from being treated
    as function starts when they appear at column 0."""
    src = (
        "int alpha(int x) {\n"
        "  return x;\n"
        "}\n"
        "for (int i = 0; i < 10; i++) {\n"  # col 0, but must NOT split here
        "  do_stuff();\n"
        "}\n"
        "int beta(int x) {\n"
        "  return x + 1;\n"
        "}\n"
    )
    chunks = chunk_generic(
        text=src, source="s", rel_path="f.c", ext=".c",
        token_limit=1, count_tokens=_above,
    )
    bodies = [c.text for c in chunks]
    # Should split on `alpha` and `beta`, NOT on `for`. So `for (` should
    # appear in the same chunk as `alpha` (or in a preamble/middle chunk)
    # not as the start of its own chunk.
    for_chunks = [b for b in bodies if "for (int i" in b]
    # Whatever chunk contains `for (int i` should also contain the previous
    # function's closing brace OR be part of `alpha`'s tail — it must not be
    # a chunk that STARTS with `for (`.
    for chunk_text in for_chunks:
        # The body section after the metadata header should not start with `for (`.
        body = chunk_text.split("---\n", 1)[1] if "---\n" in chunk_text else chunk_text
        assert not body.lstrip().startswith("for ("), \
            f"for-loop became its own chunk: {body[:80]!r}"
