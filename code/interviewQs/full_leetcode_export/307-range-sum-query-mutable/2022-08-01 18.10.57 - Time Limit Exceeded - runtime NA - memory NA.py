class NumArray:

    def __init__(self, nums: List[int]):
        self.nums = [_ for _ in nums] #shallow copy


    def update(self, index: int, val: int) -> None:
        self.nums[index] = val


    def sumRange(self, left: int, right: int) -> int:
        return sum(self.nums[left:right+1])
