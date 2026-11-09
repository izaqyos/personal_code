"""
k-length string in an infinite stream (Amazon loop 09/11) + LC 28 Find the Index of the First Occurrence (Easy)

Part A (asked at Amazon): given get_next_char() over an infinite stream and a pattern of length k,
return True as soon as the pattern appears. Memory must not grow with the stream.
    stream ...abc..., pattern "bc" -> True ; pattern "ac" -> keeps running
Part B (LC 28): return the index of the first occurrence of needle in haystack, or -1.

Implement Part A twice:
  1. KMP: build the lps (failure) table, then one state j per char. O(1) amortised per char, O(k) memory.
  2. Rabin-Karp: rolling hash over the last k chars (deque), compare the window on a hash hit.
Test streams are finite: get_next_char() returns None at the end -> return False.
"""
from typing import Callable, List, Optional


def build_lps(p: str) -> List[int]:
    pass


def stream_contains_kmp(pattern: str, get_next_char: Callable[[], Optional[str]]) -> bool:
    pass


def stream_contains_rk(pattern: str, get_next_char: Callable[[], Optional[str]]) -> bool:
    pass


def str_str(haystack: str, needle: str) -> int:
    pass


def make_stream(s: str) -> Callable[[], Optional[str]]:
    it = iter(s)
    return lambda: next(it, None)


if __name__ == "__main__":
    assert build_lps("aabaaab") == [0, 1, 0, 1, 2, 2, 3]
    assert build_lps("abab") == [0, 0, 1, 2]
    for f in (stream_contains_kmp, stream_contains_rk):
        assert f("bc", make_stream("xxabcxx"))
        assert not f("ac", make_stream("xxabcxx"))
        assert f("aab", make_stream("aaab"))             # naive restart-at-0 misses this
        assert f("abab", make_stream("abaabab"))
        assert f("a", make_stream("a"))
        assert not f("abc", make_stream("ab"))
    assert str_str("sadbutsad", "sad") == 0
    assert str_str("leetcode", "leeto") == -1
    assert str_str("mississippi", "issip") == 4
    print("All tests passed.")
