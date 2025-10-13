"""

Given a string S and a string T, find the minimum window in S which will contain all the characters in T in complexity O(n).

Example:

Input: S = "ADOBECODEBANC", T = "ABC"
Output: "BANC"
Note:

If there is no such window in S that covers all characters in T, return the empty string "".
If there is such window, you are guaranteed that there will always be only one unique minimum window in S.

Idea:
Keep to dictionaries of T chars freq. one as readonly and a second copy for running match candidate
scan S, keep track of i, lmi, hmi which are running index, low match index and high match index
lmi hmi start as -1
for each char if it is in T match dict if lmi is -1 set to i, update counter, check if full match,etc..
"""

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



def test():
    inps = [ ['', 'a'], ['abc', ''], ['ADOBECODEBANC', 'ABC'], ['helloyossi','lsil'], ['bcccab','ba' ]]
    expected = ['', 'abc', 'BANC', 'lloyossi', 'ab']
    sol = Solution()
    for inp,exp in zip(inps, expected):
        print('check min window substr of {} in {}'.format(inp[1], inp[0]))
        minsubstr = sol.minWindow(inp[0], inp[1])
        print('min windows substr is', minsubstr)
        #assert( minsubstr == exp)

if __name__ == '__main__':
    test()
        