"""
LC 994 - Rotting Oranges (Medium)

You are given an m x n grid where each cell can have one of three values:
    0 representing an empty cell,
    1 representing a fresh orange, or
    2 representing a rotten orange.

Every minute, any fresh orange that is 4-directionally adjacent to a
rotten orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has
a fresh orange. If this is impossible, return -1.

Example 1:
    Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
    Output: 4

Example 2:
    Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
    Output: -1
    Explanation: The orange in the bottom left corner never rots,
    because rotting only happens 4-directionally.

Example 3:
    Input: grid = [[0,2]]
    Output: 0
    Explanation: There are no fresh oranges, so the answer is just 0.

Constraints:
    m == grid.length
    n == grid[i].length
    1 <= m, n <= 10
    grid[i][j] is 0, 1, or 2.
"""
from typing import List


def oranges_rotting(grid: List[List[int]]) -> int:
    pass


if __name__ == "__main__":
    grid1 = [[2,1,1],[1,1,0],[0,1,1]]
    assert oranges_rotting(grid1) == 4

    grid2 = [[2,1,1],[0,1,1],[1,0,1]]
    assert oranges_rotting(grid2) == -1

    grid3 = [[0,2]]
    assert oranges_rotting(grid3) == 0

    grid4 = [[0]]
    assert oranges_rotting(grid4) == 0

    grid5 = [[1]]
    assert oranges_rotting(grid5) == -1

    print("All tests passed.")
