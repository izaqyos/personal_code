class Solution:
    def matchword(self, board, word, visited, row, column):
        #print('matchword(self, board, word={}, visited, row={}, column={})'.format(word, row, column))

        if word[0] == board[row][column]:
            if len(word) == 1:
                return True
            else:
                visited[row][column] = True
                wrd = word[1:]
                return ((row +1 < len(board)) and (not visited[row+1][column])\
                     and self.matchword(board, wrd, visited,row+1, column))\
                    or ((row > 0) and (not visited[row-1][column])\
                        and self.matchword(board, wrd, visited,row-1, column))\
                    or ( (column +1 < len(board[0])) and (not visited[row][column+1])\
                         and self.matchword(board, wrd, visited,row, column+1) )\
                    or ((column > 0) and (not visited[row][ column-1])\
                         and self.matchword(board, wrd, visited,row, column-1)) 
        else:
            return False
        
    def exist(self, board, word):
        if len(board) == 0 or len(board[0]) == 0 or len(word) == 0:
            return False

        visited = [ [False for j in board[0]] for i in board]
        for i in range(len(board)):
            for j in range(len(board[0])):
                match = self.matchword(board, word, visited, i, j)
                if match:
                    return True
        return False