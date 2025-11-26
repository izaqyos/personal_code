class Solution:
    def removeDuplicates(self, s: str) -> str:
        if not s or len(s)<2:
            return s
        i=0
        while len(s) > 1 and i<len(s)-1:
            
            if s[i]==s[i+1]:
                s = s[:i]+s[i+2:]
                if i!=0:
                    i-=1
                continue
            i+=1
        return s