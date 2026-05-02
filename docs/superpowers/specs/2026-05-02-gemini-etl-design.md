# Gemini ETL — Personal Repos → Gemini File Search Store

**Status:** design approved 2026-05-02
**Owner:** yosi
**Code root:** `tools/gemini_etl/`

## BLUF

A Python ETL that syncs two personal Git repos (`personal_KB`, `personal_code`)
into a single Gemini File Search Store for RAG retrieval. Hash-based
incremental sync, language-aware chunking, idempotent loading by `display_name`,
SQLite manifest, CLI plus zsh aliases plus launcher integration.

## 1. Goals & non-goals

### Goals

- One-command sync of both repos into a single persistent Gemini File Search
  Store (`yosi-personal-kb`).
- Incremental: only changed files re-uploaded; deleted files removed from the
  store.
- Crash-safe: a Ctrl-C or 429 mid-run does not corrupt state.
- High test coverage (≥ 90 %) with no live API calls in tests.
- First-time-setup is documented end-to-end (API-key → first sync).

### Non-goals (v1)

- Other repos. Sources are hardcoded to `personal_KB` and `personal_code`.
- Content-hash-based rename detection. Renames = delete + add.
- Streaming / push-based sync. The trigger is manual (`gemini-sync`) or
  alias / launcher menu.
- Web UI or query interface. Querying is done via Gemini's File Search API
  directly; this project only loads.

## 2. Architecture

```text
┌─────────────┐   ┌──────────────┐   ┌──────────────────┐
│   extract   │──▶│  transform   │──▶│       load       │
│  (walk +    │   │  (chunk +    │   │  (google-genai   │
│  .gitignore)│   │   metadata)  │   │   uploads)       │
└─────────────┘   └──────────────┘   └──────────────────┘
       │                                       │
       └───────────────┬───────────────────────┘
                       ▼
              ┌──────────────────┐
              │     manifest     │
              │  (~/.gemini_etl/ │
              │ sync_manifest.   │
              │      sqlite)     │
              └──────────────────┘
```

Extract → transform → load are independently testable. The manifest is the
sole stateful component and is updated **after** a successful API write so
the system is crash-safe.

### Directory layout

```text
tools/gemini_etl/
├── README.md
├── CHANGELOG.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── bin/
│   └── gemini-etl               # venv-activating shim, used by zsh aliases
├── src/gemini_etl/
│   ├── __init__.py
│   ├── __main__.py              # python -m gemini_etl
│   ├── cli.py                   # argparse: sync | status | dry-run | reset | verify
│   ├── config.py                # sources, thresholds, store name, paths
│   ├── extract.py               # walk + .gitignore + ext filter → FileRef iterator
│   ├── transform/
│   │   ├── __init__.py          # dispatcher by extension
│   │   ├── markdown.py
│   │   ├── code_python.py       # tree-sitter
│   │   ├── code_generic.py      # regex heuristics
│   │   └── header.py            # metadata-header builder
│   ├── load.py                  # google-genai client + retry/backoff
│   ├── manifest.py              # SQLite read/write + diff
│   └── tokens.py                # Gemini count_tokens helper (cached)
└── tests/
    ├── test_extract.py
    ├── test_transform_markdown.py
    ├── test_transform_code_python.py
    ├── test_transform_code_generic.py
    ├── test_manifest.py
    ├── test_load.py
    ├── test_cli.py
    └── fixtures/
        ├── sample_kb/
        └── sample_code/
```

## 3. Configuration

```python
# config.py — defaults; all overridable via env vars
SOURCES = [
    Source(name="personal_KB",   path="/Users/yosii/work/git/personal_KB",
           extensions={".md"}),
    Source(name="personal_code", path="/Users/yosii/work/git/personal_code",
           extensions={".py", ".js", ".ts", ".c", ".cpp", ".h", ".bash"}),
]
STORE_NAME           = "yosi-personal-kb"
CHUNK_TOKEN_LIMIT    = 10_000
MAX_FILE_SIZE_BYTES  = 2 * 1024**3   # 2 GB Gemini cap
MAX_CONCURRENCY      = 4
STATE_DIR            = "~/.gemini_etl/"
```

