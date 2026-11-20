"""The LLM wiki: markdown pages of rule-ID'd guidance, plus a routing index.

Page format (one rule per heading):

    ### SEC-002: Check resource ownership
    **Severity:** blocker
    **Why:** ...
    **Bad:** ```ts ... ```
    **Good:** ```ts ... ```

Index format: a markdown table with a "Paths" column of globs and a "Pages"
column of wiki-relative page paths. A Paths cell of `*` means "always read".
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .globs import match

RULE_HEAD_RE = re.compile(r"^(#{2,4})\s+([A-Z]{2,6}-\d{3})\b\s*[:—–-]?\s*(.*)$")
ANY_HEAD_RE = re.compile(r"^(#{1,6})\s")
FIELD_RE = re.compile(r"^\*\*(Severity|Why|Bad|Good|Applies to):?\*\*:?\s*(.*)$", re.IGNORECASE)
SEVERITIES = ("blocker", "major", "minor", "nit")


@dataclass
class Rule:
    id: str
    title: str
    page: str
    severity: str = ""
    why: str = ""
    has_bad: bool = False
    has_good: bool = False


@dataclass
class Route:
    globs: list[str]
    pages: list[str]

    @property
    def always(self) -> bool:
        return any(g.strip() in ("*", "**") for g in self.globs)


@dataclass
class Wiki:
    root: Path
    rules: dict[str, Rule] = field(default_factory=dict)
    routes: list[Route] = field(default_factory=list)
    pages: list[str] = field(default_factory=list)
    duplicates: list[tuple[str, str, str]] = field(default_factory=list)

    def route(self, paths: list[str]) -> dict[str, list[str]]:
        """Return {page: [reasons]} in index order for the changed paths."""
        out: dict[str, list[str]] = {}
        for r in self.routes:
            if r.always:
                for p in r.pages:
                    out.setdefault(p, []).append("always")
                continue
            hits = [path for path in paths if any(match(path, g) for g in r.globs)]
            if hits:
                for p in r.pages:
                    out.setdefault(p, []).extend(h for h in hits if h not in out.get(p, []))
        return out

    def read_page(self, page: str) -> str:
        return (self.root / page).read_text()


def parse_rules(text: str, page: str) -> list[Rule]:
    rules: list[Rule] = []
    cur: Rule | None = None
    cur_level = 0
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue  # example code may contain '#' headings or rule-like text
        m = RULE_HEAD_RE.match(line)
        if m:
            cur = Rule(id=m.group(2), title=m.group(3).strip(), page=page)
            cur_level = len(m.group(1))
            rules.append(cur)
            continue
        h = ANY_HEAD_RE.match(line)
        if h and cur is not None and len(h.group(1)) <= cur_level:
            cur = None
            continue
        if cur is None:
            continue
        fm = FIELD_RE.match(line.strip())
        if fm:
            key, val = fm.group(1).lower(), fm.group(2).strip()
            if key == "severity":
                cur.severity = val.lower().strip("` ")
            elif key == "why":
                cur.why = val
            elif key == "bad":
                cur.has_bad = True
            elif key == "good":
                cur.has_good = True
    return rules


def _split_cells(row: str) -> list[str]:
    row = row.strip()
    row = row.removeprefix("|")
    row = row.removesuffix("|")
    return [c.strip() for c in row.split("|")]


def _items(cell: str) -> list[str]:
    return [
        x.strip().strip("`").strip()
        for x in cell.replace("<br>", ",").split(",")
        if x.strip().strip("`").strip()
    ]


def parse_index(text: str) -> list[Route]:
    routes: list[Route] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        cells = _split_cells(lines[i]) if lines[i].strip().startswith("|") else []
        lower = [c.lower() for c in cells]
        if "paths" in lower and "pages" in lower:
            pi, gi = lower.index("pages"), lower.index("paths")
            i += 2  # skip header separator
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = _split_cells(lines[i])
                if len(row) > max(pi, gi):
                    globs, pages = _items(row[gi]), _items(row[pi])
                    if globs and pages:
                        routes.append(Route(globs=globs, pages=pages))
                i += 1
            continue
        i += 1
    return routes


def load_wiki(root: Path) -> Wiki:
    wiki = Wiki(root=root)
    index = root / "index.md"
    if index.exists():
        wiki.routes = parse_index(index.read_text())
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root).as_posix()
        if rel == "index.md":
            continue
        wiki.pages.append(rel)
        for rule in parse_rules(p.read_text(), rel):
            if rule.id in wiki.rules:
                wiki.duplicates.append((rule.id, wiki.rules[rule.id].page, rel))
            else:
                wiki.rules[rule.id] = rule
    return wiki


def lint(wiki: Wiki) -> tuple[list[str], list[str]]:
    """Return (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []
    if not (wiki.root / "index.md").exists():
        errors.append("index.md missing")
    elif not wiki.routes:
        errors.append("index.md has no routing table (needs 'Paths' and 'Pages' columns)")
    for rid, a, b in wiki.duplicates:
        errors.append(f"{rid}: duplicate id in {a} and {b}")
    for r in wiki.rules.values():
        where = f"{r.page}: {r.id}"
        if r.severity not in SEVERITIES:
            errors.append(f"{where}: severity {r.severity or '(missing)'!r} not in {SEVERITIES}")
        if not r.why:
            errors.append(f"{where}: missing **Why:**")
        if not (r.has_bad and r.has_good):
            warnings.append(f"{where}: add both **Bad:** and **Good:** examples")
    routed = {p for r in wiki.routes for p in r.pages}
    for p in sorted(routed):
        if not (wiki.root / p).exists():
            errors.append(f"index.md routes to missing page {p}")
    for p in wiki.pages:
        if p not in routed:
            warnings.append(f"{p}: not reachable from index.md")
    return errors, warnings
