"""Unified-diff parsing and git diff collection."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


@dataclass
class FileDiff:
    path: str
    old_path: str | None = None
    status: str = "modified"  # added | modified | deleted | renamed
    binary: bool = False
    added_lines: dict[int, str] = field(default_factory=dict)
    removed_count: int = 0
    hunks: list[tuple[int, int]] = field(default_factory=list)  # new-file ranges, inclusive
    text: str = ""

    def touches(self, line: int) -> bool:
        return any(start <= line <= end for start, end in self.hunks)

    @property
    def added_count(self) -> int:
        return len(self.added_lines)


def _strip_prefix(p: str) -> str:
    p = p.strip()
    if p.startswith('"') and p.endswith('"'):
        p = p[1:-1]
    if p.startswith(("a/", "b/")):
        return p[2:]
    return p


def parse_diff(text: str) -> list[FileDiff]:
    files: list[FileDiff] = []
    cur: FileDiff | None = None
    chunk: list[str] = []
    new_line = 0

    def flush() -> None:
        if cur is not None:
            cur.text = "\n".join(chunk)
            files.append(cur)

    for raw in text.splitlines():
        if raw.startswith("diff --git "):
            flush()
            chunk = [raw]
            m = re.match(r"diff --git (\"?a/.+?\"?) (\"?b/.+\"?)$", raw)
            path = _strip_prefix(m.group(2)) if m else raw.split()[-1]
            cur = FileDiff(path=path)
            continue
        if cur is None:
            continue
        chunk.append(raw)
        if raw.startswith("new file mode"):
            cur.status = "added"
        elif raw.startswith("deleted file mode"):
            cur.status = "deleted"
        elif raw.startswith("rename from "):
            cur.old_path = raw[len("rename from ") :]
            cur.status = "renamed"
        elif raw.startswith("rename to "):
            cur.path = raw[len("rename to ") :]
        elif raw.startswith(("Binary files ", "GIT binary patch")):
            cur.binary = True
        elif raw.startswith("--- "):
            if raw[4:].strip() != "/dev/null" and cur.status == "deleted":
                cur.path = _strip_prefix(raw[4:])
        elif raw.startswith("+++ "):
            target = raw[4:].strip()
            if target != "/dev/null":
                cur.path = _strip_prefix(target)
        elif raw.startswith("@@"):
            m = HUNK_RE.match(raw)
            if m:
                start = int(m.group(3))
                count = int(m.group(4)) if m.group(4) is not None else 1
                cur.hunks.append((start, start + max(count, 1) - 1))
                new_line = start
        elif cur.hunks:
            if raw.startswith("+"):
                cur.added_lines[new_line] = raw[1:]
                new_line += 1
            elif raw.startswith("-"):
                cur.removed_count += 1
            elif raw.startswith("\\"):
                pass  # "\ No newline at end of file"
            else:
                new_line += 1
    flush()
    return files


class GitError(RuntimeError):
    pass


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise GitError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def collect_diff(repo: Path, base: str, include_uncommitted: bool = False) -> str:
    """Diff of the branch against its merge-base with `base`.

    With include_uncommitted, compares merge-base to the working tree, so local
    reviews also see staged and unstaged edits to tracked files.
    """
    merge_base = _git(repo, "merge-base", base, "HEAD").strip()
    args = [
        "diff",
        "--no-color",
        "--no-ext-diff",
        "--find-renames",
        "--unified=3",
        merge_base,
    ]
    if not include_uncommitted:
        args.append("HEAD")
    return _git(repo, *args)
