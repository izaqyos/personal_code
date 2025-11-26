"""
Week 7, Day 6: Trie (Prefix Tree)

Learning Objectives:
- Understand trie data structure
- Implement trie operations
- Learn prefix matching
- Practice autocomplete
- Solve word search problems

Time: 10-15 minutes
"""

# ============================================================
# EXERCISE 1: Trie Node and Basic Structure
# ============================================================

class TrieNode:
    """Trie node with children and end marker"""
    
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    """
    Trie (Prefix Tree) data structure.
    
    Efficient for prefix-based operations
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """Insert word into trie"""
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
    
    def search(self, word):
        """Search for exact word"""
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return node.is_end_of_word
    
    def starts_with(self, prefix):
        """Check if any word starts with prefix"""
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return True

def test_trie_basics():
    """Test basic trie operations"""
    print("--- Exercise 1: Trie Basics ---")
    
    trie = Trie()
    words = ["apple", "app", "application", "apply", "banana"]
    
    print(f"Inserting words: {words}")
    for word in words:
        trie.insert(word)
    
    # Search tests
    search_words = ["apple", "app", "appl", "ban"]
    print("\nSearch results:")
    for word in search_words:
        found = trie.search(word)
        print(f"  '{word}': {'Found' if found else 'Not found'}")
    
    # Prefix tests
    prefixes = ["app", "ban", "cat"]
    print("\nPrefix tests:")
    for prefix in prefixes:
        exists = trie.starts_with(prefix)
        print(f"  Starts with '{prefix}': {exists}")
    
    print("\n💡 Trie: Efficient prefix operations")
    print("💡 Insert/Search: O(m) where m = word length")
    
    print()

# ============================================================
# EXERCISE 2: Autocomplete
# ============================================================

def autocomplete():
    """
    Implement autocomplete using trie.
    
    TODO: Find all words with given prefix
    """
    print("--- Exercise 2: Autocomplete ---")
    
    class AutocompleteTrie:
        """Trie with autocomplete"""
        
        def __init__(self):
            self.root = TrieNode()
        
        def insert(self, word):
            """Insert word"""
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_end_of_word = True
        
        def autocomplete(self, prefix):
            """Get all words starting with prefix"""
            node = self.root
            
            # Navigate to prefix
            for char in prefix:
                if char not in node.children:
                    return []
                node = node.children[char]
            
            # Collect all words from this node
            words = []
            self._collect_words(node, prefix, words)
            return words
        
        def _collect_words(self, node, current_word, words):
            """Recursively collect all words"""
            if node.is_end_of_word:
                words.append(current_word)
            
            for char, child_node in node.children.items():
                self._collect_words(child_node, current_word + char, words)
    
    trie = AutocompleteTrie()
    words = ["cat", "car", "card", "care", "careful", "dog", "dodge"]
    
    print(f"Dictionary: {words}")
    for word in words:
        trie.insert(word)
    
    prefixes = ["car", "ca", "do"]
    for prefix in prefixes:
        suggestions = trie.autocomplete(prefix)
        print(f"\nAutocomplete '{prefix}': {suggestions}")
    
    print()

# ============================================================
# EXERCISE 3: Word Search
# ============================================================

def word_search():
    """
    Search for words in trie.
    
    TODO: Implement wildcard search
    """
    print("--- Exercise 3: Word Search with Wildcards ---")
    
    class WordDictionary:
        """Dictionary with wildcard search"""
        
        def __init__(self):
            self.root = TrieNode()
        
        def add_word(self, word):
            """Add word to dictionary"""
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_end_of_word = True
        
        def search(self, word):
            """Search with '.' as wildcard"""
            return self._search_helper(word, 0, self.root)
        
        def _search_helper(self, word, index, node):
            """Recursive search with wildcards"""
            if index == len(word):
                return node.is_end_of_word
            
            char = word[index]
            
            if char == '.':
                # Try all children
                for child in node.children.values():
                    if self._search_helper(word, index + 1, child):
                        return True
                return False
            else:
                if char not in node.children:
                    return False
                return self._search_helper(word, index + 1, node.children[char])
    
    dictionary = WordDictionary()
    words = ["bad", "dad", "mad", "pad", "bat"]
    
    print(f"Dictionary: {words}")
    for word in words:
        dictionary.add_word(word)
    
    patterns = ["bad", "b.d", ".ad", "b..", "..."]
    print("\nPattern matching:")
    for pattern in patterns:
        found = dictionary.search(pattern)
        print(f"  '{pattern}': {found}")
    
    print()

# ============================================================
# EXERCISE 4: Longest Common Prefix
# ============================================================

def longest_common_prefix():
    """
    Find longest common prefix using trie.
    
    TODO: Use trie to find LCP
    """
    print("--- Exercise 4: Longest Common Prefix ---")
    
    def find_lcp(words):
        """Find longest common prefix"""
        if not words:
            return ""
        
        # Build trie
        trie = Trie()
        for word in words:
            trie.insert(word)
        
        # Find LCP
        lcp = []
        node = trie.root
        
        while len(node.children) == 1 and not node.is_end_of_word:
            char = list(node.children.keys())[0]
            lcp.append(char)
            node = node.children[char]
        
        return ''.join(lcp)
    
    test_cases = [
        ["flower", "flow", "flight"],
        ["dog", "racecar", "car"],
        ["interspecies", "interstellar", "interstate"]
    ]
    
    for words in test_cases:
        lcp = find_lcp(words)
        print(f"Words: {words}")
        print(f"  LCP: '{lcp}'")
    
    print()

# ============================================================
# EXERCISE 5: Word Break
# ============================================================

def word_break():
    """
    Check if string can be segmented into dictionary words.
    
    TODO: Use trie for efficient word lookup
    """
    print("--- Exercise 5: Word Break ---")
    
    def can_word_break(s, word_dict):
        """Check if s can be segmented"""
        # Build trie
        trie = Trie()
        for word in word_dict:
            trie.insert(word)
        
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        
        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and trie.search(s[j:i]):
                    dp[i] = True
                    break
        
        return dp[n]
    
    test_cases = [
        ("leetcode", ["leet", "code"]),
        ("applepenapple", ["apple", "pen"]),
        ("catsandog", ["cats", "dog", "sand", "and", "cat"])
    ]
    
    for string, dictionary in test_cases:
        result = can_word_break(string, dictionary)
        print(f"String: '{string}'")
        print(f"Dictionary: {dictionary}")
        print(f"  Can break: {result}\n")
    
    print()

# ============================================================
# EXERCISE 6: Real-World Scenario - Spell Checker
# ============================================================

def spell_checker():
    """
    Implement spell checker with suggestions.
    
    TODO: Find similar words for misspellings
    """
    print("--- Exercise 6: Spell Checker ---")
    
    class SpellChecker:
        """Spell checker with suggestions"""
        
        def __init__(self):
            self.trie = Trie()
        
        def add_word(self, word):
            """Add word to dictionary"""
            self.trie.insert(word.lower())
        
        def is_correct(self, word):
            """Check if word is spelled correctly"""
            return self.trie.search(word.lower())
        
        def suggest(self, word, max_distance=1):
            """Suggest corrections (simple version)"""
            word = word.lower()
            suggestions = []
            
            # Try single character edits
            for i in range(len(word)):
                # Deletion
                candidate = word[:i] + word[i+1:]
                if self.trie.search(candidate):
                    suggestions.append(candidate)
                
                # Substitution
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    candidate = word[:i] + c + word[i+1:]
                    if self.trie.search(candidate):
                        suggestions.append(candidate)
            
            # Insertion
            for i in range(len(word) + 1):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    candidate = word[:i] + c + word[i:]
                    if self.trie.search(candidate):
                        suggestions.append(candidate)
            
            return list(set(suggestions))
    
    checker = SpellChecker()
    dictionary = ["hello", "world", "python", "programming", "code"]
    
    print(f"Dictionary: {dictionary}")
    for word in dictionary:
        checker.add_word(word)
    
    test_words = ["hello", "helo", "wrld", "pythn"]
    print("\nSpell check:")
    for word in test_words:
        correct = checker.is_correct(word)
        if correct:
            print(f"  '{word}': ✓ Correct")
        else:
            suggestions = checker.suggest(word)
            print(f"  '{word}': ✗ Suggestions: {suggestions}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Trie with Frequency
# ============================================================

def trie_with_frequency():
    """
    Trie that tracks word frequency.
    
    TODO: Implement frequency-based autocomplete
    """
    print("--- Bonus Challenge: Trie with Frequency ---")
    
    class FrequencyTrieNode:
        """Trie node with frequency"""
        
        def __init__(self):
            self.children = {}
            self.frequency = 0
    
    class FrequencyTrie:
        """Trie with word frequencies"""
        
        def __init__(self):
            self.root = FrequencyTrieNode()
        
        def insert(self, word):
            """Insert word and increment frequency"""
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = FrequencyTrieNode()
                node = node.children[char]
            node.frequency += 1
        
        def top_suggestions(self, prefix, k=3):
            """Get top k suggestions by frequency"""
            node = self.root
            
            # Navigate to prefix
            for char in prefix:
                if char not in node.children:
                    return []
                node = node.children[char]
            
            # Collect all words with frequencies
            words = []
            self._collect_with_freq(node, prefix, words)
            
            # Sort by frequency and return top k
            words.sort(key=lambda x: x[1], reverse=True)
            return [word for word, _ in words[:k]]
        
        def _collect_with_freq(self, node, current_word, words):
            """Collect words with frequencies"""
            if node.frequency > 0:
                words.append((current_word, node.frequency))
            
            for char, child in node.children.items():
                self._collect_with_freq(child, current_word + char, words)
    
    trie = FrequencyTrie()
    
    # Simulate search history
    searches = ["python", "python", "python", "programming", "programming", 
                "program", "project", "practice", "practice"]
    
    print("Search history:")
    for word in searches:
        trie.insert(word)
        print(f"  {word}")
    
    prefix = "pr"
    suggestions = trie.top_suggestions(prefix, k=3)
    print(f"\nTop 3 suggestions for '{prefix}': {suggestions}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Trie Operations:
    - Insert: O(m) where m = word length
    - Search: O(m)
    - Prefix search: O(m)
    - Space: O(ALPHABET_SIZE * N * M) worst case
    
    Advantages:
    - Fast prefix operations
    - Better than hash table for prefixes
    - Memory efficient for common prefixes
    
    Disadvantages:
    - More space than hash table
    - Complex implementation
    - Cache unfriendly
    
    Applications:
    - Autocomplete
    - Spell checker
    - IP routing
    - Dictionary implementation
    
    Best Practices:
    - Use for prefix-heavy operations
    - Consider memory constraints
    - Implement lazy deletion
    - Use compressed trie for space
    
    Common Patterns:
    - DFS for word collection
    - Backtracking for wildcards
    - Frequency tracking
    - Path compression
    
    Security Considerations:
    - Limit trie depth
    - Validate input strings
    - Handle large dictionaries
    - Prevent memory exhaustion
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 7, Day 6: Trie (Prefix Tree)")
    print("=" * 60)
    print()
    
    test_trie_basics()
    autocomplete()
    word_search()
    longest_common_prefix()
    word_break()
    spell_checker()
    trie_with_frequency()
    
    print("=" * 60)
    print("✅ Day 6 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Trie: Efficient for prefix operations")
    print("2. Insert/Search: O(m) where m = word length")
    print("3. Perfect for autocomplete and spell check")
    print("4. Trade space for speed on prefix queries")

