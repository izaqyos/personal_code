import json

import pytest

from aireview import checks
from aireview.config import DEFAULTS
from aireview.diff import FileDiff, parse_diff

from .conftest import FAKE_AWS, FAKE_GH, FAKE_PEM, FAKE_STRIPE, PAYLOAD, SAMPLE_DIFF

PR_RULES = json.loads((PAYLOAD / "ai-review" / "pr-rules.json").read_text())

SUMMARY = "Adds GET /invoices/:id so the billing page can show a single invoice. Ticket: PAY-512."
GOOD_BODY = f"""# Add invoice endpoint
## Summary
{SUMMARY}

## How was this tested
Unit tests in tests/invoices.test.ts plus manual curl against staging.

## Risk & Rollback
Low: additive endpoint. Rollback by reverting the deploy.

## Checklist
- [x] I added or updated tests
- [X] No secrets or PII in code or logs
- [ ] I ran `/ai-review` locally
"""


def rules_of(findings):
    return sorted(f.rule for f in findings)


class TestPrBody:
    def test_good_body_passes(self):
        assert checks.check_pr_body(GOOD_BODY, PR_RULES, ["src/routes/invoices.ts"]) == []

    def test_none_body_skips(self):
        assert checks.check_pr_body(None, PR_RULES, []) == []

    def test_placeholders_grouped_into_one_finding(self):
        body = GOOD_BODY.replace(
            SUMMARY,
            "TODO PAY-1",
        ).replace(
            "Unit tests in tests/invoices.test.ts plus manual curl against staging.",
            "N/A",
        )
        found = checks.check_pr_body(body, PR_RULES, [])
        assert rules_of(found) == ["PR-001"]
        assert "'Summary'" in found[0].evidence and "'How was this tested'" in found[0].evidence

    def test_missing_section(self):
        body = GOOD_BODY.replace("## Risk & Rollback", "## Notes")
        found = checks.check_pr_body(body, PR_RULES, [])
        assert rules_of(found) == ["PR-001"]
        assert "'Risk & Rollback' missing" in found[0].evidence

    def test_html_comments_dont_count_as_content(self):
        body = GOOD_BODY.replace(
            "Unit tests in tests/invoices.test.ts plus manual curl against staging.",
            "<!-- Commands run, test names, manual steps, lots of words here -->",
        )
        assert rules_of(checks.check_pr_body(body, PR_RULES, [])) == ["PR-001"]

    def test_migration_requires_real_rollback(self):
        found = checks.check_pr_body(GOOD_BODY, PR_RULES, ["migrations/002_x.sql"])
        assert rules_of(found) == ["PR-003"]
        assert "migrations" in found[0].title

    def test_unticked_and_missing_checkboxes(self):
        body = GOOD_BODY.replace(
            "- [x] I added or updated tests", "- [ ] I added or updated tests"
        ).replace("- [X] No secrets or PII in code or logs\n", "")
        found = checks.check_pr_body(body, PR_RULES, [])
        assert rules_of(found) == ["PR-002"]
        assert "tests" in found[0].title and "secrets" in found[0].title

    def test_ticket_required(self):
        body = GOOD_BODY.replace("Ticket: PAY-512.", "No ticket, sorry about that friends.")
        assert rules_of(checks.check_pr_body(body, PR_RULES, [])) == ["PR-004"]

    def test_heading_prefix_match(self):
        body = GOOD_BODY.replace("## How was this tested", "## How was this tested?")
        assert checks.check_pr_body(body, PR_RULES, []) == []


class TestSecrets:
    def fd(self, *lines, path="src/x.ts"):
        return FileDiff(
            path=path,
            added_lines=dict(enumerate(lines, start=1)),
            hunks=[(1, len(lines))],
        )

    @pytest.mark.parametrize(
        "line",
        [
            f'const k = "{FAKE_AWS}";',
            FAKE_PEM,
            f'token: "{FAKE_GH}"',
            f'stripe = "{FAKE_STRIPE}"',
            'const apiKey = "' + "Zx9vQ2mL" + '7pR4tY8w";',
            'password: "hunter2hunter2hunter2"',
        ],
    )
    def test_detects(self, line):
        found = checks.check_secrets([self.fd(line)], [])
        assert rules_of(found) == ["SEC-003"]
        assert found[0].line == 1

    @pytest.mark.parametrize(
        "line",
        [
            "const apiKey = process.env.API_KEY;",
            'const apiKey = "changeme-changeme";',
            'password: "<your_password_here>"',
            "const secret = short;",
            "const tokenCount = 12345678901234;",
        ],
    )
    def test_ignores_placeholders(self, line):
        assert checks.check_secrets([self.fd(line)], []) == []

    def test_evidence_is_masked(self):
        found = checks.check_secrets([self.fd(f'k = "{FAKE_STRIPE}"')], [])
        assert "abcdefghijklmnop" not in found[0].evidence

    def test_ignored_and_deleted_files_skipped(self):
        line = f'k = "{FAKE_STRIPE}"'
        ignored = self.fd(line, path="dist/bundle.js")
        deleted = self.fd(line)
        deleted.status = "deleted"
        assert checks.check_secrets([ignored, deleted], ["**/dist/**"]) == []


class TestTestsTouched:
    def test_flags_source_without_tests(self):
        h = checks.touch_hints(parse_diff(SAMPLE_DIFF), DEFAULTS)
        assert set(h.source_changed) == {
            "src/app.ts",
            "src/routes/invoices.ts",
            "src/b.ts",
        }
        assert h.tests_changed == []
        assert rules_of(checks.check_tests_touched(h)) == ["TEST-001"]

    def test_tests_present_and_stem_hints(self):
        files = [
            FileDiff(path="src/routes/invoices.ts", added_lines={1: "x"}),
            FileDiff(path="src/app.ts", added_lines={1: "x"}),
            FileDiff(path="tests/invoices.test.ts", added_lines={1: "x"}),
        ]
        h = checks.touch_hints(files, DEFAULTS)
        assert checks.check_tests_touched(h) == []
        assert h.untested == ["src/app.ts"]

    def test_deletion_only_source_not_counted(self):
        h = checks.touch_hints([FileDiff(path="src/a.ts", removed_count=3)], DEFAULTS)
        assert h.source_changed == []


def test_size_check():
    cfg = {**DEFAULTS, "max_pr_lines": 3}
    big = FileDiff(path="src/a.ts", added_lines={1: "a", 2: "b"}, removed_count=2)
    lock = FileDiff(path="package-lock.json", added_lines=dict.fromkeys(range(1, 100), "x"))
    assert rules_of(checks.check_size([big, lock], cfg)) == ["PR-005"]
    assert checks.check_size([lock], cfg) == []
