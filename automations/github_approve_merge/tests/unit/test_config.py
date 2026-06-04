from pathlib import Path

from github_approve_merge.config import (
    DEFAULT_RETENTION_DAYS,
    RUN_ID_PATTERN,
    default_logs_dir,
    generate_run_id,
)


class TestDefaults:
    def test_retention_days(self):
        assert DEFAULT_RETENTION_DAYS == 10

    def test_default_logs_dir_is_cwd_relative(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        assert default_logs_dir() == tmp_path / "logs"


class TestRunId:
    def test_pattern_matches_format(self):
        rid = generate_run_id()
        assert RUN_ID_PATTERN.match(rid), f"run id {rid!r} doesn't match pattern"

    def test_pattern_constant(self):
        assert RUN_ID_PATTERN.pattern == r"^\d{8}-\d{6}-[a-f0-9]{4}$"

    def test_two_ids_differ(self):
        # rand4 suffix ensures uniqueness even within the same second
        assert generate_run_id() != generate_run_id()
