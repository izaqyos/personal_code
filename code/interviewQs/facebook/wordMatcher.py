"""
A Question I got @ a Facebook interview...
my solution. with tests and everything 
"""

import pdb

class node:
    def __init__(self, val=''):
        self.val = val
        self.sons = dict()

class wordMatcher:
    def __init__(self, words):
        self.root = node()
        self.setup(words)

    def setup(self, words):
        for word in words:
            self.addWordToTrie(word)

    def addWordToTrie(self, word):
        cur = self.root
        for c in word:
            #pdb.set_trace()
            if not c in cur.sons:
                new = node(c)
                cur.sons[c] = new
            cur = cur.sons[c]
                
        #self.printMe()

    def printMe(self):
        from collections import deque
        q = deque()
        #pdb.set_trace()
        q.append(('', self.root))

        count = 1
        numsons = 1
        while len(q) > 0: #add the new line to the q itself (save (node, newline)on q )
            indent, c = q.popleft()
            print(indent+c.val)
            indent += ' '
            for i,s in enumerate(c.sons.values()):
                if i == len(c.sons.values()) -1:
                    q.append((indent, s))
                    #q.append((indent+"\\"+"-", s))
                else:
                    q.append((indent, s))
                    #q.append((indent+'|-', s))

            
            
    def isMatch(self, word):
        """
        exact match is simple, just iterate the characters in the word
        however it is required to support '.' char, which like regex matches a-z
        this is why I need either a BFS or DFS search. 
        I opt for DFS since the trie is usually a short tree (max depth == max(len(word in words))
        """
        return self.isMatchR(self.root, word, 0)

    def isMatchR(self, root, word, index):
        if index >= len(word):
            return True
        
        c = word[index]
        if (c != '.'): #exact match
            if c in root.sons:
                return self.isMatchR(root.sons[c], word, index+1)
            else:
                return False
        else: #. can match any letter
            for son in root.sons.values():
                if self.isMatchR(son, word, index+1 ):
                    return True
        
        # unreachable
        return False



def test():
    words = ['hi', 'hello', 'hell', 'dog', 'doggy', 'dogs']
    matchList = words[:]
    matchList.extend(['yosi', 'ha', 'dogi'])
    matchList.extend(['y.si', 'h.', '...', '.x'])
    matcher = wordMatcher(words)
    matcher.printMe()
    for word in matchList:
        isMatch = matcher.isMatch(word)
        print('word {} match check is {}'.format(word, isMatch))

if __name__ == "__main__":
    test()
    
