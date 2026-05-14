"""Transform pipeline: file → list[Chunk]."""
from __future__ import annotations

from typing import Callable

from gemini_etl.transform.code_generic import chunk_generic
from gemini_etl.transform.code_python import chunk_python
from gemini_etl.transform.header import Chunk
from gemini_etl.transform.markdown import chunk_markdown

__all__ = ["Chunk", "chunk_file"]


_GENERIC_EXTS = {".js", ".ts", ".c", ".cpp", ".h", ".bash"}


def chunk_file(
    *,
    text: str,
    ext: str,
    source: str,
    rel_path: str,
    token_limit: int,
    count_tokens: Callable[[str], int],
) -> list[Chunk]:
    if ext == ".md":
        return chunk_markdown(
            text=text, source=source, rel_path=rel_path,
            token_limit=token_limit, count_tokens=count_tokens,
        )
    if ext == ".py":
        return chunk_python(
            text=text, source=source, rel_path=rel_path,
            token_limit=token_limit, count_tokens=count_tokens,
        )
    if ext in _GENERIC_EXTS:
        return chunk_generic(
            text=text, source=source, rel_path=rel_path, ext=ext,
            token_limit=token_limit, count_tokens=count_tokens,
        )
    raise ValueError(f"unsupported extension: {ext}")
