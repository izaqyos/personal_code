"""Install the review kit (instructions, wiki, harness adapters, CI) into a repo.

Adapters are thin pointers to .ai-review/REVIEW.md so there is one source of truth.
Files shared with other tooling (CLAUDE.md, AGENTS.md, copilot-instructions.md)
get an idempotent marked block instead of being overwritten.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

PAYLOAD = Path(__file__).parent / "payload"
START, END = "<!-- ai-review:start -->", "<!-- ai-review:end -->"

# group -> [(payload source, target, mode)]  mode: tree | copy | block
GROUPS: dict[str, list[tuple[str, str, str]]] = {
    "core": [
        ("ai-review", ".ai-review", "tree"),
        ("github/pull_request_template.md", ".github/pull_request_template.md", "copy"),
    ],
    "claude": [
        ("claude/commands/ai-review.md", ".claude/commands/ai-review.md", "copy"),
        ("claude/CLAUDE.block.md", "CLAUDE.md", "block"),
    ],
    "cursor": [
        ("cursor/rules/ai-review.mdc", ".cursor/rules/ai-review.mdc", "copy"),
        ("cursor/commands/ai-review.md", ".cursor/commands/ai-review.md", "copy"),
    ],
    "agents": [("agents/AGENTS.block.md", "AGENTS.md", "block")],
    "copilot": [
        (
            "github/copilot-instructions.block.md",
            ".github/copilot-instructions.md",
            "block",
        ),
        (
            "github/prompts/ai-review.prompt.md",
            ".github/prompts/ai-review.prompt.md",
            "copy",
        ),
    ],
    "ci": [("github/workflows/ai-review.yml", ".github/workflows/ai-review.yml", "copy")],
}
ALL = list(GROUPS)
RENAMES = {"gitignore": ".gitignore"}  # dotfiles are stored undotted in the package


def upsert_block(existing: str, block: str) -> str:
    wrapped = f"{START}\n{block.strip()}\n{END}"
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if pattern.search(existing):
        return pattern.sub(lambda _: wrapped, existing)
    if not existing:
        return wrapped + "\n"
    return existing.rstrip("\n") + "\n\n" + wrapped + "\n"


def _copy(src: Path, dst: Path, force: bool, actions: list) -> None:
    if dst.exists() and not force:
        actions.append(("skip (exists)", dst))
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    existed = dst.exists()
    shutil.copyfile(src, dst)
    actions.append(("overwrite" if existed else "create", dst))


def install(
    target: Path, groups: list[str] | None = None, force: bool = False
) -> list[tuple[str, Path]]:
    groups = groups or ALL
    unknown = set(groups) - set(GROUPS)
    if unknown:
        raise ValueError(
            f"unknown group(s): {', '.join(sorted(unknown))}; choose from {', '.join(ALL)}"
        )
    if "core" not in groups:
        groups = ["core", *groups]
    actions: list[tuple[str, Path]] = []
    for g in groups:
        for src_rel, dst_rel, mode in GROUPS[g]:
            src, dst = PAYLOAD / src_rel, target / dst_rel
            if mode == "tree":
                for f in sorted(p for p in src.rglob("*") if p.is_file()):
                    rel = f.relative_to(src)
                    rel = rel.with_name(RENAMES.get(rel.name, rel.name))
                    _copy(f, dst / rel, force, actions)
            elif mode == "copy":
                _copy(src, dst, force, actions)
            else:
                existing = dst.read_text() if dst.exists() else ""
                updated = upsert_block(existing, src.read_text())
                if updated != existing:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    dst.write_text(updated)
                    actions.append(("update block" if existing else "create", dst))
                else:
                    actions.append(("unchanged", dst))
    return actions
