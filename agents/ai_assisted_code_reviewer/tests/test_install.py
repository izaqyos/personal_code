import json
import re

import pytest

from aireview.install import END, GROUPS, START, install, upsert_block

from .conftest import PAYLOAD


def rels(actions, target):
    return {str(p.relative_to(target)): a for a, p in actions}


def test_full_install_layout(tmp_path):
    acts = rels(install(tmp_path), tmp_path)
    for path in [
        ".ai-review/REVIEW.md",
        ".ai-review/config.json",
        ".ai-review/pr-rules.json",
        ".ai-review/findings.schema.json",
        ".ai-review/.gitignore",
        ".ai-review/wiki/index.md",
        ".claude/commands/ai-review.md",
        "CLAUDE.md",
        ".cursor/rules/ai-review.mdc",
        ".cursor/commands/ai-review.md",
        "AGENTS.md",
        ".github/copilot-instructions.md",
        ".github/prompts/ai-review.prompt.md",
        ".github/workflows/ai-review.yml",
        ".github/pull_request_template.md",
    ]:
        assert acts.get(path) == "create", path
        assert (tmp_path / path).is_file()
    assert (tmp_path / ".ai-review/.gitignore").read_text().strip() == "out/"


def test_only_group_includes_core(tmp_path):
    acts = rels(install(tmp_path, ["claude"]), tmp_path)
    assert ".ai-review/REVIEW.md" in acts and ".claude/commands/ai-review.md" in acts
    assert "AGENTS.md" not in acts and ".cursor/rules/ai-review.mdc" not in acts


def test_unknown_group(tmp_path):
    with pytest.raises(ValueError, match="unknown group"):
        install(tmp_path, ["vim"])


def test_idempotent_and_preserves_user_edits(tmp_path):
    install(tmp_path)
    cfg = tmp_path / ".ai-review/config.json"
    cfg.write_text('{"gate": "blocker"}')
    acts = rels(install(tmp_path), tmp_path)
    assert acts[".ai-review/config.json"] == "skip (exists)"
    assert acts["CLAUDE.md"] == "unchanged"
    assert json.loads(cfg.read_text()) == {"gate": "blocker"}
    acts = rels(install(tmp_path, force=True), tmp_path)
    assert acts[".ai-review/config.json"] == "overwrite"


def test_block_appended_to_existing_file(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("# My project\n\nUse pnpm.\n")
    install(tmp_path, ["claude"])
    text = (tmp_path / "CLAUDE.md").read_text()
    assert text.startswith("# My project\n\nUse pnpm.\n\n" + START)
    assert text.count(START) == 1


def test_upsert_block_replaces_in_place():
    first = upsert_block("top\n", "v1")
    second = upsert_block(first + "\nbottom\n", "v2")
    assert "v1" not in second and "v2" in second
    assert second.startswith("top\n") and second.rstrip().endswith("bottom")
    assert second.count(START) == 1 and second.count(END) == 1
    assert upsert_block("", "x") == f"{START}\nx\n{END}\n"


def test_every_payload_file_is_installed_by_some_group():
    mapped = set()
    for entries in GROUPS.values():
        for src, _, mode in entries:
            p = PAYLOAD / src
            mapped |= {f for f in p.rglob("*") if f.is_file()} if mode == "tree" else {p}
    payload = {f for f in PAYLOAD.rglob("*") if f.is_file()}
    assert payload == mapped


def test_adapters_point_to_single_source_of_truth():
    """Every harness adapter defers to .ai-review/REVIEW.md instead of duplicating it."""
    for rel in [
        "claude/commands/ai-review.md",
        "claude/CLAUDE.block.md",
        "agents/AGENTS.block.md",
        "cursor/rules/ai-review.mdc",
        "cursor/commands/ai-review.md",
        "github/copilot-instructions.block.md",
        "github/prompts/ai-review.prompt.md",
    ]:
        text = (PAYLOAD / rel).read_text()
        assert "REVIEW.md" in text, rel
        assert len(text.splitlines()) < 30, f"{rel} should stay a thin pointer"


def test_frontmatter_present_where_harness_requires_it():
    for rel in [
        "claude/commands/ai-review.md",
        "cursor/rules/ai-review.mdc",
        "github/prompts/ai-review.prompt.md",
    ]:
        assert re.match(r"^---\n.*?\n---\n", (PAYLOAD / rel).read_text(), re.DOTALL), rel


def test_workflow_hardening():
    wf = (PAYLOAD / "github/workflows/ai-review.yml").read_text()
    assert "pull_request:" in wf and "pull_request_target" not in wf
    assert "head.repo.full_name == github.repository" in wf  # no secrets on forks
    assert "contents: read" in wf
    assert "${{ github.event.pull_request.body }}" not in wf  # no script injection via PR text
    assert "--runner claude" in wf
