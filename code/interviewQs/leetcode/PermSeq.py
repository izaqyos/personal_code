#!/usr/bin/python

class Solution(object):
    """
    n! is actually {1,2,...,n}! (all different permutations)
    A way to generate would be.
    1,{2,...,n}! 
    and
    2,{1,3,...n}!
    ...
    and
    n,(1,...,n-1}!
    note that given k we can know first digit. say we have list above indexed 0 (  1,{2,...,n}! ) to n-1 ( n,(1,...,n-1}!)
    we take k-1 and divide by (n-1)! , result index of first #. 
    Then we do (k-1)%((n-1)!) we get k1 (next index) repeat until n==1
    """
    def __init__(self):
        self.perms=[]

    def getPermutation(self, n, k):
        """
    :type n: int
    :type k: int
    :rtype: str
    """

        res = "" #empty string
    #calc perms once, to save time. 
        if n <= 0:
            return ""
        if n == 1:
            if k == 1:
                return "1"
            else:
                return ""
        curr = 1
        for i in range(1,n):
            curr = curr*i # 1,2,6,24,...,n-1!
            self.perms.append(curr)
        print self.perms, "\n" #n! at index n-1
        nums = range(1,n+1)
        index = k-1 
        for i in range(1,n):
            print "nums={2}, i={0}, k={1}, permutation[{4}]={3}".format(i,index, nums, self.perms[n-i-1], n-i-1)
            ithK = index/self.perms[n-i-1] # (k-1)/(n-1)! , ...
            #print "ithK={0}".format(ithK)
            res+=str(nums[ithK]) 
            index = index%self.perms[n-i-1] # (k-1)%(n-1)! -> index of next num
            #print "ithK={0}, digit={1}, index={2}. res={3}".format(ithK, str(nums[ithK]), index, res) 
            del(nums[ithK])
        #add last digit
        res+=str(nums[0])
        self.perms=[]
        return res

def main():
    permutations = range(10)
    kthperm=[0,1,1,2,3,1,5,4,7,362880]
    sol = Solution()
    #print sol.calcPerms([1,2,3,4]) 
    print "get 2nd permutation of [1,2,3]"
    print sol.getPermutation(3,2)
    print "get 5th permutation of [1,2,3]"
    print sol.getPermutation(3,6)
    for perm,k in zip(permutations, kthperm):
        print "Calculating the {0}th permutation of {1}! ".format(k,perm) 
        print "{0}".format(sol.getPermutation(perm,k)) 

if  __name__=="__main__":
    main()

