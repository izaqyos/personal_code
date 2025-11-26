class Solution:
    def minFlipsMonoIncrR(self, s: str, i: int) -> int:
        if i>=len(s)-1:
            return 0
        s1 = s[:]
        c = s[i]
        print('recurse to', s1, i+1)
        flips = self.minFlipsMonoIncrR(s1, i+1)
        if c=="1" and s[i+1]=="0":
            s1 = s1[:i]+"0"+s1[i+1:]
            print(s1)
            return flips+1
        
        return flips
        
    def minFlipsMonoIncr(self, s: str) -> int:
        ones, zeros2bflipped = 0,0
        for c in s:
            if c=="0":
                zeros2bflipped+=1 #0 to b flipped
            else:
                ones+=1 # count 1 bits. 
            zeros2bflipped = min(zeros2bflipped, ones) #we take min between 1 flipped to 0 and 0 flipped to 1
        return zeros2bflipped
        