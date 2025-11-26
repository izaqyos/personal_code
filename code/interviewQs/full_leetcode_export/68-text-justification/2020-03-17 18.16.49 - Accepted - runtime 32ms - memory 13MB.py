from collections import defaultdict
from functools import reduce
import copy

class Solution:
    def __init__(self):
        self.isDebug = False
        """TODO: to be defined. """

    def printLog(self, msgs, kvmap, kvmapWrapChar=''):
        if (self.isDebug):
            kvmapanchor=kvmapWrapChar+'{}={}'+kvmapWrapChar
            print('{} {}'.format(' '.join(msgs), ','.join(kvmapanchor.format(k,v) for k,v in kvmap.items())))

    def _getLen(self, words):
        total = 0
        for w in words:
            total+=len(w)
        return total

    def makeLine(self, words, first, last,  maxWidth, lastLine = False):
        """
        justifiy words left and right. distributes spaces (extra to left)
        if last line justifiy left
        """
        self.printLog(['makeLine()'], {'words': words, 'first': first, 'last':last, 'maxWidth': maxWidth})
        line = ''
        numWords = last - first
        #last line is exempt from this rule
        if lastLine:
            # pdb.set_trace()
             line = ' '.join(words[first:last])+' '*(maxWidth - self._getLen(words[first:last]) - (len(words[first:last])-1))
             return line

        if numWords == 1:
            line+=words[first] + ' '*(maxWidth - len(words[first]))
        else:
            numSpaces=maxWidth - self._getLen(words[first:last])
            spacesPerWord = int( numSpaces / (last -first-1)) #n-1 space slots for n words
            extraSpaces = int( numSpaces  % (last -first-1))
            finalWords = copy.deepcopy(words[first: last])
            i=0
            while extraSpaces > 0:
              finalWords[i] = finalWords[i]+' '  
              extraSpaces-=1;
              i+=1

            #last word is right justified so doesn't get space/s.
            for i in range(len(finalWords)-1): 
                finalWords[i] = finalWords[i] + ' '*spacesPerWord;

            line = ''.join(finalWords)
        self.printLog(['makeLine() return'], {'line': line}, '-')
        return line

    def fullJustify(self, words, maxWidth):
        self.printLog(['fullJustify()'], {'words': words, 'maxWidth': maxWidth})
        
        cwordIdx = 0
        lines = []
        lastLine = False
        while cwordIdx < len(words):
            widthLeft = maxWidth
            first = cwordIdx
            last = cwordIdx 
            current = cwordIdx 
            while current < len(words) and widthLeft - len(words[current]) >= 0: 
                widthLeft = widthLeft - len(words[current]) -1 #we need to reserve space
                current = current +1
            last = current
            cwordIdx = last 
            if current == len(words):
                line = self.makeLine(words, first, last,  maxWidth, True)
            else:
                line = self.makeLine(words, first, last,  maxWidth)
            lines.append(line) 

        return lines

        