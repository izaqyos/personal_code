class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        c2freq=dict()
        for c in text:
            if c in c2freq:
                c2freq[c]+=1
            else:
                c2freq[c]=1
        if 'b' in  c2freq and 'a' in  c2freq and 'n' in  c2freq and 'l' in  c2freq and 'o' in  c2freq:
            return min(c2freq['b'], c2freq['a'], c2freq['n'],c2freq['l']//2, c2freq['o']//2 )
        else:
            return 0
        