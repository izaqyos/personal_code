class Solution:
    def twoSum(self, nums, target):
        """
        time complexity. o(n). we will use a dictionary of values to indices to check if there's a pair 
        memory complexity o(n). dictionary w/ up to n-1 values
        """ 
        nums2index = dict()
        for i in range(len(nums)):
            delta = target - nums[i]

            if (delta in nums2index):
                return [nums2index[delta], i]

            nums2index[nums[i]] = i
