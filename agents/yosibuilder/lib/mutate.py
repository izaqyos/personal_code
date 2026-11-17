"""Tiny deterministic mutation tester: finds code changes that no test catches (Python AST, C-like lexical)."""

from __future__ import annotations

import ast
import contextlib
import os
import signal
import subprocess
import time
from collections.abc import Iterator
from pathlib import Path

import mutate_lex

LIMIT = 40
TIMEOUT_SECONDS = 20
MEMORY_LIMIT_MB = int(os.environ.get("YB_MUTANT_MEM_MB", "2048"))
POLL_SECONDS = 0.25
FLIPS: dict[type[ast.cmpop], type[ast.cmpop]] = {
    ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt, ast.Eq: ast.NotEq, ast.NotEq: ast.Eq,
}


def surviving_mutants(tree: Path, sources: list[str], test_cmd: str, *, limit: int | None = None,
                      timeout: float | None = None, mem_mb: float | None = None) -> list[str]:
    """Return a description of every mutant of the source files that the test command does not kill."""
    survivors: list[str] = []
    for name in sources:
        path = tree / name
        original = path.read_text()
        try:
            for description, mutant in list(mutants_for(name, original))[:LIMIT if limit is None else limit]:
                path.write_text(mutant)
                if _passes(test_cmd, tree, timeout, mem_mb):
                    survivors.append(f"{name}:{description}")
        finally:
            path.write_text(original)
    return survivors


def mutants_for(name: str, source: str) -> Iterator[tuple[str, str]]:
    """Mutants of one source file: Python through its AST, every other language lexically."""
    if name.endswith(".py"):
        return mutants(source)
    return mutate_lex.mutants(source, rust=name.endswith(".rs"))


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


def _passes(test_cmd: str, cwd: Path, timeout: float | None = None, mem_mb: float | None = None) -> bool:
    """Run the tests in their own process group and kill the whole group on every way out.

    A mutant can loop forever or allocate without bound (e.g. `start = end` replaced by pass in an
    append loop), so the group is killed when it times out, when it outgrows MEMORY_LIMIT_MB, and in
    `finally` when this process is interrupted (Ctrl-C, or SIGTERM via exit_on_signals) -- otherwise the
    group, being in its own session, outlives us and eats the machine (17/11 kernel panic).
    """
    proc = subprocess.Popen(test_cmd, shell=True, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            start_new_session=True, env=_mutant_env())
    deadline = time.monotonic() + (TIMEOUT_SECONDS if timeout is None else timeout)
    limit = MEMORY_LIMIT_MB if mem_mb is None else mem_mb
    try:
        while time.monotonic() < deadline:
            try:
                return proc.wait(timeout=POLL_SECONDS) == 0
            except subprocess.TimeoutExpired:
                if _group_rss_mb(proc.pid) > limit:
                    return False
        return False
    finally:
        _kill_group(proc)


def _mutant_env() -> dict[str, str]:
    """No build daemons: a Gradle daemon leaves the process group, so killing the group would not stop it."""
    env = dict(os.environ)
    env["GRADLE_OPTS"] = f"{env.get('GRADLE_OPTS', '')} -Dorg.gradle.daemon=false".strip()
    return env


def _kill_group(proc: subprocess.Popen[bytes]) -> None:
    with contextlib.suppress(ProcessLookupError):
        os.killpg(proc.pid, signal.SIGKILL)
    proc.wait()


def _group_rss_mb(pgid: int) -> float:
    """Resident memory of every process in the group, in MB (macOS has no enforced RLIMIT_AS)."""
    out = subprocess.run(["ps", "-axo", "pgid=,rss="], capture_output=True, text=True).stdout
    kb = sum(int(rss) for group, rss in (line.split() for line in out.splitlines() if line.strip())
             if int(group) == pgid)
    return kb / 1024


def exit_on_signals() -> None:
    """Turn SIGTERM/SIGHUP into SystemExit so `finally` blocks run: mutant groups die, sources are restored."""
    def handler(signum: int, _frame: object) -> None:
        raise SystemExit(128 + signum)
    for sig in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, handler)
