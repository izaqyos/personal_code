class Solution:
    def largestDivisibleSubset(self, nums: List[int]) -> List[int]:
        nums.sort()
        dp = [(1, -1) for _ in range(len(nums))] # dp contains the length of the largest divisible subset ending at nums[i] and the index of the previous element in the subset
        for i in range(1, len(nums)):
            for j in range(i):
                if nums[i] % nums[j] == 0:
                    if dp[j][0] + 1 > dp[i][0]:
                        dp[i] = (dp[j][0] + 1, j)
        max_len = 0
        end_index = -1
        for i in range(len(nums)):
            if dp[i][0] > max_len:
                max_len = dp[i][0]
                end_index = i
        result = []
        while end_index != -1:
            result.append(nums[end_index])
            end_index = dp[end_index][1]
        result.reverse()
        return result
        