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
