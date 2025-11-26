class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        s2t=dict()
        t2s=dict()
        for i in range(len(s)):
            sc=s[i]
            tc=t[i]
            
            if (sc in s2t) or (tc in t2s) :
                if sc in s2t and tc!=s2t[sc]:
                    return False
                if tc in t2s and t2s[tc]!=sc:
                    return False
            else:
                t2s[tc] = sc
                s2t[sc] = tc
        return True