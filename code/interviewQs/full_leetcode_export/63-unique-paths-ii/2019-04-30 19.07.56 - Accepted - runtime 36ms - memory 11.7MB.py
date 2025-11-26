class Solution(object):
    def uniquePathsWithObstacles(self, obstacleGrid):
        """
        :type obstacleGrid: List[List[int]]
        :rtype: int
        DP solution

        0 - free, 1 - obstacle, < 0  - #paths (to normalize mult by -1)
        """

        n = len(obstacleGrid)
        m = len(obstacleGrid[0])
    
        if (n == 0) or (m == 0):
            return 0

    
        for j in reversed(range(m)):
            for i in reversed(range(n)):
    
                if (i == n - 1) and (j == m - 1):  # init
                    if obstacleGrid[i][j] == 1:  # obstacle on finish
                        return 0
                    obstacleGrid[i][j] = -1  
                if (obstacleGrid[i][j] !=1): #not an obstacle
                    if (j < m - 1):
                        if obstacleGrid[i][j + 1] != 1:  # can aggregate right going path
                            obstacleGrid[i][j] += obstacleGrid[i][j + 1]
                    if (i < n - 1):
                        if obstacleGrid[i + 1][j] != 1:  # can aggregate down going path
                            obstacleGrid[i][j] += obstacleGrid[i + 1][j]
    
        return max(obstacleGrid[0][0] *(-1), 0)
    