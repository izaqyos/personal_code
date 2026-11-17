"""End to end with real toolchains: a weak test leaves a mutant alive, a strong test kills every mutant.

Each project has `is_adult(age) = age >= 18`. The weak test only checks 30 (so `>=` -> `>` survives); the strong
test checks the boundary 18 and 17. A toolchain that is not installed is skipped.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
import mutate  # noqa: E402

WEAK, STRONG = "weak", "strong"


def _works(*command: str) -> bool:
    return shutil.which(command[0]) is not None and subprocess.run(command, capture_output=True).returncode == 0


def _node(tree: Path, kind: str) -> tuple[list[str], str]:
    (tree / "src").mkdir()
    (tree / "src/age.ts").write_text("export function isAdult(age: number): boolean {\n  return age >= 18;\n}\n")
    checks = "assert.equal(isAdult(30), true);" if kind == WEAK else \
        "assert.equal(isAdult(18), true);\n  assert.equal(isAdult(17), false);"
    (tree / "age.test.ts").write_text(
        "import { test } from 'node:test';\nimport assert from 'node:assert/strict';\n"
        f"import {{ isAdult }} from './src/age.ts';\n\ntest('isAdult', () => {{\n  {checks}\n}});\n")
    return ["src/age.ts"], "node --test age.test.ts"


def _rust(tree: Path, kind: str) -> tuple[list[str], str]:
    (tree / "src").mkdir()
    (tree / "Cargo.toml").write_text('[package]\nname = "age"\nversion = "0.1.0"\nedition = "2021"\n')
    checks = "assert!(is_adult(30));" if kind == WEAK else "assert!(is_adult(18));\n        assert!(!is_adult(17));"
    (tree / "src/lib.rs").write_text(
        "pub fn is_adult(age: u32) -> bool {\n    age >= 18\n}\n\n#[cfg(test)]\nmod tests {\n    use super::*;\n\n"
        f"    #[test]\n    fn boundary() {{\n        {checks}\n    }}\n}}\n")
    return ["src/lib.rs"], f"cargo test --offline -q --target-dir {tree / 'target'}"


def _c_like(tree: Path, kind: str, ext: str, compiler: str) -> tuple[list[str], str]:
    (tree / f"age.{ext}").write_text("int is_adult(int age) {\n    return age >= 18;\n}\n")
    checks = "if (!is_adult(30)) return 1;" if kind == WEAK else \
        "if (!is_adult(18)) return 1;\n    if (is_adult(17)) return 2;"
    (tree / f"test_age.{ext}").write_text(
        f"int is_adult(int age);\n\nint main(void) {{\n    {checks}\n    return 0;\n}}\n")
    return [f"age.{ext}"], f"{compiler} -Wall -Werror -o t test_age.{ext} age.{ext} && ./t"


def _java(tree: Path, kind: str) -> tuple[list[str], str]:
    (tree / "Age.java").write_text("final class Age {\n    static boolean isAdult(int age) {\n"
                                   "        return age >= 18;\n    }\n}\n")
    checks = "if (!Age.isAdult(30)) System.exit(1);" if kind == WEAK else \
        "if (!Age.isAdult(18)) System.exit(1);\n        if (Age.isAdult(17)) System.exit(2);"
    (tree / "AgeTest.java").write_text(
        f"final class AgeTest {{\n    public static void main(String[] args) {{\n        {checks}\n    }}\n}}\n")
    return ["Age.java"], "javac -d out Age.java AgeTest.java && java -cp out AgeTest"


PROJECTS = {
    "node": (_node, ("node", "--version")),
    "rust": (_rust, ("cargo", "--version")),
    "c": (lambda tree, kind: _c_like(tree, kind, "c", "cc"), ("cc", "--version")),
    "cpp": (lambda tree, kind: _c_like(tree, kind, "cpp", "c++ -std=c++20"), ("c++", "--version")),
    "java": (_java, ("javac", "-version")),
}


@pytest.mark.parametrize("language", PROJECTS)
@pytest.mark.parametrize(("kind", "survives"), [(WEAK, True), (STRONG, False)])
def test_mutation_gate_with_real_toolchain(tmp_path, language, kind, survives):
    build, probe = PROJECTS[language]
    if not _works(*probe):
        pytest.skip(f"{probe[0]} not installed")
    sources, test_cmd = build(tmp_path, kind)
    assert subprocess.run(test_cmd, shell=True, cwd=tmp_path, capture_output=True).returncode == 0, "baseline green"
    original = (tmp_path / sources[0]).read_text()

    survivors = mutate.surviving_mutants(tmp_path, sources, test_cmd, timeout=120, mem_mb=4096)

    if survives:
        assert any("flip `>=` to `>`" in survivor for survivor in survivors), survivors
    else:
        assert survivors == []
    assert (tmp_path / sources[0]).read_text() == original
