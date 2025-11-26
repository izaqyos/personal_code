# Tries (Prefix Trees) - Complete Guide

## 📋 Pattern Recognition

**When to use Tries:**
- Word/string search problems
- Prefix matching ("autocomplete", "starts with")
- Multiple string searches in dictionary
- Word games (Boggle, Scrabble)
- "Find all words", "word search"

**Common Keywords:**
- Prefix, suffix, dictionary, autocomplete
- "Words that start with...", "contains word..."
- Multiple word lookups
- Longest common prefix

---

## 🎯 Trie Basics

### What is a Trie?
- Tree data structure for storing strings
- Each path from root represents a string
- Shares common prefixes (space efficient for many strings)
- Fast lookups: O(m) where m = word length

### Visual Example
```
Insert: "cat", "car", "card", "dog"

        root
       /    \
      c      d
      |      |
      a      o
     / \     |
    t   r    g*
   *    |
        d*
```
`*` = end of word

---

## 🔧 Basic Trie Implementation

### TrieNode Structure

```python
class TrieNode:
    """
    Node in a Trie
    """
    def __init__(self):
        self.children = {}      # char -> TrieNode
        self.is_end_of_word = False
        # Optional: store additional data
        # self.word = None
        # self.count = 0
```

### Complete Trie Implementation

```python
class Trie:
    """
    LeetCode #208 - Implement Trie (Prefix Tree)
    
    All operations: O(m) where m = word length
    Space: O(ALPHABET_SIZE * N * M) worst case
    """
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """
        Insert word into trie
        Time: O(m), Space: O(m) new nodes
        """
        node = self.root
        
        for char in word:
            # Create new node if path doesn't exist
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        # Mark end of word
        node.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        """
        Returns True if exact word exists
        Time: O(m)
        """
        node = self._find_node(word)
        return node is not None and node.is_end_of_word
    
    def startsWith(self, prefix: str) -> bool:
        """
        Returns True if any word starts with prefix
        Time: O(m)
        """
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix: str) -> TrieNode:
        """
        Helper: traverse to node representing prefix
        Returns None if prefix doesn't exist
        """
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node


# Usage example
trie = Trie()
trie.insert("apple")
print(trie.search("apple"))      # True
print(trie.search("app"))        # False
print(trie.startsWith("app"))    # True
trie.insert("app")
print(trie.search("app"))        # True
```

---

## 💡 Core Patterns & Problems

### Pattern 1: Basic Operations

#### Problem 1: Implement Trie
```python
# See complete implementation above
# LeetCode #208
```

#### Problem 2: Trie with Count
```python
class TrieWithCount:
    """
    Trie that tracks word frequency
    Useful for: word frequency, prefix count
    """
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.count = node.count + 1 if hasattr(node, 'count') else 1
    
    def count_words_starting_with(self, prefix: str) -> int:
        """Count how many words start with prefix"""
        node = self._find_node(prefix)
        if not node:
            return 0
        return self._count_words(node)
    
    def _count_words(self, node: TrieNode) -> int:
        """Count all words from this node down"""
        count = 1 if node.is_end_of_word else 0
        for child in node.children.values():
            count += self._count_words(child)
        return count
```

---

### Pattern 2: Wildcard Search

#### Problem 3: Add and Search Word - Data Structure Design
```python
class WordDictionary:
    """
    LeetCode #211 - Support wildcard '.' matching any char
    
    Time: O(m) for insert, O(26^m) worst case for search with wildcards
    """
    def __init__(self):
        self.root = TrieNode()
    
    def addWord(self, word: str) -> None:
        """Insert word - same as basic trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        """
        Search with wildcard support
        '.' matches any single character
        """
        return self._search_helper(word, 0, self.root)
    
    def _search_helper(self, word: str, index: int, node: TrieNode) -> bool:
        """
        Recursive helper for wildcard search
        """
        # Reached end of word
        if index == len(word):
            return node.is_end_of_word
        
        char = word[index]
        
        if char == '.':
            # Try all possible children
            for child in node.children.values():
                if self._search_helper(word, index + 1, child):
                    return True
            return False
        else:
            # Exact character match
            if char not in node.children:
                return False
            return self._search_helper(word, index + 1, node.children[char])


# Example usage
wd = WordDictionary()
wd.addWord("bad")
wd.addWord("dad")
wd.addWord("mad")
print(wd.search("pad"))   # False
print(wd.search("bad"))   # True
print(wd.search(".ad"))   # True
print(wd.search("b.."))   # True
```

