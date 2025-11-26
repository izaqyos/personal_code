class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        """
        idea, iterate over nums and if nums[i] == val, swap it with nums[n-1] and reduce n by 1 
        also return number of elements not equal to val
        """
        n = len(nums)
        i = 0
        while i < n:
            if nums[i] == val:
                while n > i and nums[n-1] == val:
                    n -= 1
                nums[i] = nums[n-1]
                n -= 1
            i += 1
        return n
