"""Gate decision and report rendering (markdown for humans, JSON for machines)."""

from __future__ import annotations

from dataclasses import dataclass, field

from .findings import GENERAL, SEVERITIES, Dropped, Finding

MARKER = "<!-- aireview-report -->"
ICONS = {"blocker": "🛑", "major": "🟠", "minor": "🟡", "nit": "⚪"}


@dataclass
class GateResult:
    status: str  # pass | warn | fail
    exit_code: int
    blocking: list[Finding] = field(default_factory=list)
    overridden: bool = False


def gate(kept: list[Finding], mode: str, override_label: str, labels: list[str]) -> GateResult:
    blocking = [f for f in kept if f.severity == "blocker" and f.rule != GENERAL]
    overridden = override_label in labels
    if blocking and mode == "blocker" and not overridden:
        return GateResult("fail", 1, blocking)
    if blocking:
        return GateResult("warn", 0, blocking, overridden)
    return GateResult("pass", 0)


def counts(kept: list[Finding]) -> dict[str, int]:
    return {s: sum(1 for f in kept if f.severity == s) for s in SEVERITIES}


def _fmt_finding(i: int, f: Finding) -> list[str]:
    loc = f" — `{f.file}:{f.line}`" if f.file and f.line else (f" — `{f.file}`" if f.file else "")
    meta = "tool" if f.source == "tool" else f"llm, conf {f.confidence:.2f}"
    lines = [f"{i}. **[{f.rule}] {f.title}**{loc} _({meta})_"]
    if f.evidence:
        lines += [
            "   ```",
            *("   " + line for line in f.evidence.strip().splitlines()[:6]),
            "   ```",
        ]
    if f.why:
        lines.append(f"   - **Why:** {f.why}")
    if f.fix:
        lines.append(f"   - **Fix:** {f.fix}")
    for n in f.notes:
        lines.append(f"   - _note: {n}_")
    return lines


def render_markdown(
    kept: list[Finding],
    dropped: list[Dropped],
    g: GateResult,
    *,
    mode: str,
    override_label: str,
    routed_pages: list[str],
    files_reviewed: int,
    notes: list[str] | None = None,
) -> str:
    c = counts(kept)
    head = {
        "fail": "❌ Changes requested",
        "warn": "⚠️ Blockers found (not gating)"
        if not g.overridden
        else "⚠️ Blockers overridden by label",
        "pass": "✅ No blocking issues",
    }[g.status]
    out = [MARKER, f"## 🤖 AI Review — {head}", ""]
    out.append(
        " · ".join(f"{ICONS[s]} {c[s]} {s}" for s in SEVERITIES)
        + f" — {files_reviewed} file(s) reviewed"
    )
    out.append("")
    out.append(
        f"Gate mode: `{mode}`"
        + (f" · override label: `{override_label}`" if mode == "blocker" else "")
    )
    if routed_pages:
        out.append("Wiki pages consulted: " + ", ".join(f"`{p}`" for p in routed_pages))
    for n in notes or []:
        out.append(f"> {n}")
    out.append("")

    if not kept:
        out += ["No findings. 🎉", ""]
    n = 0
    for sev in SEVERITIES:
        group = [f for f in kept if f.severity == sev]
        if not group:
            continue
        out += [f"### {ICONS[sev]} {sev.capitalize()} ({len(group)})", ""]
        for f in group:
            n += 1
            out += _fmt_finding(n, f)
        out.append("")

    if dropped:
        out += [
            f"<details><summary>Dropped by validation ({len(dropped)})</summary>",
            "",
            "| rule | location | reason |",
            "|---|---|---|",
        ]
        for d in dropped:
            f = d.finding
            if isinstance(f, Finding):
                loc = f"{f.file}:{f.line}" if f.file and f.line else (f.file or "—")
                out.append(f"| {f.rule} | {loc} | {d.reason} |")
            else:
                raw = f if isinstance(f, dict) else {}
                loc = ":".join(str(x) for x in (raw.get("file"), raw.get("line")) if x) or "—"
                out.append(f"| {raw.get('rule', '?')} | {loc} | {d.reason} |")
        out += ["", "</details>", ""]

    out += [
        "---",
        (
            "_Disagree? Reply on the finding. "
            "Intentional exception: `// review-ignore RULE-ID: reason`. "
            "Rules live in `.ai-review/wiki/` — fix the rule, not just the PR._"
        ),
    ]
    return "\n".join(out) + "\n"


def render_json(kept, dropped, g: GateResult, routed_pages: list[str]) -> dict:
    return {
        "status": g.status,
        "exit_code": g.exit_code,
        "counts": counts(kept),
        "routed_pages": routed_pages,
        "findings": [f.to_dict() for f in kept],
        "dropped": [
            {
                "reason": d.reason,
                "finding": d.finding.to_dict() if isinstance(d.finding, Finding) else d.finding,
            }
            for d in dropped
        ],
    }
