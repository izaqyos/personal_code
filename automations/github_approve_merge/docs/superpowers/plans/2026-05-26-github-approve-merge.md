# `github_approve_merge` V1 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Playwright Python CLI that approves + merges 1..N GitHub PRs in a batch, with JSONL logs, checkpoint screenshots, 10-day lazy-delete retention, and resume-after-interrupt via a per-batch `state.jsonl`.

**Architecture:** Layered: `cli` → `runner` (batch loop, state, signal handler) → `actions.process_pr` (per-PR flow) → `pages/` Page Objects (PRPage, FilesPage with central `selectors.py`) → `browser` (async_playwright lifecycle). Shared modules: `url`, `input_sources`, `pr_state`, `retention`, `logging_setup`, `screenshots`, `auth`, `config`.

**Tech Stack:** Python 3.12, `uv` for dep management, `playwright` (async), `pytest` + `pytest-asyncio`. Stdlib for everything else (no `rich`, no `structlog`).

**Companion spec:** `docs/superpowers/specs/2026-05-26-github-approve-merge-design.md`. The plan implements §1–§13 of the spec.

---

## File structure (locked from spec §5)

| File | Purpose |
|---|---|
| `src/github_approve_merge/__init__.py` | `__version__` |
| `src/github_approve_merge/__main__.py` | `python -m github_approve_merge` entry |
| `src/github_approve_merge/cli.py` | argparse, subcommands `auth`, `run`, `gc` |
| `src/github_approve_merge/config.py` | Default paths, constants |
| `src/github_approve_merge/url.py` | `PRRef`, `parse_pr_url` |
| `src/github_approve_merge/input_sources.py` | `collect_urls` (args + file + stdin, dedupe) |
| `src/github_approve_merge/auth.py` | `storage_state.json` load/save + login flow |
| `src/github_approve_merge/browser.py` | `async_playwright` lifecycle, context factory |
| `src/github_approve_merge/pages/selectors.py` | Named selector constants |
| `src/github_approve_merge/pages/pr_page.py` | `PRPage` |
| `src/github_approve_merge/pages/files_page.py` | `FilesPage` |
| `src/github_approve_merge/pr_state.py` | `PRState`, `StateFlag`, `detect_state` |
| `src/github_approve_merge/actions.py` | `process_pr`, `STATUS_TO_EXIT_CLASS` |
| `src/github_approve_merge/runner.py` | `Runner` (batch loop, state.jsonl, signal handler, summary) |
| `src/github_approve_merge/logging_setup.py` | `JSONFormatter`, `ColorConsoleHandler`, `make_run_logger` |
| `src/github_approve_merge/screenshots.py` | `capture(page, ctx, label)` |
| `src/github_approve_merge/retention.py` | `sweep(logs_root, max_age_days, skip)` |
| `tests/conftest.py` | Browser fixture, PYTEST_LIVE gate |
| `tests/unit/test_*.py` | Pure-logic tests |
| `tests/pages/test_*.py` | Page Object tests against `file://` fixtures |
| `tests/fixtures/html/*.html` | 13 fixtures (spec §10) |
| `tests/live/test_smoke.py` | Opt-in live test (`PYTEST_LIVE=1`) |
| `scripts/refresh_fixtures.py` | Helper to re-snapshot HTML fixtures |
| `pyproject.toml` | uv project, deps, console_scripts |
| `README.md` | Usage docs |
| `CHANGELOG.md` | Keep-a-Changelog |

---

## Phase 0 — Scaffolding

### Task 0: Initialize project, deps, and CI-ready test command

**Files:**
- Create: `pyproject.toml`
- Create: `.python-version`
- Create: `src/github_approve_merge/__init__.py`
- Create: `src/github_approve_merge/__main__.py`
- Create: `tests/__init__.py`
- Create: `tests/unit/__init__.py`
- Create: `tests/pages/__init__.py`
- Create: `tests/live/__init__.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: Write `.python-version`**

```
3.12
```

- [ ] **Step 2: Write `pyproject.toml`**

```toml
[project]
name = "github-approve-merge"
version = "0.1.0"
description = "Playwright CLI that approves and merges GitHub PRs in batch."
requires-python = ">=3.12"
authors = [{name = "Yosi Izaq", email = "me@example.com"}]
dependencies = [
    "playwright>=1.44.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
]

[project.scripts]
gh-approve-merge = "github_approve_merge.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/github_approve_merge"]

[tool.pytest.ini_options]
asyncio_mode = "strict"
markers = [
    "live: requires PYTEST_LIVE=1 and a real PR URL (not run in CI)",
]
addopts = "-ra --strict-markers"
testpaths = ["tests"]
```

- [ ] **Step 3: Write `src/github_approve_merge/__init__.py`**

```python
__version__ = "0.1.0"
```

- [ ] **Step 4: Write `src/github_approve_merge/__main__.py`**

```python
from github_approve_merge.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Write empty package + test `__init__.py` files**

```python
# src/github_approve_merge/pages/__init__.py
```

```python
# tests/__init__.py
```

```python
# tests/unit/__init__.py
```

```python
# tests/pages/__init__.py
```

```python
# tests/live/__init__.py
```

- [ ] **Step 6: Write `tests/conftest.py` (minimal — browser fixture added in Task 8)**

```python
import os
import pytest


def pytest_collection_modifyitems(config, items):
    if os.environ.get("PYTEST_LIVE") == "1":
        return
    skip_live = pytest.mark.skip(reason="PYTEST_LIVE=1 not set")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)
```

- [ ] **Step 7: Install deps and verify the package imports**

Run:
```bash
cd /Users/yosii/work/git/personal_code/automations/github_approve_merge
uv venv
uv pip install -e ".[dev]"
uv run python -c "import github_approve_merge; print(github_approve_merge.__version__)"
```

Expected output: `0.1.0`.

- [ ] **Step 8: Install Playwright browsers**

Run:
```bash
uv run playwright install chromium
```

Expected: chromium downloaded successfully.

- [ ] **Step 9: Verify pytest collects nothing yet (no errors)**

Run:
```bash
uv run pytest
```

Expected: `no tests ran` exit 5 (not an error — just empty).

- [ ] **Step 10: Commit**

```bash
git add automations/github_approve_merge
git commit -m "feat(github_approve_merge): scaffold project (uv, pytest, playwright)"
```

---

## Phase 1 — Pure-Python units

Each task here follows strict TDD: failing test → minimal impl → passing test → commit.

### Task 1: URL parsing — `url.py`

**Files:**
- Create: `src/github_approve_merge/url.py`
- Create: `tests/unit/test_url.py`

- [ ] **Step 1: Write failing tests for `parse_pr_url` and `PRRef.__str__`**

Create `tests/unit/test_url.py`:

```python
import pytest

from github_approve_merge.url import PRRef, parse_pr_url


class TestParsePrUrl:
    def test_canonical_url(self):
        assert parse_pr_url("https://github.com/acme-org/widgets-service/pull/561") == PRRef(
            owner="acme-org", repo="widgets-service", number=561
        )

    def test_trailing_slash(self):
        assert parse_pr_url("https://github.com/owner/repo/pull/1/") == PRRef("owner", "repo", 1)

    def test_files_suffix(self):
        assert parse_pr_url("https://github.com/owner/repo/pull/1/files") == PRRef("owner", "repo", 1)

    def test_commits_suffix(self):
        assert parse_pr_url("https://github.com/owner/repo/pull/1/commits") == PRRef("owner", "repo", 1)

    def test_fragment_suffix(self):
        assert parse_pr_url("https://github.com/owner/repo/pull/1#discussion_r123") == PRRef("owner", "repo", 1)

    def test_query_suffix(self):
        assert parse_pr_url("https://github.com/owner/repo/pull/1?diff=split") == PRRef("owner", "repo", 1)

    @pytest.mark.parametrize("bad_url", [
        "",
        "not a url",
        "ftp://github.com/owner/repo/pull/1",
        "http://github.com/owner/repo/pull/1",                   # http not https
        "https://example.com/owner/repo/pull/1",                 # wrong host
        "https://ghe.internal.example/owner/repo/pull/1",        # GHES, out of V1 scope
        "https://github.com/owner/repo/issues/1",                # not a PR
        "https://github.com/owner/repo/pull/abc",                # non-numeric
        "https://github.com/owner/repo/pull/",                   # no number
        "https://github.com/owner/repo/pulls/1",                 # plural
        "https://github.com/owner/repo",                         # not a PR url
    ])
    def test_bad_url_raises_value_error(self, bad_url):
        with pytest.raises(ValueError):
            parse_pr_url(bad_url)


class TestPrRefStr:
    def test_str_format(self):
        assert str(PRRef("acme-org", "widgets-service", 561)) == \
            "acme-org/widgets-service#561"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/unit/test_url.py -v
```

Expected: all fail with `ModuleNotFoundError: No module named 'github_approve_merge.url'`.

- [ ] **Step 3: Implement `url.py`**

Create `src/github_approve_merge/url.py`:

```python
from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse

_PR_PATH_RE = re.compile(r"^/(?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/(?P<number>\d+)(?:/(?:files|commits))?/?$")


@dataclass(frozen=True, slots=True)
class PRRef:
    owner: str
    repo: str
    number: int

    def __str__(self) -> str:
        return f"{self.owner}/{self.repo}#{self.number}"


def parse_pr_url(url: str) -> PRRef:
    """Parse a github.com PR URL into a PRRef.

    Accepts canonical forms and the /files, /commits suffixes, plus trailing
    slashes, query strings, and fragments. Rejects non-github.com hosts (V1
    is github.com only) and anything that doesn't match the PR path shape.
    """
    if not url or not isinstance(url, str):
        raise ValueError(f"empty or non-string url: {url!r}")

    parsed = urlparse(url.strip())
    if parsed.scheme != "https":
        raise ValueError(f"only https URLs are accepted (got scheme={parsed.scheme!r}): {url!r}")
    if parsed.netloc != "github.com":
        raise ValueError(
            f"only github.com is supported in V1 (got host={parsed.netloc!r}): {url!r}"
        )

    m = _PR_PATH_RE.match(parsed.path)
    if not m:
        raise ValueError(f"not a recognizable PR URL path: {url!r}")

    return PRRef(owner=m["owner"], repo=m["repo"], number=int(m["number"]))
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/unit/test_url.py -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/url.py tests/unit/test_url.py
git commit -m "feat(github_approve_merge): add PR URL parser (PRRef + parse_pr_url)"
```

---

### Task 2: Input sources — `input_sources.py`

**Files:**
- Create: `src/github_approve_merge/input_sources.py`
- Create: `tests/unit/test_input_sources.py`

- [ ] **Step 1: Write failing tests**

Create `tests/unit/test_input_sources.py`:

```python
import io
from pathlib import Path

import pytest

from github_approve_merge.input_sources import (
    InputSourceError,
    collect_urls,
    parse_url_file,
)
from github_approve_merge.url import PRRef


URL_A = "https://github.com/owner/repo/pull/1"
URL_B = "https://github.com/owner/repo/pull/2"
URL_C = "https://github.com/owner/repo/pull/3"

REF_A = PRRef("owner", "repo", 1)
REF_B = PRRef("owner", "repo", 2)
REF_C = PRRef("owner", "repo", 3)


class TestParseUrlFile:
    def test_one_per_line(self, tmp_path: Path):
        f = tmp_path / "urls.txt"
        f.write_text(f"{URL_A}\n{URL_B}\n")
        assert parse_url_file(f) == [URL_A, URL_B]

    def test_strips_whitespace_blank_and_comments(self, tmp_path: Path):
        f = tmp_path / "urls.txt"
        f.write_text(
            f"# header comment\n"
            f"\n"
            f"  {URL_A}  \n"
            f"# inline note\n"
            f"{URL_B}\n"
            f"\n"
        )
        assert parse_url_file(f) == [URL_A, URL_B]

    def test_missing_file_raises_input_source_error(self, tmp_path: Path):
        with pytest.raises(InputSourceError):
            parse_url_file(tmp_path / "nope.txt")


class TestCollectUrls:
    def test_args_only(self):
        refs = collect_urls(args=[URL_A, URL_B], file_path=None, stdin=None)
        assert refs == [REF_A, REF_B]

    def test_args_plus_file(self, tmp_path: Path):
        f = tmp_path / "urls.txt"
        f.write_text(f"{URL_B}\n{URL_C}\n")
        refs = collect_urls(args=[URL_A], file_path=f, stdin=None)
        assert refs == [REF_A, REF_B, REF_C]

    def test_stdin_only(self):
        refs = collect_urls(args=[], file_path=None, stdin=io.StringIO(f"{URL_A}\n{URL_B}\n"))
        assert refs == [REF_A, REF_B]

    def test_dedupe_first_occurrence_wins(self):
        refs = collect_urls(
            args=[URL_A, URL_B, URL_A],
            file_path=None,
            stdin=io.StringIO(f"{URL_B}\n{URL_C}\n"),
        )
        assert refs == [REF_A, REF_B, REF_C]

    def test_empty_inputs_raises(self):
        with pytest.raises(InputSourceError, match="no URLs"):
            collect_urls(args=[], file_path=None, stdin=None)

    def test_invalid_url_raises_with_source_context(self):
        with pytest.raises(InputSourceError, match=r"args\[1\]"):
            collect_urls(args=[URL_A, "not a url"], file_path=None, stdin=None)
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/unit/test_input_sources.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `input_sources.py`**

Create `src/github_approve_merge/input_sources.py`:

```python
from __future__ import annotations

from pathlib import Path
from typing import IO, Iterable

from github_approve_merge.url import PRRef, parse_pr_url


class InputSourceError(ValueError):
    """Raised on any failure collecting/validating URLs from inputs."""


def parse_url_file(path: Path) -> list[str]:
    """Read a URL list file. One URL per line. '#' comment lines and blank lines ignored."""
    try:
        text = path.read_text()
    except OSError as e:
        raise InputSourceError(f"could not read --file {path}: {e}") from e

    urls: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        urls.append(line)
    return urls


def _parse_stdin(stdin: IO[str]) -> list[str]:
    urls: list[str] = []
    for raw in stdin:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        urls.append(line)
    return urls


def collect_urls(
    args: Iterable[str],
    file_path: Path | None,
    stdin: IO[str] | None,
) -> list[PRRef]:
    """Merge URLs from positional args, a file, and stdin into a deduped list of PRRefs.

    Order: args, then file, then stdin. First occurrence of each URL wins.
    Raises InputSourceError if no inputs are present or any URL fails to parse.
    The error message identifies which source the bad URL came from.
    """
    sourced: list[tuple[str, str]] = []  # (source_label, raw_url)
    for i, url in enumerate(args):
        sourced.append((f"args[{i}]", url))
    if file_path is not None:
        for i, url in enumerate(parse_url_file(file_path)):
            sourced.append((f"file:{file_path}:{i + 1}", url))
    if stdin is not None:
        for i, url in enumerate(_parse_stdin(stdin)):
            sourced.append((f"stdin:{i + 1}", url))

    if not sourced:
        raise InputSourceError(
            "no URLs provided — pass them as args, via --file, or pipe them on stdin"
        )

    seen: set[str] = set()
    refs: list[PRRef] = []
    for label, url in sourced:
        if url in seen:
            continue
        seen.add(url)
        try:
            refs.append(parse_pr_url(url))
        except ValueError as e:
            raise InputSourceError(f"{label}: {e}") from e
    return refs
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/unit/test_input_sources.py -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/input_sources.py tests/unit/test_input_sources.py
git commit -m "feat(github_approve_merge): add input collector (args + --file + stdin, dedupe)"
```

---

### Task 3: Config — `config.py`

**Files:**
- Create: `src/github_approve_merge/config.py`
- Create: `tests/unit/test_config.py`

- [ ] **Step 1: Write failing tests**

Create `tests/unit/test_config.py`:

```python
import re
from pathlib import Path

