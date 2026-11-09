"""
Polish notation evaluator (Amazon loop 09/11) + LC 150 Evaluate Reverse Polish Notation (Medium)

Part A (asked at Amazon): evaluate an expression in Polish (prefix) notation.
    tokens = ["+", "3", "*", "4", "5"]      -> 23        (3 + 4*5)
    tokens = ["-", "/", "10", "3", "2"]     -> 1         (10/3 = 3, 3 - 2)
Part B (LC 150): the same in Reverse Polish (postfix) notation.
    tokens = ["2", "1", "+", "3", "*"]      -> 9
    tokens = ["4", "13", "5", "/", "+"]     -> 6
Part C (follow-up): prefix with parentheses, e.g. "(+ 1 (* 2 3) 4)" where an operator may take
    more than two operands -> 11. Evaluate the inner list and push its result back.

Rules: + - * /, integer division truncates toward zero, numbers may be negative ("-3").
Raise ValueError on malformed input.
Do Part A twice: a stack scanning right to left, and recursive descent left to right.
"""
from typing import List


def eval_prefix(tokens: List[str]) -> int:
    pass


def eval_prefix_recursive(tokens: List[str]) -> int:
    pass


def eval_rpn(tokens: List[str]) -> int:
    pass


def eval_sexpr(s: str) -> int:
    pass


if __name__ == "__main__":
    for f in (eval_prefix, eval_prefix_recursive):
        assert f("+ 3 * 4 5".split()) == 23
        assert f("- / 10 3 2".split()) == 1
        assert f("* + 1 2 - 7 3".split()) == 12
        assert f("/ -7 2".split()) == -3                 # truncate, not floor
        assert f(["42"]) == 42
        for bad in (["+", "1"], ["1", "2"]):
            try:
                f(bad)
                raise AssertionError(f"{f.__name__} accepted {bad}")
            except (ValueError, StopIteration, IndexError):
                pass
    assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
    assert eval_rpn(["4", "13", "5", "/", "+"]) == 6
    assert eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
    assert eval_sexpr("(+ 1 (* 2 3) 4)") == 11
    assert eval_sexpr("(- 10 (/ 9 2))") == 6
    print("All tests passed.")
