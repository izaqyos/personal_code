class Solution:
    def findUnsortedSubarray(self, nums: List[int]) -> int:
        #naive o(nlogn) solution
        ns = sorted(nums)
        i =0
        while i<len(nums) and ns[i] == nums[i]:
            i+=1
        j=len(nums)-1
        while  j>0 and ns[j] == nums[j]:
            j-=1
        if j>i:
            return j-i+1
        else:
            return 0
            