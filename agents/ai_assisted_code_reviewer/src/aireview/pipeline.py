"""Glue: diff -> checks -> routing -> bundle -> (LLM) -> validation -> report."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from . import checks
from .bundle import Context, render_bundle, reviewable_files
from .config import AI_DIR
from .diff import collect_diff, parse_diff
from .findings import validate
from .report import GateResult, gate, render_json, render_markdown
from .wiki import Wiki, load_wiki


@dataclass
class Paths:
    repo: Path

    @property
    def ai(self) -> Path:
        return self.repo / AI_DIR

    @property
    def wiki(self) -> Path:
        return self.ai / "wiki"

    @property
    def out(self) -> Path:
        return self.ai / "out"


def load_pr_body(repo: Path, explicit: str | None) -> str | None:
    if explicit:
        return Path(explicit).read_text()
    event = os.environ.get("GITHUB_EVENT_PATH")
    if event and Path(event).exists():
        pr = json.loads(Path(event).read_text()).get("pull_request") or {}
        if pr:
            return f"# {pr.get('title', '')}\n\n{pr.get('body') or ''}"
    default = Paths(repo).out / "pr_body.md"
    return default.read_text() if default.exists() else None


def _read_json(path: Path, default):
    return json.loads(path.read_text()) if path.exists() else default


def build_context(
    repo: Path,
    cfg: dict,
    *,
    base: str | None = None,
    pr_body: str | None = None,
    include_uncommitted: bool = False,
    diff_text: str | None = None,
) -> tuple[Context, Wiki]:
    p = Paths(repo)
    if diff_text is None:
        diff_text = collect_diff(repo, base or cfg["base"], include_uncommitted)
    files = parse_diff(diff_text)
    reviewable = reviewable_files(files, cfg["ignore_globs"])
    wiki = load_wiki(p.wiki)
    pr_rules = _read_json(p.ai / "pr-rules.json", {})
    tool_findings, hints = checks.run_all(files, pr_body, pr_rules, cfg)
    routed = wiki.route([f.path for f in reviewable])
    ctx = Context(
        files=files,
        reviewable=reviewable,
        routed=routed,
        tool_findings=tool_findings,
        hints=hints,
        pr_body=pr_body,
    )
    return ctx, wiki


def bundle_text(repo: Path, ctx: Context, wiki: Wiki, cfg: dict) -> str:
    p = Paths(repo)
    review_md = (p.ai / "REVIEW.md").read_text() if (p.ai / "REVIEW.md").exists() else ""
    schema = (
        (p.ai / "findings.schema.json").read_text()
        if (p.ai / "findings.schema.json").exists()
        else "{}"
    )
    return render_bundle(ctx, wiki, review_md, schema, cfg["max_diff_chars"])


@dataclass
class Result:
    gate: GateResult
    markdown: str
    data: dict


def finalize(
    repo: Path,
    ctx: Context,
    wiki: Wiki,
    raw: list,
    cfg: dict,
    *,
    labels: list[str] | None = None,
    notes: list[str] | None = None,
) -> Result:
    def reader(path: str) -> str | None:
        fp = repo / path
        try:
            return fp.read_text() if fp.is_file() else None
        except (OSError, UnicodeDecodeError):
            return None

    kept, dropped = validate(
        raw,
        ctx.files,
        wiki.rules,
        min_confidence=cfg["min_confidence"],
        max_findings=cfg["max_findings"],
        file_reader=reader,
        extra=ctx.tool_findings,
    )
    g = gate(kept, cfg["gate"], cfg["override_label"], labels or [])
    notes = list(notes or [])
    if ctx.pr_body is None:
        notes.append("No PR description provided — PR template checks skipped.")
    if ctx.truncated:
        notes.append(f"Diff truncated for: {', '.join(ctx.truncated)}")
    pages = list(ctx.routed)
    md = render_markdown(
        kept,
        dropped,
        g,
        mode=cfg["gate"],
        override_label=cfg["override_label"],
        routed_pages=pages,
        files_reviewed=len(ctx.reviewable),
        notes=notes,
    )
    return Result(g, md, render_json(kept, dropped, g, pages))


def write_outputs(repo: Path, result: Result, out_dir: Path | None = None) -> Path:
    out = out_dir or Paths(repo).out
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.md").write_text(result.markdown)
    (out / "report.json").write_text(json.dumps(result.data, indent=2))
    return out
