"""
Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

Follow up: The overall run time complexity should be O(log (m+n)).

 

Example 1:

Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
Example 2:

Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
Example 3:

Input: nums1 = [0,0], nums2 = [0,0]
Output: 0.00000
Example 4:

Input: nums1 = [], nums2 = [1]
Output: 1.00000
Example 5:

Input: nums1 = [2], nums2 = []
Output: 2.00000
 

Constraints:

nums1.length == m
nums2.length == n
0 <= m <= 1000
0 <= n <= 1000
1 <= m + n <= 2000

Idea.
there's must be some partition of the 2 arrays where the median is
lets say in nums1 indices i-1,i in nums2 j-1, j
it would satisfy these conditions
a, max(nums1[i-1], nums2[j-1]) <= min(nums1[i], nums2[j])
b, i+j == (len(nums1)-i)+(len(nums2)-j) #splits in half
c, the middle point (len(nums1))+(len(nums2))//2 is equal to i+j-1 
so  nums1[i-1]<= nums2[j]) and nums2[j-1]<=nums1[i] 
We will do binary search until we find the i where the 2 paris of numbers satisfy the condition
"""

class Solution:
    def getMax(self, arr, i): #use for left of median indices when out of bound we cont. "sorting" by returning - infinity
        if i<0:
            return -999999
        else:
            return arr[i]

    def getMin(self, arr, i): #use for right of median indices when out of bound we cont. "sorting" by returning infinity
        if i> len(arr)-1:
            return 999999
        else:
            return arr[i]

    def findMedianSortedArrays(self, nums1, nums2):
        if len(nums1) > len(nums2): #optimization, search on smaller array
            nums1, nums2 = nums2, nums1
        m = len(nums1)
        n = len(nums2)
        lo=0
        hi=m
        mid=(m+n)//2 #combined arrays median location
        while lo<=hi:
            i = (lo+hi)//2
            j=mid-i #i+j should always equal mid. we will adjust i and j using binary search 
            #print('lo={}, hi={}, mid={}, i={}, j={}'.format(lo, hi, mid, i, j))
            n1l = self.getMax(nums1, i-1)
            n1r = self.getMin(nums1, i)
            n2l = self.getMax(nums2, j-1)
            n2r = self.getMin(nums2, j)
            #print('n1l={}, n1r={}, n2l={}, n2r={}, '.format(n1l, n1r, n2l, n2r))
            if (n1l <= n2r) and (n2l <= n1r): #stop cond
                #we found the mid partition...
                if (m+n)%2:
                    return float(min(n1r, n2r))
                else:
                    return (max(n1l, n2l) + min(n1r, n2r))/2
            
            if n1l > n2r: #search left part
                hi = i-1
            else: #search right part
                lo = i+1

        return -1





def test():
    inputs = [
        ([1,3], [2]),
        ([1,2], [3,4]),
        ([1,2,5,7], [0,3,4,6]),
    ]
    expected = [2.0, 2.5, 3.5]
    sol = Solution()
    for inp,exp in zip(inputs, expected):
        med = sol.findMedianSortedArrays(inp[0], inp[1])
        print('median of {},{} is {}'.format(inp[0], inp[1], med))
        #assert(med == exp)

if __name__ == '__main__':
    test()