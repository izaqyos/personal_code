#!/usr/bin/env python3
"""Source audit for the craft LLM wiki.

The catalog (catalog.toml) lists every candidate source with a grade:

  A exemplar   routed in full: imitate its code and style
  B ok         routed partially: only the sections named in `use`
  C weak       not routed (kept in the catalog with the reason)
  D legacy     not routed: outdated, wrong, or a raw dump

Every route must have at least one A source. A topic with none gets a gap-fill page
(written to the playbook standards, stored in the KB, catalogued with kind = "gap"), which is graded A.

This tool:

  scan   [ids...]   automated quality signals per source (snippet parse/lint, legacy markers, tests)
  render            regenerate index.md (the routing table agents read) from the catalog
  check             validate catalog + index: paths exist, grades valid, every route has an A
                    source, nothing private, index fresh

Roots resolve from env (CRAFT_KB, CRAFT_CODE, CRAFT_PRACTICE) or the defaults in the catalog.
"""

from __future__ import annotations

import argparse
import ast
import os
import re
import subprocess
import sys
import tempfile
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
CATALOG = HERE / "catalog.toml"
INDEX = HERE / "index.md"
GRADES = {"A": "exemplar", "B": "ok (partial)", "C": "weak", "D": "legacy"}
ROUTED = {"A", "B"}
PRIVATE_MARKERS = ("personal_KB_private", "/employers/", "career-records")
FENCE_RE = re.compile(r"^(`{3,}|~{3,})\s*([\w+-]*)\s*$")
JS_LEGACY = {
    "var declaration": re.compile(r"^\s*var\s+\w+", re.M),
    "error-first callback": re.compile(r"function\s*\(\s*err\b|\(err,\s*\w+\)\s*=>"),
    "CommonJS require": re.compile(r"\brequire\(['\"]"),
}
DOC_LEGACY = {
    "legacy tag": re.compile(r"^tags:.*\blegacy\b", re.M),
    "raw source capture": re.compile(r"^capture_type:\s*source\s*$", re.M),
    "pasted chat answer": re.compile(r"\bchat ?gpt\b", re.I),
}
# Snippets legitimately reference undefined names, so F821/F401 are off; these catch real smells.
RUFF_RULES = "E722,B,F841,UP,SIM,PLW,DTZ,ASYNC"
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
PY_SMELLS = {
    "wall clock for durations": re.compile(r"time\.time\(\)"),
    "bare except": re.compile(r"except\s*:"),
    "print debugging": re.compile(r"^\s*print\(", re.M),
}
NO_COLOR_ENV = {**os.environ, "NO_COLOR": "1", "FORCE_COLOR": "0", "PY_COLORS": "0"}


@dataclass
class Source:
    id: str
    path: str
    kind: str  # doc | code | gap
    grade: str
    routes: list[str]
    note: str = ""
    use: str = ""  # B only: the sections that are worth reading
    test_cmd: str = ""
    lint_paths: list[str] = field(default_factory=list)


def load_catalog(path: Path = CATALOG) -> tuple[dict[str, str], dict[str, str], list[Source], str]:
    data = tomllib.loads(path.read_text())
    roots = {k: os.environ.get(f"CRAFT_{k}", v) for k, v in data["roots"].items()}
    routes = data["routes"]
    sources = [Source(**s) for s in data["source"]]
    return roots, routes, sources, data["audited"]


def resolve(path: str, roots: dict[str, str]) -> Path:
    root, _, rest = path.partition("/")
    if root not in roots:
        raise ValueError(f"unknown root {root!r} in {path!r}")
    base = Path(roots[root]).expanduser()
    if not base.is_absolute():
        base = HERE.parent / base  # relative roots (SUITE) are relative to the suite folder
    return base / rest


# ------------------------------------------------------------------ scan


def code_blocks(text: str) -> list[tuple[str, str]]:
    blocks, lang, buf, fence = [], None, [], None
    for line in text.splitlines():
        m = FENCE_RE.match(line)
        if fence is None and m:
            fence, lang, buf = m.group(1), m.group(2).lower(), []
        elif fence is not None and line.strip().startswith(fence):
            blocks.append((lang or "", "\n".join(buf)))
            fence = None
        elif fence is not None:
            buf.append(line)
    return blocks


