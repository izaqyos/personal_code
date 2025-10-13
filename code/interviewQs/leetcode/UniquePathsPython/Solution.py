"""
https://leetcode.com/problems/unique-paths/

62. Unique Paths
Medium

1158

82

Favorite

Share
A robot is located at the top-left corner of a m x n grid (marked 'Start' in the diagram below).

The robot can only move either down or right at any point in time. The robot is trying to reach the bottom-right corner of the grid (marked 'Finish' in the diagram below).

How many possible unique paths are there?


Above is a 7 x 3 grid. How many possible unique paths are there?

Note: m and n will be at most 100.

Example 1:

Input: m = 3, n = 2
Output: 3
Explanation:
From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
1. Right -> Right -> Down
2. Right -> Down -> Right
3. Down -> Right -> Right
Example 2:

Input: m = 7, n = 3
Output: 28

solved by yosi izaq

initial idea. init mXn matrix of (right, down) values set to 1,1
execpt buttom row set to (1,0) since can't move down
execpt right most column set to (0,1) since can't move down
Start w/ recursive solution
Then, check DP
"""

class cell:
    def __init__(self, right=1, down=1):
        self.right = right
        self.down = down

    def __del__(self):
        pass

    def __str__(self):
        return  str(self.right)+','+str(self.down)

class Solution(object):

    def __init__(self):
        self.board = [[]]

    def init(self, m, n):
        self.m = m
        self.n = n
        self.board = [[0 for x in range(m)]  for y in range(n)]
        self.paths = 0

        for j in range(m):
            for i in range(n):
                print("set {0},{1}".format(i,j))
                if j == m-1:
                    self.board[i][j] = cell(0,1);
                    if i == n-1:
                        self.board[i][j] = cell(0,0);
                elif i == n-1:
                    self.board[i][j] = cell(1,0);
                else:
                    self.board[i][j] = cell(1,1);

    def printBoard(self):
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board]))
        #for j in range(self.m):
        #    for i in range(self.n):
        #        print("[{0},{1}=r:{2},d:{3}]".format(i,j,self.board[i][j].right, self.board[i][j].down))

    def uPathsR(self, i, j):
        if (i==n-1) and (j == m-1):
            self.paths = self.paths+1
            return

        if self.board[i][j].right == 1:
            //rec on right cell
            //else check down. if 1 rec down cell

    def uniquePaths(self, m, n):
        """
        :type m: int
        :type n: int
        :rtype: int
        """
        self.paths=0
        self.init(m,n)
        self.printBoard()
        self.uPathsR(0,0)


def main():
    sol = Solution()
    sol.uniquePaths(3,2);

if __name__ == '__main__':
    main()
