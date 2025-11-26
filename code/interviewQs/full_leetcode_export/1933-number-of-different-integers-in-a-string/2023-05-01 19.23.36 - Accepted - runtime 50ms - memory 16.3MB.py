
class Solution:
    def numDifferentIntegers(self, word: str) -> int:
        if not word:
            return 0

        nums = set()
        num = ""
        for w in word:
            if w.islower() :
                if num:
                    nums.add(int(num))
                    num = ""
            else:
                num +=w
        if num:
            nums.add(int(num))
        return len(nums)
