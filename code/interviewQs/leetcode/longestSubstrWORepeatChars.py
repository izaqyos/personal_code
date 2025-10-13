"""
3. Longest Substring Without Repeating Characters
Medium

10546

606

Add to List

Share
Given a string s, find the length of the longest substring without repeating characters.

 

Example 1:

Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
Example 2:

Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
Example 3:

Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
Example 4:

Input: s = ""
Output: 0
 

Constraints:

0 <= s.length <= 5 * 104
s consists of English letters, digits, symbols and spaces.

idea. sliding windows.
start. l<-0, h<-1 (if len<=1 return explictly...)
maxsise = 1
for c in range(1,len(str)):
    if c in str[lo:hi]:
        maxsize = max(maxsixe, h-l)
        lo=str.index[c]+1
    hi+=1
maxsize = max(maxsixe, h-l)

    
abcdabcdea
"""

class Solution:
    def lengthOfLongestSubstring(self, s):
        if len(s) < 2:
            return len(s)
        l=0
        h=1
        maxsize = 1
        ctoi = {} #character to last seen position
        ctoi[s[0]] = 0
        for i in range(1,len(s)):
        #    if c in str[l:h]: #the search in window is o(n) so overall o(n^2), can use dictionary of last seen pos for total o(n)
        # space is o(1) for naive, o(n) for dictionary
        #        lo=str.index[c]+1
        #        maxsize = max(maxsize, h-l)
        #    hi+=1
            if s[i] in ctoi:
                maxsize = max(maxsize, h-l)
                l = max(l, ctoi[s[i]] +1)
                ctoi[s[i]] = i
            else:
                ctoi[s[i]] = i
            h+=1
        return max(maxsize, h-l)

def test():
    inputs = [
        '',
        'a',
        'ab',
        'aba',
        'ababcabcd',
        'cdd',
        'abba'
    ]

    excepted = [0,1,1,2,4,2,2]
    sol = Solution()
    for inp,exp in zip(inputs,excepted):
        length = sol.lengthOfLongestSubstring(inp)
        print('longest substr of {} is {}'.format(inp, length))
        
if __name__ == "__main__":
    test()