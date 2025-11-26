class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        idea , use a pointer to keep track of the next unique value
        move elements that are unique to that pointer and move it by one only when a unique value is found
        """
        if not nums:
            return 0
        next_unique = 0
        for i in range(1, len(nums)):
            if nums[next_unique] != nums[i]:
                next_unique += 1
                nums[next_unique] = nums[i]
        return next_unique + 1
