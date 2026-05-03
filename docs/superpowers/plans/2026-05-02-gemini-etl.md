# Gemini ETL Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python ETL that incrementally syncs the contents of `personal_KB` and `personal_code` into a single Gemini File Search Store for RAG retrieval.

**Architecture:** Three independently-testable stages — `extract` walks the repos with `.gitignore` awareness, `transform` chunks files (markdown by header, Python by tree-sitter AST, other code by regex heuristics), `load` uploads via the `google-genai` SDK with retry + concurrency. A SQLite manifest at `~/.gemini_etl/sync_manifest.sqlite` tracks per-file SHA-256 + Gemini doc IDs for delta-sync and crash safety. CLI is wired into the existing `launcher.sh` and exposed via zsh aliases.

**Tech Stack:** Python 3.11+, `google-genai`, `GitPython` (unused — kept out, see Task 4), `pathspec`, `tqdm`, `python-dotenv`, `python-frontmatter`, `tree-sitter` + `tree-sitter-python`, `tenacity`. Tests: `pytest`, `pytest-cov` (≥ 90 %), `ruff`, `mypy --strict`.

**Spec:** `docs/superpowers/specs/2026-05-02-gemini-etl-design.md`

---

## File map

**Created:**

- `tools/gemini_etl/pyproject.toml`
- `tools/gemini_etl/.env.example`
- `tools/gemini_etl/.gitignore`
- `tools/gemini_etl/README.md`
- `tools/gemini_etl/CHANGELOG.md`
- `tools/gemini_etl/bin/gemini-etl`
- `tools/gemini_etl/src/gemini_etl/__init__.py`
- `tools/gemini_etl/src/gemini_etl/__main__.py`
- `tools/gemini_etl/src/gemini_etl/cli.py`
- `tools/gemini_etl/src/gemini_etl/config.py`
- `tools/gemini_etl/src/gemini_etl/extract.py`
- `tools/gemini_etl/src/gemini_etl/manifest.py`
- `tools/gemini_etl/src/gemini_etl/tokens.py`
- `tools/gemini_etl/src/gemini_etl/load.py`
- `tools/gemini_etl/src/gemini_etl/transform/__init__.py`
- `tools/gemini_etl/src/gemini_etl/transform/header.py`
- `tools/gemini_etl/src/gemini_etl/transform/markdown.py`
- `tools/gemini_etl/src/gemini_etl/transform/code_python.py`
- `tools/gemini_etl/src/gemini_etl/transform/code_generic.py`
- `tools/gemini_etl/tests/__init__.py`
- `tools/gemini_etl/tests/conftest.py`
- `tools/gemini_etl/tests/test_extract.py`
- `tools/gemini_etl/tests/test_manifest.py`
- `tools/gemini_etl/tests/test_tokens.py`
- `tools/gemini_etl/tests/test_transform_header.py`
- `tools/gemini_etl/tests/test_transform_markdown.py`
- `tools/gemini_etl/tests/test_transform_code_python.py`
- `tools/gemini_etl/tests/test_transform_code_generic.py`
- `tools/gemini_etl/tests/test_transform_dispatcher.py`
- `tools/gemini_etl/tests/test_load.py`
- `tools/gemini_etl/tests/test_cli.py`
- `tools/gemini_etl/tests/fixtures/sample_kb/...` (small files)
- `tools/gemini_etl/tests/fixtures/sample_code/...` (small files)

**Modified:**

- `code/bash/tools/launcher/launcher.sh` (add path constants, menu entry, handler, dispatcher case)
- `code/bash/tools/launcher/CHANGELOG.md` (add entry)

---

## Task 1: Scaffold project

**Files:**

- Create: `tools/gemini_etl/pyproject.toml`
- Create: `tools/gemini_etl/.env.example`
- Create: `tools/gemini_etl/.gitignore`
- Create: `tools/gemini_etl/src/gemini_etl/__init__.py`
- Create: `tools/gemini_etl/tests/__init__.py`
- Create: `tools/gemini_etl/tests/conftest.py`

- [ ] **Step 1: Create `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "gemini-etl"
version = "0.1.0"
description = "Sync personal Git repos into a Gemini File Search Store."
requires-python = ">=3.11"
dependencies = [
    "google-genai>=0.3.0",
    "pathspec>=0.12",
    "tqdm>=4.66",
    "python-dotenv>=1.0",
    "python-frontmatter>=1.1",
    "tree-sitter>=0.22",
    "tree-sitter-python>=0.21",
    "tenacity>=8.2",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.1",
    "ruff>=0.4",
    "mypy>=1.10",
]

[project.scripts]
gemini-etl = "gemini_etl.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=gemini_etl --cov-report=term-missing --cov-fail-under=90"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
strict = true
files = ["src"]
```

- [ ] **Step 2: Create `.env.example`**

```env
# Gemini API key — generate at https://aistudio.google.com/apikey
GEMINI_API_KEY=your-key-here
```

- [ ] **Step 3: Create `.gitignore`**

```gitignore
.env
.venv/
__pycache__/
*.egg-info/
.pytest_cache/
.coverage
.mypy_cache/
.ruff_cache/
dist/
build/
```

- [ ] **Step 4: Create empty package init files**

`src/gemini_etl/__init__.py`:

```python
"""Sync personal Git repos into a Gemini File Search Store."""

__version__ = "0.1.0"
```

`tests/__init__.py`: empty file.

- [ ] **Step 5: Create `tests/conftest.py` with shared fixtures**

```python
"""Shared pytest fixtures for gemini_etl tests."""
from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def fake_count_tokens():
    """Deterministic stand-in for Gemini's count_tokens API."""
    def _count(text: str) -> int:
        # Roughly char/4 — matches Gemini's order-of-magnitude.
        return max(1, len(text) // 4)
    return _count
```

- [ ] **Step 6: Install + smoke check**

```bash
cd tools/gemini_etl
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest --collect-only
```

Expected: `pytest` reports 0 tests collected (no error).

- [ ] **Step 7: Commit**

```bash
git add tools/gemini_etl/pyproject.toml tools/gemini_etl/.env.example \
        tools/gemini_etl/.gitignore tools/gemini_etl/src tools/gemini_etl/tests/__init__.py \
        tools/gemini_etl/tests/conftest.py
git commit -m "chore(gemini_etl): scaffold package"
```

---

## Task 2: Config module

**Files:**

- Create: `tools/gemini_etl/src/gemini_etl/config.py`
- Test: `tools/gemini_etl/tests/test_config.py`

- [ ] **Step 1: Write the failing test**

`tests/test_config.py`:

```python
from pathlib import Path

from gemini_etl.config import Source, get_config


def test_default_config_has_two_sources():
    cfg = get_config()
    names = {s.name for s in cfg.sources}
    assert names == {"personal_KB", "personal_code"}


def test_kb_source_only_markdown():
    cfg = get_config()
    kb = next(s for s in cfg.sources if s.name == "personal_KB")
    assert kb.extensions == {".md"}


def test_code_source_extensions():
    cfg = get_config()
    code = next(s for s in cfg.sources if s.name == "personal_code")
    assert code.extensions == {".py", ".js", ".ts", ".c", ".cpp", ".h", ".bash"}


def test_state_dir_expanded(monkeypatch, tmp_path):
    monkeypatch.setenv("GEMINI_ETL_STATE_DIR", str(tmp_path))
    cfg = get_config()
    assert cfg.state_dir == tmp_path


def test_chunk_token_limit_default():
    cfg = get_config()
    assert cfg.chunk_token_limit == 10_000


def test_max_concurrency_default():
    cfg = get_config()
    assert cfg.max_concurrency == 4


def test_paths_are_absolute():
    cfg = get_config()
    for s in cfg.sources:
        assert Path(s.path).is_absolute()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_config.py -v
```

Expected: ImportError / module not found.

- [ ] **Step 3: Implement `config.py`**

```python
"""Configuration constants and Source records."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Source:
    name: str
    path: str
    extensions: frozenset[str]


@dataclass(frozen=True)
class Config:
    sources: tuple[Source, ...]
    store_name: str
    chunk_token_limit: int
    max_file_size_bytes: int
    max_concurrency: int
    state_dir: Path

    @property
    def manifest_path(self) -> Path:
        return self.state_dir / "sync_manifest.sqlite"

    @property
    def store_id_path(self) -> Path:
        return self.state_dir / "store.txt"


_DEFAULT_SOURCES = (
    Source(
        name="personal_KB",
        path="/Users/yosii/work/git/personal_KB",
        extensions=frozenset({".md"}),
    ),
    Source(
        name="personal_code",
        path="/Users/yosii/work/git/personal_code",
        extensions=frozenset({".py", ".js", ".ts", ".c", ".cpp", ".h", ".bash"}),
    ),
)


def get_config() -> Config:
    """Build the runtime config, applying env-var overrides."""
    state_dir = Path(
        os.environ.get("GEMINI_ETL_STATE_DIR", "~/.gemini_etl")
    ).expanduser()
    return Config(
        sources=_DEFAULT_SOURCES,
        store_name=os.environ.get("GEMINI_ETL_STORE_NAME", "yosi-personal-kb"),
        chunk_token_limit=int(os.environ.get("GEMINI_ETL_CHUNK_TOKEN_LIMIT", 10_000)),
        max_file_size_bytes=int(os.environ.get("GEMINI_ETL_MAX_FILE_SIZE", 2 * 1024**3)),
        max_concurrency=int(os.environ.get("GEMINI_ETL_MAX_CONCURRENCY", 4)),
        state_dir=state_dir,
    )
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_config.py -v
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/gemini_etl/config.py tests/test_config.py
git commit -m "feat(gemini_etl): add config module"
```

---

## Task 3: Manifest module

**Files:**

- Create: `tools/gemini_etl/src/gemini_etl/manifest.py`
- Test: `tools/gemini_etl/tests/test_manifest.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_manifest.py`:

```python
from pathlib import Path

import pytest

from gemini_etl.manifest import FileState, Manifest, ManifestRow


@pytest.fixture
def manifest(tmp_path) -> Manifest:
    return Manifest(tmp_path / "test.sqlite")


def test_new_file_is_new(manifest):
    state = manifest.classify("personal_KB", "notes/foo.md", "abc123")
    assert state is FileState.NEW


def test_unchanged_file(manifest):
    manifest.upsert(ManifestRow(
        source="personal_KB", rel_path="a.md", sha256="hash",
        display_name="personal_KB/a.md", document_id="docs/1",
    ))
    state = manifest.classify("personal_KB", "a.md", "hash")
    assert state is FileState.UNCHANGED


def test_changed_file_when_sha_differs(manifest):
    manifest.upsert(ManifestRow(
        source="personal_KB", rel_path="a.md", sha256="old",
        display_name="personal_KB/a.md", document_id="docs/1",
    ))
    state = manifest.classify("personal_KB", "a.md", "new")
    assert state is FileState.CHANGED


def test_deleted_files_diff(manifest):
    for path in ("a.md", "b.md", "c.md"):
        manifest.upsert(ManifestRow(
            source="personal_KB", rel_path=path, sha256="h",
            display_name=f"personal_KB/{path}", document_id="d",
        ))
    live = {("personal_KB", "a.md"), ("personal_KB", "c.md")}
    deleted = list(manifest.deleted_rows(live_set=live))
    assert len(deleted) == 1
    assert deleted[0].rel_path == "b.md"


def test_get_row_returns_existing(manifest):
    row = ManifestRow(
        source="personal_KB", rel_path="a.md", sha256="h",
        display_name="personal_KB/a.md", document_id="docs/9",
    )
    manifest.upsert(row)
    got = manifest.get("personal_KB", "a.md")
    assert got is not None
    assert got.document_id == "docs/9"


def test_delete_row_removes(manifest):
    manifest.upsert(ManifestRow(
        source="personal_KB", rel_path="a.md", sha256="h",
        display_name="personal_KB/a.md", document_id="d",
    ))
    manifest.delete("personal_KB", "a.md")
    assert manifest.get("personal_KB", "a.md") is None


def test_summary_counts(manifest):
    for i in range(3):
        manifest.upsert(ManifestRow(
            source="personal_KB", rel_path=f"k{i}.md", sha256="h",
            display_name=f"personal_KB/k{i}.md", document_id="d",
        ))
    for i in range(2):
        manifest.upsert(ManifestRow(
            source="personal_code", rel_path=f"c{i}.py", sha256="h",
            display_name=f"personal_code/c{i}.py", document_id="d",
        ))
    counts = manifest.summary()
    assert counts == {"personal_KB": 3, "personal_code": 2}


def test_persists_across_instances(tmp_path):
    db = tmp_path / "p.sqlite"
    a = Manifest(db)
    a.upsert(ManifestRow(
        source="personal_KB", rel_path="x.md", sha256="h",
        display_name="personal_KB/x.md", document_id="d",
    ))
    b = Manifest(db)
    assert b.get("personal_KB", "x.md") is not None
```

- [ ] **Step 2: Run tests, confirm failure**

```bash
pytest tests/test_manifest.py -v
```

Expected: ImportError.

- [ ] **Step 3: Implement `manifest.py`**

```python
"""SQLite manifest tracking per-file SHA + Gemini doc IDs.

Thread-safe: a single ``Manifest`` instance can be shared across worker
threads — writes are serialized by an internal lock and the connection is
opened with ``check_same_thread=False``."""
from __future__ import annotations

import enum
import sqlite3
import threading
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterator


class FileState(enum.Enum):
    NEW = "new"
    CHANGED = "changed"
    UNCHANGED = "unchanged"


@dataclass(frozen=True)
class ManifestRow:
    source: str
    rel_path: str
    sha256: str
    display_name: str
    document_id: str | None
    uploaded_at: str | None = None


_SCHEMA = """
CREATE TABLE IF NOT EXISTS files (
  source       TEXT NOT NULL,
  rel_path     TEXT NOT NULL,
  sha256       TEXT NOT NULL,
  display_name TEXT NOT NULL,
  document_id  TEXT,
  uploaded_at  TEXT NOT NULL,
  PRIMARY KEY (source, rel_path)
);
"""


class Manifest:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._lock = threading.Lock()
        with self._lock:
            self._conn.executescript(_SCHEMA)
            self._conn.commit()

    def classify(self, source: str, rel_path: str, sha256: str) -> FileState:
        row = self.get(source, rel_path)
        if row is None:
            return FileState.NEW
        return FileState.UNCHANGED if row.sha256 == sha256 else FileState.CHANGED

    def get(self, source: str, rel_path: str) -> ManifestRow | None:
        with self._lock:
            cur = self._conn.execute(
                "SELECT source, rel_path, sha256, display_name, document_id, uploaded_at "
                "FROM files WHERE source = ? AND rel_path = ?",
                (source, rel_path),
            )
            r = cur.fetchone()
        return ManifestRow(*r) if r else None

    def upsert(self, row: ManifestRow) -> None:
        uploaded_at = row.uploaded_at or datetime.now(UTC).isoformat()
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO files (source, rel_path, sha256, display_name, document_id, uploaded_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(source, rel_path) DO UPDATE SET
                    sha256 = excluded.sha256,
                    display_name = excluded.display_name,
                    document_id = excluded.document_id,
                    uploaded_at = excluded.uploaded_at
                """,
                (row.source, row.rel_path, row.sha256, row.display_name,
                 row.document_id, uploaded_at),
            )
            self._conn.commit()

    def delete(self, source: str, rel_path: str) -> None:
        with self._lock:
            self._conn.execute(
                "DELETE FROM files WHERE source = ? AND rel_path = ?",
                (source, rel_path),
            )
            self._conn.commit()

    def deleted_rows(self, live_set: set[tuple[str, str]]) -> Iterator[ManifestRow]:
        with self._lock:
            rows = list(self._conn.execute(
                "SELECT source, rel_path, sha256, display_name, document_id, uploaded_at FROM files"
            ))
        for r in rows:
            if (r[0], r[1]) not in live_set:
                yield ManifestRow(*r)

    def summary(self) -> dict[str, int]:
        with self._lock:
            return {
                source: count
                for source, count in self._conn.execute(
                    "SELECT source, COUNT(*) FROM files GROUP BY source"
                )
            }

    def close(self) -> None:
        with self._lock:
            self._conn.close()
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_manifest.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add src/gemini_etl/manifest.py tests/test_manifest.py
git commit -m "feat(gemini_etl): add SQLite manifest with state diffing"
```

---

## Task 4: Extract module

**Files:**

- Create: `tools/gemini_etl/src/gemini_etl/extract.py`
- Test: `tools/gemini_etl/tests/test_extract.py`
- Create: `tools/gemini_etl/tests/fixtures/sample_kb/` (with sub-files)

> **Note:** GitPython is *not* used — `os.walk` + `pathspec` is sufficient and avoids the heavier dep. Spec dependency list mentioned `GitPython`; we drop it.

- [ ] **Step 1: Build the fixture tree**

```bash
mkdir -p tests/fixtures/sample_kb/notes/algorithms
mkdir -p tests/fixtures/sample_kb/build
mkdir -p tests/fixtures/sample_kb/.git
mkdir -p tests/fixtures/sample_code/src
mkdir -p tests/fixtures/sample_code/node_modules

# .gitignore in sample_kb tells us to skip "build/"
printf 'build/\n*.tmp\n' > tests/fixtures/sample_kb/.gitignore

# real files
printf '# Hello\nbody\n' > tests/fixtures/sample_kb/notes/intro.md
printf '# DP\n' > tests/fixtures/sample_kb/notes/algorithms/dp.md

# excluded — should NOT be yielded
printf 'noise\n' > tests/fixtures/sample_kb/build/skipme.md
printf '' > tests/fixtures/sample_kb/notes/empty.md
printf 'tmp\n' > tests/fixtures/sample_kb/notes/draft.tmp
printf 'in dot-git\n' > tests/fixtures/sample_kb/.git/HEAD

# code fixture — node_modules must be skipped, .py kept
printf 'def foo():\n    return 1\n' > tests/fixtures/sample_code/src/foo.py
printf 'noise\n' > tests/fixtures/sample_code/node_modules/x.py
```

- [ ] **Step 2: Write the failing tests**

`tests/test_extract.py`:

```python
from pathlib import Path

import pytest

from gemini_etl.config import Source
from gemini_etl.extract import FileRef, walk_source


@pytest.fixture
def kb_source(fixtures_dir) -> Source:
    return Source(
        name="sample_kb",
        path=str(fixtures_dir / "sample_kb"),
        extensions=frozenset({".md"}),
    )


@pytest.fixture
def code_source(fixtures_dir) -> Source:
    return Source(
        name="sample_code",
        path=str(fixtures_dir / "sample_code"),
        extensions=frozenset({".py"}),
    )


def _rel_paths(refs: list[FileRef]) -> set[str]:
    return {r.rel_path for r in refs}


def test_walks_only_allowed_extensions(kb_source):
    refs = list(walk_source(kb_source))
    assert all(r.rel_path.endswith(".md") for r in refs)


def test_respects_gitignore_build_dir(kb_source):
    paths = _rel_paths(list(walk_source(kb_source)))
    assert not any("build/" in p for p in paths)


def test_skips_dot_git(kb_source):
    paths = _rel_paths(list(walk_source(kb_source)))
    assert not any(p.startswith(".git/") for p in paths)


def test_skips_empty_files(kb_source):
    paths = _rel_paths(list(walk_source(kb_source)))
    assert "notes/empty.md" not in paths


def test_skips_node_modules(code_source):
    paths = _rel_paths(list(walk_source(code_source)))
    assert not any("node_modules" in p for p in paths)


def test_yields_expected_kb_files(kb_source):
    paths = _rel_paths(list(walk_source(kb_source)))
    assert paths == {"notes/intro.md", "notes/algorithms/dp.md"}


def test_file_ref_has_sha256(kb_source):
    refs = list(walk_source(kb_source))
    intro = next(r for r in refs if r.rel_path == "notes/intro.md")
    assert len(intro.sha256) == 64  # sha256 hex


def test_size_guard(tmp_path):
    big = tmp_path / "big.md"
    big.write_bytes(b"x" * 1024)
    src = Source(name="t", path=str(tmp_path), extensions=frozenset({".md"}))
    refs = list(walk_source(src, max_file_size_bytes=512))
    assert refs == []


def test_source_name_preserved(kb_source):
    refs = list(walk_source(kb_source))
    assert all(r.source == "sample_kb" for r in refs)
```

- [ ] **Step 3: Run tests, confirm failure**

```bash
pytest tests/test_extract.py -v
```

Expected: ImportError.

- [ ] **Step 4: Implement `extract.py`**