---

### Pattern 3: Trie + Backtracking (Word Games)

#### Problem 4: Word Search II 🚨 CRITICAL
```python
def findWords(board: list[list[str]], words: list[str]) -> list[str]:
    """
    LeetCode #212 - Find all words from dictionary in 2D board
    
    Key insight: Trie + DFS is much faster than DFS per word
    
    Time: O(M * N * 4^L) where L = max word length
    Space: O(W * L) for trie where W = number of words
    """
    # Step 1: Build trie from word list
    trie = Trie()
    for word in words:
        trie.insert(word)
    
    rows, cols = len(board), len(board[0])
    result = set()  # Use set to avoid duplicates
    
    def dfs(r, c, node, path):
        """
        DFS with trie traversal
        r, c: current position
        node: current trie node
        path: current word being formed
        """
        # Boundary check
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        
        char = board[r][c]
        
        # Already visited or char not in trie
        if char == '#' or char not in node.children:
            return
        
        # Move to next node in trie
        node = node.children[char]
        path += char
        
        # Found a word!
        if node.is_end_of_word:
            result.add(path)
            # Optimization: can continue searching for longer words
            # node.is_end_of_word = False  # Prevent duplicates
        
        # Mark as visited
        temp = board[r][c]
        board[r][c] = '#'
        
        # Explore 4 directions
        dfs(r + 1, c, node, path)
        dfs(r - 1, c, node, path)
        dfs(r, c + 1, node, path)
        dfs(r, c - 1, node, path)
        
        # Restore cell
        board[r][c] = temp
    
    # Step 2: Start DFS from each cell
    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie.root, "")
    
    return list(result)


# Example
board = [
    ['o','a','a','n'],
    ['e','t','a','e'],
    ['i','h','k','r'],
    ['i','f','l','v']
]
words = ["oath","pea","eat","rain"]
print(findWords(board, words))  # ["oath","eat"]
```

**Why Trie is Critical Here:**
- Without trie: O(W * M * N * 4^L) - try each word separately
- With trie: O(M * N * 4^L) - single DFS explores all words at once!

---

### Pattern 4: Longest Common Prefix

#### Problem 5: Longest Common Prefix Using Trie
```python
def longestCommonPrefix(strs: list[str]) -> str:
    """
    LeetCode #14 - Find longest common prefix
    
    Trie approach (alternative to horizontal/vertical scanning)
    Time: O(S) where S = sum of all characters
    Space: O(S)
    """
    if not strs:
        return ""
    
    # Build trie
    trie = Trie()
    for word in strs:
        trie.insert(word)
    
    # Traverse trie while only one child exists
    node = trie.root
    prefix = []
    
    while len(node.children) == 1 and not node.is_end_of_word:
        char = list(node.children.keys())[0]
        prefix.append(char)
        node = node.children[char]
    
    return ''.join(prefix)
```

---

### Pattern 5: Word Replacement

#### Problem 6: Replace Words
```python
def replaceWords(dictionary: list[str], sentence: str) -> str:
    """
    LeetCode #648 - Replace words with their roots
    
    Example: roots = ["cat", "bat", "rat"]
             sentence = "the cattle was rattled by the battery"
             Output: "the cat was rat by the bat"
    
    Time: O(D + S) where D = dictionary size, S = sentence length
    """
    # Build trie with roots
    trie = Trie()
    for root in dictionary:
        trie.insert(root)
    
    def find_root(word: str) -> str:
        """Find shortest root for word, or return word if no root"""
        node = trie.root
        prefix = []
        
        for char in word:
            if char not in node.children:
                return word  # No root found
            
            node = node.children[char]
            prefix.append(char)
            
            if node.is_end_of_word:
                return ''.join(prefix)  # Found root!
        
        return word  # No root found
    
    words = sentence.split()
    return ' '.join(find_root(word) for word in words)
```

