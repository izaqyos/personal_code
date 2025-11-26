class Solution:
    def subsets(self, nums):
        if len(nums) == 0:
            return [[]]

        ret = []
        for i, n in enumerate(nums):
            rest = self.subsets(nums[i+1:])

            #rest = self.subsets(nums[:i]+nums[i+1:])
            for st in rest:
                if not st in ret:
                    ret.append(st)
                stplus = st[:]
                stplus.append(n)
                if not stplus in ret:
                    ret.append(stplus)

        return ret