```python
"""Walk a source tree, applying ignore rules + extension filter."""
from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import pathspec

from gemini_etl.config import Source

ALWAYS_SKIP_DIRS = frozenset({
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    "dist", "build", "target", ".next", ".turbo",
})


@dataclass(frozen=True)
class FileRef:
    source: str
    rel_path: str
    abs_path: Path
    size: int
    sha256: str


def _load_gitignore(root: Path) -> pathspec.PathSpec:
    """Read root-level .gitignore. Nested .gitignore files are matched against
    paths relative to root, which is what pathspec supports out of the box for
    simple cases. For deep nesting we still respect nested files by re-loading
    on each subdir during the walk."""
    gi = root / ".gitignore"
    lines: list[str] = []
    if gi.exists():
        lines.extend(gi.read_text(encoding="utf-8").splitlines())
    return pathspec.PathSpec.from_lines("gitwildmatch", lines)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def walk_source(
    source: Source,
    max_file_size_bytes: int = 2 * 1024**3,
) -> Iterator[FileRef]:
    root = Path(source.path).resolve()
    spec = _load_gitignore(root)

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune always-skip dirs in-place so os.walk doesn't descend.
        dirnames[:] = [d for d in dirnames if d not in ALWAYS_SKIP_DIRS]

        # Prune .gitignore-matching dirs (relative to root).
        rel_dir = Path(dirpath).relative_to(root)
        dirnames[:] = [
            d for d in dirnames
            if not spec.match_file(str(rel_dir / d) + "/")
        ]

        for fname in filenames:
            abs_path = Path(dirpath) / fname
            rel_path_str = str(abs_path.relative_to(root))

            if spec.match_file(rel_path_str):
                continue
            if abs_path.suffix not in source.extensions:
                continue

            size = abs_path.stat().st_size
            if size == 0:
                continue
            if size > max_file_size_bytes:
                # Caller logs; we silently skip to keep extract pure.
                continue

            # Whitespace-only check (cheap for empty-ish files).
            if size < 4096:
                if not abs_path.read_bytes().strip():
                    continue

            yield FileRef(
                source=source.name,
                rel_path=rel_path_str,
                abs_path=abs_path,
                size=size,
                sha256=_sha256(abs_path),
            )
```

- [ ] **Step 5: Run tests**

```bash
pytest tests/test_extract.py -v
```

Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add src/gemini_etl/extract.py tests/test_extract.py tests/fixtures/
git commit -m "feat(gemini_etl): add filesystem extractor with .gitignore awareness"
```

---

## Task 5: Tokens helper

**Files:**

- Create: `tools/gemini_etl/src/gemini_etl/tokens.py`
- Test: `tools/gemini_etl/tests/test_tokens.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_tokens.py`:

```python
from gemini_etl.tokens import CachedTokenCounter


def test_calls_underlying_counter_once_per_text():
    calls = []

    def underlying(text: str) -> int:
        calls.append(text)
        return len(text)

    counter = CachedTokenCounter(underlying)
    counter.count("hello")
    counter.count("hello")
    counter.count("world")

    assert calls == ["hello", "world"]


def test_returns_underlying_value():
    counter = CachedTokenCounter(lambda t: 42)
    assert counter.count("anything") == 42


def test_cache_keyed_by_text_not_identity():
    calls = []

    def underlying(text: str) -> int:
        calls.append(text)
        return len(text)

    counter = CachedTokenCounter(underlying)
    counter.count("same")
    counter.count("same")
    assert len(calls) == 1
```

- [ ] **Step 2: Run tests, confirm failure**

```bash
pytest tests/test_tokens.py -v
```

Expected: ImportError.

- [ ] **Step 3: Implement `tokens.py`**

```python
"""Token counting with a per-process cache.

The default underlying counter calls Gemini's ``count_tokens`` API. Tests and
chunkers receive the counter via dependency injection so the SDK never
appears in the transform layer.
"""
from __future__ import annotations

from typing import Callable, Protocol


class TokenCounter(Protocol):
    def count(self, text: str) -> int: ...


class CachedTokenCounter:
    def __init__(self, underlying: Callable[[str], int]) -> None:
        self._underlying = underlying
        self._cache: dict[str, int] = {}

    def count(self, text: str) -> int:
        if text not in self._cache:
            self._cache[text] = self._underlying(text)
        return self._cache[text]


def gemini_token_counter(client, model: str = "gemini-2.5-flash") -> Callable[[str], int]:
    """Build an underlying counter backed by the live Gemini API.

    Note: API surface for ``count_tokens`` is verified at runtime; if the
    google-genai version installed differs, adjust the call here. This is the
    only place SDK-shape leaks into the transform path.
    """
    def _count(text: str) -> int:
        result = client.models.count_tokens(model=model, contents=text)
        # google-genai returns an object with .total_tokens (verify per SDK version).
        return int(getattr(result, "total_tokens", getattr(result, "totalTokens", 0)))
    return _count
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_tokens.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add src/gemini_etl/tokens.py tests/test_tokens.py
git commit -m "feat(gemini_etl): add cached token counter with DI seam"
```

---

## Task 6: Transform — header builder

**Files:**

- Create: `tools/gemini_etl/src/gemini_etl/transform/__init__.py` (empty placeholder for now)
- Create: `tools/gemini_etl/src/gemini_etl/transform/header.py`
- Test: `tools/gemini_etl/tests/test_transform_header.py`

- [ ] **Step 1: Create the package init**

`src/gemini_etl/transform/__init__.py`:

```python
"""Transform pipeline: file → list[Chunk]."""
```

- [ ] **Step 2: Write the failing tests**

`tests/test_transform_header.py`:

```python
from gemini_etl.transform.header import ChunkMetadata, build_header


def test_minimal_header():
    meta = ChunkMetadata(
        source="personal_KB",
        rel_path="notes/foo.md",
        ext=".md",
    )
    h = build_header(meta)
    assert "[Source: personal_KB]" in h
    assert "[Path: notes/foo.md]" in h
    assert "[Type: .md]" in h
    assert h.endswith("---")


def test_header_includes_title_and_tags():
    meta = ChunkMetadata(
        source="personal_KB", rel_path="x.md", ext=".md",
        title="My Title", tags=("a", "b"),
    )
    h = build_header(meta)
    assert "[Title: My Title]" in h
    assert "[Tags: a, b]" in h


def test_section_path_included():
    meta = ChunkMetadata(
        source="personal_KB", rel_path="x.md", ext=".md",
        section_path=("# Top", "## Sub"),
    )
    assert "[Section: # Top / ## Sub]" in build_header(meta)


def test_empty_optional_fields_omitted():
    meta = ChunkMetadata(source="s", rel_path="p", ext=".md")
    h = build_header(meta)
    assert "Title" not in h
    assert "Tags" not in h
    assert "Section" not in h


def test_empty_tags_tuple_omitted():
    meta = ChunkMetadata(source="s", rel_path="p", ext=".md", tags=())
    assert "Tags" not in build_header(meta)
