"""End-to-end test: real example schedule, all CLI variants render."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

DAILY_RUNNER_DIR = Path(__file__).resolve().parents[2]


@pytest.fixture
def cfg_with_example_schedule(tmp_path: Path) -> Path:
    schedules_src = DAILY_RUNNER_DIR / "config" / "schedules.example.json"
    schedules_dst = tmp_path / "schedules.json"
    schedules_dst.write_text(schedules_src.read_text())

    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(
        json.dumps(
            {
                "version": "1.0",
                "banner": {
                    "enabled": False,
                    "schedules_path": str(schedules_dst),
                    "default_fields": [
                        "sprint",
                        "sprint_week",
                        "champion",
                        "dod",
                        "next_event",
                    ],
                },
            }
        )
    )
    return cfg_path


class _Result:
    """Lightweight stand-in for CompletedProcess that always exposes stdout/stderr."""

    def __init__(self, stdout: str, stderr: str, returncode: int | None) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


def _run(cfg: Path, *extra_args: str, timeout: int = 5) -> _Result:
    """Run the CLI as a subprocess and return its captured output.

    The CLI prints the banner, then enters an interactive Rich/keyboard loop
    which never exits without TTY input. We close stdin and rely on the
    timeout, capturing whatever was printed up to that point. Both clean exits
    and timeouts are normalized to a result object exposing stdout/stderr.
    """
    env = os.environ.copy()
    cmd = [
        sys.executable,
        "main.py",
        "--mode",
        "cli",
        "--config",
        str(cfg),
        "--team",
        "imagine_dragons",
        *extra_args,
    ]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=DAILY_RUNNER_DIR,
            env=env,
            timeout=timeout,
            stdin=subprocess.DEVNULL,
            check=False,
        )
        return _Result(proc.stdout, proc.stderr, proc.returncode)
    except subprocess.TimeoutExpired as exc:
        # Banner is printed early; capture whatever was emitted before the
        # interactive loop started blocking and treat that as the test output.
        stdout = exc.stdout.decode("utf-8", errors="replace") if exc.stdout else ""
        stderr = exc.stderr.decode("utf-8", errors="replace") if exc.stderr else ""
        return _Result(stdout, stderr, None)


def test_bare_b_prints_banner(cfg_with_example_schedule: Path) -> None:
    proc = _run(cfg_with_example_schedule, "-b")
    assert "26.Q1" in proc.stdout or "26.Q2" in proc.stdout

def test_b_with_text_prints_text(cfg_with_example_schedule: Path) -> None:
    proc = _run(cfg_with_example_schedule, "-b", "welcome back Muhe")
    assert "welcome back Muhe" in proc.stdout

def test_no_banner_suppresses_output(cfg_with_example_schedule: Path) -> None:
    proc = _run(cfg_with_example_schedule, "--no-banner")
    assert "26.Q1" not in proc.stdout
    assert "26.Q2" not in proc.stdout

def test_explicit_fields_and_text(cfg_with_example_schedule: Path) -> None:
    proc = _run(
        cfg_with_example_schedule,
        "--banner-fields",
        "sprint,dod",
        "--banner-text",
        "hello team",
    )
    assert "hello team" in proc.stdout

def test_missing_schedule_error_banner(tmp_path: Path) -> None:
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(
        json.dumps(
            {
                "version": "1.0",
                "banner": {
                    "enabled": False,
                    "schedules_path": "/definitely/does/not/exist.json",
                    "default_fields": ["sprint"],
                },
            }
        )
    )
    proc = _run(cfg_path, "-b")
    assert "unavailable" in proc.stdout.lower()
    assert "definitely/does/not/exist.json" in proc.stdout
