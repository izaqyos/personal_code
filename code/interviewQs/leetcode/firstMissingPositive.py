"""
LC 41 — First Missing Positive (Hard)

Given an unsorted integer array `nums`, return the smallest positive integer
that is NOT present in `nums`.

You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary
space (the input array itself may be modified).

Constraints:
    1 <= len(nums) <= 1e5
    -2^31 <= nums[i] <= 2^31 - 1

Examples:
    [1, 2, 0]        -> 3
    [3, 4, -1, 1]    -> 2
    [7, 8, 9, 11, 12] -> 1
    [1]              -> 2
    [2, 1]           -> 3
    [1, 1]           -> 2

Edge cases to think about:
    - all negatives / zeros          -> answer is 1
    - duplicates
    - values way larger than n
    - n = 1

    idea:
    lest mark spi_not = the smallest positive integer that is NOT present in `nums`.
    spi_not is in range 1 to n+1. "worst case" nums is 1-n so spi_not is n+1 otherwise its <=n
    with that in mind we can use nums to track seen nums. how? use -1*nums[i] to mark i+1 seen 
    ofc that only works if nums has only positive integers but we can assure that nums is only positive integers
    by swapping all negative integers and >n with a placeholder. say n+1
    so one sweep to normalize nums to be positive integers
    second sweep to mark seen nums by *-1 nums[i] = -1*nums[i] means i+1 is seen
    third sweep to find first positive number, which means spi_not is the first positive number in nums (index +1)
    
"""
from typing import List


def first_missing_positive(nums: List[int]) -> int:
    if not nums:
        return 1

    n = len(nums)
    dummy_val = n+1

    for i,num  in enumerate(nums):
        if num<=0 or num>n:
            nums[i] = dummy_val
    
    for i,num  in enumerate(nums):
        val = abs(num)
        if val < n+1 and nums[val-1] > 0 : 
            nums[val-1] *= -1
    
    for i,num  in enumerate(nums):
        if num > 0:
            return i +1

    return n + 1



if __name__ == "__main__":
    cases = [
        ([1, 2, 0], 3),
        ([3, 4, -1, 1], 2),
        ([7, 8, 9, 11, 12], 1),
        ([1], 2),
        ([2, 1], 3),
        ([1, 1], 2),
        ([0], 1),
        ([-1, -2, -3], 1),
        ([2, 2], 1),
        ([1, 2, 3, 4, 5], 6),
    ]

    passed = 0
    for nums, expected in cases:
        got = first_missing_positive(list(nums))
        ok = got == expected
        passed += ok
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] first_missing_positive({nums}) = {got}  (expected {expected})")

    print(f"\n{passed}/{len(cases)} passed")
    assert passed == len(cases), "some cases failed"
