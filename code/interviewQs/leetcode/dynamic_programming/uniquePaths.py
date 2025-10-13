class Solution(object):

    def __init__(self):
        self.board = [[]]
        self.bDebug = True

    def init(self, m, n):
        if self.bDebug:
            print('init({0},{1})'.format(n,n))
        self.m = m #columns
        self.n = n #rows
        self.board = [[0 for x in range(m)] for y in range(n)]
        self.paths = 0

    def printBoard(self):
        print('\n'.join(['\t'.join([str(self.board[i][j]) for j in range(len(self.board[i]))]) for i in range(len(self.board))]))



    def uniquePaths(self, m, n):
        """
        DP solution
        :type m: int
        :type n: int
        :rtype: int
        """
        self.init(m,n)
        if self.bDebug:
            self.printBoard()
        for j in reversed(range(m)):
            for i in reversed(range(n)):
                if (i == n -1) and (j == m-1): #init
                    self.board[i][j] = 1
                if (j < m-1): #can aggregate right going path
                    self.board[i][j] += self.board[i][j+1]
                if (i < n-1): #can aggregate down going path
                    self.board[i][j] += self.board[i+1][j]
                if self.bDebug:
                    print("set [{0},{1}]={2}".format(i, j, self.board[i][j]))

        if self.bDebug:
            self.printBoard()

        return self.board[0][0]
