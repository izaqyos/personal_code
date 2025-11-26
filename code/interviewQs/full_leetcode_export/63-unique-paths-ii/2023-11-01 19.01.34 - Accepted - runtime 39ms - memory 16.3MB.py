
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
