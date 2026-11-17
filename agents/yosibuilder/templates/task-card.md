id: T1
title: feat(text): add slugify helper
edit: src/pkg/text.py tests/unit/test_text.py
read: src/pkg/interfaces.py
test: uv run pytest tests/unit/test_text.py -q
lint: uv run ruff check src/pkg/text.py tests/unit/test_text.py
---
Goal: one sentence on what this card delivers.

## Design (implement exactly these, nothing more)

File src/pkg/text.py, standard library only (re, unicodedata):

    _SEPARATORS = re.compile(r"[^a-z0-9]+")

    def slugify(text: str, max_len: int = 64) -> str
        One-line docstring. Raise ValueError("max_len must be >= 1") if max_len < 1.
        Steps: ascii = _ascii_fold(text).lower(); slug = _SEPARATORS.sub("-", ascii).strip("-");
        return slug[:max_len].rstrip("-").

    def _ascii_fold(text: str) -> str
        NFKD-normalize, encode to ASCII ignoring errors, decode.

## Test plan (write exactly these tests in tests/unit/test_text.py)

    import pytest
    from pkg.text import slugify

test_slugify(text, expected), parametrized:
    ("Hello World", "hello-world")
    ("a__b  c", "a-b-c")
    ("", "")

test_slugify_truncates_without_trailing_dash: slugify("abc def", max_len=4) == "abc"
test_slugify_rejects_non_positive_max_len: pytest.raises(ValueError) for slugify("x", max_len=0)

Constraints: no comments, no other files, functions about 20 lines or fewer, typed.
