"""
LC 424. Longest Repeating Character Replacement (Medium)

You are given a string s and an integer k. You can choose any character of the
string and change it to any other uppercase English character. You can perform
this operation at most k times.

Return the length of the longest substring containing the same letter you can
get after performing the above operations.

Example 1:
    Input: s = "ABAB", k = 2
    Output: 4
    Explanation: Replace the two 'A's with two 'B's or vice versa.

Example 2:
    Input: s = "AABABBA", k = 1
    Output: 4
    Explanation: Replace the one 'A' in the middle with 'B' and form "AABBBBA".
    The substring "BBBB" has the longest repeating letters, which is 4.
    There may exist other ways to achieve this answer too.

Constraints:
    1 <= s.length <= 10^5
    s consists of only uppercase English letters.
    0 <= k <= s.length
"""

from collections import defaultdict
def characterReplacement(s: str, k: int) -> int:
    c_f = defaultdict(int) #char freq
    l,r = 0, 0 #slide window
    max_freq = 0 #global max char freq

    while r<len(s):
        c_f[s[r]] += 1
        max_freq = max(max_freq, c_f[s[r]])

        if r-l+1 - max_freq > k: #no way to replace enough chars must advance l, 
            # note that I could use a while to advance l but then I'd need to keep and update 
            # max_len variable. by advancing both l and r I maintain monotonic non-decreasing 
            # invariant so max_len at end is r-l
            c_f[s[l]] -= 1
            l += 1

        r+=1 #advance right side

    return r-l
    


if __name__ == "__main__":
    tests = [
        (("ABAB", 2), 4),
        (("AABABBA", 1), 4),
        (("A", 0), 1),
        (("AAAA", 0), 4),
        (("ABCD", 0), 1),
        (("ABCD", 4), 4),
        (("ABBB", 2), 4),
        (("BAAAB", 2), 5),
        (("ABAA", 0), 2),
        (("AABBBCCDDDD", 2), 6),
    ]
    passed = 0
    for (s, k), expected in tests:
        got = characterReplacement(s, k)
        assert got == expected, f"characterReplacement({s!r}, {k}) = {got}, expected {expected}"
        passed += 1
    print(f"All {passed} tests passed")
