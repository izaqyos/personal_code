"""
Given a string s, return the longest palindromic substring in s.
Example 1:

Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.

Example 2:

Input: s = "cbbd"
Output: "bb"

Constraints:

1 <= s.length <= 1000
s consist of only digits and English letters.
"""

"""
idea:
    Recursive solution:
        stop condition: len(s) <= 1 , return s
        we to identify for each i,j where i<=j and i>=0 and j<len(s) whether s[i:j+1] is a palindrom , if so and len(s[i:j+1]) is biggest seen then update maxi, maxj to i,j 
        at the end return s[maxi:maxj+1]
"""

class Solution:
    def longestPalindrome(self, s: str) -> str:
        if len(s) <= 1:
            return s

        n = len(s)
        dp = [[False for _ in s] for _ in s]
        longest_i, longest_j = 0,0
        #for i in range(n):
        #    dp[i][j] = True

        for step in range(n):
            for i in range(0, n-step):
                j=i+step
                if i==j:
                    dp[i][j] = True
                #elif i>j: #loop revised so that i>=j invariant
                #    #dp[i][j] = False #no need, alread initialized to False
                #    continue
                else:
                    if j-i == 1:
                        if s[i] == s[j]:
                            dp[i][j] = True
                            if j-i > longest_j - longest_i: 
                                longest_i, longest_j = i,j
                    else:
                        if dp[i+1][j-1] and s[i] == s[j]:
                            dp[i][j] = True
                            if j-i > longest_j - longest_i: 
                                longest_i, longest_j = i,j
                print(f"Filling DP[{i}][{j}] = {dp[i][j]}")
        return s[longest_i:longest_j+1]


def test():
    inputs = [
       "babad",
       "cbbd",
            ]

    sol = Solution()
    for inp in inputs:
        solution = sol.longestPalindrome(inp)
        print(f"longest palindromic string of {inp} is {solution}")

def main():
    test()

if __name__ == "__main__":
    main()
        
