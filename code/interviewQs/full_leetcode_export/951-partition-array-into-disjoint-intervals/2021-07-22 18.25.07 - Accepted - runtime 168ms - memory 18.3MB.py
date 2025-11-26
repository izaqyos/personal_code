class Solution:
    def partitionDisjoint(self, nums: List[int]) -> int:
        n = len(nums)
        lastMax = nums[0]
        localMax = lastMax
        partition = 0
        
        for i in range(1,n):
            if nums[i]<lastMax:
                partition = i
                lastMax = localMax
            else:
                localMax = max(localMax, nums[i])
        return partition+1
                
        