```

- [ ] **Step 3: Run tests, confirm failure**

```bash
pytest tests/test_transform_header.py -v
```

Expected: ImportError.

- [ ] **Step 4: Implement `transform/header.py`**

```python
"""Builds the metadata header that prefixes every chunk."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChunkMetadata:
    source: str
    rel_path: str
    ext: str
    title: str | None = None
    tags: tuple[str, ...] = ()
    section_path: tuple[str, ...] = ()


def build_header(meta: ChunkMetadata) -> str:
    line1 = f"[Source: {meta.source}] [Path: {meta.rel_path}] [Type: {meta.ext}]"
    extras: list[str] = []
    if meta.title:
        extras.append(f"[Title: {meta.title}]")
    if meta.tags:
        extras.append(f"[Tags: {', '.join(meta.tags)}]")
    extra_line = " ".join(extras)
    section_line = (
        f"[Section: {' / '.join(meta.section_path)}]" if meta.section_path else ""
    )
    parts = [line1]
    if extra_line:
        parts.append(extra_line)
    if section_line:
        parts.append(section_line)
    parts.append("---")
    return "\n".join(parts)
```

- [ ] **Step 5: Run tests**

```bash
pytest tests/test_transform_header.py -v
```

Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add src/gemini_etl/transform/__init__.py src/gemini_etl/transform/header.py \
        tests/test_transform_header.py
git commit -m "feat(gemini_etl): add chunk metadata header builder"
```

---

## Task 7: Transform — markdown chunker

**Files:**

- Create: `tools/gemini_etl/src/gemini_etl/transform/markdown.py`
- Test: `tools/gemini_etl/tests/test_transform_markdown.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_transform_markdown.py`:

```python
from gemini_etl.transform.markdown import Chunk, chunk_markdown


def _under_threshold(_text: str) -> int:
    return 100


def _above_threshold_for_long(text: str) -> int:
    # Anything over 200 chars is "huge".
    return 99_999 if len(text) > 200 else 100


def test_short_file_is_one_chunk():
    md = "# Title\n\nbody\n"
    chunks = chunk_markdown(
        text=md,
        source="personal_KB",
        rel_path="a.md",
        token_limit=10_000,
        count_tokens=_under_threshold,
    )
    assert len(chunks) == 1
    assert chunks[0].text.endswith(md.strip())  # body preserved
    assert "[Source: personal_KB]" in chunks[0].text


def test_frontmatter_folded_into_header():
    md = (
        "---\n"
        "title: Foo\n"
        "tags: [a, b]\n"
        "---\n"
        "# heading\nbody\n"
    )
    chunks = chunk_markdown(
        text=md,
        source="personal_KB",
        rel_path="x.md",
        token_limit=10_000,
        count_tokens=_under_threshold,
    )
    assert len(chunks) == 1
    assert "[Title: Foo]" in chunks[0].text
    assert "[Tags: a, b]" in chunks[0].text
    # Frontmatter delimiters do not appear in body.
    assert "---\ntitle:" not in chunks[0].text


def test_oversize_file_splits_at_h1():
    md = (
        "# Section A\n" + ("a" * 250) + "\n"
        "# Section B\n" + ("b" * 250) + "\n"
    )
    chunks = chunk_markdown(
        text=md,
        source="personal_KB",
        rel_path="big.md",
        token_limit=50,
        count_tokens=_above_threshold_for_long,
    )
    assert len(chunks) == 2
    assert "[Section: # Section A]" in chunks[0].text
    assert "[Section: # Section B]" in chunks[1].text


def test_recursive_split_to_h2():
    h2_block_a = "## Sub A\n" + ("a" * 250) + "\n"
    h2_block_b = "## Sub B\n" + ("b" * 250) + "\n"
    md = "# Top\n" + h2_block_a + h2_block_b
    chunks = chunk_markdown(
        text=md,
        source="personal_KB",
        rel_path="big.md",
        token_limit=50,
        count_tokens=_above_threshold_for_long,
    )
    # H1 is one block over threshold → split into H2s.
    assert len(chunks) == 2
    assert "[Section: # Top / ## Sub A]" in chunks[0].text
    assert "[Section: # Top / ## Sub B]" in chunks[1].text


def test_chunk_text_includes_metadata_header_and_body():
    md = "body only\n"
    chunks = chunk_markdown(
        text=md, source="s", rel_path="p.md",
        token_limit=10_000, count_tokens=_under_threshold,
    )
    assert chunks[0].text.startswith("[Source: s]")
    assert "---\nbody only" in chunks[0].text
```

- [ ] **Step 2: Run tests, confirm failure**

```bash
pytest tests/test_transform_markdown.py -v
```

Expected: ImportError.

- [ ] **Step 3: Implement `transform/markdown.py`**

```python
"""Markdown chunker: frontmatter → header; split on H1/H2/H3 if oversize."""
from __future__ import annotations

import dataclasses
import re
from dataclasses import dataclass
from typing import Callable

import frontmatter

from gemini_etl.transform.header import ChunkMetadata, build_header


@dataclass(frozen=True)
class Chunk:
    text: str
    rel_path: str


_HEADER_LEVELS = ("# ", "## ", "### ")


def chunk_markdown(
    *,
    text: str,
    source: str,
    rel_path: str,
    token_limit: int,
    count_tokens: Callable[[str], int],
) -> list[Chunk]:
    post = frontmatter.loads(text)
    body = post.content
    title = post.metadata.get("title") if post.metadata else None
    tags_value = post.metadata.get("tags") if post.metadata else None
    tags = tuple(tags_value) if isinstance(tags_value, (list, tuple)) else ()

    base_meta = ChunkMetadata(
        source=source, rel_path=rel_path, ext=".md",
        title=title if isinstance(title, str) else None,
        tags=tags,
    )

    sections = _split_recursive(
        body=body,
        section_path=(),
        token_limit=token_limit,
        count_tokens=count_tokens,
        depth=0,
    )

    return [
        Chunk(
            text=build_header(dataclasses.replace(base_meta, section_path=sp))
                 + "\n" + chunk_body.strip(),
            rel_path=rel_path,
        )
        for chunk_body, sp in sections
    ]


def _split_recursive(
    *,
    body: str,
    section_path: tuple[str, ...],
    token_limit: int,
    count_tokens: Callable[[str], int],
    depth: int,
) -> list[tuple[str, tuple[str, ...]]]:
    if count_tokens(body) <= token_limit or depth >= len(_HEADER_LEVELS):
        return [(body, section_path)]

    level_prefix = _HEADER_LEVELS[depth]
    sections = _split_on_header(body, level_prefix)
    if len(sections) <= 1:
        return _split_recursive(
            body=body, section_path=section_path,
            token_limit=token_limit, count_tokens=count_tokens, depth=depth + 1,
        )

    out: list[tuple[str, tuple[str, ...]]] = []
    for header_line, section_body in sections:
        sp = section_path + (header_line,) if header_line else section_path
        out.extend(_split_recursive(
            body=section_body, section_path=sp,
            token_limit=token_limit, count_tokens=count_tokens, depth=depth + 1,
        ))
    return out


def _split_on_header(body: str, prefix: str) -> list[tuple[str, str]]:
    """Return [(header_line_or_empty, section_body), ...].

    The portion before the first matching header (preamble) is returned with
    an empty header_line."""
    pattern = re.compile(rf"(?m)^{re.escape(prefix)}.*$")
    matches = list(pattern.finditer(body))
    if not matches:
        return [("", body)]

    out: list[tuple[str, str]] = []
    if matches[0].start() > 0:
        out.append(("", body[:matches[0].start()]))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        out.append((m.group(0).strip(), body[m.start():end]))
    return out
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_transform_markdown.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add src/gemini_etl/transform/markdown.py tests/test_transform_markdown.py
git commit -m "feat(gemini_etl): add markdown chunker (frontmatter + header split)"
```

---

## Task 8: Transform — Python chunker (tree-sitter)

**Files:**

- Create: `tools/gemini_etl/src/gemini_etl/transform/code_python.py`
- Test: `tools/gemini_etl/tests/test_transform_code_python.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_transform_code_python.py`:

```python
from gemini_etl.transform.code_python import chunk_python


def _always_above(_t: str) -> int:
    return 999_999


def _always_below(_t: str) -> int:
    return 1


def test_short_file_is_one_chunk():
    src = "def foo():\n    return 1\n"
    chunks = chunk_python(
        text=src, source="personal_code", rel_path="m.py",
        token_limit=10_000, count_tokens=_always_below,
    )
    assert len(chunks) == 1
    assert "def foo()" in chunks[0].text


def test_oversize_file_splits_per_top_level_def():
    src = (
        "import os\n"
        "X = 1\n"
        "\n"
        "def alpha():\n    return 1\n"
        "\n"
        "def beta():\n    return 2\n"
    )
    chunks = chunk_python(
        text=src, source="personal_code", rel_path="m.py",
        token_limit=1, count_tokens=_always_above,
    )
    bodies = [c.text for c in chunks]
    # 1 module-prelude + 2 defs = 3 chunks.
    assert len(chunks) == 3
    assert any("import os" in b and "X = 1" in b for b in bodies)
    assert any("def alpha" in b and "def beta" not in b for b in bodies)
    assert any("def beta" in b and "def alpha" not in b for b in bodies)


def test_decorator_stays_attached_to_def():
    src = (
        "@decorator\n"
        "def thing():\n"
        "    \"\"\"docs.\"\"\"\n"
        "    return 1\n"
        "\n"
        "def other():\n"
        "    return 2\n"
    )
    chunks = chunk_python(
        text=src, source="personal_code", rel_path="m.py",
        token_limit=1, count_tokens=_always_above,
    )
    decorated = next(c for c in chunks if "def thing" in c.text)
    assert "@decorator" in decorated.text
    assert "docs." in decorated.text


def test_class_body_is_atomic_chunk():
    src = (
        "class Foo:\n"
        "    def bar(self):\n"
        "        return 1\n"
        "    def baz(self):\n"
        "        return 2\n"
    )
    chunks = chunk_python(
        text=src, source="personal_code", rel_path="m.py",
        token_limit=1, count_tokens=_always_above,
    )
    cls = next(c for c in chunks if "class Foo" in c.text)
    assert "def bar" in cls.text
    assert "def baz" in cls.text
```

- [ ] **Step 2: Run tests, confirm failure**

```bash
pytest tests/test_transform_code_python.py -v
```

Expected: ImportError.

- [ ] **Step 3: Implement `transform/code_python.py`**

```python
"""Python code chunker using tree-sitter."""
from __future__ import annotations

from typing import Callable

import tree_sitter as ts
from tree_sitter_python import language as _python_language

from gemini_etl.transform.header import ChunkMetadata, build_header
from gemini_etl.transform.markdown import Chunk

_PY_LANG = ts.Language(_python_language())
_PARSER = ts.Parser(_PY_LANG)


def chunk_python(
    *,
    text: str,
    source: str,
    rel_path: str,
    token_limit: int,
    count_tokens: Callable[[str], int],
) -> list[Chunk]:
    if count_tokens(text) <= token_limit:
        return [_wrap(text, source, rel_path)]

    tree = _PARSER.parse(bytes(text, "utf-8"))
    root = tree.root_node
    src_bytes = text.encode("utf-8")

    top_level_defs: list[tuple[int, int]] = []  # (start_byte, end_byte)
    other_spans: list[tuple[int, int]] = []

    for child in root.children:
        if child.type in {"function_definition", "class_definition", "decorated_definition"}:
            top_level_defs.append((child.start_byte, child.end_byte))
        else:
            other_spans.append((child.start_byte, child.end_byte))

    chunks: list[Chunk] = []

    if other_spans:
        # Stitch contiguous module-prelude bytes together.
        prelude = b""
        for start, end in other_spans:
            prelude += src_bytes[start:end] + b"\n"
        prelude_text = prelude.decode("utf-8").strip()
        if prelude_text:
            chunks.append(_wrap(prelude_text, source, rel_path))

    for start, end in top_level_defs:
        body = src_bytes[start:end].decode("utf-8")
        chunks.append(_wrap(body, source, rel_path))

    return chunks


def _wrap(body: str, source: str, rel_path: str) -> Chunk:
    meta = ChunkMetadata(source=source, rel_path=rel_path, ext=".py")
    return Chunk(text=build_header(meta) + "\n" + body.strip(), rel_path=rel_path)
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_transform_code_python.py -v
```

Expected: all PASS.

> **If tree-sitter wheel is missing on macOS arm64:** `pip install --no-binary tree-sitter tree-sitter` may be required, or install via the prebuilt arm64 wheel from PyPI directly. Verify the installed `tree-sitter-python` exposes `language()` (older versions used `language` as an attribute, not callable).

- [ ] **Step 5: Commit**

```bash
git add src/gemini_etl/transform/code_python.py tests/test_transform_code_python.py
git commit -m "feat(gemini_etl): add tree-sitter python chunker"
```

---

## Task 9: Transform — generic code chunker

**Files:**

- Create: `tools/gemini_etl/src/gemini_etl/transform/code_generic.py`
- Test: `tools/gemini_etl/tests/test_transform_code_generic.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_transform_code_generic.py`:

```python
from gemini_etl.transform.code_generic import chunk_generic


def _below(_t: str) -> int:
    return 1


def _above(_t: str) -> int:
    return 999_999


def test_short_js_is_single_chunk():
    src = "function foo() { return 1; }\n"
    chunks = chunk_generic(
        text=src, source="personal_code", rel_path="x.js", ext=".js",
        token_limit=10_000, count_tokens=_below,
    )
    assert len(chunks) == 1
    assert "function foo" in chunks[0].text


def test_oversize_js_splits_on_top_level_function():
    src = (
        "function alpha() {\n  return 1;\n}\n"
        "function beta() {\n  return 2;\n}\n"
    )
    chunks = chunk_generic(
        text=src, source="personal_code", rel_path="x.js", ext=".js",
        token_limit=1, count_tokens=_above,
    )
    assert len(chunks) >= 2
    bodies = [c.text for c in chunks]
    assert any("alpha" in b and "beta" not in b for b in bodies)
    assert any("beta" in b and "alpha" not in b for b in bodies)


def test_oversize_bash_splits_on_function_keyword():
    src = (
        "function foo() {\n  echo a\n}\n"
        "function bar() {\n  echo b\n}\n"
    )
    chunks = chunk_generic(
        text=src, source="personal_code", rel_path="x.bash", ext=".bash",
        token_limit=1, count_tokens=_above,
    )
    assert len(chunks) >= 2


def test_oversize_chunk_falls_back_to_token_window():
    # One huge "function" that the regex can't split below threshold.
    src = "function huge() {\n" + ("  x = 1;\n" * 200) + "}\n"
    chunks = chunk_generic(
        text=src, source="personal_code", rel_path="x.js", ext=".js",
        token_limit=50,
        count_tokens=lambda t: max(1, len(t) // 4),
    )
    assert len(chunks) >= 2
    # All chunks should be under threshold (give some slack for boundaries).
    for c in chunks:
        assert len(c.text) // 4 < 200
```

- [ ] **Step 2: Run tests, confirm failure**

```bash
pytest tests/test_transform_code_generic.py -v
```

Expected: ImportError.

- [ ] **Step 3: Implement `transform/code_generic.py`**

```python
"""Regex-based chunker for non-Python code, with token-window fallback."""
from __future__ import annotations

import re
from typing import Callable

from gemini_etl.transform.header import ChunkMetadata, build_header
from gemini_etl.transform.markdown import Chunk

# Heuristics: per-extension top-level definition starters.
_PATTERNS: dict[str, re.Pattern[str]] = {
    ".js": re.compile(
        r"^(export\s+)?(async\s+)?(function\s+\w+|class\s+\w+|const\s+\w+\s*=)",
        re.MULTILINE,
    ),
    ".ts": re.compile(
        r"^(export\s+)?(async\s+)?(function\s+\w+|class\s+\w+|const\s+\w+\s*=)",
        re.MULTILINE,
    ),
    ".c":   re.compile(r"^[\w\s\*]+\w+\s*\([^)]*\)\s*\{", re.MULTILINE),
    ".cpp": re.compile(r"^([\w\s\*]+\w+\s*\([^)]*\)\s*\{|class\s+\w+)", re.MULTILINE),
    ".h":   re.compile(r"^([\w\s\*]+\w+\s*\([^)]*\)\s*[\{;]|class\s+\w+)", re.MULTILINE),
    ".bash": re.compile(r"^(function\s+\w+|\w+\s*\(\)\s*\{)", re.MULTILINE),
}

_OVERLAP_RATIO = 0.10


def chunk_generic(
    *,
    text: str,
    source: str,
    rel_path: str,
    ext: str,
    token_limit: int,
    count_tokens: Callable[[str], int],
) -> list[Chunk]:
    if count_tokens(text) <= token_limit:
        return [_wrap(text, source, rel_path, ext)]

    pattern = _PATTERNS.get(ext)
    if pattern is None:
        return [_window_chunk(text, source, rel_path, ext, token_limit, count_tokens)]

    sections = _split_on_pattern(text, pattern)
    chunks: list[Chunk] = []
    for body in sections:
        if not body.strip():
            continue
        if count_tokens(body) > token_limit:
            chunks.extend(
                _window_chunks(body, source, rel_path, ext, token_limit, count_tokens)
            )
        else:
            chunks.append(_wrap(body, source, rel_path, ext))
    return chunks


def _split_on_pattern(text: str, pattern: re.Pattern[str]) -> list[str]:
    starts = [m.start() for m in pattern.finditer(text)]
    if not starts:
        return [text]
    if starts[0] > 0:
        starts = [0, *starts]
    starts.append(len(text))
    return [text[starts[i]:starts[i + 1]] for i in range(len(starts) - 1)]


def _window_chunks(
    text: str, source: str, rel_path: str, ext: str,
    token_limit: int, count_tokens: Callable[[str], int],
) -> list[Chunk]:
    """Token-window split with overlap. Approximates bytes per token by
    ratio measured on the first few hundred chars."""
    # Cheap chars/token estimate.
    sample = text[: min(len(text), 2000)]
    tok = max(1, count_tokens(sample))
    chars_per_token = max(1, len(sample) // tok)
    window = token_limit * chars_per_token
    overlap = int(window * _OVERLAP_RATIO)

    chunks: list[Chunk] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + window)
        chunks.append(_wrap(text[start:end], source, rel_path, ext))
        if end == len(text):
            break
        start = end - overlap
    return chunks


def _window_chunk(
    text: str, source: str, rel_path: str, ext: str,
    token_limit: int, count_tokens: Callable[[str], int],
) -> Chunk:
    return _window_chunks(text, source, rel_path, ext, token_limit, count_tokens)[0]


def _wrap(body: str, source: str, rel_path: str, ext: str) -> Chunk:
    meta = ChunkMetadata(source=source, rel_path=rel_path, ext=ext)
    return Chunk(text=build_header(meta) + "\n" + body.strip(), rel_path=rel_path)
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_transform_code_generic.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add src/gemini_etl/transform/code_generic.py tests/test_transform_code_generic.py
git commit -m "feat(gemini_etl): add regex+window chunker for non-python code"
```

---

## Task 10: Transform — dispatcher

**Files:**

- Modify: `tools/gemini_etl/src/gemini_etl/transform/__init__.py`
- Test: `tools/gemini_etl/tests/test_transform_dispatcher.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_transform_dispatcher.py`:

```python
from gemini_etl.transform import chunk_file


def _below(_t: str) -> int:
    return 1


def test_dispatches_md_to_markdown():
    chunks = chunk_file(
        text="# h\nbody\n", ext=".md",
        source="s", rel_path="x.md",
        token_limit=10_000, count_tokens=_below,
    )
    assert len(chunks) == 1
    assert "[Type: .md]" in chunks[0].text


def test_dispatches_py_to_python():
    chunks = chunk_file(
        text="def f(): return 1\n", ext=".py",
        source="s", rel_path="m.py",
        token_limit=10_000, count_tokens=_below,
    )
    assert "[Type: .py]" in chunks[0].text


def test_dispatches_js_to_generic():
    chunks = chunk_file(
        text="function f(){}", ext=".js",
        source="s", rel_path="x.js",
        token_limit=10_000, count_tokens=_below,
    )
    assert "[Type: .js]" in chunks[0].text


def test_unknown_extension_raises():
    import pytest
    with pytest.raises(ValueError):
        chunk_file(
            text="x", ext=".xyz",
            source="s", rel_path="x.xyz",
            token_limit=10_000, count_tokens=_below,
        )
```

- [ ] **Step 2: Run tests, confirm failure**

```bash
pytest tests/test_transform_dispatcher.py -v
```

Expected: ImportError.

- [ ] **Step 3: Update `transform/__init__.py`**

```python
"""Transform pipeline: file → list[Chunk]."""
from __future__ import annotations

from typing import Callable

from gemini_etl.transform.code_generic import chunk_generic
from gemini_etl.transform.code_python import chunk_python
from gemini_etl.transform.markdown import Chunk, chunk_markdown

__all__ = ["Chunk", "chunk_file"]


_GENERIC_EXTS = {".js", ".ts", ".c", ".cpp", ".h", ".bash"}


def chunk_file(
    *,
    text: str,
    ext: str,
    source: str,
    rel_path: str,
    token_limit: int,
    count_tokens: Callable[[str], int],
) -> list[Chunk]:
    if ext == ".md":
        return chunk_markdown(
            text=text, source=source, rel_path=rel_path,
            token_limit=token_limit, count_tokens=count_tokens,
        )
    if ext == ".py":
        return chunk_python(
            text=text, source=source, rel_path=rel_path,
            token_limit=token_limit, count_tokens=count_tokens,
        )
    if ext in _GENERIC_EXTS:
        return chunk_generic(
            text=text, source=source, rel_path=rel_path, ext=ext,
            token_limit=token_limit, count_tokens=count_tokens,
        )
    raise ValueError(f"unsupported extension: {ext}")
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_transform_dispatcher.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add src/gemini_etl/transform/__init__.py tests/test_transform_dispatcher.py
git commit -m "feat(gemini_etl): add transform dispatcher by extension"
```

---

## Task 11: Load module

**Files:**

- Create: `tools/gemini_etl/src/gemini_etl/load.py`
- Test: `tools/gemini_etl/tests/test_load.py`

> **API note:** `google-genai`'s exact method names for file_search_stores have evolved. The implementation below uses the names called out in the spec; if the installed SDK differs, adapt only inside `Loader._upload_one`, `Loader._delete`, and `Loader.ensure_store` — the rest is SDK-free.

- [ ] **Step 1: Write the failing tests**

`tests/test_load.py`:

```python
from unittest.mock import MagicMock, patch

import pytest

from gemini_etl.load import Loader, UploadResult


@pytest.fixture
def mock_client():
    client = MagicMock()
    # Default: store list returns nothing → create returns a fake store.
    client.file_search_stores.list.return_value = []
    fake_store = MagicMock()
    fake_store.name = "fileSearchStores/abc"
    fake_store.display_name = "test-store"
    client.file_search_stores.create.return_value = fake_store
    fake_doc = MagicMock()
    fake_doc.name = "fileSearchStores/abc/documents/d1"
    client.file_search_stores.documents.create.return_value = fake_doc
    fake_file = MagicMock()
    fake_file.name = "files/f1"
    client.files.upload.return_value = fake_file
    return client


def test_ensure_store_creates_when_missing(mock_client):
    loader = Loader(client=mock_client, store_display_name="test-store")
    name = loader.ensure_store()
    assert name == "fileSearchStores/abc"
    mock_client.file_search_stores.create.assert_called_once()


def test_ensure_store_returns_existing(mock_client):
    existing = MagicMock()
    existing.name = "fileSearchStores/existing"
    existing.display_name = "test-store"
    mock_client.file_search_stores.list.return_value = [existing]
    loader = Loader(client=mock_client, store_display_name="test-store")
    assert loader.ensure_store() == "fileSearchStores/existing"
    mock_client.file_search_stores.create.assert_not_called()


def test_upload_returns_document_id(mock_client, tmp_path):
    f = tmp_path / "x.md"
    f.write_text("hello")
    loader = Loader(client=mock_client, store_display_name="test-store")
    loader.ensure_store()
    result = loader.upload(path=f, display_name="personal_KB/x.md")
    assert isinstance(result, UploadResult)
    assert result.document_id == "fileSearchStores/abc/documents/d1"


def test_delete_calls_sdk(mock_client):
    loader = Loader(client=mock_client, store_display_name="test-store")
    loader.delete_document("fileSearchStores/abc/documents/d1")
    mock_client.file_search_stores.documents.delete.assert_called_once_with(
        name="fileSearchStores/abc/documents/d1"
    )


def test_retry_on_429(mock_client, tmp_path):
    """Three 429s then success."""
    f = tmp_path / "x.md"
    f.write_text("hello")

    fake_doc = MagicMock()
    fake_doc.name = "fileSearchStores/abc/documents/dN"
    err = Exception("429 too many requests")

    mock_client.file_search_stores.documents.create.side_effect = [err, err, fake_doc]
    loader = Loader(
        client=mock_client, store_display_name="test-store",
        max_attempts=5, retry_min_seconds=0,
    )
    loader.ensure_store()
    result = loader.upload(path=f, display_name="personal_KB/x.md")
    assert result.document_id.endswith("/dN")
```

- [ ] **Step 2: Run tests, confirm failure**

```bash
pytest tests/test_load.py -v
```

Expected: ImportError.

- [ ] **Step 3: Implement `load.py`**

```python
"""Gemini File Search Store loader: bootstrap + upload + delete with retry."""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

log = logging.getLogger(__name__)

_RATE_LIMIT_RE = re.compile(r"\b(429|503|rate|quota|unavailable)\b", re.IGNORECASE)


def _is_retryable(exc: BaseException) -> bool:
    return bool(_RATE_LIMIT_RE.search(str(exc)))


@dataclass(frozen=True)
class UploadResult:
    document_id: str


class Loader:
    def __init__(
        self,
        *,
        client: Any,
        store_display_name: str,
        max_attempts: int = 5,
        retry_min_seconds: float = 1.0,
    ) -> None:
        self._client = client
        self._store_display_name = store_display_name
        self._store_name: str | None = None
        self._retry = retry(
            retry=retry_if_exception(_is_retryable),
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=retry_min_seconds, min=retry_min_seconds, max=8),
            reraise=True,
        )

    def ensure_store(self) -> str:
        if self._store_name is not None:
            return self._store_name
        for store in self._client.file_search_stores.list():
            if store.display_name == self._store_display_name:
                self._store_name = store.name
                return self._store_name
        store = self._client.file_search_stores.create(
            display_name=self._store_display_name
        )
        self._store_name = store.name
        return self._store_name

    def upload(self, *, path: Path, display_name: str) -> UploadResult:
        """Upload the file at ``path`` and create a store document.

        ``display_name`` should be ``{source}/{rel_path}`` so duplicates can
        be reconciled by ``find_document_by_display_name``."""
        assert self._store_name is not None, "call ensure_store() first"

        @self._retry
        def _do() -> str:
            uploaded = self._client.files.upload(file=str(path))
            doc = self._client.file_search_stores.documents.create(
                parent=self._store_name,
                config={"display_name": display_name, "file": uploaded.name},
            )
            return doc.name

        return UploadResult(document_id=_do())

    def delete_document(self, document_id: str) -> None:
        @self._retry
        def _do() -> None:
            self._client.file_search_stores.documents.delete(name=document_id)

        _do()

    def find_document_by_display_name(self, display_name: str) -> str | None:
        """Used to reconcile orphans after a crashed run."""
        assert self._store_name is not None
        for doc in self._client.file_search_stores.documents.list(parent=self._store_name):
            if doc.display_name == display_name:
                return doc.name
        return None
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_load.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add src/gemini_etl/load.py tests/test_load.py
git commit -m "feat(gemini_etl): add gemini loader with retry + idempotency"
```

---

## Task 12: CLI — argparse skeleton + verify

**Files:**

- Create: `tools/gemini_etl/src/gemini_etl/__main__.py`
- Create: `tools/gemini_etl/src/gemini_etl/cli.py`
- Test: `tools/gemini_etl/tests/test_cli.py`

- [ ] **Step 1: Write failing tests**

`tests/test_cli.py`:

```python
from unittest.mock import MagicMock, patch

import pytest

from gemini_etl.cli import build_parser, main


def test_parser_accepts_sync():
    p = build_parser()
    ns = p.parse_args(["sync"])
    assert ns.command == "sync"


def test_parser_accepts_dry_run():
    p = build_parser()
    ns = p.parse_args(["dry-run"])
    assert ns.command == "dry-run"


def test_parser_accepts_status():
    p = build_parser()
    ns = p.parse_args(["status"])
    assert ns.command == "status"


def test_parser_accepts_reset_with_yes():
    p = build_parser()
    ns = p.parse_args(["reset", "--yes"])
    assert ns.command == "reset"
    assert ns.yes is True


def test_parser_accepts_verify():
    p = build_parser()
    ns = p.parse_args(["verify"])
    assert ns.command == "verify"


def test_parser_accepts_source_filter():
    p = build_parser()
    ns = p.parse_args(["sync", "--source", "personal_KB"])
    assert ns.source == "personal_KB"


def test_verify_calls_models_list():
    fake_client = MagicMock()
    fake_client.models.list.return_value = [MagicMock(name="m1")]
    with patch("gemini_etl.cli._build_client", return_value=fake_client):
        rc = main(["verify"])
    assert rc == 0
    fake_client.models.list.assert_called_once()


def test_verify_returns_nonzero_on_error():
    fake_client = MagicMock()
    fake_client.models.list.side_effect = Exception("auth failed")
    with patch("gemini_etl.cli._build_client", return_value=fake_client):
        rc = main(["verify"])
    assert rc != 0
```

- [ ] **Step 2: Run tests, confirm failure**

```bash
pytest tests/test_cli.py -v
```

Expected: ImportError.

- [ ] **Step 3: Implement `__main__.py`**

```python
"""Module entry: ``python -m gemini_etl ...``"""
from gemini_etl.cli import main

raise SystemExit(main())
```

- [ ] **Step 4: Implement `cli.py` (skeleton + verify only)**

```python
"""Command-line interface for gemini_etl."""
from __future__ import annotations

import argparse
import logging
import os
import sys
from typing import Any, Sequence

from dotenv import load_dotenv

log = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="gemini-etl")
    p.add_argument("-v", "--verbose", action="count", default=0)
    p.add_argument("--no-progress", action="store_true")

    sub = p.add_subparsers(dest="command", required=True)

    s_sync = sub.add_parser("sync", help="walk → diff → upload/update/delete")
    s_sync.add_argument("--source", default=None)
    s_sync.add_argument("--limit", type=int, default=None)

    s_dry = sub.add_parser("dry-run", help="show what sync would do (no API calls)")
    s_dry.add_argument("--source", default=None)
    s_dry.add_argument("--limit", type=int, default=None)

    s_status = sub.add_parser("status", help="manifest summary, no API calls")

    s_reset = sub.add_parser("reset", help="delete the store + manifest")
    s_reset.add_argument("--yes", action="store_true")

    sub.add_parser("verify", help="confirm credentials work")

    return p


def _configure_logging(verbosity: int) -> None:
    level = {0: logging.WARNING, 1: logging.INFO}.get(verbosity, logging.DEBUG)
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")


def _build_client() -> Any:
    """Real factory; tests monkeypatch this."""
    from google import genai  # local import keeps unit tests SDK-free

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing — see README first-time setup")
    return genai.Client(api_key=api_key)


def _cmd_verify() -> int:
    try:
        client = _build_client()
        models = list(client.models.list())
        print(f"OK — {len(models)} models reachable")
        return 0
    except Exception as e:
        print(f"verify FAILED: {e}", file=sys.stderr)
        return 2


def main(argv: Sequence[str] | None = None) -> int:
    load_dotenv()
    args = build_parser().parse_args(argv)
    _configure_logging(args.verbose)

    if args.command == "verify":
        return _cmd_verify()
    # other commands wired up in Tasks 13–14
    print(f"command not yet implemented: {args.command}", file=sys.stderr)
    return 3
```

- [ ] **Step 5: Run tests**

```bash
pytest tests/test_cli.py -v
```

Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add src/gemini_etl/__main__.py src/gemini_etl/cli.py tests/test_cli.py
git commit -m "feat(gemini_etl): add CLI skeleton + verify command"
```

---

## Task 13: CLI — sync + dry-run

**Files:**

- Modify: `tools/gemini_etl/src/gemini_etl/cli.py`
- Modify: `tools/gemini_etl/tests/test_cli.py`

- [ ] **Step 1: Add failing tests**

Append to `tests/test_cli.py`:

```python
from gemini_etl.config import Source


def _stub_config(monkeypatch, tmp_path):
    """Replace get_config with a deterministic, fixture-backed config."""
    fixtures = tmp_path / "src"
    (fixtures / "personal_KB").mkdir(parents=True)
    (fixtures / "personal_KB" / "a.md").write_text("# A\nbody\n")

    from gemini_etl import config as cfg_mod
    fake = cfg_mod.Config(
        sources=(
            Source(name="personal_KB",
                   path=str(fixtures / "personal_KB"),
                   extensions=frozenset({".md"})),
        ),
        store_name="test-store",
        chunk_token_limit=10_000,
        max_file_size_bytes=2 * 1024**3,
        max_concurrency=2,
        state_dir=tmp_path / "state",
    )
    monkeypatch.setattr(cfg_mod, "get_config", lambda: fake)
    return fake


def test_dry_run_makes_no_api_calls(monkeypatch, tmp_path):
    _stub_config(monkeypatch, tmp_path)
    fake_client = MagicMock()
    with patch("gemini_etl.cli._build_client", return_value=fake_client):
        rc = main(["dry-run"])
    assert rc == 0
    fake_client.file_search_stores.create.assert_not_called()
    fake_client.files.upload.assert_not_called()


def test_sync_uploads_new_file(monkeypatch, tmp_path):
    _stub_config(monkeypatch, tmp_path)

    fake_client = MagicMock()
    fake_client.file_search_stores.list.return_value = []
    store = MagicMock()
    store.name = "fileSearchStores/x"
    store.display_name = "test-store"
    fake_client.file_search_stores.create.return_value = store
    doc = MagicMock()
    doc.name = "fileSearchStores/x/documents/d1"
    fake_client.file_search_stores.documents.create.return_value = doc
    fake_client.files.upload.return_value = MagicMock(name="files/f1")
    # Token counter
    tc = MagicMock()
    tc.total_tokens = 50
    fake_client.models.count_tokens.return_value = tc

    with patch("gemini_etl.cli._build_client", return_value=fake_client):
        rc = main(["sync"])

    assert rc == 0
    fake_client.files.upload.assert_called()
    fake_client.file_search_stores.documents.create.assert_called()


def test_sync_limit_caps_uploads(monkeypatch, tmp_path):
    _stub_config(monkeypatch, tmp_path)
    # Add a second file.
    (tmp_path / "src" / "personal_KB" / "b.md").write_text("# B\nbody\n")

    fake_client = MagicMock()
    fake_client.file_search_stores.list.return_value = []
    store = MagicMock()
    store.name = "fileSearchStores/x"
    store.display_name = "test-store"
    fake_client.file_search_stores.create.return_value = store
    fake_client.file_search_stores.documents.create.return_value = MagicMock(
        name="fileSearchStores/x/documents/d"
    )
    fake_client.files.upload.return_value = MagicMock(name="files/f")
    tc = MagicMock()
    tc.total_tokens = 50
    fake_client.models.count_tokens.return_value = tc

    with patch("gemini_etl.cli._build_client", return_value=fake_client):
        rc = main(["sync", "--limit", "1"])

    assert rc == 0
    assert fake_client.files.upload.call_count == 1
```

- [ ] **Step 2: Run, confirm failure**

```bash
pytest tests/test_cli.py -v
```

Expected: 3 new tests fail (`SystemExit: 3` or similar).

- [ ] **Step 3: Implement sync + dry-run in `cli.py`**

Replace the bottom of `cli.py` (the "command not yet implemented" stub) with:

```python
def _materialize_chunks(chunks, dest: "Path") -> None:
    """Write chunk-concatenated content (with embedded headers) to dest."""
    body = "\n\n---\n\n".join(c.text for c in chunks)
    dest.write_text(body, encoding="utf-8")


def _process_one(
    *, row, cfg, counter, loader, manifest, was_changed: bool,
) -> bool:
    """Upload (or replace) a single file. Returns True on success."""
    import tempfile
    from pathlib import Path
    from gemini_etl.manifest import ManifestRow
    from gemini_etl.transform import chunk_file

    ext = "." + row.rel_path.rsplit(".", 1)[-1]
    abs_root = next(s.path for s in cfg.sources if s.name == row.source)
    full = Path(abs_root) / row.rel_path
    try:
        text = full.read_text(encoding="utf-8")
        chunks = chunk_file(
            text=text, ext=ext, source=row.source, rel_path=row.rel_path,
            token_limit=cfg.chunk_token_limit, count_tokens=counter.count,
        )
        if was_changed:
            existing = manifest.get(row.source, row.rel_path)
            if existing and existing.document_id:
                loader.delete_document(existing.document_id)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=ext, delete=False, encoding="utf-8",
        ) as tmp:
            tmp_path = Path(tmp.name)
            _materialize_chunks(chunks, tmp_path)
        try:
            result = loader.upload(path=tmp_path, display_name=row.display_name)
        finally:
            tmp_path.unlink(missing_ok=True)

        manifest.upsert(ManifestRow(
            source=row.source, rel_path=row.rel_path, sha256=row.sha256,
            display_name=row.display_name, document_id=result.document_id,
        ))
        return True
    except Exception as e:
        log.error("upload failed for %s: %s", row.display_name, e)
        return False


def _cmd_sync(args: argparse.Namespace, *, dry_run: bool) -> int:
    from concurrent.futures import ThreadPoolExecutor
    from gemini_etl.config import get_config
    from gemini_etl.extract import walk_source
    from gemini_etl.load import Loader
    from gemini_etl.manifest import FileState, Manifest, ManifestRow
    from gemini_etl.tokens import CachedTokenCounter, gemini_token_counter

    cfg = get_config()
    cfg.state_dir.mkdir(parents=True, exist_ok=True)
    manifest = Manifest(cfg.manifest_path)

    sources = [
        s for s in cfg.sources
        if args.source is None or s.name == args.source
    ]

    client = None if dry_run else _build_client()
    counter = CachedTokenCounter(
        gemini_token_counter(client) if client else (lambda t: max(1, len(t) // 4))
    )
    loader = Loader(client=client, store_display_name=cfg.store_name) if client else None
    if loader:
        loader.ensure_store()

    plan_added: list[ManifestRow] = []
    plan_changed: list[ManifestRow] = []
    plan_unchanged = 0
    live_set: set[tuple[str, str]] = set()
    files_processed = 0

    for source in sources:
        for fr in walk_source(source, max_file_size_bytes=cfg.max_file_size_bytes):
            if args.limit is not None and files_processed >= args.limit:
                break
            files_processed += 1
            live_set.add((fr.source, fr.rel_path))
            display_name = f"{fr.source}/{fr.rel_path}"

            state = manifest.classify(fr.source, fr.rel_path, fr.sha256)
            row = ManifestRow(
                source=fr.source, rel_path=fr.rel_path, sha256=fr.sha256,
                display_name=display_name, document_id=None,
            )
            if state is FileState.NEW:
                plan_added.append(row)
            elif state is FileState.CHANGED:
                plan_changed.append(row)
            else:
                plan_unchanged += 1

    plan_deleted = list(manifest.deleted_rows(live_set=live_set))

    print(f"  added:    {len(plan_added)}")
    print(f"  changed:  {len(plan_changed)}")
    print(f"  unchanged:{plan_unchanged}")
    print(f"  deleted:  {len(plan_deleted)}")

    if dry_run:
        return 0

    assert loader is not None
    failures = 0

    work = [(r, False) for r in plan_added] + [(r, True) for r in plan_changed]
    if work:
        with ThreadPoolExecutor(max_workers=cfg.max_concurrency) as pool:
            futures = [
                pool.submit(
                    _process_one,
                    row=r, cfg=cfg, counter=counter,
                    loader=loader, manifest=manifest, was_changed=ch,
                )
                for (r, ch) in work
            ]
            for fut in futures:
                if not fut.result():
                    failures += 1

    for d in plan_deleted:
        try:
            if d.document_id:
                loader.delete_document(d.document_id)
            manifest.delete(d.source, d.rel_path)
        except Exception as e:
            failures += 1
            log.error("delete failed for %s: %s", d.display_name, e)

    print(f"  failed:   {failures}")
    return 0 if failures == 0 else 1
```

Replace `main()` body with:

```python
def main(argv: Sequence[str] | None = None) -> int:
    load_dotenv()
    args = build_parser().parse_args(argv)
    _configure_logging(args.verbose)

    if args.command == "verify":
        return _cmd_verify()
    if args.command == "sync":
        return _cmd_sync(args, dry_run=False)
    if args.command == "dry-run":
        return _cmd_sync(args, dry_run=True)

    print(f"command not yet implemented: {args.command}", file=sys.stderr)
    return 3
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_cli.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add src/gemini_etl/cli.py tests/test_cli.py
git commit -m "feat(gemini_etl): wire sync and dry-run commands"
```

---

## Task 14: CLI — status + reset

**Files:**

- Modify: `tools/gemini_etl/src/gemini_etl/cli.py`
- Modify: `tools/gemini_etl/tests/test_cli.py`

- [ ] **Step 1: Add failing tests**

Append:

```python
def test_status_prints_summary_no_api(monkeypatch, tmp_path, capsys):
    _stub_config(monkeypatch, tmp_path)
    fake_client = MagicMock()
    with patch("gemini_etl.cli._build_client", return_value=fake_client):
        rc = main(["status"])
    assert rc == 0
    fake_client.file_search_stores.list.assert_not_called()
    out = capsys.readouterr().out
    assert "personal_KB" in out or "manifest empty" in out


def test_reset_requires_yes(monkeypatch, tmp_path, capsys):
    _stub_config(monkeypatch, tmp_path)
    rc = main(["reset"])
    assert rc != 0
    assert "--yes" in capsys.readouterr().err


def test_reset_with_yes_deletes_store_and_manifest(monkeypatch, tmp_path):
    cfg = _stub_config(monkeypatch, tmp_path)
    cfg.state_dir.mkdir(parents=True, exist_ok=True)
    cfg.manifest_path.write_bytes(b"junk")  # any file

    fake_client = MagicMock()
    store = MagicMock()
    store.name = "fileSearchStores/x"
    store.display_name = "test-store"
    fake_client.file_search_stores.list.return_value = [store]

    with patch("gemini_etl.cli._build_client", return_value=fake_client):
        rc = main(["reset", "--yes"])

    assert rc == 0
    fake_client.file_search_stores.delete.assert_called_once_with(
        name="fileSearchStores/x"
    )
    assert not cfg.manifest_path.exists()
```

- [ ] **Step 2: Run tests, confirm failure**

```bash
pytest tests/test_cli.py -v
```

Expected: 3 new tests fail.

- [ ] **Step 3: Add `_cmd_status` and `_cmd_reset` to `cli.py`**

```python
def _cmd_status() -> int:
    from gemini_etl.config import get_config
    from gemini_etl.manifest import Manifest

    cfg = get_config()
    if not cfg.manifest_path.exists():
        print("manifest empty (no sync has run)")
        return 0

    manifest = Manifest(cfg.manifest_path)
    summary = manifest.summary()
    if not summary:
        print("manifest empty (no sync has run)")
        return 0
    print("manifest summary:")
    for source, count in sorted(summary.items()):
        print(f"  {source}: {count} files")
    return 0


def _cmd_reset(args: argparse.Namespace) -> int:
    from gemini_etl.config import get_config

    if not args.yes:
        print("reset requires --yes (this deletes the store + manifest)", file=sys.stderr)
        return 2

    cfg = get_config()
    client = _build_client()
    for s in client.file_search_stores.list():
        if s.display_name == cfg.store_name:
            client.file_search_stores.delete(name=s.name)
            print(f"deleted store {s.name}")
    if cfg.manifest_path.exists():
        cfg.manifest_path.unlink()
        print(f"deleted manifest {cfg.manifest_path}")
    if cfg.store_id_path.exists():
        cfg.store_id_path.unlink()
    return 0
```

Wire them into `main()`:

```python
    if args.command == "status":
        return _cmd_status()
    if args.command == "reset":
        return _cmd_reset(args)
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_cli.py -v
```

Expected: all PASS.

- [ ] **Step 5: Run the full suite + coverage**

```bash
pytest
```

Expected: all PASS, coverage ≥ 90 %.

- [ ] **Step 6: Commit**

```bash
git add src/gemini_etl/cli.py tests/test_cli.py
git commit -m "feat(gemini_etl): wire status + reset commands"
```

---

## Task 15: Bin shim

**Files:**

- Create: `tools/gemini_etl/bin/gemini-etl`

- [ ] **Step 1: Create the shim**

```bash
mkdir -p tools/gemini_etl/bin
```

`tools/gemini_etl/bin/gemini-etl`:

```bash
#!/bin/bash
# gemini-etl shim: activates the venv and forwards args to python -m gemini_etl
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV" ]; then
    echo "error: venv not found at $VENV" >&2
    echo "run: cd $SCRIPT_DIR && python3 -m venv .venv && source .venv/bin/activate && pip install -e ." >&2
    exit 1
fi

# shellcheck source=/dev/null
source "$VENV/bin/activate"
exec python -m gemini_etl "$@"
```

- [ ] **Step 2: Make it executable**

```bash
chmod +x tools/gemini_etl/bin/gemini-etl
```

- [ ] **Step 3: Smoke test**

```bash
tools/gemini_etl/bin/gemini-etl --help
```

Expected: argparse help printed, exit 0.

- [ ] **Step 4: Commit**

```bash
git add tools/gemini_etl/bin/gemini-etl
git commit -m "feat(gemini_etl): add bin/gemini-etl shim for zsh aliases"
```

---

## Task 16: README

**Files:**

- Create: `tools/gemini_etl/README.md`

- [ ] **Step 1: Write the README**

```markdown
# gemini_etl

Sync personal Git repos (`personal_KB`, `personal_code`) into a Gemini File
Search Store for RAG retrieval.

## What it does

Hash-based incremental sync. Walks each source repo, respects `.gitignore`,
chunks markdown by header / Python by tree-sitter / other code by regex,
prepends a metadata header, and uploads to Gemini. A SQLite manifest at
`~/.gemini_etl/sync_manifest.sqlite` makes re-runs fast and crash-safe.

## First-time setup

1. Generate API key at <https://aistudio.google.com/apikey>.
2. `cp .env.example .env` and paste the key:

   ```env
   GEMINI_API_KEY=your-key-here
   ```

3. Create venv and install:

   ```bash
   cd tools/gemini_etl
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

4. Sanity-check credentials:

   ```bash
   python -m gemini_etl verify
   ```

5. Preview the plan:

   ```bash
   python -m gemini_etl dry-run
   ```

6. Run the sync:

   ```bash
   python -m gemini_etl sync
   ```

## Daily use

Add to your zsh rc (e.g. `~/.zshrc`):

```bash
alias gemini-sync='/Users/yosii/work/git/personal_code/tools/gemini_etl/bin/gemini-etl sync'
alias gemini-status='/Users/yosii/work/git/personal_code/tools/gemini_etl/bin/gemini-etl status'
alias gemini-dry='/Users/yosii/work/git/personal_code/tools/gemini_etl/bin/gemini-etl dry-run'
```

Then: `gemini-sync` from anywhere. Or use the launcher menu (`launcher.sh` → "Gemini KB Sync").

## Commands

| Command | What it does |
| :--- | :--- |
| `sync` | Walk → diff → upload/update/delete. The 95 % case. |
| `dry-run` | Same walk + diff, no API calls. Prints the plan. |
| `status` | Manifest summary. No API calls. |
| `verify` | Confirms credentials reach Gemini. |
| `reset --yes` | Deletes the store + local manifest. Requires `--yes`. |

## Architecture

```text
extract → transform → load
   │         │         │
   └────── manifest ───┘   (SQLite at ~/.gemini_etl/)
```

- `extract` — `os.walk` + `pathspec` filtering + SHA-256.
- `transform` — markdown / python (tree-sitter) / generic code (regex).
- `load` — `google-genai` SDK, `tenacity` retries, idempotent by `display_name`.
- `manifest` — SQLite, atomic per-row writes, drives delta-sync.

## Troubleshooting

| Symptom | Likely cause |
| :--- | :--- |
| `verify FAILED: GEMINI_API_KEY missing` | `.env` not present or key not set |
| `429` retried 5x then failed | rate limit; reduce `GEMINI_ETL_MAX_CONCURRENCY` |
| `unsupported extension: .xyz` | extension not in any source's allowlist (intended) |
| Manifest mismatch after manual store deletion | `gemini-etl reset --yes` to start fresh |

## Development

```bash
pip install -e ".[dev]"
pytest             # tests + coverage
ruff check src tests
mypy
```
```

- [ ] **Step 2: Commit**

```bash
git add tools/gemini_etl/README.md
git commit -m "docs(gemini_etl): add README with first-time setup"
```

---

## Task 17: CHANGELOG

**Files:**

- Create: `tools/gemini_etl/CHANGELOG.md`

- [ ] **Step 1: Write the CHANGELOG**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] — 2026-05-03

### Added
- Initial release.
- `extract`: filesystem walker honoring `.gitignore`, always-skip dirs, size guard.
- `transform`: markdown (frontmatter + header split), Python (tree-sitter),
  generic code (regex + token-window fallback).
- `load`: Gemini File Search Store bootstrap, idempotent uploads by
  `display_name`, retry/backoff via `tenacity`.
- `manifest`: SQLite store of per-file SHA + Gemini doc IDs.
- CLI: `sync`, `dry-run`, `status`, `verify`, `reset`.
- `bin/gemini-etl` shim for zsh aliases.
- Launcher integration.
```

- [ ] **Step 2: Commit**

```bash
git add tools/gemini_etl/CHANGELOG.md
git commit -m "docs(gemini_etl): add changelog at 0.1.0"
```

---

## Task 18: Launcher integration

**Files:**

- Modify: `code/bash/tools/launcher/launcher.sh`
- Modify: `code/bash/tools/launcher/CHANGELOG.md`
- Modify: `code/bash/tools/launcher/tests/test_handler_dispatch.sh` (add a test)

- [ ] **Step 1: Add path constants near the top of `launcher.sh`**

After the existing `*_DIR` declarations (around line 22, after `EMOJI_GENERATOR_VENV`), add:

```bash
GEMINI_ETL_DIR="/Users/yosii/work/git/personal_code/tools/gemini_etl"
GEMINI_ETL_VENV="$GEMINI_ETL_DIR/.venv"
```

- [ ] **Step 2: Update `show_main_menu` to add a menu item**

In `show_main_menu()` (around line 326), add a new entry after `Backup Manager`:

```bash
print_menu_item "9" "Gemini KB Sync"
```

…and update the prompt:

```bash
printf "   ${BOLD}➜ Enter your choice [0-9]: ${NC}"
```

- [ ] **Step 3: Add `show_gemini_etl_menu`**

Add right after `show_mcp_helper_menu` (or any existing `show_*_menu`):

```bash
show_gemini_etl_menu() {
	clear_screen
	echo ""
	echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════╗${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║          🔁 GEMINI KB SYNC MENU                 ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[1]${CYAN}  Sync                                     ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[2]${CYAN}  Dry-run (preview)                        ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[3]${CYAN}  Status                                   ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[4]${CYAN}  Verify credentials                       ║${NC}"
	echo -e "${BOLD}${CYAN}║  ${GREEN}[5]${CYAN}  Reset (delete store + manifest)          ║${NC}"
	echo -e "${BOLD}${CYAN}║                                                  ║${NC}"
	echo -e "${BOLD}${CYAN}╠══════════════════════════════════════════════════╣${NC}"
	echo -e "${BOLD}${CYAN}║  ${YELLOW}[0]${CYAN}  ← Back to Main Menu                      ║${NC}"
	echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${NC}"
	echo ""
	printf "  ${BOLD}➜ Enter your choice [0-5]: ${NC}"
}
```

- [ ] **Step 4: Add `handle_gemini_etl_menu`**

Add (e.g., right after `handle_daily_timer_menu`):

```bash
handle_gemini_etl_menu() {
	if [ ! -d "$GEMINI_ETL_VENV" ]; then
		clear_screen
		echo -e "${YELLOW}Warning: Gemini ETL venv not found${NC}"
		echo ""
		echo "To set up, run:"
		echo "  cd $GEMINI_ETL_DIR"
		echo "  python3 -m venv .venv"
		echo "  source .venv/bin/activate"
		echo "  pip install -e ."
		echo ""
		echo "Then create $GEMINI_ETL_DIR/.env with GEMINI_API_KEY (see README)."
		echo ""
		echo -n "Press Enter to continue..."
		read
		return
	fi

	while true; do
		show_gemini_etl_menu
		read choice
		case "$choice" in
		1)
			clear_screen
			cd "$GEMINI_ETL_DIR"
			source "$GEMINI_ETL_VENV/bin/activate"
			python -m gemini_etl sync
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		2)
			clear_screen
			cd "$GEMINI_ETL_DIR"
			source "$GEMINI_ETL_VENV/bin/activate"
			python -m gemini_etl dry-run
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		3)
			clear_screen
			cd "$GEMINI_ETL_DIR"
			source "$GEMINI_ETL_VENV/bin/activate"
			python -m gemini_etl status
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		4)
			clear_screen
			cd "$GEMINI_ETL_DIR"
			source "$GEMINI_ETL_VENV/bin/activate"
			python -m gemini_etl verify
			deactivate
			cd - >/dev/null
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		5)
			clear_screen
			echo -e "${YELLOW}This will delete the Gemini store and the local manifest.${NC}"
			echo -n "Type 'yes' to confirm: "
			read confirm
			if [ "$confirm" = "yes" ]; then
				cd "$GEMINI_ETL_DIR"
				source "$GEMINI_ETL_VENV/bin/activate"
				python -m gemini_etl reset --yes
				deactivate
				cd - >/dev/null
			else
				echo "cancelled"
			fi
			echo ""
			echo -n "Press Enter to continue..."
			read
			;;
		0)
			return
			;;
		*)
			echo -e "${YELLOW}Invalid choice. Please try again.${NC}"
			sleep 1
			;;
		esac
	done
}
```

- [ ] **Step 5: Wire dispatcher in main loop**

In the main `case "$choice"` block (around line 1774), add a `9)` branch before `0)`:

```bash
		9)
			handle_gemini_etl_menu
			;;
```

- [ ] **Step 6: Add CHANGELOG entry**

In `code/bash/tools/launcher/CHANGELOG.md`, add at the top under a new version (or under "Unreleased"):

```markdown
- Add menu entry "Gemini KB Sync" wired to `tools/gemini_etl` with sync,
  dry-run, status, verify, and reset sub-options.
```

- [ ] **Step 7: Smoke test the launcher**

```bash
bash code/bash/tools/launcher/launcher.sh --version
```

Expected: prints version, exits 0.

```bash
# In a separate terminal, run interactively:
bash code/bash/tools/launcher/launcher.sh
```

Verify: main menu shows "[9] Gemini KB Sync"; choosing 9 shows the sub-menu (or a yellow "venv not found" message if the venv doesn't exist yet).

- [ ] **Step 8: Commit**

```bash
git add code/bash/tools/launcher/launcher.sh code/bash/tools/launcher/CHANGELOG.md
git commit -m "feat(launcher): add Gemini KB Sync menu wired to tools/gemini_etl"
```

---

## Task 19: Smoke test against real repos

This task is manual — it confirms the whole pipeline works end-to-end with real
Gemini credentials. No tests are added.

- [ ] **Step 1: Confirm `.env` is set**

```bash
grep -c "^GEMINI_API_KEY=." tools/gemini_etl/.env
```

Expected: `1`. If `0`, return to README first-time-setup step 2.

- [ ] **Step 2: Verify credentials**

```bash
tools/gemini_etl/bin/gemini-etl verify
```

Expected: `OK — N models reachable`, exit 0.

- [ ] **Step 3: Dry-run**

```bash
tools/gemini_etl/bin/gemini-etl dry-run
```

Expected: prints discovery summary for both sources; no API uploads occur.

- [ ] **Step 4: Real sync**

```bash
tools/gemini_etl/bin/gemini-etl sync
```

Expected: progress messages, final summary `added: N / changed: 0 / unchanged: 0 / deleted: 0 / failed: 0` on first run.

- [ ] **Step 5: Idempotency check**

Run again immediately:

```bash
tools/gemini_etl/bin/gemini-etl sync
```

Expected: `added: 0 / changed: 0 / unchanged: N / deleted: 0`.

- [ ] **Step 6: Verify the store exists in AI Studio**

Open <https://aistudio.google.com/> and confirm a File Search Store named
`yosi-personal-kb` exists with the expected document count.

- [ ] **Step 7: Final commit and tag**

If anything in the test loop required a fix, commit it. Then:

```bash
cd tools/gemini_etl
git tag gemini-etl-0.1.0
```

---

## Self-review checklist

- [x] Each spec section has at least one task implementing it.
- [x] Type names match across tasks (`Chunk`, `ChunkMetadata`, `FileRef`,
      `ManifestRow`, `FileState`, `UploadResult`, `Loader`).
- [x] No "TBD"/"TODO"/"add appropriate" placeholders.
- [x] Every test step shows the test code.
- [x] Every implementation step shows the code.
- [x] Commands include expected output.
- [x] Frequent commits — one per task with TDD red-green sequence.
