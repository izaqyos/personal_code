#!/usr/local/bin/python3

from random import randint
import numpy as np

"""
Problem Description:
You are in charge of preparing a recently purchased lot for one of a new building. The lot is covered with trenches and has a single obstacle that needs to be taken down before the foundation can be prepared for the building. The demolition robot must remove the obstacle before progress can be made on the building. Write an algorithm to determine the minimum distance required for the demolition robot to remove the obstacle.
Assumptions:
1. The lot is flat, except for trenches, and can be represented as a 2-D grid.
2. The demolition robot must start from the top left corner of the lot, which is always flat and can move one block up, down, right or left at a time.
3. The demolition robot cannot enter trenches and cannot leave the lot.
4. The flat areas are represented as 1, areas with trenches as 0 and obstacle by 9.
Output:
Return an integer representing the minimum distance traversed to remove the obstacle else return -1.
"""

def genGrid(size, obstPrcent = 20):
    """
    will generate a sizeXsize grid.
    w/ a precentage of randomly placed trenches
    w/ a random location of an obstacle
    """

    if (obstPrcent < 0) or(obstPrcent > 100):
        obstPrcent = 20 #default to 20 percent

    if (size == 0):
        return []
    if (size == 1):
        return [[9]]

    lot = [ [1 for _ in range(size)] for _ in range(size)]
    for i in range( size*size*obstPrcent//100):
        x,y = randint(0,size-1), randint(0,size-1)
        lot[x][y] = 0 #add trench

    lot[randint(0,size-1)][randint(0,size-1)] = 9
    return lot

def neighbors(i,j, m,n):
    """
    util, return list of indices for valid cells, up/down/right/left in matrix
    boundary
    """
    ret = []
    if i>0: #up
        ret.append((i-1,j))

    if i<m-1: #down
        ret.append((i+1,j))

    if j>0: #left
        ret.append((i,j-1))
    if j<n-1: #right
        ret.append((i,j+1))

    #print('neighbors ret={}'.format(ret))
    return ret

def clearObstacle(matrix):
    """
    BFS search for obstacle.
    space complexity o(log(m*n)) , for max size of Q 
    time complexty o(m*n)
    use list as Q, performance hit and pop() (o(n)) vs deque popleft (o(1))
    """

    m = len(matrix)
    if m == 0:
        return -1

    n = len(matrix[0])
    #q,visited = [(0,0,0)] , {(0,0)} #classic BFS uses visited set. here we can use a simpler bool matrix
    q= [(0,0,0)]
    visited = [ [False for _ in range(n)] for _ in range(m) ]
    visited[0][0] = True
    path = [] #in 2nd phase impl I'll pass path on Q (making curr cell the right most cell) and then print it
    dist = 0

    #print('grid dims {}X{}, \nvisited matrix=\n{} \ndist={}, Q={}'.format(m,n,np.matrix(visited), dist, q))
    while len(q) > 0:
        i,j,dist = q.pop(0)
        #print('at cell ({},{}), dist {}'.format(i,j,dist))
        if (matrix[i][j] == 9):
            return dist

        for indices in neighbors(i, j, m, n):
            x,y = indices
            if (matrix[x][y] != 0) and (not visited[x][y]):
                q.append((x,y, dist+1))
                visited[x][y] = True

    return -1

def clearObstacleDeque(matrix):
    """
    BFS search for obstacle.
    space complexity o(log(m*n)) , for max size of Q 
    time complexty o(m*n)
    use deque as Q, also calculate and plot path
    """

    from collections import deque
    m = len(matrix)
    if m == 0:
        return -1

    n = len(matrix[0])
    #q,visited = [(0,0,0)] , {(0,0)} #classic BFS uses visited set. here we can use a simpler bool matrix
    q= deque()
    q.append([(0,0)]) #append current path, dist is len(path) -1
    visited = [ [False for _ in range(n)] for _ in range(m) ]
    visited[0][0] = True

    #print('grid dims {}X{}, \nvisited matrix=\n{} \ndist={}, Q={}'.format(m,n,np.matrix(visited), dist, q))
    while len(q) > 0:
        path = q.popleft()
        i,j = path[-1]
        #print('at cell ({},{}), dist {}'.format(i,j,dist))
        if (matrix[i][j] == 9):
            print('path to obstacle is: {}'.format(path))
            return len(path)-1

        for indices in neighbors(i, j, m, n):
            x,y = indices
            if (matrix[x][y] != 0) and (not visited[x][y]):
                new_path = path[:]
                new_path.append((x,y))
                q.append(new_path)
                visited[x][y] = True

    return -1

def test():
    #mat10 = genGrid(10)
    #print(np.matrix(mat10))
    grids = [ genGrid(i) for i in range(15) ]

    print('randomly generated lots:')
    for grid in grids:
        print('-'*100, '\n')
        print(np.matrix(grid))
        print('min dist is: ', clearObstacleDeque(grid))
        #print('min dist is: ', clearObstacle(grid))
        print('-'*100, '\n')

    

if __name__ == '__main__':
    test()

