class Solution:
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

        