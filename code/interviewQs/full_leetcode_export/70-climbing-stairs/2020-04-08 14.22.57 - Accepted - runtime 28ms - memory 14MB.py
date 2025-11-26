class Solution:
    def climbStairs(self, n):
        if n>=0 and n<=2  :
            return n

        ndp = [1,2]
        for i in range(2, n):
            ndp.append(ndp[i-1] + ndp[i-2])
        
        return ndp[n-1]
