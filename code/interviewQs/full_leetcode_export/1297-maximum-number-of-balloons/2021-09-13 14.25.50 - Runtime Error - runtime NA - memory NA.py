class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        c2freq=dict()
        for c in text:
            if c in c2freq:
                c2freq[c]+=1
            else:
                c2freq[c]=1
        return min(c2freq['b'], c2freq['a'], c2freq['n'],c2freq['l']//2, c2freq['o']//2 )
        