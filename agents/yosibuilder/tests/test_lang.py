"""Language profiles: inference, test files, planned test names, failure lines, gate programs."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
import lang  # noqa: E402


@pytest.mark.parametrize(("declared", "files", "expected"), [
    ("", ["src/pkg/text.py", "tests/unit/test_text.py"], "python"),
    ("", ["src/slug.ts", "src/slug.spec.ts"], "node"),
    ("", ["src/users/users.service.ts", "src/users/users.controller.ts", "package.json"], "node"),
    ("", ["src/lib.rs", "tests/api.rs"], "rust"),
    ("", ["src/main/java/a/Slug.java", "src/test/java/a/SlugTest.java"], "java"),
    ("", ["src/slug.c", "include/slug.h", "tests/test_slug.c"], "c"),
    ("", ["include/slug.h", "src/slug.cpp", "tests/slug_test.cc"], "cpp"),
    ("nestjs", ["src/a.ts"], "node"),
    ("C++", ["src/a.h"], "cpp"),
    ("ts", ["src/a.js"], "node"),
])
def test_language_for(declared, files, expected):
    assert lang.language_for(declared, files).name == expected


@pytest.mark.parametrize(("declared", "files"), [("cobol", ["a.cbl"]), ("", ["README.md", "Makefile"])])
def test_language_for_rejects_unknown(declared, files):
    with pytest.raises(lang.UnknownLanguage):
        lang.language_for(declared, files)


@pytest.mark.parametrize(("name", "path", "is_test"), [
    ("python", "tests/unit/test_text.py", True),
    ("python", "src/pkg/text.py", False),
    ("node", "src/users/users.service.spec.ts", True),
    ("node", "test/app.e2e-spec.ts", True),
    ("node", "src/__tests__/slug.js", True),
    ("node", "src/users/users.service.ts", False),
    ("rust", "tests/api.rs", True),
    ("rust", "src/lib.rs", False),
    ("java", "src/test/java/a/SlugTest.java", True),
    ("java", "src/main/java/a/Slug.java", False),
    ("c", "tests/test_slug.c", True),
    ("c", "src/slug.c", False),
    ("cpp", "src/slug_test.cc", True),
    ("cpp", "src/slug.cpp", False),
])
def test_is_test(name, path, is_test):
    assert lang.LANGUAGES[name].is_test(path) is is_test


def test_planned_tests_across_styles():
    plan = """
    tests/unit/test_text.py: test_slugify(text, expected); test_rejects_zero
    it("returns empty for blank input"); test('keeps digits')
    TEST(Slug, HandlesEmpty)  TEST_F(SlugFixture, TrimsDashes)
    fn rejects_zero_width()   void rejectsNegative()   TEST_CASE("unicode folds")
    testTruncatesLongInput
    """
    assert lang.planned_tests(plan) == sorted([
        "test_slugify", "test_rejects_zero", "returns empty for blank input", "keeps digits", "HandlesEmpty",
        "TrimsDashes", "rejects_zero_width", "rejectsNegative", "unicode folds", "testTruncatesLongInput"])


@pytest.mark.parametrize(("name", "test", "text", "found"), [
    ("python", "test_x", "def test_x(case):", True),
    ("python", "test_x", "# test_x is planned", False),
    ("node", "returns empty", "it('returns empty', () => {})", True),
    ("node", "returns empty", "it('returns empty list', () => {})", False),
    ("rust", "rejects_zero", "#[test]\nfn rejects_zero() {}", True),
    ("java", "rejectsNegative", "@Test void rejectsNegative() {}", True),
    ("cpp", "HandlesEmpty", "TEST(Slug, HandlesEmpty) {}", True),
])
def test_defines_test(name, test, text, found):
    assert lang.LANGUAGES[name].defines_test(test, text) is found


@pytest.mark.parametrize(("name", "line"), [
    ("python", "FAILED tests/test_a.py::test_x - assert 1 == 2"),
    ("node", "  ● slugify › returns empty"),
    ("node", "src/a.ts(3,5): error TS2322: Type 'string' is not assignable to type 'number'."),
    ("node", "src/a.ts:3:5 - error TS2322: Type 'string' is not assignable"),
    ("node", "  12:3  error  'x' is defined but never used  no-unused-vars"),
    ("rust", "error[E0308]: mismatched types"),
    ("rust", "test tests::rejects_zero ... FAILED"),
    ("java", "[ERROR] Tests run: 3, Failures: 1, Errors: 0, Skipped: 0"),
    ("java", "src/main/java/a/Slug.java:7: error: ';' expected"),
    ("c", "src/slug.c:12:5: error: use of undeclared identifier 'x'"),
    ("cpp", "[  FAILED  ] Slug.HandlesEmpty (0 ms)"),
])
def test_failure_lines(name, line):
    assert lang.LANGUAGES[name].failure_line.match(line)


@pytest.mark.parametrize(("commands", "expected"), [
    (["uv run pytest tests -q", "uv run ruff check src"], ["uv run"]),
    (["npx jest --ci", "npx tsc --noEmit && npx eslint src"], ["npx jest", "npx tsc", "npx eslint"]),
    (["CI=1 npm test -- --runInBand"], ["npm test"]),
    (["cmake -S . -B build && cmake --build build && ctest --test-dir build"], ["cmake", "ctest"]),
    (["cargo test -q", "cargo clippy -- -D warnings"], ["cargo test", "cargo clippy"]),
    (["./gradlew test --no-daemon"], ["./gradlew"]),
    (["cc -Wall -o t t.c a.c && ./t"], ["cc", "./t"]),
])
def test_gate_programs(commands, expected):
    assert lang.gate_programs(*commands) == expected


@pytest.mark.parametrize(("lockfile", "expected"), [
    ("package-lock.json", "npm ci"), ("pnpm-lock.yaml", "pnpm install"), ("yarn.lock", "yarn install"), (None, "")])
def test_node_default_setup(tmp_path, lockfile, expected):
    if lockfile:
        (tmp_path / lockfile).write_text("{}")
    assert lang.NODE.default_setup(tmp_path).startswith(expected)
    assert lang.RUST.default_setup(tmp_path) == ""
