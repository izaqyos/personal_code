"""Tiny deterministic mutation tester: finds code changes that no test catches."""

from __future__ import annotations

import ast
import os
import signal
import subprocess
from collections.abc import Iterator
from pathlib import Path

LIMIT = 40
TIMEOUT_SECONDS = 20
FLIPS: dict[type[ast.cmpop], type[ast.cmpop]] = {
    ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt, ast.Eq: ast.NotEq, ast.NotEq: ast.Eq,
}


def surviving_mutants(tree: Path, sources: list[str], test_cmd: str) -> list[str]:
    """Return a description of every mutant of the source files that the test command does not kill."""
    survivors: list[str] = []
    for name in sources:
        path = tree / name
        original = path.read_text()
        try:
            for description, mutant in list(mutants(original))[:LIMIT]:
                path.write_text(mutant)
                if _passes(test_cmd, tree):
                    survivors.append(f"{name}:{description}")
        finally:
            path.write_text(original)
    return survivors


def mutants(source: str) -> Iterator[tuple[str, str]]:
    """Yield (description, mutated source): each statement in a function replaced by pass, each comparison flipped."""
    count = len(_targets(ast.parse(source)))
    for index in range(count):
        module = ast.parse(source)
        node = _targets(module)[index]
        description = _describe(source, node)
        mutated = _flip(node) if isinstance(node, ast.Compare) else _ReplaceWithPass(node).visit(module)
        yield description, ast.unparse(ast.fix_missing_locations(mutated if mutated is not None else module))


def _targets(module: ast.Module) -> list[ast.AST]:
    functions = (n for n in ast.walk(module) if isinstance(n, ast.FunctionDef | ast.AsyncFunctionDef))
    return _unique([node for func in functions for node in ast.walk(func)
                    if node is not func and (_is_mutable_statement(node) or _is_flippable(node))])


def _is_flippable(node: ast.AST) -> bool:
    return isinstance(node, ast.Compare) and len(node.ops) == 1 and type(node.ops[0]) in FLIPS


def _is_mutable_statement(node: ast.AST) -> bool:
    if not isinstance(node, ast.stmt) or isinstance(node, ast.Pass):
        return False
    return not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant))


def _unique(nodes: list[ast.AST]) -> list[ast.AST]:
    seen: set[int] = set()
    unique: list[ast.AST] = []
    for node in nodes:
        if id(node) not in seen:
            seen.add(id(node))
            unique.append(node)
    return unique


def _flip(node: ast.Compare) -> None:
    node.ops = [FLIPS[type(node.ops[0])]()]


def _describe(source: str, node: ast.AST) -> str:
    text = (ast.get_source_segment(source, node) or "").splitlines()[0][:80]
    if isinstance(node, ast.Compare):
        op = type(node.ops[0])
        return f"{node.lineno}: flip {op.__name__} to {FLIPS[op].__name__} in `{text}`"
    return f"{node.lineno}: replace `{text}` with pass"


class _ReplaceWithPass(ast.NodeTransformer):
    def __init__(self, target: ast.AST) -> None:
        self.target = target

    def visit(self, node: ast.AST) -> ast.AST:
        if node is self.target:
            return ast.copy_location(ast.Pass(), node)
        return super().visit(node)


def _passes(test_cmd: str, cwd: Path) -> bool:
    """Run the tests in their own process group; a timeout (a mutant that loops forever) kills the whole group."""
    proc = subprocess.Popen(test_cmd, shell=True, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            start_new_session=True)
    try:
        return proc.wait(timeout=TIMEOUT_SECONDS) == 0
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.wait()
        return False
