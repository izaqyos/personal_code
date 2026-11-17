"""Mutation tester must never leave a test process behind (17/11 kernel panic: orphaned 50 GB mutants)."""

from __future__ import annotations

import contextlib
import os
import signal
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import pytest

LIB = Path(__file__).resolve().parent.parent / "lib"
sys.path.insert(0, str(LIB))
import mutate  # noqa: E402

SOURCE = "def f(x):\n    return x < 1\n"
PY = sys.executable


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    # a zombie still answers kill(pid, 0); ps reports it as state Z
    state = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    return bool(state) and not state.startswith("Z")


def _wait_dead(pid: int, seconds: float = 5.0) -> bool:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if not _alive(pid):
            return True
        time.sleep(0.05)
    return False


def _wait_for(path: Path, seconds: float = 10.0) -> str:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if path.exists() and path.read_text().strip():
            return path.read_text().strip()
        time.sleep(0.05)
    raise AssertionError(f"{path} never written")


def _hanging_cmd(pidfile: Path) -> str:
    """A 'test suite' that records its pid and then hangs like an infinite-loop mutant."""
    code = f"import os,time; open({str(pidfile)!r},'w').write(str(os.getpid())); time.sleep(600)"
    return f'{PY} -c "{code}"'


def test_timeout_kills_hanging_tests(tmp_path, monkeypatch):
    monkeypatch.setattr(mutate, "TIMEOUT_SECONDS", 1)
    pidfile = tmp_path / "pid"
    start = time.monotonic()
    assert mutate._passes(_hanging_cmd(pidfile), tmp_path) is False
    assert time.monotonic() - start < 5
    assert _wait_dead(int(pidfile.read_text()))


def test_memory_cap_kills_runaway_allocation(tmp_path, monkeypatch):
    monkeypatch.setattr(mutate, "MEMORY_LIMIT_MB", 200)
    pidfile = tmp_path / "pid"
    # grows ~100 MB per step like an append loop whose `start = end` became `pass`; self-capped at ~2 GB
    # so that a regression in the cap fails this test without endangering the machine
    code = (f"import os,time; open({str(pidfile)!r},'w').write(str(os.getpid())); chunks=[]\\n"
            "while len(chunks) < 20: chunks.append(bytearray(100*1024*1024)); time.sleep(0.05)\\n"
            "time.sleep(600)")
    start = time.monotonic()
    assert mutate._passes(f'{PY} -c "exec(\\"{code}\\")"', tmp_path) is False
    assert time.monotonic() - start < mutate.TIMEOUT_SECONDS / 2, "killed by memory cap, not by timeout"
    assert _wait_dead(int(_wait_for(pidfile)))


def test_passing_and_failing_suites_still_report_correctly(tmp_path):
    assert mutate._passes(f'{PY} -c "pass"', tmp_path) is True
    assert mutate._passes(f'{PY} -c "raise SystemExit(1)"', tmp_path) is False


@pytest.mark.parametrize("sig", [signal.SIGTERM, signal.SIGINT, signal.SIGHUP])
def test_killing_the_runner_mid_mutation_leaves_no_test_process(tmp_path, sig):
    src = tmp_path / "mod.py"
    src.write_text(SOURCE)
    pidfile = tmp_path / "pid"
    driver = tmp_path / "driver.py"
    driver.write_text(textwrap.dedent(f"""
        import sys
        sys.path.insert(0, {str(LIB)!r})
        from pathlib import Path
        import mutate
        mutate.exit_on_signals()          # what `yb main()` does
        mutate.surviving_mutants(Path({str(tmp_path)!r}), ["mod.py"], {_hanging_cmd(pidfile)!r})
    """))
    runner = subprocess.Popen([PY, str(driver)], start_new_session=True)
    test_pid = int(_wait_for(pidfile))
    assert src.read_text() != SOURCE, "a mutant should be on disk while its tests run"

    try:
        os.kill(runner.pid, sig)
        runner.wait(timeout=10)
        assert _wait_dead(test_pid), f"test process {test_pid} outlived the runner (would be orphaned to launchd)"
        assert src.read_text() == SOURCE, "original source must be restored"
    finally:  # never leave an orphan behind, even when this test fails
        with contextlib.suppress(ProcessLookupError):
            os.killpg(test_pid, signal.SIGKILL)
