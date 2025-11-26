from collections import defaultdict

class Solution:
    digits = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    sign_chars = {'-', '+' }
    other_chars = {'e', '.', }
    special_chars =  other_chars | sign_chars
    allowedChars = digits | special_chars
    def isNumber(self, inp):
        start = 0
        end = len(inp)-1
        while start<=end and inp[start] == ' ':
            start = start+1
        while end>=start and inp[end] == ' ':
            end = end-1

        found_e=found_dot=found_sign=found_digit=False

        index = start
        while ( index <= end):
            if (inp[index] in self.digits):
                found_digit = True 
            elif (inp[index] in self.sign_chars):
                if found_digit or found_sign or found_dot:
                    return False
                found_sign = True
            elif (inp[index] in '.'):
                if found_dot or found_e:
                    return False
                found_dot = True
            elif  (inp[index] in 'e'):
                if found_e or not found_digit:
                    return False
                found_e = True 
                found_digit = found_sign = found_dot = False
            else:
                return False

            index = index +1

        return found_digit
