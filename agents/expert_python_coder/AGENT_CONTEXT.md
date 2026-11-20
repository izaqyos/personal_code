# expert_python_coder — Agent Context

Read by the agent on every invocation. Supplements `SKILL.md` with commands, config and checklists.

---

## Tool commands (uv first, no global installs)

`uv` is installed; the tools below run without installing anything globally.
If the project has its own venv / `pyproject.toml` dev dependencies, use those instead.

| Purpose | Command |
|---------|---------|
| Tests + coverage | `uv run --with pytest --with pytest-cov pytest --cov=<pkg_or_module> --cov-branch --cov-report=term-missing` |
| Lint | `uvx ruff check .` |
| Format check | `uvx ruff format --check .` (apply with `uvx ruff format .`) |
| Types | `uv run --with mypy mypy --strict <paths>` (drop `--strict` for an existing untyped codebase) |
| Property tests (optional) | add `--with hypothesis` to the pytest command |

Coverage target: **≥ 90% line and branch** on new code. Report the actual number.
If a tool is unavailable (offline, no uv), say so in the report; don't claim it passed.

---

## Default layout for new code

Single module (interview, small tool):
```
solution.py
test_solution.py
```

Package:
```
pyproject.toml
src/<pkg>/__init__.py
src/<pkg>/<module>.py
tests/test_<module>.py
```

Minimal `pyproject.toml` tool config when the repo has none:
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP", "SIM", "C4", "RET", "PTH", "PL", "RUF"]

[tool.pytest.ini_options]
addopts = "-q"

[tool.coverage.run]
branch = true

[tool.coverage.report]
show_missing = true
fail_under = 90
```

---

## Testing checklist

- [ ] Happy path, one test per behavior (not per function).
- [ ] Edge cases: empty, one element, duplicates, boundaries (0, -1, max), unicode, very large input.
- [ ] Error paths: each documented exception is raised with a clear message (`pytest.raises(..., match=...)`).
- [ ] Parametrized tables for input → output cases.
- [ ] No real network, clock or filesystem: `monkeypatch`, `tmp_path`, injected clocks, fakes over mocks.
- [ ] Deterministic: seeded randomness, no sleeps, no order dependence between tests.
- [ ] For algorithms: a brute-force oracle on random small inputs when cheap.
- [ ] Test names read as sentences: `test_expired_entries_are_evicted_first`.

---

## Review checklist (run on every diff before reporting)

- [ ] Does each function do one thing, and does its name say what?
- [ ] Any dead code, unused variables, unreachable branches or guards for excluded inputs? Delete them.
- [ ] Any resource opened without `with`? Any exception swallowed?
- [ ] Any mutable default argument, shared mutable state, or hidden global?
- [ ] Types on every signature; `X | None` handled where it can be None.
- [ ] Complexity reasonable for the stated input size?
- [ ] Would a reader new to the code understand it in one pass?

---

## Common Python traps (for review and drill modes)

| Trap | Example | Fix |
|------|---------|-----|
| Mutable default argument | `def add(x, items=[])` | default to `None`, create the list inside the function |
| Late-binding closures | `[lambda: i for i in range(3)]` all return 2 | `lambda i=i: i` or `functools.partial` |
| Modifying a list while iterating | `for x in xs: xs.remove(x)` | iterate a copy or build a new list |
| Iterator exhaustion | reusing a generator / `map` / file object twice | materialize with `list()` or recreate |
| `is` vs `==` | `if x is 1000`, `if s is "abc"` | `==` for values; `is` only for `None`/singletons |
| Truthiness bug | `if count:` when 0 is valid | `if count is not None:` |
| Off-by-one / slicing | `range(len(xs) - 1)` skipping the last item | check boundaries with a 1-element input |
| Integer vs float division | `/` where `//` was meant (or the reverse) | be explicit |
| Shadowing builtins | `list = ...`, `id = ...`, `input = ...` | rename |
| Bare / broad except | `except: pass` hides `KeyboardInterrupt` and real bugs | catch the specific exception |
| Resource leak | `open()` without `with`; connection not closed on error | context manager |
| Dict mutation during iteration | `for k in d: del d[k]` → RuntimeError | iterate `list(d)` |
| Shared class attribute | `class A: items = []` shared by all instances | set in `__init__` |
| Copy confusion | `b = a` or shallow `copy()` of nested lists | `copy.deepcopy` when nested |
| `[[0] * n] * m` | rows alias the same list | `[[0] * n for _ in range(m)]` |
| String building in a loop | `s += piece` in a hot loop | `"".join(parts)` |
| Default `dict.get` misuse | `d.get(k) or default` when the value can be falsy | `d.get(k, default)` |
| Float equality | `0.1 + 0.2 == 0.3` | `math.isclose` |
| Timezone-naive datetimes | `datetime.now()` compared with aware times | `datetime.now(tz=UTC)` |
| Async misuse | missing `await`; blocking call (`time.sleep`, `requests`) inside `async def` | `await`, `asyncio.sleep`, an async client |
| Recursion depth | deep recursion on large input | iterative version |
| Return in `finally` | swallows the exception | don't return from `finally` |
| `sort` vs `sorted` | `xs = xs.sort()` → None | `xs.sort()` or `xs = sorted(xs)` |
| Unpinned / wrong exception order | `except Exception` before `except ValueError` | most specific first |
