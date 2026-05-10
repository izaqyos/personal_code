"""Python code chunker using tree-sitter."""
from __future__ import annotations

import logging
import threading
from typing import Callable

import tree_sitter as ts
import tree_sitter_python as _tsp

from gemini_etl.transform.header import Chunk, ChunkMetadata, build_header

log = logging.getLogger(__name__)

_PY_LANG = ts.Language(_tsp.language())
_local = threading.local()


def _get_parser() -> ts.Parser:
    """Return a thread-local Parser. tree-sitter Parser is not thread-safe;
    Language objects are read-only and safe to share."""
    if not hasattr(_local, "parser"):
        _local.parser = ts.Parser(_PY_LANG)
    parser: ts.Parser = _local.parser
    return parser


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

    src_bytes = text.encode("utf-8")
    tree = _get_parser().parse(src_bytes)
    root = tree.root_node

    chunks: list[Chunk] = []
    pending_other: list[bytes] = []

    def _flush_pending() -> None:
        if pending_other:
            prelude_text = b"".join(pending_other).decode("utf-8").strip()
            if prelude_text:
                chunks.append(_wrap(prelude_text, source, rel_path))
            pending_other.clear()

    for child in root.children:
        if child.type in {
            "function_definition", "class_definition", "decorated_definition",
        }:
            _flush_pending()
            body = src_bytes[child.start_byte:child.end_byte].decode("utf-8")
            if count_tokens(body) > token_limit:
                log.warning(
                    "oversize def in %s: chunk exceeds token_limit=%d (using as-is)",
                    rel_path, token_limit,
                )
            chunks.append(_wrap(body, source, rel_path))
        else:
            pending_other.append(
                src_bytes[child.start_byte:child.end_byte] + b"\n"
            )

    _flush_pending()
    return chunks


def _wrap(body: str, source: str, rel_path: str) -> Chunk:
    meta = ChunkMetadata(source=source, rel_path=rel_path, ext=".py")
    return Chunk(text=build_header(meta) + "\n" + body.strip(), rel_path=rel_path)
