"""
49. Group Anagrams
https://leetcode.com/problems/group-anagrams/

Given an array of strings strs, group the anagrams together.
You can return the answer in any order.

An anagram is a word or phrase formed by rearranging the letters of a
different word or phrase, using all the original letters exactly once.

Constraints:
- 1 <= strs.length <= 10^4
- 0 <= strs[i].length <= 100
- strs[i] consists of lowercase English letters

Example 1: ["eat","tea","tan","ate","nat","bat"] -> [["bat"],["nat","tan"],["ate","eat","tea"]]
Example 2: [""] -> [[""]]
Example 3: ["a"] -> [["a"]]
"""

# Three approaches:
# 1. Prime product   — map each letter to a prime, multiply => unique signature per anagram group
#                      O(n*k) time, O(n*k) space. Risk: huge ints for long strings (Python handles it, but slow hashing)
# 2. Sorted key      — sort each word, use as dict key
#                      O(n * k log k) time, O(n*k) space. Simplest to write.
# 3. Char-count tuple — count letter frequencies, use tuple(counts) as key
#                      O(n*k) time, O(n*k) space. Optimal — no sorting, no overflow.
from collections import defaultdict
from typing import Generator


def eratosthenes_sieve() -> list[int]:
    #nums = [_ + 1 for _ in range(1, 100)]
    nums = list(range(2, 101))
    #print(f"nums={nums}")
    ind = 0
    p = nums[ind]  # first prime, 2
    while p * p < 100:
        c_ind = ind + p
        #print(f"c_ind={c_ind}, p={p}, ind={ind}")
        while c_ind < len(nums):
            nums[c_ind] = 0
            #print(f"nums[c_ind]={nums[c_ind]}, c_ind={c_ind}")
            c_ind += p
        ind+=1
        while nums[ind] == 0:
            ind += 1
        p = nums[ind]

    #print("[", end="")
    #for n in nums:
    #    if n > 0:
    #        print(n, end=", ")
    #print("]")

    return nums

def primes_generator() -> Generator[int, None, None]:
    nums = eratosthenes_sieve()
    for n in nums:
        if n > 0:
            yield n

CHAR_PRIMES = [i for _, i in zip(range(26), primes_generator())]
def unique_signature(s: str) -> int :
    #index by ord(c) - ord('a')
    #print(f"char_primes={char_primes}")
    signature = 1
    for c in s.lower():
        signature *= CHAR_PRIMES[ord(c) - ord('a')]
    #print(f" {s} -> signature={signature}")
    return signature

def group_anagrams(strs: list[str]) -> list[list[str]]:
    anagrams = defaultdict(list)
    for s in strs:
        anagrams[unique_signature( s)].append(s)
    #print(f"anagrams={anagrams}")
    #ret = list() 
    #for group in anagrams.values():
    #    ret.append(group)
    #return ret
    return list(anagrams.values())


# Approach 2: Sorted key — O(n * k log k)
# Sort each string to get a canonical form; anagrams sort to the same key.
def group_anagrams_sortedkey(strs: list[str]) -> list[list[str]]:
    anagrams = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))  # "eat" -> ('a','e','t'), "tea" -> ('a','e','t')
        anagrams[key].append(s)
    return list(anagrams.values())


# Approach 3: Char-count tuple — O(n * k), optimal
# Count frequency of each letter; the 26-element tuple is the key.
# No sorting, no overflow — best of both worlds.
def group_anagrams_charcount(strs: list[str]) -> list[list[str]]:
    anagrams = defaultdict(list)
    for s in strs:
        counts = [0] * 26
        for c in s:
            counts[ord(c) - ord('a')] += 1
        anagrams[tuple(counts)].append(s)  # e.g. "eat" -> (1,0,0,0,1,...,1,...0)
    return list(anagrams.values())


if __name__ == "__main__":
    def sorted_result(result: list[list[str]]) -> list[list[str]]:
        return sorted([sorted(group) for group in result])

    tests = [
        (
            ["eat", "tea", "tan", "ate", "nat", "bat"],
            [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]],
        ),
        ([""], [[""]]),
        (["a"], [["a"]]),
        (
            ["", ""],
            [["", ""]],
        ),
        (
            ["abc", "cba", "bac", "foo", "ofo"],
            [["abc", "bac", "cba"], ["foo", "ofo"]],
        ),
    ]
    approaches = [
        ("prime product", group_anagrams),
        ("sorted key",    group_anagrams_sortedkey),
        ("char count",    group_anagrams_charcount),
    ]
    for name, fn in approaches:
        print(f"\n--- {name} ---")
        for i, (strs, expected) in enumerate(tests):
            result = fn(strs)
            status = "PASS" if sorted_result(result) == sorted_result(expected) else "FAIL"
            print(f"Test {i+1}: {status} | input={strs}")
