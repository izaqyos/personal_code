from aireview.findings import Dropped, Finding
from aireview.report import MARKER, gate, render_json, render_markdown

B = Finding(
    rule="SEC-001",
    severity="blocker",
    title="sqli",
    file="src/a.ts",
    line=5,
    evidence="db.raw(x)",
    why="w",
    fix="fx",
    confidence=0.9,
)
G = Finding(rule="general", severity="blocker", title="weird")  # can't gate even if mis-set
M = Finding(rule="TEST-001", severity="major", title="no tests", source="tool")


def test_gate_matrix():
    assert gate([B], "blocker", "ovr", []).status == "fail"
    assert gate([B], "blocker", "ovr", []).exit_code == 1
    r = gate([B], "blocker", "ovr", ["ovr"])
    assert (r.status, r.exit_code, r.overridden) == ("warn", 0, True)
    assert gate([B], "advisory", "ovr", []).status == "warn"
    assert gate([M], "blocker", "ovr", []).status == "pass"
    assert gate([G], "blocker", "ovr", []).status == "pass"
    assert gate([], "blocker", "ovr", []).exit_code == 0


def md(kept, dropped=(), g=None, mode="blocker"):
    g = g or gate(kept, mode, "ovr", [])
    return render_markdown(
        list(kept),
        list(dropped),
        g,
        mode=mode,
        override_label="ovr",
        routed_pages=["security/injection.md"],
        files_reviewed=2,
        notes=["a note"],
    )


def test_markdown_structure():
    text = md(
        [B, M],
        [
            Dropped(
                Finding(rule="SEC-999", severity="major", title="x", file="f", line=1),
                "unknown rule",
            ),
            Dropped({"rule": "X-001", "file": "a.ts", "line": 3}, "schema: missing 'title'"),
        ],
    )
    assert text.startswith(MARKER)
    assert "❌ Changes requested" in text
    assert "🛑 1 blocker · 🟠 1 major · 🟡 0 minor · ⚪ 0 nit" in text
    assert "**[SEC-001] sqli** — `src/a.ts:5` _(llm, conf 0.90)_" in text
    assert "_(tool)_" in text
    assert "db.raw(x)" in text and "**Fix:** fx" in text
    assert "Dropped by validation (2)" in text
    assert "| X-001 | a.ts:3 | schema: missing 'title' |" in text
    assert "`security/injection.md`" in text and "> a note" in text


def test_markdown_pass_and_empty():
    text = md([])
    assert "✅ No blocking issues" in text and "No findings" in text


def test_markdown_override_headline():
    g = gate([B], "blocker", "ovr", ["ovr"])
    assert "overridden by label" in md([B], g=g)


def test_json():
    g = gate([B], "blocker", "ovr", [])
    data = render_json([B], [Dropped({"rule": "x"}, "schema")], g, ["p.md"])
    assert data["status"] == "fail" and data["counts"]["blocker"] == 1
    assert data["findings"][0]["rule"] == "SEC-001"
    assert data["dropped"][0] == {"reason": "schema", "finding": {"rule": "x"}}
