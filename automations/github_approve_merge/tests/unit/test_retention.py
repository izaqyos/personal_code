import os
import time
from pathlib import Path

from github_approve_merge.retention import sweep


def _touch_dir(root: Path, name: str, age_days: float) -> Path:
    d = root / name
    d.mkdir()
    (d / "marker").write_text("x")
    mtime = time.time() - age_days * 86400
    os.utime(d, (mtime, mtime))
    return d


class TestSweep:
    def test_deletes_only_run_dirs_older_than_threshold(self, tmp_path: Path):
        old_a = _touch_dir(tmp_path, "20260101-100000-aaaa", age_days=15)
        old_b = _touch_dir(tmp_path, "20260102-100000-bbbb", age_days=12)
        fresh = _touch_dir(tmp_path, "20260520-100000-cccc", age_days=2)

        deleted = sweep(tmp_path, max_age_days=10, skip=set())
        assert set(deleted) == {old_a, old_b}
        assert not old_a.exists()
        assert not old_b.exists()
        assert fresh.exists()

    def test_skip_set_protects_current_run_dir(self, tmp_path: Path):
        old = _touch_dir(tmp_path, "20260101-100000-aaaa", age_days=15)
        deleted = sweep(tmp_path, max_age_days=10, skip={old})
        assert deleted == []
        assert old.exists()

    def test_non_matching_dir_name_is_never_deleted(self, tmp_path: Path):
        not_a_run = tmp_path / "old_logs"
        not_a_run.mkdir()
        mtime = time.time() - 30 * 86400
        os.utime(not_a_run, (mtime, mtime))

        deleted = sweep(tmp_path, max_age_days=10, skip=set())
        assert deleted == []
        assert not_a_run.exists()

    def test_misplaced_storage_state_file_is_never_deleted(self, tmp_path: Path):
        stray = tmp_path / "storage_state.json"
        stray.write_text("{}")
        mtime = time.time() - 30 * 86400
        os.utime(stray, (mtime, mtime))

        deleted = sweep(tmp_path, max_age_days=10, skip=set())
        assert deleted == []
        assert stray.exists()

    def test_missing_logs_root_returns_empty(self, tmp_path: Path):
        missing = tmp_path / "no_such_dir"
        assert sweep(missing, max_age_days=10, skip=set()) == []
