"""Tests for the Backup Specialist Agent CLI."""

import os
import subprocess
import sys
import time
from argparse import Namespace
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import backup_agent as ba


# ── Helper function tests ────────────────────────────────────────────────────


class TestFormatSize:
    def test_bytes(self):
        assert ba._format_size(500) == "500.0 B"

    def test_kilobytes(self):
        assert ba._format_size(2048) == "2.0 KB"

    def test_megabytes(self):
        assert ba._format_size(5 * 1024 * 1024) == "5.0 MB"

    def test_gigabytes(self):
        assert ba._format_size(3 * 1024**3) == "3.0 GB"

    def test_terabytes(self):
        assert ba._format_size(2 * 1024**4) == "2.0 TB"

    def test_zero(self):
        assert ba._format_size(0) == "0.0 B"


class TestLastModified:
    def test_nonexistent_path(self, tmp_path):
        assert ba._last_modified(tmp_path / "nope") == "never"

    def test_existing_file(self, tmp_path):
        f = tmp_path / "test.log"
        f.write_text("data")
        result = ba._last_modified(f)
        assert result != "never"
        assert "-" in result and ":" in result  # YYYY-MM-DD HH:MM format


class TestAgeDays:
    def test_nonexistent_path(self, tmp_path):
        assert ba._age_days(tmp_path / "nope") == float("inf")

    def test_fresh_file(self, tmp_path):
        f = tmp_path / "fresh.log"
        f.write_text("data")
        assert ba._age_days(f) < 0.01  # less than ~15 minutes

    def test_old_file(self, tmp_path):
        f = tmp_path / "old.log"
        f.write_text("data")
        old_time = time.time() - (5 * 86400)
        os.utime(f, (old_time, old_time))
        age = ba._age_days(f)
        assert 4.9 < age < 5.1


class TestOutputFormatters:
    def test_ok(self, capsys):
        ba._ok("all good")
        assert "[OK] all good" in capsys.readouterr().out

    def test_warn(self, capsys):
        ba._warn("heads up")
        assert "[!]  heads up" in capsys.readouterr().out

    def test_crit(self, capsys):
        ba._crit("failure")
        assert "[!!] failure" in capsys.readouterr().out

    def test_header(self, capsys):
        ba._header("Section:")
        out = capsys.readouterr().out
        assert "Section:" in out
        assert "---" in out


# ── Status checks ────────────────────────────────────────────────────────────


class TestCheckOnedrive:
    def test_onedrive_not_found(self, capsys, monkeypatch):
        monkeypatch.setattr(ba, "ONEDRIVE_PATH", Path("/nonexistent/onedrive"))
        ba._check_onedrive()
        out = capsys.readouterr().out
        assert "[!!]" in out
        assert "not found" in out

    def test_backup_dir_not_found(self, capsys, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "ONEDRIVE_PATH", tmp_path)
        monkeypatch.setattr(ba, "ONEDRIVE_BACKUP_DIR", tmp_path / "Backups")
        ba._check_onedrive()
        out = capsys.readouterr().out
        assert "[!]" in out

    def test_no_archives(self, capsys, tmp_path, monkeypatch):
        backup_dir = tmp_path / "Backups"
        backup_dir.mkdir()
        monkeypatch.setattr(ba, "ONEDRIVE_PATH", tmp_path)
        monkeypatch.setattr(ba, "ONEDRIVE_BACKUP_DIR", backup_dir)
        ba._check_onedrive()
        out = capsys.readouterr().out
        assert "No backup archives" in out

    def test_fresh_archives(self, capsys, tmp_path, monkeypatch):
        backup_dir = tmp_path / "Backups"
        backup_dir.mkdir()
        (backup_dir / "test_20260209.tar.gz").write_bytes(b"x" * 1024)
        monkeypatch.setattr(ba, "ONEDRIVE_PATH", tmp_path)
        monkeypatch.setattr(ba, "ONEDRIVE_BACKUP_DIR", backup_dir)
        ba._check_onedrive()
        out = capsys.readouterr().out
        assert "[OK]" in out
        assert "1 archives" in out

    def test_stale_archives(self, capsys, tmp_path, monkeypatch):
        backup_dir = tmp_path / "Backups"
        backup_dir.mkdir()
        archive = backup_dir / "old_20260101.tar.gz"
        archive.write_bytes(b"x" * 2048)
        old_time = time.time() - (15 * 86400)
        os.utime(archive, (old_time, old_time))
        monkeypatch.setattr(ba, "ONEDRIVE_PATH", tmp_path)
        monkeypatch.setattr(ba, "ONEDRIVE_BACKUP_DIR", backup_dir)
        ba._check_onedrive()
        out = capsys.readouterr().out
        assert "[!!]" in out
        assert "stale" in out