def ruff_findings(snippets: list[str]) -> list[str]:
    if not snippets:
        return []
    with tempfile.TemporaryDirectory() as tmp:
        for i, s in enumerate(snippets):
            Path(tmp, f"s{i}.py").write_text(s + "\n")
        proc = subprocess.run(
            [
                "ruff",
                "check",
                "--no-cache",
                "--isolated",
                "--select",
                RUFF_RULES,
                "--output-format",
                "concise",
                tmp,
            ],
            capture_output=True,
            text=True,
            check=False,
            env=NO_COLOR_ENV,
        )
    codes = re.findall(r":\d+:\d+: ([A-Z]+\d+)", ANSI_RE.sub("", proc.stdout))
    return sorted(set(codes))


def scan_doc(p: Path) -> dict:
    text = p.read_text(errors="replace")
    blocks = code_blocks(text)
    py = [b for lang, b in blocks if lang in ("python", "py")]
    js = [b for lang, b in blocks if lang in ("javascript", "js", "typescript", "ts")]
    unparsable = 0
    for s in py:
        try:
            ast.parse(s)
        except SyntaxError:
            unparsable += 1
    signals = [name for name, rx in DOC_LEGACY.items() if rx.search(text)]
    signals += [f"py: {name}" for name, rx in PY_SMELLS.items() if any(rx.search(b) for b in py)]
    signals += [f"js: {name}" for name, rx in JS_LEGACY.items() if any(rx.search(b) for b in js)]
    return {
        "lines": len(text.splitlines()),
        "py_blocks": len(py),
        "py_unparsable": unparsable,
        "ruff": ruff_findings([s for s in py if _parses(s)]),
        "untyped_defs": sum(_untyped_defs(s) for s in py if _parses(s)),
        "js_blocks": len(js),
        "legacy": signals,
        "private": [m for m in PRIVATE_MARKERS if m in text],
    }


def _parses(s: str) -> bool:
    try:
        ast.parse(s)
    except SyntaxError:
        return False
    return True


def _untyped_defs(snippet: str) -> int:
    """Functions with no annotations at all (self/cls aside): a currency/clean-code signal."""
    count = 0
    for node in ast.walk(ast.parse(snippet)):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            args = [a for a in node.args.args if a.arg not in ("self", "cls")]
            if node.returns is None and not any(a.annotation for a in args):
                count += 1
    return count


def scan_code(src: Source, p: Path) -> dict:
    out: dict = {}
    if src.test_cmd:
        proc = subprocess.run(
            src.test_cmd,
            shell=True,
            cwd=p,
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
            env=NO_COLOR_ENV,
        )
        lines = ANSI_RE.sub("", proc.stdout + proc.stderr).splitlines()
        summary = next((ln for ln in reversed(lines) if "passed" in ln or "failed" in ln), "")
        out["tests"] = f"{'PASS' if proc.returncode == 0 else 'FAIL'}: {summary.strip()[:100]}"
    if src.lint_paths:
        proc = subprocess.run(
            ["ruff", "check", "--no-cache", *src.lint_paths],
            cwd=p,
            capture_output=True,
            text=True,
            check=False,
            env=NO_COLOR_ENV,
        )
        last = ANSI_RE.sub("", proc.stdout).strip().splitlines()[-1:] or [""]
        out["ruff"] = "clean" if proc.returncode == 0 else last[0][:100]
    return out


def cmd_scan(ids: list[str]) -> int:
    roots, _, sources, _ = load_catalog()
    for src in sources:
        if ids and src.id not in ids:
            continue
        p = resolve(src.path, roots)
        if not p.exists():
            print(f"{src.id:28} MISSING {p}")
            continue
        result = scan_code(src, p) if src.kind == "code" else scan_doc(p)
        print(f"{src.id:28} [{src.grade}] {result}")
    return 0


# ------------------------------------------------------------------ render / check


