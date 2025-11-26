class Solution(object):
    def __init__(self):
        self.bDebug = False

    def printGrid(self, grid):
        print('[')
        for line in grid:
            print('[', end='')
            for elem in line:
                print('{}, '.format(elem), end='')
            print(']')
        print(']')


    def minPathSum(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int

        my idea for a DP solution. keep a matrix w/ same dimensions for tracking min path sum per cell.
        Start w. cell grid[n-1][m-1] where n,m = line len, column len 
        init pathSum[n-1][m-1] to  grid[n-1][m-1] 
        for m-1 column there's no choice so add weight. e.g pathSum[n-1][m-2] = grid[n-2][m-1] + pathSum[n-1][m-1]
         
        """
        if (self.bDebug):
            self.printGrid(grid)

        if len(grid) == 0:
            return 0
        
        if len(grid[0]) == 0: 
            return 0

        n = len(grid)
        m = len(grid[0])
        pathSums = [ [0 for x in range(m) ] for y in range(n) ]

        for j in reversed(range(m)):
            for i in reversed(range(n)):
                if self.bDebug:
                    print('at cell ({},{})'.format(i,j))
                if (i==n-1) and (j==m-1): #start condition
                    pathSums[i][j] = grid[i][j]
                    if self.bDebug:
                        print('at last cell ({},{})={}'.format(i,j,pathSums[i][j]))
                elif j==m-1: #for last column only way is down
                    pathSums[i][j] = pathSums[i+1][j] + grid[i][j]
                    if self.bDebug:
                        print('at last column ({},{})={}'.format(i,j,pathSums[i][j]))
                elif i==n-1:
                    pathSums[i][j] = pathSums[i][j+1] + grid[i][j]
                    if self.bDebug:
                        print('at last line ({},{})={}'.format(i,j,pathSums[i][j]))
                else: #can go either down or right so add min(down,right)
                    pathSums[i][j] = min(pathSums[i][j+1], pathSums[i+1][j]) + grid[i][j]
                    if self.bDebug:
                        print('at cell ({},{})={}'.format(i,j,pathSums[i][j]))

        return pathSums[0][0]