class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        if not triangle:
            return -1
        m = len(triangle)
        if m == 1 :
            return triangle[0][0]

        dp = [0 for _ in range(m+1) ]
        iplus1val, temp = 0,0
        for i in range(m-1, -1, -1):
            iplus1val = dp[i+1] 
            for j in range(i, -1, -1):
                temp = dp[j]
                print(f"i={i}, j={j}, temp={temp}, dp[j]=triangle[i][j]={triangle[i][j]} + min(dp[j]={dp[j]}, iplus1val={iplus1val})")
                dp[j]=triangle[i][j] + min(dp[j], iplus1val)
                iplus1val = temp
        return dp[0]
