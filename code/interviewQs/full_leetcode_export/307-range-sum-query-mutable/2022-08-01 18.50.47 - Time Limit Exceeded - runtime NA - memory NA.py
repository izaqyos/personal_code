
# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# obj.update(index,val)
# param_2 = obj.sumRange(left,right)
"""
option b
"""
class NumArray:

    def __init__(self, nums: List[int]):
        self.nums = [_ for _ in nums] #shallow copy
        self.sums = [0] #sums indices start from 1 to n+1, 0 element is added to make solution simpler 
        prevSum = 0
        for i in range(len(nums)):
            self.sums.append(prevSum + nums[i] )
            prevSum = self.sums[-1]
        #print(self.nums)
        #print(self.sums)


    def update(self, index: int, val: int) -> None:
        self.nums[index] = val
        prevSum = self.sums[index]
        for i in range(index+1, len(self.nums)+1):
            self.sums[i] = prevSum + self.nums[i-1]
            prevSum = self.sums[i]
        #print(f"updated index {index}, val {val}")
        #print(self.nums)
        #print(self.sums)


    def sumRange(self, left: int, right: int) -> int:
        #print(f"sumrange from left {left}, to right {right}")
        #print(self.nums)
        #print(self.sums)
        return self.sums[right+1] - self.sums[left]
