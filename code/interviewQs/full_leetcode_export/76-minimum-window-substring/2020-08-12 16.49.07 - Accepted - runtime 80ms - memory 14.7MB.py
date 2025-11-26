from sys import maxsize

class Solution:

    def minWindow(self, s, t):

        if len(s) == 0 or len(t) == 0:
            return s
        
        if len(t) > len(s):
            return ''

        minLen = maxsize
        left = 0
        found = 0
        sRet = ""
        tCharFreqs = {} #match dictionary. 
        for c in t:
            if c in tCharFreqs:
                tCharFreqs[c] += 1 
            else:
                tCharFreqs[c] = 1

        for i,c in enumerate(s):
            if c in tCharFreqs:
                if tCharFreqs[c] > 0: #only contributes to found if seen up to tCharFreqs[c] times
                    found +=1
                tCharFreqs[c] -= 1 #extra matching chars 

            while found == len(t): #found match, now move left index to skip non match chars
                if (i - left +1) < minLen:
                    sRet = s[left: i+1]
                    minLen = i-left+1

                if s[left] in tCharFreqs: 
                    tCharFreqs[s[left]] += 1  #when we move forward, 'unsee' s[left] char
                    if tCharFreqs[s[left]] > 0: #now we no longer have a match.  
                        found -= 1
                left+=1
        return sRet

