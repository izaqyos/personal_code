"""
Given an integer array nums, handle multiple queries of the following types:

Update the value of an element in nums.
Calculate the sum of the elements of nums between indices left and right inclusive where left <= right.
Implement the NumArray class:

NumArray(int[] nums) Initializes the object with the integer array nums.
void update(int index, int val) Updates the value of nums[index] to be val.
int sumRange(int left, int right) Returns the sum of the elements of nums between indices left and right inclusive (i.e. nums[left] + nums[left + 1] + ... + nums[right]).
 

Example 1:

Input
["NumArray", "sumRange", "update", "sumRange"]
[[[1, 3, 5]], [0, 2], [1, 2], [0, 2]]
Output
[null, 9, null, 8]

Explanation
NumArray numArray = new NumArray([1, 3, 5]);
numArray.sumRange(0, 2); // return 1 + 3 + 5 = 9
numArray.update(1, 2);   // nums = [1, 2, 5]
numArray.sumRange(0, 2); // return 1 + 2 + 5 = 8
 

Constraints:

1 <= nums.length <= 3 * 104
-100 <= nums[i] <= 100
0 <= index < nums.length
-100 <= val <= 100
0 <= left <= right < nums.length
At most 3 * 104 calls will be made to update and sumRange.

idea. we can do two alternatives.
a. space O(1). update time O(1). sum time O(n). naive. update element i, sum i-j
b. Space (n). update time  O(n), sum time O(1) . details.
keep array sums. size n. where sums[0] is 0 and sums[i] is sum from 0 to i-1 inclusive. to Calculate sum [i,j] where i<=j so sum[j]-sums[i-1] (that's why we add sums[0] as 0)
so sum[1,1] is sums[1] ( == nums[0]) - 0
so sum[1,2] is sums[2] - sums[1] ( == nums[0] + nums[1] - nums[0]) == nums[1]
etc
"""

"""
option a
TLE as expected
"""
class NumArray1:

    def __init__(self, nums: List[int]):
        self.nums = [_ for _ in nums] #shallow copy


    def update(self, index: int, val: int) -> None:
        self.nums[index] = val


    def sumRange(self, left: int, right: int) -> int:
        return sum(self.nums[left:right+1])



# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# obj.update(index,val)
# param_2 = obj.sumRange(left,right)
"""
option b, also TLE. apperantly the operations need to be O(logn) complexity. 
This can be acheived using a Binary Index Tree (BIT)
"""
class NumArray2:

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

"""
option C. using BITTree
"""
class BITree:
    def __init__(self, numbers):
        self.numbers = [_ for _ in numbers] #make a copy
        self.size = len(numbers)
        self.bit = [0 for _ in range(self.size+1)] #0 index is dummy
        self.construct()

    def construct(self):
        #o(nlogn)
        for i,n in enumerate(self.numbers): 
            #print(f"updating value {n} at index {i} in BIT")
            self.updateSum(i,n) #o(logn)


    def updateValue(self, index, value):
        addedSumToBIT = value-self.numbers[index]
        self.numbers[index] = value
        #print(f"updating value {addedSumToBIT} at original index {index} in BIT")
        self.updateSum(index, addedSumToBIT)

    def updateSum(self, index, value):
        index+=1
        while index<=self.size:
            #print(f"updating sum at index {index} adding value {value}")
            self.bit[index]+=value
            index +=index&(-index) #bitwise operation n&-n leaves last set bit, add it to index to get it's parent in bittree 

    def getSumPrefix(self, right):
        retsum , index = 0, right+1
        while (index>0):
            retsum += self.bit[index]
            index -= index&(-index) #travel to parents in sum view of bittree by removing last set bit. idea is each node in bit keeps sum of certain range corressponding to a power of 2  representation of the index.
            #say index 11=8+2+1 so in node 11 is last value in this range, in node 10 last 2 sum and node 8 first eight values sum
        #print(f"sum in range 0 to {right} is retsum")
        return retsum

    def getSum(self, left, right):
        return self.getSumPrefix(right) - self.getSumPrefix(left-1)

    def printMe(self):
        print("indices row and numbers row are")
        for i in range(self.size):
            print(f"{i:<3d}", end='')
        print('')
        for n in self.numbers:
            print(f"{n:<3d}", end='')
        print('')

        print("BITree node indices and values rows are")
        for i in range(self.size + 1):
            print(f"{i:<3d}", end='')
        print('')
        for n in self.bit:
            print(f"{n:<3d}", end='')
        print('')

class NumArray:

    def __init__(self, nums: List[int]):
        self.bittree = BITree(nums)

    def update(self, index: int, val: int) -> None:
        self.bittree.updateValue(index, val)


    def sumRange(self, left: int, right: int) -> int:
        return self.bittree.getSum(left, right)

