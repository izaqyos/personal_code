class Solution:
    def findLength(self, nums1: List[int], nums2: List[int]) -> int:
        """
        idea. if we had a recursive call that would get the length of repeated subarray ending in
        positions i,j for nums1/2 respectively. Then for i+1,j+1 if values are equal we can add 1.
        if not same value do not increase the length.  Use DP matrix to memorize sub results
        """
        m=len(nums1)
        n=len(nums2)
        maxlen = 0
        dp = [[0 for _ in range(n+1)] for _ in range(m+1)]
        for i in range(m):
            for j in range(n):
                if nums1[i] == nums2[j]:
                    dp[i][j] = dp[i-1][j-1]+1
                    maxlen = max(maxlen, dp[i][j])
        return maxlen
