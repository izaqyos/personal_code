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
            return 2 + (num_freq -4)//2
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
