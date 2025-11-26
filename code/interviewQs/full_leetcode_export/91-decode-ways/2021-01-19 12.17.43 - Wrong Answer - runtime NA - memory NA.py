class Solution:
    def numDecodings(self, s):
        return self.numDecodingsMemo(s)

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
        pass

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

        memo = [ -1 for _ in range(len(s)+1)]
        memo[len(s)] = 1 #This is for recursion stop cond to return 1 
        return self.numDecodingsMemoHelper(s, 0,  memo)

    def numDecodingsMemoHelper(self, s, i,  memo):
        #pdb.set_trace()
        n = len(s)
        if i>=len(s):
            return 1
        if s[i] == 0: #0 can't be leading. it is guaranteed to be least significat either 10 or 20 so it never adds an option 
            return 0
        if memo[i] != -1: #have we been here before??
            return memo[i]

        num = self.numDecodingsMemoHelper(s, i+1, memo) # any digit not 0 guaranteed to be a valid option
        if (i+1<n) and (int(s[i:i+2])<27):
            num += self.numDecodingsMemoHelper(s, i+2, memo)
        memo[i] = num 
        return num