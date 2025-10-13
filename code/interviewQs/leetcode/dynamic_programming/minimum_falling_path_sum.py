"""
Minimum Falling Path Sum
Given an n x n array of integers matrix, return the minimum sum of any falling path through matrix.

A falling path starts at any element in the first row and chooses the element in the next row that is either directly below or diagonally left/right. Specifically, the next element from position (row, col) will be (row + 1, col - 1), (row + 1, col), or (row + 1, col + 1).

Example 1:

Input: matrix = [[2,1,3],[6,5,4],[7,8,9]]
Output: 13
Explanation: There are two falling paths with a minimum sum as shown.
Example 2:


Input: matrix = [[-19,57],[-40,-5]]
Output: -59
Explanation: The falling path with a minimum sum is shown.
Constraints:

n == matrix.length == matrix[i].length
1 <= n <= 100
-100 <= matrix[i][j] <= 100
"""

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

