#!/opt/homebrew/bin/python3

from typing import List 

class Solution:
    def printGrid(self, grid):
        print('[')
        for line in grid:
            print('[', end='')
            for elem in line:
                print('{}, '.format(elem), end='')
            print(']')
        print(']')

    def minPathSum(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return -1
        m,n = len(grid), len(grid[0])
        dfs = [  [float('inf') for _ in grid[0]] for _ in grid ]
        #self.printGrid(grid)
        #self.printGrid(dfs)
        dfs[m-1][n-1] = grid[m-1][n-1]

        #fill last column
        for i in range(m-2,-1,-1):
            dfs[i][n-1] = dfs[i+1][n-1] + grid[i][n-1]

        #fill last row
        for j in range(n-2, -1, -1):
            dfs[m-1][j] = dfs[m-1][j+1] + grid[m-1][j]

        
        for i in range(m-2,-1,-1):
            for j in range(n-2, -1, -1):
                dfs[i][j] = grid[i][j] + min(dfs[i][j+1], dfs[i+1][j])

        return dfs[0][0]


##old solution
#class Solution(object):
#    def __init__(self):
#        self.bDebug = True
#
#    def printGrid(self, grid):
#        print('[')
#        for line in grid:
#            print('[', end='')
#            for elem in line:
#                print('{}, '.format(elem), end='')
#            print(']')
#        print(']')
#    def minPathSum(self, grid):
#        """
#        :type grid: List[List[int]]
#        :rtype: int
#
#        my idea for a DP solution. keep a matrix w/ same dimensions for tracking min path sum per cell.
#        Start w. cell grid[n-1][m-1] where n,m = line len, column len 
#        init pathSum[n-1][m-1] to  grid[n-1][m-1] 
#        for m-1 column there's no choice so add weight. e.g pathSum[n-1][m-2] = grid[n-2][m-1] + pathSum[n-1][m-1]
#         
#        """
#        if (self.bDebug):
#            self.printGrid(grid)
#
#        if len(grid) == 0:
#            return 0
#        
#        if len(grid[0]) == 0: 
#            return 0
#
#        n = len(grid)
#        m = len(grid[0])
#        pathSums = [ [0 for x in range(m) ] for y in range(n) ]
#
#        for j in reversed(range(m)):
#            for i in reversed(range(n)):
#                if self.bDebug:
#                    print('at cell ({},{})'.format(i,j))
#                if (i==n-1) and (j==m-1): #start condition
#                    pathSums[i][j] = grid[i][j]
#                    if self.bDebug:
#                        print('at last cell ({},{})={}'.format(i,j,pathSums[i][j]))
#                elif j==m-1: #for last column only way is down
#                    pathSums[i][j] = pathSums[i+1][j] + grid[i][j]
#                    if self.bDebug:
#                        print('at last column ({},{})={}'.format(i,j,pathSums[i][j]))
#                elif i==n-1:
#                    pathSums[i][j] = pathSums[i][j+1] + grid[i][j]
#                    if self.bDebug:
#                        print('at last line ({},{})={}'.format(i,j,pathSums[i][j]))
#                else: #can go either down or right so add min(down,right)
#                    pathSums[i][j] = min(pathSums[i][j+1], pathSums[i+1][j]) + grid[i][j]
#                    if self.bDebug:
#                        print('at cell ({},{})={}'.format(i,j,pathSums[i][j]))
#
#        return pathSums[0][0]


def tests():
    print('tests()')
    grids = [
        [],
        [[]],
        [[1]],
        [[1,1]],
        [
            [1,2,3],
            [4,5,6]
            ],
        [
  [1,3,1],
  [1,5,1],
  [4,2,1]
]
    ]
    sol = Solution()

    for grid in grids:
        #sol.minPathSum(grid)
        print(f"min path sum= {sol.minPathSum(grid)}")

if __name__ == "__main__":
    print('main()')
    tests()


       
