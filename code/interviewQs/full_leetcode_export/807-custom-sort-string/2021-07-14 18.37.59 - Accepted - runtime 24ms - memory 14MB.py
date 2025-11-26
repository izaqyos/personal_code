class Solution:
    def customSortString(self, order: str, str: str) -> str:
        ret = ''
        freqs=dict()
        
        for c in str:
            if c in freqs:
                freqs[c]+=1
            else:
                freqs[c]=1
                
        for c in order:
            if c in freqs:
                ret+=c*freqs[c]
            
        for c in str:
            if not c in order:
                ret+=c
                
        return ret
        