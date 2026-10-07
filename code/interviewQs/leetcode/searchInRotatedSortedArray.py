"""
LC 33 - Search in Rotated Sorted Array (Medium)

There is an integer array nums sorted in ascending order (with distinct
values). Prior to being passed to your function, nums is possibly rotated
at an unknown pivot index k (1 <= k < nums.length) such that the resulting
array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]
(0-indexed).

Given the array nums after the possible rotation and an integer target,
return the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
    Input: nums = [4,5,6,7,0,1,2], target = 0
    Output: 4

Example 2:
    Input: nums = [4,5,6,7,0,1,2], target = 3
    Output: -1

Example 3:
    Input: nums = [1], target = 0
    Output: -1

Constraints:
    1 <= nums.length <= 5000
    -10^4 <= nums[i] <= 10^4
    All values of nums are unique.
    nums is an ascending array that is possibly rotated.
    -10^4 <= target <= 10^4
"""
from typing import List


def search(nums: List[int], target: int) -> int:
    if not nums: return -1
    n = len(nums)

    #optimization, general algo will handle this case as well
    if n == 1:
        if nums[0] == target: 
            return 0
        else:
            return -1

    l, r = 0, n - 1
    while l<=r:
        m = (l+r)//2
        if nums[m] == target: 
            return m
        # lets determine which side is sorted
        if nums[l] <= nums[m]: # left side is sorted, note no dupe so only == when l is m (can happen for even sized array slice)
            if nums[l] <= target < nums[m]: # cool, we can search in this side
                r = m - 1
            else: # we must search right
                l = m+1
        else: # if right side is sorted we search there, otherwise we search left side
            if nums[m] < target <= nums[r]: # cool, we can search in this side
                l = m + 1
            else: # left side not sorted but target 4 sure not in right so we search left
                r = m-1
    return -1
    


if __name__ == "__main__":
    assert search([4,5,6,7,0,1,2], 0) == 4
    assert search([4,5,6,7,0,1,2], 3) == -1
    assert search([1], 0) == -1
    assert search([1], 1) == 0
    assert search([5,1,3], 5) == 0
    assert search([3,1], 1) == 1
    assert search([4,5,6,7,8,1,2,3], 8) == 4

    print("All tests passed.")
