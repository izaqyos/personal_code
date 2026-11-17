"""Lexical mutants for C-like languages (C, C++, Java, JavaScript/TypeScript, Rust).

Two operators, mirroring the Python AST mutator: flip a comparison or boolean operator, and delete a simple
statement (assignment, increment, call, throw, break, continue). Comments, strings and preprocessor lines are
never touched. A `<`/`>` is flipped only with spaces on both sides, so generics (`Vec<i32>`, `List<String>`) and
includes are left alone. In Rust, everything from `#[cfg(test)]` on is the test module and is skipped.
"""

from __future__ import annotations

import re
from collections.abc import Iterator

_STRING = r'"(?:\\.|[^"\\])*"'
_TEMPLATE = r"`(?:\\.|[^`\\])*`"
_COMMENT = r"//[^\n]*|/\*.*?\*/"
_ANY_QUOTE = r"'(?:\\.|[^'\\\n])*'"
_RUST_CHAR = r"'(?:\\u\{[0-9a-fA-F]+\}|\\.|[^'\\\n])'"
_RUST_RAW = r'r(#*)".*?"\1'
_OPERATOR = re.compile(r"===|!==|<<=|>>=|==|!=|<=|>=|&&|\|\||<<|>>|->|=>|::|<|>")
FLIPS = {"===": "!==", "!==": "===", "==": "!=", "!=": "==", "<=": "<", ">=": ">", "<": "<=", ">": ">=",
         "&&": "||", "||": "&&"}
_SPACED_ONLY = {"<", ">"}
_LVALUE = r"\*?\s*[A-Za-z_$][\w$]*(?:(?:\.|->|::|\?\.)[A-Za-z_$][\w$]*|\[[^\]]*\])*"
_STATEMENT = re.compile(
    rf"^(?:await\s+)?(?:{_LVALUE}\s*(?:[-+*/%&|^]|<<|>>)?=(?!=).+"
    rf"|(?:\+\+|--){_LVALUE}|{_LVALUE}(?:\+\+|--)"
    rf"|{_LVALUE}\s*\(.*\)"
    r"|throw\b.+|break|continue);$")


def mutants(source: str, rust: bool = False) -> Iterator[tuple[str, str]]:
    """Yield (description, mutated source) for every operator flip and simple-statement deletion, in file order."""
    end = source.find("#[cfg(test)]") if rust else -1
    code = _blank_literals(source[:end] if end >= 0 else source, rust)
    found = [*_flips(source, code), *_deletions(source, code)]
    for _, description, mutated in sorted(found):
        yield description, mutated


def _blank_literals(source: str, rust: bool) -> str:
    """Same text with comments, strings and preprocessor lines replaced by spaces (newlines kept)."""
    literals = [_COMMENT, _RUST_RAW, _STRING, _RUST_CHAR] if rust else [_COMMENT, _STRING, _TEMPLATE, _ANY_QUOTE]
    pattern = re.compile("|".join(literals) + r"|^[ \t]*#[^\n]*", re.DOTALL | re.MULTILINE)
    return pattern.sub(lambda m: re.sub(r"[^\n]", " ", m.group()), source)


def _flips(source: str, code: str) -> Iterator[tuple[int, str, str]]:
    for match in _OPERATOR.finditer(code):
        op, start, stop = match.group(), match.start(), match.end()
        if op not in FLIPS:
            continue
        if op in _SPACED_ONLY and not (code[start - 1:start].isspace() and code[stop:stop + 1].isspace()):
            continue
        line = _line_of(source, start)
        description = f"{line[0]}: flip `{op}` to `{FLIPS[op]}` in `{line[1]}`"
        yield start, description, source[:start] + FLIPS[op] + source[stop:]


def _deletions(source: str, code: str) -> Iterator[tuple[int, str, str]]:
    depth, offset = 0, 0
    for code_line in code.splitlines(keepends=True):
        text = code_line.strip()
        if depth > 0 and _STATEMENT.match(text):
            start = offset + code_line.index(text)
            stop = start + len(text)
            line = _line_of(source, start)
            yield start, f"{line[0]}: delete `{line[1]}`", source[:start] + source[stop:]
        depth += code_line.count("{") - code_line.count("}")
        offset += len(code_line)


def _line_of(source: str, index: int) -> tuple[int, str]:
    number = source.count("\n", 0, index) + 1
    start = source.rfind("\n", 0, index) + 1
    stop = source.find("\n", index)
    return number, source[start:stop if stop >= 0 else None].strip()[:80]
