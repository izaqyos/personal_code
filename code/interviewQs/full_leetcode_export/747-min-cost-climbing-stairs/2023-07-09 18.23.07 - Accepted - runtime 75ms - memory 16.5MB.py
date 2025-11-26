class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int: 
        #cost length is at min 2 so I don't check len < 2
        dp = [0]  + [_ for _ in cost]
        cost.insert(0,0)
        for i in range(len(dp)-3,-1,-1):
            dp[i] = cost[i]+min(dp[i+1], dp[i+2])
        return dp[0]