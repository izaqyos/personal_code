import pytest

from gemini_etl.manifest import FileState, Manifest, ManifestRow


@pytest.fixture
def manifest(tmp_path) -> Manifest:
    return Manifest(tmp_path / "test.sqlite")


def test_new_file_is_new(manifest):
    state = manifest.classify("personal_KB", "notes/foo.md", "abc123")
    assert state is FileState.NEW


def test_unchanged_file(manifest):
    manifest.upsert(ManifestRow(
        source="personal_KB", rel_path="a.md", sha256="hash",
        display_name="personal_KB/a.md", document_id="docs/1",
    ))
    state = manifest.classify("personal_KB", "a.md", "hash")
    assert state is FileState.UNCHANGED


def test_changed_file_when_sha_differs(manifest):
    manifest.upsert(ManifestRow(
        source="personal_KB", rel_path="a.md", sha256="old",
        display_name="personal_KB/a.md", document_id="docs/1",
    ))
    state = manifest.classify("personal_KB", "a.md", "new")
    assert state is FileState.CHANGED


def test_deleted_files_diff(manifest):
    for path in ("a.md", "b.md", "c.md"):
        manifest.upsert(ManifestRow(
            source="personal_KB", rel_path=path, sha256="h",
            display_name=f"personal_KB/{path}", document_id="d",
        ))
    live = {("personal_KB", "a.md"), ("personal_KB", "c.md")}
    deleted = list(manifest.deleted_rows(live_set=live))
    assert len(deleted) == 1
    assert deleted[0].rel_path == "b.md"


def test_get_row_returns_existing(manifest):
    row = ManifestRow(
        source="personal_KB", rel_path="a.md", sha256="h",
        display_name="personal_KB/a.md", document_id="docs/9",
    )
    manifest.upsert(row)
    got = manifest.get("personal_KB", "a.md")
    assert got is not None
    assert got.document_id == "docs/9"
    assert got.uploaded_at is not None  # substituted by upsert when row had None


def test_delete_row_removes(manifest):
    manifest.upsert(ManifestRow(
        source="personal_KB", rel_path="a.md", sha256="h",
        display_name="personal_KB/a.md", document_id="d",
    ))
    manifest.delete("personal_KB", "a.md")
    assert manifest.get("personal_KB", "a.md") is None


def test_summary_counts(manifest):
    for i in range(3):
        manifest.upsert(ManifestRow(
            source="personal_KB", rel_path=f"k{i}.md", sha256="h",
            display_name=f"personal_KB/k{i}.md", document_id="d",
        ))
    for i in range(2):
        manifest.upsert(ManifestRow(
            source="personal_code", rel_path=f"c{i}.py", sha256="h",
            display_name=f"personal_code/c{i}.py", document_id="d",
        ))
    counts = manifest.summary()
    assert counts == {"personal_KB": 3, "personal_code": 2}


def test_persists_across_instances(tmp_path):
    db = tmp_path / "p.sqlite"
    a = Manifest(db)
    a.upsert(ManifestRow(
        source="personal_KB", rel_path="x.md", sha256="h",
        display_name="personal_KB/x.md", document_id="d",
    ))
    b = Manifest(db)
    assert b.get("personal_KB", "x.md") is not None


def test_close_does_not_raise(manifest):
    manifest.close()


def test_concurrent_upserts_do_not_raise(manifest):
    """Validate check_same_thread=False + Lock combination."""
    import threading

    errors: list[BaseException] = []

    def worker(tid: int) -> None:
        try:
            for i in range(20):
                manifest.upsert(ManifestRow(
                    source="personal_KB",
                    rel_path=f"t{tid}/f{i}.md",
                    sha256=f"hash-{tid}-{i}",
                    display_name=f"personal_KB/t{tid}/f{i}.md",
                    document_id=None,
                ))
                manifest.classify("personal_KB", f"t{tid}/f{i}.md", f"hash-{tid}-{i}")
        except BaseException as e:
            errors.append(e)

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == []
    counts = manifest.summary()
    assert counts.get("personal_KB") == 4 * 20
