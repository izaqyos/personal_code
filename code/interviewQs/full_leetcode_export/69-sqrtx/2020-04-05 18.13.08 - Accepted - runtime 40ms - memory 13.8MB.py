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