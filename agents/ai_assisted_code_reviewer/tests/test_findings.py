import pytest

from aireview.diff import FileDiff
from aireview.findings import Finding, SchemaError, from_dict, validate
from aireview.suppress import is_suppressed, parse_suppression
from aireview.wiki import Rule

RULES = {
    "SEC-001": Rule("SEC-001", "sqli", "s.md", severity="blocker", why="w"),
    "CONV-003": Rule("CONV-003", "console", "c.md", severity="minor", why="w"),
    "TEST-001": Rule("TEST-001", "tests", "t.md", severity="major", why="w"),
}
FILES = [
    FileDiff(
        path="src/a.ts",
        added_lines={
            5: "bad()",
            6: "console.log(x) // review-ignore CONV-003: boot log",
        },
        hunks=[(3, 8)],
    ),
    FileDiff(path="src/b.ts", added_lines={1: "x"}, hunks=[(1, 1)]),
]


def run(raw, **kw):
    opts = {"min_confidence": 0.6, "max_findings": 15}
    opts.update(kw)
    return validate(raw, FILES, RULES, **opts)


def f(**kw):
    base = {
        "rule": "SEC-001",
        "title": "t",
        "file": "src/a.ts",
        "line": 5,
        "confidence": 0.9,
    }
    base.update(kw)
    return base


def reasons(dropped):
    return [d.reason for d in dropped]


class TestFromDict:
    def test_minimal(self):
        x = from_dict({"rule": "SEC-001", "title": "t"})
        assert (x.severity, x.confidence, x.file, x.line) == ("", 1.0, None, None)

    def test_normalizes_dot_slash(self):
        assert from_dict(f(file="./src/a.ts")).file == "src/a.ts"
        assert from_dict(f(file=".github/x.yml")).file == ".github/x.yml"

    def test_line_coerced(self):
        assert from_dict(f(line="5")).line == 5

    @pytest.mark.parametrize(
        "bad",
        [
            {"title": "t"},
            {"rule": "SEC-001"},
            f(line="five"),
            f(confidence=1.5),
            f(confidence="x"),
            f(severity="critical"),
            "not a dict",
        ],
    )
    def test_schema_errors(self, bad):
        with pytest.raises(SchemaError):
            from_dict(bad)


class TestValidate:
    def test_keeps_valid_and_inherits_severity(self):
        kept, dropped = run([f()])
        assert dropped == []
        assert kept[0].severity == "blocker"

    def test_unknown_rule(self):
        kept, dropped = run([f(rule="SEC-999")])
        assert kept == [] and "unknown rule" in reasons(dropped)[0]

    def test_file_not_in_diff(self):
        kept, dropped = run([f(file="src/zzz.ts")])
        assert kept == [] and "not in diff" in reasons(dropped)[0]

    def test_line_outside_hunks(self):
        kept, dropped = run([f(line=40)])
        assert kept == [] and "not in changed hunks" in reasons(dropped)[0]

    def test_context_line_inside_hunk_is_allowed(self):
        kept, _ = run([f(line=3)])
        assert len(kept) == 1

    def test_line_without_file(self):
        kept, dropped = run([f(file=None)])
        assert kept == [] and "without file" in reasons(dropped)[0]

    def test_pr_level_finding_allowed(self):
        kept, _ = run([f(rule="TEST-001", file=None, line=None)])
        assert kept[0].severity == "major"

    def test_low_confidence(self):
        kept, dropped = run([f(confidence=0.3)])
        assert kept == [] and "confidence" in reasons(dropped)[0]

    def test_general_cannot_block(self):
        kept, _ = run([f(rule="general", severity="blocker")])
        assert kept[0].severity == "major" and kept[0].notes

    def test_general_defaults_to_minor(self):
        kept, _ = run([f(rule="general")])
        assert kept[0].severity == "minor"

    def test_suppression_with_reason(self):
        kept, dropped = run([f(rule="CONV-003", line=6)])
        assert kept == [] and "suppressed" in reasons(dropped)[0]

    def test_suppression_is_rule_specific(self):
        kept, _ = run([f(rule="SEC-001", line=6)])
        assert len(kept) == 1

    def test_suppression_reads_current_file_when_available(self):
        text = "l1\nl2\nl3\n// review-ignore SEC-001: vetted by appsec (SEC-4711)\nbad()"
        kept, dropped = run([f(line=5)], file_reader=lambda p: text)
        assert kept == [] and "vetted by appsec" in reasons(dropped)[0]

    def test_dedupe_keeps_most_confident_and_prefers_tool(self):
        tool = Finding(
            rule="SEC-001",
            severity="",
            title="tool",
            file="src/a.ts",
            line=5,
            source="tool",
        )
        kept, dropped = run([f(confidence=0.95), f(confidence=0.7)], extra=[tool])
        assert [k.source for k in kept] == ["tool"]
        assert reasons(dropped) == ["duplicate", "duplicate"]

    def test_pr_level_dedupe_uses_title(self):
        kept, _ = run(
            [
                f(rule="TEST-001", file=None, line=None, title="a"),
                f(rule="TEST-001", file=None, line=None, title="b"),
            ]
        )
        assert len(kept) == 2

    def test_schema_error_dropped_not_raised(self):
        kept, dropped = run([{"rule": "SEC-001"}, f()])
        assert len(kept) == 1 and reasons(dropped)[0].startswith("schema:")

    def test_sorted_by_severity(self):
        kept, _ = run([f(rule="CONV-003", file="src/b.ts", line=1), f()])
        assert [k.severity for k in kept] == ["blocker", "minor"]

    def test_cap_never_drops_blockers(self):
        raw = [f(rule="SEC-001", file="src/a.ts", line=n) for n in (3, 4, 5)]
        raw += [f(rule="CONV-003", file="src/a.ts", line=n) for n in (3, 4)]
        kept, dropped = run(raw, max_findings=2)
        assert [k.severity for k in kept] == ["blocker"] * 3
        assert reasons(dropped).count("over cap of 2 findings") == 2

    def test_cap_trims_least_severe(self):
        raw = [
            f(rule="SEC-001", line=3),
            f(rule="TEST-001", file=None, line=None),
            f(rule="CONV-003", line=4),
        ]
        kept, dropped = run(raw, max_findings=2)
        assert [k.rule for k in kept] == ["SEC-001", "TEST-001"]
        assert dropped[-1].finding.rule == "CONV-003"


class TestSuppress:
    def test_parse(self):
        assert parse_suppression("x // review-ignore SEC-001: reason here") == (
            "SEC-001",
            "reason here",
        )
        assert parse_suppression("/* review-ignore CONV-003 - why */") == (
            "CONV-003",
            "why",
        )
        assert parse_suppression("# review-ignore general: ok fine") == (
            "general",
            "ok fine",
        )
        assert parse_suppression("no marker") is None

    def test_reason_required(self):
        assert is_suppressed("SEC-001", 1, None, {1: "x // review-ignore SEC-001"}) is None
        assert (
            is_suppressed("SEC-001", 1, None, {1: "x // review-ignore SEC-001: ok"}) is None
        )  # too short

    def test_line_above(self):
        assert (
            is_suppressed("SEC-001", 2, "// review-ignore SEC-001: legacy\nbad()", {}) == "legacy"
        )

    def test_out_of_range(self):
        assert is_suppressed("SEC-001", 99, "a\nb", {}) is None
