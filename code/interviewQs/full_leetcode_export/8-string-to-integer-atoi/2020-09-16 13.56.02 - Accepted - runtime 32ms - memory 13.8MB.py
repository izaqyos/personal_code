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

