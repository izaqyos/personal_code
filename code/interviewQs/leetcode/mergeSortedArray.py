"""
88. Merge Sorted Array
https://leetcode.com/problems/merge-sorted-array/

You are given two integer arrays nums1 and nums2, sorted in non-decreasing order,
and two integers m and n, representing the number of elements in nums1 and nums2
respectively.

Merge nums2 into nums1 as one sorted array. The final sorted array should be
stored inside nums1 (which has length m + n, with the last n elements set to 0).

Do not return anything, modify nums1 in-place instead.

Constraints:
- nums1.length == m + n
- nums2.length == n
- 0 <= m, n <= 200
- 1 <= m + n <= 200
- -10^9 <= nums1[i], nums2[j] <= 10^9

Follow up: Can you come up with an algorithm that runs in O(m + n) time?

Example 1: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3 -> [1,2,2,3,5,6]
Example 2: nums1 = [1], m = 1, nums2 = [], n = 0 -> [1]
Example 3: nums1 = [0], m = 0, nums2 = [1], n = 1 -> [1]
"""


def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    n = len(nums2)
    m = len(nums1) - n
    nums1_idx, nums2_idx, res_idx = m-1, n-1, m+n-1

    while nums1_idx > -1 and nums2_idx > -1:
        if nums1[nums1_idx] > nums2[nums2_idx]:
            nums1[res_idx] = nums1[nums1_idx]
            nums1_idx -= 1
        else:
            nums1[res_idx] = nums2[nums2_idx]
            nums2_idx -= 1
        res_idx -= 1

    while nums2_idx > -1:
        nums1[res_idx] = nums2[nums2_idx]
        nums2_idx -= 1
        res_idx -= 1
    
    while nums1_idx > -1:
        nums1[res_idx] = nums1[nums1_idx]
        nums1_idx -= 1
        res_idx -= 1
    
        



if __name__ == "__main__":
    tests = [
        ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3, [1, 2, 2, 3, 5, 6]),
        ([1], 1, [], 0, [1]),
        ([0], 0, [1], 1, [1]),
        ([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3, [1, 2, 3, 4, 5, 6]),  # nums2 all smaller
        ([1, 2, 3, 0, 0, 0], 3, [4, 5, 6], 3, [1, 2, 3, 4, 5, 6]),  # nums2 all larger
        ([1, 3, 5, 0, 0], 3, [2, 4], 2, [1, 2, 3, 4, 5]),           # interleaved
        ([0, 0, 0], 0, [1, 2, 3], 3, [1, 2, 3]),                     # nums1 empty
        ([-3, -1, 0, 0, 0, 0], 3, [-2, 1, 2], 3, [-3, -2, -1, 0, 1, 2]),  # negatives
    ]
    for i, (nums1, m, nums2, n, expected) in enumerate(tests):
        merge(nums1, m, nums2, n)
        status = "PASS" if nums1 == expected else "FAIL"
        print(f"Test {i+1}: {status} | result={nums1}, expected={expected}")
