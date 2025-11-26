from sys import maxsize
from collections import defaultdict
from copy import deepcopy
from functools import reduce

class match:
    def __init__(self, charFreq):
            self.hi = -1
            self.charFreqs = charFreq

class Solution:

    def minWindow(self, s, t):
        def fullMatch(charFreqDict):
            #for v in charFreqDict.values():
            #    if v > 0:
            #        return False
            #return True 
            #Note nice functional alternative
            return all([v <= 0 for v in charFreqDict.values()])

        if len(s) == 0 or len(t) == 0:
            return s
        
        if len(t) > len(s):
            return ''

        minLen = maxsize
        retlmi, rethmi = -1, -1
        tCharFreqs = defaultdict(int) #default factory returns 0, note same as defaultdict(lambda: 0)
        for c in t:
            tCharFreqs[c] += 1 
        
        # matchCharFreqs = deepcopy(tCharFreqs) 

        possibleMatches = dict() # start index to match
        for i,c in enumerate(s):
            if tCharFreqs[c] > 0:
                # add possible match
                mtch = match(deepcopy(tCharFreqs))
                possibleMatches[i] = mtch
                #print('possible match at',i)
                
                # update all matches that c was found
                for index, mtch in possibleMatches.items():
                    if mtch.hi == -1: 
                        mtch.charFreqs[c] -=1 
                        #print('updated match at',index)
                        #print('match char frequency dict', mtch.charFreqs)
                        if fullMatch(mtch.charFreqs): #mark match found
                            mtch.hi = i+1
                            #print('mark match hi',i+1)
                            
                    

        for i, mtch in possibleMatches.items():
            #print('match', s[i:mtch.hi])
            if mtch.hi != -1:
                #print('checking match', s[i:mtch.hi])
                if (mtch.hi -i) <  minLen:
                    minLen = mtch.hi -i
                    retlmi, rethmi = i, mtch.hi

        if minLen < maxsize:
            return s[retlmi: rethmi] 
        else:
            return ""

