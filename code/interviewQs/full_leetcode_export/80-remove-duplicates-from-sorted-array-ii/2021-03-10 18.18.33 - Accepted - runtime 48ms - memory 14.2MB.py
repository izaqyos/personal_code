class Solution:
    def removeDuplicates(self, nums):
        """
        idea, run two indices. running and latest
        swap latest (non valid address) with next valid
        validity condition. repeat < 3.
        note. sorted means if we have three elements. a1,a2,a3 if a3==a1 => a3==a2. so we can skip one comparison
        """
        n = len(nums)
        if n<3:
            return n

        last = 2
        for i in range(2,n):
            if nums[i]!=nums[last-2]:
                nums[last],nums[i] = nums[i], nums[last]
                last+=1
        return last