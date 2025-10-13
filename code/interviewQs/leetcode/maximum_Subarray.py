"""
Given an integer array nums, find the 
subarray
 with the largest sum, and return its sum.
Example 1:

Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.
Example 2:

Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.
Example 3:

Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.
Constraints:

1 <= nums.length <= 105
-104 <= nums[i] <= 104
Follow up: If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.


Intuition of this Problem:
We can solve this problem using Kadane's Algorithm

LETS DRY RUN THIS CODE WITH ONE EXAPMPLE :

Suppose we have the following input vector: [-2, 1, -3, 4, -1, 2, 1, -5, 4].

We initialize the maximumSum = INT_MIN (-2147483648) and currSumSubarray = 0.

We loop through the input vector and perform the following operations:

At the first iteration, currSumSubarray becomes -2 and since it is less than 0, we set it to 0. maximumSum remains at INT_MIN.

At the second iteration, currSumSubarray becomes 1, which is greater than 0, so we keep it as it is. We update maximumSum to 1.

At the third iteration, currSumSubarray becomes -2, which is less than 0, so we set it to 0. maximumSum remains at 1.

At the fourth iteration, currSumSubarray becomes 4, which is greater than 0, so we keep it as it is. We update maximumSum to 4.

At the fifth iteration, currSumSubarray becomes 3, which is greater than 0, so we keep it as it is. maximumSum remains at 4.

At the sixth iteration, currSumSubarray becomes 5, which is greater than 0, so we keep it as it is. We update maximumSum to 5.

At the seventh iteration, currSumSubarray becomes 6, which is greater than 0, so we keep it as it is. We update maximumSum to 6.

At the eighth iteration, currSumSubarray becomes 1, which is greater than 0, so we keep it as it is. maximumSum remains at 6.

At the ninth iteration, currSumSubarray becomes 5, which is greater than 0, so we keep it as it is. maximumSum remains at 6.

After iterating through the input vector, we return maximumSum which is equal to 6. Therefore, the maximum sum subarray of the given input vector is [4, -1, 2, 1], and the sum of this subarray is 6.

Approach for this Problem:
Initialize two variables, maximumSum and currSumSubarray to the minimum integer value (INT_MIN) and 0, respectively.
Loop through the array from index 0 to n-1, where n is the size of the array.
In each iteration, add the current element of the array to the currSumSubarray variable.
Take the maximum between maximumSum and currSumSubarray and store it in the maximumSum variable.
Take the maximum between currSumSubarray and 0 and store it in currSumSubarray. This is done because if the currSumSubarray becomes negative, it means that we should start a new subarray, so we reset currSumSubarray to 0.
After the loop ends, return the maximumSum variable, which contains the maximum sum of a subarray.

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        n = len(nums)
        maximumSum, currSumSubarray = float('-inf'), 0
        for i in range(n):
            currSumSubarray += nums[i]
            maximumSum = max(maximumSum, currSumSubarray)
            currSumSubarray = max(currSumSubarray, 0)
        return maximumSumo

    Time Complexity and Space Complexity:
Time complexity: O(n), where n is the size of the input array. The algorithm has to loop through the array only once.
Space complexity: O(1), since the algorithm is using only a constant amount of extra space regardless of the input size.


divide and conquer java:
class Solution {
    public int maxSubArray(int[] nums) {
        return findMaxSum(nums, 0, nums.length-1);     
    }
    
    private int findMaxSum(int[] nums, int s, int e){
        if(s==e) return nums[s];
        
        int mid = s + (e-s)/2;
        
        int leftMax = findMaxSum(nums, s, mid);
        int rightMax = findMaxSum(nums, mid+1, e);
        int arrMax = findMaxCrossSum(nums, s, mid, e);
      
        
        return Math.max(leftMax, Math.max(rightMax, arrMax));
    }
    
    private int findMaxCrossSum(int []nums, int s, int m, int e){

        int lSum=0, lMax=Integer.MIN_VALUE;
		
        for(int i=m; i>=s; i--){
            lSum+=nums[i];
            lMax = Math.max(lMax, lSum);        
        }
        
        int rSum=0, rMax=Integer.MIN_VALUE;
		
        for(int i=m+1; i<=e; i++){
            rSum+=nums[i];
            rMax = Math.max(rMax, rSum);
        }
        
        return lMax+rMax;
    }
}
"""