**Auth:** `.env` in `tools/gemini_etl/` loaded via `python-dotenv`. `.env`
is gitignored; `.env.example` is committed.

**State location:** `~/.gemini_etl/` (not in the repo) holds:

- `sync_manifest.sqlite` — per-file SHA + Gemini doc IDs
- `store.txt` — cached Gemini store ID for fast reuse

## 4. Manifest schema

```sql
CREATE TABLE files (
  source       TEXT NOT NULL,
  rel_path     TEXT NOT NULL,
  sha256       TEXT NOT NULL,
  display_name TEXT NOT NULL,        -- "{source}/{rel_path}", Gemini doc identity
  document_id  TEXT,                 -- Gemini-returned doc ID, used for delete
  uploaded_at  TEXT NOT NULL,        -- ISO 8601 UTC
  PRIMARY KEY (source, rel_path)
);
```

SQLite is chosen over JSON for atomic per-row writes, no full-file rewrites,
and easy delete-set queries (`WHERE source=?` minus current walk = stale rows).

## 5. Extract

For each `Source`:

1. **Always-skip dirs** — `.git/`, `node_modules/`, `__pycache__/`, `.venv/`,
   `venv/`, `dist/`, `build/`, `target/`, `.next/`, `.turbo/`. Hardcoded.
2. **`.gitignore`** — parsed via `pathspec`, including nested `.gitignore`s.
3. **Extension allowlist** — only files whose suffix ∈ `Source.extensions`.
4. **Size guard** — files > `MAX_FILE_SIZE_BYTES` skipped with a warning.
5. **Empty-file skip** — zero-byte or whitespace-only files skipped silently.

**Output:** iterator of `FileRef(source, rel_path, abs_path, size, sha256)`.
SHA computed once at extract time so transform/load do not re-read the file.

**Delete detection:** after the walk, manifest rows whose `(source, rel_path)`
is not in the live set are deleted from the store and the manifest.

## 6. Transform

Dispatcher in `transform/__init__.py` selects a chunker by extension and
returns `list[Chunk]` where `Chunk = (text, metadata)`.

### 6.1 Markdown (`.md`)

1. Parse YAML frontmatter with `python-frontmatter`. Fields (`title`, `tags`,
   `aliases`, etc.) are folded into the metadata header — not stripped away.
2. Token count via `client.models.count_tokens(...)`. One call per file,
   cached.
3. If `tokens ≤ CHUNK_TOKEN_LIMIT` → one chunk = whole file.
4. Else split on `#` headers; if any section is still too large, recurse to
   `##`, then `###`. Each chunk records its full header path
   (e.g., `"# Foo / ## Bar"`) in metadata.

### 6.2 Python code (`.py`) — tree-sitter

1. Token count first; if under threshold, whole file (no parsing).
2. Else parse with `tree-sitter-python` and extract top-level
   `function_definition` and `class_definition` nodes. Decorators and
   leading docstrings stay attached to their owning def.
3. Module-level prelude (imports, top-level constants) becomes a separate
   "module header" chunk.
4. If a single top-level def itself exceeds the threshold, accept the
   oversize chunk and log a warning. Splitting mid-function is worse than
   oversize.

### 6.3 Generic code (`.js`, `.ts`, `.c`, `.cpp`, `.h`, `.bash`) — regex

Same flow: whole-file if under threshold; otherwise split by language-specific
patterns:

- **JS/TS:** `^(export\s+)?(async\s+)?(function|class|const\s+\w+\s*=\s*(async\s*)?\()`
- **C/C++/headers:** function-signature regex and `^class\s+\w+`
- **Bash:** `^(function\s+\w+|^\w+\s*\(\)\s*\{)`

