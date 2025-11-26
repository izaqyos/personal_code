class Solution:
    def climbStairs(self, n):
        if n>=0 and n<=2  :
            return n

        ##o(n) space, o(n) time
        #ndp = [1,2]
        #for i in range(2, n):
        #    ndp.append(ndp[i-1] + ndp[i-2])
        #return ndp[n-1]
        
        #o(1) space, o(n) time
        fibLastTwo = [1,2]
        for i in range(2, n):
            cur = fibLastTwo[0] + fibLastTwo[1]
            fibLastTwo[0] = fibLastTwo[1]
            fibLastTwo[1] = cur
        return fibLastTwo[1]