class TestCheckCheckpoints:
    def test_dir_not_found(self, capsys, monkeypatch):
        monkeypatch.setattr(ba, "CHECKPOINT_BACKUP_DIR", Path("/nonexistent"))
        ba._check_checkpoints()
        out = capsys.readouterr().out
        assert "[!]" in out

    def test_no_backups(self, capsys, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "CHECKPOINT_BACKUP_DIR", tmp_path)
        ba._check_checkpoints()
        out = capsys.readouterr().out
        assert "No checkpoint backups" in out

    def test_fresh_backup(self, capsys, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "CHECKPOINT_BACKUP_DIR", tmp_path)
        (tmp_path / "backup-2026-02-09_120000").mkdir()
        ba._check_checkpoints()
        out = capsys.readouterr().out
        assert "[OK]" in out
        assert "1 backup" in out

    def test_stale_backup(self, capsys, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "CHECKPOINT_BACKUP_DIR", tmp_path)
        d = tmp_path / "backup-2026-01-01_120000"
        d.mkdir()
        old_time = time.time() - (20 * 86400)
        os.utime(d, (old_time, old_time))
        ba._check_checkpoints()
        out = capsys.readouterr().out
        assert "[!!]" in out
        assert "stale" in out

    def test_ignores_non_backup_dirs(self, capsys, tmp_path, monkeypatch):
        monkeypatch.setattr(ba, "CHECKPOINT_BACKUP_DIR", tmp_path)
        (tmp_path / "random-dir").mkdir()
        (tmp_path / "backup-2026-02-09_120000").mkdir()
        ba._check_checkpoints()
        out = capsys.readouterr().out
        assert "1 backup" in out


class TestCheckLaunchagents:
    @patch("backup_agent._launchctl_loaded_jobs")
    def test_all_loaded(self, mock_loaded, capsys):
        mock_loaded.return_value = {
            "com.yosii.gitbackup",
            "com.yosii.onedrive.backup",
            "com.yosii.obsidian.checkpoint",
        }
        ba._check_launchagents()
        out = capsys.readouterr().out
        assert out.count("[OK]") == 3
        assert "[!!]" not in out

    @patch("backup_agent._launchctl_loaded_jobs")
    def test_none_loaded(self, mock_loaded, capsys):
        mock_loaded.return_value = set()
        ba._check_launchagents()
        out = capsys.readouterr().out
        assert out.count("[!!]") == 3
        assert "[OK]" not in out

    @patch("backup_agent._launchctl_loaded_jobs")
    def test_partial_loaded(self, mock_loaded, capsys):
        mock_loaded.return_value = {"com.yosii.gitbackup"}
        ba._check_launchagents()
        out = capsys.readouterr().out
        assert out.count("[OK]") == 1
        assert out.count("[!!]") == 2


# ── Config ───────────────────────────────────────────────────────────────────


