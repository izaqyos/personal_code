class Solution:
    def rob(self, nums: List[int]) -> int:
        h = nums
        n = len(h)
        if not h:
            return 0
        elif n == 1:
            return h[0]
        elif n == 2:
            return max(h[0],h[1])
        dp = [0 for _ in range(len(h)+1)]
        dp[n-1] = h[n-1]
        dp[n-2] = max(h[n-2], h[n-1])
        for i in range(n-3, -1, -1):
            dp[i] = max(h[i]+dp[i+2], h[i+1]+dp[i+3])
        return dp[0]

    def deleteAndEarn(self, nums: List[int]) -> int:
        vals = [0 for _ in range(105)]
        for n in nums:
            vals[n]+=n
        return self.rob(vals)