from github_approve_merge.config import (
    DEFAULT_RETENTION_DAYS,
    DEFAULT_TIMEOUT_SECONDS,
    RUN_ID_PATTERN,
    default_logs_dir,
    default_storage_state_path,
    generate_run_id,
)


class TestDefaults:
    def test_retention_days(self):
        assert DEFAULT_RETENTION_DAYS == 10

    def test_timeout_seconds(self):
        assert DEFAULT_TIMEOUT_SECONDS == 30

    def test_default_logs_dir_is_cwd_relative(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        assert default_logs_dir() == tmp_path / "logs"

    def test_default_storage_state_path_uses_xdg(self, monkeypatch, tmp_path: Path):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        assert default_storage_state_path() == tmp_path / "github_approve_merge" / "storage_state.json"

    def test_default_storage_state_path_falls_back_to_home_config(self, monkeypatch, tmp_path: Path):
        monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
        monkeypatch.setenv("HOME", str(tmp_path))
        assert default_storage_state_path() == tmp_path / ".config" / "github_approve_merge" / "storage_state.json"


class TestRunId:
    def test_pattern_matches_format(self):
        rid = generate_run_id()
        assert RUN_ID_PATTERN.match(rid), f"run id {rid!r} doesn't match pattern"

    def test_pattern_constant(self):
        assert RUN_ID_PATTERN.pattern == r"^\d{8}-\d{6}-[a-f0-9]{4}$"

    def test_two_ids_differ(self):
        # rand4 suffix ensures uniqueness even within the same second
        assert generate_run_id() != generate_run_id()
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/unit/test_config.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `config.py`**

Create `src/github_approve_merge/config.py`:

```python
from __future__ import annotations

import os
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_RETENTION_DAYS = 10
DEFAULT_TIMEOUT_SECONDS = 30

RUN_ID_PATTERN = re.compile(r"^\d{8}-\d{6}-[a-f0-9]{4}$")


def default_logs_dir() -> Path:
    """`./logs` relative to the current working directory."""
    return Path.cwd() / "logs"


def default_storage_state_path() -> Path:
    """XDG-style location for the persisted browser session.

    Honours `$XDG_CONFIG_HOME` if set, otherwise `~/.config`.
    """
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg) if xdg else Path.home() / ".config"
    return base / "github_approve_merge" / "storage_state.json"


def generate_run_id() -> str:
    """`YYYYMMDD-HHMMSS-<rand4>` (UTC) — matches RUN_ID_PATTERN."""
    now = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{now}-{secrets.token_hex(2)}"
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/unit/test_config.py -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/config.py tests/unit/test_config.py
git commit -m "feat(github_approve_merge): add config (defaults, paths, run-id generator)"
```

---

### Task 4: Retention — `retention.py`

**Files:**
- Create: `src/github_approve_merge/retention.py`
- Create: `tests/unit/test_retention.py`

- [ ] **Step 1: Write failing tests**

Create `tests/unit/test_retention.py`:

```python
import os
import time
from pathlib import Path

from github_approve_merge.retention import sweep


def _touch_dir(root: Path, name: str, age_days: float) -> Path:
    d = root / name
    d.mkdir()
    (d / "marker").write_text("x")
    mtime = time.time() - age_days * 86400
    os.utime(d, (mtime, mtime))
    return d


class TestSweep:
    def test_deletes_only_run_dirs_older_than_threshold(self, tmp_path: Path):
        old_a = _touch_dir(tmp_path, "20260101-100000-aaaa", age_days=15)
        old_b = _touch_dir(tmp_path, "20260102-100000-bbbb", age_days=12)
        fresh = _touch_dir(tmp_path, "20260520-100000-cccc", age_days=2)

        deleted = sweep(tmp_path, max_age_days=10, skip=set())
        assert set(deleted) == {old_a, old_b}
        assert not old_a.exists()
        assert not old_b.exists()
        assert fresh.exists()

    def test_skip_set_protects_current_run_dir(self, tmp_path: Path):
        old = _touch_dir(tmp_path, "20260101-100000-aaaa", age_days=15)
        deleted = sweep(tmp_path, max_age_days=10, skip={old})
        assert deleted == []
        assert old.exists()

    def test_non_matching_dir_name_is_never_deleted(self, tmp_path: Path):
        not_a_run = tmp_path / "old_logs"
        not_a_run.mkdir()
        mtime = time.time() - 30 * 86400
        os.utime(not_a_run, (mtime, mtime))

        deleted = sweep(tmp_path, max_age_days=10, skip=set())
        assert deleted == []
        assert not_a_run.exists()

    def test_misplaced_storage_state_file_is_never_deleted(self, tmp_path: Path):
        stray = tmp_path / "storage_state.json"
        stray.write_text("{}")
        mtime = time.time() - 30 * 86400
        os.utime(stray, (mtime, mtime))

        deleted = sweep(tmp_path, max_age_days=10, skip=set())
        assert deleted == []
        assert stray.exists()

    def test_missing_logs_root_returns_empty(self, tmp_path: Path):
        missing = tmp_path / "no_such_dir"
        assert sweep(missing, max_age_days=10, skip=set()) == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/unit/test_retention.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `retention.py`**

Create `src/github_approve_merge/retention.py`:

```python
from __future__ import annotations

import logging
import shutil
import time
from pathlib import Path

from github_approve_merge.config import RUN_ID_PATTERN

_log = logging.getLogger("gam")


def sweep(logs_root: Path, max_age_days: int, skip: set[Path]) -> list[Path]:
    """Delete run-dirs older than max_age_days. Return the list of paths actually deleted.

    Only deletes immediate children of logs_root that are directories AND whose
    name matches RUN_ID_PATTERN. This is structural: a stray file or
    differently-named dir cannot be deleted by accident.

    Never raises on individual delete failures — logs them at WARN and moves on.
    """
    if not logs_root.exists():
        return []

    threshold = time.time() - max_age_days * 86400
    deleted: list[Path] = []
    skip = {p.resolve() for p in skip}

    for child in logs_root.iterdir():
        if not child.is_dir():
            continue
        if not RUN_ID_PATTERN.match(child.name):
            continue
        if child.resolve() in skip:
            continue
        try:
            mtime = child.stat().st_mtime
        except OSError:
            continue
        if mtime >= threshold:
            continue

        try:
            shutil.rmtree(child, onerror=_rmtree_onerror)
        except OSError as e:
            _log.warning("retention: failed to delete %s: %s", child, e)
            continue
        deleted.append(child)

    return deleted


def _rmtree_onerror(func, path, exc_info):
    _log.warning("retention: rmtree could not remove %s (%s): %s", path, func.__name__, exc_info[1])
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/unit/test_retention.py -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/retention.py tests/unit/test_retention.py
git commit -m "feat(github_approve_merge): add lazy-delete retention sweep (10-day default)"
```

---

### Task 5: Logging setup — `logging_setup.py`

**Files:**
- Create: `src/github_approve_merge/logging_setup.py`
- Create: `tests/unit/test_logging_setup.py`

- [ ] **Step 1: Write failing tests**

Create `tests/unit/test_logging_setup.py`:

```python
import io
import json
import logging
from pathlib import Path

from github_approve_merge.logging_setup import (
    ColorConsoleHandler,
    JSONFormatter,
    RunContext,
    make_run_logger,
)


class TestJsonFormatter:
    def test_basic_event_shape(self):
        fmt = JSONFormatter()
        rec = logging.LogRecord(
            name="gam", level=logging.INFO, pathname=__file__, lineno=1,
            msg="hello", args=(), exc_info=None,
        )
        rec.run_id = "20260526-143012-7af3"
        rec.step = "after-load"
        out = fmt.format(rec)
        payload = json.loads(out)
        assert payload["msg"] == "hello"
        assert payload["level"] == "INFO"
        assert payload["run_id"] == "20260526-143012-7af3"
        assert payload["step"] == "after-load"
        assert payload["ts"].endswith("Z")
        assert "T" in payload["ts"]  # ISO 8601

    def test_extra_fields_are_included(self):
        fmt = JSONFormatter()
        rec = logging.LogRecord(
            name="gam", level=logging.INFO, pathname=__file__, lineno=1,
            msg="approved", args=(), exc_info=None,
        )
        rec.run_id = "rid"
        rec.step = "approve"
        rec.pr = "owner/repo#1"
        rec.state = "OPEN_APPROVABLE"
        rec.screenshot = "screenshots/foo.png"
        rec.duration_ms = 123
        payload = json.loads(fmt.format(rec))
        assert payload["pr"] == "owner/repo#1"
        assert payload["state"] == "OPEN_APPROVABLE"
        assert payload["screenshot"] == "screenshots/foo.png"
        assert payload["duration_ms"] == 123

    def test_exception_serialized(self):
        fmt = JSONFormatter()
        try:
            raise RuntimeError("kaboom")
        except RuntimeError:
            import sys
            exc_info = sys.exc_info()
        rec = logging.LogRecord(
            name="gam", level=logging.ERROR, pathname=__file__, lineno=1,
            msg="oops", args=(), exc_info=exc_info,
        )
        rec.run_id = "rid"
        rec.step = "bang"
        payload = json.loads(fmt.format(rec))
        assert payload["exception"]["type"] == "RuntimeError"
        assert "kaboom" in payload["exception"]["repr"]
        assert "Traceback" in payload["exception"]["traceback"]


class TestColorConsoleHandler:
    def test_format_contains_pr_and_step(self):
        h = ColorConsoleHandler(stream=io.StringIO(), use_color=False)
        rec = logging.LogRecord(
            name="gam", level=logging.INFO, pathname=__file__, lineno=1,
            msg="approve submitted", args=(), exc_info=None,
        )
        rec.run_id = "rid"
        rec.pr = "owner/repo#1"
        rec.step = "approve"
        line = h.format(rec)
        assert "approve submitted" in line
        assert "pr=owner/repo#1" in line
        assert "step=approve" in line
        assert "INFO" in line


class TestMakeRunLogger:
    def test_writes_jsonl_to_run_dir(self, tmp_path: Path):
        run_dir = tmp_path / "20260526-143012-7af3"
        run_dir.mkdir()
        ctx = RunContext(run_id="20260526-143012-7af3", run_dir=run_dir)
        logger = make_run_logger(ctx, verbose=False, quiet=True)
        logger.info("hello world", extra={"step": "boot"})

        line = (run_dir / "run.jsonl").read_text().splitlines()[0]
        payload = json.loads(line)
        assert payload["msg"] == "hello world"
        assert payload["step"] == "boot"
        assert payload["run_id"] == "20260526-143012-7af3"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/unit/test_logging_setup.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `logging_setup.py`**

Create `src/github_approve_merge/logging_setup.py`:

```python
from __future__ import annotations

import json
import logging
import sys
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import IO

LOGGER_NAME = "gam"

_OPTIONAL_KEYS = ("pr", "state", "screenshot", "duration_ms")
_ANSI = {
    "DEBUG": "\x1b[90m",
    "INFO": "\x1b[36m",
    "WARNING": "\x1b[33m",
    "ERROR": "\x1b[31m",
    "CRITICAL": "\x1b[1;31m",
    "RESET": "\x1b[0m",
}


@dataclass
class RunContext:
    """Shared context for a single `run` invocation."""

    run_id: str
    run_dir: Path
    authenticated_login: str | None = None
    screenshot_counters: dict[str, int] = field(default_factory=dict)


class JSONFormatter(logging.Formatter):
    """Emit one JSON object per log event matching the run.jsonl schema in spec §7.2."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict = {
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") +
                  f"{int(record.msecs):03d}Z",
            "level": record.levelname,
            "run_id": getattr(record, "run_id", None),
            "step": getattr(record, "step", None),
            "msg": record.getMessage(),
        }
        for key in _OPTIONAL_KEYS:
            val = getattr(record, key, None)
            if val is not None:
                payload[key] = val
        if record.exc_info:
            etype, evalue, etb = record.exc_info
            payload["exception"] = {
                "type": etype.__name__ if etype else "UnknownError",
                "repr": repr(evalue),
                "traceback": "".join(traceback.format_exception(etype, evalue, etb)),
            }
        return json.dumps(payload, ensure_ascii=False)


class ColorConsoleHandler(logging.StreamHandler):
    """Stream handler with ANSI level coloring and a human-readable layout.

    Format: `HH:MM:SS LEVEL [pr=… step=…] message`
    """

    def __init__(self, stream: IO[str] | None = None, *, use_color: bool | None = None):
        super().__init__(stream or sys.stdout)
        if use_color is None:
            use_color = bool(getattr(self.stream, "isatty", lambda: False)())
        self.use_color = use_color

    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        bits = [ts, record.levelname]
        ctx_bits = []
        pr = getattr(record, "pr", None)
        step = getattr(record, "step", None)
        if pr:
            ctx_bits.append(f"pr={pr}")
        if step:
            ctx_bits.append(f"step={step}")
        if ctx_bits:
            bits.append("[" + " ".join(ctx_bits) + "]")
        bits.append(record.getMessage())
        line = " ".join(bits)
        if self.use_color:
            color = _ANSI.get(record.levelname, "")
            line = f"{color}{line}{_ANSI['RESET']}"
        if record.exc_info:
            line += "\n" + "".join(traceback.format_exception(*record.exc_info))
        return line


class _ContextFilter(logging.Filter):
    """Inject default RunContext fields onto every record."""

    def __init__(self, ctx: RunContext):
        super().__init__()
        self.ctx = ctx

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "run_id"):
            record.run_id = self.ctx.run_id
        return True


def make_run_logger(ctx: RunContext, *, verbose: bool, quiet: bool) -> logging.Logger:
    """Build the `gam` logger, attach JSON file + colored stdout handlers, install context filter."""
    logger = logging.getLogger(LOGGER_NAME)
    # Reset handlers on re-init so tests can call this repeatedly.
    for h in list(logger.handlers):
        logger.removeHandler(h)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    ctx.run_dir.mkdir(parents=True, exist_ok=True)
    file_h = logging.FileHandler(ctx.run_dir / "run.jsonl", encoding="utf-8")
    file_h.setLevel(logging.DEBUG)
    file_h.setFormatter(JSONFormatter())
    logger.addHandler(file_h)

    console_h = ColorConsoleHandler()
    if verbose:
        console_h.setLevel(logging.DEBUG)
    elif quiet:
        console_h.setLevel(logging.WARNING)
    else:
        console_h.setLevel(logging.INFO)
    logger.addHandler(console_h)

    logger.addFilter(_ContextFilter(ctx))
    return logger
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/unit/test_logging_setup.py -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/logging_setup.py tests/unit/test_logging_setup.py
git commit -m "feat(github_approve_merge): add JSONL+colorized logging (JSONFormatter, ColorConsoleHandler, RunContext)"
```

---

### Task 6: PR-state taxonomy — `pr_state.py` (enums + status exit-class map)

**Files:**
- Create: `src/github_approve_merge/pr_state.py`
- Create: `src/github_approve_merge/actions.py` (status taxonomy only in this task — `process_pr` comes later)
- Create: `tests/unit/test_pr_state_enums.py`

- [ ] **Step 1: Write failing tests**

Create `tests/unit/test_pr_state_enums.py`:

```python
import pytest

from github_approve_merge.actions import (
    EXIT_CODE_FAILURE,
    EXIT_CODE_SUCCESS,
    STATUS_TO_EXIT_CLASS,
    ExitClass,
    aggregate_exit_code,
)
from github_approve_merge.pr_state import PRState, StateFlag


class TestPRStateEnum:
    def test_has_all_required_members(self):
        # Spec §9 detection table rows.
        expected = {
            "MERGED", "CLOSED", "DRAFT", "LOCKED", "SELF_AUTHORED",
            "CONFLICT", "REQUIRED_FAILING", "REQUIRED_PENDING",
            "OPEN_MERGEABLE", "OPEN_APPROVABLE",
        }
        assert {m.name for m in PRState} == expected


class TestStateFlagEnum:
    def test_already_approved_present(self):
        assert StateFlag.ALREADY_APPROVED.name == "ALREADY_APPROVED"


class TestStatusExitClassMap:
    @pytest.mark.parametrize("status,cls", [
        ("done", ExitClass.SUCCESS),
        ("skipped-merged", ExitClass.SUCCESS),
        ("skipped-closed", ExitClass.WARN),
        ("skipped-draft", ExitClass.WARN),
        ("skipped-self", ExitClass.WARN),
        ("skipped-needs-more-approvals", ExitClass.WARN),
        ("failed-conflict", ExitClass.ERROR),
        ("failed-required-check", ExitClass.ERROR),
        ("failed-locked", ExitClass.ERROR),
        ("failed-interrupted", ExitClass.ERROR),
        ("failed-exception", ExitClass.ERROR),
    ])
    def test_known_statuses(self, status: str, cls: ExitClass):
        assert STATUS_TO_EXIT_CLASS[status] is cls


class TestAggregateExitCode:
    def test_all_success(self):
        assert aggregate_exit_code(["done", "done", "skipped-merged"]) == EXIT_CODE_SUCCESS

    def test_any_warn_means_failure(self):
        assert aggregate_exit_code(["done", "skipped-closed"]) == EXIT_CODE_FAILURE

    def test_any_error_means_failure(self):
        assert aggregate_exit_code(["done", "failed-conflict"]) == EXIT_CODE_FAILURE

    def test_empty_means_failure(self):
        # No PRs processed (e.g. all filtered out): treat as failure so caller notices.
        assert aggregate_exit_code([]) == EXIT_CODE_FAILURE
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/unit/test_pr_state_enums.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `pr_state.py` (enums only — `detect_state` comes in Task 12)**

Create `src/github_approve_merge/pr_state.py`:

```python
from __future__ import annotations

from enum import Enum, auto


class PRState(Enum):
    """Terminal classification of a PR's current state. See spec §9."""

    MERGED = auto()
    CLOSED = auto()
    DRAFT = auto()
    LOCKED = auto()
    SELF_AUTHORED = auto()
    CONFLICT = auto()
    REQUIRED_FAILING = auto()
    REQUIRED_PENDING = auto()
    OPEN_MERGEABLE = auto()
    OPEN_APPROVABLE = auto()


class StateFlag(Enum):
    """Modifier flags that combine with a PRState. See spec §9."""

    ALREADY_APPROVED = auto()
```

- [ ] **Step 4: Implement `actions.py` (status taxonomy slice — `process_pr` comes in Task 15)**

Create `src/github_approve_merge/actions.py`:

```python
from __future__ import annotations

from enum import Enum

EXIT_CODE_SUCCESS = 0
EXIT_CODE_FAILURE = 1
EXIT_CODE_USAGE = 2
EXIT_CODE_INTERRUPTED = 130


class ExitClass(Enum):
    SUCCESS = "success"
    WARN = "warn"
    ERROR = "error"


STATUS_TO_EXIT_CLASS: dict[str, ExitClass] = {
    # Terminal success
    "done": ExitClass.SUCCESS,
    "skipped-merged": ExitClass.SUCCESS,
    # Terminal warn (user gave us a URL we couldn't merge)
    "skipped-closed": ExitClass.WARN,
    "skipped-draft": ExitClass.WARN,
    "skipped-self": ExitClass.WARN,
    "skipped-needs-more-approvals": ExitClass.WARN,
    # Terminal error
    "failed-conflict": ExitClass.ERROR,
    "failed-required-check": ExitClass.ERROR,
    "failed-locked": ExitClass.ERROR,
    "failed-interrupted": ExitClass.ERROR,
    "failed-exception": ExitClass.ERROR,
}


def aggregate_exit_code(statuses: list[str]) -> int:
    """Return EXIT_CODE_SUCCESS iff every status is SUCCESS-class. Otherwise EXIT_CODE_FAILURE.

    Empty input is treated as failure so the caller notices that nothing was processed.
    Unknown statuses are conservatively treated as failures.
    """
    if not statuses:
        return EXIT_CODE_FAILURE
    for s in statuses:
        cls = STATUS_TO_EXIT_CLASS.get(s)
        if cls is None or cls is not ExitClass.SUCCESS:
            return EXIT_CODE_FAILURE
    return EXIT_CODE_SUCCESS
```

- [ ] **Step 5: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/unit/test_pr_state_enums.py -v
```

Expected: all pass.

- [ ] **Step 6: Commit**

```bash
git add src/github_approve_merge/pr_state.py src/github_approve_merge/actions.py tests/unit/test_pr_state_enums.py
git commit -m "feat(github_approve_merge): add PRState/StateFlag enums and exit-class taxonomy"
```

---

### Task 7: Selector constants — `pages/selectors.py`

**Files:**
- Create: `src/github_approve_merge/pages/selectors.py`
- Create: `tests/unit/test_selectors.py`

- [ ] **Step 1: Write failing tests**

Create `tests/unit/test_selectors.py`:

```python
import re

from github_approve_merge.pages import selectors as S


class TestSelectors:
    def test_constants_present(self):
        # Spec §9 selectors live in this module as named constants.
        for name in (
            "APPROVE_RADIO_VALUE",
            "SUBMIT_REVIEW_NAME",
            "MERGE_BUTTON_NAME",
            "CONFIRM_MERGE_NAME",
            "MERGE_WHEN_READY_NAME",
            "ENABLE_AUTO_MERGE_NAME",
            "USER_LOGIN_META",
            "STATE_BADGE_MERGED",
            "STATE_BADGE_CLOSED",
            "DRAFT_BADGE_TEXT",
            "LOCKED_NOTICE_TEXT",
            "CONFLICT_NOTICE_TEXT",
            "REQUIRED_STATUS_TEXT",
            "REVIEWERS_PANEL_APPROVED_LABEL",
            "PR_AUTHOR_LINK_CSS",
        ):
            assert hasattr(S, name), f"missing selector constant {name}"

    def test_merge_button_pattern_covers_all_methods(self):
        # GitHub renames the primary button based on merge method.
        for label in ("Merge pull request", "Squash and merge", "Rebase and merge",
                      "Create a merge commit"):
            assert S.MERGE_BUTTON_NAME.fullmatch(label), label

    def test_confirm_merge_pattern_covers_all_methods(self):
        for label in ("Confirm merge", "Confirm squash and merge", "Confirm rebase and merge"):
            assert S.CONFIRM_MERGE_NAME.fullmatch(label), label

    def test_merge_when_ready_exact(self):
        assert S.MERGE_WHEN_READY_NAME.fullmatch("Merge when ready")
        assert not S.MERGE_WHEN_READY_NAME.fullmatch("Merge pull request")

    def test_patterns_are_compiled_regex(self):
        for attr in (S.MERGE_BUTTON_NAME, S.CONFIRM_MERGE_NAME,
                     S.MERGE_WHEN_READY_NAME, S.ENABLE_AUTO_MERGE_NAME,
                     S.SUBMIT_REVIEW_NAME):
            assert isinstance(attr, re.Pattern), attr
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/unit/test_selectors.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `pages/selectors.py`**

Create `src/github_approve_merge/pages/selectors.py`:

```python
"""Central registry of every selector used by Page Objects.

When GitHub redesigns and tests start failing, this is the single file to update.

Prefer role + accessible name (regex). Fall back to data-* attributes. Use CSS
class only as a last resort and explain why in a comment next to the constant.
"""
from __future__ import annotations

import re

# --- Review submission form (FilesPage) -------------------------------------

APPROVE_RADIO_VALUE = "approve"  # name="pull_request_review[event]", value="approve"
SUBMIT_REVIEW_NAME = re.compile(r"^Submit review$")

# --- Merge box (PRPage) -----------------------------------------------------

MERGE_BUTTON_NAME = re.compile(
    r"^(Merge pull request|Create a merge commit|Squash and merge|Rebase and merge)$"
)
CONFIRM_MERGE_NAME = re.compile(
    r"^Confirm (merge|squash and merge|rebase and merge)$"
)
MERGE_WHEN_READY_NAME = re.compile(r"^Merge when ready$")
ENABLE_AUTO_MERGE_NAME = re.compile(r"^Enable auto-merge$")  # alternative copy GitHub uses

# --- Identity ---------------------------------------------------------------

USER_LOGIN_META = 'meta[name="user-login"]'  # `content=<login>` on every github.com page

# --- Status badges and notices (used by detect_state) -----------------------

STATE_BADGE_MERGED = re.compile(r"^Merged$")          # role=status/title in header
STATE_BADGE_CLOSED = re.compile(r"^Closed$")
DRAFT_BADGE_TEXT = re.compile(r"^Draft$")
LOCKED_NOTICE_TEXT = re.compile(r"This conversation has been locked", re.I)
CONFLICT_NOTICE_TEXT = re.compile(r"This branch has conflicts", re.I)
REQUIRED_STATUS_TEXT = re.compile(r"Required statuses must pass", re.I)

# --- Reviewers panel --------------------------------------------------------

REVIEWERS_PANEL_APPROVED_LABEL = re.compile(r"approved these changes", re.I)

# CSS fallback used by PR-author lookup. The accessible-name path is the
# author link's text in the PR header timeline; this CSS hook is the
# resilient identifier (data-hovercard-type=user inside .timeline-comment-header
# for the PR opening comment).
PR_AUTHOR_LINK_CSS = '.gh-header-meta a.author[data-hovercard-type="user"]'
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/unit/test_selectors.py -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/pages/selectors.py tests/unit/test_selectors.py
git commit -m "feat(github_approve_merge): add central selector constants for Page Objects"
```

---

## Phase 2 — Playwright units against HTML fixtures

### Task 8: HTML fixtures + browser fixture in conftest

**Files:**
- Create: `tests/fixtures/html/pr_mergeable.html`
- Create: `tests/fixtures/html/pr_needs_approval.html`
- Create: `tests/fixtures/html/pr_ci_pending.html`
- Create: `tests/fixtures/html/pr_required_check_failing.html`
- Create: `tests/fixtures/html/pr_conflict.html`
- Create: `tests/fixtures/html/pr_merged.html`
- Create: `tests/fixtures/html/pr_closed.html`
- Create: `tests/fixtures/html/pr_draft.html`
- Create: `tests/fixtures/html/pr_locked.html`
- Create: `tests/fixtures/html/pr_self.html`
- Create: `tests/fixtures/html/pr_already_approved_by_me.html`
- Create: `tests/fixtures/html/files_can_approve.html`
- Create: `tests/fixtures/html/files_already_approved.html`
- Modify: `tests/conftest.py`

Each fixture contains the minimum elements needed for selectors in `pages/selectors.py` to resolve correctly. They use the GitHub structural cues a real page would have (`meta[name=user-login]`, `.gh-header-meta`, role-buttons, etc.) but stripped of unrelated chrome.

- [ ] **Step 1: Write `pr_mergeable.html`**

```html
<!doctype html>
<html><head>
  <title>Mergeable PR</title>
  <meta name="user-login" content="reviewer-bot">
</head><body>
  <div class="gh-header-meta">
    <a class="author" data-hovercard-type="user" href="/somebody">somebody</a>
  </div>
  <span title="Status: Open">Open</span>
  <div id="partial-pull-merging">
    <button type="button">Merge pull request</button>
    <button type="button">Confirm merge</button>
  </div>
</body></html>
```

- [ ] **Step 2: Write `pr_needs_approval.html`**

```html
<!doctype html>
<html><head>
  <title>Needs approval PR</title>
  <meta name="user-login" content="reviewer-bot">
</head><body>
  <div class="gh-header-meta">
    <a class="author" data-hovercard-type="user" href="/somebody">somebody</a>
  </div>
  <span title="Status: Open">Open</span>
  <div id="partial-pull-merging">
    <button type="button" disabled aria-disabled="true">Merge pull request</button>
    <p>Review required: At least 1 approving review is required.</p>
  </div>
</body></html>
```

- [ ] **Step 3: Write `pr_ci_pending.html`**

```html
<!doctype html>
<html><head>
  <title>CI pending PR</title>
  <meta name="user-login" content="reviewer-bot">
</head><body>
  <div class="gh-header-meta">
    <a class="author" data-hovercard-type="user" href="/somebody">somebody</a>
  </div>
  <span title="Status: Open">Open</span>
  <div id="partial-pull-merging">
    <p>Required statuses must pass before merging.</p>
    <span class="dot yellow" aria-label="pending">pending</span>
    <button type="button">Merge when ready</button>
    <button type="button" hidden>Confirm merge</button>
  </div>
</body></html>
```

- [ ] **Step 4: Write `pr_required_check_failing.html`**

```html
<!doctype html>
<html><head>
  <title>Required check failing</title>
  <meta name="user-login" content="reviewer-bot">
</head><body>
  <div class="gh-header-meta">
    <a class="author" data-hovercard-type="user" href="/somebody">somebody</a>
  </div>
  <span title="Status: Open">Open</span>
  <div id="partial-pull-merging">
    <p>Required statuses must pass before merging.</p>
    <span class="dot red" aria-label="failed">failed</span>
  </div>
</body></html>
```

- [ ] **Step 5: Write `pr_conflict.html`**

```html
<!doctype html>
<html><head>
  <title>Conflict PR</title>
  <meta name="user-login" content="reviewer-bot">
</head><body>
  <div class="gh-header-meta">
    <a class="author" data-hovercard-type="user" href="/somebody">somebody</a>
  </div>
  <span title="Status: Open">Open</span>
  <div id="partial-pull-merging">
    <p>This branch has conflicts that must be resolved.</p>
  </div>
</body></html>
```

- [ ] **Step 6: Write `pr_merged.html`**

```html
<!doctype html>
<html><head>
  <title>Merged PR</title>
  <meta name="user-login" content="reviewer-bot">
</head><body>
  <div class="gh-header-meta">
    <a class="author" data-hovercard-type="user" href="/somebody">somebody</a>
  </div>
  <span class="State State--merged" title="Status: Merged">Merged</span>
</body></html>
```

- [ ] **Step 7: Write `pr_closed.html`**

```html
<!doctype html>
<html><head>
  <title>Closed PR</title>
  <meta name="user-login" content="reviewer-bot">
</head><body>
  <div class="gh-header-meta">
    <a class="author" data-hovercard-type="user" href="/somebody">somebody</a>
  </div>
  <span class="State State--closed" title="Status: Closed">Closed</span>
</body></html>
```

- [ ] **Step 8: Write `pr_draft.html`**

```html
<!doctype html>
<html><head>
  <title>Draft PR</title>
  <meta name="user-login" content="reviewer-bot">
</head><body>
  <div class="gh-header-meta">
    <a class="author" data-hovercard-type="user" href="/somebody">somebody</a>
  </div>
  <span class="State State--draft" title="Status: Draft">Draft</span>
  <div id="partial-pull-merging">
    <p>This pull request is still a work in progress.</p>
  </div>
</body></html>
```

- [ ] **Step 9: Write `pr_locked.html`**

```html
<!doctype html>
<html><head>
  <title>Locked PR</title>
  <meta name="user-login" content="reviewer-bot">
</head><body>
  <div class="gh-header-meta">
    <a class="author" data-hovercard-type="user" href="/somebody">somebody</a>
  </div>
  <span title="Status: Open">Open</span>
  <div id="partial-pull-merging">
    <p>This conversation has been locked.</p>
  </div>
</body></html>
```

- [ ] **Step 10: Write `pr_self.html`** (PR author == authenticated user)

```html
<!doctype html>
<html><head>
  <title>Self-authored PR</title>
  <meta name="user-login" content="reviewer-bot">
</head><body>
  <div class="gh-header-meta">
    <a class="author" data-hovercard-type="user" href="/reviewer-bot">reviewer-bot</a>
  </div>
  <span title="Status: Open">Open</span>
  <div id="partial-pull-merging">
    <button type="button">Merge pull request</button>
  </div>
</body></html>
```

- [ ] **Step 11: Write `pr_already_approved_by_me.html`**

```html
<!doctype html>
<html><head>
  <title>Already approved by me</title>
  <meta name="user-login" content="reviewer-bot">
</head><body>
  <div class="gh-header-meta">
    <a class="author" data-hovercard-type="user" href="/somebody">somebody</a>
  </div>
  <span title="Status: Open">Open</span>
  <div id="reviewers-panel">
    <div>
      <a href="/reviewer-bot">reviewer-bot</a>
      <span>approved these changes</span>
    </div>
  </div>
  <div id="partial-pull-merging">
    <button type="button">Merge pull request</button>
    <button type="button">Confirm merge</button>
  </div>
</body></html>
```

- [ ] **Step 12: Write `files_can_approve.html`**

```html
<!doctype html>
<html><head>
  <title>Files — can approve</title>
  <meta name="user-login" content="reviewer-bot">
</head><body>
  <form action="/owner/repo/pull/1/reviews">
    <input type="radio" name="pull_request_review[event]" value="approve">
    <input type="radio" name="pull_request_review[event]" value="request_changes">
    <input type="radio" name="pull_request_review[event]" value="comment">
    <button type="submit">Submit review</button>
  </form>
</body></html>
```

- [ ] **Step 13: Write `files_already_approved.html`**

```html
<!doctype html>
<html><head>
  <title>Files — already approved</title>
  <meta name="user-login" content="reviewer-bot">
</head><body>
  <div>You approved these changes on Jan 1.</div>
  <form action="/owner/repo/pull/1/reviews">
    <input type="radio" name="pull_request_review[event]" value="comment">
    <input type="radio" name="pull_request_review[event]" value="request_changes">
    <button type="submit">Submit review</button>
  </form>
</body></html>
```

- [ ] **Step 14: Update `tests/conftest.py` with the browser fixture**

Replace the existing `tests/conftest.py` content with:

```python
import os
from pathlib import Path

import pytest
import pytest_asyncio
from playwright.async_api import Browser, async_playwright


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "html"


def pytest_collection_modifyitems(config, items):
    if os.environ.get("PYTEST_LIVE") == "1":
        return
    skip_live = pytest.mark.skip(reason="PYTEST_LIVE=1 not set")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)


