"""
LC 31. Next Permutation (Medium)

A permutation of an array of integers is an arrangement of its members into a
sequence or linear order.

The next permutation of an array of integers is the next lexicographically
greater permutation of its integers. More formally, if all the permutations of
the array are sorted in one container according to their lexicographical
order, then the next permutation of that array is the permutation that follows
it in the sorted container. If such an arrangement is not possible, the array
must be rearranged as the lowest possible order (i.e., sorted in ascending
order).

- [1,2,3] -> [1,3,2]
- [2,3,1] -> [3,1,2]
- [3,2,1] -> [1,2,3] (no lexicographically larger rearrangement)

Given an array of integers nums, find the next permutation of nums.
The replacement must be in place and use only constant extra memory.

Example 1: nums = [1,2,3] -> [1,3,2]
Example 2: nums = [3,2,1] -> [1,2,3]
Example 3: nums = [1,1,5] -> [1,5,1]

Constraints:
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 100
"""

from itertools import permutations


class Solution:
    def nextPermutation(self, nums: list[int]) -> None:
        """Do not return anything, modify nums in-place instead."""
        """
        three phases. 
        a. find pivot. k=n-1 , move k right so long as nums[k-1]>=nums[k], pivot loc is k-1 (if k==0 we skip swap)
        b. find swap trg again r=n-1, move r right until we find r>=k nums[r] > nums[k-1] , now we swap them
        note nums[k..n-1] still dsc. b.c nums[r-1]>=nums[r]>nums[k-1]>=nums[r+1] (b.c r is first loc to the right where nums[r]>nums[k-1])
        c. now that we changes most significant digit lets start from smallest num, we need to make nums[k..n-1] asc instead of dsc
        d. we now its dsc so we can have l=k, r=n-1 while l<r swap(l,r) 
        """
        n = len(nums)
        k = n-1
        l,r = 0, n-1
        while k>0 and nums[k-1]>=nums[k]:
            k-=1
        
            
        if k>0: #swap only if k>0 otherwise number is fully dsc we need to wrap around - make it asc
            while r>=k:
                if nums[r] > nums[k-1]:
                    nums[r], nums[k-1] = nums[k-1], nums[r]
                    l = k
                    break
                r-=1
        
        r = n-1 # reset r 
        #now make asc
        while l<r:
            nums[l], nums[r] = nums[r], nums[l]
            l+=1
            r-=1
                

        


def _oracle(nums: list[int]) -> list[int]:
    """Brute force: next distinct permutation in sorted order, wrapping to the smallest."""
    perms = sorted(set(permutations(nums)))
    i = perms.index(tuple(nums))
    return list(perms[(i + 1) % len(perms)])


if __name__ == "__main__":
    import random

    cases = [
        ([1, 2, 3], [1, 3, 2]),
        ([3, 2, 1], [1, 2, 3]),
        ([1, 1, 5], [1, 5, 1]),
        ([1], [1]),
        ([2, 3, 1], [3, 1, 2]),
        ([1, 3, 2], [2, 1, 3]),
        ([1, 5, 8, 4, 7, 6, 5, 3, 1], [1, 5, 8, 5, 1, 3, 4, 6, 7]),
        ([5, 1, 1], [1, 1, 5]),
        ([1, 5, 1], [5, 1, 1]),
        ([2, 2, 2], [2, 2, 2]),
    ]
    passed = 0
    for nums, want in cases:
        got = list(nums)
        Solution().nextPermutation(got)
        assert got == want, f"{nums}: got {got}, want {want}"
        passed += 1

    rng = random.Random(31)
    for _ in range(300):
        nums = [rng.randint(0, 4) for _ in range(rng.randint(1, 7))]
        got = list(nums)
        Solution().nextPermutation(got)
        want = _oracle(nums)
        assert got == want, f"{nums}: got {got}, want {want}"
        passed += 1

    print(f"{passed}/{passed} passed")
