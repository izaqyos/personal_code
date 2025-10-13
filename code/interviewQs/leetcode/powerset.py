"""
Given a set of distinct integers, nums, return all possible subsets (the power set).

Note: The solution set must not contain duplicate subsets.

Example:

Input: nums = [1,2,3]
Output:
[
  [3],
  [1],
  [2],
  [1,2,3],
  [1,3],
  [2,3],
  [1,2],
  []
]
"""


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


def test():
    inputs = [[], [1], [1, 2], [1, 2, 3, 4]]
    expected = [ [[]], [[], [1]], [[], [1], [2], [1, 2]],
                [[], [1], [2], [2, 1], [3], [3, 1], [3, 2], [3, 2, 1], [4], [4, 1], [4, 2], [4, 2, 1], [4, 3], [4, 3, 1], [4, 3, 2], [4, 3, 2, 1]]]
    sol = Solution()
    for inp, exp in zip(inputs, expected):
        pset = sol.subsets(inp)
        print('power set of {} is {}, expected={}'.format(inp, pset, exp))


if __name__ == '__main__':
    test()