@pytest_asyncio.fixture(scope="session")
async def browser() -> Browser:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        yield browser
        await browser.close()


@pytest_asyncio.fixture
async def page(browser: Browser):
    ctx = await browser.new_context()
    page = await ctx.new_page()
    yield page
    await ctx.close()


@pytest.fixture
def fixture_url():
    """Return a callable that builds a `file://` URL for a fixture filename."""
    def _build(name: str) -> str:
        return (FIXTURES_DIR / name).as_uri()
    return _build
```

- [ ] **Step 15: Verify the browser fixture works**

Create a throwaway smoke test `tests/pages/test_browser_fixture.py`:

```python
import pytest


@pytest.mark.asyncio
async def test_browser_loads_fixture(page, fixture_url):
    await page.goto(fixture_url("pr_mergeable.html"))
    assert await page.title() == "Mergeable PR"
```

Run:
```bash
uv run pytest tests/pages/test_browser_fixture.py -v
```

Expected: pass.

- [ ] **Step 16: Remove the throwaway smoke test (kept fixtures in tree, but it served its purpose)**

```bash
rm tests/pages/test_browser_fixture.py
```

- [ ] **Step 17: Commit**

```bash
git add tests/fixtures tests/conftest.py
git commit -m "test(github_approve_merge): add 13 PR-state HTML fixtures + Playwright browser/page pytest fixtures"
```

---

### Task 9: Screenshots — `screenshots.py`

**Files:**
- Create: `src/github_approve_merge/screenshots.py`
- Create: `tests/pages/test_screenshots.py`

- [ ] **Step 1: Write failing tests**

Create `tests/pages/test_screenshots.py`:

```python
from pathlib import Path

