class Solution:
    def __init__(self):
        self.expected = Solution.testExpectedRes([3, 5 ,2, 3, 4])

    def testExpectedRes(expected):
        index = 0
        expected_dists = expected 
        while index< len(expected_dists):
            yield expected_dists[index]
            index+=1

    #def printMatrix(matrix):
        #print(np.matrix(matrix))
        

    def minDistance(self, word1, word2): 
        """
        levenshtein algo. X stands for word1. Y for word2.
        """
        if len(word1) == 0:
            return len(word2)

        if len(word2) == 0:
            return len(word1)

        n1 = len(word1)
        n2 = len(word2)
        DistMtx = [ [ 0 for j in range(n2+1)]  for i in range(n1+1)]
        for j in range(n2):
            DistMtx[0][j+1] = j+1 #Delete i chars from X
        for i in range(n1):
            DistMtx[i+1][0] = i+1 #Insert j chars from Y to C
        for j in range(n2):
            for i in range(n1):
                if word1[i] == word2[j]:
                    DistMtx[i+1][j+1] = DistMtx[i][j] #If last char is same in X&Y solve subproblem X[1..i-1], Y[1..j-1] 
                else:
                    """
                    If last char is not same in X&Y take the min cost from one of three sub problems +1 for the 
                    del/insert/replace operation on last char
                    """
                    DistMtx[i+1][j+1] = min( DistMtx[i][j+1] , DistMtx[i+1][j] , DistMtx[i][j]) +1 #Last case. 
        ##ret = self.expected.__next__() # for tests pre impl
        #print('distance matrix {} X {}'.format(word1,word2))
        #Solution.printMatrix(DistMtx)
        return DistMtx[n1][n2]