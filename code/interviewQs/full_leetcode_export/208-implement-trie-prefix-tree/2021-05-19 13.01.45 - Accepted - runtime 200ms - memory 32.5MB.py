
class node:
    def __init__(self, char):
        self.char = char
        self.sons=dict()
        self.isWord = False
        
class Trie:

    def __init__(self):
        """
        data structure. tree each node has sons d ictionary. 
        when adding word app for example we set root.sons['a'] to new node for son, which has char 'a'
        then in son node we set son.sons['p'] to a new node son2
        then in son2 node we set son2 char to 'p' and set flag valid_word=True
        """
        self.root = node('')


    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        cur = self.root
        for c in word:
            if c in cur.sons:
                cur = cur.sons[c]
            else:
                son = node(c)
                cur.sons[c]=son
                cur = son
        if cur!=self.root:
            cur.isWord = True



    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        """
        cur = self.root
        for i in range(len(word)):
            c = word[i]
            if not c in cur.sons:
                return False
            else:
                cur = cur.sons[c]

        if cur.isWord:
            return True
        else:
            return False



    def startsWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        cur = self.root
        for c in prefix:
            if not c in cur.sons:
                return False
            else:
                cur = cur.sons[c]

        return True