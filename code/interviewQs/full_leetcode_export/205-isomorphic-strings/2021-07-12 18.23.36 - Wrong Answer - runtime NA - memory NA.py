class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        s2t=dict()
        for i in range(len(s)):
            sc=s[i]
            tc=t[i]
            if sc in s2t:
                if tc!=s2t[sc]:
                    return False
            else:
                s2t[sc] = tc
        return True