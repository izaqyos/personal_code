"""
Write a function that takes an unsigned integer and returns the number of '1' bits it has (also known as the Hamming weight).

Note:

Note that in some languages such as Java, there is no unsigned integer type. In this case, the input will be given as a signed integer type. It should not affect your implementation, as the integer's internal binary representation is the same, whether it is signed or unsigned.
In Java, the compiler represents the signed integers using 2's complement notation. Therefore, in Example 3 above, the input represents the signed integer. -3.
Follow up: If this function is called many times, how would you optimize it?

can also do it o(num of 1 bits)
class Solution:
    def hammingWeight(self, n: int) -> int:
        num1bits = 0
        while n&n-1:
            num1bits+=1
        return num1bits

"""

class Solution:
    def hammingWeight(self, n: int) -> int:
        num1bits = 0
        while n>0:
            if n&1:
                num1bits+=1
            n>>=1
        return num1bits

def test():
    nums = [0,1,3, 2**31-1]
    sol = Solution()
    for n in nums:
        n1b = sol.hammingWeight(n)
        print('hamming weight of {} is {}'.format(n, n1b))
    
if __name__ == '__main__':
    test()


