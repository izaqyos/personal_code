import sys
from pathlib import Path

import pytest

from github_approve_merge.cli import build_parser, main


class TestArgs:
    def test_help_smoke(self, capsys):
        with pytest.raises(SystemExit) as exc:
            build_parser().parse_args(["--help"])
        assert exc.value.code == 0
        assert "gh-approve-merge" in capsys.readouterr().out

    def test_parser_has_new_verbs(self):
        p = build_parser()
        sub = [a for a in p._actions if a.dest == "command"][0]
        assert set(sub.choices) >= {"auth", "approve", "merge", "run", "gc"}

    def test_run_with_url(self):
        ns = build_parser().parse_args(["run", "https://github.com/o/r/pull/1"])
        assert ns.command == "run"
        assert ns.urls == ["https://github.com/o/r/pull/1"]

    def test_run_accepts_merge_method_and_yes(self):
        ns = build_parser().parse_args(["run", "--merge-method", "squash", "--yes",
                                        "https://github.com/o/r/pull/1"])
        assert ns.merge_method == "squash"
        assert ns.yes is True

    def test_merge_method_default_is_merge(self):
        ns = build_parser().parse_args(["merge", "https://github.com/o/r/pull/1"])
        assert ns.merge_method == "merge"

    def test_no_auth_login_subcommand(self):
        with pytest.raises(SystemExit):
            build_parser().parse_args(["auth", "login"])  # login removed; only `status`

    def test_gc_subcommand_parses(self):
        ns = build_parser().parse_args(["gc", "--retention-days", "5"])
        assert ns.command == "gc"
        assert ns.retention_days == 5

    def test_redact_logs_flag_parses(self):
        ns = build_parser().parse_args(["run", "https://github.com/acme-org/widgets-service/pull/1",
                                        "--redact-logs"])
        assert ns.redact_logs is True

    def test_confirm_each_flag_parses(self):
        ns = build_parser().parse_args(["merge", "https://github.com/o/r/pull/1", "--confirm-each"])
        assert ns.confirm_each is True

    def test_resume_and_urls_conflict_returns_2(self, capsys, monkeypatch):
        _stub_gh_ok(monkeypatch)
        rc = main(["run", "--resume", "20260526-143012-aaaa",
                   "https://github.com/o/r/pull/1"])
        assert rc == 2
        assert "--resume" in capsys.readouterr().err

    def test_no_inputs_returns_2(self, capsys, monkeypatch):
        _stub_gh_ok(monkeypatch)
        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        rc = main(["run"])
        assert rc == 2


def _stub_gh_ok(monkeypatch):
    """Make preflight + current_login succeed without touching real gh."""
    from github_approve_merge import gh_client
    monkeypatch.setattr(gh_client.GhClient, "preflight", lambda self: None)
    monkeypatch.setattr(gh_client.GhClient, "current_login", lambda self: "me")


class TestRunWiring:
    def test_run_invokes_run_batch_with_resolved_inputs(self, tmp_path: Path, monkeypatch):
        _stub_gh_ok(monkeypatch)
        calls = {}

        async def fake_run_batch(prs, **kwargs):
            calls["prs"] = list(prs)
            calls["kwargs"] = kwargs
            return {"exit_code": 0, "counts": {}, "prs": []}

        def fake_sweep(root, max_age_days, skip):
            calls["sweep_days"] = max_age_days
            return []

        from github_approve_merge import cli, retention
        monkeypatch.setattr(cli, "run_batch", fake_run_batch)
        monkeypatch.setattr(retention, "sweep", fake_sweep)

        rc = main(["run", "https://github.com/o/r/pull/1", "--yes",
                   "--logs-dir", str(tmp_path / "logs")])
        assert rc == 0
        assert [str(p) for p in calls["prs"]] == ["o/r#1"]
        assert calls["kwargs"]["method"] == "merge"
        assert calls["sweep_days"] == 10

    def test_merge_verb_sets_no_approve(self, tmp_path: Path, monkeypatch):
        _stub_gh_ok(monkeypatch)
        calls = {}

        async def fake_run_batch(prs, **kwargs):
            calls["kwargs"] = kwargs
            return {"exit_code": 0, "counts": {}, "prs": []}

        from github_approve_merge import cli, retention
        monkeypatch.setattr(cli, "run_batch", fake_run_batch)
        monkeypatch.setattr(retention, "sweep", lambda *a, **k: [])

        main(["merge", "https://github.com/o/r/pull/1", "--yes",
              "--logs-dir", str(tmp_path / "logs")])
        assert calls["kwargs"]["approve"] is False
        assert calls["kwargs"]["do_merge"] is True

    def test_approve_verb_sets_no_merge(self, tmp_path: Path, monkeypatch):
        _stub_gh_ok(monkeypatch)
        calls = {}

        async def fake_run_batch(prs, **kwargs):
            calls["kwargs"] = kwargs
            return {"exit_code": 0, "counts": {}, "prs": []}

        from github_approve_merge import cli, retention
        monkeypatch.setattr(cli, "run_batch", fake_run_batch)
        monkeypatch.setattr(retention, "sweep", lambda *a, **k: [])

        main(["approve", "https://github.com/o/r/pull/1",
              "--logs-dir", str(tmp_path / "logs")])
        assert calls["kwargs"]["approve"] is True
        assert calls["kwargs"]["do_merge"] is False
