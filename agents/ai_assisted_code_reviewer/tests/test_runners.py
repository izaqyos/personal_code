import json
import subprocess
from pathlib import Path

import pytest

from aireview.config import DEFAULTS
from aireview.runners import RunnerError, extract_findings, get_runner
from aireview.runners.claude import ClaudeRunner, parse_output
from aireview.runners.mock import MockRunner

ONE = {"rule": "SEC-001", "title": "t"}


class TestExtract:
    def test_fenced_json_with_prose(self):
        text = "Here you go:\n```json\n" + json.dumps({"findings": [ONE]}) + "\n```\nThanks"
        assert extract_findings(text) == [ONE]

    def test_last_parseable_fence_wins(self):
        text = (
            '```json\n{"findings": []}\n```\nrevised:\n```json\n'
            + json.dumps({"findings": [ONE]})
            + "\n```"
        )
        assert extract_findings(text) == [ONE]

    def test_unparseable_last_fence_falls_back(self):
        text = "```json\n" + json.dumps({"findings": [ONE]}) + "\n```\n```json\n{oops\n```"
        assert extract_findings(text) == [ONE]

    def test_bare_object_and_array(self):
        assert extract_findings(json.dumps({"findings": [ONE]})) == [ONE]
        assert extract_findings(json.dumps([ONE])) == [ONE]

    def test_object_embedded_in_prose(self):
        assert extract_findings('Result: {"findings": []} done') == []

    def test_no_json(self):
        with pytest.raises(RunnerError):
            extract_findings("I could not review this.")

    def test_object_without_findings_key(self):
        with pytest.raises(RunnerError):
            extract_findings('{"result": 1}')


class TestClaude:
    def runner(self, **over):
        cfg = {**DEFAULTS["claude"], **over}
        return ClaudeRunner(cfg)

    def test_command_is_read_only(self):
        cmd = self.runner(model="claude-sonnet-5-5").command()
        assert cmd[:2] == ["claude", "-p"]
        assert cmd[cmd.index("--allowedTools") + 1] == "Read,Grep,Glob"
        disallowed = cmd[cmd.index("--disallowedTools") + 1].split(",")
        assert {"Bash", "Edit", "Write", "WebFetch"} <= set(disallowed)
        assert cmd[cmd.index("--model") + 1] == "claude-sonnet-5-5"
        assert cmd[cmd.index("--output-format") + 1] == "json"

    def test_no_model_flag_by_default(self):
        assert "--model" not in self.runner().command()

    def test_parse_envelope(self):
        env = {
            "type": "result",
            "is_error": False,
            "result": "```json\n" + json.dumps({"findings": [ONE]}) + "\n```",
        }
        assert parse_output(json.dumps(env)) == [ONE]

    def test_parse_error_envelope(self):
        with pytest.raises(RunnerError, match="error"):
            parse_output(json.dumps({"is_error": True, "result": "max turns"}))

    def test_parse_plain_text(self):
        assert parse_output("```json\n" + json.dumps({"findings": []}) + "\n```") == []

    def test_missing_binary(self, tmp_path):
        with pytest.raises(RunnerError, match="not found"):
            self.runner(bin="definitely-not-claude-xyz").review("b", tmp_path)

    def test_subprocess_success_and_failure(self, tmp_path, monkeypatch):
        calls = {}

        def fake_run(cmd, input, cwd, **kwargs):
            calls.update(cmd=cmd, input=input, cwd=cwd)
            return subprocess.CompletedProcess(
                cmd, 0, json.dumps({"result": json.dumps({"findings": [ONE]})}), ""
            )

        monkeypatch.setattr("aireview.runners.claude.shutil.which", lambda b: "/usr/bin/claude")
        monkeypatch.setattr("aireview.runners.claude.subprocess.run", fake_run)
        assert self.runner().review("BUNDLE", tmp_path) == [ONE]
        assert calls["input"] == "BUNDLE" and calls["cwd"] == tmp_path

        monkeypatch.setattr(
            "aireview.runners.claude.subprocess.run",
            lambda *a, **k: subprocess.CompletedProcess(a[0], 1, "", "auth failed"),
        )
        with pytest.raises(RunnerError, match="auth failed"):
            self.runner().review("B", tmp_path)

    def test_timeout(self, tmp_path, monkeypatch):
        def boom(*a, **k):
            raise subprocess.TimeoutExpired("claude", 1)

        monkeypatch.setattr("aireview.runners.claude.shutil.which", lambda b: "/usr/bin/claude")
        monkeypatch.setattr("aireview.runners.claude.subprocess.run", boom)
        with pytest.raises(RunnerError, match="timed out"):
            self.runner().review("B", tmp_path)


def test_mock_runner(tmp_path: Path):
    p = tmp_path / "r.md"
    p.write_text("```json\n" + json.dumps({"findings": [ONE]}) + "\n```")
    r = MockRunner(str(p))
    assert r.review("BUNDLE", tmp_path) == [ONE]
    assert r.last_bundle == "BUNDLE"


def test_get_runner():
    assert isinstance(get_runner("claude", DEFAULTS), ClaudeRunner)
    with pytest.raises(RunnerError):
        get_runner("mock", DEFAULTS)
    with pytest.raises(RunnerError):
        get_runner("gpt", DEFAULTS)
