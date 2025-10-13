"""
Given an integer array nums, you need to find one continuous subarray that if you only sort this subarray in ascending order, then the whole array will be sorted in ascending order.

Return the shortest such subarray and output its length.

 

Example 1:

Input: nums = [2,6,4,8,10,9,15]
Output: 5
Explanation: You need to sort [6, 4, 8, 10, 9] in ascending order to make the whole array sorted in ascending order.
Example 2:

Input: nums = [1,2,3,4]
Output: 0
Example 3:

Input: nums = [1]
Output: 0
 

Constraints:

1 <= nums.length <= 104
-105 <= nums[i] <= 105
 

Follow up: Can you solve it in O(n) time complexity?
"""

#class Solution:
    #def findUnsortedSubarray(self, nums: List[int]) -> int:
    #    #naive o(nlogn) solution
    #    ns = sorted(nums)
    #    i =0
    #    while i<len(nums) and ns[i] == nums[i]:
    #        i+=1
    #    j=len(nums)-1
    #    while  j>0 and ns[j] == nums[j]:
    #        j-=1
    #    if j>i:
    #        return j-i+1
    #    else:
    #        return 0


class Solution:
    def findUnsortedSubarray(self, nums: List[int]) -> int:
        """
algo:
    use left and right pointers to scan from left to right and right to left respectively.
    first find unsorted subarray candidate. how?
    1. scan left to right stop at first element > then next (breaking sorted cond of <=)
    2. scan right to left stop at first element < then next (breaking sorted cond of >= when going right to left)
    3. then search in 2 sorted arrays at start and end for possible additions to candidate unsorded arrray.  how?
    4. scan unsorded array to deduct min and max
    5. for start (0,l-1) check for first element > min , set l to its index 
    6. for end (r+1,len(n)-1) check for first element < max , set r to its index 
    return r-l+1
        """
        left =  0
        right = len(nums)-1
        min_num = float('inf')
        max_num = float('-inf')
        n = len(nums)
        
        #1
        while left < n-1:
            if nums[left] > nums[left+1]:
                break
            left +=1

        #2
        while right > 0:
            if nums[right] < nums[right-1]:
                break
            right -=1

        #print(left, right)
        if left>=right:
            return 0

        #3, 4
        for i in range(left, right+1):
            num = nums[i]
            if num<min_num:
                min_num = num
            if num>max_num:
                max_num = num
        #print(f"unsorted subarray candidate min=${min_num}, max={max_num}")
        #5
        for i in range(0, left):
            if nums[i]>min_num:
                left=i
                break
        #6
        
        for i in range(n-1, right, -1):
            #print(f"n[{i}]={nums[i]}")
            if nums[i]<max_num:
                right=i
                break
                
        #print(left, right)
        return right-left+1

