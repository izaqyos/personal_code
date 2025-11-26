
class Solution:
    def maximalSquare(self, matrix: list[list[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0
        m,n = len(matrix), len(matrix[0])
        dp = [ [0 for _ in matrix[0]] for _ in matrix]
        max_rect_size = 0
        for i in range(m):
            dp[i][n-1] = int(matrix[i][n-1]) #in last column max size is at max 1 since it's not possible to increase size by expanding right, down or diagonal
            #print(f"matrix[{i}][{n-1}] = {matrix[i][n-1]}, dp[{i}][{n-1}] = {dp[i][n-1]}, max_rect_size={max_rect_size}")
            if dp[i][n-1] == 1:
                #print(f"found cell 1 in {i},{n-1}")
                max_rect_size = 1
        for j in range(n):
            dp[m-1][j] = int(matrix[m-1][j])
            if dp[m-1][j] == 1:
                #print(f"found cell 1 in {m-1},{j}")
                max_rect_size = 1

        #now let's fill the rest top down and keep tabs on max size seen
        for i in range(m-2, -1, -1):
            for j in range(n-2, -1, -1):
                #print(f"checking {i},{j}={matrix[i][j]} , max_rect_size = {max_rect_size}, dp={dp}")
                if matrix[i][j] == "1":
                    dp[i][j] = 1
                    #print(f"dp at {i},{j} = {dp[i][j]}")
                    min_adjacent_squares_size = min(dp[i+1][j] ,  dp[i+1][j+1] ,  dp[i][j+1] )
                    if min_adjacent_squares_size >= dp[i][j]:
                        #print(f"found bigger square at {i},{j} of size {min_adjacent_squares_size +1}")
                        dp[i][j] = min_adjacent_squares_size +1
                    max_rect_size = max(max_rect_size, dp[i][j])

        return max_rect_size*max_rect_size
