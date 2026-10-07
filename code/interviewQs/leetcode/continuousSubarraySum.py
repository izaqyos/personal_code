"""
LC 523 — Continuous Subarray Sum  (Medium)

Given an integer array nums and an integer k, return True if nums has a
*continuous* subarray of size **at least two** whose elements sum up to a
multiple of k, or False otherwise.

An integer x is a multiple of k if there exists an integer n such that x = n * k.
0 is always a multiple of k.

Examples
--------
nums = [23, 2, 4, 6, 7],  k = 6   -> True    # [2, 4] sums to 6
nums = [23, 2, 6, 4, 7],  k = 6   -> True    # whole array sums to 42 = 7 * 6
nums = [23, 2, 6, 4, 7],  k = 13  -> False

Constraints
-----------
1 <= len(nums) <= 10**5
0 <= nums[i] <= 10**9
0 <= sum(nums) <= 2**31 - 1
1 <= k <= 2**31 - 1

Note the constraints: nums is non-negative, and k >= 1.

I worked out the way to solve, use map:
- key = prefix_sum % k
- value = earliest index with that remainder, never overwritten (overwriting shrinks the gap → false negatives)
- query = "have I seen this remainder before?"
- invariant (the trick :) ) = if prefix[j] ≡ prefix[i] (mod k) then nums[i+1..j] sums to a multiple of k; that subarray has length j - i, so the size rule is j - i >= 2
- seed -1 , also map index -1 in key 0 so we catch subarr starting at 0
"""
from typing import List


def checkSubarraySum(nums: List[int], k: int) -> bool:

    prefix_sum = 0
    reminders_seen = {0 : -1 }
    for i, num in enumerate(nums):
        prefix_sum += num
        pmodk = prefix_sum % k
        prev = reminders_seen.get(pmodk)
        if prev is not None:
            if i - prev > 1:
                return True
        else:
            reminders_seen[pmodk] = i

    return False
        


if __name__ == "__main__":
    cases = [
        ([23, 2, 4, 6, 7], 6, True),       # [2, 4]
        ([23, 2, 6, 4, 7], 6, True),       # whole array, 42
        ([23, 2, 6, 4, 7], 13, False),
        ([1, 2, 3], 5, True),              # [2, 3]
        ([1, 2, 12], 6, False),
        ([1, 0], 2, False),                # only size-2 subarray sums to 1
        ([0, 0], 1, True),
        ([0, 1, 0], 1, True),
        ([5, 0, 0, 0], 3, True),           # [0, 0] sums to 0
        ([1], 1, False),                   # size must be >= 2
        ([1, 1], 2, True),
        ([29, 6, 5], 11, True),            # [6, 5]
        ([2, 4, 3], 6, True),              # [2, 4]
        ([1, 2, 4], 7, True),
        ([0], 1, False),
    ]

    passed = 0
    for i, (nums, k, expected) in enumerate(cases, 1):
        got = checkSubarraySum(list(nums), k)
        if got == expected:
            passed += 1
        else:
            print(f"FAIL case {i}: nums={nums}, k={k} -> got {got!r}, expected {expected!r}")

    print(f"\n{passed}/{len(cases)} passed")
    assert passed == len(cases), "not all cases passed"
