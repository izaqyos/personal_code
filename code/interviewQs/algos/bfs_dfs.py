#from collections import defaultdict
from collections import deque

class Graph:
    def __init__(self):
        self.graph = dict()
        #self.graph = defaultdict(set)
    
    def addEdge(self, v, u):
        if v in self.graph:
            if not (u in self.graph[v]):
                self.graph[v].add(u)
        else:
            self.graph[v] = {u}
        if u in self.graph:
            if not (v in self.graph[u]):
                self.graph[u].add(v)
        else:
            self.graph[u] = {v}

# Note that BFS by nature will always find the shortest path from root to any node by edge count
# if edges were weighted then for min path we would have needed to keep tabs of path weithts 
    def bfspath(self, r, cb):
        q = deque()
        q.append((r, [r]))
        visited = {r}

        while len(q)>0:
            (c, path) = q.popleft()
            cb((c,path))
            #print('node: {}. path: {}'.format(c, path))

            for neigh in self.graph[c]:
                if not neigh in visited:
                    visited.add(neigh)
                    npath = path[:]
                    npath.append(neigh)
                    q.append((neigh, npath ))

    def bfs(self, r, cb):
        q = deque()
        q.append(r)
        visited = {r}

        while len(q)>0:
            c = q.popleft()
            cb(c)
            for neigh in self.graph[c]:
                if not neigh in visited:
                    visited.add(neigh)
                    q.append(neigh)

    def dfs(self, r, cb):
        s = [(r, [r])]  #use list for stack. node, path tuple
        visited = {r}

        while len(s) > 0:
            c,path = s.pop()
            cb((c, path))
            for neigh in self.graph[c]:
                if not neigh in visited:
                    visited.add(neigh)
                    npath = path[:]
                    npath.append(neigh) 
                    s.append((neigh, npath))

    def dfsR(self, r, cb):
        visited = {r}
        self.dfsRInner(r, visited, cb)

    def dfsRInner(self, r, visited , cb):
        cb(r)
        for neigh in self.graph[r]:
            if not neigh in visited:
                visited.add(neigh)
                self.dfsRInner(neigh, visited, cb)


# practice section
    def bfs1(self, r, cb):
        q = deque()
        visited = {r}
        q.append(r)
        while q:
            c = q.popleft()
            cb(c)
            for n in self.graph[c]:
                if not (n in visited):
                    visited.add(n)
                    q.append(n)

    def dfsr1(self, r, cb):
        def dfsrr1(r,cb, visited):
            cb(r)
            for n in self.graph[r]:
                if not n in visited:
                    visited.add(n)
                    dfsrr1(n,cb,visited)
        visited = {r}
        dfsrr1(r, cb, visited)

    def dfs1(self, r, cb):
        s = deque() #faster than list
        s.append(r)
        visited = {r}
        while s:
            c = s.pop()
            cb(c)
            for n in self.graph[c]:
                if not n in visited:
                    s.append(n)
                    visited.add(n)


# practice section

        


    def printme(self):
        nodes = list(self.graph.keys())

        print('non recursive bfs:')
        self.bfs(nodes[0], lambda x: print(x, ' '))
        print('non recursive bfs, plus path:')
        self.bfspath(nodes[0], lambda x: print(x, ' '))
        print('recursive dfs:')
        self.dfsR(nodes[0],  lambda x: print(x, ' '))
        print('non recursive dfs:')
        self.dfs(nodes[0],  lambda x: print(x, ' '))
        print('practice ---')
        print('simple bfs')
        self.bfs1(nodes[0],  lambda x: print(x, ' '))
        print('simple dfs')
        self.dfs1(nodes[0],  lambda x: print(x, ' '))
        print('simple recursive dfs')
        self.dfsr1(nodes[0],  lambda x: print(x, ' '))
        print('practice ---')

def test_graph():
    g = Graph()
    g.addEdge('a', 'b')
    g.addEdge('a', 'c')
    g.addEdge('a', 'd')
    g.addEdge('b', 'd')
    g.addEdge('b', 'e')
    g.addEdge('e', 'f')
    g.printme()

def shortest_path(mtx):
    #0-clear. 1 - blocked
    def neighbors(i,j):
        possible = [(1,0), (0,1), (-1,0), (0,-1)] 
        neighbors = []
        for l,m in possible:
            if (i+l>=0) and  (i+l <len(mtx)) and (j+m>=0) and  (j+m<len(mtx[0])):
                if mtx[i+l][j+m] == 0:
                    neighbors.append((i+l, j+m))
        print(neighbors)
        return neighbors
            
    if (len(mtx) == 0) or len(mtx[0]) ==0 or (mtx[0][0] == 1) or (mtx[len(mtx)-1][len(mtx[0])-1] == 1):
        return -1
    visited = {(0,0)}
    q = deque()
    pathLen =  0
    q.append(((0,0), pathLen))
    m = len(mtx)
    n = len(mtx[0])
    while q:
        c,pathLen = q.popleft()
        if c == (m-1, n-1):
            return pathLen
        else:
            for neighbor in neighbors(*c):
                if neighbor not in visited :
                    q.append((neighbor, pathLen+1)) 
                    visited.add(neighbor)
    return -1



def test_matrix():
    matrix = [
            [0,0,0,0],
            [0,1,0,1],
            [0,1,0,0],
            [1,0,0,0]
            ]
    pathLen = shortest_path(matrix)
    print("calculate shortest path len of matrix", matrix)
    print("path len", pathLen)

if __name__ == "__main__":
    test_graph()
    test_matrix()
        

