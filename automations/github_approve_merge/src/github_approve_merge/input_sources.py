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
