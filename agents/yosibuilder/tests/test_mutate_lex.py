"""Lexical mutants: right operators flipped, right statements deleted, literals and generics left alone."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
import mutate_lex  # noqa: E402


def descriptions(source: str, rust: bool = False) -> list[str]:
    return [description.split(": ", 1)[1] for description, _ in mutate_lex.mutants(source, rust)]


def test_flips_comparisons_and_boolean_operators():
    source = "function f(a, b) {\n  return a === b && a < 3 || b >= 4;\n}\n"
    got = {description: mutant for description, mutant in mutate_lex.mutants(source)}
    assert sorted(d.split(": ", 1)[1].split(" in ")[0] for d in got) == sorted([
        "flip `===` to `!==`", "flip `&&` to `||`", "flip `<` to `<=`", "flip `||` to `&&`", "flip `>=` to `>`"])
    assert "return a === b && a <= 3 || b >= 4;" in got["2: flip `<` to `<=` in `return a === b && a < 3 || b >= 4;`"]


def test_leaves_strings_comments_templates_and_includes_alone():
    source = ('#include <stdio.h>\nint f(int a) {\n  // a < b\n  /* a == b */\n  const char *s = "a < b == c";\n'
              "  return a;\n}\nconst t = `${a < b}`; const c = 'x == y';\n")
    assert descriptions(source) == []


def test_generics_and_arrows_are_not_comparisons():
    source = "fn f(v: Vec<Vec<i32>>) -> Option<u8> { let m: HashMap<String, u8>; v.len() > 1 }"
    assert descriptions(source, rust=True) == ["flip `>` to `>=` in `" + source[:80] + "`"]


def test_rust_lifetimes_do_not_hide_code():
    source = "fn f<'a>(s: &'a str) -> bool {\n    s.len() >= 1\n}\n"
    assert descriptions(source, rust=True) == ["flip `>=` to `>` in `s.len() >= 1`"]


def test_rust_test_module_is_skipped():
    source = "pub fn f(a: u8) -> bool {\n    a == 1\n}\n#[cfg(test)]\nmod tests {\n    fn t() { assert!(1 == 1); }\n}\n"
    assert descriptions(source, rust=True) == ["flip `==` to `!=` in `a == 1`"]


def test_deletes_simple_statements_only_inside_bodies():
    source = """counter = 0;
class Counter {
  bump(n) {
    this.count += n;
    total++;
    log.push(n);
    await this.save();
    if (n > 9) {
      throw new Error("too big");
    }
    let x = 1;
    const y = f(x);
    int z = 2;
    std::string s = name;
    return x;
  }
}
"""
    deleted = [d for d in descriptions(source) if d.startswith("delete")]
    assert deleted == ["delete `this.count += n;`", "delete `total++;`", "delete `log.push(n);`",
                       "delete `await this.save();`", 'delete `throw new Error("too big");`']


def test_deletion_keeps_line_structure():
    source = "void f(int *n) {\n    *n += 1;\n}\n"
    [(description, mutant)] = list(mutate_lex.mutants(source))
    assert description == "2: delete `*n += 1;`"
    assert mutant == "void f(int *n) {\n    \n}\n"
