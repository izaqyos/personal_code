"""Language profiles: which files are source and tests, how failures read, what a gate may run, mutation budgets."""

from __future__ import annotations

import re
import shlex
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

_COMPILER_LINE = r"\S+\.(?:c|h|cc|cpp|cxx|hh|hpp|hxx):\d+:\d+: (?:fatal )?error"


@dataclass(frozen=True)
class Language:
    """Everything yb needs to know about one language; the card's test and lint commands stay the card's."""
    name: str
    extensions: tuple[str, ...]
    test_file: re.Pattern[str]
    failure_line: re.Pattern[str]
    test_def: str
    junk: tuple[str, ...]
    mutation_timeout: int
    mutant_mem_mb: int

    def owns(self, path: str) -> bool:
        return Path(path).suffix in self.extensions

    def is_test(self, path: str) -> bool:
        return bool(self.test_file.search(Path(path).as_posix()))

    def defines_test(self, name: str, text: str) -> bool:
        """True if a planned test name is defined (identifiers) or titled (quoted strings) in the test text."""
        if not re.fullmatch(r"\w+", name):
            return re.search(rf"([\"'`]){re.escape(name)}\1", text) is not None
        return re.search(self.test_def.format(name=re.escape(name)), text) is not None

    def default_setup(self, tree: Path) -> str:
        """Command that makes a fresh worktree buildable, or '' when the toolchain needs none."""
        if self.name != "node":
            return ""
        lockfiles = {"pnpm-lock.yaml": "pnpm install --frozen-lockfile --prefer-offline",
                     "yarn.lock": "yarn install --frozen-lockfile --prefer-offline",
                     "package-lock.json": "npm ci --prefer-offline --no-audit --no-fund"}
        return next((command for lock, command in lockfiles.items() if (tree / lock).exists()), "")


PYTHON = Language(
    "python", (".py",),
    re.compile(r"(^|/)(test_[^/]*|[^/]*_test)\.py$"),
    re.compile(r"^(E |FAILED |ERROR |\S+\.py:\d+:\d+: )"),
    r"def {name}\(",
    ("__pycache__/", "*.pyc", ".pytest_cache/", ".ruff_cache/", ".mypy_cache/", ".venv/", "uv.lock"),
    20, 2048)

