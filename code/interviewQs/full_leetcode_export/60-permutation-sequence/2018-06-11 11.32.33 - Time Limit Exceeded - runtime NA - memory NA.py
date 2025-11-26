class permGen():
    """
        permutation generator using narayana algorithm 
        sort list (nlogn) , then generate k-1 next permutations in lexicographical order. its o(n) to get next perm and k is n! in worst case
        use narayana algorithm (o(n) for next permutation in increasing lexicographical order which goes as follows:
        Find the largest index k such that a[k] < a[k + 1]. If no such index exists, the permutation is the last permutation.
        Find the largest index l greater than k such that a[k] < a[l].
        Swap the value of a[k] with that of a[l].
        Reverse the sequence from a[k + 1] up to and including the final element a[n].
    """
    def __init__(self, l):
        self.list = sorted(l)
        self.lastPerm = False 
        self.bDebug = False
        #self.bDebug = True
        if self.bDebug: print "__init__() list={0}, lastPerm={1}".format(self.list, self.lastPerm)
        
    def __iter__(self):
        return self

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def reverseRange(self, lst, start, end):
        if self.bDebug: print "reverseRange() list={0}, start={1}, end={2}".format(lst, start, end)
        if  (start<0) or (end >= len(lst) )  :
            return

        while (start < end):
            lst[start],lst[end] = lst[end],lst[start]
            start = start+1
            end = end -1

    #def __iter__(): #genNextLexiPerm
    def genNextLexiPerm(self, ignored_arg): #
        if not self.lastPerm:
            #yield self.list #note. generator class next method doesn't use yield syntax.

            bKExists = False
            retList = self.list[:]
            i=len(self.list)-1
            k=0
            l=0
            if self.bDebug: print "genNextLexiPerm() retList={0}, i={1}".format(retList, i)
            while i > 0:
                #if self.bDebug: print "genNextLexiPerm() i={0}, self.list[i]={1}, self.list[i-1]={2}, ".format( i, self.list[i] , self.list[i-1])
                if (self.list[i] > self.list[i-1]):
                    k=i-1
                    bKExists = True
                    break
                i=i-1

            if self.bDebug: print "genNextLexiPerm() index of largest elem in increasing order k={0}".format(k)
            if (not bKExists): #no k such that kth elem < kth+1 meaning self.list is in full descending order => this is last perm
                self.lastPerm = True 

            j=len(self.list)-1
            while j >  k:
                if self.list[j] > self.list[k]:
                    l = j 
                    break;
                j=j-1

            if self.bDebug: print "genNextLexiPerm() index of largest elem larger than element k. l={0}".format(l)
            self.list[k], self.list[l]= self.list[l] ,self.list[k] 

            #now reverse range k+1 to end ... todo write reverse range method
            self.reverseRange(self.list,k+1, len(self.list)-1)
            if self.bDebug: print "genNextLexiPerm() returning List={0}".format(retList)
            return retList

        #gen next perm
        else :
            raise StopIteration

        
    def next(self):
        return self.genNextLexiPerm(None)

    def close(self):
        """
        Raise GeneratorExit inside generator.
        """
        try:
            self.throw(GeneratorExit)
        except (GeneratorExit, StopIteration):
            pass
        else:
            raise RuntimeError("generator ignored GeneratorExit")


class Solution(object):

    def calcPerms(self, nums):
        if not nums:
            return [[]]

        numsList = []
        """
        This is for practice. gen all permutations o(n!)
        """

        for n in nums:
            tempnums = nums[:] #deep copy
            tempnums.remove(n)
            numsList.extend( [ [n] + r for r in self.calcPerms(tempnums) ] )

        return numsList


    def getPermutation(self, n, k):
        """

        :type n: int
        :type k: int
        :rtype: str
        """
        if n == 0:
            return None
        pGen=permGen(range(1,n+1))
        i=0
        while i<k-1:
            next(pGen)
            i=i+1
        return ''.join(map(str, next(pGen))) #convert list to string


        