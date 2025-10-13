"""
You are given an m x n integer matrix grid where each cell is either 0 (empty) or 1 (obstacle). You can move up, down, left, or right from and to an empty cell in one step.

Return the minimum number of steps to walk from the upper left corner (0, 0) to the lower right corner (m - 1, n - 1) given that you can eliminate at most k obstacles. If it is not possible to find such walk return -1.

 

Example 1:


Input: grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]], k = 1
Output: 6
Explanation: 
The shortest path without eliminating any obstacle is 10.
The shortest path with one obstacle elimination at position (3,2) is 6. Such path is (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2) -> (3,2) -> (4,2).
Example 2:


Input: grid = [[0,1,1],[1,1,1],[1,0,0]], k = 1
Output: -1
Explanation: We need to eliminate at least two obstacles to find such a walk.
 

Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 40
1 <= k <= m * n
grid[i][j] is either 0 or 1.
grid[0][0] == grid[m - 1][n - 1] == 0

idea:
    brute force BFS. brute force in the sense that we keep track of how many obstacles we can remove and as long as we have removals left 

    Reference Solution:
        class Solution:
    def shortestPath(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])

        # x, y, obstacles, steps
        q = deque([(0,0,k,0)])
        seen = set()

        while q:
            x, y, left, steps = q.popleft()
            if (x,y,left) in seen or left<0:
                continue
            if (x, y) == (m-1, n-1):
                return steps
            seen.add((x,y,left))
            if grid[x][y] == 1:
                left-=1
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                new_x, new_y = x+dx, y+dy
                if 0<=new_x<m and 0<=new_y<n:
                    q.append((new_x, new_y, left, steps+1))
        return -1

"""

class Solution:
    def shortestPath(self, grid: List[List[int]], k: int) -> int:
        if not grid or not grid[0]:
            return -1
        removalsLeft = k
        m,n = len(grid), len(grid[0])
        q = deque([(0,0,removalsLeft, 0)])
        visited = set()

        while q:
            x,y,left,steps = q.popleft()
            #print(x,y,left,steps )
            if left<0 or (x,y,left) in visited:
                continue # no go, either obstacle can't be removed 
            if (x,y) == (m-1, n-1):
                return steps
            visited.add((x,y,left))
            if grid[x][y] == 1:
                left -=1
            #Add next neighbors, since it's a matrix we can either move up, down, right or left 
            for dx, dy in [(1,0), (-1,0),(0,1),(0,-1)]:
                nextx, nexty = x+dx, y+dy 
                if 0<=nextx<m and 0<=nexty<n:
                    q.append((nextx, nexty, left, steps+1))

        return -1