class TestConfigShow:
    @patch("backup_agent._load_config")
    def test_show_output(self, mock_config, capsys):
        mock_config.return_value = {
            "repos": {
                "dotfiles": {"local_path": "/tmp/dotfiles", "auto_sync": True},
                "code": {"local_path": "/tmp/code", "auto_sync": False},
            },
            "schedule": {
                "main_backup": {"weekdays": [0, 2, 4], "hour": 15, "minute": 30},
                "checkpoint_backup": {"weekday": 0, "hour": 15, "minute": 0},
            },
            "logging": {"log_file": "/tmp/backup.log", "level": "INFO"},
            "notifications": {"email": {"enabled": True, "to": "test@test.com"}},
        }
        ba.cmd_config(Namespace(action="show"))
        out = capsys.readouterr().out
        assert "dotfiles" in out
        assert "[auto-sync]" in out
        assert "[monitor]" in out
        assert "Sun, Tue, Thu" in out
        assert "15:30" in out
        assert "test@test.com" in out

    @patch("backup_agent._load_config")
    def test_show_no_config(self, mock_config):
        mock_config.return_value = None
        with pytest.raises(SystemExit):
            ba.cmd_config(Namespace(action="show"))


class TestConfigValidate:
    @patch("backup_agent._load_config")
    def test_validate_all_present(self, mock_config, capsys, tmp_path):
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        obs_src = tmp_path / "obsidian"
        obs_src.mkdir()
        cp_src = tmp_path / "checkpoint"
        cp_src.mkdir()
        cp_dst = tmp_path / "backup"
        cp_dst.mkdir()

        mock_config.return_value = {
            "repos": {
                "dotfiles": {"local_path": str(repo_path)},
                "obsidian_notes": {"local_path": str(repo_path), "source_dir": str(obs_src)},
            },
            "checkpoint_backup": {"source": str(cp_src), "destination": str(cp_dst)},
        }

        with patch.object(ba, "VENV_PYTHON", tmp_path / "python"):
            (tmp_path / "python").touch()
            with patch.dict(ba.PLIST_JOBS, {
                k: {**v, "plist": tmp_path / f"{k}.plist"}
                for k, v in ba.PLIST_JOBS.items()
            }):
                for k in ba.PLIST_JOBS:
                    (tmp_path / f"{k}.plist").touch()
                ba.cmd_config(Namespace(action="validate"))

        out = capsys.readouterr().out
        assert "0 issue(s)" in out

    @patch("backup_agent._load_config")
    def test_validate_missing_paths(self, mock_config, capsys):
        mock_config.return_value = {
            "repos": {
                "dotfiles": {"local_path": "/nonexistent/dotfiles"},
                "obsidian_notes": {"local_path": "/nonexistent/obs", "source_dir": "/nonexistent/src"},
            },
            "checkpoint_backup": {"source": "/nonexistent/cp", "destination": "/nonexistent/dst"},
        }
        ba.cmd_config(Namespace(action="validate"))
        out = capsys.readouterr().out
        assert "NOT found" in out
        assert int(out.split("issue(s)")[0].strip().split()[-1]) > 0


# ── Run command ──────────────────────────────────────────────────────────────


class TestRunScript:
    def test_missing_script(self, capsys):
        result = ba._run_script(Path("/nonexistent/backup.py"))
        assert result is False
        assert "not found" in capsys.readouterr().out

    @patch("subprocess.run")
    def test_success(self, mock_run, capsys, tmp_path, monkeypatch):
        script = tmp_path / "backup.py"
        script.touch()
        venv = tmp_path / "python"
        venv.touch()
        monkeypatch.setattr(ba, "VENV_PYTHON", venv)
        monkeypatch.setattr(ba, "GIT_BACKUP_DIR", tmp_path)
        mock_run.return_value = MagicMock(returncode=0)

        result = ba._run_script(script)
        assert result is True
        assert "successfully" in capsys.readouterr().out

    @patch("subprocess.run")
    def test_failure(self, mock_run, capsys, tmp_path, monkeypatch):
        script = tmp_path / "backup.py"
        script.touch()
        venv = tmp_path / "python"
        venv.touch()
        monkeypatch.setattr(ba, "VENV_PYTHON", venv)
        monkeypatch.setattr(ba, "GIT_BACKUP_DIR", tmp_path)
        mock_run.return_value = MagicMock(returncode=1)

        result = ba._run_script(script)
        assert result is False
        assert "Exited with code 1" in capsys.readouterr().out

    @patch("subprocess.run")
    def test_dry_run_flag(self, mock_run, tmp_path, monkeypatch):
        script = tmp_path / "backup.py"
        script.touch()
        venv = tmp_path / "python"
        venv.touch()
        monkeypatch.setattr(ba, "VENV_PYTHON", venv)
        monkeypatch.setattr(ba, "GIT_BACKUP_DIR", tmp_path)
        mock_run.return_value = MagicMock(returncode=0)

        ba._run_script(script, dry_run=True)
        call_args = mock_run.call_args[0][0]
        assert "--dry-run" in call_args


