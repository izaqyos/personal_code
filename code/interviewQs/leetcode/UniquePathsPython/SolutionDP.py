class Solution(object):

    def __init__(self):
        self.board = [[]]
        self.bDebug = True
        #self.bDebug = False

    def init(self, m, n):
        if self.bDebug:
            print('init({0},{1})'.format(n, n))
        self.m = m  # columns
        self.n = n  # rows
        self.board = [[0 for x in range(m)] for y in range(n)]
        self.paths = 0

    def printBoard(self):
        print('\n'.join(
            ['\t'.join([str(self.board[i][j]) for j in range(len(self.board[i]))]) for i in range(len(self.board))]))

    def uniquePaths(self, m, n):
        """
        DP solution
        :type m: int
        :type n: int
        :rtype: int
        """
        self.init(m, n)
        if self.bDebug:
            self.printBoard()
        for j in reversed(range(m)):
            for i in reversed(range(n)):
                if (i == n - 1) and (j == m - 1):  # init
                    self.board[i][j] = 1
                if (j < m - 1):  # can aggregate right going path
                    self.board[i][j] += self.board[i][j + 1]
                if (i < n - 1):  # can aggregate down going path
                    self.board[i][j] += self.board[i + 1][j]
                if self.bDebug:
                    print("set [{0},{1}]={2}".format(i, j, self.board[i][j]))

        if self.bDebug:
            self.printBoard()

        return self.board[0][0]

    def uniquePathsWithObstacles(self, obstacleGrid):
        """
        :type obstacleGrid: List[List[int]]
        :rtype: int
        DP solution

        0 - free, 1 - obstacle, < 0  - #paths (to normalize mult by -1)
        """

        n = len(obstacleGrid)
        m = len(obstacleGrid[0])
        if self.bDebug:
            print("got grid of ({},{})".format(n,m))
        if (n == 0) or (m == 0):
            return 0

        if self.bDebug:
            self.printBoard()
        for j in reversed(range(m)):
            for i in reversed(range(n)):
                if self.bDebug:
                    print('at cell ({},{})'.format(i,j))
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
                if self.bDebug:
                    print("set [{0},{1}]={2}".format(i, j, obstacleGrid[i][j]))

        if self.bDebug:
            self.printBoard()

        return max(obstacleGrid[0][0] *(-1), 0)

    #garbage. doesn't work.
    def uniquePathsWithObstaclesSimple(self, a):
        m, n = len(a), len(a[0])
        dp = [0] * n        
        dp[0] = 1
        for i in range(m):            
            for j in range(n):
                if not a[i][j]:                                        
                    if j >= 1 and not a[i][j-1]: dp[j] += dp[j-1] 
                else: dp[j] = 0                    
        return dp[-1]


def testUniquePaths():
    sol = Solution()
    print('unique paths of 2x3: ', sol.uniquePaths(3, 2))
    print('unique paths of 4x4: ', sol.uniquePaths(4, 4))
    print('unique paths of 6x9: ', sol.uniquePaths(3, 9))


def testUniquePathsObstacle():
    listofObstacleLists = [
        [
            [0,1],
            [1,0], 
        ],
        [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
        ],
        [
        [0, 0, 0],
        [0, 1, 0],
        [0, 1, 0]
        ],
        [
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        ],
        [
            [0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0],[1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,1],[0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0],[0,0,0,1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0],[1,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0],[0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0],[0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0],[0,1,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0],[0,1,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,1],[1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1],[0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,1,0,1],[1,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1],[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0]
        ]
    ]
    sol = Solution()
    for lst in listofObstacleLists:
        #print('unique paths with obstacles of {}: {} '.format(lst, sol.uniquePathsWithObstaclesSimple(lst)))
        print('unique paths with obstacles of {}: {} '.format(lst, sol.uniquePathsWithObstacles(lst)))


if __name__ == "__main__":
    #testUniquePaths()
    testUniquePathsObstacle()