---

### Pattern 6: Prefix Sum / Map Sum

#### Problem 7: Map Sum Pairs
```python
class MapSum:
    """
    LeetCode #677 - Trie with values
    
    insert(key, val): insert key-value pair
    sum(prefix): return sum of all values whose keys start with prefix
    """
    def __init__(self):
        self.root = TrieNode()
        self.map = {}  # Track key-value for updates
    
    def insert(self, key: str, val: int) -> None:
        # Calculate delta if key already exists
        delta = val - self.map.get(key, 0)
        self.map[key] = val
        
        # Update trie with delta
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            
            # Store cumulative sum at each node
            if not hasattr(node, 'sum'):
                node.sum = 0
            node.sum += delta
    
    def sum(self, prefix: str) -> int:
        node = self.root
        
        # Navigate to prefix
        for char in prefix:
            if char not in node.children:
                return 0
            node = node.children[char]
        
        return getattr(node, 'sum', 0)
```

---

### Pattern 7: Lexicographical Problems

#### Problem 8: Lexicographical Numbers
```python
def lexicalOrder(n: int) -> list[int]:
    """
    LeetCode #386 - Return 1 to n in lexicographical order
    
    Example: n = 13
    Output: [1,10,11,12,13,2,3,4,5,6,7,8,9]
    
    Trie approach: DFS traversal of implicit trie
    Time: O(n), Space: O(log n) recursion
    """
    result = []
    
    def dfs(current):
        if current > n:
            return
        
        result.append(current)
        
        # Try appending 0-9
        for digit in range(10):
            next_num = current * 10 + digit
            if next_num > n:
                break
            dfs(next_num)
    
    # Start with 1-9 (not 0)
    for i in range(1, 10):
        dfs(i)
    
    return result
```

---

## 🎓 Advanced Problems

### Problem 9: Palindrome Pairs (Hard)
```python
def palindromePairs(words: list[str]) -> list[list[int]]:
    """
    LeetCode #336 - Find all pairs that form palindrome
    
    Trie approach for efficient palindrome checking
    Time: O(n * k²) where n = words, k = max length
    """
    def is_palindrome(word, start, end):
        while start < end:
            if word[start] != word[end]:
                return False
            start += 1
            end -= 1
        return True
    
    # Build trie with reversed words
    trie = Trie()
    for i, word in enumerate(words):
        # Store index at end node
        node = trie.root
        for char in reversed(word):
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.word_index = i
    
    result = []
    
    # For each word, search in trie
    for i, word in enumerate(words):
        node = trie.root
        
        for j, char in enumerate(word):
            # Check if remaining word is palindrome
            if hasattr(node, 'word_index'):
                if i != node.word_index and is_palindrome(word, j, len(word) - 1):
                    result.append([i, node.word_index])
            
            if char not in node.children:
                break
            node = node.children[char]
        else:
            # Word fully matched in trie
            # Check for palindrome suffixes
            # ... (additional logic)
            pass
    
    return result
```

---

## 🐛 Common Mistakes

### Mistake 1: Not Marking End of Word
```python
# ❌ WRONG - Can't distinguish "car" from "card"
def insert(self, word):
    node = self.root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    # Forgot to mark end!

# ✅ CORRECT
def insert(self, word):
    node = self.root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.is_end_of_word = True  # Mark end!
```

### Mistake 2: Returning Node Instead of Boolean
```python
# ❌ WRONG
def search(self, word):
    return self._find_node(word)  # Returns TrieNode or None

# ✅ CORRECT
def search(self, word):
    node = self._find_node(word)
    return node is not None and node.is_end_of_word
```

### Mistake 3: Not Handling Empty Strings
```python
# ❌ May crash on empty string
def search(self, word):
    node = self.root
    for char in word:  # What if word is ""?
        ...

# ✅ CORRECT - handle edge case
def search(self, word):
    if not word:
        return False  # or True if you inserted ""
    node = self.root
    for char in word:
        ...
```

