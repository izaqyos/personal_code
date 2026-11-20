"""Structure and grounding checks for the craft suite.

Slow checks (the exemplars' own test suites) run only with CRAFT_RUN_EXEMPLARS=1.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

SUITE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SUITE / "wiki"))
sys.path.insert(0, str(SUITE / "tests"))

import audit  # noqa: E402
import snippets  # noqa: E402

SKILLS = sorted(p for p in (SUITE / "skills").iterdir() if p.is_dir())
PLAYBOOKS = sorted((SUITE / "playbooks").glob("*.md"))
ADAPTERS = [p for p in (SUITE / "adapters").rglob("*") if p.is_file()]
TASKS = sorted((SUITE / "rehearsal" / "tasks").glob("*.md"))
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
SUITE_REF_RE = re.compile(r"SUITE/([\w./-]+?)(?=[`)\s,]|$)")
HOME_REF_RE = re.compile(r"(~/work/[\w./-]+?)(?=[`)\s,]|$)")
REL_REF_RE = re.compile(r"`((?:skills|playbooks|wiki)/[\w./-]+)`")


def _kb_pages() -> tuple[list[Path], list[Path]]:
    """Gap pages and the Python playbook live in the KB now; resolve them through the catalog."""
    roots, _, sources, _ = audit.load_catalog()
    gaps = sorted(audit.resolve(s.path, roots) for s in sources if s.kind == "gap")
    extra = [audit.resolve(s.path, roots) for s in sources if s.id == "suite-python"]
    return gaps, extra


GAP_PAGES, _EXTRA = _kb_pages()
RUNNABLE_PAGES = PLAYBOOKS + GAP_PAGES + _EXTRA


def frontmatter(path: Path) -> dict[str, str]:
    m = FRONTMATTER_RE.match(path.read_text())
    assert m, f"{path} has no frontmatter"
    out = {}
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip()
    return out


def refs(text: str) -> set[Path]:
    found = {SUITE / r.rstrip(".") for r in SUITE_REF_RE.findall(text)}
    found |= {Path(r.rstrip(".")).expanduser() for r in HOME_REF_RE.findall(text)}
    found |= {SUITE / r for r in REL_REF_RE.findall(text) if "*" not in r and "<" not in r}
    return found


def test_six_phase_skills_exist():
    assert [p.name for p in SKILLS] == [
        "craft",
        "craft-build",
        "craft-frame",
        "craft-harden",
        "craft-review",
        "craft-test",
    ]


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.name)
def test_skill_frontmatter(skill: Path):
    fm = frontmatter(skill / "SKILL.md")
    assert fm.get("name") == skill.name
    assert len(fm.get("description", "")) > 60
    assert fm.get("argument-hint")


@pytest.mark.parametrize(
    "doc",
    [s / "SKILL.md" for s in SKILLS]
    + PLAYBOOKS
    + ADAPTERS
    + [SUITE / "README.md", SUITE / "wiki" / "profile.md"],
    ids=lambda p: str(p.relative_to(SUITE)),
)
def test_every_referenced_path_exists(doc: Path):
    missing = sorted(str(p) for p in refs(doc.read_text()) if not p.exists())
    assert not missing, missing


def test_every_playbook_is_used_by_a_skill():
    skill_text = "\n".join((s / "SKILL.md").read_text() for s in SKILLS)
    for pb in PLAYBOOKS:
        assert f"playbooks/{pb.name}" in skill_text, pb.name


@pytest.mark.parametrize("adapter", ADAPTERS, ids=lambda p: p.name)
def test_adapters_are_thin_and_point_at_the_suite(adapter: Path):
    text = adapter.read_text()
    assert len(text.splitlines()) < 30
    if adapter.name != "PROMPT.md":  # the paste-anywhere prompt is self-contained by design
        assert "skills/craft" in text


def test_catalog_and_index_are_valid():
    assert audit.check() == []


def test_low_grade_sources_are_never_referenced():
    _, _, sources, _ = audit.load_catalog()
    banned = [s.path.partition("/")[2] for s in sources if s.grade in ("C", "D")]
    texts = {p: p.read_text() for p in [s / "SKILL.md" for s in SKILLS] + PLAYBOOKS + ADAPTERS}
    for path, text in texts.items():
        for b in banned:
            assert b not in text, f"{path.name} references low-grade source {b}"


def test_no_path_reference_points_into_private_repos():
    # Docs may *name* the private KB to exclude it; no actual path reference may point into it.
    for p in SUITE.rglob("*.md"):
        private = [r for r in refs(p.read_text()) if any(m in str(r) for m in audit.PRIVATE_MARKERS)]
        assert not private, (p, private)


@pytest.mark.parametrize("page", RUNNABLE_PAGES, ids=lambda p: p.name)
def test_runnable_snippets_execute_and_lint(page: Path):
    assert snippets.check_page(page) == []


def test_gap_pages_are_runnable_where_they_teach_code():
    assert len(GAP_PAGES) == 7, GAP_PAGES
    for page in (p for p in GAP_PAGES if p.parent.name == "system-design"):
        langs = {lang for lang, _, _ in snippets.runnable_blocks(page.read_text())}
        assert "python" in langs, f"{page.name} has no executed Python example"


@pytest.mark.parametrize("task", TASKS, ids=lambda p: p.name)
def test_rehearsal_tasks_have_all_sections(task: Path):
    text = task.read_text()
    headings = ("## Interviewer prompt", "## Hidden NFR hooks", "## Expert moves", "## Likely follow-ups")
    for heading in headings:
        assert heading in text, f"{task.name} missing {heading}"


def test_install_links_and_removes(tmp_path: Path):
    env = {**os.environ, "CLAUDE_SKILLS_DIR": str(tmp_path)}
    script = str(SUITE / "install.sh")
    subprocess.run(["bash", script], env=env, check=True, capture_output=True)
    assert sorted(p.name for p in tmp_path.iterdir()) == [s.name for s in SKILLS]
    assert all((tmp_path / s.name).is_symlink() for s in SKILLS)
    (tmp_path / "craft-foreign").mkdir()  # unrelated dirs survive
    subprocess.run(["bash", script, "--remove"], env=env, check=True, capture_output=True)
    assert [p.name for p in tmp_path.iterdir()] == ["craft-foreign"]


@pytest.mark.skipif(not os.environ.get("CRAFT_RUN_EXEMPLARS"), reason="set CRAFT_RUN_EXEMPLARS=1")
def test_grade_a_code_exemplars_still_pass_their_own_gates():
    roots, _, sources, _ = audit.load_catalog()
    for src in (s for s in sources if s.kind == "code" and s.grade == "A"):
        result = audit.scan_code(src, audit.resolve(src.path, roots))
        assert result["tests"].startswith("PASS"), (src.id, result)
        assert result["ruff"] == "clean", (src.id, result)


TSC_FLAGS = [
    "--strict",
    "--noUncheckedIndexedAccess",
    "--erasableSyntaxOnly",
    "--exactOptionalPropertyTypes",
    "--target",
    "es2023",
    "--module",
    "nodenext",
    "--moduleResolution",
    "nodenext",
    "--lib",
    "es2023,dom",
    "--types",
    "node",
    "--noEmit",
]


@pytest.mark.skipif(
    not os.environ.get("CRAFT_TSC_DIR"), reason="set CRAFT_TSC_DIR to a dir with typescript + @types/node"
)
def test_ts_snippets_typecheck_with_playbook_flags(tmp_path: Path):
    """Type stripping only runs TS; this type-checks it with the typescript-node playbook flags."""
    files = []
    for page in RUNNABLE_PAGES:
        for lang, line, code in snippets.runnable_blocks(page.read_text()):
            if lang == "ts":
                f = tmp_path / f"{page.stem}_{line}.mts"
                f.write_text(code + "export {};\n")
                files.append(str(f))
    tsc_dir = Path(os.environ["CRAFT_TSC_DIR"])
    (tmp_path / "node_modules").symlink_to(tsc_dir / "node_modules")
    proc = subprocess.run(
        [str(tsc_dir / "node_modules" / ".bin" / "tsc"), *TSC_FLAGS, *files],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout
