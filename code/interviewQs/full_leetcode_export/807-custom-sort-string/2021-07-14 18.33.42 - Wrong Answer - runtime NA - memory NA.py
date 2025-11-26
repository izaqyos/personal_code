class Solution:
    def customSortString(self, order: str, str: str) -> str:
        ret = ''
        rightside=''
        freqs=dict()
        
        for c in str:
            if c in freqs:
                freqs[c]+=1
            else:
                freqs[c]=1
                
        for c in order:
            if c in freqs:
                ret+=c*freqs[c]
            else:
                rightside+=c
                
        return ret+rightside
        