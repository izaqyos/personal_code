"""
Determine whether an integer is a palindrome. An integer is a palindrome when it reads the same backward as forward.

Example 1:

Input: 121
Output: true
Example 2:

Input: -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
Example 3:

Input: 10
Output: false
Explanation: Reads 01 from right to left. Therefore it is not a palindrome.
"""

class Solution:
    def isPalindrome(self, x):
        """
        if <0 retrun False. there's a - prefix only...
        rebuild the num from the end if its same as original then its a pali
        """
        if x<0:
            return False

        if x == 0:
            return True
        
        xcopy = x
        nx = 0
        magnitute = 10
        while xcopy > 0:
            d = xcopy % 10
            xcopy //= 10
            nx*=magnitute
            nx+=d
        
        return nx == x


        return True

def test():
    inputs = [121, -121, 10, 1, 33, 5432345, 54323345]
    expected = [True, False, False, True, True, True, False ]
    sol = Solution()
    for inp, exp in zip(inputs, expected):
        res = sol.isPalindrome(inp)
        print('{} palindrome test {}'.format(inp, res))
        assert (res == exp)

if __name__ == "__main__":
    test()        