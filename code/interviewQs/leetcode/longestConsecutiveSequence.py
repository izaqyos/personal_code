"""
128. Longest Consecutive Sequence
https://leetcode.com/problems/longest-consecutive-sequence/

Given an unsorted array of integers nums, return the length of the longest
consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Constraints:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9

Example 1: nums = [100,4,200,1,3,2]   -> 4  (sequence: [1,2,3,4])
Example 2: nums = [0,3,7,2,5,8,4,6,0,1] -> 9  (sequence: [0,1,2,3,4,5,6,7,8])
"""


def longest_consecutive(nums: list[int]) -> int:
    if not nums:
        return 0
    if len(nums) == 1:
        return 1

    seen = set[int]() # O(n) space complexity
    global_lcs, local_lcs = 1 , 1
    for n in nums:
        seen.add(n)
    
    for n in seen:
        if n-1 not in seen:
            local_lcs = 1
            while n+1 in seen:
                local_lcs +=1
                n += 1
            global_lcs = max(global_lcs, local_lcs)

    return global_lcs



if __name__ == "__main__":
    tests = [
        ([100, 4, 200, 1, 3, 2], 4),
        ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
        ([], 0),                          # empty
        ([1], 1),                         # single element
        ([1, 2, 3, 4, 5], 5),            # already consecutive
        ([5, 4, 3, 2, 1], 5),            # reverse order
        ([1, 3, 5, 7], 1),               # no consecutive pairs
        ([1, 2, 2, 3], 3),               # duplicates in sequence
        ([-3, -2, -1, 0, 1], 5),         # negatives into positives
        ([10, 5, 6, 7, 100, 8, 9], 6),   # sequence in the middle: [5,6,7,8,9,10]
    ]
    for i, (nums, expected) in enumerate(tests):
        result = longest_consecutive(nums)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i+1}: {status} | nums={nums}, expected={expected}, got={result}")
