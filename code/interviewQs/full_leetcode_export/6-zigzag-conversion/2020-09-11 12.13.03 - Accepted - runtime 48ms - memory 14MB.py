class Solution:
    def convert(self, s, numRows):
        if len(s) <= numRows:
            return s
        
        if numRows == 1:
            return s

        direction = 1 #down, -1 up
        cr = 0
        rows = [''] * numRows
        for c in s:
            rows[cr]+=c
            if (direction==1 and cr == numRows-1) or (direction==-1 and cr== 0 ):
                direction*=-1
            cr+=direction

        return ''.join(rows)