class TestCmdRun:
    @patch("backup_agent._run_script")
    def test_run_git(self, mock_run):
        mock_run.return_value = True
        ba.cmd_run(Namespace(target="git", dry_run=False))
        mock_run.assert_called_once()
        script_arg = mock_run.call_args[0][0]
        assert "backup.py" in str(script_arg)

    @patch("backup_agent._run_script")
    def test_run_all(self, mock_run):
        mock_run.return_value = True
        ba.cmd_run(Namespace(target="all", dry_run=False))
        assert mock_run.call_count == 3

    @patch("backup_agent._run_script")
    def test_run_with_dry_run(self, mock_run):
        mock_run.return_value = True
        ba.cmd_run(Namespace(target="onedrive", dry_run=True))
        mock_run.assert_called_once_with(ba.PLIST_JOBS["onedrive"]["script"], True)


# ── Launchctl ────────────────────────────────────────────────────────────────


class TestResolveJob:
    def test_exact_key(self):
        job = ba._resolve_job("gitbackup")
        assert job["label"] == "com.yosii.gitbackup"

    def test_label_substring(self):
        job = ba._resolve_job("onedrive")
        assert job["label"] == "com.yosii.onedrive.backup"

    def test_unknown_job(self):
        with pytest.raises(SystemExit):
            ba._resolve_job("nonexistent")


class TestCmdLaunchctlStatus:
    @patch("backup_agent._launchctl_loaded_jobs")
    def test_status_display(self, mock_loaded, capsys):
        mock_loaded.return_value = {"com.yosii.gitbackup"}
        ba.cmd_launchctl(Namespace(action="status", job=None))
        out = capsys.readouterr().out
        assert "LaunchAgent Status" in out
        assert "Loaded" in out
        assert "NOT LOADED" in out

    def test_reload_no_job(self):
        with pytest.raises(SystemExit):
            ba.cmd_launchctl(Namespace(action="reload", job=None))

    def test_logs_no_job(self):
        with pytest.raises(SystemExit):
            ba.cmd_launchctl(Namespace(action="logs", job=None))

    def test_logs_with_files(self, capsys, tmp_path, monkeypatch):
        log_content = "\n".join([f"line {i}" for i in range(40)])
        stdout_log = tmp_path / "stdout.log"
        stderr_log = tmp_path / "stderr.log"
        stdout_log.write_text(log_content)
        stderr_log.write_text("error line")

        test_jobs = {
            "testjob": {
                "label": "com.test.job",
                "plist": tmp_path / "test.plist",
                "script": tmp_path / "test.py",
                "schedule": "Daily @ 12:00",
                "stdout_log": stdout_log,
                "stderr_log": stderr_log,
            }
        }
        monkeypatch.setattr(ba, "PLIST_JOBS", test_jobs)
        ba.cmd_launchctl(Namespace(action="logs", job="testjob"))
        out = capsys.readouterr().out
        assert "line 39" in out  # last line shown
        assert "line 0" not in out  # first line truncated (only last 30)
        assert "error line" in out

    def test_logs_missing_file(self, capsys, tmp_path, monkeypatch):
        test_jobs = {
            "testjob": {
                "label": "com.test.job",
                "plist": tmp_path / "test.plist",
                "script": tmp_path / "test.py",
                "schedule": "Daily @ 12:00",
                "stdout_log": tmp_path / "nope_stdout.log",
                "stderr_log": tmp_path / "nope_stderr.log",
            }
        }
        monkeypatch.setattr(ba, "PLIST_JOBS", test_jobs)
        ba.cmd_launchctl(Namespace(action="logs", job="testjob"))
        out = capsys.readouterr().out
        assert "(no log file)" in out


