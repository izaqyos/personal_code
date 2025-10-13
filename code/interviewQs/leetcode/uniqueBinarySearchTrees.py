"""
96. Unique Binary Search Trees


Example 1:


Input: n = 3
Output: 5
Example 2:

Input: n = 1
Output: 1


Constraints:

1 <= n <= 19

idea, 
Use recursion (optimize with memo array...)
So, n==1 => 1 ; there's 1 option.
n==2. Two options. consider L,R as left / right subtrees. f(L/R) is # nodes in left/right subtree
so f(L),f(R) options are 0,1 and 1,0 mem[1] is 1 so we add and get 2.

n==3 
f(L),f(R) options are 0,2 and 2,0 and 1,1 so 2*mem[2] + 1 so we add and get 5.

n==4
f(L),f(R) options are 0,3 and 3,0, 1,2, 2,1  and 1,1 so 2*mem[3] + 2*mem[2] so we add and get 12.

So clearly when we memorize 1..n-1 calculate mem[n] by loop i<=n/2
calculate i,n-1 pairs and sum their memorized values
"""

#class Solution:
#    def numTrees(self, n):
#        if n == 1:
#            return 1
#        mem = [0 for _ in range(n+1)] # 0 val is helper for recursion. real values in 1,..,n 
#        for i in range(1,n+1): #memorization loop
#            total = 0
#            for j in range(i): #add two possible subtees with i-1 nodes. the ith is the root always.
#                if 2*j == i-1:
#                    total += mem[j] #subtrees are same so L,R or R,L have same structure => count as 1
#                else:
#                    total+= mem[j]+mem[i-1-j]+1
#            mem[i] = total
#        return mem[n]

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

def test():
    """TODO: Docstring for test.
    :returns: TODO

    """
    inputs = [_ for _ in range(1,20)]
    expected = [1, 2, 5]
    sol = Solution()
    for inp in inputs:
        ans = sol.numTrees(inp)
        print('Number of unique binary search trees for n={} is {}'.format(inp, ans))

if __name__ == "__main__":
    test()
