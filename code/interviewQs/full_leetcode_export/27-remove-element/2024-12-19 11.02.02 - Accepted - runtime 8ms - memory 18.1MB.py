
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        """
        idea, iterate over nums and if nums[i] == val, swap it with nums[n-1] and reduce n by 1 
        also return number of elements not equal to val
        """
        n = len(nums)
        i = 0
        while i < n:
            print(f"i = {i}, n = {n}, nums = {nums}")
            if nums[i] == val:
                print(f"swapping {nums[i]} with {nums[n-1]}")
                while n > i and nums[n-1] == val:
                    print(f"found val on right most side {nums[n-1]}")
                    n -= 1
                if n > i:
                    nums[i] = nums[n-1]
                    n -= 1
            i += 1
        print(f"returning n = {n}, nums = {nums[:n]}")
        return n
