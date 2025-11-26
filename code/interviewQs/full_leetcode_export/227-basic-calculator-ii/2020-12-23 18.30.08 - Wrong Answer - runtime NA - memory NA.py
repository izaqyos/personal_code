class Solution:
    def calculate(self, s):
        operators = {"+", "-", "*", "/" }
        #digits = { chr(ord('0')+i) for i in range(10)} #more concise with str
        digits = { str(i) for i in range(10)}
        
        
        state = 1 # 0- digits+init, 1-operator. setting it to 1 also disallows leading operator
        nums = [] #hold the numbers ready to be summed so when op is - will add -1*n, when * add m*n etc
        n = 0
        op = '+' #we always have an operator prior to adding a num

        for i in range(len(s)):
            c = s[i]
            if c in digits:
                #we don't enforce no space between digits...
                n= n*10 + int(c)
                state = 0
            if c in operators or i == len(s)-1:
                if state == 0:
                    if op == '+':
                        nums.append(n)
                    if op == '-':
                        nums.append(-1*n)
                    if op == '*':
                        prev = nums.pop()
                        nums.append(prev*n)
                    if op == '/':
                        prev = nums.pop()
                        nums.append(prev//n) 
                    n = 0
                    op = c
                    state = 1
                else: #two consecutive operators 
                    return #

        return sum(nums)