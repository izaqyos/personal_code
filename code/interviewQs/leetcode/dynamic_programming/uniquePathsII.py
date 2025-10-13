"""
You are given an m x n integer array grid. There is a robot initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

An obstacle and space are marked as 1 or 0 respectively in grid. A path that the robot takes cannot include any square that is an obstacle.

Return the number of possible unique paths that the robot can take to reach the bottom-right corner.

The testcases are generated so that the answer will be less than or equal to 2 * 109.



Example 1:


Input: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
Output: 2
Explanation: There is one obstacle in the middle of the 3x3 grid above.
There are two ways to reach the bottom-right corner:
1. Right -> Right -> Down -> Down
2. Down -> Down -> Right -> Right
Example 2:


Input: obstacleGrid = [[0,1],[0,0]]
Output: 1


Constraints:

m == obstacleGrid.length
n == obstacleGrid[i].length
1 <= m, n <= 100
obstacleGrid[i][j] is 0 or 1.
"""

"""
since at any given cell we can move either right or down recursion equations is:
    R(grid[i][j]) = R(grid[i+1][j])+R(grid[i][j+1])
    This translate to DP if we start from DP[m-1][n-1] as 1 (in this cell there's only one path)
    we can mark last line and column as 1 (because in last line you can only move right, last column only move down)
    then double loop to fill inner DP matrix m-2,n-2 to 0,0 
    where DP[i][j] = DP[i+1][j] + DP[i][j+1] if both are clear, 0 if both are obstacles and just the clear one if only one is clear
    then return DP[0][0]
"""

class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int :
        if not obstacleGrid or not obstacleGrid[0]:
            return -1
        m,n = len(obstacleGrid), len(obstacleGrid[0])
        if obstacleGrid[m-1][n-1] == 1 or obstacleGrid[0][0] == 1:
            return 0

        dp = [   [0 for i in range(n)] for _ in range(m)]

        foundObstacle = False
        for i in range(m-1,-1,-1):
            #print(f"foundObstacle={foundObstacle}, obstacleGrid[{i}][{n-1}]=obstacleGrid[i][n-1]") 
            if obstacleGrid[i][n-1] == 1 or foundObstacle:
                if not foundObstacle:
                    foundObstacle = True
                dp[i][n-1] = 0
            else:
                dp[i][n-1] = 1

        foundObstacle = False
        for j in range(n-1,-1,-1):
            if obstacleGrid[m-1][j] == 1 or foundObstacle:
                if not foundObstacle:
                    foundObstacle = True
                dp[m-1][j] = 0
            else:
                dp[m-1][j] = 1

        #print(f"dp after setting last row and column: {dp}") 
        for i in range(m-2, -1, -1):
            for j in range(n-2, -1, -1):
                if obstacleGrid[i][j] == 1:
                    dp[i][j] = 0
                    #print(f"Detected obstacle at {i},{j}, setting dp[{i}][{j}] to 0")
                else:
                    if obstacleGrid[i+1][j] == 0 and obstacleGrid[i][j+1] == 0:
                        dp[i][j] = dp[i+1][j] + dp[i][j+1]
                        #print(f"Detected clear path down and right from {i},{j}, setting dp[{i}][{j}] to {dp[i][j]}")
                    elif obstacleGrid[i+1][j] == 0: 
                        dp[i][j] = dp[i+1][j] 
                        #print(f"Detected clear path down from {i},{j}, setting dp[{i}][{j}] to {dp[i][j]}")
                    elif obstacleGrid[i][j+1] == 0: 
                        dp[i][j] = dp[i][j+1]
                        #print(f"Detected clear path right from {i},{j}, setting dp[{i}][{j}] to {dp[i][j]}")
                    else:
                        #print(f"Detected no clear path from {i},{j}, setting dp[{i}][{j}] to {dp[i][j]}")
                        dp[i][j] = 0

        return dp[0][0]
        
"""
Todo, fix wrong TC:
    nput
obstacleGrid =
[[0,0],[1,1],[0,0]]
Output
1
Expected
0
"""
