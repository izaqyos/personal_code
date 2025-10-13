#!/opt/homebrew/bin/python3

from typing import List
"""
Word Break
Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times in the segmentation.
inp
Example 1:

Input: s = "leetcode", wordDict = ["leet","code"]
Output: true
Explanation: Return true because "leetcode" can be segmented as "leet code".
Example 2:

Input: s = "applepenapple", wordDict = ["apple","pen"]
Output: true
Explanation: Return true because "applepenapple" can be segmented as "apple pen apple".
Note that you are allowed to reuse a dictionary word.
Example 3:

Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
Output: false
Constraints:

1 <= s.length <= 300
1 <= wordDict.length <= 1000
1 <= wordDict[i].length <= 20
s and wordDict[i] consist of only lowercase English letters.
All the strings of wordDict are unique.

"""

"""
Recursion. R(s) = True iff 
for in i in range(len(s)):
    s[0:i] in dict and R(s[i:])
To avoid recalculating recursion on the suffixes use memorization
memo[s] is T/F iff s is word breakable, can use a set, if it's in set then its breakable
"""

#Not my solution
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        dp = [True] + [False] * (l:=len(s))
        s = ' '+ s 
        wordDict = set(wordDict)
        max_word_len = len(max(wordDict, key=len))
        for i in range(1,l+1):
            for j in range(i-1,max(i-max_word_len-1,-1),-1):
                #print(f"i={i}, j={j}, dp[{j}]={dp[j]}, check word {s[j+1:i+1]} in dictionary")  
                if dp[j] and s[j+1:i+1] in wordDict:
                    dp[i] = True
                    break
        return dp[-1]

"""
Also TLE:
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        memo = set() 
        wdict = set(wordDict)
        return self.helper(s, wdict, memo)

    def helper(self, s: str, wordDict: Set[str], memo) -> bool:
        if not s:
            return False
        if s in memo:
            return True
        for i in range(1, len(s)+1):
            if s[:i] in wordDict:
                if not s[i:] or self.helper(s[i:], wordDict, memo):
                    memo.add(s)
                    return True
        return False
"""

"""
This version. TLE 
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        memo = set() 
        return self.helper(s, wordDict, memo)

    def helper(self, s: str, wordDict: List[str], memo) -> bool:
        for i in range(1, len(s)+1):
            if s[0:i] in wordDict:
                if not s[i:]:
                    return True
                if s[i:] in memo:
                    return True
                if self.helper(s[i:], wordDict, memo):
                    memo.add(s[i:])
                    return True
        return False

s =
"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab"
wordDict =
["a","aa","aaa","aaaa","aaaaa","aaaaaa","aaaaaaa","aaaaaaaa","aaaaaaaaa","aaaaaaaaaa"]
"""

def test():
    inputs=(
            ("leetcode", ["leet","code"]),
            ("applepenapple", ["apple","pen"]),
            ( "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab", ["a","aa","aaa","aaaa","aaaaa","aaaaaa","aaaaaaa","aaaaaaaa","aaaaaaaaa","aaaaaaaaaa"]),
            )
    sol = Solution()
    for inp in inputs:
        print('-'*100)
        print(f"Solving word break for string {inp[0]}, words dictionary {inp[1]}")
        res = sol.wordBreak(inp[0], inp[1])
        print('-'*100)

def main():
    test()
if __name__ == "__main__":
    main()
