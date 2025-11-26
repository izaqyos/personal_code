
class Solution:
    def longestPalindrome(self, s: str) -> str:
        if len(s) <= 1:
            return s

        n = len(s)
        dp = [[False for _ in s] for _ in s]
        longest_i, longest_j = 0,0
        #for i in range(n):
        #    dp[i][j] = True

        for step in range(n):
            for i in range(0, n-step):
                j=i+step
                if i==j:
                    dp[i][j] = True
                #elif i>j: #loop revised so that i>=j invariant
                #    #dp[i][j] = False #no need, alread initialized to False
                #    continue
                else:
                    if j-i == 1:
                        if s[i] == s[j]:
                            dp[i][j] = True
                            if j-i > longest_j - longest_i: 
                                longest_i, longest_j = i,j
                    else:
                        if dp[i+1][j-1] and s[i] == s[j]:
                            dp[i][j] = True
                            if j-i > longest_j - longest_i: 
                                longest_i, longest_j = i,j
                #print(f"Filling DP[{i}][{j}] = {dp[i][j]}")
        return s[longest_i:longest_j+1]
