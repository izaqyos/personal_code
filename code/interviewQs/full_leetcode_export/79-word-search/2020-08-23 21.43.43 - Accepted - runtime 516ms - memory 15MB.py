class Solution:
    def verifyPosition(self, board, word, windex, row, column):
        return row>=0 and row<len(board)\
            and column>=0 and column<len(board[0])\
            and windex<len(word) and (word[windex] == board[row][column])

    def matchword(self, board, word, windex, row, column):
        if len(word) == windex: #at this point we matched the whole word
            return True
        #print('matchword(self, board, word[{}]={}, visited, row={}, column={})'.format(windex, word[windex], row, column))
        directons = [(1,0), (0,1), (-1, 0), (0,-1)] 

        if not self.verifyPosition(board, word, windex, row, column ):
            return False
            
        prev = board[row][column]
        board[row][column] = ' ' #words don't contain space 
        ret = False
        for direction in directons:
            ret = ret or self.matchword(board, word, windex+1, row+direction[0], column+direction[1])
        
        board[row][column] = prev
        return ret
        
    def exist(self, board, word):
        if len(board) == 0 or len(board[0]) == 0 or len(word) == 0:
            return False

        for i in range(len(board)):
            for j in range(len(board[0])):
                match = self.matchword(board, word, 0, i, j)
                if match:
                    return True
                
        return False