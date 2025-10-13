"""
Given two binary strings, return their sum (also a binary string).

The input strings are both non-empty and contains only characters 1 or 0.

Example 1:

Input: a = "11", b = "1"
Output: "100"
Example 2:

Input: a = "1010", b = "1011"
Output: "10101"
"""

class Solution:
    def plusOne(self, digits):
        if len(digits) == 0:
            return digits

        #pdb.set_trace()
        end = len(digits)-1
        while (end >= 0 ):
            if digits[end]< 9:
                digits[end] = digits[end] +1
                return digits
            else:
                digits[end] = 0
            end = end -1
        if digits[0] == 0:
            digits.insert(0,1)
            return digits
        return digits

def test():
    inputs = [ [1,0,1], [], [0,0,1], [9], [9,9,9] ];
    sol = Solution()
    for inp in inputs:
        print('plus one to {}'.format(inp))
        print('is {}'.format(sol.plusOne(inp)))

if __name__ == '__main__':
    test()
        
