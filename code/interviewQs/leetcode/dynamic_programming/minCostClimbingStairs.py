"""
Min Cost Climbing Stairs
You are given an integer array cost where cost[i] is the cost of ith step on a staircase. Once you pay the cost, you can either climb one or two steps.

You can either start from the step with index 0, or the step with index 1.

Return the minimum cost to reach the top of the floor.

Example 1:

Input: cost = [10,15,20]
Output: 15
Explanation: You will start at index 1.
- Pay 15 and climb two steps to reach the top.
The total cost is 15.

Example 2:

Input: cost = [1,100,1,1,1,100,1,1,100,1]
Output: 6
Explanation: You will start at index 0.
- Pay 1 and climb two steps to reach index 2.
- Pay 1 and climb two steps to reach index 4.
- Pay 1 and climb two steps to reach index 6.
- Pay 1 and climb one step to reach index 7.
- Pay 1 and climb two steps to reach index 9.
- Pay 1 and climb one step to reach the top.
The total cost is 6.

Constraints:

2 <= cost.length <= 1000
0 <= cost[i] <= 999
"""
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int: 
        #cost length is at min 2 so I don't check len < 2
        dp = [0]  + [_ for _ in cost]
        cost.insert(0,0)
        for i in range(len(dp)-3,-1,-1):
            dp[i] = cost[i]+min(dp[i+1], dp[i+2])
        return dp[0]

            

        """
first build recursion algorithm.
define f(i) = cost from stair i to top
so min(f(0), f(1)) is the solution.
recursion equation is. f(i) = cost[i]+min(f(i+1),f(i+2))
stop cond. i==n(one step to top) or i==n-1 (two steps to top)
in code.
def helper(self, cost, index, total_cost, n):
    if index==n or index==(n-1):
        return total_cost
    total_cost = cost[index]+min(helper(cost, index+1, total_cost, n), helper(cost, index+2, total_cost, n))

call:
total_cost = 0
cost=[0]+cost
return helper(cost, 0, 0, n) 

convert to DP we need a 1d array. dp where dp[i] == f(i)
we will set dp to length n+1 where dp[0] is for convenience a 0 cost stair added to costs (cost.insert(0,0)) from which we can start at first or second stair
and we will fill the values in dp in reversed order of costs (so start from end, index n)
dp[n] == cost[n]
dp[n-1] == cost[n-1]
dp[n-2] == cost[n-2]+min(dp[n-1],dp[n])
...
dp[0] == cost[0] +min(dp[1],dp[2])
        """

