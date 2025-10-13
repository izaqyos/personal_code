#!/opt/homebrew/bin/python3

from typing import List, Set, Dict, Tuple, Optional

class Solution:
    def Matrix2List(self, matrix: List[List[int]], row: int, col: int) -> int:
        m = len(matrix)
        n=len(matrix[0])
        return m*row+col
    
    def List2Matrix(self, matrix: List[List[int]], index: int) -> (int,int):
        n=len(matrix[0])
        row = index//n
        col = index%n
        return (row,col)
    
    #def bsearchMatrix(self, matrix: List[List[int]], target: int, len) -> bool:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        print(matrix)
        if (type(matrix) != list) or not matrix or len(matrix) == 0 or (type(matrix[0]) !=list):
            return False
        m = len(matrix)
        n=len(matrix[0])
        mid = (m*n)//2
        while mid>=0 and mid<m*n:
            i,j = self.List2Matrix(matrix, mid)
            if matrix[i][j] == target:
                return True
            elif matrix[i][j] > target:
                mid = (i*n+j)//2
            else:
                mid = (m*n + i*n+j)//2
        return False
        
def test():
    sol = Solution()
    inputs = [
        1,
        [1],
        [[]],
        [
            [1,   3,  5,  7],
            [10, 11, 16, 20],
            [23, 30, 34, 50]
        ],
        [
            [1,   3,  5,  7],
            [10, 11, 16, 20],
            [23, 30, 34, 50]
        ],
        [[1]],
        [[1,3,5]],
        [[1],[3],[5]] 
    ]
    targets = [1, 2, 3, 3, 13, 1, 4, 0]
    expected = [False, False, False, True, False, True, False, False]
    for (matrix, target, expect) in zip(inputs, targets, expected):
        #print('sol.searchMatrix({},{})'.format(matrix, target))
        #print('returns {} '.format(sol.searchMatrix(matrix, target)))
        print(f"searching target {target} in matrix {matrix}")
        print(f"search result is {sol.searchMatrix(matrix, target)}")
        assert(sol.searchMatrix(matrix, target) == expect)


if __name__ == "__main__":
    test()

