
from collections import deque

def isValid(m,n,i,j):
    return ( (0<=i) and (i<m)) and ( (0<=j) and (j<n) ) 

def findPath(maze):
    if (len(maze) ==0) or (len(maze[0])==0):
        return -1

    m = len(maze)
    n = len(maze[0])
    if (not maze[0][0]) or (not maze[m-1][n-1]):
        return -1
    visited = [ [ False for j in maze[0]] for i in maze]
    neigbors = [(1,0), (-1, 0), (0,1), (0,-1)]
    q = deque()
    q.append((0,0,0)) #i,j, pathlen
    
    while (len(q) > 0):
        i,j,length = q.popleft()
        if (i==m-1) and (j==n-1):
            return length
        visited[i][j] = True
        for neigbor in neigbors:
            k = i+neigbor[0]
            l = j+neigbor[1] 
            if isValid(m,n,k,l) and (not visited[k][l]) and maze[k][l]:
                q.append((k,l, length+1))
    return -1



def printMatrix(matrix):
    for line in matrix:
        for i, elem in enumerate(line):
            if i == len(line) -1:
                print(elem)
            else:
                print(str(elem)+',', end='')
def test():
    maze = []
    maze.append([True, True, False, False, False])
    maze.append([True, True, False, False, True])
    maze.append([True, False, True, True, True])
    maze.append([True, True, True, False, True])
    printMatrix(maze)
    length = findPath(maze)
    print('path length',length)

    maze = []
    maze.append([False, True, False, False, False])
    maze.append([True, True, False, False, True])
    maze.append([True, False, True, True, True])
    maze.append([True, True, True, False, True])
    printMatrix(maze)
    length = findPath(maze)
    print('path length',length)

    maze = []
    maze.append([False, True, False, False, False])
    maze.append([True, True, False, False, True])
    maze.append([True, False, True, True, True])
    maze.append([True, True, True, False, False])
    printMatrix(maze)
    length = findPath(maze)
    print('path length',length)

    maze = []
    maze.append([True, True, True, True, True])
    maze.append([True, True, False, False, True])
    maze.append([True, False, True, True, True])
    maze.append([True, True, True, False, True])
    printMatrix(maze)
    length = findPath(maze)
    print('path length',length)

    maze = []
    maze.append([True, True, True, True, True])
    maze.append([True, True, False, False, True])
    maze.append([True, False, True, False, False])
    maze.append([True, True, True, False, True])
    printMatrix(maze)
    length = findPath(maze)
    print('path length',length)
    
   

    
   

    
   

    
   

if __name__ == "__main__":
    test()