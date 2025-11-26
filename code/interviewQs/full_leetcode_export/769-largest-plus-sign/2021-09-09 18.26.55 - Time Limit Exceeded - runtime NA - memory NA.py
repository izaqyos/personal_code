class Solution:
    def orderOfLargestPlusSign(self, n: int, mines: List[List[int]]) -> int:
        """
        idea. gen a nXn 1s matrix.  First set all mine locations to 0
        Then build four nXN DP matrices. l,r,u,d - left, right, up, down. 
        where i,j of each is how many consecutive 1s are from pos i,j in the corresponding direction
        """
        matrix = [ [1 for _ in range(n)] for _ in range(n) ]
        for idx in mines:
            matrix[idx[0]][idx[1]] = 0
        left = [ [0 for _ in range(n)] for _ in range(n) ]
        right = [ [0 for _ in range(n)] for _ in range(n) ]
        up = [ [0 for _ in range(n)] for _ in range(n) ]
        down = [ [0 for _ in range(n)] for _ in range(n) ]
        for i in range(n):
            for j in range(n):
                ci, cj= i,j
                while cj>=0:
                    if matrix[ci][cj]:
                        left[ci][cj] +=1
                        cj-=1
                    else:
                        break
                ci, cj= i,j
                while cj<n:
                    if matrix[ci][cj]:
                        right[ci][cj] +=1
                        cj+=1
                    else:
                        break
                ci, cj= i,j
                while ci>=0:
                    if matrix[ci][cj]:
                        down[ci][cj] +=1
                        ci-=1
                    else:
                        break
                ci, cj= i,j
                while ci<n:
                    if matrix[ci][cj]:
                        up[ci][cj] +=1
                        ci+=1
                    else:
                        break
        maxorder = 0
        for i in range(n):
            for j in range(n):
                localmax=min(left[i][j], right[i][j], up[i][j], down[i][j])
                if localmax>maxorder:
                    maxorder = localmax
        return maxorder
