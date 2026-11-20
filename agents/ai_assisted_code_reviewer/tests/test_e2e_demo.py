"""End-to-end over the demo repo: the same flow a dev or CI runs, with the mock LLM."""

import json
import subprocess
import sys

import pytest

from aireview.cli import main

from .conftest import DEMO, ROOT

MOCK = str(DEMO / "mock_llm_response.md")


@pytest.fixture
def in_repo(demo_repo, monkeypatch):
    monkeypatch.chdir(demo_repo)
    monkeypatch.delenv("GITHUB_EVENT_PATH", raising=False)
    return demo_repo


def report(repo):
    return json.loads((repo / ".ai-review/out/report.json").read_text())


def test_mock_run_full_pipeline(in_repo, capsys):
    rc = main(["run", "--runner", "mock", "--mock-response", MOCK, "--base", "main"])
    assert rc == 1  # demo config: gate=blocker
    data = report(in_repo)
    assert data["status"] == "fail"

    kept = {(f["rule"], f["file"], f["line"]) for f in data["findings"]}
    for expected in [
        ("SEC-001", "src/routes/invoices.ts", 17),
        ("SEC-002", "src/routes/invoices.ts", 23),
        ("SEC-007", "src/app.ts", 13),
        ("SEC-003", "src/config.ts", 11),
        ("MIG-001", "migrations/002_drop_legacy_email.sql", 2),
        ("PIT-002", "src/services/reminders.ts", 18),
        ("TEST-001", None, None),
        ("PR-003", None, None),
    ]:
        assert expected in kept, expected

    sec3 = next(f for f in data["findings"] if f["rule"] == "SEC-003")
    assert sec3["source"] == "tool"  # tool finding beats the LLM duplicate

    reasons = {d["reason"].split(" ")[0] for d in data["dropped"]}
    joined = " | ".join(d["reason"] for d in data["dropped"])
    assert "suppressed in code: boot banner" in joined
    assert "line 88 not in changed hunks" in joined
    assert "unknown rule 'SEC-999'" in joined
    assert "file 'src/routes/users.ts' not in diff" in joined
    assert "confidence 0.35" in joined
    assert "duplicate" in reasons and "schema:" in reasons

    general = next(f for f in data["findings"] if f["title"].startswith("toDto"))
    assert general["severity"] == "major"  # downgraded from blocker

    md = (in_repo / ".ai-review/out/report.md").read_text()
    assert "❌ Changes requested" in md
    assert "sk_live_51" not in md  # secret masked in the report
    ctx = (in_repo / ".ai-review/out/context.md").read_text()
    assert "=== UNTRUSTED INPUT ===" in ctx and "### wiki/security/authz.md" in ctx


def test_override_label_unblocks(in_repo):
    assert (
        main(
            [
                "run",
                "--runner",
                "mock",
                "--mock-response",
                MOCK,
                "--base",
                "main",
                "--labels",
                "ai-review-override",
                "--quiet",
            ]
        )
        == 0
    )
    assert report(in_repo)["status"] == "warn"


def test_advisory_gate_never_fails(in_repo):
    assert (
        main(
            [
                "run",
                "--runner",
                "mock",
                "--mock-response",
                MOCK,
                "--base",
                "main",
                "--gate",
                "advisory",
                "--quiet",
            ]
        )
        == 0
    )


def test_context_bundle_contents(in_repo, capsys):
    assert main(["context", "--base", "main"]) == 0
    ctx = (in_repo / ".ai-review/out/context.md").read_text()
    head, untrusted = ctx.split("\n=== UNTRUSTED INPUT ===\n", 1)
    assert "# Team AI Code Review — Procedure" in head  # REVIEW.md embedded
    assert "### SEC-002" in head  # routed wiki page content embedded
    assert (
        "[SEC-003] `src/config.ts:11`" in head
    )  # tool findings listed so the LLM won't repeat them
    assert "ignore previous instructions" in untrusted  # injection stays on the untrusted side
    assert "```diff" in untrusted
    out = capsys.readouterr().out
    assert "security/authz.md" in out


def test_validate_flow_for_harness_agents(in_repo):
    """Local flow: the agent writes findings.json, then runs `aireview validate`."""
    out = in_repo / ".ai-review/out"
    (out / "findings.json").write_text(
        json.dumps(
            {
                "findings": [
                    {
                        "rule": "SEC-002",
                        "title": "IDOR",
                        "file": "src/routes/invoices.ts",
                        "line": 23,
                        "confidence": 0.9,
                    },
                ]
            }
        )
    )
    assert main(["validate", "--base", "main", "--quiet"]) == 1
    rules = [f["rule"] for f in report(in_repo)["findings"]]
    assert "SEC-002" in rules and "SEC-003" in rules  # agent finding + tool finding merged


