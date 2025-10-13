"""
6. ZigZag Conversion
Medium

1823

4894

Add to List

Share
The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)

P   A   H   N
A P L S I I G
Y   I   R
And then read line by line: "PAHNAPLSIIGYIR"

Write the code that will take a string and make this conversion given a number of rows:

string convert(string s, int numRows);
Example 1:

Input: s = "PAYPALISHIRING", numRows = 3
Output: "PAHNAPLSIIGYIR"
Example 2:

Input: s = "PAYPALISHIRING", numRows = 4
Output: "PINALSIGYAHRPI"
Explanation:

P     I    N
A   L S  I G
Y A   H R
P     I

1st idea. brute force.
make n rows. keep state(one of 'down','up'. when down add chars to next row same col
when up. add char to next col, row -1. set the rest of this col to '')

2nd idea.
1st idea is too complex. take into account that adding '' to columns is a noop so just skip it.
Taking this into account we actually only need to fill rows.
so, what is the pattern for adding to rows in loop over s?
rows order: (down) 0, 1, 2, ..., n-1, (up), n-2, n-3, ..., 0 (down), 1, 2, ..., n-1, (up) etc.
so crow starts as 1 (we append to rows[cr-1]....). increment by direction (down+1, up -1) , change direction on (cr)%(n)  == 0

"""
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




def test():
    inputs = [ 
        ('',1),
        ('a',2),
        ('PAYPALISHIRING', 3),
        ('PAYPALISHIRING', 4), 
    ]
    expected = [
        '',
        'a',
        'PAHNAPLSIIGYIR',
        'PINALSIGYAHRPI' 
    ]
    sol = Solution()
    for inp,exp in zip(inputs, expected):
        converted = sol.convert(inp[0], inp[1])
        print('conversion of {} is {}'.format(inp, converted))
        assert(converted==exp)


if __name__ == "__main__":
    test()
        