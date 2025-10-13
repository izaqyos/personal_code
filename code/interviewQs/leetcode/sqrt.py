#!/usr/local/bin/python3

class Solution:
    def mySqrt(self, x):
        """
        log(n), binary search
        """
        if x == 0 or x == 1:
            return x

        ret = x
        high= x
        low = 1
        while (low <= high ):
            candidate = (high + low)//2
            guess = candidate * candidate
            if guess == x:
                return candidate
            elif guess > x:
                high = candidate -1
            else:
                low = candidate +1
                ret = candidate
        
        return ret


    def mySqrtLinear(self, x):
        """
        Compute and return the square root of x, where x is guaranteed to be a non-negative integer.

Since the return type is an integer, the decimal digits are truncated and only the integer part of the result is returned.

Example 1:

Input: 4
Output: 2
Example 2:

Input: 8
Output: 2
Explanation: The square root of 8 is 2.82842..., and since 
             the decimal part is truncated, 2 is returned.
        """

        if x == 0 or x == 1:
            return x

        # optimization
        if x == 2 or x == 3:
            return 1;

        ret = 2

        while True:
            if ret*ret == x:
                return ret
            elif ret*ret > x:
                return ret-1
            else:
                ret+=1
        

def test():
    sol = Solution()
    for x in range(100):
        print('{} sqrt = {}'.format(x, sol.mySqrt(x)))
     
if __name__ == '__main__':
    test()