If a regex-produced chunk still exceeds the threshold, fall back to a
token-windowed split with 10 % overlap. Heuristics are best-effort by design.

### 6.4 Metadata header (prepended to every chunk)

```text
[Source: personal_KB] [Path: notes/algorithms/dp.md] [Type: .md]
[Title: Dynamic Programming] [Tags: algorithms, leetcode]
[Section: # Overview / ## Memoization]
---
<chunk body>
```

Empty fields are omitted, not left blank.

## 7. Load

**SDK:** `google-genai` (the unified Python SDK), not the legacy
`google-generativeai`.

**Store bootstrap (per run):**

1. List `file_search_stores`; find one with `display_name == STORE_NAME`.
2. If absent → `client.file_search_stores.create(display_name=STORE_NAME)`.
3. Cache the returned store name to `~/.gemini_etl/store.txt`.

**Per-file flow** (state from manifest diff):

| State | Action |
| :--- | :--- |
| **New** (not in manifest) | upload → create document → insert manifest row |
| **Changed** (sha differs) | delete old document by `document_id` → upload → create document → update row |
| **Unchanged** | no-op |
| **Deleted** (in manifest, not on disk) | delete document → remove manifest row |

**Idempotency:** `display_name = "{source}/{rel_path}"`. If a previous run
crashed after upload but before manifest write, the next run sees the file
as "new"; before creating, we query-by-display-name and reconcile any
duplicate. Cheap safety net.

**Concurrency:** `concurrent.futures.ThreadPoolExecutor(max_workers=4)`.
The SDK's mature surface is sync; threads are sufficient for I/O-bound work.

**Retries:** `tenacity` with exponential backoff (1 s, 2 s, 4 s, 8 s; max 5
attempts) on `429`, `503`, and connection errors. Other errors fail the
file, log, and continue — they do not abort the whole run.

**Checkpointing:** the manifest row is written **after**
`documents.create()` succeeds. Ctrl-C is safe at any point.

## 8. CLI

`python -m gemini_etl <command> [flags]`. Also exposed as the `gemini-etl`
console script via `pyproject.toml`. (User-facing names like `gemini-sync`
are zsh aliases pointing to `bin/gemini-etl <command>` — see Section 9.1.)

| Command | Behavior |
| :--- | :--- |
| `sync` | Walk → diff → upload/update/delete. Default workflow. |
| `status` | Read-only. Manifest summary; lists pending work without API calls. |
| `dry-run` | Like `sync` but no API calls. Prints `+ added / ~ changed / - deleted`. |
| `reset` | Delete the store + manifest. Requires `--yes`. |
| `verify` | Sanity check: load `.env`, call `client.models.list()`, confirm creds. |

**Common flags:** `--source <name>`, `--limit <N>`, `-v`/`-vv`,
`--no-progress`.

Sample `sync` output:

```text
[gemini-sync] discovering files...
  personal_KB: 412 files (3 new, 7 changed, 2 deleted, 400 unchanged)
  personal_code: 89 files (0 new, 1 changed, 0 deleted, 88 unchanged)

uploading: 100%|████████████████| 11/11 [00:42<00:00,  3.8s/file]

summary:
  added:    3
  updated:  8
  deleted:  2
  failed:   0
  store:    fileSearchStores/abc123 (yosi-personal-kb)
```

## 9. Integration

### 9.1 Zsh aliases

A shim script `tools/gemini_etl/bin/gemini-etl` activates the venv and
forwards args to `python -m gemini_etl`. The user's shell rc adds:

```bash
alias gemini-sync='/Users/yosii/work/git/personal_code/tools/gemini_etl/bin/gemini-etl sync'
alias gemini-status='/Users/yosii/work/git/personal_code/tools/gemini_etl/bin/gemini-etl status'
alias gemini-dry='/Users/yosii/work/git/personal_code/tools/gemini_etl/bin/gemini-etl dry-run'
```

