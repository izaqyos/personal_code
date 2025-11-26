class Solution:
    def lengthOfLISDP(self, nums):
        """
        recursion. 
        LIS(nums, n) = max(join(LIS(nums,j),j, nums[n]) (j in {0,..,n-1})
        join(lis, j, num):
            if num>nums[j]:
                return lis+1
            else:
                return lis
        complexity: each pass has n steps of calling LIS(0,..,n-1) , seems to
        me like o(n!)

        DP save LIS values instead of call recursion. o(n^2) 
        """
        if len(nums) == 0:
            return 0

        LISDP = [1 for i in nums]
        n = len(nums)
        for i in range(1,n):
            for j in range(0,i):
                if nums[i] > nums[j]:
                    LISDP[i] = max(LISDP[i], LISDP[j]+1)

        return LISDP[n-1]



    def lengthOfLIS(self, nums):
        return self.lengthOfLISDP(nums)