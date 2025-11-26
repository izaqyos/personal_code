class Solution:

    def addOneBit(self, b1, b2, carry): 
        #print('addOneBit(b1={}, b2={}, carry={})'.format(b1, b2, carry))
        """
        does the equivalent of b1^b2, and then b1&b2 for carry calculation
        return bit, carry
        """
        #pdb.set_trace()
        if  carry == "0":
            if b1 == "0" and b2 == "0":
                return ("0","0")
            elif b1 == "1" and b2 == "1":
                return ("0","1")
            else: 
                return ("1","0")
    
        elif  carry == "1":
            if b1 == "0" and b2 == "0":
                return ("1","0")
            elif b1 == "1" and b2 == "1":
                return ("1","1")
            else: 
                return ("0","1")

    def addBinary(self, a, b):
        """
        input is non empty, and contains only 0,1 chars. no need to validate
        """
        #print('addBinary(a={}, b={})'.format(a,b))
        carry = "0"
        res = ""
        nchar = ""
        i = 0 #index for a 
        shortest = min(len(a), len(b))
        while i<shortest:
            nchar, carry = self.addOneBit(a[len(a) - 1 - i], b[len(b) - 1 - i], carry)
            res = nchar + res
            i = i+1
            
        if len(a) < len (b):
            while i < len(b):
                nchar, carry = self.addOneBit("0" , b[len(b) - 1 - i], carry)
                res = nchar + res
                i = i+1
        else:
            while i < len(a):
                nchar, carry = self.addOneBit("0" , a[len(a) - 1 - i], carry)
                res = nchar + res
                i = i+1

        if carry == "1":
            res = "1" +res

        return res