import pytest

from github_approve_merge.logging_setup import RunContext
from github_approve_merge.screenshots import capture
from github_approve_merge.url import PRRef


@pytest.mark.asyncio
async def test_capture_checkpoint_writes_png_with_counter(page, fixture_url, tmp_path: Path):
    ctx = RunContext(run_id="20260526-143012-7af3", run_dir=tmp_path)
    pr = PRRef("acme-org", "widgets-service", 561)
    await page.goto(fixture_url("pr_mergeable.html"))

    p1 = await capture(page, ctx, pr, "after-load")
    p2 = await capture(page, ctx, pr, "before-merge-click")

    assert p1 == Path("screenshots/acme-org__widgets-service__561__01-after-load.png")
    assert p2 == Path("screenshots/acme-org__widgets-service__561__02-before-merge-click.png")
    assert (tmp_path / p1).exists()
    assert (tmp_path / p2).exists()


@pytest.mark.asyncio
async def test_capture_error_skips_counter(page, fixture_url, tmp_path: Path):
    ctx = RunContext(run_id="rid", run_dir=tmp_path)
    pr = PRRef("o", "r", 1)
    await page.goto(fixture_url("pr_conflict.html"))

    p = await capture(page, ctx, pr, "error-conflict-detected")
    assert p == Path("screenshots/o__r__1__error-conflict-detected.png")
    assert (tmp_path / p).exists()


@pytest.mark.asyncio
async def test_capture_never_raises_on_failure(monkeypatch, page, fixture_url, tmp_path: Path):
    ctx = RunContext(run_id="rid", run_dir=tmp_path)
    pr = PRRef("o", "r", 1)
    await page.goto(fixture_url("pr_mergeable.html"))

    async def boom(*_args, **_kwargs):
        raise RuntimeError("disk full")

    monkeypatch.setattr(page, "screenshot", boom)

    # Should swallow the error and return None instead of raising.
    result = await capture(page, ctx, pr, "after-load")
    assert result is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/pages/test_screenshots.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `screenshots.py`**

Create `src/github_approve_merge/screenshots.py`:

```python
from __future__ import annotations

import logging
from pathlib import Path

from playwright.async_api import Page

from github_approve_merge.logging_setup import RunContext
from github_approve_merge.url import PRRef

_log = logging.getLogger("gam")


async def capture(page: Page, ctx: RunContext, pr: PRRef, label: str) -> Path | None:
    """Take a full-page screenshot and write it under `ctx.run_dir/screenshots/`.

    Filename: `<owner>__<repo>__<pr_num>__<NN>-<label>.png` for checkpoint labels;
    `<owner>__<repo>__<pr_num>__<label>.png` (no counter) when label starts with
    `error-`. Returns the path RELATIVE to ctx.run_dir, so log events stay portable.

    Never raises on failure — a broken screenshot must not abort the per-PR flow.
    """
    slug = _slug_for(pr, label, ctx)
    rel = Path("screenshots") / f"{slug}.png"
    full = ctx.run_dir / rel
    full.parent.mkdir(parents=True, exist_ok=True)
    try:
        await page.screenshot(path=str(full), full_page=True)
    except Exception as e:  # pragma: no cover - defensive, exercised by monkeypatch test
        _log.warning(
            "screenshot failed for %s (%s): %s",
            pr, label, e,
            extra={"pr": str(pr), "step": label},
        )
        return None
    return rel


def _slug_for(pr: PRRef, label: str, ctx: RunContext) -> str:
    base = f"{pr.owner}__{pr.repo}__{pr.number}"
    if label.startswith("error-"):
        return f"{base}__{label}"
    counter_key = f"{ctx.run_id}/{pr}"
    n = ctx.screenshot_counters.get(counter_key, 0) + 1
    ctx.screenshot_counters[counter_key] = n
    return f"{base}__{n:02d}-{label}"
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/pages/test_screenshots.py -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/screenshots.py tests/pages/test_screenshots.py
git commit -m "feat(github_approve_merge): add screenshot helper (full-page, counter, error-safe)"
```

---

### Task 10: `PRPage` Page Object — `pages/pr_page.py`

**Files:**
- Create: `src/github_approve_merge/pages/pr_page.py`
- Create: `tests/pages/test_pr_page.py`

- [ ] **Step 1: Write failing tests**

Create `tests/pages/test_pr_page.py`:

```python
import pytest

from github_approve_merge.pages.pr_page import PRPage


@pytest.mark.asyncio
async def test_merge_button_locator_resolves(page, fixture_url):
    await page.goto(fixture_url("pr_mergeable.html"))
    locator = PRPage(page).merge_button()
    assert await locator.count() == 1
    assert await locator.is_enabled()


@pytest.mark.asyncio
async def test_merge_button_disabled_on_needs_approval(page, fixture_url):
    await page.goto(fixture_url("pr_needs_approval.html"))
    locator = PRPage(page).merge_button()
    # The button exists but is disabled.
    assert await locator.count() == 1
    assert not await locator.is_enabled()


@pytest.mark.asyncio
async def test_merge_when_ready_locator_resolves_on_ci_pending(page, fixture_url):
    await page.goto(fixture_url("pr_ci_pending.html"))
    locator = PRPage(page).merge_when_ready_button()
    assert await locator.count() == 1
    assert await locator.is_enabled()


@pytest.mark.asyncio
async def test_confirm_merge_locator_resolves(page, fixture_url):
    await page.goto(fixture_url("pr_mergeable.html"))
    locator = PRPage(page).confirm_merge_button()
    assert await locator.count() == 1


@pytest.mark.asyncio
async def test_user_login_lookup(page, fixture_url):
    await page.goto(fixture_url("pr_mergeable.html"))
    assert await PRPage(page).authenticated_login() == "reviewer-bot"


@pytest.mark.asyncio
async def test_pr_author_lookup(page, fixture_url):
    await page.goto(fixture_url("pr_self.html"))
    assert await PRPage(page).pr_author_login() == "reviewer-bot"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/pages/test_pr_page.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `pages/pr_page.py`**

Create `src/github_approve_merge/pages/pr_page.py`:

```python
from __future__ import annotations

from playwright.async_api import Locator, Page

from github_approve_merge.pages import selectors as S
from github_approve_merge.url import PRRef


class PRPage:
    """Page Object for the PR overview page (the merge widget lives here)."""

    def __init__(self, page: Page):
        self.page = page

    # --- Navigation ---------------------------------------------------------

    async def goto(self, pr: PRRef) -> None:
        url = f"https://github.com/{pr.owner}/{pr.repo}/pull/{pr.number}"
        await self.page.goto(url, wait_until="domcontentloaded")

    # --- Locators (no clicks; used by tests and by action methods) ---------

    def merge_button(self) -> Locator:
        return self.page.get_by_role("button", name=S.MERGE_BUTTON_NAME)

    def confirm_merge_button(self) -> Locator:
        return self.page.get_by_role("button", name=S.CONFIRM_MERGE_NAME)

    def merge_when_ready_button(self) -> Locator:
        # GitHub uses either label depending on the moment in the rollout.
        primary = self.page.get_by_role("button", name=S.MERGE_WHEN_READY_NAME)
        return primary.or_(self.page.get_by_role("button", name=S.ENABLE_AUTO_MERGE_NAME))

    # --- High-level actions -------------------------------------------------

    async def click_merge_and_confirm(self) -> None:
        await self.merge_button().click()
        await self.confirm_merge_button().click()

    async def click_merge_when_ready(self) -> None:
        await self.merge_when_ready_button().click()
        # GitHub may show a confirm dialog with the same text; click it if present.
        confirm = self.confirm_merge_button()
        if await confirm.count() > 0 and await confirm.first.is_visible():
            await confirm.first.click()

    async def wait_for_merged(self, timeout_ms: int = 30_000) -> None:
        """Wait for either the merged-state badge or the 'Merge when ready' state to settle."""
        merged = self.page.get_by_text(S.STATE_BADGE_MERGED).first
        scheduled = self.page.get_by_role("button", name=S.MERGE_WHEN_READY_NAME)
        await merged.or_(scheduled).wait_for(state="attached", timeout=timeout_ms)

    # --- Identity lookups ---------------------------------------------------

    async def authenticated_login(self) -> str | None:
        el = self.page.locator(S.USER_LOGIN_META)
        if await el.count() == 0:
            return None
        return await el.first.get_attribute("content")

    async def pr_author_login(self) -> str | None:
        el = self.page.locator(S.PR_AUTHOR_LINK_CSS)
        if await el.count() == 0:
            return None
        text = await el.first.text_content()
        return text.strip() if text else None
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/pages/test_pr_page.py -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/pages/pr_page.py tests/pages/test_pr_page.py
git commit -m "feat(github_approve_merge): add PRPage Page Object (merge / merge-when-ready / identity)"
```

---

### Task 11: `FilesPage` Page Object — `pages/files_page.py`

**Files:**
- Create: `src/github_approve_merge/pages/files_page.py`
- Create: `tests/pages/test_files_page.py`

- [ ] **Step 1: Write failing tests**

Create `tests/pages/test_files_page.py`:

```python
import pytest

from github_approve_merge.pages.files_page import FilesPage


@pytest.mark.asyncio
async def test_approve_radio_locator_resolves(page, fixture_url):
    await page.goto(fixture_url("files_can_approve.html"))
    locator = FilesPage(page).approve_radio()
    assert await locator.count() == 1


@pytest.mark.asyncio
async def test_approve_radio_absent_when_already_approved(page, fixture_url):
    await page.goto(fixture_url("files_already_approved.html"))
    locator = FilesPage(page).approve_radio()
    # Fixture deliberately omits the approve radio in this state.
    assert await locator.count() == 0


