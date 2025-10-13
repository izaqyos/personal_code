"""
Mini Challenge: Top-K Words

Task:
Implement top_k_words(text: str, k: int = 3) -> list[tuple[str, int]] that returns the k most frequent words (case-insensitive) as (word, count) pairs.

Rules (kept minimal):

Words are sequences of letters and apostrophes (so "it's" counts as a single word).

Case-insensitive (normalize to lower).

Tie-break by word ascending (alphabetical).

If there are fewer than k unique words, return them all.
"""

import re
from collections import Counter

# WORD_RE = re.compile(r"[A-Za-z']+") # will allow '' "" 'this etc. so we use a more strict regex
WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)*")


def top_k_words(text: str, k: int = 3) -> list[tuple[str, int]]:
    """
    Return the k most frequent words as (word, count) pairs.
    - Case-insensitive
    - Words: sequences of letters and apostrophes
    - Tie-break by word ascending
    """
    if not text and k <= 0:
        return []

    words = WORD_RE.findall(text.lower())
    words_count = Counter(words)
    return sorted(words_count.items(), key = lambda x : (-x[1], x[0]))[:k]

# --- Tests ---
if __name__ == "__main__":
    print("Running tests...")

    s = "It's time, time to test—test the TEST! It's fine."
    # tokens (lower): it's x2, time x2, to x2, test x3, the x1, fine x1
    got = top_k_words(s, 3)
    expected = [("test", 3), ("it's", 2), ("time", 2)]
    print(f"Test Case1: input: {s}, got: {got}, expected: {expected}")
    assert got == expected, f"Got {got}, expected {expected}"

    # Case-insensitivity + apostrophes
    s2 = "Don't stop believing. don't, DON'T."
    got = top_k_words(s2, 2)
    expected = [("don't", 3), ("believing", 1)]
    print(f"Test Case1: input: {s2}, got: {got}, expected: {expected}")
    assert got == expected

    # Fewer unique words than k
    s3 = "alpha alpha beta"
    got = top_k_words(s3, 5)
    expected = [("alpha", 2), ("beta", 1)]
    print(f"Test Case1: input: {s3}, got: {got}, expected: {expected}")
    assert got == expected

    # Ties resolved by word asc
    s4 = "b a a b c"
    got = top_k_words(s4, 3)
    expected = [("a", 2), ("b", 2), ("c", 1)]
    print(f"Test Case1: input: {s4}, got: {got}, expected: {expected}")
    assert got == expected

    print("All tests passed.")
