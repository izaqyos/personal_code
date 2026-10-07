"""
LC 200 - Number of Islands (Medium)

Given an m x n 2D binary grid `grid` which represents a map of '1's (land)
and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent
lands horizontally or vertically. You may assume all four edges of the
grid are all surrounded by water.

Example 1:
    Input: grid = [
      ["1","1","1","1","0"],
      ["1","1","0","1","0"],
      ["1","1","0","0","0"],
      ["0","0","0","0","0"]
    ]
    Output: 1

Example 2:
    Input: grid = [
      ["1","1","0","0","0"],
      ["1","1","0","0","0"],
      ["0","0","1","0","0"],
      ["0","0","0","1","1"]
    ]
    Output: 3

Constraints:
    m == grid.length
    n == grid[i].length
    1 <= m, n <= 300
    grid[i][j] is '0' or '1'
"""
from typing import List

from collections import deque

def get_neighbors(i,j, m, n):
    neighbors = []
    if i > 0: neighbors.append((i-1,j))
    if i<m-1 : neighbors.append((i+1,j))
    if j > 0: neighbors.append((i,j-1))
    if j<n-1 : neighbors.append((i,j+1))
    return neighbors

def num_islands(grid: List[List[str]]) -> int:
    ret = 0
    q = deque()
    m,n = len(grid), len(grid[0])
    for i in range(m):
        for j in range(n):
            print(f"checking {i},{j}, value {grid[i][j]}")
            if grid[i][j] == '1': # found island
                ret+=1
                print(f"found island, adding to ret, now ret is {ret}")
                # not lets BFS connected parts to mark this island
                q.append((i,j))
                grid[i][j] = '0'
                while q:
                    r,c = q.popleft()
                    for x,y in get_neighbors(r,c,m,n):
                        if grid[x][y] == '1':
                            q.append((x,y))
                            grid[x][y] = '0'

    print(f"ret is {ret}")
    return ret


if __name__ == "__main__":
    grid1 = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"],
    ]
    assert num_islands(grid1) == 1

    grid2 = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"],
    ]
    assert num_islands(grid2) == 3

    grid3 = [["0"]]
    assert num_islands(grid3) == 0

    grid4 = [["1"]]
    assert num_islands(grid4) == 1

    print("All tests passed.")
