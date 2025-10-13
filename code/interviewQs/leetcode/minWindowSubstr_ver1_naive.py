from sys import maxsize
from collections import defaultdict
from copy import deepcopy

class Solution:

    def minWindow(self, s, t):
        def fullMatch(charFreqDict):
            #for v in charFreqDict.values():
            #    if v > 0:
            #        return False
            #return True 
            #Note nice functional alternative
            return all([v == 0 for v in charFreqDict.values()])

        if len(s) == 0 or len(t) == 0:
            return s
        
        if len(t) > len(s):
            return ''

        minLen = maxsize
        lmi, hmi, retlmi, rethmi = -1, -1, -1, -1
        tCharFreqs = defaultdict(int) #default factory returns 0, note same as defaultdict(lambda: 0)
        for c in t:
            tCharFreqs[c] += 1 
        matchCharFreqs = deepcopy(tCharFreqs) 

        for i,c in enumerate(s):
            if matchCharFreqs[c] > 0:
                if lmi == -1:
                    lmi = i #start match
                
                matchCharFreqs[c] -= 1
                if fullMatch(matchCharFreqs): #end match
                    hmi = i+1
                    if (hmi-lmi) < minLen:
                        minLen = hmi - lmi 
                        retlmi, rethmi = lmi, hmi
                        lmi, hmi = -1, -1 #prep for next match
                        matchCharFreqs = deepcopy(tCharFreqs)
        if minLen < maxsize:
            return s[retlmi: rethmi] 
        else:
            return ""
