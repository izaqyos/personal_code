class Solution:
    def combineR(self, nums, k):
        n = len(nums)
        if n == k:
            return [nums]
        if k == 1:
            return [[i] for i in nums]

        final = []
        for i in range(len(nums) - k + 1):
            rest = self.combineR(nums[i+1:], k-1)
            for lst in rest:
                lst.append(nums[i])
                final.append(lst)

        return final

    def combine(self, n: int, k: int):
        if k == 0:
            return [[]]

        if  n == 0 or n < k:
            return []

        nlist = [i+1 for i in range(n)]
        return self.combineR(nlist, k)