@pytest.mark.asyncio
async def test_submit_review_locator_resolves(page, fixture_url):
    await page.goto(fixture_url("files_can_approve.html"))
    locator = FilesPage(page).submit_review_button()
    assert await locator.count() == 1


@pytest.mark.asyncio
async def test_select_approve_then_submit_succeeds_against_fixture(page, fixture_url):
    # No backend, so this just verifies the method completes without raising:
    # the radio is selected and the submit button is clicked.
    await page.goto(fixture_url("files_can_approve.html"))
    fp = FilesPage(page)
    await fp.select_approve_and_submit()
    assert await fp.approve_radio().is_checked()
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/pages/test_files_page.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `pages/files_page.py`**

Create `src/github_approve_merge/pages/files_page.py`:

```python
from __future__ import annotations

from playwright.async_api import Locator, Page

from github_approve_merge.pages import selectors as S
from github_approve_merge.url import PRRef


class FilesPage:
    """Page Object for the Files-changed tab (where the Approve form lives)."""

    def __init__(self, page: Page):
        self.page = page

    async def goto(self, pr: PRRef) -> None:
        url = f"https://github.com/{pr.owner}/{pr.repo}/pull/{pr.number}/files"
        await self.page.goto(url, wait_until="domcontentloaded")

    def approve_radio(self) -> Locator:
        return self.page.locator(
            f'input[type="radio"][name="pull_request_review[event]"][value="{S.APPROVE_RADIO_VALUE}"]'
        )

    def submit_review_button(self) -> Locator:
        return self.page.get_by_role("button", name=S.SUBMIT_REVIEW_NAME)

    async def select_approve_and_submit(self) -> None:
        radio = self.approve_radio()
        await radio.check()
        await self.submit_review_button().click()
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/pages/test_files_page.py -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/pages/files_page.py tests/pages/test_files_page.py
git commit -m "feat(github_approve_merge): add FilesPage Page Object (approve form)"
```

---

### Task 12: `detect_state` against fixtures

**Files:**
- Modify: `src/github_approve_merge/pr_state.py` (add `detect_state` and supporting helpers)
- Create: `tests/pages/test_detect_state.py`

- [ ] **Step 1: Write failing tests**

Create `tests/pages/test_detect_state.py`:

```python
import pytest

from github_approve_merge.pr_state import PRState, StateFlag, detect_state


@pytest.mark.asyncio
async def test_merged(page, fixture_url):
    await page.goto(fixture_url("pr_merged.html"))
    state, flags = await detect_state(page, me="reviewer-bot")
    assert state is PRState.MERGED
    assert flags == set()


@pytest.mark.asyncio
async def test_closed(page, fixture_url):
    await page.goto(fixture_url("pr_closed.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.CLOSED


@pytest.mark.asyncio
async def test_draft(page, fixture_url):
    await page.goto(fixture_url("pr_draft.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.DRAFT


@pytest.mark.asyncio
async def test_locked(page, fixture_url):
    await page.goto(fixture_url("pr_locked.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.LOCKED


@pytest.mark.asyncio
async def test_self_authored(page, fixture_url):
    await page.goto(fixture_url("pr_self.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.SELF_AUTHORED


@pytest.mark.asyncio
async def test_conflict(page, fixture_url):
    await page.goto(fixture_url("pr_conflict.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.CONFLICT


@pytest.mark.asyncio
async def test_required_failing(page, fixture_url):
    await page.goto(fixture_url("pr_required_check_failing.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.REQUIRED_FAILING


@pytest.mark.asyncio
async def test_required_pending(page, fixture_url):
    await page.goto(fixture_url("pr_ci_pending.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.REQUIRED_PENDING


@pytest.mark.asyncio
async def test_open_mergeable(page, fixture_url):
    await page.goto(fixture_url("pr_mergeable.html"))
    state, flags = await detect_state(page, me="reviewer-bot")
    assert state is PRState.OPEN_MERGEABLE
    assert StateFlag.ALREADY_APPROVED not in flags


@pytest.mark.asyncio
async def test_open_approvable(page, fixture_url):
    await page.goto(fixture_url("pr_needs_approval.html"))
    state, _ = await detect_state(page, me="reviewer-bot")
    assert state is PRState.OPEN_APPROVABLE


@pytest.mark.asyncio
async def test_already_approved_flag(page, fixture_url):
    await page.goto(fixture_url("pr_already_approved_by_me.html"))
    state, flags = await detect_state(page, me="reviewer-bot")
    assert state is PRState.OPEN_MERGEABLE
    assert StateFlag.ALREADY_APPROVED in flags
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/pages/test_detect_state.py -v
```

Expected: `ImportError: cannot import name 'detect_state'`.

- [ ] **Step 3: Extend `pr_state.py` with `detect_state`**

Append to `src/github_approve_merge/pr_state.py`:

```python
from playwright.async_api import Page

from github_approve_merge.pages import selectors as S
from github_approve_merge.pages.pr_page import PRPage


async def detect_state(page: Page, *, me: str | None) -> tuple[PRState, set[StateFlag]]:
    """Inspect the loaded PR page DOM and classify it. See spec §9.

    `me` is the authenticated user's login (e.g. "reviewer-bot"). Pass None to skip the
    self-PR check.
    """
    flags: set[StateFlag] = set()

    # 1-2: header status badges.
    if await _text_visible(page, S.STATE_BADGE_MERGED):
        return PRState.MERGED, flags
    if await _text_visible(page, S.STATE_BADGE_CLOSED):
        return PRState.CLOSED, flags

    # 3: draft.
    if await _text_visible(page, S.DRAFT_BADGE_TEXT):
        return PRState.DRAFT, flags

    # 4: locked.
    if await _text_visible(page, S.LOCKED_NOTICE_TEXT):
        return PRState.LOCKED, flags

    # 5: authored by me?
    if me:
        author = await PRPage(page).pr_author_login()
        if author and author == me:
            return PRState.SELF_AUTHORED, flags

    # 6: merge conflict.
    if await _text_visible(page, S.CONFLICT_NOTICE_TEXT):
        return PRState.CONFLICT, flags

    # 7-8: required-statuses widget. Distinguish failing from pending.
    if await _text_visible(page, S.REQUIRED_STATUS_TEXT):
        # "Merge when ready" present → pending; otherwise treat as failing.
        if await page.get_by_role("button", name=S.MERGE_WHEN_READY_NAME).count() > 0:
            return PRState.REQUIRED_PENDING, flags
        return PRState.REQUIRED_FAILING, flags

    # 9: already-approved-by-me flag (combines with OPEN_*).
    if me and await _approved_by(page, me):
        flags.add(StateFlag.ALREADY_APPROVED)

    # 10-11: default — merge button enabled vs not.
    pr_page = PRPage(page)
    btn = pr_page.merge_button()
    if await btn.count() > 0 and await btn.is_enabled():
        return PRState.OPEN_MERGEABLE, flags
    return PRState.OPEN_APPROVABLE, flags


async def _text_visible(page: Page, pattern) -> bool:
    locator = page.get_by_text(pattern)
    return await locator.count() > 0


async def _approved_by(page: Page, login: str) -> bool:
    panel = page.locator("#reviewers-panel")
    if await panel.count() == 0:
        return False
    text = await panel.first.text_content() or ""
    return login in text and "approved these changes" in text.lower()
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/pages/test_detect_state.py -v
```

Expected: all 11 tests pass.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/pr_state.py tests/pages/test_detect_state.py
git commit -m "feat(github_approve_merge): add detect_state classifier (11 PR states + ALREADY_APPROVED flag)"
```

---

### Task 13: Browser lifecycle — `browser.py`

**Files:**
- Create: `src/github_approve_merge/browser.py`
- Create: `tests/pages/test_browser.py`

- [ ] **Step 1: Write failing tests**

Create `tests/pages/test_browser.py`:

```python
import json
from pathlib import Path

import pytest

from github_approve_merge.browser import StorageStateError, open_context


@pytest.mark.asyncio
async def test_open_context_with_valid_storage_state(tmp_path: Path):
    ss = tmp_path / "ss.json"
    ss.write_text(json.dumps({"cookies": [], "origins": []}))
    async with open_context(storage_state_path=ss, headless=True) as ctx:
        page = await ctx.new_page()
        await page.goto("about:blank")
        assert await page.title() == ""


@pytest.mark.asyncio
async def test_open_context_missing_storage_state_raises(tmp_path: Path):
    with pytest.raises(StorageStateError, match="not found"):
        async with open_context(storage_state_path=tmp_path / "missing.json", headless=True):
            pass


@pytest.mark.asyncio
async def test_open_context_unreadable_storage_state_raises(tmp_path: Path):
    bad = tmp_path / "ss.json"
    bad.write_text("not json")
    with pytest.raises(StorageStateError, match="parse"):
        async with open_context(storage_state_path=bad, headless=True):
            pass
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/pages/test_browser.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `browser.py`**

Create `src/github_approve_merge/browser.py`:

```python
from __future__ import annotations

import contextlib
import json
from pathlib import Path
from typing import AsyncIterator

from playwright.async_api import BrowserContext, async_playwright


class StorageStateError(RuntimeError):
    """Raised when storage_state.json is missing or unparseable."""


@contextlib.asynccontextmanager
async def open_context(
    *,
    storage_state_path: Path,
    headless: bool,
    timeout_seconds: float = 30.0,
) -> AsyncIterator[BrowserContext]:
    """Launch chromium + open a context loaded from storage_state_path.

    Raises StorageStateError if the storage_state.json file is missing or
    unparseable. Sets a default per-step timeout on the context.
    """
    if not storage_state_path.exists():
        raise StorageStateError(
            f"storage_state not found at {storage_state_path}. "
            "Run `gh-approve-merge auth login` first."
        )
    try:
        # Pre-validate the JSON so Playwright doesn't crash mid-launch with a vague error.
        json.loads(storage_state_path.read_text())
    except json.JSONDecodeError as e:
        raise StorageStateError(
            f"could not parse storage_state at {storage_state_path}: {e}"
        ) from e

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        try:
            ctx = await browser.new_context(storage_state=str(storage_state_path))
            ctx.set_default_timeout(timeout_seconds * 1000)
            try:
                yield ctx
            finally:
                await ctx.close()
        finally:
            await browser.close()
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/pages/test_browser.py -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/browser.py tests/pages/test_browser.py
git commit -m "feat(github_approve_merge): add browser lifecycle (open_context with storage_state validation)"
```

---

## Phase 3 — Composition layer

### Task 14: Auth module — `auth.py`

**Files:**
- Create: `src/github_approve_merge/auth.py`
- Create: `tests/unit/test_auth.py`

- [ ] **Step 1: Write failing tests**

Create `tests/unit/test_auth.py`:

```python
import json
import os
import stat
from pathlib import Path

import pytest

from github_approve_merge.auth import (
    AuthStatus,
    AuthStatusResult,
    check_storage_state,
    save_storage_state,
)


class TestSaveStorageState:
    def test_writes_file_with_0600_permissions(self, tmp_path: Path):
        target = tmp_path / "nested" / "storage_state.json"
        payload = {"cookies": [], "origins": []}
        save_storage_state(payload, target)
        assert target.exists()
        assert json.loads(target.read_text()) == payload
        mode = stat.S_IMODE(target.stat().st_mode)
        assert mode == 0o600, oct(mode)

    def test_creates_parent_dirs(self, tmp_path: Path):
        target = tmp_path / "a" / "b" / "c" / "ss.json"
        save_storage_state({"cookies": []}, target)
        assert target.exists()


class TestCheckStorageState:
    def test_missing_file(self, tmp_path: Path):
        result = check_storage_state(tmp_path / "nope.json")
        assert result.status is AuthStatus.MISSING

    def test_unparseable_file(self, tmp_path: Path):
        f = tmp_path / "ss.json"
        f.write_text("not json")
        result = check_storage_state(f)
        assert result.status is AuthStatus.INVALID
        assert "parse" in result.message.lower()

    def test_valid_shape(self, tmp_path: Path):
        f = tmp_path / "ss.json"
        f.write_text(json.dumps({"cookies": [{"name": "user_session"}], "origins": []}))
        result = check_storage_state(f)
        assert result.status is AuthStatus.PRESENT
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/unit/test_auth.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `auth.py`**

Create `src/github_approve_merge/auth.py`:

```python
from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from playwright.async_api import async_playwright

_log = logging.getLogger("gam")


class AuthStatus(Enum):
    MISSING = "missing"
    INVALID = "invalid"
    PRESENT = "present"


@dataclass(frozen=True)
class AuthStatusResult:
    status: AuthStatus
    message: str


def save_storage_state(payload: dict, target: Path) -> None:
    """Write storage_state.json with parents and 0600 perms."""
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(json.dumps(payload))
    os.chmod(tmp, 0o600)
    os.replace(tmp, target)


def check_storage_state(path: Path) -> AuthStatusResult:
    """Cheap local check — does the file exist and parse as JSON?

    Does NOT contact GitHub. For an online check use `verify_storage_state_live`
    (added when the `auth status` subcommand is wired up — see CLI task).
    """
    if not path.exists():
        return AuthStatusResult(AuthStatus.MISSING, f"no file at {path}")
    try:
        json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        return AuthStatusResult(AuthStatus.INVALID, f"could not parse: {e}")
    return AuthStatusResult(AuthStatus.PRESENT, f"present at {path}")


