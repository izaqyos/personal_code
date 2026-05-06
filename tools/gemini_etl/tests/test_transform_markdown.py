from gemini_etl.transform.markdown import Chunk, chunk_markdown  # noqa: F401


def _under_threshold(_text: str) -> int:
    return 100


def _above_threshold_for_long(text: str) -> int:
    # Anything over 200 chars is "huge".
    return 99_999 if len(text) > 200 else 100


def test_short_file_is_one_chunk():
    md = "# Title\n\nbody\n"
    chunks = chunk_markdown(
        text=md,
        source="personal_KB",
        rel_path="a.md",
        token_limit=10_000,
        count_tokens=_under_threshold,
    )
    assert len(chunks) == 1
    assert chunks[0].text.endswith(md.strip())  # body preserved
    assert "[Source: personal_KB]" in chunks[0].text


def test_frontmatter_folded_into_header():
    md = (
        "---\n"
        "title: Foo\n"
        "tags: [a, b]\n"
        "---\n"
        "# heading\nbody\n"
    )
    chunks = chunk_markdown(
        text=md,
        source="personal_KB",
        rel_path="x.md",
        token_limit=10_000,
        count_tokens=_under_threshold,
    )
    assert len(chunks) == 1
    assert "[Title: Foo]" in chunks[0].text
    assert "[Tags: a, b]" in chunks[0].text
    # Frontmatter delimiters do not appear in body.
    assert "---\ntitle:" not in chunks[0].text


def test_oversize_file_splits_at_h1():
    md = (
        "# Section A\n" + ("a" * 250) + "\n"
        "# Section B\n" + ("b" * 250) + "\n"
    )
    chunks = chunk_markdown(
        text=md,
        source="personal_KB",
        rel_path="big.md",
        token_limit=50,
        count_tokens=_above_threshold_for_long,
    )
    assert len(chunks) == 2
    assert "[Section: # Section A]" in chunks[0].text
    assert "[Section: # Section B]" in chunks[1].text


def test_recursive_split_to_h2():
    h2_block_a = "## Sub A\n" + ("a" * 250) + "\n"
    h2_block_b = "## Sub B\n" + ("b" * 250) + "\n"
    md = "# Top\n" + h2_block_a + h2_block_b
    chunks = chunk_markdown(
        text=md,
        source="personal_KB",
        rel_path="big.md",
        token_limit=50,
        count_tokens=_above_threshold_for_long,
    )
    # H1 is one block over threshold → split into H2s.
    assert len(chunks) == 2
    assert "[Section: # Top / ## Sub A]" in chunks[0].text
    assert "[Section: # Top / ## Sub B]" in chunks[1].text


def test_chunk_text_includes_metadata_header_and_body():
    md = "body only\n"
    chunks = chunk_markdown(
        text=md, source="s", rel_path="p.md",
        token_limit=10_000, count_tokens=_under_threshold,
    )
    assert chunks[0].text.startswith("[Source: s]")
    assert "---\nbody only" in chunks[0].text


def test_preamble_prose_is_preserved_as_own_chunk():
    """Intro prose before the first H2 must become a chunk, not be silently dropped."""
    md = (
        "# Parent\n"
        "Intro paragraph.\n"
        "## Sub A\n" + ("a" * 250) + "\n"
        "## Sub B\n" + ("b" * 250) + "\n"
    )
    chunks = chunk_markdown(
        text=md, source="s", rel_path="p.md",
        token_limit=50, count_tokens=_above_threshold_for_long,
    )
    # Expected: 3 chunks — the H1 preamble (intro paragraph) and the 2 H2 sections.
    assert len(chunks) == 3
    intro = chunks[0]
    assert "Intro paragraph." in intro.text
    assert "[Section: # Parent]" in intro.text


def test_preamble_only_headers_suppressed():
    """Preamble that is only header lines (no real prose) should not produce a chunk."""
    md = (
        "# Parent\n"
        "## Sub A\n" + ("a" * 250) + "\n"
        "## Sub B\n" + ("b" * 250) + "\n"
    )
    chunks = chunk_markdown(
        text=md, source="s", rel_path="p.md",
        token_limit=50, count_tokens=_above_threshold_for_long,
    )
    # Only 2 chunks (the two H2s); the empty H1 preamble is dropped by _has_prose.
    assert len(chunks) == 2


def test_string_tags_coerced_to_single_element_tuple():
    md = (
        "---\n"
        "tags: single-tag\n"
        "---\n"
        "body\n"
    )
    chunks = chunk_markdown(
        text=md, source="s", rel_path="p.md",
        token_limit=10_000, count_tokens=_under_threshold,
    )
    assert "[Tags: single-tag]" in chunks[0].text
