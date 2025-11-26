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