async def interactive_login(storage_state_path: Path) -> None:
    """Open a headed chromium window pointed at github.com/login.

    Wait for the user to finish signing in (SSO/2FA/whatever) by polling for the
    presence of the meta[name=user-login] tag on a github.com page that isn't
    /login. Save the resulting BrowserContext.storage_state() to disk.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        try:
            ctx = await browser.new_context()
            page = await ctx.new_page()
            print(
                "\nA browser window will open. Sign in to GitHub (incl. SSO/2FA), "
                "then this command will detect the session and save it.\n"
            )
            await page.goto("https://github.com/login")
            # Wait for any github.com page that isn't /login and has a user-login meta.
            await page.wait_for_function(
                """() => {
                    const meta = document.querySelector('meta[name="user-login"]');
                    return meta && meta.getAttribute('content') &&
                        !location.pathname.startsWith('/login') &&
                        location.host === 'github.com';
                }""",
                timeout=300_000,  # 5 min for SSO/2FA
            )
            state = await ctx.storage_state()
            save_storage_state(state, storage_state_path)
            login = await page.evaluate(
                "() => document.querySelector('meta[name=\"user-login\"]').content"
            )
            print(f"Logged in as {login}. Session saved to {storage_state_path} (mode 600).")
        finally:
            await browser.close()
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/unit/test_auth.py -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/auth.py tests/unit/test_auth.py
git commit -m "feat(github_approve_merge): add storage_state save/check + interactive login"
```

---

### Task 15: `actions.process_pr` (per-PR flow)

**Files:**
- Modify: `src/github_approve_merge/actions.py` (append `ProcessResult` + `process_pr`)
- Create: `tests/unit/test_process_pr.py`

This is the central per-PR flow. It composes the Page Objects + detect_state and produces a terminal status. Tests inject a small `FakePRPage` / `FakeFilesPage` so we don't need a live browser here.

- [ ] **Step 1: Write failing tests**

Create `tests/unit/test_process_pr.py`:

```python
from pathlib import Path

import pytest

from github_approve_merge.actions import ProcessResult, process_pr
from github_approve_merge.logging_setup import RunContext
from github_approve_merge.pr_state import PRState, StateFlag
from github_approve_merge.url import PRRef


class FakePage:
    """Minimal stand-in for playwright.Page used by FakePRPage.detect_state seam."""


class FakePRPage:
    def __init__(self, states: list[tuple[PRState, set[StateFlag]]]):
        # Each call to detect_state pops the next pre-canned state.
        self._states = list(states)
        self.merge_clicked = False
        self.merge_when_ready_clicked = False
        self.goto_calls = 0

    async def goto(self, pr: PRRef) -> None:
        self.goto_calls += 1

    async def detect_state(self, me: str | None):
        return self._states.pop(0)

    async def click_merge_and_confirm(self):
        self.merge_clicked = True

    async def click_merge_when_ready(self):
        self.merge_when_ready_clicked = True

    async def wait_for_merged(self, timeout_ms: int = 30_000):
        pass


class FakeFilesPage:
    def __init__(self):
        self.approve_submitted = False

    async def goto(self, pr: PRRef):
        pass

    async def select_approve_and_submit(self):
        self.approve_submitted = True


@pytest.fixture
def ctx(tmp_path: Path) -> RunContext:
    return RunContext(
        run_id="rid",
        run_dir=tmp_path,
        authenticated_login="reviewer-bot",
    )


PR = PRRef("o", "r", 1)


@pytest.mark.asyncio
async def test_merged_state_skips(ctx):
    pr_page = FakePRPage([(PRState.MERGED, set())])
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=FakeFilesPage(),
                              capture=_noop_capture)
    assert result == ProcessResult(status="skipped-merged")
    assert not pr_page.merge_clicked


@pytest.mark.asyncio
async def test_closed_state_skips_warn(ctx):
    pr_page = FakePRPage([(PRState.CLOSED, set())])
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=FakeFilesPage(),
                              capture=_noop_capture)
    assert result.status == "skipped-closed"


@pytest.mark.asyncio
async def test_self_authored_state_skips(ctx):
    pr_page = FakePRPage([(PRState.SELF_AUTHORED, set())])
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=FakeFilesPage(),
                              capture=_noop_capture)
    assert result.status == "skipped-self"


@pytest.mark.asyncio
async def test_conflict_fails(ctx):
    pr_page = FakePRPage([(PRState.CONFLICT, set())])
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=FakeFilesPage(),
                              capture=_noop_capture)
    assert result.status == "failed-conflict"


@pytest.mark.asyncio
async def test_open_mergeable_path(ctx):
    pr_page = FakePRPage([(PRState.OPEN_MERGEABLE, set())])
    fp = FakeFilesPage()
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=fp, capture=_noop_capture)
    assert result.status == "done"
    assert pr_page.merge_clicked
    assert not fp.approve_submitted  # No approve step needed.


@pytest.mark.asyncio
async def test_open_approvable_path_approves_then_merges(ctx):
    # First detect: needs approve. After approve+refresh: mergeable.
    pr_page = FakePRPage([
        (PRState.OPEN_APPROVABLE, set()),
        (PRState.OPEN_MERGEABLE, set()),
    ])
    fp = FakeFilesPage()
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=fp, capture=_noop_capture)
    assert result.status == "done"
    assert fp.approve_submitted
    assert pr_page.merge_clicked


@pytest.mark.asyncio
async def test_already_approved_skips_approve_still_merges(ctx):
    pr_page = FakePRPage([(PRState.OPEN_MERGEABLE, {StateFlag.ALREADY_APPROVED})])
    fp = FakeFilesPage()
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=fp, capture=_noop_capture)
    assert result.status == "done"
    assert not fp.approve_submitted
    assert pr_page.merge_clicked


@pytest.mark.asyncio
async def test_required_pending_uses_merge_when_ready(ctx):
    pr_page = FakePRPage([(PRState.REQUIRED_PENDING, set())])
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=FakeFilesPage(),
                              capture=_noop_capture)
    assert result.status == "done"
    assert pr_page.merge_when_ready_clicked


@pytest.mark.asyncio
async def test_post_approve_state_still_approvable_means_needs_more_reviewers(ctx):
    pr_page = FakePRPage([
        (PRState.OPEN_APPROVABLE, set()),
        (PRState.OPEN_APPROVABLE, set()),  # didn't unlock merge
    ])
    fp = FakeFilesPage()
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=fp, capture=_noop_capture)
    assert result.status == "skipped-needs-more-approvals"
    assert fp.approve_submitted
    assert not pr_page.merge_clicked


@pytest.mark.asyncio
async def test_dry_run_classifies_but_does_not_act(ctx):
    pr_page = FakePRPage([(PRState.OPEN_MERGEABLE, set())])
    fp = FakeFilesPage()
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=fp,
                              capture=_noop_capture, dry_run=True)
    assert result.status == "skipped-merged" or result.status.startswith("skipped-")
    assert not pr_page.merge_clicked
    assert not fp.approve_submitted


@pytest.mark.asyncio
async def test_unexpected_exception_yields_failed_exception(ctx):
    class Boom(FakePRPage):
        async def click_merge_and_confirm(self):
            raise RuntimeError("network gone")
    pr_page = Boom([(PRState.OPEN_MERGEABLE, set())])
    result = await process_pr(ctx, PR, pr_page=pr_page, files_page=FakeFilesPage(),
                              capture=_noop_capture)
    assert result.status == "failed-exception"
    assert "network gone" in result.error_message


async def _noop_capture(_pr_page, _ctx, _pr, _label):
    return None
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/unit/test_process_pr.py -v
```

Expected: `ImportError: cannot import name 'process_pr'`.

- [ ] **Step 3: Implement `process_pr` and `ProcessResult` in `actions.py`**

Append to `src/github_approve_merge/actions.py`:

```python
import logging
import time
from dataclasses import dataclass
from typing import Awaitable, Callable, Protocol

from github_approve_merge.logging_setup import RunContext
from github_approve_merge.pr_state import PRState, StateFlag
from github_approve_merge.url import PRRef


_log = logging.getLogger("gam")


# Mapping from terminal PRState to a status string for state.jsonl.
_STATE_TO_TERMINAL_STATUS: dict[PRState, str] = {
    PRState.MERGED: "skipped-merged",
    PRState.CLOSED: "skipped-closed",
    PRState.DRAFT: "skipped-draft",
    PRState.SELF_AUTHORED: "skipped-self",
    PRState.CONFLICT: "failed-conflict",
    PRState.REQUIRED_FAILING: "failed-required-check",
    PRState.LOCKED: "failed-locked",
}
_TERMINAL_STATES: set[PRState] = set(_STATE_TO_TERMINAL_STATUS)


@dataclass(frozen=True)
class ProcessResult:
    status: str
    error_message: str = ""
    duration_ms: int = 0


# Structural protocols make the action layer browser-agnostic; tests inject fakes.

class PRPageProto(Protocol):
    async def goto(self, pr: PRRef) -> None: ...
    async def click_merge_and_confirm(self) -> None: ...
    async def click_merge_when_ready(self) -> None: ...
    async def wait_for_merged(self, timeout_ms: int = ...) -> None: ...


class FilesPageProto(Protocol):
    async def goto(self, pr: PRRef) -> None: ...
    async def select_approve_and_submit(self) -> None: ...


CaptureFn = Callable[[object, RunContext, PRRef, str], Awaitable[object]]


async def process_pr(
    ctx: RunContext,
    pr: PRRef,
    *,
    pr_page: PRPageProto,
    files_page: FilesPageProto,
    capture: CaptureFn,
    dry_run: bool = False,
) -> ProcessResult:
    """Execute the full per-PR flow described in spec §5.

    - Phase 1: load PR, detect state, short-circuit on any terminal state.
    - Phase 2: if OPEN_APPROVABLE without ALREADY_APPROVED flag, approve and re-detect.
    - Phase 3: merge (either click_merge_and_confirm or click_merge_when_ready).

    Any unexpected exception in the per-PR flow becomes a `failed-exception` result;
    the runner keeps the batch going.

    `dry_run` short-circuits Phase 2/3: we still classify the initial state, but
    we don't click anything. The returned status is a synthetic mapping for
    visibility but no real action was taken.
    """
    started = time.monotonic()
    try:
        await pr_page.goto(pr)
        await capture(pr_page, ctx, pr, "after-load")

        state, flags = await pr_page.detect_state(me=ctx.authenticated_login)

        if state in _TERMINAL_STATES:
            return _result(_STATE_TO_TERMINAL_STATUS[state], started)

        if dry_run:
            return _result(_dry_run_status_for(state, flags), started)

        if state is PRState.OPEN_APPROVABLE and StateFlag.ALREADY_APPROVED not in flags:
            await files_page.goto(pr)
            await files_page.select_approve_and_submit()
            await capture(pr_page, ctx, pr, "after-approve-submit")
            await pr_page.goto(pr)
            state, flags = await pr_page.detect_state(me=ctx.authenticated_login)
            if state in _TERMINAL_STATES:
                return _result(_STATE_TO_TERMINAL_STATUS[state], started)
            if state is PRState.OPEN_APPROVABLE:
                return _result("skipped-needs-more-approvals", started)

        await capture(pr_page, ctx, pr, "before-merge-click")
        if state is PRState.REQUIRED_PENDING:
            await pr_page.click_merge_when_ready()
        else:  # OPEN_MERGEABLE
            await pr_page.click_merge_and_confirm()
        await pr_page.wait_for_merged()
        await capture(pr_page, ctx, pr, "after-merge")
        return _result("done", started)

    except Exception as e:  # broad on purpose: batch must continue
        _log.error("process_pr failed", exc_info=True, extra={"pr": str(pr), "step": "process_pr"})
        return ProcessResult(
            status="failed-exception",
            error_message=repr(e),
            duration_ms=_elapsed(started),
        )


def _result(status: str, started: float) -> ProcessResult:
    return ProcessResult(status=status, duration_ms=_elapsed(started))


def _elapsed(started: float) -> int:
    return int((time.monotonic() - started) * 1000)


def _dry_run_status_for(state: PRState, flags: set[StateFlag]) -> str:
    """In dry-run mode return what the action WOULD have ended in, prefixed with a synthetic marker."""
    if state is PRState.OPEN_APPROVABLE and StateFlag.ALREADY_APPROVED not in flags:
        return "skipped-merged"  # would approve+merge → success-class
    if state in (PRState.OPEN_MERGEABLE, PRState.REQUIRED_PENDING):
        return "skipped-merged"
    return _STATE_TO_TERMINAL_STATUS.get(state, "failed-exception")
```

Note: `detect_state` is called as a method on the `pr_page` parameter, so the protocol needs that method. Update `PRPage` to expose it as a method that delegates to the module-level function:

- [ ] **Step 4: Add `detect_state` as a method on `PRPage`**

Edit `src/github_approve_merge/pages/pr_page.py`. Inside the `PRPage` class, add (after `pr_author_login`):

```python
    async def detect_state(self, *, me: str | None):
        # Delegates to the module-level function for testability.
        from github_approve_merge.pr_state import detect_state as _ds
        return await _ds(self.page, me=me)
```

Also update the protocol in `actions.py` to include `detect_state`:

```python
class PRPageProto(Protocol):
    async def goto(self, pr: PRRef) -> None: ...
    async def detect_state(self, *, me: str | None): ...
    async def click_merge_and_confirm(self) -> None: ...
    async def click_merge_when_ready(self) -> None: ...
    async def wait_for_merged(self, timeout_ms: int = ...) -> None: ...
```

- [ ] **Step 5: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/unit/test_process_pr.py tests/pages/test_pr_page.py -v
```

Expected: all pass.

- [ ] **Step 6: Commit**

```bash
git add src/github_approve_merge/actions.py src/github_approve_merge/pages/pr_page.py tests/unit/test_process_pr.py
git commit -m "feat(github_approve_merge): add process_pr per-PR flow (approve, merge, merge-when-ready)"
```

---

### Task 16: Runner — `runner.py` (batch loop, state.jsonl, summary, signal handler)

**Files:**
- Create: `src/github_approve_merge/runner.py`
- Create: `tests/unit/test_runner.py`

- [ ] **Step 1: Write failing tests**

Create `tests/unit/test_runner.py`:

```python
import json
from pathlib import Path

import pytest

from github_approve_merge.actions import ProcessResult
from github_approve_merge.runner import Runner
from github_approve_merge.url import PRRef


PR1 = PRRef("o", "r", 1)
PR2 = PRRef("o", "r", 2)
PR3 = PRRef("o", "r", 3)


def _make_runner(tmp_path: Path, results: dict[str, ProcessResult]) -> Runner:
    """Build a Runner whose process_pr returns the canned result for each PR."""
    async def fake_process(ctx, pr, **_kwargs):
        return results[str(pr)]
    return Runner(
        logs_dir=tmp_path,
        run_id="20260526-143012-aaaa",
        process_pr_fn=fake_process,
    )


def _read_state(run_dir: Path) -> list[dict]:
    return [json.loads(l) for l in (run_dir / "state.jsonl").read_text().splitlines() if l]


def _read_summary(run_dir: Path) -> dict:
    return json.loads((run_dir / "summary.json").read_text())


@pytest.mark.asyncio
async def test_happy_path(tmp_path: Path):
    runner = _make_runner(tmp_path, {
        "o/r#1": ProcessResult(status="done", duration_ms=100),
        "o/r#2": ProcessResult(status="done", duration_ms=200),
    })
    exit_code = await runner.execute([PR1, PR2])
    assert exit_code == 0
    run_dir = tmp_path / "20260526-143012-aaaa"
    transitions = _read_state(run_dir)
    # 2 queued + 2 in_progress + 2 done = 6 lines
    statuses = [t["status"] for t in transitions]
    assert statuses == ["queued", "queued", "in_progress", "done", "in_progress", "done"]
    summary = _read_summary(run_dir)
    assert summary["exit_code"] == 0
    assert summary["counts"] == {"done": 2, "skipped": 0, "failed": 0}


@pytest.mark.asyncio
async def test_failure_in_one_pr_does_not_stop_batch(tmp_path: Path):
    runner = _make_runner(tmp_path, {
        "o/r#1": ProcessResult(status="failed-conflict"),
        "o/r#2": ProcessResult(status="done"),
    })
    exit_code = await runner.execute([PR1, PR2])
    assert exit_code == 1
    run_dir = tmp_path / "20260526-143012-aaaa"
    summary = _read_summary(run_dir)
    assert summary["counts"] == {"done": 1, "skipped": 0, "failed": 1}


@pytest.mark.asyncio
async def test_resume_skips_done_prs(tmp_path: Path):
    run_dir = tmp_path / "20260526-143012-aaaa"
    run_dir.mkdir()
    (run_dir / "state.jsonl").write_text(
        '{"ts":"...","pr":"o/r#1","status":"queued"}\n'
        '{"ts":"...","pr":"o/r#1","status":"in_progress"}\n'
        '{"ts":"...","pr":"o/r#1","status":"done","duration_ms":100}\n'
        '{"ts":"...","pr":"o/r#2","status":"queued"}\n'
    )

    called: list[str] = []

    async def fake_process(ctx, pr, **_kwargs):
        called.append(str(pr))
        return ProcessResult(status="done")

    runner = Runner(
        logs_dir=tmp_path,
        run_id="20260526-143012-aaaa",
        process_pr_fn=fake_process,
        resume=True,
    )
    exit_code = await runner.execute([PR1, PR2])
    assert exit_code == 0
    assert called == ["o/r#2"]   # PR1 was skipped (already done)


@pytest.mark.asyncio
async def test_warn_class_skip_yields_exit_1(tmp_path: Path):
    runner = _make_runner(tmp_path, {
        "o/r#1": ProcessResult(status="skipped-closed"),
    })
    exit_code = await runner.execute([PR1])
    assert exit_code == 1


@pytest.mark.asyncio
async def test_success_skip_yields_exit_0(tmp_path: Path):
    runner = _make_runner(tmp_path, {
        "o/r#1": ProcessResult(status="skipped-merged"),
    })
    exit_code = await runner.execute([PR1])
    assert exit_code == 0


@pytest.mark.asyncio
async def test_signal_marks_current_as_interrupted(tmp_path: Path):
    """If process_pr raises CancelledError mid-flight, the in-progress PR ends `failed-interrupted`."""
    import asyncio

    async def fake_process(ctx, pr, **_kwargs):
        if str(pr) == "o/r#2":
            raise asyncio.CancelledError()
        return ProcessResult(status="done")

    runner = Runner(
        logs_dir=tmp_path,
        run_id="20260526-143012-aaaa",
        process_pr_fn=fake_process,
    )
    exit_code = await runner.execute([PR1, PR2, PR3])
    assert exit_code == 130

    run_dir = tmp_path / "20260526-143012-aaaa"
    transitions = _read_state(run_dir)
    pr2_terminal = [t for t in transitions if t["pr"] == "o/r#2" and t["status"].startswith("failed")]
    assert pr2_terminal and pr2_terminal[-1]["status"] == "failed-interrupted"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/unit/test_runner.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `runner.py`**

Create `src/github_approve_merge/runner.py`:

```python
from __future__ import annotations

import asyncio
import json
import logging
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Awaitable, Callable

from github_approve_merge.actions import (
    EXIT_CODE_FAILURE,
    EXIT_CODE_INTERRUPTED,
    EXIT_CODE_SUCCESS,
    STATUS_TO_EXIT_CLASS,
    ExitClass,
    ProcessResult,
)
from github_approve_merge.logging_setup import RunContext
from github_approve_merge.url import PRRef

_log = logging.getLogger("gam")

ProcessFn = Callable[..., Awaitable[ProcessResult]]


class Runner:
    """Orchestrates a batch: iterates PRs, writes state.jsonl per transition, writes summary.json."""

    def __init__(
        self,
        *,
        logs_dir: Path,
        run_id: str,
        process_pr_fn: ProcessFn,
        resume: bool = False,
        ctx: RunContext | None = None,
    ):
        self.logs_dir = logs_dir
        self.run_id = run_id
        self.run_dir = logs_dir / run_id
        self.process_pr_fn = process_pr_fn
        self.resume = resume
        self.ctx = ctx or RunContext(run_id=run_id, run_dir=self.run_dir)

    async def execute(self, prs: list[PRRef]) -> int:
        self.run_dir.mkdir(parents=True, exist_ok=True)
        started = _utcnow_iso()
        completed_on_resume = self._load_completed_for_resume() if self.resume else set()

        # Queue every PR up front so a SIGINT before the first one still leaves a record.
        for pr in prs:
            if str(pr) in completed_on_resume:
                continue
            self._append_state(pr, "queued")

        interrupted = False
        results: list[tuple[PRRef, ProcessResult]] = []
        for pr in prs:
            slug = str(pr)
            if slug in completed_on_resume:
                _log.info("resume: skipping already-done PR", extra={"pr": slug, "step": "resume"})
                continue

            self._append_state(pr, "in_progress")
            try:
                result = await self.process_pr_fn(self.ctx, pr)
            except asyncio.CancelledError:
                self._append_state(pr, "failed-interrupted")
                results.append((pr, ProcessResult(status="failed-interrupted")))
                interrupted = True
                break
            self._append_state(pr, result.status, duration_ms=result.duration_ms,
                               error_message=result.error_message)
            results.append((pr, result))

        exit_code = self._compute_exit_code(results, interrupted)
        self._write_summary(started, results, exit_code)
        self._print_summary(results, exit_code)
        return exit_code

    # --- state.jsonl --------------------------------------------------------

    def _state_path(self) -> Path:
        return self.run_dir / "state.jsonl"

    def _append_state(self, pr: PRRef, status: str, *, duration_ms: int = 0,
                      error_message: str = "") -> None:
        record = {"ts": _utcnow_iso(), "pr": str(pr), "status": status}
        if duration_ms:
            record["duration_ms"] = duration_ms
        if error_message:
            record["error"] = error_message
        with self._state_path().open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def _load_completed_for_resume(self) -> set[str]:
        """Read existing state.jsonl (if any) and return the PRs whose latest status is terminal+success-class."""
        path = self._state_path()
        if not path.exists():
            return set()
        latest: dict[str, str] = {}
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue  # tolerate partial last line from SIGINT
            if "pr" in rec and "status" in rec:
                latest[rec["pr"]] = rec["status"]
        done: set[str] = set()
        for pr, status in latest.items():
            cls = STATUS_TO_EXIT_CLASS.get(status)
            if status == "done" or status.startswith("skipped-"):
                done.add(pr)
            elif cls is ExitClass.SUCCESS:
                done.add(pr)
        return done

    # --- summary -----------------------------------------------------------

    def _compute_exit_code(self, results: list[tuple[PRRef, ProcessResult]], interrupted: bool) -> int:
        if interrupted:
            return EXIT_CODE_INTERRUPTED
        for _pr, r in results:
            cls = STATUS_TO_EXIT_CLASS.get(r.status)
            if cls is None or cls is not ExitClass.SUCCESS:
                return EXIT_CODE_FAILURE
        return EXIT_CODE_SUCCESS

    def _write_summary(self, started: str, results: list[tuple[PRRef, ProcessResult]], exit_code: int) -> None:
        counts = Counter()
        for _pr, r in results:
            cls = STATUS_TO_EXIT_CLASS.get(r.status, ExitClass.ERROR)
            if r.status == "done":
                counts["done"] += 1
            elif cls is ExitClass.ERROR:
                counts["failed"] += 1
            else:
                counts["skipped"] += 1
        summary = {
            "run_id": self.run_id,
            "started": started,
            "ended": _utcnow_iso(),
            "exit_code": exit_code,
            "counts": {"done": counts["done"], "skipped": counts["skipped"], "failed": counts["failed"]},
            "prs": [
                {"pr": str(pr), "status": r.status, "duration_ms": r.duration_ms}
                for pr, r in results
            ],
        }
        (self.run_dir / "summary.json").write_text(json.dumps(summary, indent=2))

    def _print_summary(self, results: list[tuple[PRRef, ProcessResult]], exit_code: int) -> None:
        print()
        print(f"=== github_approve_merge summary (run {self.run_id}) ===")
        for pr, r in results:
            print(f"  {str(pr):<60s}  {r.status:<28s}  {r.duration_ms} ms")
        print(f"Exit: {exit_code}")


def _utcnow_iso() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/unit/test_runner.py -v
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/runner.py tests/unit/test_runner.py
git commit -m "feat(github_approve_merge): add Runner (state.jsonl, --resume, summary.json, exit codes, interrupt handling)"
```

---

## Phase 4 — CLI and docs

### Task 17: CLI — `cli.py`

**Files:**
- Create: `src/github_approve_merge/cli.py`
- Create: `tests/unit/test_cli.py`

- [ ] **Step 1: Write failing tests**

Create `tests/unit/test_cli.py`:

```python
import sys
from pathlib import Path

import pytest

from github_approve_merge.cli import build_parser, main


class TestArgs:
    def test_help_smoke(self, capsys):
        parser = build_parser()
        with pytest.raises(SystemExit) as exc:
            parser.parse_args(["--help"])
        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert "gh-approve-merge" in out

    def test_run_with_url(self):
        parser = build_parser()
        ns = parser.parse_args(["run", "https://github.com/o/r/pull/1"])
        assert ns.subcommand == "run"
        assert ns.urls == ["https://github.com/o/r/pull/1"]

    def test_resume_and_urls_conflict_returns_2(self, capsys):
        rc = main(["run", "--resume", "20260526-143012-aaaa",
                   "https://github.com/o/r/pull/1"])
        assert rc == 2
        err = capsys.readouterr().err
        assert "--resume" in err

    def test_no_inputs_returns_2(self, capsys, monkeypatch):
        # When stdin is a TTY and no args/file given.
        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        rc = main(["run"])
        assert rc == 2

    def test_version_flag(self, capsys):
        with pytest.raises(SystemExit) as exc:
            main(["--version"])
        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert "0.1.0" in out

    def test_gc_subcommand_parses(self):
        ns = build_parser().parse_args(["gc", "--retention-days", "5"])
        assert ns.subcommand == "gc"
        assert ns.retention_days == 5

    def test_auth_login_subcommand_parses(self):
        ns = build_parser().parse_args(["auth", "login"])
        assert ns.subcommand == "auth"
        assert ns.auth_subcommand == "login"


class TestRunWiring:
    def test_run_invokes_runner_with_resolved_inputs(self, tmp_path: Path, monkeypatch, capsys):
        # Stub everything heavy: retention.sweep, browser launch, runner execution.
        calls = {}

        async def fake_execute(self, prs):
            calls["prs"] = list(prs)
            return 0

        def fake_sweep(root, max_age_days, skip):
            calls["sweep"] = (root, max_age_days, skip)
            return []

        # Patch the runner factory so the CLI uses a fake.
        from github_approve_merge import cli, retention, runner

        class FakeContext:
            async def __aenter__(self): return self
            async def __aexit__(self, *a): return False
            async def new_page(self): raise AssertionError("should not run")

        from contextlib import asynccontextmanager

        @asynccontextmanager
        async def fake_open_context(**kwargs):
            yield FakeContext()

        monkeypatch.setattr(runner.Runner, "execute", fake_execute)
        monkeypatch.setattr(retention, "sweep", fake_sweep)
        monkeypatch.setattr(cli, "open_context", fake_open_context)

        ss = tmp_path / "ss.json"
        ss.write_text('{"cookies":[],"origins":[]}')

        rc = main([
            "run",
            "https://github.com/o/r/pull/1",
            "--storage-state", str(ss),
            "--logs-dir", str(tmp_path / "logs"),
        ])
        assert rc == 0
        assert [str(p) for p in calls["prs"]] == ["o/r#1"]
        assert calls["sweep"][1] == 10  # default retention days
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
uv run pytest tests/unit/test_cli.py -v
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Implement `cli.py`**

Create `src/github_approve_merge/cli.py`:

```python
from __future__ import annotations

import argparse
import asyncio
import signal
import sys
from pathlib import Path
from typing import Sequence

from github_approve_merge import __version__, retention
from github_approve_merge.actions import (
    EXIT_CODE_FAILURE,
    EXIT_CODE_INTERRUPTED,
    EXIT_CODE_USAGE,
    process_pr,
)
from github_approve_merge.auth import AuthStatus, check_storage_state, interactive_login
from github_approve_merge.browser import StorageStateError, open_context
from github_approve_merge.config import (
    DEFAULT_RETENTION_DAYS,
    DEFAULT_TIMEOUT_SECONDS,
    default_logs_dir,
    default_storage_state_path,
    generate_run_id,
)
from github_approve_merge.input_sources import InputSourceError, collect_urls
from github_approve_merge.logging_setup import RunContext, make_run_logger
from github_approve_merge.pages.files_page import FilesPage
from github_approve_merge.pages.pr_page import PRPage
from github_approve_merge.runner import Runner
from github_approve_merge.screenshots import capture


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gh-approve-merge",
        description="Approve and merge GitHub PRs in batch via Playwright.",
    )
    p.add_argument("--version", action="version", version=f"gh-approve-merge {__version__}")
    sub = p.add_subparsers(dest="subcommand", required=True)

    # auth
    auth = sub.add_parser("auth", help="Manage browser session for github.com.")
    auth_sub = auth.add_subparsers(dest="auth_subcommand", required=True)
    auth_login = auth_sub.add_parser("login", help="Open a headed browser and save session.")
    auth_login.add_argument("--storage-state", type=Path, default=default_storage_state_path())
    auth_status = auth_sub.add_parser("status", help="Show whether the saved session exists.")
    auth_status.add_argument("--storage-state", type=Path, default=default_storage_state_path())

    # run
    run = sub.add_parser("run", help="Approve and merge a batch of PRs.")
    run.add_argument("urls", nargs="*", help="PR URLs (in addition to --file / stdin).")
    run.add_argument("--file", type=Path, default=None,
                     help="Path to a file with one URL per line ('#' comments OK).")
    run.add_argument("--retention-days", type=int, default=DEFAULT_RETENTION_DAYS)
    run.add_argument("--storage-state", type=Path, default=default_storage_state_path())
    run.add_argument("--logs-dir", type=Path, default=default_logs_dir())
    run.add_argument("--run-id", default=None)
    run.add_argument("--resume", default=None, metavar="ID",
                     help="Resume a previous batch by reusing its logs/<ID>/ dir.")
    run.add_argument("--dry-run", action="store_true",
                     help="Classify PR states without clicking anything.")
    run.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    verbosity = run.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", action="store_true")
    verbosity.add_argument("--quiet", action="store_true")

    # gc
    gc = sub.add_parser("gc", help="Run the retention sweep without doing anything else.")
    gc.add_argument("--logs-dir", type=Path, default=default_logs_dir())
    gc.add_argument("--retention-days", type=int, default=DEFAULT_RETENTION_DAYS)

    return p


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.subcommand == "auth":
        if args.auth_subcommand == "login":
            return _cmd_auth_login(args.storage_state)
        if args.auth_subcommand == "status":
            return _cmd_auth_status(args.storage_state)
        return EXIT_CODE_USAGE

    if args.subcommand == "gc":
        deleted = retention.sweep(args.logs_dir, max_age_days=args.retention_days, skip=set())
        print(f"Deleted {len(deleted)} expired run dir(s) under {args.logs_dir}")
        return 0

    if args.subcommand == "run":
        return _cmd_run(args)

    parser.error(f"unknown subcommand: {args.subcommand}")
    return EXIT_CODE_USAGE


def _cmd_auth_login(storage_state_path: Path) -> int:
    try:
        asyncio.run(interactive_login(storage_state_path))
    except KeyboardInterrupt:
        print("Login cancelled.", file=sys.stderr)
        return EXIT_CODE_INTERRUPTED
    return 0


def _cmd_auth_status(storage_state_path: Path) -> int:
    result = check_storage_state(storage_state_path)
    print(f"storage_state: {result.status.value} ({result.message})")
    return 0 if result.status is AuthStatus.PRESENT else EXIT_CODE_FAILURE


def _cmd_run(args) -> int:
    # --resume cannot combine with explicit URLs/file/stdin.
    has_args_input = bool(args.urls) or args.file is not None or not sys.stdin.isatty()
    if args.resume and has_args_input:
        print("error: --resume is mutually exclusive with URLs/--file/stdin", file=sys.stderr)
        return EXIT_CODE_USAGE

    # Collect URLs (unless resuming — in resume mode the URLs come from the existing state.jsonl).
    if args.resume:
        prs = _load_prs_from_state(args.logs_dir / args.resume)
    else:
        try:
            stdin = sys.stdin if not sys.stdin.isatty() else None
            prs = collect_urls(args=args.urls, file_path=args.file, stdin=stdin)
        except InputSourceError as e:
            print(f"error: {e}", file=sys.stderr)
            return EXIT_CODE_USAGE

    run_id = args.resume or args.run_id or generate_run_id()
    run_dir = args.logs_dir / run_id
    ctx = RunContext(run_id=run_id, run_dir=run_dir)
    logger = make_run_logger(ctx, verbose=args.verbose, quiet=args.quiet)

    if not args.dry_run:
        deleted = retention.sweep(args.logs_dir, max_age_days=args.retention_days,
                                  skip={run_dir})
        if deleted:
            logger.info("retention swept %d old run dir(s)", len(deleted),
                        extra={"step": "retention"})

    try:
        return asyncio.run(_run_with_browser(args, ctx, prs))
    except StorageStateError as e:
        logger.error("storage_state error: %s", e, extra={"step": "auth"})
        return EXIT_CODE_FAILURE


async def _run_with_browser(args, ctx: RunContext, prs) -> int:
    async with open_context(
        storage_state_path=args.storage_state,
        headless=True,
        timeout_seconds=args.timeout_seconds,
    ) as bctx:
        # In dry-run mode the capture is a no-op so we leave zero side effects on disk
        # beyond state.jsonl + summary.json (which the spec considers part of the run record).
        capture_fn = _noop_capture if args.dry_run else capture

        # Build a process_pr closure that knows about the live browser context.
        async def process(ctx_, pr):
            page = await bctx.new_page()
            try:
                pr_page = PRPage(page)
                files_page = FilesPage(page)
                # Authenticated login is cached on ctx after the first PR.
                if ctx_.authenticated_login is None:
                    await pr_page.goto(pr)
                    ctx_.authenticated_login = await pr_page.authenticated_login()
                return await process_pr(
                    ctx_, pr,
                    pr_page=pr_page,
                    files_page=files_page,
                    capture=capture_fn,
                    dry_run=args.dry_run,
                )
            finally:
                await page.close()

        runner = Runner(
            logs_dir=args.logs_dir,
            run_id=ctx.run_id,
            process_pr_fn=process,
            resume=bool(args.resume),
            ctx=ctx,
        )
        # Install signal handlers so Ctrl-C surfaces as CancelledError to process_pr.
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, _cancel_current_task)
            except NotImplementedError:
                pass  # Windows
        return await runner.execute(prs)


def _cancel_current_task():
    task = asyncio.current_task()
    if task is not None:
        task.cancel()


async def _noop_capture(_pr_page, _ctx, _pr, _label):
    """Replacement for `capture` in dry-run mode — leaves no screenshot side effects."""
    return None


def _load_prs_from_state(run_dir: Path):
    import json

    from github_approve_merge.url import parse_pr_url

    state_path = run_dir / "state.jsonl"
    if not state_path.exists():
        raise InputSourceError(
            f"--resume target {run_dir} has no state.jsonl — nothing to resume"
        )
    seen: list[str] = []
    seen_set: set[str] = set()
    for line in state_path.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        pr_slug = rec.get("pr")
        if pr_slug and pr_slug not in seen_set:
            seen.append(pr_slug)
            seen_set.add(pr_slug)

    refs = []
    for slug in seen:
        owner_repo, _, number = slug.partition("#")
        owner, repo = owner_repo.split("/", 1)
        refs.append(parse_pr_url(f"https://github.com/{owner}/{repo}/pull/{number}"))
    return refs
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
uv run pytest tests/unit/test_cli.py -v
```

Expected: all pass.

- [ ] **Step 5: Verify the entry point works**

Run:
```bash
uv run gh-approve-merge --version
uv run gh-approve-merge --help
uv run gh-approve-merge gc --logs-dir /tmp/nope-does-not-exist
```

Expected: version `0.1.0`, help text, and `Deleted 0 expired run dir(s) under /tmp/nope-does-not-exist`.

- [ ] **Step 6: Commit**

```bash
git add src/github_approve_merge/cli.py tests/unit/test_cli.py
git commit -m "feat(github_approve_merge): add CLI (auth login/status, run, gc subcommands)"
```

---

### Task 18: Live smoke test scaffold, README, CHANGELOG, fixture-refresh script

**Files:**
- Create: `tests/live/test_smoke.py`
- Create: `scripts/refresh_fixtures.py`
- Create: `README.md`
- Create: `CHANGELOG.md`

- [ ] **Step 1: Write the live smoke test (gated, but in the tree)**

Create `tests/live/test_smoke.py`:

```python
"""Live smoke test.

