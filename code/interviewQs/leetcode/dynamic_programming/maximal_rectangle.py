#!/opt/homebrew/bin/python3

"""
Maximal Square
Given an m x n binary matrix filled with 0's and 1's, find the largest square containing only 1's and return its area.
Example 1:
Input: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
Output: 4

Example 2:
Input: matrix = [["0","1"],["1","0"]]
Output: 1
Example 3:

Input: matrix = [["0"]]
Output: 0


Constraints:

m == matrix.length
n == matrix[i].length
1 <= m, n <= 300
matrix[i][j] is '0' or '1'.


Strategy:
    Recursion. how to break into subproblems?
    imagine u r at cell i,j , if value is 0 it can't add up to a bigger rectangle so skip it 
    new if its a 1 and next to it to the right (i,j+1) there's a rectangle of length X
    also to the diagonal (i+1,j+1) there's a rectangle of length X
    and also to the right there's a rectangle of length X
    Then the 1 in i,j completes to a rectangle of length X+1
    ex:
        1 1 1 
        1 1 1 
        1 1 1 
i,j = 0,0 
i,j+1 we have a rectangle of length 2
i+1,j we have a rectangle of length 2
i+1,j+1 we have a rectangle of length 2
so in 0,0 we have a rectangle of length 3

Now recursion will force us to recalculate a lot of subproblems and will run in complexity O((mXn)^2)
better approach, top down dp.
lets start dp of mXn with values of 0 (length of square of top left corner i,j)
then fill it from end. for last column and row just put 1 iff matrix[i][j] == 1
then loop in reverse on lines and colums and set dp as follows
dp[i][j] = X + 1 if following conditions are met:
    a. matrix[i][j] == 1
    b. dp[i][j+1]   == X
    c. dp[i+1][j]  == X
    d. dp[i+1][j+1]  == X
"""

class Solution:
    def maximalSquare(self, matrix: list[list[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0
        m,n = len(matrix), len(matrix[0])
        dp = [ [0 for _ in matrix[0]] for _ in matrix]
        max_rect_size = 0
        for i in range(m):
            dp[i][n-1] = int(matrix[i][n-1]) #in last column max size is at max 1 since it's not possible to increase size by expanding right, down or diagonal
            #print(f"matrix[{i}][{n-1}] = {matrix[i][n-1]}, dp[{i}][{n-1}] = {dp[i][n-1]}, max_rect_size={max_rect_size}")
            if dp[i][n-1] == 1:
                #print(f"found cell 1 in {i},{n-1}")
                max_rect_size = 1
        for j in range(n):
            dp[m-1][j] = int(matrix[m-1][j])
            if dp[m-1][j] == 1:
                #print(f"found cell 1 in {m-1},{j}")
                max_rect_size = 1

        #now let's fill the rest top down and keep tabs on max size seen
        for i in range(m-2, -1, -1):
            for j in range(n-2, -1, -1):
                #print(f"checking {i},{j}={matrix[i][j]} , max_rect_size = {max_rect_size}, dp={dp}")
                if matrix[i][j] == "1":
                    dp[i][j] = 1
                    #print(f"dp at {i},{j} = {dp[i][j]}")
                    min_adjacent_squares_size = min(dp[i+1][j] ,  dp[i+1][j+1] ,  dp[i][j+1] )
                    if min_adjacent_squares_size >= dp[i][j]:
                        #print(f"found bigger square at {i},{j} of size {min_adjacent_squares_size +1}")
                        dp[i][j] = min_adjacent_squares_size +1
                    max_rect_size = max(max_rect_size, dp[i][j])

        return max_rect_size*max_rect_size

def test():
    input_list = [
            [["1","1","1","1","0"],["1","1","1","1","0"],["1","1","1","1","1"],["1","1","1","1","1"],["0","0","1","1","1"]],
            [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]],
            [["0","1"],["1","0"]],
            [["0"]]
            ]
    sol = Solution()
    for inp in input_list:
        size = sol.maximalSquare(inp)
        print(f"Solved for {inp}, size={size}")

def main():
    test()

if __name__ == "__main__":
    main()
