import json
import os
import stat
from pathlib import Path

import pytest

from github_approve_merge.auth import (
    AuthStatus,
    AuthStatusResult,
    check_storage_state,
    save_storage_state,
)


class TestSaveStorageState:
    def test_writes_file_with_0600_permissions(self, tmp_path: Path):
        target = tmp_path / "nested" / "storage_state.json"
        payload = {"cookies": [], "origins": []}
        save_storage_state(payload, target)
        assert target.exists()
        assert json.loads(target.read_text()) == payload
        mode = stat.S_IMODE(target.stat().st_mode)
        assert mode == 0o600, oct(mode)

    def test_creates_parent_dirs(self, tmp_path: Path):
        target = tmp_path / "a" / "b" / "c" / "ss.json"
        save_storage_state({"cookies": []}, target)
        assert target.exists()


class TestCheckStorageState:
    def test_missing_file(self, tmp_path: Path):
        result = check_storage_state(tmp_path / "nope.json")
        assert result.status is AuthStatus.MISSING

    def test_unparseable_file(self, tmp_path: Path):
        f = tmp_path / "ss.json"
        f.write_text("not json")
        result = check_storage_state(f)
        assert result.status is AuthStatus.INVALID
        assert "parse" in result.message.lower()

    def test_valid_shape(self, tmp_path: Path):
        f = tmp_path / "ss.json"
        f.write_text(json.dumps({"cookies": [{"name": "user_session"}], "origins": []}))
        result = check_storage_state(f)
        assert result.status is AuthStatus.PRESENT
