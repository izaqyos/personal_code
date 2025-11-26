class cell:
    def __init__(self, right=1, down=1):
        self.right = right
        self.down = down

    def __del__(self):
        pass

    def __str__(self):
        return str(self.right) + ',' + str(self.down)

    
class Solution(object):

    def __init__(self):
        self.board = [[]]
        self.bDebug = False

    def init(self, m, n):
        self.m = m #columns
        self.n = n #rows
        self.board = [[0 for x in range(m)] for y in range(n)]
        self.paths = 0

        for j in range(m):
            for i in range(n):
                if self.bDebug:
                    ("set {0},{1}".format(i, j))
                if j == m - 1:
                    self.board[i][j] = cell(0, 1);
                    if i == n - 1:
                        self.board[i][j] = cell(0, 0);
                elif i == n - 1:
                    self.board[i][j] = cell(1, 0);
                else:
                    self.board[i][j] = cell(1, 1);

    def printBoard(self):
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board]))
        # for j in range(self.m):
        #    for i in range(self.n):
        #        print("[{0},{1}=r:{2},d:{3}]".format(i,j,self.board[i][j].right, self.board[i][j].down))

    def uPathsR(self, i, j):
        if self.bDebug:
            print('uPaths called for ({},{})'.format(i,j))

        if (i == self.n - 1) and (j == self.m - 1):
            self.paths += 1
            if self.bDebug:
                print('uPaths reached end condition. paths={}'.format(self.paths))
            return

        if (j < self.m-1) :#and self.board[i][j].right == 1:
           self.board[i][j].right = 0
           self.uPathsR(i,j+1)

        if (i < self.n -1) :#and self.board[i][j].down == 1:
            self.board[i][j].down = 0
            self.uPathsR(i+1,j)

            # rec on right cell
            # else check down. if 1 rec down cell

    def uniquePaths(self, m, n):
        """
        :type m: int
        :type n: int
        :rtype: int
        """
        self.paths = 0
        self.init(m, n)
        if self.bDebug:
            self.printBoard()
        self.uPathsR(0, 0)
        return self.paths