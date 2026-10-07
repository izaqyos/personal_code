"""
LC 53 — Maximum Subarray (Medium)

Given an integer array nums, find the subarray with the largest sum, and return its sum.
A subarray is a contiguous non-empty sequence of elements within an array.

Example 1:
    Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
    Output: 6
    Explanation: The subarray [4,-1,2,1] has the largest sum 6.

Example 2:
    Input: nums = [1]
    Output: 1

Example 3:
    Input: nums = [5,4,-1,7,8]
    Output: 23

Constraints:
    1 <= nums.length <= 10^5
    -10^4 <= nums[i] <= 10^4

Follow up: if you have the O(n) solution, try divide and conquer (more subtle).
"""


def max_sub_array(nums: list[int]) -> int:
    running_sum = 0
    max_sum = nums[0]
    for num in nums:
        running_sum += num
        max_sum = max(max_sum, running_sum)
        running_sum = max(running_sum, 0)
    return max_sum


if __name__ == "__main__":
    tests = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([1], 1),
        ([5, 4, -1, 7, 8], 23),
        ([-3, -1, -2], -1),
        ([-5], -5),
        ([2, -1, 2], 3),
        ([0, 0, 0], 0),
        ([-1, 3, -1, -1, 4], 5),
    ]
    for i, (nums, expected) in enumerate(tests):
        got = max_sub_array(nums)
        assert got == expected, f"test {i}: max_sub_array({nums}) = {got}, expected {expected}"
    print(f"All {len(tests)} tests passed.")
