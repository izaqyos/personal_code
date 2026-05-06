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
