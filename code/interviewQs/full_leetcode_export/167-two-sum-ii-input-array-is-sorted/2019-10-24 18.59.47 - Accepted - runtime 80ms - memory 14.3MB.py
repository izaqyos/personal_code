class Solution:
        def twoSum(self, nums, target):
            i = 0
            j = len(nums)-1
            while j>i: 
                if (nums[j] + nums[i]) == target:
                    return [i+1,j+1]
                if (nums[j] + nums[i]) > target:
                    j = j-1
                if (nums[j] + nums[i]) < target:
                    i = i+1
    