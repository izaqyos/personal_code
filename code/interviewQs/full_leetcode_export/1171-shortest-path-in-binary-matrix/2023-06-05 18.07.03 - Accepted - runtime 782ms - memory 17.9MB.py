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
