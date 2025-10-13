#!/usr/local/bin/python3
"""
Text Justification

Given an array of words and a width maxWidth, format the text such that each line has exactly maxWidth characters and is fully (left and right) justified.

You should pack your words in a greedy approach; that is, pack as many words as you can in each line. Pad extra spaces ' ' when necessary so that each line has exactly maxWidth characters.

Extra spaces between words should be distributed as evenly as possible. If the number of spaces on a line do not divide evenly between words, the empty slots on the left will be assigned more spaces than the slots on the right.

For the last line of text, it should be left justified and no extra space is inserted between words.

Note:

A word is defined as a character sequence consisting of non-space characters only.
Each word's length is guaranteed to be greater than 0 and not exceed maxWidth.
The input array words contains at least one word.
Example 1:

Input:
words = ["This", "is", "an", "example", "of", "text", "justification."]
maxWidth = 16
Output:
[
   "This    is    an",
   "example  of text",
   "justification.  "
]
Example 2:

Input:
words = ["What","must","be","acknowledgment","shall","be"]
maxWidth = 16
Output:
[
  "What   must   be",
  "acknowledgment  ",
  "shall be        "
]
Explanation: Note that the last line is "shall be    " instead of "shall     be",
             because the last line must be left-justified instead of fully-justified.
             Note that the second line is also left-justified becase it contains only one word.
Example 3:

Input:
words = ["Science","is","what","we","understand","well","enough","to","explain",
         "to","a","computer.","Art","is","everything","else","we","do"]
maxWidth = 20
Output:
[
  "Science  is  what we",
  "understand      well",
  "enough to explain to",
  "a  computer.  Art is",
  "everything  else  we",
  "do                  "
]
"""

from collections import defaultdict
from functools import reduce
import copy
import pdb

class Solution():

    """Docstring for MyClass. """

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

def test():
    words_maxW_list = [
            (["Science","is","what","we","understand","well","enough","to","explain",
                "to","a","computer.","Art","is","everything","else","we","do"],
                20),
            (["This", "is", "an", "example", "of", "text", "justification."],
                16),
            (["What","must","be","acknowledgment","shall","be"], 16)
            ]
    for words,max_w in words_maxW_list:
        print('Justification of {} using maxWidth {} is:'.format(words, max_w))
        sol = Solution()
        print(sol.fullJustify(words, max_w))

if __name__ == '__main__':
    test()
