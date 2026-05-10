"""Builds the metadata header that prefixes every chunk."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    text: str
    rel_path: str


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
        title_clean = " ".join(meta.title.split())  # strip + collapse whitespace incl. newlines
        if title_clean:
            extras.append(f"[Title: {title_clean}]")

    clean_tags = tuple(t for t in meta.tags if t and t.strip())
    if clean_tags:
        extras.append(f"[Tags: {', '.join(t.strip() for t in clean_tags)}]")

    extra_line = " ".join(extras)

    clean_section = tuple(s for s in meta.section_path if s and s.strip())
    section_line = (
        f"[Section: {' / '.join(s.strip() for s in clean_section)}]"
        if clean_section else ""
    )

    parts = [line1]
    if extra_line:
        parts.append(extra_line)
    if section_line:
        parts.append(section_line)
    parts.append("---")
    return "\n".join(parts)
