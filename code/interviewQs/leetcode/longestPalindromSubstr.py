"""

5. Longest Palindromic Substring
Medium

7836

567

Add to List

Share
Given a string s, find the longest palindromic substring in s. You may assume that the maximum length of s is 1000.

Example 1:

Input: "babad"
Output: "bab"
Note: "aba" is also a valid answer.
Example 2:

Input: "cbbd"
Output: "bb"

idea.
1st brute force.double loop for all substrs. (n^2) then check if pali (o(n)) -> o(n^3). space o(1)
improve. check pali from each position by expanding left and right until not pali s[left] != s[right]
note 2 kinds of pali. xxyxx and xxxx. so we want three indexes. l,s,r (left, start, right.)
start them all at current char.
then skip same chars so that right is after all same chars. left is start. go left -offset, right -offset compare chars
"""

import pdb
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
            





def test():
    #inputs = ['cbbd']
    #expected = ['cbbd']
    inputs = ['', 'a', 'aa', 'babad', 'cbbd', 'abcdefedcba', 'abccba', 'yosi']
    expected = ['', 'a', 'aa', 'bab', 'cbbd', 'abcdefedcba', 'abccba', 'y' ]
    for inp,exp in zip(inputs, expected):
        sol = Solution()
        paliLen = sol.longestPalindrome(inp)
        print('longest palindrome substr of {} is {}'.format(inp, paliLen))
    
if __name__ == "__main__":
    test()