# ── CLI argument parsing ─────────────────────────────────────────────────────


class TestCLIParsing:
    def _parse(self, args_list):
        """Helper: parse args like main() does."""
        parser = ba.argparse.ArgumentParser(prog="backup_agent")
        sub = parser.add_subparsers(dest="command")
        sub.add_parser("status")
        run_p = sub.add_parser("run")
        run_p.add_argument("target", choices=["git", "onedrive", "checkpoint", "all"])
        run_p.add_argument("--dry-run", action="store_true")
        config_p = sub.add_parser("config")
        config_p.add_argument("action", choices=["show", "edit", "validate"])
        launch_p = sub.add_parser("launchctl")
        launch_p.add_argument("action", choices=["status", "reload", "logs"])
        launch_p.add_argument("job", nargs="?")
        return parser.parse_args(args_list)

    def test_status(self):
        args = self._parse(["status"])
        assert args.command == "status"

    def test_run_git(self):
        args = self._parse(["run", "git"])
        assert args.command == "run"
        assert args.target == "git"
        assert args.dry_run is False

    def test_run_dry_run(self):
        args = self._parse(["run", "checkpoint", "--dry-run"])
        assert args.dry_run is True

    def test_config_show(self):
        args = self._parse(["config", "show"])
        assert args.action == "show"

    def test_launchctl_logs(self):
        args = self._parse(["launchctl", "logs", "gitbackup"])
        assert args.action == "logs"
        assert args.job == "gitbackup"

    def test_launchctl_no_job(self):
        args = self._parse(["launchctl", "status"])
        assert args.job is None

    def test_invalid_target(self):
        with pytest.raises(SystemExit):
            self._parse(["run", "invalid"])


# ── Weekday mapping ─────────────────────────────────────────────────────────


class TestWeekdayNames:
    def test_sunday_is_zero(self):
        assert ba.WEEKDAY_NAMES[0] == "Sun"

    def test_saturday_is_six(self):
        assert ba.WEEKDAY_NAMES[6] == "Sat"

    def test_config_weekdays_map_correctly(self):
        config_weekdays = [0, 2, 4]
        names = [ba.WEEKDAY_NAMES[d] for d in config_weekdays]
        assert names == ["Sun", "Tue", "Thu"]


# ── Integration: full status command ─────────────────────────────────────────


class TestCmdStatusIntegration:
    @patch("backup_agent._check_checkpoints")
    @patch("backup_agent._check_onedrive")
    @patch("backup_agent._check_git_repos")
    @patch("backup_agent._check_launchagents")
    def test_status_calls_all_checks(self, mock_la, mock_git, mock_od, mock_cp, capsys):
        ba.cmd_status(Namespace())
        mock_la.assert_called_once()
        mock_git.assert_called_once()
        mock_od.assert_called_once()
        mock_cp.assert_called_once()
        out = capsys.readouterr().out
        assert "Backup System Status" in out


# ── PLIST_JOBS structure ─────────────────────────────────────────────────────


class TestPlistJobsIntegrity:
    """Verify the PLIST_JOBS dict is well-formed."""

    def test_all_jobs_have_required_keys(self):
        required = {"label", "plist", "script", "schedule", "stdout_log", "stderr_log"}
        for name, job in ba.PLIST_JOBS.items():
            missing = required - set(job.keys())
            assert not missing, f"Job '{name}' missing keys: {missing}"

    def test_three_jobs_defined(self):
        assert set(ba.PLIST_JOBS.keys()) == {"gitbackup", "onedrive", "checkpoint"}

    def test_labels_are_unique(self):
        labels = [j["label"] for j in ba.PLIST_JOBS.values()]
        assert len(labels) == len(set(labels))
