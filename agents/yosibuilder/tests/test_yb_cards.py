"""yb's language wiring: cards infer their language, workers may run exactly the gates, budgets resolve."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import shlex
import sys
from pathlib import Path

import pytest

YB = Path(__file__).resolve().parent.parent / "bin" / "yb"
_loader = importlib.machinery.SourceFileLoader("yb", str(YB))
_spec = importlib.util.spec_from_loader("yb", _loader)
yb = importlib.util.module_from_spec(_spec)
sys.modules["yb"] = yb
_loader.exec_module(yb)

NEST_CARD = """id: N1
title: feat(users): find user by email
edit: src/users/users.service.ts src/users/users.service.spec.ts
read: src/users/user.entity.ts
test: npx jest src/users --ci
lint: npx tsc --noEmit && npx eslint src/users
mutants: 15
---
Goal: look a user up by email.

## Test plan
it("returns the user for a known email")
it('throws NotFoundException for an unknown email')
"""


def card(tmp_path: Path, text: str) -> yb.Card:
    path = tmp_path / "card.md"
    path.write_text(text)
    return yb.Card.load(path)


def test_nest_card_is_node_with_its_tests_and_sources(tmp_path):
    nest = card(tmp_path, NEST_CARD)
    assert nest.language.name == "node"
    assert nest.test_files == ["src/users/users.service.spec.ts"]
    assert nest.source_files == ["src/users/users.service.ts"]
    assert nest.planned_tests() == ["returns the user for a known email",
                                    "throws NotFoundException for an unknown email"]


def test_python_card_unchanged(tmp_path):
    text = (Path(__file__).resolve().parent.parent / "templates" / "task-card.md").read_text()
    python = card(tmp_path, text)
    assert python.language.name == "python"
    assert python.source_files == ["src/pkg/text.py"]
    assert "test_slugify_truncates_without_trailing_dash" in python.planned_tests()


def test_mutation_budget_card_then_env_then_language(tmp_path, monkeypatch):
    monkeypatch.delenv("YB_MUTANT_MEM_MB", raising=False)
    nest = card(tmp_path, NEST_CARD)
    assert nest.mutation_args() == {"limit": 15, "timeout": 60, "mem_mb": 4096}
    monkeypatch.setenv("YB_MUTANT_MEM_MB", "1024")
    assert nest.mutation_args()["mem_mb"] == 1024
    pinned = card(tmp_path, NEST_CARD.replace("mutants: 15", "mutant_mem_mb: 512"))
    assert pinned.mutation_args()["mem_mb"] == 512


@pytest.mark.parametrize(("header", "error"), [("lang: cobol", "unknown lang"), ("mutants: many", "must be a number")])
def test_bad_headers_are_card_errors(tmp_path, header, error):
    with pytest.raises(yb.YbError, match=error):
        card(tmp_path, NEST_CARD.replace("mutants: 15", header))


def test_claude_worker_may_run_exactly_the_gate_programs(tmp_path):
    command = yb.bind_gates(yb.claude_worker("haiku"), card(tmp_path, NEST_CARD))
    args = shlex.split(command)
    allowed = args[args.index("--allowedTools") + 1:args.index("--permission-mode")]
    assert allowed == ["Read", "Edit", "Write", "Bash(npx jest:*)", "Bash(npx tsc:*)", "Bash(npx eslint:*)"]


def test_agy_worker_allows_gate_programs_and_read_commands(tmp_path):
    command = yb.bind_gates(yb.agy_worker("m"), card(tmp_path, NEST_CARD))
    args = shlex.split(command)
    settings = json.loads(args[args.index("--settings") + 1])
    assert settings["permissions"]["allow"] == [
        f"command({name})" for name in ("npx", "ls", "cat", "grep", "find", "head")]


def test_custom_worker_command_passes_through(tmp_path):
    assert yb.bind_gates("my-worker --fast", card(tmp_path, NEST_CARD)) == "my-worker --fast"


def test_failed_setup_stops_the_card(tmp_path):
    ws = yb.Workspace(tmp_path)
    ws.runs.mkdir(parents=True)
    (ws.state_dir / "WORKLOG.md").touch()
    nest = card(tmp_path, NEST_CARD.replace("mutants: 15", "setup: exit 3"))
    with pytest.raises(yb.YbError, match="setup failed"):
        ws.prepare(nest, tmp_path)


@pytest.mark.parametrize(("template", "language", "planned"), [
    ("task-card.md", "python", 3),
    ("task-card-node.md", "node", 3),
    ("task-card-rust.md", "rust", 3),
    ("task-card-java.md", "java", 3),
    ("task-card-cpp.md", "cpp", 3),
])
def test_templates_load(template, language, planned):
    loaded = yb.Card.load(YB.parent.parent / "templates" / template)
    assert loaded.language.name == language
    assert len(loaded.planned_tests()) == planned
    assert loaded.source_files and loaded.test_files
