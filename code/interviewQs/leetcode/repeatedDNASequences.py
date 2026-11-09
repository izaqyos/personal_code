"""
LC 187 Repeated DNA Sequences (Medium): Rabin-Karp / rolling-hash practice.

Return all 10-letter substrings that occur more than once in a DNA string (A, C, G, T).
    s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT" -> ["AAAAACCCCC", "CCCCCAAAAA"]
    s = "AAAAAAAAAAAAA"                     -> ["AAAAAAAAAA"]
Do it with a rolling hash: 2 bits per letter, a 20-bit window, O(n) time, no substring slicing per step.
"""
from typing import List


def find_repeated_dna(s: str) -> List[str]:
    pass


if __name__ == "__main__":
    assert sorted(find_repeated_dna("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT")) == ["AAAAACCCCC", "CCCCCAAAAA"]
    assert find_repeated_dna("AAAAAAAAAAAAA") == ["AAAAAAAAAA"]
    assert find_repeated_dna("ACGT") == []
    print("All tests passed.")
