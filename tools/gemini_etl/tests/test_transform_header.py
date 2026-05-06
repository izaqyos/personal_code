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
