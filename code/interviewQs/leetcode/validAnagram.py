"""
242. Valid Anagram
https://leetcode.com/problems/valid-anagram/

Given two strings s and t, return true if t is an anagram of s, and false otherwise.

An anagram is a word or phrase formed by rearranging the letters of a different word
or phrase, using all the original letters exactly once.

Constraints:
- 1 <= s.length, t.length <= 5 * 10^4
- s and t consist of lowercase English letters

Follow up: What if the inputs contain Unicode characters?

Example 1: s = "anagram", t = "nagaram" -> true
Example 2: s = "rat", t = "car" -> false
"""


def is_anagram_not_optimized(s: str, t: str) -> bool:
    char_count_s, char_count_t = [0]*26 , [0]*26

    # I know its guaranteed. still..
    s = s.lower()
    t = t.lower()

    for c in s:
        char_count_s[(ord(c)-ord('a'))] += 1

    for c in t:
        char_count_t[(ord(c)-ord('a'))]+=1

    #print(f"s={s}, t={t}, char_count_s={char_count_s} , char_count_t={char_count_t} ")
    for i in range(26):
        if char_count_s[i] != char_count_t[i]:
            return False
    return True

def is_anagram(s: str, t: str) -> bool:
    char_count_s= [0]*26
    s = s.lower()
    t = t.lower()

    if len(s) != len(t):
        return False

    for c in s:
        char_count_s[(ord(c)-ord('a'))] += 1

    for c in t:
        char_count_s[(ord(c)-ord('a'))]-=1

    return all(c == 0 for c in char_count_s)


if __name__ == "__main__":
    tests = [
        ("anagram", "nagaram", True),
        ("rat", "car", False),
        ("", "", True),
        ("a", "a", True),
        ("a", "b", False),
        ("a", "ab", False),        # different lengths
        ("ab", "a", False),         # different lengths (reversed)
        ("aabbcc", "abcabc", True), # repeated chars, same counts
        ("aabbcc", "aabbc", False), # subset but shorter
        ("aacc", "ccac", False),    # same length, different counts
    ]
    for i, (s, t, expected) in enumerate(tests):
        result = is_anagram(s, t)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i+1}: {status} | s={s!r}, t={t!r}, expected={expected}, got={result}")
