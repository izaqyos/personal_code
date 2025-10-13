"""
416. Partition Equal Subset Sum
Given a non-empty array nums containing only positive integers, find if the array can be partitioned into two subsets such that the sum of elements in both subsets is equal.



Example 1:

Input: nums = [1,5,11,5]
Output: true
Explanation: The array can be partitioned as [1, 5, 5] and [11].
Example 2:

Input: nums = [1,2,3,5]
Output: false
Explanation: The array cannot be partitioned into equal sum subsets.


Constraints:

1 <= nums.length <= 200
1 <= nums[i] <= 100
Todo:
    implement: brute force recursion, DP n*n and n space, last bitset.
    see <url:/Users/I500695/work/code/interviewQs/leetcode/partitionEqualSubsetSumSolutionExplained>
"""
class Solution:
    def canPartitionRecursive(self, nums: List[int]) -> bool:
        """
        if sum(nums)%2 == 1 then return False (no way to partition)
        else, j
        """
        import functools
        sumall = functools.reduce(lambda a,b: a+b, nums) 
        if sumall %2 !=0:
            return False
        return self.dfs(nums, sumall/2, 0) #True if there's a subset of nums whose sum is half total sum

    def dfs(self, nums, sumr, i):
        if sumr == 0:
            return True

        if i == len(nums) or sumr < 0:
            return False

        return self.dfs(nums, sumr-nums[i], i+1) or self.dfs(nums, sumr, i+1)

    def canPartitionDP2Dim(self, nums: List[int]) -> bool:
        """
        if sum(nums)%2 == 1 then return False (no way to partition) O(n)
        else, build bool matrix dp, dimenstions: nX(sum(n)/2)
        where dp[i][j] means that elements 0-i contain subset whose sum is j
        dp[n][sum(n)/2] is True means we can partition 
        """
        import functools
        sumall = functools.reduce(lambda a,b: a+b, nums) 
        if sumall %2 !=0:
            return False
        dp=[[False for _ in range(sumall//2+1)] for _ in range(len(nums)+1)]
        #print(f"created dp[{len(dp)}][{len(dp[0])}]")

        for i in range(len(nums)+1):
            dp[i][0] = True #can always find subset whose sum is 0 - the empty set
            
        for i in range(1,len(nums)+1): #we can skip i==0 (no elements), dp[0][j] where j>0 is always False and dp is initialised to False so we can skip
            for j in range(1, sumall//2+1):
                if nums[i-1] > j: #we can use ith elem to get sum j since its bigger than sum
                    dp[i][j] = dp[i-1][j]
                else: #recursion condition like: return self.dfs(nums, sumr-nums[i], i+1) or self.dfs(nums, sumr, i+1)
                    dp[i][j] = dp[i-1][j] or dp[i-1][j-nums[i-1]]
                
        return dp[len(nums)][sumall//2]


    def canPartitionDP1Dim(self, nums: List[int]) -> bool:
        """
        if sum(nums)%2 == 1 then return False (no way to partition) O(n)
        else, build array of length sumall//2+1, where dp[j] is True iff nums contain subset whose sum is j
        """
        import functools
        sumall = functools.reduce(lambda a,b: a+b, nums) 
        if sumall %2 !=0:
            return False
        dp=[False for _ in range(sumall//2+1)] 
        dp[0] = True #take empty set to get 0 sum
        for n in nums:
            for j in range(sumall//2,n-1,-1):
                if (n == j) or dp[j-n] == True:
                    dp[j] = True
        return dp[len(nums)][sumall//2]

    def canPartitionDPBitSet(self, nums: List[int]) -> bool:
        """
        if sum(nums)%2 == 1 then return False (no way to partition) O(n)
        else, build bit array of length sumall//2+1, where dp[j] is 1 iff nums contain subset whose sum is j
        Ex:
            When num=2, bits=101, which represents nums can sum to 0 and 2
When num=3, bits=101101, which represents nums can sum to 0, 2, 3, 5
When num=5, bits=10110101101, which represents nums can sum to 0, 2, 3, 5, 7, 8, 10
Finally, we just need to check if bits[5] is 0 or 1.

        """
        import functools
        sumall = functools.reduce(lambda a,b: a+b, nums) 
        if sumall %2 !=0:
            return False
        dp=[False for _ in range(sumall//2+1)] 
        dp[0] = True #take empty set to get 0 sum
        for n in nums:
            for j in range(sumall//2,n-1,-1):
                if (n == j) or dp[j-n] == True:
                    dp[j] = True
        return dp[len(nums)][sumall//2]

