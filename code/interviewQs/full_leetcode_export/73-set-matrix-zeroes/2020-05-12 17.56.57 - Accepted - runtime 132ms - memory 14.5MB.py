class Solution:
    def setZeroesOMN(self, matrix):
        """
        O(mn) space. keep to lists rows/columns mark 0 for each row/column to be zeroized
        """
        rows = [False for i in matrix]
        columns = [False for i in matrix[0]]

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 0:
                    #print('mark row {}, column {} to be zero'.format(i,j))
                    rows[i] = True
                    columns[j] = True
        
        for i in range(len(rows)):
            if rows[i]:
                for j in range(len(matrix[i])):
                    #print('mark  set {},{} to zero'.format(i,j))
                    matrix[i][j] = 0

        for j in range(len(columns)):
            if columns[j]:
                for i in range(len(matrix)):
                    #print('mark  set {},{} to zero'.format(i,j))
                    matrix[i][j] = 0
                

    def setZeroesO1(self, matrix):
        m = len(matrix)
        n = len(matrix[0])
        zrow = False
        zcol = False

        #Store 0 in first col in a boolean - o(1) space
        for i in range(m):
            if matrix[i][0] == 0:
                zrow = True

        #Store 0 in first row in a boolean
        for j in range(n):
            if matrix[0][j] == 0:
                zcol = True

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 0:
                    #print('mark row {}, column {} to be zero'.format(i,j))
                    rows[0][j] = 0
                    columns[i][0] = 0

        #zeroize inner (m-1)X(n-1) matrix
        for i in range(m):
            if matrix[i][0] == 0:
                for j in range(n):
                    matrix[i][j] = 0

        for j in range(n):
            if matrix[0][j] == 0:
                for i in range(m):
                    matrix[i][j] = 0

        #If needed zeroize first row
        if zrow:
            for j in range(n):
                matrix[0][j] = 0

        #If needed zeroize first column
        if zcol:
            for i in range(m):
                matrix[i][0] = 0




         
        
        

    def setZeroes(self, matrix):
        """
        Do not return anything, modify matrix in-place instead.
        """
        if (len(matrix) == 0) or (not isinstance(matrix, list)):
            return matrix

        # lists r nobrainers
        if (not isinstance(matrix[0], list)):
            zeroize = False
            for n in matrix:
                if n == 0:
                    zeroize = True

            for i in range(len(matrix)):
                matrix[i] = 0
            return matrix

        #print('run O(mn) space solution')
        return self.setZeroesOMN(matrix)

        #print('run O(1) space solution')
        return self.setZeroesO1(matrix)


