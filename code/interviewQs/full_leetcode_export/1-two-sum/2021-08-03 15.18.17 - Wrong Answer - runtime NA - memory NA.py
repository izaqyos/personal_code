class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        compl=dict()
        for i,el in enumerate(nums):
            if not el in compl:
                compl[el] = i
            if (target -el) in compl:
                return [compl[target-el], i]