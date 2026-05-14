"""Regex-based chunker for non-Python code, with token-window fallback."""
from __future__ import annotations

import re
from typing import Callable

from gemini_etl.transform.header import Chunk, ChunkMetadata, build_header

# Heuristics: per-extension top-level definition starters. These are
# best-effort and will over-split (e.g. JS `const X = ...` for every module
# constant) or under-split (e.g. multi-line C return types) on real code.
# Cost is a few extra chunks; never lost content.
_PATTERNS: dict[str, re.Pattern[str]] = {
    ".js": re.compile(
        r"^(export\s+)?(async\s+)?(function\s+\w+|class\s+\w+|const\s+\w+\s*=)",
        re.MULTILINE,
    ),
    ".ts": re.compile(
        r"^(export\s+)?(async\s+)?(function\s+\w+|class\s+\w+|const\s+\w+\s*=)",
        re.MULTILINE,
    ),
    ".c":   re.compile(
        r"^(?!for\b|if\b|while\b|switch\b|do\b|return\b)[\w\s\*]+\w+\s*\([^)]*\)\s*\{",
        re.MULTILINE,
    ),
    ".cpp": re.compile(
        r"^((?!for\b|if\b|while\b|switch\b|do\b|return\b)[\w\s\*]+\w+\s*\([^)]*\)\s*\{|class\s+\w+)",
        re.MULTILINE,
    ),
    ".h":   re.compile(
        r"^((?!for\b|if\b|while\b|switch\b|do\b|return\b)[\w\s\*]+\w+\s*\([^)]*\)\s*[\{;]|class\s+\w+)",
        re.MULTILINE,
    ),
    ".bash": re.compile(r"^(function\s+\w+|\w+\s*\(\)\s*\{)", re.MULTILINE),
}

# 10 % overlap — retains boundary context for RAG retrieval without
# materially doubling the chunk count.
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
        return _window_chunks(text, source, rel_path, ext, token_limit, count_tokens)

    sections = _split_on_pattern(text, pattern)
    # When the regex genuinely couldn't split (one section), we fall back to
    # a token-windowed split. When it DID split, we keep each section whole
    # even if oversized — preserving the semantic boundary is more valuable
    # for RAG retrieval than rigid size compliance.
    only_one_section = len(sections) == 1
    chunks: list[Chunk] = []
    for body in sections:
        if not body.strip():
            continue
        if only_one_section and count_tokens(body) > token_limit:
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
    text: str,
    source: str,
    rel_path: str,
    ext: str,
    token_limit: int,
    count_tokens: Callable[[str], int],
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


def _wrap(body: str, source: str, rel_path: str, ext: str) -> Chunk:
    meta = ChunkMetadata(source=source, rel_path=rel_path, ext=ext)
    return Chunk(text=build_header(meta) + "\n" + body.strip(), rel_path=rel_path)
