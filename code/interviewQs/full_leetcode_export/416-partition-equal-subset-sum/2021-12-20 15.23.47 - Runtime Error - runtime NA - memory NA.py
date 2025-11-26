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
        else, build bool matrix dp, dimenstions: nX(sum(n)/2)
        where dp[i][j] means that elements 0-i contain subset whose sum is j
        dp[n][sum(n)/2] is True means we can partition 
        """
        import functools
        sumall = functools.reduce(lambda a,b: a+b, nums) 
        if sumall %2 !=0:
            return False
        dp=[[False for _ in range(len(nums)+1)] for _ in range(sumall/2+1)]

        for i in range(1,len(nums)): #we can skip i==0 (no elements), dp[0][j] where j>0 is always False and dp is initialised to False so we can skip
            for j in range(sumall/2+1):
                if j == 0:
                    dp[i][j] = True #can always find subset whose sum is 0 - the empty set
            else: #handle ith elem nums[i-1]
                if nums[i-1] > j: #we can use ith elem to get sum j since its bigger than sum
                    dp[i][j] = dp[i-1][j]
                else: #recursion condition like: return self.dfs(nums, sumr-nums[i], i+1) or self.dfs(nums, sumr, i+1)
                    dp[i][j] = dp[i-1][j] or dp[i-1][j-nums[i-1]]
                
        return dp[n][sumall/2]
