"""
LC 1 — Two Sum (Easy) — fresh practice run

Given an array of integers `nums` and an integer `target`, return the indices
of the two numbers such that they add up to `target`.

Exactly one solution per input. Cannot use the same element twice.
Return indices in any order.

Aim for O(n) time, O(n) space — one-pass hash map.

Constraints:
    2 <= len(nums) <= 10^4
    -10^9 <= nums[i] <= 10^9
    -10^9 <= target  <= 10^9
    exactly one valid answer exists

Examples:
    [2, 7, 11, 15],       target=9  -> [0, 1]
    [3, 2, 4],            target=6  -> [1, 2]
    [3, 3],               target=6  -> [0, 1]   (same value, different indices)
    [-1, -2, -3, -4, -5], target=-8 -> [2, 4]
    [0, 4, 3, 0],         target=0  -> [0, 3]
    [1, 2, 3, 4, 5],      target=9  -> [3, 4]

Edge cases to think about:
    - duplicate values at different indices ([3, 3])
    - negatives, zeros
    - solution at the very end
    - same element can't be used twice (i ≠ j)
"""
from typing import List


def two_sum(nums: List[int], target: int) -> List[int]:
    wanted: dict[int, int] = dict()
    for i,n in enumerate(nums):
        if n in wanted:
            return [wanted[n], i]
        wanted[target - n] = i

    return [-1, -1]





def _check(got, expected) -> bool:
    """order-insensitive index-pair check"""
    if got is None or len(got) != 2:
        return False
    return sorted(got) == sorted(expected)


if __name__ == "__main__":
    cases = [
        ([2, 7, 11, 15],       9,  [0, 1]),
        ([3, 2, 4],            6,  [1, 2]),
        ([3, 3],               6,  [0, 1]),
        ([-1, -2, -3, -4, -5], -8, [2, 4]),
        ([0, 4, 3, 0],         0,  [0, 3]),
        ([1, 2, 3, 4, 5],      9,  [3, 4]),
        ([5, 75, 25],          100, [1, 2]),
        ([-3, 4, 3, 90],       0,  [0, 2]),
        ([1, 5, 1, 5],         10, [1, 3]),
    ]

    passed = 0
    for nums, target, expected in cases:
        got = two_sum(list(nums), target)
        ok = _check(got, expected)
        passed += ok
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] two_sum({nums}, {target}) = {got}  (expected {expected})")

    print(f"\n{passed}/{len(cases)} passed")
    assert passed == len(cases), "some cases failed"
