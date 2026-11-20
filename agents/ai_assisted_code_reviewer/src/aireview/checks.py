"""Deterministic checks. Cheap, repeatable, and run before any LLM is involved.

Each check emits Findings with source="tool" that cite wiki rule IDs, so a team
disables a check simply by deleting its rule from the wiki.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import PurePosixPath

from .diff import FileDiff
from .findings import Finding
from .globs import match_any

# ---------------------------------------------------------------- PR template

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[( |x|X)\]\s+(.*)$")
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", s.lower()).strip()


def parse_sections(body: str) -> dict[str, str]:
    """Map normalized heading -> section text (until next heading of same or higher level)."""
    body = COMMENT_RE.sub("", body)
    lines = body.splitlines()
    heads = [
        (i, len(m.group(1)), m.group(2))
        for i, line in enumerate(lines)
        if (m := HEADING_RE.match(line))
    ]
    out: dict[str, str] = {}
    for idx, (i, level, title) in enumerate(heads):
        end = len(lines)
        for j, lvl, _ in heads[idx + 1 :]:
            if lvl <= level:
                end = j
                break
        out[_norm(title)] = "\n".join(lines[i + 1 : end]).strip()
    return out


def _meaningful(text: str, placeholders: list[str]) -> str:
    """Section text with checkbox lines, sub-headings and placeholder lines removed."""
    keep = []
    ph = {_norm(p) for p in placeholders}
    for line in text.splitlines():
        if CHECKBOX_RE.match(line) or HEADING_RE.match(line):
            continue
        if _norm(line) in ph:
            continue
        keep.append(line)
    return "\n".join(keep).strip()


def check_pr_body(body: str | None, rules: dict, changed_paths: list[str]) -> list[Finding]:
    """One finding per rule (problems for the same rule are grouped into a single finding)."""
    if body is None:
        return []
    sections = parse_sections(body)
    placeholders = rules.get("placeholders", [])
    problems: dict[str, list[str]] = {}  # rule -> problem descriptions
    custom: dict[str, str] = {}  # rule -> custom title

    def find_section(heading: str) -> str | None:
        want = _norm(heading)
        for k, v in sections.items():
            if k == want or k.startswith(want):
                return v
        return None

    def section_check(heading: str, min_chars: int, rule: str, message: str | None = None) -> None:
        text = find_section(heading)
        if text is None:
            problems.setdefault(rule, []).append(f"'{heading}' missing")
        elif len(_meaningful(text, placeholders)) < min_chars:
            first = text.strip().splitlines()[0][:60] if text.strip() else ""
            problems.setdefault(rule, []).append(
                f"'{heading}' empty/placeholder" + (f' ("{first}")' if first else "")
            )
        else:
            return
        if message:
            custom[rule] = message

    for s in rules.get("sections", []):
        section_check(s["heading"], s.get("min_chars", 1), s.get("rule", "PR-001"))

    for cond in rules.get("conditional", []):
        if any(match_any(p, cond["paths"]) for p in changed_paths):
            section_check(
                cond["section"],
                cond.get("min_chars", 1),
                cond.get("rule", "PR-003"),
                cond.get("message"),
            )

    boxes = {}
    for line in COMMENT_RE.sub("", body).splitlines():
        m = CHECKBOX_RE.match(line)
        if m:
            boxes[_norm(m.group(2))] = m.group(1).lower() == "x"
    unticked: dict[str, list[str]] = {}
    for cb in rules.get("checkboxes", []):
        want = _norm(cb["text"])
        state = next((v for k, v in boxes.items() if k.startswith(want)), None)
        if state is not True:
            unticked.setdefault(cb.get("rule", "PR-002"), []).append(cb["text"])

    findings: list[Finding] = []
    for rule, items in problems.items():
        findings.append(
            Finding(
                rule=rule,
                severity="",
                source="tool",
                title=custom.get(rule) or "PR description sections missing or placeholder",
                evidence="\n".join(items),
                fix="Fill these sections with real content (placeholders like TODO don't count).",
            )
        )
    for rule, items in unticked.items():
        findings.append(
            Finding(
                rule=rule,
                severity="",
                source="tool",
                title="Checklist items not ticked: " + "; ".join(f"'{t}'" for t in items),
                fix="Tick them if true; otherwise explain in the PR why they don't apply.",
            )
        )

    ticket = rules.get("ticket")
    if ticket and not re.search(ticket["pattern"], body):
        findings.append(
            Finding(
                rule=ticket.get("rule", "PR-004"),
                severity="",
                source="tool",
                title="PR description does not reference a ticket",
                fix="Add the tracking ticket, e.g. 'Ticket: PAY-123'.",
            )
        )
    return findings


# ---------------------------------------------------------------- secrets

SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("AWS access key", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    (
        "Private key",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    ),
    ("GitHub token", re.compile(r"\b(ghp|gho|ghs|ghu|github_pat)_[A-Za-z0-9_]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("Stripe live key", re.compile(r"\b[sr]k_live_[A-Za-z0-9]{16,}\b")),
    ("Anthropic/OpenAI key", re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}\b")),
    (
        "Hardcoded credential",
        re.compile(
            r"""(?i)\b[\w]*(api[_-]?key|secret|passw(?:or)?d|token|auth)[\w]*\b\s*[:=]\s*["']([^"'\s]{12,})["']"""
        ),
    ),
]
PLACEHOLDER_HINTS = (
    "process.env",
    "${",
    "changeme",
    "example",
    "xxxx",
    "dummy",
    "placeholder",
    "<",
    "your_",
)


def _mask(s: str) -> str:
    return s[:4] + "…" + "*" * 6 if len(s) > 6 else "****"


def check_secrets(files: list[FileDiff], ignore_globs: list[str]) -> list[Finding]:
    out: list[Finding] = []
    for fd in files:
        if fd.binary or fd.status == "deleted" or match_any(fd.path, ignore_globs):
            continue
        for ln, text in fd.added_lines.items():
            for label, pat in SECRET_PATTERNS:
                m = pat.search(text)
                if not m:
                    continue
                secret = (
                    m.group(m.lastindex or 0) if label == "Hardcoded credential" else m.group(0)
                )
                if any(h in secret.lower() for h in PLACEHOLDER_HINTS):
                    continue
                out.append(
                    Finding(
                        rule="SEC-003",
                        severity="",
                        source="tool",
                        file=fd.path,
                        line=ln,
                        title=f"{label} committed in source",
                        evidence=text.replace(secret, _mask(secret)).strip()[:160],
                        fix="Remove it, rotate the credential, load it from the secret manager.",
                    )
                )
                break
    return out


# ---------------------------------------------------------------- tests touched


@dataclass
class TouchHints:
    source_changed: list[str] = field(default_factory=list)
    tests_changed: list[str] = field(default_factory=list)
    untested: list[str] = field(default_factory=list)  # source files with no same-stem test changed


def _stem(path: str) -> str:
    name = PurePosixPath(path).name
    name = re.sub(r"\.(test|spec)(?=\.)", "", name)
    return name.split(".")[0]


def touch_hints(files: list[FileDiff], cfg: dict) -> TouchHints:
    h = TouchHints()
    for fd in files:
        if fd.status == "deleted" or fd.binary or match_any(fd.path, cfg["ignore_globs"]):
            continue
        if match_any(fd.path, cfg["test_globs"]):
            h.tests_changed.append(fd.path)
        elif match_any(fd.path, cfg["source_globs"]) and fd.added_count:
            h.source_changed.append(fd.path)
    test_stems = {_stem(t) for t in h.tests_changed}
    h.untested = [s for s in h.source_changed if _stem(s) not in test_stems]
    return h


def check_tests_touched(h: TouchHints) -> list[Finding]:
    if h.source_changed and not h.tests_changed:
        listed = ", ".join(h.source_changed[:6]) + (" …" if len(h.source_changed) > 6 else "")
        return [
            Finding(
                rule="TEST-001",
                severity="",
                source="tool",
                title=f"Source changed but no test files changed ({listed})",
                fix="Add or update tests that exercise the new behavior.",
            )
        ]
    return []


# ---------------------------------------------------------------- size


def check_size(files: list[FileDiff], cfg: dict) -> list[Finding]:
    total = sum(
        fd.added_count + fd.removed_count
        for fd in files
        if not match_any(fd.path, cfg["ignore_globs"])
    )
    if total > cfg["max_pr_lines"]:
        return [
            Finding(
                rule="PR-005",
                severity="",
                source="tool",
                title=f"PR changes {total} lines (limit {cfg['max_pr_lines']})",
                fix="Split into smaller, independently reviewable PRs.",
            )
        ]
    return []


def run_all(
    files: list[FileDiff], pr_body: str | None, pr_rules: dict, cfg: dict
) -> tuple[list[Finding], TouchHints]:
    hints = touch_hints(files, cfg)
    changed = [f.path for f in files]
    found = [
        *check_secrets(files, cfg["ignore_globs"]),
        *check_tests_touched(hints),
        *check_pr_body(pr_body, pr_rules, changed),
        *check_size(files, cfg),
    ]
    return found, hints
