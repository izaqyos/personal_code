"""Finding model plus the validation layer that turns raw LLM output into trusted findings.

The LLM is treated as an untrusted proposer: every finding must reference a real
wiki rule (or `general`), point at a line the diff actually changed, clear the
confidence bar, and survive suppressions, dedupe and the findings cap.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .diff import FileDiff
from .suppress import is_suppressed

SEVERITIES = ("blocker", "major", "minor", "nit")
SEV_RANK = {s: i for i, s in enumerate(SEVERITIES)}
GENERAL = "general"


@dataclass
class Finding:
    rule: str
    severity: str
    title: str
    file: str | None = None
    line: int | None = None
    evidence: str = ""
    why: str = ""
    fix: str = ""
    confidence: float = 1.0
    source: str = "llm"  # llm | tool
    notes: list[str] = field(default_factory=list)

    def key(self) -> tuple:
        # Line-anchored findings dedupe by location; PR-level ones also by title.
        return (
            self.rule,
            self.file,
            self.line,
            self.title if self.file is None else None,
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Dropped:
    finding: Finding | dict
    reason: str


class SchemaError(ValueError):
    pass


def from_dict(d: dict, source: str = "llm") -> Finding:
    if not isinstance(d, dict):
        raise SchemaError("finding is not an object")
    for req in ("rule", "title"):
        if not isinstance(d.get(req), str) or not d[req].strip():
            raise SchemaError(f"missing '{req}'")
    line = d.get("line")
    if line is not None:
        try:
            line = int(line)
        except (TypeError, ValueError):
            raise SchemaError(f"bad line {line!r}") from None
    conf = d.get("confidence", 1.0)
    try:
        conf = float(conf)
    except (TypeError, ValueError):
        raise SchemaError(f"bad confidence {conf!r}") from None
    if not 0.0 <= conf <= 1.0:
        raise SchemaError(f"confidence {conf} out of [0,1]")
    sev = d.get("severity")
    if sev is not None and sev not in SEVERITIES:
        raise SchemaError(f"bad severity {sev!r}")
    file = d.get("file") or None
    if file is not None:
        file = str(file).removeprefix("./")
    return Finding(
        rule=d["rule"].strip(),
        severity=sev or "",
        title=d["title"].strip(),
        file=file,
        line=line,
        evidence=str(d.get("evidence", "")),
        why=str(d.get("why", "")),
        fix=str(d.get("fix", "")),
        confidence=conf,
        source=source,
    )


def validate(
    raw: list,
    diff_files: list[FileDiff],
    rules: dict,
    *,
    min_confidence: float,
    max_findings: int,
    file_reader=None,
    extra: list[Finding] | None = None,
) -> tuple[list[Finding], list[Dropped]]:
    """Validate LLM findings and merge in tool findings.

    `rules` maps rule id -> wiki Rule (needs `.severity`). `file_reader(path)`
    returns current file text for suppression lookups (None to use diff only).
    """
    by_path = {f.path: f for f in diff_files}
    kept: list[Finding] = []
    dropped: list[Dropped] = []

    candidates: list[Finding] = list(extra or [])
    for item in raw:
        try:
            candidates.append(from_dict(item))
        except SchemaError as e:
            dropped.append(Dropped(item, f"schema: {e}"))

    for f in candidates:
        if f.rule != GENERAL and f.rule not in rules:
            dropped.append(Dropped(f, f"unknown rule '{f.rule}' (not in wiki)"))
            continue
        if not f.severity:
            f.severity = rules[f.rule].severity if f.rule in rules else "minor"
        if f.rule == GENERAL and f.severity == "blocker":
            f.severity = "major"
            f.notes.append(
                "downgraded: 'general' findings cannot block; add a wiki rule to enforce"
            )
        if f.file is not None:
            fd = by_path.get(f.file)
            if fd is None:
                dropped.append(Dropped(f, f"file '{f.file}' not in diff"))
                continue
            if f.line is not None and not fd.touches(f.line):
                dropped.append(Dropped(f, f"line {f.line} not in changed hunks of {f.file}"))
                continue
        elif f.line is not None:
            dropped.append(Dropped(f, "line given without file"))
            continue
        if f.confidence < min_confidence:
            dropped.append(Dropped(f, f"confidence {f.confidence:.2f} < {min_confidence:.2f}"))
            continue
        if f.file and f.line:
            text = file_reader(f.file) if file_reader else None
            sup = is_suppressed(f.rule, f.line, text, by_path[f.file].added_lines)
            if sup:
                dropped.append(Dropped(f, f"suppressed in code: {sup}"))
                continue
        kept.append(f)

    # Dedupe on (rule, file, line); keep the most confident (tool beats llm on ties).
    best: dict[tuple, Finding] = {}
    for f in kept:
        k = f.key()
        cur = best.get(k)
        if cur is None or (f.confidence, f.source == "tool") > (
            cur.confidence,
            cur.source == "tool",
        ):
            if cur is not None:
                dropped.append(Dropped(cur, "duplicate"))
            best[k] = f
        else:
            dropped.append(Dropped(f, "duplicate"))
    kept = sorted(best.values(), key=sort_key)

    if len(kept) > max_findings:
        # Blockers are never capped away; the cap trims the least severe first.
        blockers = [f for f in kept if f.severity == "blocker"]
        rest = [f for f in kept if f.severity != "blocker"]
        room = max(max_findings - len(blockers), 0)
        for f in rest[room:]:
            dropped.append(Dropped(f, f"over cap of {max_findings} findings"))
        kept = sorted(blockers + rest[:room], key=sort_key)
    return kept, dropped


def sort_key(f: Finding) -> tuple:
    return (SEV_RANK.get(f.severity, 9), f.file or "", f.line or 0, f.rule)
