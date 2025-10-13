class TrieNode:
    def __init__(self):
        self.children = {}  # Dictionary to store child nodes
        self.is_end_of_word = False  # Flag to mark the end of a word

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Inserts a word into the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        """Searches for a word in the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        """Checks if any word in the Trie starts with the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

# Example usage
trie = Trie()
trie.insert("apple")
trie.insert("app")
trie.insert("banana")

print(f" search apple: {trie.search('apple')}")  # Output: True (apple is in the trie) print(trie.search("apple"))  # Output: True
print(f" search app: {trie.search('app')}")  # Output: True (app is in the trie) print(trie.search("app"))  # Output: True
print(f" search grape : {trie.search('grape')}")  # Output: False (grape is not in the trie) print(trie.search("grape"))  # Output: False
print(f" starts with app : {trie.starts_with('app')}")  # Output: True (apple is in the trie) print(trie.starts_with("app"))  # Output: True
print(f" starts with gra : {trie.starts_with('gra')}")  # Output: False (grape is not in the trie) print(trie.starts_with("gra"))  # Output: False
