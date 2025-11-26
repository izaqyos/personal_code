class Solution:
    def minFallingPathSum(self, matrix: List[List[int]]) -> int:
        """
Idea, use dp approach to calculate the path sum from the end back to start
when setting the path sums to the first row also update minimum seen
        """
        n = len(matrix)
        if n == 0:
            return -1
        if n==1:
            return matrix[0][0]
        dp = [ row[:] for row in matrix]

        for i in range(n-2,-1,-1):
            for j in range(n-1,-1,-1):
                if j == 0:
                    dp[i][j] = matrix[i][j] + min(dp[i+1][j], dp[i+1][j+1])
                elif j == n-1:
                    dp[i][j] = matrix[i][j] + min(dp[i+1][j-1], dp[i+1][j])
                else :
                    dp[i][j] = matrix[i][j] + min(dp[i+1][j-1], dp[i+1][j], dp[i+1][j+1])

        min_path_sum = float('inf')
        for j in range(n):
            min_path_sum = min(min_path_sum, dp[0][j])

        return min_path_sum
