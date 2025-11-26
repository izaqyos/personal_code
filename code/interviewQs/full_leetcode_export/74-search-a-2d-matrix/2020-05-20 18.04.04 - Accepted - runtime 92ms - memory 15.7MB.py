class Solution:
    """
    binary search the matrix is if it were a list where
    MT is a MXN matrix
    MT[i][j] == L[i*N +j] 
    """

    def __init__(self):
        super().__init__()
        self.M = 0
        self.N = 0

    def convert2D(self, index):
        #print('converting {} using line size {}'.format( index, self.N))
        if self.N > 0:
            return index // (self.N), index % (self.N)

    def convert1D(self, i, j):
        return i*(self.N) + j

    def bsearch(self, matrix, low, high, target):
        #print('bsearch(low={}, high={}'.format(low, high))
        found = False
        if (low > high):
            return found
        elif low == high:
            (i, j) = self.convert2D(low)
            return matrix[i][j] == target

        (i, j) = self.convert2D((low+high)//2)
        #print('middle={}, i={}, j={}, convert21D={}'.format((low+high)//2, i, j, self.convert1D(i,j)))
        if target == matrix[i][j]:
            return True
        elif target > matrix[i][j]:
            found = self.bsearch(matrix, self.convert1D(i, j)+1, high, target)
        else:
            found = self.bsearch(matrix, low, self.convert1D(i, j)-1, target)

        return found

    def searchMatrix(self, matrix, target):
        """
        basically, bsearch, reduce 2d to 1d indices wise
        """
        if (not isinstance(matrix, list)):
            return False

        self.M = len(matrix)
        if self.M == 0 or (not isinstance(matrix[0], list)):
            return False

        # list is invalid input
        if not isinstance(matrix, list):
            return False

        self.N = len(matrix[0])
        if self.N == 0:
            return False

        return self.bsearch(matrix, 0, (self.M)*(self.N)-1, target)