"""Tests for kb.py."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
import yaml

from bug_triage.kb import KBError, KnowledgeBase, load_eval


def _edit_yaml(d: Path, name: str, key: str, fn: Callable[[list[dict[str, Any]]], None]) -> None:
    path = d / name
    data = yaml.safe_load(path.read_text())
    fn(data[key])
    path.write_text(yaml.safe_dump(data))


def _edit_history(d: Path, fn: Callable[[list[dict[str, Any]]], None]) -> None:
    path = d / "history.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    fn(rows)
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))


def test_load_tiny(tiny_kb: KnowledgeBase) -> None:
    assert set(tiny_kb.teams) == {"Alpha", "Beta"}
    assert len(tiny_kb.components) == 3 and len(tiny_kb.known_issues) == 2
    assert len(tiny_kb.use_cases) == 1 and len(tiny_kb.history) == 8


def test_load_real_data(kb: KnowledgeBase) -> None:
    assert len(kb.teams) == 4 and len(kb.components) == 11


def test_lookups(tiny_kb: KnowledgeBase) -> None:
    assert tiny_kb.owner_team("ui") == "Beta"
    assert tiny_kb.default_assignee("api") == "Ben Hart"
    assert tiny_kb.team_of("Dev Patel") == "Beta"
    assert tiny_kb.is_valid_component("auth") and not tiny_kb.is_valid_component("nope")
    assert tiny_kb.is_valid_assignee("Ada Quill") and not tiny_kb.is_valid_assignee("Zed")
    assert tiny_kb.history_ids() == {f"BUG-{i}" for i in range(1, 9)}


def test_lookup_keyerrors(tiny_kb: KnowledgeBase) -> None:
    with pytest.raises(KeyError):
        tiny_kb.owner_team("nope")
    with pytest.raises(KeyError):
        tiny_kb.default_assignee("nope")
    with pytest.raises(KeyError):
        tiny_kb.team_of("Zed")


def test_roster_text(tiny_kb: KnowledgeBase) -> None:
    text = tiny_kb.roster_text()
    assert "Team Alpha" in text and "Ada Quill" in text
    assert "ui (default assignee Cleo Marsh" in text and "keywords: button" in text


def test_load_eval(tiny_kb_dir: Path) -> None:
    ev = load_eval(tiny_kb_dir)
    assert [b.id for b in ev] == ["EVAL-001", "EVAL-002", "EVAL-003"]
    assert len(load_eval()) == 40


def test_env_override(tiny_kb_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BUG_TRIAGE_DATA_DIR", str(tiny_kb_dir))
    assert len(KnowledgeBase.load().history) == 8
    assert len(load_eval()) == 3
    other = tiny_kb_dir.parent / "elsewhere"
    with pytest.raises(KBError):
        KnowledgeBase.load(other)  # explicit arg wins over env


def test_missing_files(tmp_path: Path, tiny_kb_dir: Path) -> None:
    with pytest.raises(KBError, match="missing"):
        KnowledgeBase.load(tmp_path / "empty")
    (tiny_kb_dir / "history.jsonl").unlink()
    with pytest.raises(KBError, match="missing"):
        KnowledgeBase.load(tiny_kb_dir)
    with pytest.raises(KBError, match="missing"):
        load_eval(tmp_path / "empty")


def test_malformed_files(tiny_kb_dir: Path) -> None:
    (tiny_kb_dir / "teams.yaml").write_text("teams: [unclosed")
    with pytest.raises(KBError, match="invalid YAML"):
        KnowledgeBase.load(tiny_kb_dir)
    (tiny_kb_dir / "teams.yaml").write_text("- just a list\n")
    with pytest.raises(KBError, match="top-level list"):
        KnowledgeBase.load(tiny_kb_dir)
    (tiny_kb_dir / "teams.yaml").write_text("teams: [{name: X}]\n")
    with pytest.raises(KBError, match="invalid Team"):
        KnowledgeBase.load(tiny_kb_dir)


def test_malformed_jsonl(tiny_kb_dir: Path) -> None:
    (tiny_kb_dir / "history.jsonl").write_text("{not json}\n")
    with pytest.raises(KBError, match="history.jsonl:1"):
        KnowledgeBase.load(tiny_kb_dir)
    (tiny_kb_dir / "history.jsonl").write_text('{"id": "x"}\n')
    with pytest.raises(KBError, match="invalid record"):
        KnowledgeBase.load(tiny_kb_dir)
    (tiny_kb_dir / "eval.jsonl").write_text('\n{"id": "x"}\n')
    with pytest.raises(KBError):
        load_eval(tiny_kb_dir)


def test_blank_lines_ignored(tiny_kb_dir: Path) -> None:
    path = tiny_kb_dir / "history.jsonl"
    path.write_text(path.read_text() + "\n\n")
    assert len(KnowledgeBase.load(tiny_kb_dir).history) == 8


def test_duplicate_names(tiny_kb_dir: Path) -> None:
    _edit_yaml(tiny_kb_dir, "known_issues.yaml", "known_issues", lambda r: r.append(dict(r[0])))
    with pytest.raises(KBError, match="duplicate known issue"):
        KnowledgeBase.load(tiny_kb_dir)


def test_unknown_owner_team(tiny_kb_dir: Path) -> None:
    _edit_yaml(
        tiny_kb_dir, "components.yaml", "components", lambda r: r[0].update(owner_team="Zeta")
    )
    with pytest.raises(KBError, match="unknown owner team"):
        KnowledgeBase.load(tiny_kb_dir)


def test_default_assignee_not_member(tiny_kb_dir: Path) -> None:
    _edit_yaml(
        tiny_kb_dir,
        "components.yaml",
        "components",
        lambda r: r[0].update(default_assignee="Cleo Marsh"),
    )
    with pytest.raises(KBError, match="default assignee"):
        KnowledgeBase.load(tiny_kb_dir)


def test_team_lists_foreign_component(tiny_kb_dir: Path) -> None:
    _edit_yaml(tiny_kb_dir, "teams.yaml", "teams", lambda r: r[1]["components"].append("auth"))
    with pytest.raises(KBError, match="does not own"):
        KnowledgeBase.load(tiny_kb_dir)
    _edit_yaml(tiny_kb_dir, "teams.yaml", "teams", lambda r: r[1]["components"].append("ghost"))
    with pytest.raises(KBError, match="does not own"):
        KnowledgeBase.load(tiny_kb_dir)


def test_known_issue_unknown_component(tiny_kb_dir: Path) -> None:
    _edit_yaml(
        tiny_kb_dir, "known_issues.yaml", "known_issues", lambda r: r[0].update(component="ghost")
    )
    with pytest.raises(KBError, match="known issue KI-001"):
        KnowledgeBase.load(tiny_kb_dir)


def test_use_case_unknown_component(tiny_kb_dir: Path) -> None:
    _edit_yaml(
        tiny_kb_dir, "use_cases.yaml", "use_cases", lambda r: r[0]["components"].append("ghost")
    )
    with pytest.raises(KBError, match="use case"):
        KnowledgeBase.load(tiny_kb_dir)


@pytest.mark.parametrize(
    ("patch", "match"),
    [
        (lambda r: r[1].update(id="BUG-1"), "duplicate history id"),
        (lambda r: r[0].update(component="ghost"), "unknown component"),
        (lambda r: r[0].update(team="Beta"), "does not own"),
        (lambda r: r[0].update(assignee="Cleo Marsh"), "not in team"),
        (lambda r: r[0].update(duplicate_of="BUG-4"), "not an earlier id"),
        (lambda r: r[0].update(duplicate_of="BUG-0"), "not an earlier id"),
        (lambda r: r[0].update(known_issue="KI-999"), "unknown known issue"),
        (lambda r: r[0].update(known_issue="KI-002"), "belongs to"),
    ],
)
def test_history_integrity(
    tiny_kb_dir: Path, patch: Callable[[list[dict[str, Any]]], None], match: str
) -> None:
    _edit_history(tiny_kb_dir, patch)
    with pytest.raises(KBError, match=match):
        KnowledgeBase.load(tiny_kb_dir)
