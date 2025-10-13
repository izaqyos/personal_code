"""
A peak element is an element that is strictly greater than its neighbors.

Given an integer array nums, find a peak element, and return its index. If the array contains multiple peaks, return the index to any of the peaks.

You may imagine that nums[-1] = nums[n] = -∞.

You must write an algorithm that runs in O(log n) time.

 

Example 1:

Input: nums = [1,2,3,1]
Output: 2
Explanation: 3 is a peak element and your function should return the index number 2.
Example 2:

Input: nums = [1,2,1,3,5,6,4]
Output: 5
Explanation: Your function can return either index number 1 where the peak element is 2, or index number 5 where the peak element is 6.
 

Constraints:

1 <= nums.length <= 1000
-231 <= nums[i] <= 231 - 1
nums[i] != nums[i + 1] for all valid i.
"""

class Solution:
    def islocalpeak(self, nums, i):
        if len(nums) == 1:
            return True
        if i==0 and nums[i+1]<nums[i]:
            return True
        if (i==len(nums)-1) and nums[i-1]<nums[i]:
            return True
        if nums[i+1]<nums[i] and nums[i-1]<nums[i]:
            return True

    def findPeakElement(self, nums: List[int]) -> int:
        """ binary search. decide upper or lower part of array according to > test. if 
        high end of lower part is greater than middle go left
        high end of higher part is greater than middle go right
        if middle is greater than both then we've found a peak. return it
        """
        l,h = 0, len(nums)-1
        while l<=h:
            m = (h+l)//2
            if self.islocalpeak(nums,m):
                return m
            elif (m>0) and nums[m-1]>nums[m]:
                h=m
            elif (m<len(nums)-1) and nums[m+1]>nums[m]:
                l=m+1
