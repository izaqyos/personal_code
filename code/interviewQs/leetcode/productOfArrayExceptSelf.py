"""
238. Product of Array Except Self
https://leetcode.com/problems/product-of-array-except-self/

Given an integer array nums, return an array answer such that answer[i]
is equal to the product of all the elements of nums except nums[i].

You must write an algorithm that runs in O(n) time and without using division.

Follow-up: Can you solve it with O(1) extra space? (The output array does not count.)
"""

# ToDo O(1) space

def product_except_self(nums: list[int]) -> list[int]:
    return product_except_self_v2(nums)

def product_except_self_v2(nums: list[int]) -> list[int]:
    #O(1) space
    if not nums:
        return []

    if len(nums) == 1:
        return [1]

    ans = [1 for _ in range(len(nums))] # use ans as suffixes multiplication
    fact = 1
    ind = len(nums)-2
    while ind >= 0:
        fact *= nums[ind+1]
        ans[ind] = fact
        ind -= 1

    pref = 1
    ind = 1
    ans[0] = pref * ans[0]
    while ind < len(nums) :
        pref *= nums[ind-1]
        ans[ind] = ans[ind] * pref
        ind += 1

    return ans

def product_except_self_v1(nums: list[int]) -> list[int]:
    if not nums:
        return []

    if len(nums) == 1:
        return [1]

    pref, suff = [1 for _ in nums] , [1 for _ in nums]

    fact = 1
    ind = 1
    while ind < len(nums) :
        fact *= nums[ind-1]
        pref[ind] = fact
        ind += 1

    fact = 1
    ind = len(nums)-2
    while ind >= 0:
        fact *= nums[ind+1]
        suff[ind] = fact
        ind -= 1

    ans = [ x*y for x,y in zip(pref,suff)]
    return ans

if __name__ == "__main__":
    tests = [
        ([1, 2, 3, 4], [24, 12, 8, 6]),
        ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
        ([0, 0], [0, 0]),
        ([1, 1], [1, 1]),
        ([2, 3, 4, 5], [60, 40, 30, 24]),
    ]
    for i, (nums, expected) in enumerate(tests):
        result = product_except_self(nums)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i+1}: {status} | input={nums} expected={expected} got={result}")
