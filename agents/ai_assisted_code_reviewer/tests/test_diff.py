import pytest

from aireview.diff import GitError, collect_diff, parse_diff

from .conftest import SAMPLE_DIFF, commit


@pytest.fixture
def files():
    return {f.path: f for f in parse_diff(SAMPLE_DIFF)}


def test_paths_and_statuses(files):
    assert set(files) == {
        "src/app.ts",
        "src/routes/invoices.ts",
        "old.txt",
        "src/b.ts",
        "logo.png",
    }
    assert files["src/app.ts"].status == "modified"
    assert files["src/routes/invoices.ts"].status == "added"
    assert files["old.txt"].status == "deleted"
    assert files["src/b.ts"].status == "renamed"
    assert files["src/b.ts"].old_path == "src/a.ts"
    assert files["logo.png"].binary


def test_added_line_numbers_track_new_file(files):
    app = files["src/app.ts"]
    assert app.added_lines == {12: 'app.use("/invoices", invoicesRouter);'}
    assert app.hunks == [(10, 14)]
    assert app.touches(12) and app.touches(10) and not app.touches(15)


def test_new_file_lines(files):
    inv = files["src/routes/invoices.ts"]
    assert sorted(inv.added_lines) == [1, 2, 3]
    assert inv.hunks == [(1, 3)]


def test_rename_counts(files):
    b = files["src/b.ts"]
    assert b.added_lines == {2: "const b = 3;"}
    assert b.removed_count == 1


def test_deleted_file_has_no_added_lines(files):
    old = files["old.txt"]
    assert old.added_count == 0 and old.removed_count == 2


def test_no_newline_marker_ignored():
    d = parse_diff(
        "diff --git a/x b/x\n--- a/x\n+++ b/x\n@@ -1 +1 @@\n"
        "-a\n\\ No newline at end of file\n+b\n\\ No newline at end of file\n"
    )
    assert d[0].added_lines == {1: "b"}


def test_multiple_hunks_line_numbers():
    d = parse_diff(
        "diff --git a/x b/x\n--- a/x\n+++ b/x\n"
        "@@ -1,2 +1,3 @@\n a\n+b\n c\n"
        "@@ -20,2 +21,2 @@\n x\n-y\n+z\n"
    )
    assert d[0].added_lines == {2: "b", 22: "z"}
    assert d[0].hunks == [(1, 3), (21, 22)]


def test_empty_diff():
    assert parse_diff("") == []


def test_collect_diff_committed_vs_uncommitted(git_repo):
    (git_repo / "a.txt").write_text("one\n")
    commit(git_repo)
    import subprocess

    subprocess.run(["git", "checkout", "-q", "-b", "feat"], cwd=git_repo, check=True)
    (git_repo / "a.txt").write_text("one\ntwo\n")
    commit(git_repo)
    (git_repo / "a.txt").write_text("one\ntwo\nthree\n")  # uncommitted

    committed = parse_diff(collect_diff(git_repo, "main"))
    assert committed[0].added_lines == {2: "two"}
    wip = parse_diff(collect_diff(git_repo, "main", include_uncommitted=True))
    assert wip[0].added_lines == {2: "two", 3: "three"}


def test_collect_diff_bad_base(git_repo):
    (git_repo / "a.txt").write_text("x\n")
    commit(git_repo)
    with pytest.raises(GitError):
        collect_diff(git_repo, "no-such-ref")
