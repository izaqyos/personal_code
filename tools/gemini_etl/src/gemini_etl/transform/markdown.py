"""Markdown chunker: frontmatter → header; split on H1/H2/H3 if oversize."""
from __future__ import annotations

import dataclasses
import re
from typing import Callable

import frontmatter

from gemini_etl.transform.header import Chunk, ChunkMetadata, build_header


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
    if isinstance(tags_value, (list, tuple)):
        tags = tuple(tags_value)
    elif isinstance(tags_value, str):
        tags = (tags_value,)
    else:
        tags = ()

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
        # Either no header found at this level, or the whole body is one block.
        # Capture a single header into the section path before diving deeper.
        new_sp = section_path
        if sections and sections[0][0]:
            new_sp = section_path + (sections[0][0],)
        return _split_recursive(
            body=body, section_path=new_sp,
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
    an empty header_line. Section bodies start AFTER the header line — the
    header is captured in section_path metadata, not duplicated in the body."""
    pattern = re.compile(rf"(?m)^{re.escape(prefix)}.*$")
    matches = list(pattern.finditer(body))
    if not matches:
        return [("", body)]

    out: list[tuple[str, str]] = []
    if matches[0].start() > 0:
        preamble = body[:matches[0].start()]
        if _has_prose(preamble):
            out.append(("", preamble))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        # Skip the header line and following newline so the body doesn't
        # duplicate the heading captured in section_path.
        body_start = m.end()
        if body_start < len(body) and body[body_start] == "\n":
            body_start += 1
        out.append((m.group(0).strip(), body[body_start:end]))
    return out


def _has_prose(text: str) -> bool:
    """Return True if *text* contains at least one non-blank, non-header line."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return True
    return False
