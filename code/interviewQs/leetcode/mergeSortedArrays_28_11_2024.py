from typing import List

class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        """
        do not return anything, modify nums1 in-place instead.

        first pass shift all nums1 n to the right (make room for nums2)
        next pass move over both nums1 and nums2
        if nums1[i] < nums2[j] then move nums1[i] to the right most 0 cell and move pointer to right most 0 by 1
        else write nums2[j]  to the right most 0 cell and move pointer to right most 0 by 1
        """

        i = m-1
        while i >= 0:
            nums1[n+i] = nums1[i]
            i -= 1
        i,j, l = 0, 0, 0 # pointers to nums1, nums2 and left most free spot in nums1 
        #Todo, i should be in range 0 to m, however remember that all nums1 elements are shifted to the right n times
        while i<m and j<n:
            if nums1[i+n] <= nums2[j]:
                nums1[l] = nums1[i+n]
                i += 1
            else:
                nums1[l] = nums2[j]
                j += 1
            l += 1

        print(f"i={i}, j={j}, l={l}")
        # copy remaining elements
        while j < n:
            nums1[l] = nums2[j]
            l += 1
            j += 1

        while l < i < m+n:
            nums1[l] = nums1[i]
            l += 1
            i += 1

            

# create tests for the merge function
def test_merge1():
    s = Solution()
    nums1 = [1,2,3,0,0,0]
    m = 3
    nums2 = [2,5,6]
    n = 3
    print(f"Testing sorted merge of {nums1} with {nums2} = ")
    s.merge(nums1, m, nums2, n)
    print(nums1)
    assert nums1 == [1,2,2,3,5,6]

#now test with [1] and []
def test_merge2():
    s = Solution()
    nums1 = [1]
    m = 1
    nums2 = []
    n = 0
    print(f"Testing sorted merge of {nums1} with {nums2} = ")
    s.merge(nums1, m, nums2, n)
    print(nums1)
    assert nums1 == [1]

# test with [0] and [1]
def test_merge3():
    s = Solution()
    nums1 = [0]
    m = 0
    nums2 = [1]
    n = 1
    print(f"Testing sorted merge of {nums1} with {nums2} = ")
    s.merge(nums1, m, nums2, n)
    print(nums1)
    assert nums1 == [1]

# Test with nums1 = [4,0,0,0,0,0] m = 1 nums2 = [1,2,3,5,6] n = 5
def test_merge4():
    s = Solution()
    nums1 = [4,0,0,0,0,0]
    m = 1
    nums2 = [1,2,3,5,6]
    n = 5
    print(f"Testing sorted merge of {nums1} with {nums2} = ")
    s.merge(nums1, m, nums2, n)
    print(nums1)
    assert nums1 == [1,2,3,4,5,6]

if __name__ == "__main__":
    test_merge1()
    test_merge2()
    test_merge3()
    test_merge4()
