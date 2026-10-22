"""Tests for scripts/generate_data.py and the invariants of the generated data."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

from bug_triage.kb import KnowledgeBase, load_eval

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generate_data.py"
FILES = [
    "teams.yaml",
    "components.yaml",
    "known_issues.yaml",
    "use_cases.yaml",
    "history.jsonl",
    "eval.jsonl",
]
# Real names that must never leak into the invented data. The list itself is private, so it
# lives in a gitignored file next to this test (one name per line); without it the check skips.
FORBIDDEN_FILE = Path(__file__).with_name("forbidden_names.local.txt")


@pytest.fixture(scope="module")
def gen() -> ModuleType:
    spec = importlib.util.spec_from_file_location("generate_data", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["generate_data"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def data_dir(gen: ModuleType, tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("gen")
    gen.generate(out)
    return out


def test_deterministic(gen: ModuleType, data_dir: Path, tmp_path: Path) -> None:
    gen.generate(tmp_path / "again")
    for name in FILES:
        assert (data_dir / name).read_bytes() == (tmp_path / "again" / name).read_bytes()


def test_main_writes_files(
    gen: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert gen.main(["--out", str(tmp_path / "o")]) == 0
    assert all((tmp_path / "o" / n).is_file() for n in FILES)
    assert "wrote" in capsys.readouterr().out


def test_committed_data_matches_generator(data_dir: Path) -> None:
    real = Path(__file__).resolve().parents[1] / "data"
    for name in FILES:
        assert (real / name).read_bytes() == (data_dir / name).read_bytes(), name


def test_counts_and_validity(data_dir: Path) -> None:
    kb = KnowledgeBase.load(data_dir)
    assert len(kb.teams) == 4 and all(3 <= len(t.members) <= 4 for t in kb.teams.values())
    assert 10 <= len(kb.components) <= 12
    assert all(4 <= len(c.keywords) <= 8 for c in kb.components.values())
    assert 12 <= len(kb.known_issues) <= 18
    assert len(kb.use_cases) == 8
    assert 140 <= len(kb.history) <= 160
    ev = load_eval(data_dir)
    assert 36 <= len(ev) <= 44
    assert {s.status for s in kb.known_issues.values()} == {"open", "fixed", "wontfix"}


def test_history_invariants(data_dir: Path) -> None:
    kb = KnowledgeBase.load(data_dir)  # validates labels, duplicate_of order, KI component match
    n = len(kb.history)
    dups = [b for b in kb.history if b.duplicate_of]
    kis = [b for b in kb.history if b.known_issue]
    assert 0.10 <= len(dups) / n <= 0.22
    assert 0.12 <= len(kis) / n <= 0.35
    by_id = {b.id: b for b in kb.history}
    for d in dups:
        orig = by_id[d.duplicate_of or ""]
        assert orig.id < d.id and orig.component == d.component and orig.title == d.title
    assert len({b.severity for b in kb.history}) == 4
    non_default = [b for b in kb.history if b.assignee != kb.default_assignee(b.component)]
    assert non_default


def test_eval_invariants(data_dir: Path) -> None:
    kb = KnowledgeBase.load(data_dir)
    ev = load_eval(data_dir)
    hist = kb.history_ids()
    assert [b.id for b in ev] == [f"EVAL-{i:03d}" for i in range(1, len(ev) + 1)]
    dups = [b for b in ev if b.duplicate_of]
    assert len(dups) >= 6 and all(b.duplicate_of in hist for b in dups)
    kis = [b for b in ev if b.known_issue]
    assert len(kis) >= 8
    for b in kis:
        assert kb.known_issues[b.known_issue or ""].component == b.component
    for b in ev:
        assert kb.is_valid_component(b.component)
        assert b.team == kb.owner_team(b.component)
        assert kb.team_of(b.assignee) == b.team


def test_ambiguous_cases_present(gen: ModuleType) -> None:
    assert len(gen.AMBIGUOUS) == 10
    for _title, _desc, _log, comp in gen.AMBIGUOUS:
        assert comp in gen.COMPONENTS


def test_shared_vocabulary_is_ambiguous(data_dir: Path) -> None:
    kb = KnowledgeBase.load(data_dir)
    for word in ("login", "export", "timeout"):
        comps = {b.component for b in kb.history if word in b.text().lower()}
        assert len(comps) >= 3, word


def test_no_forbidden_names(data_dir: Path) -> None:
    if not FORBIDDEN_FILE.exists():
        pytest.skip(f"{FORBIDDEN_FILE.name} not present")
    lines = FORBIDDEN_FILE.read_text().splitlines()
    forbidden = [ln for ln in lines if ln.strip() and not ln.startswith("#")]
    blob = "".join((data_dir / n).read_text() for n in FILES)
    for name in forbidden:
        assert name not in blob
