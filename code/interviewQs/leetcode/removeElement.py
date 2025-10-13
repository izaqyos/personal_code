from typing import List

"""
Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. The order of the elements may be changed. Then return the number of elements in nums which are not equal to val.

Consider the number of elements in nums which are not equal to val be k, to get accepted, you need to do the following things:

Change the array nums such that the first k elements of nums contain the elements which are not equal to val. The remaining elements of nums are not important as well as the size of nums.
Return k.
Custom Judge:

The judge will test your solution with the following code:

int[] nums = [...]; // Input array
int val = ...; // Value to remove
int[] expectedNums = [...]; // The expected answer with correct length.
                            // It is sorted with no values equaling val.

int k = removeElement(nums, val); // Calls your implementation

assert k == expectedNums.length;
sort(nums, 0, k); // Sort the first k elements of nums
for (int i = 0; i < actualLength; i++) {
    assert nums[i] == expectedNums[i];
}
If all assertions pass, then your solution will be accepted.

 

Example 1:

Input: nums = [3,2,2,3], val = 3
Output: 2, nums = [2,2,_,_]
Explanation: Your function should return k = 2, with the first two elements of nums being 2.
It does not matter what you leave beyond the returned k (hence they are underscores).
Example 2:

Input: nums = [0,1,2,2,3,0,4,2], val = 2
Output: 5, nums = [0,1,4,0,3,_,_,_]
Explanation: Your function should return k = 5, with the first five elements of nums containing 0, 0, 1, 3, and 4.
Note that the five elements can be returned in any order.
It does not matter what you leave beyond the returned k (hence they are underscores).
 

Constraints:

0 <= nums.length <= 100
0 <= nums[i] <= 50
0 <= val <= 100
"""


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        """
        idea, iterate over nums and if nums[i] == val, swap it with nums[n-1] and reduce n by 1 
        also return number of elements not equal to val
        """
        n = len(nums)
        i = 0
        while i < n:
            print(f"i = {i}, n = {n}, nums = {nums}")
            if nums[i] == val:
                print(f"swapping {nums[i]} with {nums[n-1]}")
                while n > i and nums[n-1] == val:
                    print(f"found val on right most side {nums[n-1]}")
                    n -= 1
                if n > i:
                    nums[i] = nums[n-1]
                    n -= 1
            i += 1
        print(f"returning n = {n}, nums = {nums[:n]}")
        return n

# write tests for removeElement() method,
# firt test case Input: nums = [3,2,2,3], val = 3
# Output: 2, nums = [2,2,_,_]


class Solution2:
    """
    resolve 24.04.25
    """
    def removeElement(self, nums: List[int], val: int) -> int:
        pass

def test1():
    nums = [3, 2, 2, 3]
    val = 3
    expected = 2
    assert Solution().removeElement(nums, val) == expected
    assert nums[:expected] == [2, 2]

# second test case Input: nums = [0,1,2,2,3,0,4,2], val = 2
# Output: 5, nums = [0,1,4,0,3,_,_,_]
def test2():
    nums = [0, 1, 2, 2, 3, 0, 4, 2]
    val = 2
    expected = 5
    assert Solution().removeElement(nums, val) == expected
    assert nums[:expected] == [0, 1, 4, 0, 3]

# 3rd test nums = [3,3] val = 3, expected = 0, []
def test3():
    nums = [3, 3]
    val = 3
    expected = 0
    assert Solution().removeElement(nums, val) == expected
    assert nums[:expected] == []

def failtest():
    assert False

def main():
    test1()
    test2()
    test3()
    #failtest()

if __name__ == "__main__":
    main()

