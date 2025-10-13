"""
 String to Integer (atoi)
Medium

1736

9973

Add to List

Share
Implement atoi which converts a string to an integer.

The function first discards as many whitespace characters as necessary until the first non-whitespace character is found. Then, starting from this character, takes an optional initial plus or minus sign followed by as many numerical digits as possible, and interprets them as a numerical value.

The string can contain additional characters after those that form the integral number, which are ignored and have no effect on the behavior of this function.

If the first sequence of non-whitespace characters in str is not a valid integral number, or if no such sequence exists because either str is empty or it contains only whitespace characters, no conversion is performed.

If no valid conversion could be performed, a zero value is returned.

Note:

Only the space character ' ' is considered as whitespace character.
Assume we are dealing with an environment which could only store integers within the 32-bit signed integer range: [−231,  231 − 1]. If the numerical value is out of the range of representable values, INT_MAX (231 − 1) or INT_MIN (−231) is returned.
Example 1:

Input: "42"
Output: 42
Example 2:

Input: "   -42"
Output: -42
Explanation: The first non-whitespace character is '-', which is the minus sign.
             Then take as many numerical digits as possible, which gets 42.
Example 3:

Input: "4193 with words"
Output: 4193
Explanation: Conversion stops at digit '3' as the next character is not a numerical digit.
Example 4:

Input: "words and 987"
Output: 0
Explanation: The first non-whitespace character is 'w', which is not a numerical 
             digit or a +/- sign. Therefore no valid conversion could be performed.
Example 5:

Input: "-91283472332"
Output: -2147483648
Explanation: The number "-91283472332" is out of the range of a 32-bit signed integer.
             Thefore INT_MIN (−231) is returned.


"""

class Solution:
    """
strategy:
eat white spaces (' ')
if empty str or just white spaces return 0
first non white space must be either sign or digit
if sign is '-' set sign=-1
for digits use magnitude = 10**i (i starts as 0) multiplier
create num, set sign 
check boundaries according to sign. negative < -(2**31), positive (2**31-1) 
    """
    def myAtoi(self, s):
        ret = 0
        if len(s) == 0:
            return ret

        i = 0
        sign = 1
        while i<len(s): #eat white spaces
            if s[i] == ' ':
                i+=1
            else:
                break

        if i == len(s): #all spaces str
            return 0

        if (s[i] == '+') or (s[i] == '-'):
            if (s[i] == '-'):
                sign *= -1
            i+=1

        if i == len(s): #just +/-
            return 0

        if (ord(s[i]) < ord('0')) or (ord(s[i]) > ord('9')):
            return 0

        
        while i<len(s): #eat leading 0
            if ord(s[i]) == '0':
                i+=1
            else:
                break

        if i == len(s): #just leading 0
            return 0

        magnitude = 10
        while i<len(s): #process number 
            if (ord(s[i]) >= ord('0')) and (ord(s[i]) <= ord('9')):
                ret*=magnitude
                ret += (ord(s[i])-ord('0'))
            else: #trailing non digits. we don't cate
                break
            i+=1
        
        ret *=sign
        if ret < (-1*(2**31)):
            return -1*(2**31)
        
        if ret > (2**31 -1):
            return 2**31 -1

        return ret


def test():
    inputs = [ '0', '000', 'hi 0', ' ', '    ', '',
        '42',
        '0042',
        '-42',
        '4193 with words',
        '-91283472332',
        '2147483648',
        '+',
        '-',
        '+-2'
    ]
    expected = [ 0, 0, 0, 0, 0, 0, 42, 42, -42, 4193, -2147483648, 2147483647 ,0,0,0]

    sol = Solution()
    for inp,exp in zip(inputs, expected):
        num = sol.myAtoi(inp)
        print('atoi of {} is {}'.format(inp, num))
        assert(inp == exp)

if __name__ == "__main__":
    test()
