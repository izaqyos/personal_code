class Solution:
    def plusOne(self, digits):
        if len(digits) == 0:
            return digits

        #pdb.set_trace()
        end = len(digits)-1
        while (end >= 0 ):
            if digits[end]< 9:
                digits[end] = digits[end] +1
                return digits
            else:
                digits[end] = 0
            end = end -1
        if digits[0] == 0:
            digits.insert(0,1)
            return digits
        return digits
