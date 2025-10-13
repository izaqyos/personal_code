"""
Given a m x n matrix, if an element is 0, set its entire row and column to 0. Do it in-place.

Example 1:

Input: 
[
  [1,1,1],
  [1,0,1],
  [1,1,1]
]
Output: 
[
  [1,0,1],
  [0,0,0],
  [1,0,1]
]
Example 2:

Input: 
[
  [0,1,2,0],
  [3,4,5,2],
  [1,3,1,5]
]
Output: 
[
  [0,0,0,0],
  [0,4,5,0],
  [0,3,1,0]
]
Follow up:

A straight forward solution using O(mn) space is probably a bad idea.
A simple improvement uses O(m + n) space, but still not the best solution.
Could you devise a constant space solution?

will test two solutions.
O(mn) space. keep to lists rows/columns mark 0 for each row/column to be zeroized
O(1) spaces. use 1st col/row as the row/col list like in O(mn) solution. 
problem. we lose the data that was in 1st col/row. 
solution. if there r zeros in 1st col/row raise a bool col/row flag.
At the end do three loops.
1st. MxN each M[i][j] where M[i][0] / M[0][j] r 0 set to 0
2nd. if col flag run over all columns. if M[0][j] is 0 zeroize the whole column
3rd. if row flag run over all rows. if M[0][j] is 0 zeroize the whole column
"""

import numpy as np
import pdb


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


def testEqlMatrices(m1, m2):
    if not isinstance(m1, list):
        return False
    if not isinstance(m2, list):
        return False

    if len(m1) == 0 and len(m2) == 0:
        return True
    if len(m1) != len(m2):
        return False

    #list and matrix
    if isinstance(m2[0], list) and (not isinstance(m1[0], list)):
        return False
    if isinstance(m1[0], list) and (not isinstance(m2[0], list)):
        return False

    # pdb.set_trace()
    # two lists
    if (not isinstance(m1[0], list)) and (not isinstance(m2[0], list)):
        for i in range(len(m1)):
            if m1[i] != m2[i]:
                return False
        return True

    # two matrices
    if len(m1[0]) != len(m2[0]):
        return False

    # same dims
    for i in range(len(m1)):
        for j in range(len(m1[0])):
            if m1[i][j] != m2[i][j]:
                return False
    return True


def testEqlMtx():
    inputMatrices = [
        [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ],
        [
            [0, 1, 2, 0],
            [3, 4, 5, 2],
            [1, 3, 1, 5]
        ],
        [],
        [1, 2, 3],
    ]
    expectedEqualityOfInputvInput = [True, True, True, True]

    compareMatrices = [
        [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ],
        [
            [0, 1, 2, 0],
            [3, 4, 6, 2],
            [1, 3, 1, 5]
        ],
        [[1, 2],
         [3, 4]
         ],
        [],
    ]
    expectedEqualityOfInputvCompare = [True, False, False, False]

    for mtx in inputMatrices:
        print('test matrix eql itself')
        print(np.matrix(mtx))
        assert(testEqlMatrices(mtx, mtx))

    for i in range(len(inputMatrices)):
        print('test matrix equality. Expect equation to be {}'.format(
            expectedEqualityOfInputvCompare[i]))
        print(np.matrix(inputMatrices[i]))
        print(np.matrix(compareMatrices[i]))
        assert(testEqlMatrices(
            inputMatrices[i], compareMatrices[i]) == expectedEqualityOfInputvCompare[i])


def test():
    inputMatrices = [
        [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ],
        [
            [0, 1, 2, 0],
            [3, 4, 5, 2],
            [1, 3, 1, 5]
        ],
    ]

    exceptedMatrices = [
        [
            [1, 0, 1],
            [0, 0, 0],
            [1, 0, 1]
        ],
        [
            [0, 0, 0, 0],
            [0, 4, 5, 0],
            [0, 3, 1, 0]
        ]
    ]

    sol = Solution()
    for i in range(len(inputMatrices)):
        print('original matrix')
        print(np.matrix(inputMatrices[i]))
        sol.setZeroes(inputMatrices[i])
        print('zeroized matrix')
        print(np.matrix(inputMatrices[i]))
        assert(testEqlMatrices(inputMatrices[i], exceptedMatrices[i]))


if __name__ == "__main__":
    # testEqlMtx()
    test()
