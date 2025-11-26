class Solution:
    def orderOfLargestPlusSign(self, n: int, mines: List[List[int]]) -> int:
        """
        idea. gen a nXn 1s matrix.  First set all mine locations to 0
        Then build four nXN DP matrices. l,r,u,d - left, right, up, down. 
        where i,j of each is how many consecutive 1s are from pos i,j in the corresponding direction
        TLE. complexity: NX2N
        """
        matrix = [ [1 for _ in range(n)] for _ in range(n) ]
        for idx in mines:
            matrix[idx[0]][idx[1]] = 0
        left = [ [0 for _ in range(n)] for _ in range(n) ]
        right = [ [0 for _ in range(n)] for _ in range(n) ]
        up = [ [0 for _ in range(n)] for _ in range(n) ]
        down = [ [0 for _ in range(n)] for _ in range(n) ]
        for i in range(n):
            for j in range(1, n):
                if matrix[i][j]: 
                    left[i][j] = left[i][j-1]+1
                    down[j][i] = left[j-1][i]+1
                else:
                    left[i][j] = 0
                    down[j][i] = 0
            for j in range(n-2,0,-1):
                if matrix[i][j]: 
                    right[i][j] = left[i][j+1]+1
                    up[i][j] = up[i][j+1]+1
                else:
                    right[i][j] = 0
                    up[j][i] = 0
        maxorder = 0
        for i in range(n):
            for j in range(n):
                if not matrix[i][j]:
                    continue
                localmax=min(left[i][j], right[i][j], up[i][j], down[i][j])
                if localmax>maxorder:
                    maxorder = localmax
        return maxorder