Skipped by default. Set `PYTEST_LIVE=1` and `LIVE_TEST_PR_URL=https://github.com/...` to run.
The test will REAL-WORLD approve and (auto-)merge the target PR — only point it at a throwaway
PR in a sandbox repo.
"""
import os
import subprocess
import sys

import pytest


@pytest.mark.live
def test_approve_and_merge_throwaway_pr(tmp_path):
    url = os.environ.get("LIVE_TEST_PR_URL")
    if not url:
        pytest.skip("LIVE_TEST_PR_URL not set")
    result = subprocess.run(
        [sys.executable, "-m", "github_approve_merge", "run", url,
         "--logs-dir", str(tmp_path / "logs")],
        capture_output=True, text=True, check=False,
    )
    print(result.stdout)
    print(result.stderr, file=sys.stderr)
    assert result.returncode in (0, 1), f"unexpected exit code {result.returncode}"
```

- [ ] **Step 2: Write the fixture refresh helper**

Create `scripts/refresh_fixtures.py`:

```python
"""Re-snapshot the HTML fixtures from real GitHub pages.

Usage:
    python scripts/refresh_fixtures.py FIXTURE_NAME PR_URL

Example:
    python scripts/refresh_fixtures.py pr_mergeable.html \
        https://github.com/sandbox-org/sandbox-repo/pull/42

