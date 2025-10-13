"""
Given a 32-bit signed integer, reverse digits of an integer.

Example 1:

Input: 123
Output: 321
Example 2:

Input: -123
Output: -321
Example 3:

Input: 120
Output: 21
Note:
Assume we are dealing with an environment which could only store integers within the 32-bit signed integer range: [−231,  231 − 1]. For the purpose of this problem, assume that your function returns 0 when the reversed integer overflows.
"""

class Solution:
    def reverse(self, x): 
        ret = 0
        magnitud = 10
        sign = 1
        if x<0:
            sign = -1
            x = sign*x

        ret = x%10
        x = x//10
        while (x!=0):
            ret *= magnitud
            ret += x%10
            x=x//10
        if ret<=(2**31-1) and ret >= (-(2**31)): 
            return ret*sign
        else:
            return 0


        
def test():
    inputs=[123, -123, 0, 59381, -9431, 1247483647, -1247483648 ]
    expected=[321, -321, 0, 18395, -1349, 0, 0]
    sol = Solution()
    for inp,exp in zip(inputs, expected):
        reverse = sol.reverse(inp)
        print('Reversed of {} is {}'.format(inp, reverse))
        assert(exp==reverse)

if __name__ == "__main__":
    test()
