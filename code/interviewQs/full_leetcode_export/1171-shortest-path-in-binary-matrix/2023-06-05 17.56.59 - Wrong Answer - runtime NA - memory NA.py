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
        visited.add((0,0))
        explore_q = deque() 
        explore_q.append ( (0,0,1) ) #cell row,col,path length

        while explore_q:
            row, col, path_length = explore_q.popleft() 
            #print(f"Current cell {row,col}, path length {path_length}")
            if grid[row][col]:
                return path_length
            for (row_diff,col_diff) in adjacancies:
                #print(f"exploring neighbor cell {row+row_diff, col+col_diff}")
                if self.is_valid_pos(grid, row+row_diff, col+col_diff) and (not (row+row_diff, col+col_diff) in visited) and grid[row+row_diff][col+col_diff] == 0:
                    #print(f"cell {row+row_diff, col+col_diff} is not visited and its value is 0 ")
                    visited.add((row+row_diff, col+col_diff))
                    explore_q.append((row+row_diff, col+col_diff, path_length+1))
        return path_length