This uses your saved storage_state, navigates to PR_URL, waits for the page to
settle, and writes `page.content()` to tests/fixtures/html/FIXTURE_NAME.

Run when fixture-based tests fail after a GitHub UI redesign — review the new
content, sanitise PII (commit hashes, real avatars), and commit.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright

from github_approve_merge.config import default_storage_state_path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "html"


async def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    name, url = sys.argv[1], sys.argv[2]
    target = FIXTURES_DIR / name
    if not name.endswith(".html"):
        print("fixture name must end with .html", file=sys.stderr)
        return 2

    storage_state = default_storage_state_path()
    if not storage_state.exists():
        print(f"missing storage_state at {storage_state}. Run `gh-approve-merge auth login`.",
              file=sys.stderr)
        return 2

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(storage_state=str(storage_state))
        page = await ctx.new_page()
        await page.goto(url, wait_until="networkidle")
        html = await page.content()
        target.write_text(html)
        print(f"wrote {target} ({len(html)} bytes)")
        await browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
```

- [ ] **Step 3: Write `README.md`**

Create `README.md`:

````markdown
# github_approve_merge

Approve and merge a batch of GitHub PRs from the command line, driven by a
real browser via Playwright. Logs every step, captures screenshots, and
survives interruption.

## Install

Requires Python 3.12. Recommended: install with `uv`.

```bash
uv venv
uv pip install -e .
uv run playwright install chromium
```

Or with `pipx`:

```bash
pipx install -e .
playwright install chromium
```

## One-time login

```bash
gh-approve-merge auth login
```

This opens a real Chromium window. Sign in to github.com (SSO/2FA all work).
The session is saved to `~/.config/github_approve_merge/storage_state.json`
with mode `0600`. **Treat this file like a credential** — it grants
PR-merging power on your account.

Check it exists later:

```bash
gh-approve-merge auth status
```

## Approve + merge PRs

Pass URLs as args, via a file, or piped on stdin:

```bash
# Args
gh-approve-merge run \
  https://github.com/acme-org/widgets-service/pull/561 \
  https://github.com/acme-org/api-gateway/pull/101

# File
gh-approve-merge run --file ~/prs.txt

# Pipe
gh pr list --json url -q '.[].url' | gh-approve-merge run
```

A `urls.txt` file looks like:

```
# Comments and blank lines OK
https://github.com/owner/repo/pull/1
https://github.com/owner/repo/pull/2
```

## What it does, per PR

1. Loads the PR page.
2. Inspects the state. If merged / closed / draft / locked / conflict / required-check failing / your own PR — records the result and moves on.
3. If approval is needed (and you haven't already approved): goes to the Files-changed tab, picks "Approve", submits.
4. Goes back to the PR.
5. If required checks are still pending, clicks "Merge when ready" (auto-merge). Otherwise clicks the primary "Merge" button, then "Confirm".

It never opens the merge-method dropdown — whatever GitHub pre-selects (your repo default) is what gets used.

## Where artifacts land

```
./logs/<YYYYMMDD-HHMMSS-rand4>/
  run.jsonl         # every log event
  state.jsonl       # per-PR status transitions
  summary.json      # final summary (also written on Ctrl-C)
  screenshots/      # 4 checkpoints per PR + one on each failure
```

Old run dirs are deleted lazily on every `run` (default: keep 10 days).
Override with `--retention-days N`, or run the sweep alone with
`gh-approve-merge gc`.

## Resume after Ctrl-C / crash

```bash
gh-approve-merge run --resume 20260526-143012-7af3
```

The resumed run skips any PR whose latest status is `done` or `skipped-*`.
Each PR is also re-classified against GitHub before action, so a stale
state file cannot cause double-action.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Every PR ended `done` or `skipped-merged` (success-class). |
| 1 | Any PR ended in a warn-class skip (closed/draft/self/needs-more-approvals) or a failure. |
| 2 | Usage / configuration error before any PR was touched. |
| 130 | Interrupted (SIGINT / SIGTERM). |

## Troubleshooting

- **`storage_state not found`** — run `gh-approve-merge auth login`.
- **Selector resolution failed in CI** — GitHub redesigned a widget. Refresh fixtures with `python scripts/refresh_fixtures.py <name>.html <url>` and update the affected selector in `src/github_approve_merge/pages/selectors.py`.
- **Re-running a failed batch** — `gh-approve-merge run --resume <run-id>`.

## Development

```bash
uv pip install -e ".[dev]"
uv run pytest                       # unit + page-object tests
PYTEST_LIVE=1 LIVE_TEST_PR_URL=https://... uv run pytest tests/live
```

See `docs/superpowers/specs/2026-05-26-github-approve-merge-design.md` for the full design.
````

- [ ] **Step 4: Write `CHANGELOG.md`**

Create `CHANGELOG.md`:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `auth login` / `auth status` / `run` / `gc` subcommands.
- Batch approve + merge of GitHub PRs via Playwright.
- "Merge when ready" auto-merge when required checks are pending.
- PR-state classifier: MERGED / CLOSED / DRAFT / LOCKED / SELF_AUTHORED / CONFLICT / REQUIRED_FAILING / REQUIRED_PENDING / OPEN_MERGEABLE / OPEN_APPROVABLE plus the ALREADY_APPROVED flag.
- JSONL run log (`run.jsonl`) and per-PR state file (`state.jsonl`).
- Checkpoint screenshots (after-load, after-approve-submit, before-merge-click, after-merge) plus on-failure screenshots.
- 10-day lazy-delete retention sweep on every `run`, also runnable via `gc`.
- `--resume <id>` to retry an interrupted batch; idempotency safety net re-checks GitHub state.
- Three-tier test suite: unit (pure logic), Page Object tests against HTML fixtures, opt-in live smoke (`PYTEST_LIVE=1`).
- `scripts/refresh_fixtures.py` helper for re-snapshotting HTML fixtures after GitHub UI changes.

## [0.1.0] - 2026-05-26

Initial scaffold.
```

- [ ] **Step 5: Verify everything still builds and tests pass**

Run:
```bash
uv run pytest -v
```

Expected: all unit + page tests pass. Live test skipped.

- [ ] **Step 6: Commit**

```bash
git add tests/live/test_smoke.py scripts/refresh_fixtures.py README.md CHANGELOG.md
git commit -m "docs(github_approve_merge): add README, CHANGELOG, fixture-refresh script, live smoke test"
```

---

### Task 19: Final integration smoke — `python -m github_approve_merge --help` works end-to-end

**Files:** (no changes — verification + version tag)

- [ ] **Step 1: Verify package is invokable as a module**

Run:
```bash
uv run python -m github_approve_merge --version
uv run python -m github_approve_merge --help
uv run python -m github_approve_merge run --help
uv run python -m github_approve_merge auth --help
uv run python -m github_approve_merge gc --help
```

Expected: all print sensible help and exit 0. No tracebacks.

- [ ] **Step 2: Verify dry-run end-to-end produces the expected artifacts**

```bash
uv run gh-approve-merge run --dry-run \
  https://github.com/owner/repo/pull/1 \
  https://github.com/owner/repo/pull/2 \
  --logs-dir /tmp/gam-smoke
ls /tmp/gam-smoke/*/
cat /tmp/gam-smoke/*/summary.json
rm -rf /tmp/gam-smoke
```

Expected: a `logs/<run_id>/` directory with `run.jsonl`, `state.jsonl`, `summary.json`. `summary.json` has `exit_code: 0` and `counts.done == 0, skipped == 2, failed == 0` (dry-run statuses are all `skipped-merged`).

- [ ] **Step 3: Verify the full test suite still passes**

```bash
uv run pytest -v
```

Expected: every test passes.

- [ ] **Step 4: Tag v0.1.0**

```bash
git tag -a v0.1.0 -m "v0.1.0 — initial scaffold"
```

- [ ] **Step 5: Final commit (if any uncommitted lint fixes etc.)**

```bash
git status   # should be clean; otherwise commit fixes
```

---

## Self-review (done at plan-write time)

- **Spec coverage:** every numbered decision (1–15) and every section (§1–§13) is implemented by at least one task. Verified by walking the table in spec §4: auth=Task 14, "merge when ready"=Tasks 10+15, self-PR=Tasks 12+15, merge method (don't open dropdown)=Task 10's `click_merge_and_confirm` (no dropdown code), sequential concurrency=runner loop (Task 16), screenshots=Tasks 9+15, CLI input shape=Tasks 2+17, browser mode=Tasks 13+14+17, edge matrix=Tasks 12+15, test strategy=Tasks 1-19 collectively, logging=Task 5, retention=Task 4+17, resume=Task 16+17, exit codes=Tasks 6+16, YAGNI=intentionally not represented (negative requirement).
- **Placeholder scan:** no "TBD", no "fill in", every step has runnable code or a verifiable command.
- **Type consistency:** `RunContext`, `PRRef`, `ProcessResult`, `ExitClass`, `PRState`, `StateFlag` are defined exactly once each (Tasks 5, 1, 6+15, 6, 6, 6 respectively) and referenced everywhere by the same name and signature. `process_pr` signature is fixed in Task 15 (`ctx, pr, *, pr_page, files_page, capture, dry_run`) and matched by the runner's `ProcessFn` typing (`Callable[..., Awaitable[ProcessResult]]`) and the CLI's process-closure.
- **Selector source-of-truth:** all selectors live in `pages/selectors.py` (Task 7) and are referenced by name everywhere else.
