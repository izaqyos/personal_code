
from collections import deque

def isValid(m,n,i,j):
    return ( (0<=i) and (i<m)) and ( (0<=j) and (j<n) ) 

def findPath(maze):
    """
    0 is free
    1 obstacle
    return the shortest path from (0,0) to (m-1,n-1)
    will use a dictionary from cells to parents for backtrack in order to calculate the path
    will use BFS since it has the trait that it expands by distance from root so when getting to target it's guaranteed to be shortest path 
    """
    if (len(maze) ==0) or (len(maze[0])==0) or (maze[0][0] == 1): #empty matrix, 1d list, block on 1st cell -> return no path
        return []

    m = len(maze)
    n = len(maze[0])
    if  (maze[m-1][n-1] == 1): #target blocked -> return no path
        return []

    visited = [ [ False for j in maze[0]] for i in maze]
    neigbors = [(1,0), (-1, 0), (0,1), (0,-1)]
    q = deque()
    # q.append((0,0,0)) #i,j, pathlen
    q.append((0,0)) # no need to push path len since we will reconstruct path by backtracking, then just take it length...
    parents = {}
    parents[(0,0)] = None
    shortest = []
    
    while (len(q) > 0):
        i,j = q.popleft()

        if (i==m-1) and (j==n-1):
            cur = (m-1, n-1)
            while cur!=None:
                shortest.append(cur)
                cur = parents[cur]
            return shortest[::-1] #reverse list can also be done by poping until its empty to a new list

        visited[i][j] = True
        for neigbor in neigbors:
            k = i+neigbor[0]
            l = j+neigbor[1] 
            if isValid(m,n,k,l) and (maze[k][l] == 0) and (not visited[k][l]):
                q.append((k,l))
                parents[(k,l)] = (i,j)
    return []



def printMatrix(matrix):
    for line in matrix:
        for i, elem in enumerate(line):
            if i == len(line) -1:
                print(elem)
            else:
                print(str(elem)+',', end='')

def test():
    maze = []
    maze.append([0, 0, 1, 1, 1])
    maze.append([0, 0, 1, 1, 0])
    maze.append([0, 1, 0, 0, 0])
    maze.append([0, 0, 0, 1, 0])
    printMatrix(maze)
    path = findPath(maze)
    print('path ',path)

    maze = []
    maze.append([1, 0, 1, 1, 1])
    maze.append([0, 0, 1, 1, 0])
    maze.append([0, 1, 0, 0, 0])
    maze.append([0, 0, 0, 1, 0])
    printMatrix(maze)
    path = findPath(maze)
    print('path ',path)

    maze = []
    maze.append([1, 0, 1, 1, 1])
    maze.append([0, 0, 1, 1, 0])
    maze.append([0, 1, 0, 0, 0])
    maze.append([0, 0, 0, 1, 1])
    printMatrix(maze)
    path = findPath(maze)
    print('path ',path)

    maze = []
    maze.append([0, 0, 0, 0, 0])
    maze.append([0, 0, 1, 1, 0])
    maze.append([0, 1, 0, 0, 0])
    maze.append([0, 0, 0, 1, 0])
    printMatrix(maze)
    path = findPath(maze)
    print('path ',path)

    maze = []
    maze.append([0, 0, 0, 0, 0])
    maze.append([0, 0, 1, 1, 0])
    maze.append([0, 1, 0, 1, 1])
    maze.append([0, 0, 0, 1, 0])
    printMatrix(maze)
    path = findPath(maze)
    print('path ',path)
    
   

    
   

    
   

    
   

if __name__ == "__main__":
    test()