NODE = Language(
    "node", (".ts", ".tsx", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs"),
    re.compile(r"(^|/)(__tests__|tests?)/|\.(test|spec|e2e-spec)\.[cm]?[jt]sx?$"),
    re.compile(r"^\s*(●|✕|×|✖|FAIL\b|not ok\b|AssertionError|\S+\.[cm]?[jt]sx?(:\d+:\d+| ?\(\d+,\d+\)):? "
               r"(- )?error|\d+:\d+\s+error\b)"),
    r"\b{name}\b",
    ("node_modules/", "dist/", "coverage/", ".turbo/", "*.tsbuildinfo"),
    60, 4096)

RUST = Language(
    "rust", (".rs",),
    re.compile(r"(^|/)(tests|benches)/[^/]*\.rs$"),
    re.compile(r"^(error(\[E\d+\])?:|test \S+ \.\.\. FAILED|thread '.*' panicked|---- \S+ stdout ----"
               r"|\s+--> \S+\.rs:)"),
    r"fn {name}\(",
    ("target/",),
    120, 4096)

JAVA = Language(
    "java", (".java",),
    re.compile(r"(^|/)src/test/|(Test|Tests|IT)\.java$"),
    re.compile(r"^(\[ERROR\]|\S+\.java:\d+: error:|.* > .* FAILED$|Tests run: .*Failures: [1-9]|.*Exception: )"),
    r"\b{name}\s*\(",
    ("target/", "build/", ".gradle/", "out/"),
    180, 4096)

_C_FAILURES = re.compile(rf"^({_COMPILER_LINE}|\[  FAILED  \]|.*Assertion .* failed|.*\*\*\*Failed|"
                         r".*:\d+:.*FAIL|\S+:\d+: Failure$)")

C = Language(
    "c", (".c", ".h"),
    re.compile(r"(^|/)tests?/|(^|/)test_[^/]*\.c$|_test\.c$"),
    _C_FAILURES, r"\b{name}\b",
    ("build/", "cmake-build-*/", "*.o", "*.a", "*.dSYM/"),
    120, 4096)

CPP = Language(
    "cpp", (".cc", ".cpp", ".cxx", ".hh", ".hpp", ".hxx", ".h"),
    re.compile(r"(^|/)tests?/|_(unit)?test\.(cc|cpp|cxx)$|(^|/)test_[^/]*\.(cc|cpp|cxx)$"),
    _C_FAILURES, r"\b{name}\b",
    ("build/", "cmake-build-*/", "*.o", "*.a", "*.dSYM/"),
    120, 4096)

LANGUAGES = {lang.name: lang for lang in (PYTHON, NODE, RUST, JAVA, C, CPP)}
ALIASES = {"py": "python", "js": "node", "javascript": "node", "ts": "node", "typescript": "node",
           "nest": "node", "nestjs": "node", "rs": "rust", "c++": "cpp", "cxx": "cpp"}
_INFERENCE_ORDER = (PYTHON, NODE, RUST, JAVA, CPP, C)  # .h alone means C; with any C++ file it is C++


class UnknownLanguage(ValueError):
    pass


def language_for(declared: str, files: list[str]) -> Language:
    """The card's `lang:` if given, else the language owning most of its files (headers follow C++ when present)."""
    if declared:
        key = ALIASES.get(declared.lower(), declared.lower())
        if key not in LANGUAGES:
            raise UnknownLanguage(f"unknown lang '{declared}'; choose from {', '.join(LANGUAGES)}")
        return LANGUAGES[key]
    suffixes = {Path(name).suffix for name in files}
    if suffixes & set(CPP.extensions) - {".h"}:
        return CPP
    votes = Counter(next((lang.name for lang in _INFERENCE_ORDER if lang.owns(name)), None) for name in files)
    votes.pop(None, None)
    if not votes:
        raise UnknownLanguage(f"cannot infer the language of {' '.join(files)}; add a 'lang:' header")
    return LANGUAGES[votes.most_common(1)[0][0]]


_SEPARATORS = re.compile(r"&&|\|\||;|\|")
_LAUNCHERS = {"npx", "npm", "pnpm", "yarn", "bun", "bunx", "uv", "cargo", "go", "dotnet"}
_ASSIGNMENT = re.compile(r"^[A-Za-z_]\w*=")


def gate_programs(*commands: str) -> list[str]:
    """Command prefixes a worker may run to reproduce the gates: `uv run`, `npx jest`, `cargo test`, `ctest`..."""
    prefixes: list[str] = []
    for command in commands:
        for part in _SEPARATORS.split(command):
            words = [word for word in shlex.split(part) if word] if part.strip() else []
            while words and _ASSIGNMENT.match(words[0]):
                words.pop(0)
            if not words:
                continue
            prefix = " ".join(words[:2]) if words[0] in _LAUNCHERS and len(words) > 1 else words[0]
            if prefix not in prefixes:
                prefixes.append(prefix)
    return prefixes


_PLAN_NAMES = (
    re.compile(r"\b(test(?:_\w+|[A-Z]\w*))(?![\w.])"),                  # test_x, testX (any language)
    re.compile(r"\b(?:fn|void)\s+(\w+)\s*\("),                             # fn name(, void name(
    re.compile(r"\bTEST(?:_F|_P)?\(\s*\w+\s*,\s*(\w+)\s*\)"),              # GoogleTest TEST(Suite, Name)
    re.compile(r"\b(?:it|test|TEST_CASE)\(\s*([\"'`])(.+?)\1"),            # it("title"), TEST_CASE("title")
)


def planned_tests(plan: str) -> list[str]:
    """Test names or titles a card's test plan promises, in any of the supported test styles."""
    names: set[str] = set()
    for pattern in _PLAN_NAMES:
        for match in pattern.finditer(plan):
            names.add(match.group(match.lastindex or 1))
    return sorted(names)
