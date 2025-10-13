"""
Given a m x n grid filled with non-negative numbers, find a path from top left to bottom right, which minimizes the sum of all numbers along its path.

Note: You can only move either down or right at any point in time.

Example 1:
Input: grid = [[1,3,1],[1,5,1],[4,2,1]]
Output: 7
Explanation: Because the path 1 → 3 → 1 → 1 → 1 minimizes the sum.
Example 2:

Input: grid = [[1,2,3],[4,5,6]]
Output: 12
Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 200
0 <= grid[i][j] <= 200
"""

"""
Solution, similar to uniquePaths, instead of calculating unique paths, calculate the sum
since at any given cell we can move either right or down recursion equations is:
    R(grid[i][j]) = min( R(grid[i+1][j]),R(grid[i][j+1])) + grid[i][j]
    This translate to DP if we start from DP[m-1][n-1] as 1 (in this cell there's only one path)
    DP[i][j] starts same as grid[i][j]
    we can easily calculate sum in last line and column just add the value to the right for last line, value below to last column
    then double loop to fill inner DP matrix m-2,n-2 to 0,0 
    where DP[i][j] = min(DP[i+1][j] , DP[i][j+1]) + DP[i][j]
    last, return DP[0][0]
"""

class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        dp = [ r[:] for r in grid] #shallow copy grid to dp
        for i in range(m-2, -1, -1):
            dp[i][n-1] += dp[i+1][n-1]
        for j in range(n-2, -1, -1):
            dp[m-1][j] += dp[m-1][j+1]
        for i in range(m-2, -1, -1):
            for j in range(n-2, -1, -1):
                dp[i][j] = min(dp[i+1][j] , dp[i][j+1]) + dp[i][j]

        return dp[0][0]


