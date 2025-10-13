#!/opt/homebrew/bin/python3
from typing import List

"""
Minimum Number of Operations to Make Array Empty
You are given a 0-indexed array nums consisting of positive integers.

There are two types of operations that you can apply on the array any number of times:

Choose two elements with equal values and delete them from the array.
Choose three elements with equal values and delete them from the array.
Return the minimum number of operations required to make the array empty, or -1 if it is not possible.

 

Example 1:

Input: nums = [2,3,3,2,2,4,2,3,4]
Output: 4
Explanation: We can apply the following operations to make the array empty:
- Apply the first operation on the elements at indices 0 and 3. The resulting array is nums = [3,3,2,4,2,3,4].
- Apply the first operation on the elements at indices 2 and 4. The resulting array is nums = [3,3,4,3,4].
- Apply the second operation on the elements at indices 0, 1, and 3. The resulting array is nums = [4,4].
- Apply the first operation on the elements at indices 0 and 1. The resulting array is nums = [].
It can be shown that we cannot make the array empty in less than 4 operations.
Example 2:

Input: nums = [2,1,2,2,3,3]
Output: -1
Explanation: It is impossible to empty the array.
 

Constraints:

2 <= nums.length <= 105
1 <= nums[i] <= 106

strategy:
a. get frequencies of each array number
b. if frequency of one number is 1 return -1
c. set minops = infinity
d. for each number in array run helper(num_freq, ops) a recursive function that returns the min number of ops
e. return sum of helper mins 

helper(num_freq):
    if num_freq == 1:
        return infinity
    if num_freq == 2 or num_freq == 3:
        return 1

    if num_freq%3 == 0:
        return num_freq//3
    elif  num_freq%3 == 1: #mod 3 is 1 so substract 2 times get us a number that its mod 3 is 2, so substract 2 again we get the mod 3 0
        return 2 + (num_freq-4)//3
    else: #mod3 is 2, substract 2 times to get to mod 3 == 0
        return 1 + (num_freq-2)//3

    #else:
    #    if num_freq == 2 or num_freq == 3:
    #        return 1
    #else:
    #    return min(helper(num_freq-2), helper(num_freq-3))
"""
from collections import Counter
class Solution:
    def helper(self, num_freq):
        if num_freq == 1:
            return -1
            #return float('-inf')
        if num_freq == 2 or num_freq == 3:
            return 1

        if num_freq%3 == 0:
            return num_freq//3 
        elif num_freq%3==1:
            return 2 + (num_freq -4)//3
        else: 
            return 1 + (num_freq)//3

    def minOperations(self, nums: List[int]) -> int:
        nums_freq = Counter(nums)
        total_min = 0
        for v in nums_freq.values():
            cmin = self.helper(v)
            if cmin == -1:
                return -1
            else:
                total_min += cmin
        return total_min

       

def test():
    inputs= [
            [1,2],
            [2,2],
            [3,3,3],
            [2,1,2,2,3,3],
            [2,3,3,2,2,4,2,3,4],
            [14,12,14,14,12,14,14,12,12,12,12,14,14,12,14,14,14,12,12],
            ]
    expected = [
            -1,
            1,
            1,
            -1,
            4,
            7
            ]
    sol  = Solution()
    for inp,exp in zip(inputs, expected):
        res = sol.minOperations(inp)
        print(f"solving for {inp}, got result {res}, expected result {exp}")
        assert res == exp


def main():
    test()

if __name__ == "__main__":
    main()