def render(roots_spec: dict[str, str], routes: dict[str, str], sources: list[Source], audited: str) -> str:
    out = [
        "# craft wiki: routing index",
        "",
        "<!-- GENERATED by wiki/audit.py render from wiki/catalog.toml; do not edit by hand. -->",
        "",
        f"Sources audited {audited} against the rubric in `audit.md`. Only grades A and B are routed.",
        "",
        "**How to use (agents):** pick the rows for the current phase, NFR lens and language; read at most",
        "3 pages, A first; cite what you used. **A** = exemplar: imitate it. **B** = ok: read only the",
        "listed sections, and write any code to the playbook standards. `gap` pages were written to fill",
        "topics where no source graded A. If a root or page is missing, skip it and say so.",
        "",
        "Roots: " + " · ".join(f"`{k}` = `{v}`" for k, v in roots_spec.items()),
        "",
        "| Route | Use when | Sources |",
        "|---|---|---|",
    ]
    for key, when in routes.items():
        picked = sorted((s for s in sources if key in s.routes and s.grade in ROUTED), key=lambda s: s.grade)
        cells = "<br>".join(_cell(s) for s in picked)
        out.append(f"| `{key}` | {when} | {cells} |")
    return "\n".join(out) + "\n"


def _cell(s: Source) -> str:
    scope = f" (read only: {s.use})" if s.grade == "B" else ""
    return f"**{s.grade}** `{s.path}`: {s.note}{scope}"


def _source_errors(s: Source, roots: dict[str, str], routes: dict[str, str]) -> list[str]:
    errors: list[str] = []
    if s.grade not in GRADES:
        errors.append(f"{s.id}: grade {s.grade!r} not in {sorted(GRADES)}")
    if s.kind not in ("doc", "code", "gap"):
        errors.append(f"{s.id}: kind {s.kind!r} not in ['code', 'doc', 'gap']")
    if s.grade == "B" and not s.use:
        errors.append(f"{s.id}: grade B needs `use` (which sections to read)")
    if s.kind == "gap" and s.grade != "A":
        errors.append(f"{s.id}: gap-fill pages must be written to grade A")
    if any(m in s.path for m in PRIVATE_MARKERS):
        errors.append(f"{s.id}: private path {s.path}")
    errors += [f"{s.id}: unknown route {r!r}" for r in s.routes if r not in routes]
    if s.grade in ROUTED and not s.routes:
        errors.append(f"{s.id}: grade {s.grade} but no routes")
    if not s.note:
        errors.append(f"{s.id}: missing note")
    try:
        if not resolve(s.path, roots).exists():
            errors.append(f"{s.id}: path does not exist: {s.path}")
    except ValueError as e:
        errors.append(f"{s.id}: {e}")
    return errors


def check() -> list[str]:
    raw_roots = tomllib.loads(CATALOG.read_text())["roots"]
    roots, routes, sources, audited = load_catalog()
    ids = [s.id for s in sources]
    errors = [f"{i}: duplicate id" for i in sorted({i for i in ids if ids.count(i) > 1})]
    for s in sources:
        errors += _source_errors(s, roots, routes)
    for key in routes:
        if not any(key in s.routes and s.grade == "A" for s in sources):
            errors.append(f"route {key!r} has no grade-A source: write a gap page in the KB and catalog it (kind = \"gap\")")
    if not INDEX.exists() or INDEX.read_text() != render(raw_roots, routes, sources, audited):
        errors.append("index.md is stale: run `python3 wiki/audit.py render`")
    return errors


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("scan").add_argument("ids", nargs="*")
    sub.add_parser("render")
    sub.add_parser("check")
    args = ap.parse_args(argv)
    if args.cmd == "scan":
        return cmd_scan(args.ids)
    if args.cmd == "render":
        raw_roots = tomllib.loads(CATALOG.read_text())["roots"]
        _, routes, sources, audited = load_catalog()
        INDEX.write_text(render(raw_roots, routes, sources, audited))
        print(f"wrote {INDEX}")
        return 0
    errors = check()
    for e in errors:
        print(f"error: {e}")
    print("catalog OK" if not errors else f"{len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
