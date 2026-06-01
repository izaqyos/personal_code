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
