"""
Given two sorted integer arrays nums1 and nums2, merge nums2 into nums1 as one sorted array.

The number of elements initialized in nums1 and nums2 are m and n respectively. You may assume that nums1 has enough space (size that is equal to m + n) to hold additional elements from nums2.



Example 1:

Input: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
Output: [1,2,2,3,5,6]
Example 2:

Input: nums1 = [1], m = 1, nums2 = [], n = 0
Output: [1]


Constraints:

0 <= n, m <= 200
1 <= n + m <= 200
nums1.length == m + n
nums2.length == n
-109 <= nums1[i], nums2[i] <= 109
"""

class Solution:
    def merge(self, nums1, m, nums2, n):
        """
        Do not return anything, modify nums1 in-place instead.
        """
        n1copy=nums1[:m]
        i,j=0,0
        while (i<m) and (j<n):
            if n1copy[i]<nums2[j]:
                nums1[i+j] = n1copy[i]
                i+=1
            else:
                nums1[i+j]=nums2[j]
                j+=1

        while i<m:
            nums1[i+j] = n1copy[i]
            i+=1

        while j<n:
            nums1[i+j] = nums2[j]
            j+=1



def test():
    inputs = [
[[1,2,3,0,0,0], 3, [2,5,6], 3],
[[1,7,13,20,0,0, 0], 4, [0,17,21], 3],
            ]
    expected = [
            [1,2,2,3,5,6],
            [0,1,7,13,17,20,21],
            ]
    sol = Solution()
    for inp,exp in zip(inputs, expected):
        ans = inp[0]
        print('merge sorted input {}, {}, {}, {}'.format(*inp))
        sol.merge(*inp)
        print('merge sorted output {}'.format(ans))
        assert(exp == ans)


if __name__ == "__main__":
    test()

