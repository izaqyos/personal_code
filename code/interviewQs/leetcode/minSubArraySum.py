#!/opt/homebrew/bin/python3
from typing import List

"""
Minimum Size Subarray Sum
Given an array of positive integers nums and a positive integer target, return the minimal length of a
subarray
 whose sum is greater than or equal to target. If there is no such subarray, return 0 instead.



Example 1:

Input: target = 7, nums = [2,3,1,2,4,3]
Output: 2
Explanation: The subarray [4,3] has the minimal length under the problem constraint.
Example 2:

Input: target = 4, nums = [1,4,4]
Output: 1
Example 3:

Input: target = 11, nums = [1,1,1,1,1,1,1,1]
Output: 0


Constraints:

1 <= target <= 109
1 <= nums.length <= 105
1 <= nums[i] <= 104
"""

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        """
        first Solution sliding window
        """
        if not nums:
            return 0
        if len(nums) == 1:
            if nums[0] >= target:
                return 1
            else:
                return 0

        l,r=0,0
        window_sum = nums[0]
        min_len = float('inf')
        while l<=r and r< len(nums):
            #print(f"l={l}, r={r}, window_sum={window_sum}, target={target}, min_len={min_len}, nums={nums}")
            if window_sum >= target:
                min_len = min(r-l+1, min_len)
                l = l+1
                window_sum = window_sum - nums[l-1]
            else:
                r=r+1
                if r< len(nums):
                    if nums[r] >= target:
                        return 1
                    else:
                        window_sum += nums[r]
        if min_len< float('inf'):
            return min_len
        else:
            return 0


def test():
    """
    """
    inputs = (
            (7, [2,3,1,2,4,3]),
            (4, [1,4,4]),
            (11, [1,1,1,1,1,1,1,1])
            )
    sol = Solution()
    for inp in inputs:
        t, nums = inp
        minlen = sol.minSubArrayLen(t, nums)
        print(f"for target {t} and nums {nums} the minimum length subarray whose sum is geq is {minlen}")



def main():
    test()

if __name__ == "__main__":
    main()
