"""
91. Decode Ways
A message containing letters from A-Z can be encoded into numbers using the following mapping:

'A' -> "1"
'B' -> "2"
...
'Z' -> "26"
To decode an encoded message, all the digits must be mapped back into letters using the reverse of the mapping above (there may be multiple ways). For example, "111" can have each of its "1"s be mapped into 'A's to make "AAA", or it could be mapped to "11" and "1" ('K' and 'A' respectively) to make "KA". Note that "06" cannot be mapped into 'F' since "6" is different from "06".

Given a non-empty string num containing only digits, return the number of ways to decode it.

The answer is guaranteed to fit in a 32-bit integer.



Example 1:

Input: s = "12"
Output: 2
Explanation: "12" could be decoded as "AB" (1 2) or "L" (12).
Example 2:

Input: s = "226"
Output: 3
Explanation: "226" could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).
Example 3:

Input: s = "0"
Output: 0
Explanation: There is no character that is mapped to a number starting with 0. The only valid mappings with 0 are 'J' -> "10" and 'T' -> "20".
Since there is no character, there are no valid ways to decode this since all digits need to be mapped.
Example 4:

Input: s = "1"
Output: 1


Constraints:

1 <= s.length <= 100
s contains only digits and may contain leading zero(s).
"""

import pdb

class Solution:
    def numDecodings(self, s):
        return self.numDecodingsDP(s)
        #return self.numDecodingsMemo(s)

    def numDecodingsDP(self, s):
        """
        DP techique. Start calc from end (s[len(s)-1) to start 
        use a list dp=[-1 for _ in rage(len(s)+1). set dp[len(s)] = 1.
        first 0 return immediatly 0. 
        before loop check s[len(s)-1] set it to 1
        then loop on range(len(s)-2, 0, -1)
        For each i set it to dp[i+1]
        if s[i:i+2] <= 26 we have a second option so add dp[i] += dp[i+2]
        """
        n = len(s)
        if (n == 0) or (int(s[0]) == 0):
            return 0

        dp = [ -1 for _ in range(n+1)]
        dp[n] = 1 # if valid, at least one way
        if (int(s[-1]) == 0):
            dp[n-1] = 0
        else:
            dp[n-1] = 1

        for i in range(n-2,-1, -1):
            if int(s[i]) == 0:
                    dp[i] = 0
                    continue

            num = dp[i+1]
            if (int(s[i:i+2])<=26):
                num+=dp[i+2]
            dp[i] = num

        return dp[0]
        

    def numDecodingsMemo(self, s):
        """
        Memorization techique. Do a recursion but instead of repeating sub problems save solution in list
        recursion is simple. stop cases: i>len(s), 0 - ret 0. (first 0 return immediatly). 
        if memo for i return it. else if we treat ith char as single digit recurse into s,i+1 ways. 
        if s[i:i+2] <= 26 we have a second option so add s,i+2 ways
        """
        n = len(s)
        if (n == 0) or (int(s[0]) == 0):
            return 0

        memo = [ -1 for _ in range(n+1)]
        memo[n] = 1 #This is for recursion stop cond to return 1 
        return self.numDecodingsMemoHelper(s, 0,  memo)

    def numDecodingsMemoHelper(self, s, i,  memo):
        n = len(s)
        if i>=len(s):
            return 1
        if int(s[i]) == 0: #0 can't be leading. it is guaranteed to be least significat either 10 or 20 so it never adds an option 
            return 0
        if memo[i] != -1: #have we been here before??
            return memo[i]

        num = self.numDecodingsMemoHelper(s, i+1, memo) # any digit not 0 guaranteed to be a valid option
        if (i+1<n) and (int(s[i:i+2])<27):
            num += self.numDecodingsMemoHelper(s, i+2, memo)
        memo[i] = num 
        return num

def test():
    inputs = ["12", "226", "0", "1", "00123", "122112211221", "262729", "", "9876", "10", "2101"]
    expected = [2, 3, 0, 1, 0, 233, 2, 0, 1, 1, 1] 
    sol = Solution()
    for i,e in zip(inputs, expected):
        ans = sol.numDecodings(i)
        print('Number of ways to decode {} is {}'.format(i, ans))
        assert(ans == e)


if __name__ == "__main__":
    test()
