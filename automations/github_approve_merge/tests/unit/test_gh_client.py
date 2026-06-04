import pytest

from github_approve_merge import gh_client as gc


def test_run_returns_stdout_on_success():
    fake = gc.FakeRunner(stdout='{"ok": true}', stderr="", returncode=0)
    client = gc.GhClient(runner=fake)
    assert client._run(["api", "user"]) == '{"ok": true}'
    assert fake.calls == [["gh", "api", "user"]]


def test_run_raises_auth_error_on_sso_message():
    fake = gc.FakeRunner(stdout="", stderr="SSO authorization required", returncode=1)
    client = gc.GhClient(runner=fake)
    with pytest.raises(gc.GhAuthError):
        client._run(["pr", "view", "1"])


def test_run_raises_not_found_on_404():
    fake = gc.FakeRunner(stdout="", stderr="Could not resolve to a Repository", returncode=1)
    client = gc.GhClient(runner=fake)
    with pytest.raises(gc.GhNotFound):
        client._run(["pr", "view", "1"])


def test_run_raises_generic_on_other_failure():
    fake = gc.FakeRunner(stdout="", stderr="boom", returncode=1)
    client = gc.GhClient(runner=fake)
    with pytest.raises(gc.GhError):
        client._run(["pr", "view", "1"])


import json as _json

PR_JSON = _json.dumps({
    "number": 565, "state": "OPEN", "isDraft": False, "locked": False,
    "mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN",
    "reviewDecision": "APPROVED",
    "author": {"login": "chkp-muhammady"}, "baseRefName": "master",
    "reviews": [{"author": {"login": "YosiIzaq"}, "state": "APPROVED"}],
})


def test_fetch_pr_parses_fields():
    fake = gc.FakeRunner(stdout=PR_JSON)
    client = gc.GhClient(runner=fake)
    pr = client.fetch_pr("perimeter-81", "platform-global-domain", 565)
    assert pr.state == "OPEN"
    assert pr.mergeable == "MERGEABLE"
    assert pr.review_decision == "APPROVED"
    assert pr.author_login == "chkp-muhammady"
    assert pr.base_ref == "master"
    assert pr.approved_by("YosiIzaq") is True
    assert pr.approved_by("someone-else") is False


def test_current_login():
    fake = gc.FakeRunner(stdout="YosiIzaq\n")
    client = gc.GhClient(runner=fake)
    assert client.current_login() == "YosiIzaq"


def test_has_merge_queue_true_when_node_present():
    fake = gc.FakeRunner(stdout=_json.dumps(
        {"data": {"repository": {"mergeQueue": {"id": "MQ_x"}}}}))
    client = gc.GhClient(runner=fake)
    assert client.has_merge_queue("perimeter-81", "platform-global-domain", "master") is True


def test_has_merge_queue_false_when_null():
    fake = gc.FakeRunner(stdout=_json.dumps(
        {"data": {"repository": {"mergeQueue": None}}}))
    client = gc.GhClient(runner=fake)
    assert client.has_merge_queue("perimeter-81", "platform-global-domain", "master") is False


def test_preflight_ok():
    fake = gc.FakeRunner(stdout="Logged in to github.com account YosiIzaq", returncode=0)
    gc.GhClient(runner=fake).preflight()  # no raise


def test_preflight_raises_auth_when_logged_out():
    fake = gc.FakeRunner(stdout="", stderr="You are not logged into any GitHub hosts", returncode=1)
    with pytest.raises(gc.GhAuthError):
        gc.GhClient(runner=fake).preflight()


def test_enqueue_calls_graphql_mutation():
    fake = gc.FakeRunner(queue=[
        (_json.dumps({"data": {"repository": {"pullRequest": {"id": "PR_x"}}}}), "", 0),  # node id
        (_json.dumps({"data": {"enqueuePullRequest": {"mergeQueueEntry": {"state": "QUEUED"}}}}), "", 0),
    ])
    client = gc.GhClient(runner=fake)
    client.enqueue("perimeter-81", "platform-global-domain", 565)
    assert any("enqueuePullRequest" in " ".join(c) for c in fake.calls)


def test_direct_merge_uses_method_flag():
    fake = gc.FakeRunner(stdout="", returncode=0)
    client = gc.GhClient(runner=fake)
    client.direct_merge("perimeter-81", "repo", 7, method="merge")
    assert fake.calls[-1] == ["gh", "pr", "merge", "7", "--repo",
                              "perimeter-81/repo", "--merge"]


def test_approve_calls_pr_review():
    fake = gc.FakeRunner(returncode=0)
    client = gc.GhClient(runner=fake)
    client.approve("perimeter-81", "repo", 7)
    assert fake.calls[-1] == ["gh", "pr", "review", "7", "--repo",
                              "perimeter-81/repo", "--approve"]


def test_direct_merge_falls_back_by_attempting_other_methods():
    # Repo allow_* flags are unreliable (branch rulesets override them), so the fallback
    # *attempts* other methods rather than reading flags. Requested merge fails → squash works.
    fake = gc.FakeRunner(queue=[
        ("", "Merge commits are not allowed on this repository", 1),  # --merge fails
        ("", "", 0),                                                  # --squash succeeds
    ])
    client = gc.GhClient(runner=fake)
    client.direct_merge("perimeter-81", "repo", 7, method="merge")
    assert fake.calls[-1] == ["gh", "pr", "merge", "7", "--repo",
                              "perimeter-81/repo", "--squash"]
    # No repo-flags query — we never call `gh api repos/...`.
    assert all("api" not in c for c in fake.calls)


def test_direct_merge_raises_when_all_methods_disallowed():
    fake = gc.FakeRunner(queue=[
        ("", "Merge commits are not allowed", 1),
        ("", "Squash merges are not allowed", 1),
        ("", "Rebase merges are not allowed", 1),
    ])
    with pytest.raises(gc.GhError):
        gc.GhClient(runner=fake).direct_merge("o", "r", 7, method="merge")


def test_direct_merge_no_fallback_on_first_success():
    fake = gc.FakeRunner(stdout="", returncode=0)
    gc.GhClient(runner=fake).direct_merge("o", "r", 7, method="squash")
    assert len(fake.calls) == 1
    assert fake.calls[0][-1] == "--squash"


def test_prclient_classify_caches_queue_probe():
    # fetch_pr makes 2 gh calls (pr view + locked REST); has_merge_queue is a 3rd.
    fake = gc.FakeRunner(queue=[
        (PR_JSON, "", 0),                                                # classify1: pr view
        ("false", "", 0),                                               # classify1: locked REST
        (_json.dumps({"data": {"repository": {"mergeQueue": {"id": "x"}}}}), "", 0),  # queue probe
        (PR_JSON, "", 0),                                                # classify2: pr view
        ("false", "", 0),                                               # classify2: locked REST
    ])
    pc = gc.PrClient(gh=gc.GhClient(runner=fake), owner="o", repo="r", number=565, me="YosiIzaq")
    pc.classify(None)
    pc.classify(None)            # second classify must NOT re-probe the queue
    probe_calls = [c for c in fake.calls if "mergeQueue" in " ".join(c)]
    assert len(probe_calls) == 1
    assert pc.has_queue(None) is True
