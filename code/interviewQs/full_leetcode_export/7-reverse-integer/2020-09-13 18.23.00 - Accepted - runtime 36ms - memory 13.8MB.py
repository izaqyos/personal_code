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