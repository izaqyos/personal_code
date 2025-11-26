class Solution:
    def convertToInt(self, n: str):
        ret = 0
        ordenance = 1
        while n:
            c = n[-1]
            d = int(c)
            n = n[:-1]
            ret +=d*ordenance
            ordenance*=10
        return ret
    
    def convertToStr(self, n: int):
        ret=""
        while n:
            d = n%10
            n //= 10
            ret=str(d)+ret
        if ret:
            return ret
        else:
            return "0"
    
    def addStrings(self, num1: str, num2: str) -> str:
        n1 = self.convertToInt(num1)
        n2 = self.convertToInt(num2)
        n = n1+n2
        return self.convertToStr(n)