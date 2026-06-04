"""
LC 15 — 3Sum (Medium)

Given an integer array `nums`, return all *unique* triplets [a, b, c] such that
a + b + c == 0, drawn from distinct indices in `nums`.

The result must not contain duplicate triplets (treat each triplet as a multiset).

Aim for O(n²) time, O(1) extra space (sort + two-pointer per anchor).
The naive O(n³) brute force gets no credit.

Constraints:
    3 <= len(nums) <= 3000
    -10^5 <= nums[i] <= 10^5

Examples:
    [-1, 0, 1, 2, -1, -4]   -> [[-1, -1, 2], [-1, 0, 1]]
    [0, 1, 1]               -> []
    [0, 0, 0]               -> [[0, 0, 0]]
    [0, 0, 0, 0]            -> [[0, 0, 0]]          (no duplicate triplets)
    [-2, 0, 1, 1, 2]        -> [[-2, 0, 2], [-2, 1, 1]]
    [1, 2, -2, -1]          -> []
    [-1, -1, 2]             -> [[-1, -1, 2]]

Edge cases to think about:
    - all zeros (n large) — must return exactly one [0,0,0]
    - heavy duplicates — must dedupe both the anchor and the inner pointers
    - all positive or all negative — no solution
    - exactly n = 3 with no sum-to-zero
    - mixed signs with multiple solutions
"""
from typing import List


def three_sum(nums: List[int]) -> List[List[int]]:
    """
three pointers.
anchor steady move from 0 - n-3
then in window right of anchor l(eft) and r(ight) move from anchor + 1 , n-1 in reverse direction 
if nums at anchor + l + r == target then add to result and move both pointers 
important slide anchor right on equal values, on found target move l,r on same nums 
l moves right, r moves left , never cross
l<r always 

so we have three branches 
the sum of 3 < 0 , l += 1 (we need bigger)
elif the sum of 3 > 0 , r -= 1 (we need smaller)
else (== 0) 
    capture triplet, l+=1, r-=1 now slide l,r on same vals
    """
    if not nums:
        return []
    n = len(nums)
    if n < 3:
        return []
    if n == 3:
        if nums[0] + nums[1] + nums[2] == 0:
            return [[nums[0], nums[1], nums[2]] ]
        else:
            return []
    anc, l, r = 0, 1, n-1 # invariant anc<l<r so anc at most n-3
    triplets: List[List[int]] = []
    nums.sort()
    for anc in range(n-2):
        if anc > 0 and nums[anc] == nums[anc -1]:
            continue # skip duplicates
        l = anc +1 
        r = n-1
        while l<r:
            if nums[anc] + nums[l] + nums[r] < 0 :
                l += 1
            elif nums[anc] + nums[l] + nums[r] > 0 :
                r -= 1
            else:
                # capture triplet, l+=1, r-=1 now slide l,r on same vals
                triplets.append([nums[anc], nums[l], nums[r]])
                l += 1
                r -= 1
                while l<n and nums[l] == nums[l - 1]:
                    l += 1
                while r>0 and nums[r] == nums[r + 1]:
                    r -= 1
                if l>=r:
                    break
    
    return triplets


def _normalize(triplets):
    """sort each triplet internally and sort the outer list — order-insensitive compare"""
    if triplets is None:
        return None
    return sorted(sorted(t) for t in triplets)


if __name__ == "__main__":
    cases = [
        ([-1, 0, 1, 2, -1, -4],   [[-1, -1, 2], [-1, 0, 1]]),
        ([0, 1, 1],               []),
        ([0, 0, 0],               [[0, 0, 0]]),
        ([0, 0, 0, 0],            [[0, 0, 0]]),
        ([-2, 0, 1, 1, 2],        [[-2, 0, 2], [-2, 1, 1]]),
        ([1, 2, -2, -1],          []),
        ([-1, -1, 2],             [[-1, -1, 2]]),
        ([3, 0, -2, -1, 1, 2],    [[-2, -1, 3], [-2, 0, 2], [-1, 0, 1]]),
        ([1, 1, 1],               []),
        ([-1, -1, -1],            []),
        ([1, 2, 3, 4, 5],         []),
    ]

    passed = 0
    for nums, expected in cases:
        got = three_sum(list(nums))
        ok = _normalize(got) == _normalize(expected)
        passed += ok
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] three_sum({nums}) = {got}  (expected {expected})")

    print(f"\n{passed}/{len(cases)} passed")
    assert passed == len(cases), "some cases failed"
