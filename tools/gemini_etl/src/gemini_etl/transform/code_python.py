"""Python code chunker using tree-sitter."""
from __future__ import annotations

from typing import Callable

import tree_sitter as ts
import tree_sitter_python as _tsp

from gemini_etl.transform.header import ChunkMetadata, build_header
from gemini_etl.transform.markdown import Chunk

_PY_LANG = ts.Language(_tsp.language())
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
