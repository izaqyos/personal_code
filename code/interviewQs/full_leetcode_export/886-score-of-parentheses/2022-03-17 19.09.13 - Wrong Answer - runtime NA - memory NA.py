class Solution:
    def scoreOfParentheses(self, s: str) -> int:
        i,total, cnt = 0,0,0
        
        while i<len(s):
            c= s[i]
            i+=1
            if c =='(':
                total +=cnt
                cnt=0
                continue
            if cnt == 0:
                cnt =1
            else:
                cnt*=2
        total+=cnt
        return total
 
        