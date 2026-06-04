"""Live smoke test (read-only).

Skipped by default. Set `PYTEST_LIVE=1` to run. This only *reads* a real PR via `gh`
(no approve, no merge) to confirm auth + the API path work end-to-end.
"""
import os

import pytest

from github_approve_merge.gh_client import GhClient

pytestmark = pytest.mark.skipif(os.environ.get("PYTEST_LIVE") != "1",
                                reason="PYTEST_LIVE=1 not set")


@pytest.mark.live
def test_live_fetch_pr_readonly():
    gh = GhClient()
    gh.preflight()
    pr = gh.fetch_pr("perimeter-81", "platform-global-domain", 565)
    assert pr.number == 565
    assert pr.state in {"OPEN", "MERGED", "CLOSED"}
