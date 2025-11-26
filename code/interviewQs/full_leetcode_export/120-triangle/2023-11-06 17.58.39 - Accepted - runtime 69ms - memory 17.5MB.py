class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        if not triangle:
            return -1
        m = len(triangle)
        if m == 1 :
            return triangle[0][0]

        dp = [ [ _ for _ in row] for row in triangle ]
        for i in range(m-2,-1,-1):
            for j in range(len(triangle[i])):
               dp[i][j] = triangle[i][j] + min(dp[i+1][j], dp[i+1][j+1])

        return dp[0][0]
