"""
LC 763 — Partition Labels  (Medium)

You are given a string `s`. Partition the string into as many parts as possible
so that each letter appears in at most one part.

Return a list of integers representing the size of each part, in order. The
parts, concatenated in order, must equal the original string.

Examples:
    Input:  s = "ababcbacadefegdehijhklij"
    Output: [9, 7, 8]
    ("ababcbaca" | "defegde" | "hijhklij" -- no letter spans two parts)

    Input:  s = "eccbbbbdec"
    Output: [10]
    (every split would put 'e' or 'c' in two parts)

Constraints:
    1 <= len(s) <= 500
    s consists of lowercase English letters only
"""

from typing import List


def partition_labels(s: str) -> List[int]:
    ret: List[int] = []
    last_indices = {c:i for i,c in enumerate(s)}
    #last_indices = dict()
    #for i, c in enumerate(s):
    #    last_indices[c] = i

    start, end = 0, 0
    for i, c in enumerate(s):
        end = max(end, last_indices[c])
        if i == end:
            ret.append(end -start + 1)
            start=end + 1
    #print(f" got str {s}, returning {ret}")
    return ret


if __name__ == "__main__":
    assert partition_labels("ababcbacadefegdehijhklij") == [9, 7, 8]
    assert partition_labels("eccbbbbdec") == [10]

    # single character
    assert partition_labels("a") == [1]

    # all distinct -> every char its own part
    assert partition_labels("abc") == [1, 1, 1]

    # all identical -> one part
    assert partition_labels("aaaa") == [4]

    # interleaved, cannot split
    assert partition_labels("abab") == [4]
    assert partition_labels("abcabc") == [6]

    # nested (first char closes last)
    assert partition_labels("abba") == [4]

    # two clean groups
    assert partition_labels("abaccbdeffed") == [6, 6]

    # part boundary at the very last index
    assert partition_labels("abcdd") == [1, 1, 1, 2]

    print("all tests pass")
