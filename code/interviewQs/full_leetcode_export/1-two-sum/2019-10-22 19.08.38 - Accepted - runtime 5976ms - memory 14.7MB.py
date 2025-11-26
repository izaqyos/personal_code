class Solution:
    #def twoSum(self, nums: List[int], target: int) -> List[int]:
    def twoSum(self, nums, target):
        #twoSums={} #can be used if more than one pair is possible, like in amazon packages and truck question 
        #nums = sorted(nums) #0(nlogn)

        """
        min time complexity. o(n^2). since we must take into account all pairs.
        and selecting 2 from n is binomial coefficient so n*(n-1)/2
        """

        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                sum = nums[i] + nums[j]
                if sum == target:
                    return [i,j]
