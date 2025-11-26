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