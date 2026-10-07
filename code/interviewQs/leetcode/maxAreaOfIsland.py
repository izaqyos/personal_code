"""
LC 695 - Max Area of Island (Medium)

You are given an m x n binary matrix `grid`. An island is a group of 1's
(representing land) connected 4-directionally (horizontal or vertical).
You may assume all four edges of the grid are surrounded by water.

The area of an island is the number of cells with a value 1 in the island.

Return the maximum area of an island in `grid`. If there is no island,
return 0.

Example 1:
    Input: grid = [
      [0,0,1,0,0,0,0,1,0,0,0,0,0],
      [0,0,0,0,0,0,0,1,1,1,0,0,0],
      [0,1,1,0,1,0,0,0,0,0,0,0,0],
      [0,1,0,0,1,1,0,0,1,0,1,0,0],
      [0,1,0,0,1,1,0,0,1,1,1,0,0],
      [0,0,0,0,0,0,0,0,0,0,1,0,0],
      [0,0,0,0,0,0,0,1,1,1,0,0,0],
      [0,0,0,0,0,0,0,1,1,0,0,0,0]
    ]
    Output: 6
    Explanation: The answer is not 11, because the island must be
    connected 4-directionally.

Example 2:
    Input: grid = [[0,0,0,0,0,0,0,0]]
    Output: 0

Constraints:
    m == grid.length
    n == grid[i].length
    1 <= m, n <= 50
    grid[i][j] is either 0 or 1.
"""
from typing import List
from collections import deque


def neighbors(i,j,m,n):
    return [ (x,y) for (x,y) in [(i+1,j), (i-1,j), (i, j+1), (i, j-1)] if 0 <= x < m and 0 <= y < n ]

def max_area_of_island(grid: List[List[int]]) -> int:
    if not grid: return 0
    m = len(grid)
    if m == 0: return 0
    n = len(grid[0])
    if n == 0: return 0
    
    q = deque()
    max_area_of_island_counter = 0
    local_max = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1: #boom, island found
                q.append((i,j))
                grid[i][j] = 0 #mark as visited
                local_max = 1
                #now BFS connected parts
                while q:
                    r, c = q.popleft()
                    for x,y in neighbors(r,c,m,n):
                        if grid[x][y] == 1:
                            q.append((x,y))
                            grid[x][y] = 0
                            local_max += 1
                # lets update max area
                max_area_of_island_counter = max(max_area_of_island_counter, local_max)
                local_max = 0
    return max_area_of_island_counter



if __name__ == "__main__":
    grid1 = [
        [0,0,1,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,0,0,0],
        [0,1,1,0,1,0,0,0,0,0,0,0,0],
        [0,1,0,0,1,1,0,0,1,0,1,0,0],
        [0,1,0,0,1,1,0,0,1,1,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,0,0,0],
    ]
    assert max_area_of_island(grid1) == 6

    grid2 = [[0,0,0,0,0,0,0,0]]
    assert max_area_of_island(grid2) == 0

    grid3 = [[1]]
    assert max_area_of_island(grid3) == 1

    grid4 = [
        [1,1],
        [1,1],
    ]
    assert max_area_of_island(grid4) == 4

    print("All tests passed.")
