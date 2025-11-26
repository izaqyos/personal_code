class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        dp = [1 for _ in range(n+1)]
        dp[2] = 2
        for i in range(3,n+1):
            dp[i]+=dp[i-2]+dp[i-1]-1 
        return dp[n]
    
"""
My idea. recursion with dp.
dp[1] - 1 dp[2] - 2 made of 2 and 1,1
dp[3] - 3 made of 1,2 (dp[0]+2) 2,1 (dp[1]+1) and 1,1,1 (can be seen as dp[0]+1+1 or dp[1]+1)
dp[4] - 1,1,1,1 (can be seen as dp[2]+1+1 or dp[3]+1), 2,2 (dp[2]+2), 1,2,1 (dp[3]+1), 2,1,1 etc
u get the pattern. dp[i] is dp[i-2]+dp[i-1] -1 . The -1 is for the all climb options 1 which both have 
"""
            
            