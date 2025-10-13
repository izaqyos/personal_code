"""
Shortest Path in Binary Matrix
Given an n x n binary matrix grid, return the length of the shortest clear path in the matrix. If there is no clear path, return -1.

A clear path in a binary matrix is a path from the top-left cell (i.e., (0, 0)) to the bottom-right cell (i.e., (n - 1, n - 1)) such that:

All the visited cells of the path are 0.
All the adjacent cells of the path are 8-directionally connected (i.e., they are different and they share an edge or a corner).
The length of a clear path is the number of visited cells of this path.

 

Example 1:


Input: grid = [[0,1],[1,0]]
Output: 2
Example 2:


Input: grid = [[0,0,0],[1,1,0],[1,1,0]]
Output: 4
Example 3:

Input: grid = [[1,0,0],[1,1,0],[1,1,0]]
Output: -1
 

Constraints:

n == grid.length
n == grid[i].length
1 <= n <= 100
grid[i][j] is 0 or 1
"""

"""
idea. BFS. now in regular BFS we can traverse by vertice to left, right,up, down
for 8 directionally neighbors we can also traverse by edges so diaganolas up-right (i-1,j+1), down-right (i+1,j+1), down-left (i+1,j-1) and up-left (i-1,j-1)
basically adjacancies diffs are [(-1,0), (-1,+1), (0,+1), (+1,+1), (+1,0), (+1,-1), (0, -1), (-1,-1)]  
"""

class Solution:
    def is_valid_pos(self, grid, i, j):
        n = len(grid)
        return 0<=i<n and 0<=j<n

    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0] or grid[0][0] == 1:
            return -1
        from collections import deque
        adjacancies = [(-1,0), (-1,+1), (0,+1), (+1,+1), (+1,0), (+1,-1), (0, -1), (-1,-1)]
        visited = set()
        row,col = 0, 0
        visited.add((row,col))
        explore_q = deque() 
        explore_q.append ( (row,col,1) ) #cell row,col,path length

        while explore_q:
            row, col, path_length = explore_q.popleft() 
            #print(f"Current cell {row,col} val={grid[row][col]}, path length {path_length}")
            if row==len(grid)-1 and col==len(grid)-1 :
                if grid[row][col] == 0:
                    return path_length
                else: #unreachable code since won't be added 2 q
                    return -1
            for (row_diff,col_diff) in adjacancies:
                #print(f"exploring neighbor cell {row+row_diff, col+col_diff}")
                if self.is_valid_pos(grid, row+row_diff, col+col_diff) and (not (row+row_diff, col+col_diff) in visited) and grid[row+row_diff][col+col_diff] == 0:
                    #print(f"cell {row+row_diff, col+col_diff} is not visited and its value is 0 ")
                    visited.add((row+row_diff, col+col_diff))
                    explore_q.append((row+row_diff, col+col_diff, path_length+1))
        if row==len(grid)-1 and col==len(grid)-1 :
            return path_length
        else:
            return -1
