"""
LC 42 — Trapping Rain Water (Hard)

Given n non-negative integers representing an elevation map where the width of
each bar is 1, compute how much water it can trap after raining.

Water above index i = max(0, min(maxLeft[i], maxRight[i]) - height[i])
Total = sum over all i.

Aim for O(n) time, O(1) extra space (two pointers).

Constraints:
    1 <= len(height) <= 2 * 10^4
    0 <= height[i] <= 10^5

Examples:
    [0,1,0,2,1,0,1,3,2,1,2,1] -> 6
    [4,2,0,3,2,5]             -> 9
    [0,0,0,0]                 -> 0
    [3,0,3]                   -> 3
    [5,4,3,2,1]               -> 0   (monotonic decreasing)
    [1,2,3,4,5]               -> 0   (monotonic increasing)
    [1]                       -> 0
    [2,2]                     -> 0

Edge cases to think about:
    - n < 3 (no water possible)
    - flat array
    - monotonic up / down
    - single peak vs. valley between two equal peaks
    - very tall walls bracketing a wide flat zone
"""
from typing import List


"""
2 ptr strat, 
advance lower ptr always, 
save 2 calc water 4 i w/o scanning r b/c
 we only advance left if its lower than right and even if right side isn't lowest (in range l+1..r) its still a wall
high enough, so left max is at most height[right] which in turn is at most right max 
so min(left max, true right max (not neccesarily known)) = left max, so height is left max - height[i]

"""
def trap(height: List[int]) -> int:
    if not height:
        return 0

    n = len(height)
    total_sum, max_left, max_right, left, right = 0, 0, 0, 0, n-1
    while left < right:
        if height[left] < height[right]:
            if height[left] > max_left:
                max_left = height[left]
            else:
                total_sum += max_left - height[left] # remember invariant, we only advance left if its lower than right etc 
            left += 1
        else:
            if height[right] > max_right:
                max_right = height[right]
            else:
                total_sum += max_right - height[right]
            right -= 1
    return total_sum




if __name__ == "__main__":
    cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([4, 2, 0, 3, 2, 5], 9),
        ([0, 0, 0, 0], 0),
        ([3, 0, 3], 3),
        ([5, 4, 3, 2, 1], 0),
        ([1, 2, 3, 4, 5], 0),
        ([1], 0),
        ([2, 2], 0),
        ([0, 2, 0], 0),
        ([2, 0, 2], 2),
        ([5, 0, 0, 0, 5], 15),
    ]

    passed = 0
    for height, expected in cases:
        got = trap(list(height))
        ok = got == expected
        passed += ok
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] trap({height}) = {got}  (expected {expected})")

    print(f"\n{passed}/{len(cases)} passed")
    assert passed == len(cases), "some cases failed"
