"""Live smoke test.

Skipped by default. Set `PYTEST_LIVE=1` and `LIVE_TEST_PR_URL=https://github.com/...` to run.
The test will REAL-WORLD approve and (auto-)merge the target PR — only point it at a throwaway
PR in a sandbox repo.
"""
import os
import subprocess
import sys

import pytest


@pytest.mark.live
def test_approve_and_merge_throwaway_pr(tmp_path):
    url = os.environ.get("LIVE_TEST_PR_URL")
    if not url:
        pytest.skip("LIVE_TEST_PR_URL not set")
    result = subprocess.run(
        [sys.executable, "-m", "github_approve_merge", "run", url,
         "--logs-dir", str(tmp_path / "logs")],
        capture_output=True, text=True, check=False,
    )
    print(result.stdout)
    print(result.stderr, file=sys.stderr)
    assert result.returncode in (0, 1), f"unexpected exit code {result.returncode}"
