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
        i,j, l = m, 0, 0 # pointers to nums1, nums2 and left most free spot in nums1 
        while l<i<m+n and j<n:
            if nums1[i] <= nums2[j]:
                nums1[l] = nums1[i]
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
