"""Walk a source tree, applying ignore rules + extension filter."""
from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from pathspec import GitIgnoreSpec

from gemini_etl.config import Source

ALWAYS_SKIP_DIRS = frozenset({
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    "dist", "build", "target", ".next", ".turbo",
})

# Whitespace-only files larger than one page are vanishingly rare; only
# strip-check small files to avoid the cost of a full read for every file.
_WHITESPACE_CHECK_LIMIT = 4096


@dataclass(frozen=True)
class FileRef:
    source: str
    rel_path: str
    abs_path: Path
    size: int
    sha256: str


def _load_gitignore(root: Path) -> "GitIgnoreSpec":
    """Read root-level ``.gitignore`` only. Nested ``.gitignore`` files are NOT loaded.

    This is sufficient for ``personal_KB`` and ``personal_code``, which are
    shallow trees with root-level ignore rules. If we ever need nested-gitignore
    support, swap this for a per-directory load during ``os.walk``."""
    gi = root / ".gitignore"
    lines: list[str] = []
    if gi.exists():
        lines.extend(gi.read_text(encoding="utf-8").splitlines())
    return GitIgnoreSpec.from_lines(lines)


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
            if size < _WHITESPACE_CHECK_LIMIT:
                if not abs_path.read_bytes().strip():
                    continue

            yield FileRef(
                source=source.name,
                rel_path=rel_path_str,
                abs_path=abs_path,
                size=size,
                sha256=_sha256(abs_path),
            )
