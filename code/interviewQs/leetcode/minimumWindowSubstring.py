"""
LC 76 — Minimum Window Substring (Hard)

Given strings `s` and `t`, return the minimum-length substring of `s` such that
every character of `t` (including duplicates) is contained in the window.
If no such substring exists, return "".

If multiple windows of the same minimum length exist, return any one of them
(the LeetCode harness accepts the first match).

Aim for O(|s| + |t|) time. O(|s| + |t|) space (frequency maps).

Constraints:
    1 <= len(s), len(t) <= 10^5
    s and t consist of uppercase and lowercase English letters

Examples:
    s = "ADOBECODEBANC", t = "ABC"  -> "BANC"
    s = "a",            t = "a"     -> "a"
    s = "a",            t = "aa"    -> ""        (need two 'a's, only one)
    s = "ab",           t = "b"     -> "b"
    s = "aa",           t = "aa"    -> "aa"
    s = "abc",          t = "ac"    -> "abc"
    s = "ADOBECODEBANC", t = "AABC" -> ""        (only one 'A' in s before BANC; needs two)

Edge cases to think about:
    - len(t) > len(s)               -> ""
    - char in t that never appears in s
    - duplicates in t (count, not just presence)
    - whole s is the answer
    - multiple equal-length minima (any one is fine)
    - t and s share no characters
"""
from typing import Tuple
from collections import Counter
from collections import defaultdict
import sys


def min_window(s: str, t: str) -> str:
    """
    strategy:
    1. pass over t create t_char_freq dict (can use Counter)
    2. set num_satisfy to 0 (incr by 1 for each c in s that has freq match exactly t_char_freq[c])
    3. sliding window over s, l,r start at 0, r expands to right 
        3.1 if c at s[r] in t_char_freq,
            have_char_freq[c] += 1
             if have_char_freq[c] == t_char_freq[c], num_satisfy += 1 
             if num_satisfy == len(t_char_freq) # compact win from left
              if r-l+1 < best_len (init as len(s)) we have new best lets mark
              best_len = r-l+1, best_l = l
              now move l by 1 to right so take care of seen (seen[s[l]] -= 1) and if it was in t_char_freq, num_satify -= 1
              l += 1
    """
    t_char_freq: dict[str, int] = Counter(t) 
    s_have_char_freq: defaultdict[str, int] = defaultdict(int)
    num_satisfy: int = 0
    left: int = 0
    best_l: int = 0
    best_len: int = sys.maxsize
    for r in range(len(s)):
        c = s[r]
        s_have_char_freq[c] += 1
        if c in t_char_freq and s_have_char_freq[c] == t_char_freq[c]: # boom, we have a match, lets num_satisfy +=1
            num_satisfy +=1
        while num_satisfy == len(t_char_freq): #we found a window, lets minimize it if possible
            if r - left +1  < best_len:
                best_len = r - left +1
                best_l= left
            # now move l one 2 right, we need to remove d from have, and if needed updated num_satisfy
            # basically we shrink winow from left side until we have no more matches
            d = s[left]
            s_have_char_freq[d] -= 1 
            if d in t_char_freq and  s_have_char_freq[d] < t_char_freq[d] :
                num_satisfy -= 1
            left += 1

    print(f"best_len = {best_len}, found match starting at {best_l} = {s[best_l: best_l + best_len]}")
    return "" if best_len == sys.maxsize else s[best_l: best_l + best_len]


if __name__ == "__main__":
    cases: list[Tuple[str, str, str]] = [
        ("ADOBECODEBANC", "ABC",  "BANC"),
        ("a",            "a",    "a"),
        ("a",            "aa",   ""),
        ("ab",           "b",    "b"),
        ("aa",           "aa",   "aa"),
        ("abc",          "ac",   "abc"),
        ("ADOBECODEBANC", "AABC", "ADOBECODEBA"),  # 2 A's at idx 0 & 10 force the window to span them
        ("ab",           "a",    "a"),
        ("ab",           "A",    ""),                 # case-sensitive
        ("cabwefgewcwaefgcf", "cae", "cwae"),
        ("xyz",          "abc",  ""),
        ("aaflslflsldkalskaaa", "aaa", "aaa"),
    ]

    passed = 0
    for s, t, expected in cases:
        got = min_window(s, t)
        # any minimum-length window is acceptable as long as it contains all of t
        ok = got == expected
        passed += ok
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] min_window({s!r}, {t!r}) = {got!r}  (expected {expected!r})")

    print(f"\n{passed}/{len(cases)} passed")
    assert passed == len(cases), "some cases failed"
