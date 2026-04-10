"""
217. Contains Duplicate
https://leetcode.com/problems/contains-duplicate/

Given an integer array nums, return true if any value appears at least twice
in the array, and return false if every element is distinct.

Constraints:
- 1 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9

Example 1: nums = [1,2,3,1]       -> true
Example 2: nums = [1,2,3,4]       -> false
Example 3: nums = [1,1,1,3,3,5,3,2,4,2] -> true
"""

from typing import List
#from collections import defaultdict

def contains_duplicate(nums: list[int]) -> bool:
    # O(n) time complexity, O(n) space complexity , use seen set
    seen = set[int]()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
        
    return False


if __name__ == "__main__":
    tests = [
        ([1, 2, 3, 1], True),
        ([1, 2, 3, 4], False),
        ([1, 1, 1, 3, 3, 5, 3, 2, 4, 2], True),
        ([1], False),                    # single element
        ([1, 1], True),                  # minimal duplicate
        ([-1, -1], True),                # negative duplicates
        ([-1, 1], False),                # negative vs positive
        (list(range(100000)), False),     # large array, no dupure
        (list(range(99999)) + [0], True), # large array, one dup at end
    ]
    for i, (nums, expected) in enumerate(tests):
        result = contains_duplicate(nums)
        label = f"len={len(nums)}" if len(nums) > 10 else f"nums={nums}"
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i+1}: {status} | {label}, expected={expected}, got={result}")
