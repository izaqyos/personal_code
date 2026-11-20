from pathlib import Path

from aireview.wiki import lint, load_wiki, parse_index, parse_rules

from .conftest import PAYLOAD

SHIPPED = PAYLOAD / "ai-review" / "wiki"

PAGE = """# Page

### SEC-010: Do the thing
**Severity:** blocker
**Why:** Because.

**Bad:**
```md
## Not a heading inside a fence
### SEC-999: not a rule either
```

**Good:**
```ts
ok();
```

### SEC-011 — Second rule
**Severity:** Major
**Why:** Reasons.

## Unrelated section
**Severity:** nit
"""


def test_parse_rules_ignores_fenced_headings():
    rules = {r.id: r for r in parse_rules(PAGE, "p.md")}
    assert set(rules) == {"SEC-010", "SEC-011"}
    r = rules["SEC-010"]
    assert (r.severity, r.why, r.has_bad, r.has_good) == (
        "blocker",
        "Because.",
        True,
        True,
    )
    assert rules["SEC-011"].title == "Second rule"
    # Normalized, and not overwritten by the later section.
    assert rules["SEC-011"].severity == "major"


def test_parse_index_table():
    routes = parse_index(
        "| Paths | Pages | Notes |\n|---|---|---|\n"
        "| `*` | `a.md` | always |\n"
        "| `src/**`, `lib/**` | `b.md`, `c.md` | |\n"
        "| | | empty row ignored |\n"
    )
    assert [(r.globs, r.pages, r.always) for r in routes] == [
        (["*"], ["a.md"], True),
        (["src/**", "lib/**"], ["b.md", "c.md"], False),
    ]


def test_route_orders_and_explains(tmp_path: Path):
    (tmp_path / "index.md").write_text(
        "| Paths | Pages |\n|---|---|\n"
        "| `*` | `always.md` |\n"
        "| `src/**` | `src.md` |\n"
        "| `**/*.sql` | `sql.md`, `src.md` |\n"
    )
    wiki = load_wiki(tmp_path)
    routed = wiki.route(["src/a.ts", "db/x.sql", "README.md"])
    assert list(routed) == ["always.md", "src.md", "sql.md"]
    assert routed["src.md"] == ["src/a.ts", "db/x.sql"]
    assert routed["always.md"] == ["always"]


def test_lint_detects_problems(tmp_path: Path):
    (tmp_path / "index.md").write_text(
        "| Paths | Pages |\n|---|---|\n| `*` | `a.md`, `missing.md` |\n"
    )
    (tmp_path / "a.md").write_text("### AB-001: x\n**Severity:** huge\n")
    (tmp_path / "b.md").write_text("### AB-001: dup\n**Severity:** nit\n**Why:** y\n")
    errors, warnings = lint(load_wiki(tmp_path))
    joined = "\n".join(errors)
    assert "duplicate id" in joined
    assert "severity 'huge'" in joined
    assert "missing **Why:**" in joined
    assert "missing page missing.md" in joined
    assert any("b.md: not reachable" in w for w in warnings)
    assert any("Bad:** and **Good:**" in w for w in warnings)


def test_lint_requires_index(tmp_path: Path):
    errors, _ = lint(load_wiki(tmp_path))
    assert errors == ["index.md missing"]


def test_shipped_wiki_is_clean():
    wiki = load_wiki(SHIPPED)
    errors, warnings = lint(wiki)
    assert errors == [] and warnings == []
    assert len(wiki.rules) >= 25
    # Every rule referenced by deterministic checks exists in the shipped wiki.
    for rid in (
        "SEC-003",
        "TEST-001",
        "PR-001",
        "PR-002",
        "PR-003",
        "PR-004",
        "PR-005",
    ):
        assert rid in wiki.rules


def test_shipped_routing_for_typical_paths():
    wiki = load_wiki(SHIPPED)
    pages = wiki.route(["src/routes/invoices.ts", "migrations/002.sql"])
    assert "security/authz.md" in pages
    assert "data/migrations.md" in pages
    assert "conventions/typescript.md" in pages
    assert "security/secrets-and-pii.md" in pages  # always
