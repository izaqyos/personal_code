"""
347. Top K Frequent Elements
https://leetcode.com/problems/top-k-frequent-elements/

Given an integer array nums and an integer k, return the k most frequent elements.
You may return the answer in any order.

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- k is in the range [1, the number of unique elements in the array]
- It is guaranteed that the answer is unique.

Follow up: Your algorithm's time complexity must be better than O(n log n).

Example 1: nums = [1,1,1,2,2,3], k = 2 -> [1,2]
Example 2: nums = [1], k = 1 -> [1]
"""


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    pass


if __name__ == "__main__":
    tests = [
        ([1, 1, 1, 2, 2, 3], 2, [1, 2]),
        ([1], 1, [1]),
        ([1, 2], 2, [1, 2]),                        # k == unique count
        ([3, 3, 3, 1, 1, 2], 1, [3]),               # single most frequent
        ([1, 1, 2, 2, 3, 3], 3, [1, 2, 3]),         # all same frequency
        ([-1, -1, -1, 2, 2], 1, [-1]),              # negatives
        ([4, 4, 4, 4, 1, 2, 3], 2, [4, 1]),         # one dominant element
        ([1, 2, 3, 4, 5, 5, 5, 5], 3, [5, 1, 2]),   # k=3, ties broken arbitrarily
    ]
    for i, (nums, k, expected) in enumerate(tests):
        result = top_k_frequent(nums, k)
        status = "PASS" if sorted(result) == sorted(expected) else "FAIL"
        print(f"Test {i+1}: {status} | nums={nums}, k={k}, expected={expected}, got={result}")
