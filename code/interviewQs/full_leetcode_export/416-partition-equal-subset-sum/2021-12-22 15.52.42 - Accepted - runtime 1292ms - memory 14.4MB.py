class Solution:
    def canPartitionRecursive(self, nums: List[int]) -> bool:
        """
        if sum(nums)%2 == 1 then return False (no way to partition)
        else, j
        """
        import functools
        sumall = functools.reduce(lambda a,b: a+b, nums) 
        if sumall %2 !=0:
            return False
        return self.dfs(nums, sumall/2, 0) #True if there's a subset of nums whose sum is half total sum

    def dfs(self, nums, sumr, i):
        if sumr == 0:
            return True

        if i == len(nums) or sumr < 0:
            return False

        return self.dfs(nums, sumr-nums[i], i+1) or self.dfs(nums, sumr, i+1)

    def canPartition(self, nums: List[int]) -> bool:
        """
        if sum(nums)%2 == 1 then return False (no way to partition) O(n)
        else, build array of length sumall//2+1, where dp[j] is True iff nums contain subset whose sum is j
        """
        import functools
        sumall = functools.reduce(lambda a,b: a+b, nums) 
        if sumall %2 !=0:
            return False
        dp=[False for _ in range(sumall//2+1)] 
        dp[0] = True #take empty set to get 0 sum
        for n in nums:
            for j in range(sumall//2,n-1,-1):
                if (n == j) or dp[j-n] == True:
                    dp[j] = True
        return dp[sumall//2]

