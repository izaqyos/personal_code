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