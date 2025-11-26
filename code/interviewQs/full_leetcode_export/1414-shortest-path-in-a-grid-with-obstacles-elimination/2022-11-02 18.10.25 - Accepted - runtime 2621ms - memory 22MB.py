
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
