"""
Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times in the segmentation.



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
"""

class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        """
        recursion would be run on all possible prefixes if valid word check recursion on reminder.
        do same just use dictionary for memorizing sub problem ansewrs
        """
        if not s or not wordDict:
            return False

        def wordBreakHelper(s: str, wordSet: set, memo: dict):
            if not s:
                return False
            if s in memo:
                return memo[s]
            for i in range(len(s)+1):
                if s[:i] in wordSet and (len(s[i:]) == 0 or wordBreakHelper(s[i:], wordSet, memo)):
                    memo[s]= True
                    break
            if not s in memo:
                memo[s] = False
            return memo[s]

        wordSet: set = set(wordDict)
        memo: dict = dict()
        return wordBreakHelper(s, wordSet, memo)


