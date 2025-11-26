class Solution:
    def numTrees(self, n):
        mem = [0 for _ in range(n+1)] # 0 val is helper for recursion. real values in 1,..,n
        mem[0], mem[1] = 1,1
        for i in range(2,n+1): #memorization loop
            total = 0
            for j in range(i): #add two possible subtees with i-1 nodes. the ith is the root always.
                total+= mem[j]*mem[i-1-j]
            mem[i] = total
        return mem[n]
