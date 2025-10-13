"""
Basic Calculator II
Given a string s which represents an expression, evaluate this expression and return its value. 

The integer division should truncate toward zero.

 

Example 1:

Input: s = "3+2*2"
Output: 7
Example 2:

Input: s = " 3/2 "
Output: 1
Example 3:

Input: s = " 3+5 / 2 "
Output: 5
 

Constraints:

1 <= s.length <= 3 * 105
s consists of integers and operators ('+', '-', '*', '/') separated by some number of spaces.
s represents a valid expression.
All the integers in the expression are non-negative integers in the range [0, 231 - 1].
The answer is guaranteed to fit in a 32-bit integer.
"""

class Solution:
    def calculate(self, s):
        operators = {"+", "-", "*", "/" }
        #digits = { chr(ord('0')+i) for i in range(10)} #more concise with str
        digits = { str(i) for i in range(10)}
        
        
        state = 1 # 0- digits+init, 1-operator. setting it to 1 also disallows leading operator
        nums = [] #hold the numbers ready to be summed so when op is - will add -1*n, when * add m*n etc
        n = 0
        op = '+' #we always have an operator prior to adding a num

        for i in range(len(s)):
            c = s[i]
            if c in digits:
                #we don't enforce no space between digits...
                n= n*10 + int(c)
                state = 0
            if c in operators or i == len(s)-1:
                if state == 0:
                    if op == '+':
                        nums.append(n)
                    if op == '-':
                        nums.append(-1*n)
                    if op == '*':
                        prev = nums.pop()
                        nums.append(prev*n)
                    if op == '/':
                        prev = nums.pop()
                        nums.append(int(prev/n)) 
                    n = 0
                    op = c
                    state = 1
                else: #two consecutive operators 
                    return #

        return sum(nums)


def test():
    inputs = ["3+2*2"," 3/2 ", " 3+5 / 2 ", "1++2", "-1" , "1230+500*4+12/3", "1230+500*4", "500*4", "14-3/2"]
    expected = [7, 1, 5, None, None, 3234, 3230, 2000, 13]

    sol = Solution()
    for i,e in zip(inputs, expected):
        ans = sol.calculate(i)
        print('{}={}'.format(i, ans))
        assert(e == ans)

if __name__ == "__main__":
    test()