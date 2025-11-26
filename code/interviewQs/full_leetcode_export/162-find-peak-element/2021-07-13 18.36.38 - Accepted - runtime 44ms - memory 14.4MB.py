class Solution:
    def islocalpeak(self, nums, i):
        if len(nums) == 1:
            return True
        if i==0 and nums[i+1]<nums[i]:
            return True
        if (i==len(nums)-1) and nums[i-1]<nums[i]:
            return True
        if nums[i+1]<nums[i] and nums[i-1]<nums[i]:
            return True
            
    def findPeakElement(self, nums: List[int]) -> int:
        """ binary search """
        l,h = 0, len(nums)-1
        while l<=h:
            m = (h+l)//2
            if self.islocalpeak(nums,m):
                return m
            elif (m>0) and nums[m-1]>nums[m]:
                h=m
            elif (m<len(nums)-1) and nums[m+1]>nums[m]:
                l=m+1
            