The shim approach keeps the rc file free of venv-activation logic, and
naming the shim/script `gemini-etl` (matching the package) avoids any
collision with the user-facing `gemini-sync` alias.

### 9.2 Launcher (`code/bash/tools/launcher/launcher.sh`)

Following the existing `DAILY_RUNNER` pattern:

1. **Path constants** added near the top:

   ```bash
   GEMINI_ETL_DIR="/Users/yosii/work/git/personal_code/tools/gemini_etl"
   GEMINI_ETL_VENV="$GEMINI_ETL_DIR/.venv"
   ```

2. **Menu entry** "Gemini KB Sync" with sub-options: `sync`, `dry-run`,
   `status`, `verify`, `reset`.
3. **Handler** activates the venv, checks `.env`, calls the chosen command.
   Mirrors the daily-runner handler structure.
4. **Startup warning** when venv missing, matching the existing yellow
   warning style.
5. **CHANGELOG** entry in `code/bash/tools/launcher/CHANGELOG.md`.

## 10. Tests

**Tooling:** `pytest`, `pytest-cov` (`fail_under = 90`), `ruff`,
`mypy --strict` over `src/`.

**No live API calls.** The `google-genai` client is mocked. Fixtures live in
`tests/fixtures/sample_kb/` and `tests/fixtures/sample_code/` (small,
checked-in).

| File | Covers |
| :--- | :--- |
| `test_extract.py` | gitignore respected, always-skip dirs, ext filter, size guard, empty-file skip, SHA correctness |
| `test_transform_markdown.py` | frontmatter folded, single-chunk under threshold, header-split at `#`/`##`/`###`, section-path tracking |
| `test_transform_code_python.py` | top-level def split, decorators+docstrings preserved, oversize-def fallback |
| `test_transform_code_generic.py` | regex split for js/ts/c/cpp/h/bash, oversize fallback to token-window |
| `test_manifest.py` | new/changed/unchanged/deleted diffing, atomic write |
| `test_load.py` | mocked SDK: idempotency by display_name, retry on 429, manifest written *after* upload |
| `test_cli.py` | argparse smoke, dry-run produces no API calls, `--limit` honored |

## 11. First-time setup (for the README)

1. Generate API key at <https://aistudio.google.com/apikey>.
2. `cp tools/gemini_etl/.env.example tools/gemini_etl/.env`, paste key as
   `GEMINI_API_KEY=...`.
3. `cd tools/gemini_etl && python -m venv .venv && source .venv/bin/activate && pip install -e .`
4. `python -m gemini_etl verify` (sanity check creds).
5. `python -m gemini_etl dry-run` (preview the plan).
6. `python -m gemini_etl sync` (do it).
7. From here on: `gemini-sync` (zsh) or launcher menu.

## 12. Delivery checklist

- [ ] Scaffold `tools/gemini_etl/` (`pyproject.toml`, `.env.example`, `.gitignore`)
- [ ] Implement `config`, `extract`, `manifest` (+ tests)
- [ ] Implement `transform/markdown`, `transform/code_python`,
      `transform/code_generic`, `transform/header` (+ tests)
- [ ] Implement `load` with mocked-SDK tests
- [ ] Implement `cli` with all 5 commands
- [ ] Write `README.md` (incl. first-time setup) + `CHANGELOG.md`
- [ ] Wire into `launcher.sh` + add launcher CHANGELOG entry
- [ ] Add `bin/gemini-etl` shim + zsh alias instructions in README
- [ ] Smoke test: `verify` → `dry-run` → `sync` against the real repos

## 13. Open items left to the implementation plan

- Exact zsh-rc file path for alias installation (the user will paste; we
  do not edit shell rc automatically).
- Final `pyproject.toml` dep pins (latest stable at implementation time).
- Concrete tree-sitter-python install path (wheel availability on macOS arm64
  occasionally requires a build dep — confirm during scaffold).
