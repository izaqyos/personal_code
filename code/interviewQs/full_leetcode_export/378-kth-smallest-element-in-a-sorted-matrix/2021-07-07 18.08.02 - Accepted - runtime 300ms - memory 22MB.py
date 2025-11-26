class Solution:
    def getNext(self, matrix, r, c):
        ret = []
        if c<len(matrix[0])-1:
            right = (matrix[r][c+1], r,c+1)
            ret.append(right)
        if r<len(matrix)-1:
            down = (matrix[r+1][c], r+1, c)
            ret.append(down)
        return ret
    
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        next_steps = []
        import heapq
        current = (matrix[0][0],0,0)
        visited={(0,0)}
        heapq.heappush(next_steps, current)
        steps=0
        
        while steps<k:
            
            v,i,j = heapq.heappop(next_steps)
            steps+=1
            #print(steps,v,i,j)
            if steps==k:
                return v
            nexts = self.getNext(matrix, i, j)
            for n in nexts:
                nv,ni,nj = n
                if not (ni,nj) in visited:
                    heapq.heappush(next_steps, n)
                    visited.add((ni,nj))
        
            