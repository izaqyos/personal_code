"""
LC 560 — Subarray Sum Equals K  (Medium)

Given an array of integers `nums` and an integer `k`, return the total number of
subarrays whose sum equals `k`.

A subarray is a contiguous non-empty sequence of elements within an array.

Examples:
    Input:  nums = [1, 1, 1], k = 2
    Output: 2
    (the subarrays [1,1] at indices 0-1 and 1-2)

    Input:  nums = [1, 2, 3], k = 3
    Output: 2
    ([3] and [1,2])

Constraints:
    1 <= len(nums) <= 2 * 10**4
    -1000 <= nums[i] <= 1000
    -10**7 <= k <= 10**7

Note: values can be negative and zero -- sliding window does not apply.
"""

from typing import List


def subarray_sum(nums: List[int], k: int) -> int:
    prefix_sum = 0
    count = 0
    prefix_sum_counts = {0: 1}
    for n in nums:
        prefix_sum += n
        count += prefix_sum_counts.get(prefix_sum - k, 0)
        prefix_sum_counts[prefix_sum] = prefix_sum_counts.get(prefix_sum, 0) + 1
    return count


if __name__ == "__main__":
    assert subarray_sum([1, 1, 1], 2) == 2
    assert subarray_sum([1, 2, 3], 3) == 2

    # single element
    assert subarray_sum([5], 5) == 1
    assert subarray_sum([5], 3) == 0

    # k = 0
    assert subarray_sum([0, 0, 0], 0) == 6
    assert subarray_sum([1, -1, 0], 0) == 3

    # negatives
    assert subarray_sum([-1, -1, 1], 0) == 1
    assert subarray_sum([3, 4, -7, 1, 3, 3, 1, -4], 7) == 4

    # subarray starting at index 0
    assert subarray_sum([1, 2, 3], 6) == 1

    # no match
    assert subarray_sum([1, 2, 3], 100) == 0

    # overlapping counts
    assert subarray_sum([1, 2, 1, 2, 1], 3) == 4

    print("all tests pass")