### Mistake 4: Wildcard Search Without Recursion
```python
# ❌ WRONG - Can't handle '.' properly with iteration
def search_with_dot(self, word):
    node = self.root
    for char in word:
        if char == '.':
            # Can't try all children in loop!
            pass

# ✅ CORRECT - Use recursion for wildcards
def search_with_dot(self, word):
    return self._dfs_search(word, 0, self.root)
```

---

## 💡 Pro Tips

### Tip 1: When to Use Trie vs Hash Set

| Use Case | Trie | Hash Set |
|----------|------|----------|
| Exact word lookup | ❌ O(m) | ✅ O(1) |
| Prefix queries | ✅ O(m) | ❌ O(n) |
| Multiple lookups | ✅ Reuses prefixes | ❌ Each word stored fully |
| Autocomplete | ✅ Natural fit | ❌ Not suited |
| Space for many similar words | ✅ Saves space | ❌ Wastes space |

### Tip 2: Trie Space Optimization
```python
# Instead of dict (overhead per node):
node.children = {}

# Use array for lowercase letters only:
node.children = [None] * 26

# Access: node.children[ord(char) - ord('a')]
```

### Tip 3: Storing Additional Data
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        
        # Optional additions:
        self.word = None          # Store complete word
        self.count = 0            # Frequency
        self.indices = []         # Which words pass through
        self.value = 0            # For sum problems
```

### Tip 4: Trie + DFS Pattern
```python
# Common in board games (Boggle, Word Search II)
def trie_dfs(board, trie):
    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie.root, "")  # Start from trie root
    
    def dfs(r, c, node, path):
        char = board[r][c]
        if char not in node.children:
            return
        
        next_node = node.children[char]
        # Continue DFS with next_node...
```

### Tip 5: Early Termination
```python
# In Word Search II, remove word after finding it:
if node.is_end_of_word:
    result.add(path)
    node.is_end_of_word = False  # Prevent finding again
    
    # Optionally: prune leaf nodes to speed up further searches
```

---

## 🎓 Practice Problems by Difficulty

### Easy
1. **#208 Implement Trie** 🚨 **START HERE**
2. **#720 Longest Word in Dictionary**
3. **#1032 Stream of Characters**

### Medium
1. **#211 Design Add and Search Words** 🚨 **MUST DO**
2. **#648 Replace Words** - Prefix matching
3. **#677 Map Sum Pairs** - Trie with values
4. **#386 Lexicographical Numbers** - Implicit trie
5. **#1268 Search Suggestions System** - Autocomplete
6. **#139 Word Break** - Can solve with trie
7. **#820 Short Encoding of Words** - Suffix trie

### Hard
1. **#212 Word Search II** 🚨 **MUST DO** - Trie + backtracking
2. **#336 Palindrome Pairs** - Advanced trie usage
3. **#425 Word Squares** (Premium) - Trie + backtracking
4. **#472 Concatenated Words** - Trie + DP
5. **#588 Design In-Memory File System** (Premium) - Trie for paths

---

## 📊 Complexity Summary

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Insert | O(m) | O(m) | m = word length |
| Search | O(m) | O(1) | |
| Prefix search | O(m) | O(1) | |
| Wildcard search | O(26^m) | O(m) | Worst case with all '.' |
| Space for n words | O(ALPHABET * n * m) | Worst case | |
| Space for n words | O(total_chars) | Average case | Shared prefixes |

---

## 🎯 Interview Strategy

### Step 1: Recognize Trie Problem (30 sec)
Look for:
- "Dictionary", "prefix", "autocomplete"
- Multiple string lookups
- Word games on boards
- "All words that start with..."

### Step 2: Choose Implementation (1 min)
- Basic dict or array-based children?
- What extra data to store in nodes?
- Need wildcards? → Plan for recursion

### Step 3: Explain Approach (1 min)
- "I'll use a trie to store all words"
- "Each path from root represents a word"
- "This allows O(m) lookups instead of O(n)"

### Step 4: Handle Edge Cases
```python
# Always consider:
1. Empty string
2. Single character
3. Duplicate words
4. Prefix is a complete word
5. Word contains prefix
```

---

**Remember:** Tries excel at prefix operations! If the problem involves "starts with" or searching multiple words, think Trie!

