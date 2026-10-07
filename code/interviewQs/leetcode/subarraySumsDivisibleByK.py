"""
LC 974 — Subarray Sums Divisible by K  (Medium)

Given an integer array nums and an integer k, return the number of non-empty
subarrays that have a sum divisible by k.

A subarray is a contiguous part of an array.

Examples
--------
nums = [4, 5, 0, -2, -3, 1],  k = 5  -> 7
    # [4,5,0,-2,-3,1], [5], [5,0], [5,0,-2,-3], [0], [0,-2,-3], [-2,-3]
nums = [5],  k = 9                   -> 0

Constraints
-----------
1 <= len(nums) <= 3 * 10**4
-10**4 <= nums[i] <= 10**4
2 <= k <= 10**4
"""
"""
Value is count pref[i]%k == key where key in [0,k-1] ; here ans is how many times prefix sub sum % k is given
 remainder (key) ; we do need seed also for 0 but val is 1 - this will give right ans for [0] or [d*k] d int ,
   4. we needed at least size 2, here we don't so no need to keep indices and make sure j-i>=2 ,
     now at the end we process all reminders dics values and sum arith seq (val-1)
same as Count C(c,2) - pick all pairs from c order doesn't matter: c*(c-1)/2 
"""
from collections import defaultdict

def subarraysDivByK(nums: list[int], k: int) -> int:
    remainders_count = defaultdict(int) 
    remainders_count[0] = 1  # remainder 0 is always divisible by k, also seed so on first m*k we have 1 pair
    prefix_sum = 0
    for  n in nums:
        prefix_sum += n
        # can also use a list of size k (if k small) or another dict if n small to add sum_of_rem += remainders_count[prefix_sum % k]
        remainders_count[prefix_sum % k] += 1

    return sum(c*(c-1)//2 for c in remainders_count.values())


if __name__ == "__main__":
    cases = [
        ([4, 5, 0, -2, -3, 1], 5, 7),
        ([5], 9, 0),
        ([5], 5, 1),
        ([0], 2, 1),                  # 0 is divisible by k
        ([0, 0], 3, 3),               # [0], [0], [0,0]
        ([1, 2, 3], 3, 3),            # [3], [1,2], [1,2,3]
        ([-1, 2, 9], 2, 2),           # [2], [-1,2,9]
        ([2, -2, 2, -4], 6, 2),       # [2,-2], [-2,2]
        ([-5], 5, 1),
        ([7, -7], 7, 3),              # [7], [-7], [7,-7]
        ([1, 1, 1], 2, 2),            # [1,1] twice
        ([3, 3, 3], 3, 6),            # every subarray
    ]

    passed = 0
    for i, (nums, k, expected) in enumerate(cases, 1):
        got = subarraysDivByK(list(nums), k)
        if got == expected:
            passed += 1
        else:
            print(f"FAIL case {i}: nums={nums}, k={k} -> got {got!r}, expected {expected!r}")

    print(f"\n{passed}/{len(cases)} passed")
    assert passed == len(cases), "not all cases passed"
