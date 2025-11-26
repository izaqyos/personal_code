class Solution:
    def longestPalindrome(self, s):
        if len(s) < 2:
            return s

        n = len(s)
        left,right,start = 0,0,0
        longestPaliIndex = 0
        longestPaliLen = 1
        #pdb.set_trace()
        while (start<n and ((n-start) > longestPaliLen/2) ): # since we expand 2 right and left if (n-start) <= max/2, no way to find bigger pali
            #print('at pos', start)
            left,right= start, start
            while (right<(n-1) and (s[right] == s[right+1])):
                right+=1 #now right is at last same char sequence (len>=1)

            start = right+1
            #print('right', right)
            #expand pali
            while left>0 and right<n-1 and s[left-1] == s[right+1]:
                left-=1
                right+=1

            #print('left={}, right={}, max={}, maxindex={}'.format(left, right, longestPaliLen, longestPaliIndex))
            if (right-left+1) > longestPaliLen:
                longestPaliLen = right-left+1
                longestPaliIndex = left

        return s[longestPaliIndex:longestPaliIndex+longestPaliLen]