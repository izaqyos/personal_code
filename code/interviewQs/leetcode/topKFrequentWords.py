"""
LC 692 - Top K Frequent Words (Medium)

Given an array of strings words and an integer k, return the k most frequent strings.

Return the answer sorted by frequency from highest to lowest. Sort words with the same
frequency by their lexicographical order (alphabetical, ascending).

Example 1:
    Input: words = ["i","love","leetcode","i","love","coding"], k = 2
    Output: ["i","love"]
    Explanation: "i" and "love" are the two most frequent words.
    Note that "i" comes before "love" due to a lower alphabetical order.

Example 2:
    Input: words = ["the","day","is","sunny","the","the","the","sunny","is","is"], k = 4
    Output: ["the","is","sunny","day"]
    Explanation: "the", "is", "sunny" and "day" are the four most frequent words,
    with frequencies 4, 3, 2 and 1 respectively.

Constraints:
    1 <= words.length <= 500
    1 <= words[i].length <= 10
    words[i] consists of lowercase English letters.
    k is in the range [1, number of unique words]

Follow-up: Could you solve it in O(n log k) time and O(n) extra space?
"""
from typing import List
from collections import Counter
import heapq

class Solution:

    ## Counter + Sort, U- unique words. Space: O(U), Time: O(n) Counter dict ctor, O(Ulog(U)) sort dict
    ## so worst case U=n O(nlogn)
    #def topKFrequent(self, words: List[str], k: int) -> List[str]:
    #    cnt = Counter(words)
    #    sorted_cnt = sorted(cnt, key=lambda x: (-cnt[x], x) )
    #    return sorted_cnt[:k]

    #w/ heap 
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        cnt = Counter(words)
        return heapq.nsmallest(k, cnt, key=lambda elem: (-cnt[elem], elem))

if __name__ == "__main__":
    s = Solution()
    cases = [
        # (words, k, expected, label)
        (["i", "love", "leetcode", "i", "love", "coding"], 2, ["i", "love"], "example 1: tie broken alphabetically"),
        (["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4,
         ["the", "is", "sunny", "day"], "example 2"),
        (["a"], 1, ["a"], "single word"),
        (["b", "a", "c"], 3, ["a", "b", "c"], "all tied: pure alphabetical"),
        (["b", "a", "c"], 2, ["a", "b"], "all tied, k < unique: smallest words win"),
        (["aaa", "aa", "a"], 1, ["a"], "prefix ordering: 'a' < 'aa' < 'aaa'"),
        (["x", "y", "y", "z", "z", "z"], 3, ["z", "y", "x"], "distinct counts"),
        (["dog", "cat", "dog", "cat", "bird"], 2, ["cat", "dog"], "tie at the top"),
        (["dog", "cat", "dog", "cat", "bird", "ant"], 3, ["cat", "dog", "ant"], "tie at the cut-off"),
    ]
    passed = 0
    for words, k, exp, label in cases:
        got = s.topKFrequent(words[:], k)
        assert got == exp, f"FAIL [{label}]: expected {exp}, got {got}"
        passed += 1
    print(f"All {passed}/{len(cases)} tests passed")
