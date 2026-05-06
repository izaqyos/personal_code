from gemini_etl.transform.header import ChunkMetadata, build_header


def test_minimal_header():
    meta = ChunkMetadata(
        source="personal_KB",
        rel_path="notes/foo.md",
        ext=".md",
    )
    h = build_header(meta)
    assert "[Source: personal_KB]" in h
    assert "[Path: notes/foo.md]" in h
    assert "[Type: .md]" in h
    assert h.endswith("---")


def test_header_includes_title_and_tags():
    meta = ChunkMetadata(
        source="personal_KB", rel_path="x.md", ext=".md",
        title="My Title", tags=("a", "b"),
    )
    h = build_header(meta)
    assert "[Title: My Title]" in h
    assert "[Tags: a, b]" in h


def test_section_path_included():
    meta = ChunkMetadata(
        source="personal_KB", rel_path="x.md", ext=".md",
        section_path=("# Top", "## Sub"),
    )
    assert "[Section: # Top / ## Sub]" in build_header(meta)


def test_empty_optional_fields_omitted():
    meta = ChunkMetadata(source="s", rel_path="p", ext=".md")
    h = build_header(meta)
    assert "Title" not in h
    assert "Tags" not in h
    assert "Section" not in h


def test_empty_tags_tuple_omitted():
    meta = ChunkMetadata(source="s", rel_path="p", ext=".md", tags=())
    assert "Tags" not in build_header(meta)


def test_full_header_exact_structure():
    """Locks in the exact line ordering and final form."""
    meta = ChunkMetadata(
        source="KB", rel_path="a.md", ext=".md",
        title="T", tags=("x",), section_path=("H1",),
    )
    assert build_header(meta) == (
        "[Source: KB] [Path: a.md] [Type: .md]\n"
        "[Title: T] [Tags: x]\n"
        "[Section: H1]\n"
        "---"
    )


def test_whitespace_only_title_omitted():
    meta = ChunkMetadata(source="s", rel_path="p", ext=".md", title="   ")
    assert "Title" not in build_header(meta)


def test_multiline_title_collapsed_to_single_line():
    meta = ChunkMetadata(source="s", rel_path="p", ext=".md", title="line1\nline2")
    h = build_header(meta)
    assert "[Title: line1 line2]" in h
    assert h.count("\n") <= 3  # source line + title line + --- (no extras)


def test_empty_string_tags_filtered():
    meta = ChunkMetadata(source="s", rel_path="p", ext=".md", tags=("a", "", "b"))
    assert "[Tags: a, b]" in build_header(meta)


def test_only_empty_tags_omits_tags_line():
    meta = ChunkMetadata(source="s", rel_path="p", ext=".md", tags=("",))
    assert "Tags" not in build_header(meta)


def test_empty_string_section_path_entries_filtered():
    meta = ChunkMetadata(
        source="s", rel_path="p", ext=".md",
        section_path=("# Top", "", "## Sub"),
    )
    assert "[Section: # Top / ## Sub]" in build_header(meta)


def test_only_empty_section_path_omits_section():
    meta = ChunkMetadata(source="s", rel_path="p", ext=".md", section_path=("",))
    assert "Section" not in build_header(meta)
