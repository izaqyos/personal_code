"""
 Integer to Roman
Medium

1222

2747

Add to List

Share
Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.

Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
For example, two is written as II in Roman numeral, just two one's added together. Twelve is written as, XII, which is simply X + II. The number twenty seven is written as XXVII, which is XX + V + II.

Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:

I can be placed before V (5) and X (10) to make 4 and 9. 
X can be placed before L (50) and C (100) to make 40 and 90. 
C can be placed before D (500) and M (1000) to make 400 and 900.
Given an integer, convert it to a roman numeral. Input is guaranteed to be within the range from 1 to 3999.

Example 1:

Input: 3
Output: "III"
Example 2:

Input: 4
Output: "IV"
Example 3:

Input: 9
Output: "IX"
Example 4:

Input: 58
Output: "LVIII"
Explanation: L = 50, V = 5, III = 3.
Example 5:

Input: 1994
Output: "MCMXCIV"
Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.
"""

class Solution:
    def intToRoman(self, num):
        digits = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
        tens = ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC']
        hundreds = ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM']
        thousands = ['', 'M', 'MM', 'MMM'] #max input 3999
        ret = ''
        power = 0
        while num>0:
            cur = num%10
            num//=10
            if power == 0:
                ret = digits[cur] 
            elif power == 1:
                ret = tens[cur]+ret
            elif power == 2:
                ret = hundreds[cur]+ret
            elif power == 3:
                ret = thousands[cur]+ret
            else:
                print('unexpected input')
                return 0
            power+=1
        return ret
            

            


def test():
    inputs = [1, 4, 9, 10, 19, 40, 99, 400, 652, 1549, 3999]
    expected =[ 'I', 'IV', 'IX', 'X', 'XIX', 'XL', 'XCIX', 'CD', 'DCLII', 'MDXLIX', 'MMMCMXCIX']
    sol = Solution()
    for inp,exp in zip(inputs, expected):
        roman = sol.intToRoman(inp)
        print('int to roman. {}={}'.format(inp, roman))
        assert(roman == exp)

if __name__ == "__main__":
    test()
        