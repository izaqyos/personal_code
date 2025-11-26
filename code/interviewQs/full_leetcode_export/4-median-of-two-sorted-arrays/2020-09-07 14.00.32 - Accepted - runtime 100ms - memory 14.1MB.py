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

