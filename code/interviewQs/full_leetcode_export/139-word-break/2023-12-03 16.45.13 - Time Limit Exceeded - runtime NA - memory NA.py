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
