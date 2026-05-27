import sys
from pathlib import Path

import pytest

from github_approve_merge.cli import build_parser, main


class TestArgs:
    def test_help_smoke(self, capsys):
        parser = build_parser()
        with pytest.raises(SystemExit) as exc:
            parser.parse_args(["--help"])
        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert "gh-approve-merge" in out

    def test_run_with_url(self):
        parser = build_parser()
        ns = parser.parse_args(["run", "https://github.com/o/r/pull/1"])
        assert ns.subcommand == "run"
        assert ns.urls == ["https://github.com/o/r/pull/1"]

    def test_resume_and_urls_conflict_returns_2(self, capsys):
        rc = main(["run", "--resume", "20260526-143012-aaaa",
                   "https://github.com/o/r/pull/1"])
        assert rc == 2
        err = capsys.readouterr().err
        assert "--resume" in err

    def test_no_inputs_returns_2(self, capsys, monkeypatch):
        # When stdin is a TTY and no args/file given.
        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        rc = main(["run"])
        assert rc == 2

    def test_version_flag(self, capsys):
        with pytest.raises(SystemExit) as exc:
            main(["--version"])
        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert "0.1.0" in out

    def test_gc_subcommand_parses(self):
        ns = build_parser().parse_args(["gc", "--retention-days", "5"])
        assert ns.subcommand == "gc"
        assert ns.retention_days == 5

    def test_auth_login_subcommand_parses(self):
        ns = build_parser().parse_args(["auth", "login"])
        assert ns.subcommand == "auth"
        assert ns.auth_subcommand == "login"

    def test_redact_logs_flag_parses(self):
        ns = build_parser().parse_args(["run", "https://github.com/acme-org/widgets-service/pull/1",
                                        "--redact-logs"])
        assert ns.redact_logs is True

    def test_redact_logs_default_off(self):
        ns = build_parser().parse_args(["run", "https://github.com/acme-org/widgets-service/pull/1"])
        assert ns.redact_logs is False


class TestRunWiring:
    def test_run_invokes_runner_with_resolved_inputs(self, tmp_path: Path, monkeypatch, capsys):
        # Stub everything heavy: retention.sweep, browser launch, runner execution.
        calls = {}

        async def fake_execute(self, prs):
            calls["prs"] = list(prs)
            return 0

        def fake_sweep(root, max_age_days, skip):
            calls["sweep"] = (root, max_age_days, skip)
            return []

        # Patch the runner factory so the CLI uses a fake.
        from github_approve_merge import cli, retention, runner

        class FakeContext:
            async def __aenter__(self): return self
            async def __aexit__(self, *a): return False
            async def new_page(self): raise AssertionError("should not run")

        from contextlib import asynccontextmanager

        @asynccontextmanager
        async def fake_open_context(**kwargs):
            yield FakeContext()

        monkeypatch.setattr(runner.Runner, "execute", fake_execute)
        monkeypatch.setattr(retention, "sweep", fake_sweep)
        monkeypatch.setattr(cli, "open_context", fake_open_context)

        ss = tmp_path / "ss.json"
        ss.write_text('{"cookies":[],"origins":[]}')

        rc = main([
            "run",
            "https://github.com/o/r/pull/1",
            "--storage-state", str(ss),
            "--logs-dir", str(tmp_path / "logs"),
        ])
        assert rc == 0
        assert [str(p) for p in calls["prs"]] == ["o/r#1"]
        assert calls["sweep"][1] == 10  # default retention days
