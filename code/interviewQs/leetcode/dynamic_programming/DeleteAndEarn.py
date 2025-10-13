"""
Delete and Earn
You are given an integer array nums. You want to maximize the number of points you get by performing the following operation any number of times:

Pick any nums[i] and delete it to earn nums[i] points. Afterwards, you must delete every element equal to nums[i] - 1 and every element equal to nums[i] + 1.
Return the maximum number of points you can earn by applying the above operation some number of times.

Example 1:

Input: nums = [3,4,2]
Output: 6
Explanation: You can perform the following operations:
- Delete 4 to earn 4 points. Consequently, 3 is also deleted. nums = [2].
- Delete 2 to earn 2 points. nums = [].
You earn a total of 6 points.
Example 2:

Input: nums = [2,2,3,3,3,4]
Output: 9
Explanation: You can perform the following operations:
- Delete a 3 to earn 3 points. All 2's and 4's are also deleted. nums = [3,3].
- Delete a 3 again to earn 3 points. nums = [3].
- Delete a 3 once more to earn 3 points. nums = [].
You earn a total of 9 points.

Constraints:
1 <= nums.length <= 2 * 10^4
1 <= nums[i] <= 104
"""

"""
C. further improve.
note Constraints:
1 <= nums.length <= 2 * 10^4
1 <= nums[i] <= 104
since actual values are in range [1,104] we can create an array of length 105. where val[i] is number of times i is in nums so i*n 
so first scan O(n)
then it's 1:1 house robber
"""
class Solution:
    def rob(self, nums: List[int]) -> int:
        h = nums
        n = len(h)
        if not h:
            return 0
        elif n == 1:
            return h[0]
        elif n == 2:
            return max(h[0],h[1])
        dp = [0 for _ in range(len(h)+1)]
        dp[n-1] = h[n-1]
        dp[n-2] = max(h[n-2], h[n-1])
        for i in range(n-3, -1, -1):
            dp[i] = max(h[i]+dp[i+2], h[i+1]+dp[i+3])
        return dp[0]

    def deleteAndEarn(self, nums: List[int]) -> int:
        vals = [0 for _ in range(10**4 +1)]
        for n in nums:
            vals[n]+=n
        return self.rob(vals)

"""
B. improve - find similarities to house robber problem
instead of going brute force recursion lets change this problem so that house robber solution can be applied to it.
how?
First, recall house robber. <url:/Users/i500695/work/code/interviewQs/leetcode/dynamic_programming/houseRobber.py>
House Robber
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.
Example 1:

Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.

we can sort the array and generate another list as follows
sort(nums)
gains = []
i=0
while i<len(nums):
    if len(gains) == 0 or (i == 0) or gains[i-1] == nums[i]-1
        gains.append(nums[i]) #we want gains[i-1] to be "adjacent" to gains[i+1] since nums[i] == nums[i-1]+1
    else: #plant a separator since we don't want gains[i], gains[i-1] to be considered adjacent
        gains.append(0)
    while i+1<len(nums) and nums[i] == nums[i+1]:
        gains[-1]+=nums[i]
        i+=1
    i+=1
basically if number repeates the gain is num*repeates
then we can run house robber solution on gains 

"""

"""
A. First thoughts.
Note. recursion is getting complex, also dict of lists not possible so got a tip for a better way to solve.
Strategy. First formulate the recursion equation.
So R(nums) is 
Stop conditions: 
    if len(nums) == 0 return max_p
in general.
max_p = float('-inf')
R(nums) = 
    for i in range(len(nums)):
        p = nums[i]
        new_nums = Erase(nums, nums[i])
        max_p = max(max_p, p+R(new_nums))
Erase removes from nums all elements equal to p-1 or p+1

I'll use memorization technique
memo = dict()
memo[[]] = 0
memo[[i]] = i
then:
R(nums) = 
    max_p = 0
    if nums in memo return memo[nums]
    for i in range(len(nums)):
        p = nums[i]
        new_nums = Erase(nums, nums[i])
        max_p = max(max_p, p+R(new_nums))

class Solution:
    def __init__(self):
        self.memo = dict()

    def erase(self, nums, n):
    def helper(self, nums):
        if nums in self.memo:
            return self.memo[nums]

        max_p = 0
        for n in nums:
            new_nums = nums[:]
            self.erase(new_nums,n) 
            max_p = max(max_p, n+self.helper(new_nums))
        self.memo[nums] = max_p    
        return max_p
        
        
    def deleteAndEarn(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        self.mem[[]] = 0
        for n in nums:
            self.memo[[n]] = n
        return self.helper(nums)
"""