def test_checks_only(in_repo):
    assert main(["checks", "--base", "main", "--quiet"]) == 1  # the secret is a blocker
    data = report(in_repo)
    assert {f["source"] for f in data["findings"]} == {"tool"}


def test_runner_failure_degrades_to_tool_checks(in_repo, tmp_path):
    bad = tmp_path / "bad.md"
    bad.write_text("Sorry, I can't help with that.")
    assert (
        main(
            [
                "run",
                "--runner",
                "mock",
                "--mock-response",
                str(bad),
                "--base",
                "main",
                "--quiet",
                "--gate",
                "advisory",
            ]
        )
        == 0
    )
    md = (in_repo / ".ai-review/out/report.md").read_text()
    assert "LLM review failed" in md
    assert (
        main(
            [
                "run",
                "--runner",
                "mock",
                "--mock-response",
                str(bad),
                "--base",
                "main",
                "--quiet",
                "--strict",
            ]
        )
        == 2
    )


def test_pr_body_from_github_event(in_repo, tmp_path, monkeypatch):
    (in_repo / ".ai-review/out/pr_body.md").unlink()
    event = tmp_path / "event.json"
    event.write_text(
        json.dumps(
            {
                "pull_request": {
                    "title": "Invoices PAY-512",
                    "body": "## Summary\n"
                    "Adds the invoices API and the overdue reminder job for billing.\n"
                    "## How was this tested\nUnit tests and a staging run of the job.\n"
                    "## Risk & Rollback\n"
                    "Revert deploy; migration 002 down restores the column from backup "
                    "s3://backups/legacy_email.\n"
                    "- [x] I added or updated tests\n"
                    "- [x] No secrets or PII in code or logs\n",
                }
            }
        )
    )
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    main(["checks", "--base", "main", "--quiet", "--gate", "advisory"])
    rules = {f["rule"] for f in report(in_repo)["findings"]}
    assert not rules & {"PR-001", "PR-002", "PR-003", "PR-004"}


def test_no_pr_body_notes_skip(in_repo):
    (in_repo / ".ai-review/out/pr_body.md").unlink()
    main(["checks", "--base", "main", "--quiet", "--gate", "advisory"])
    assert "PR template checks skipped" in (in_repo / ".ai-review/out/report.md").read_text()


def test_wiki_lint_and_route_commands(in_repo, capsys):
    assert main(["wiki-lint", "--strict"]) == 0
    assert main(["route", "migrations/003.sql"]) == 0
    assert "data/migrations.md" in capsys.readouterr().out


def test_bad_base_is_a_clean_error(in_repo, capsys):
    assert main(["checks", "--base", "nope"]) == 2
    assert "aireview: error" in capsys.readouterr().err


def test_python_dash_m_entrypoint(in_repo):
    proc = subprocess.run(
        [sys.executable, "-m", "aireview", "wiki-lint"],
        cwd=in_repo,
        capture_output=True,
        text=True,
        check=False,
        env={"PYTHONPATH": str(ROOT / "src"), "PATH": "/usr/bin:/bin"},
    )
    assert proc.returncode == 0, proc.stderr


def test_run_demo_script(tmp_path):
    proc = subprocess.run(
        ["bash", str(DEMO / "run_demo.sh")],
        capture_output=True,
        text=True,
        check=False,
        env={
            "DEMO_DIR": str(tmp_path / "d"),
            "PYTHON": sys.executable,
            "PATH": "/usr/bin:/bin",
        },
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "Gate exit code: 1" in proc.stdout
    assert "exit 0 (overridden)" in proc.stdout


def test_present_script_auto(tmp_path):
    proc = subprocess.run(
        ["bash", str(DEMO / "present.sh"), "--auto"],
        capture_output=True,
        text=True,
        check=False,
        env={
            "DEMO_DIR": str(tmp_path / "p"),
            "PYTHON": sys.executable,
            "PATH": "/usr/bin:/bin",
        },
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "STEP 12" in proc.stdout
    assert "gate exit code: 1" in proc.stdout and "exit code with override label: 0" in proc.stdout
    assert "line 88 not in changed hunks" in proc.stdout
