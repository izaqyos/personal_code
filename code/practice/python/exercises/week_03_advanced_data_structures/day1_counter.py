"""
Week 3, Day 1: Counter - Frequency Counting and most_common

Learning Objectives:
- Master the Counter class from collections
- Learn frequency counting patterns
- Understand most_common() and arithmetic operations
- Practice real-world counting scenarios

Time: 10-15 minutes
"""

from collections import Counter
from typing import List, Dict
import string

# ============================================================
# EXERCISE 1: Counter Basics
# ============================================================

def counter_basics():
    """
    Learn basic Counter operations.
    
    Counter is a dict subclass for counting hashable objects
    """
    print("--- Exercise 1: Counter Basics ---")
    
    # Create Counter from iterable
    words = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
    word_count = Counter(words)
    
    print(f"Words: {words}")
    print(f"Counter: {word_count}")
    print(f"Type: {type(word_count)}")
    
    # Access counts
    print(f"\nCount of 'apple': {word_count['apple']}")
    print(f"Count of 'orange': {word_count['orange']}")  # Returns 0, not KeyError!
    
    # Create from string
    letter_count = Counter("mississippi")
    print(f"\nLetters in 'mississippi': {letter_count}")
    
    # Create from dict
    inventory = Counter({'apples': 5, 'oranges': 3})
    print(f"\nInventory: {inventory}")
    
    print()

# ============================================================
# EXERCISE 2: most_common() Method
# ============================================================

def most_common_examples():
    """
    Use most_common() to find top items.
    
    TODO: Practice finding most frequent items
    """
    print("--- Exercise 2: most_common() ---")
    
    # Sample data: website visits
    visits = [
        'home', 'about', 'home', 'products', 'home', 'about',
        'contact', 'products', 'home', 'products', 'home'
    ]
    
    page_views = Counter(visits)
    
    # Get all items sorted by frequency
    print("All pages (sorted by frequency):")
    for page, count in page_views.most_common():
        print(f"  {page}: {count} views")
    
    # Get top 3
    print("\nTop 3 pages:")
    for page, count in page_views.most_common(3):
        print(f"  {page}: {count} views")
    
    # Get least common (negative index)
    print("\nLeast common page:")
    least = page_views.most_common()[:-2:-1]
    print(f"  {least}")
    
    print()

# ============================================================
# EXERCISE 3: Counter Arithmetic
# ============================================================

def counter_arithmetic():
    """
    Perform arithmetic operations on Counters.
    
    TODO: Practice Counter addition, subtraction, intersection, union
    """
    print("--- Exercise 3: Counter Arithmetic ---")
    
    # Two days of sales
    monday_sales = Counter({'apples': 10, 'oranges': 5, 'bananas': 8})
    tuesday_sales = Counter({'apples': 7, 'oranges': 9, 'bananas': 3})
    
    print(f"Monday sales: {monday_sales}")
    print(f"Tuesday sales: {tuesday_sales}")
    
    # Addition: combine counts
    total_sales = monday_sales + tuesday_sales
    print(f"\nTotal sales (Mon + Tue): {total_sales}")
    
    # Subtraction: keep only positive counts
    difference = monday_sales - tuesday_sales
    print(f"Monday > Tuesday: {difference}")
    
    # Intersection: minimum of counts
    min_sales = monday_sales & tuesday_sales
    print(f"Minimum (intersection): {min_sales}")
    
    # Union: maximum of counts
    max_sales = monday_sales | tuesday_sales
    print(f"Maximum (union): {max_sales}")
    
    print()

# ============================================================
# EXERCISE 4: Updating Counters
# ============================================================

def updating_counters():
    """
    Update Counter objects with new data.
    
    TODO: Practice update() and subtract() methods
    """
    print("--- Exercise 4: Updating Counters ---")
    
    # Start with empty counter
    inventory = Counter()
    
    # Add items
    print("Adding items:")
    inventory.update(['apple', 'apple', 'banana'])
    print(f"  After first update: {inventory}")
    
    inventory.update({'apple': 2, 'orange': 3})
    print(f"  After second update: {inventory}")
    
    # Subtract items
    print("\nRemoving items:")
    inventory.subtract(['apple', 'apple', 'banana'])
    print(f"  After subtract: {inventory}")
    
    # Remove zero and negative counts
    +inventory  # Unary plus removes non-positive counts
    print(f"  After cleanup: {+inventory}")
    
    print()

# ============================================================
# EXERCISE 5: Real-World Scenario - Word Frequency
# ============================================================

def word_frequency_analyzer(text: str, top_n: int = 10) -> List[tuple]:
    """
    Analyze word frequency in text.
    
    TODO: Implement word frequency analysis
    """
    # Clean and tokenize
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    
    # Count words
    word_count = Counter(words)
    
    # Return top N
    return word_count.most_common(top_n)

def test_word_frequency():
    """Test word frequency analyzer"""
    print("--- Exercise 5: Word Frequency Analysis ---")
    
    text = """
    Python is an amazing programming language. Python is easy to learn
    and Python is powerful. Many developers love Python because Python
    has a simple syntax. Python is used for web development, data science,
    machine learning, and automation. Python Python Python!
    """
    
    print("Text analysis:")
    for word, count in word_frequency_analyzer(text, top_n=5):
        print(f"  '{word}': {count} times")
    
    print()

# ============================================================
# EXERCISE 6: Log Analysis with Counter
# ============================================================

def analyze_logs():
    """
    Analyze log files using Counter.
    
    TODO: Count error types, status codes, etc.
    """
    print("--- Exercise 6: Log Analysis ---")
    
    # Simulated log entries: (level, status_code, endpoint)
    logs = [
        ('ERROR', 500, '/api/users'),
        ('INFO', 200, '/api/users'),
        ('ERROR', 404, '/api/posts'),
        ('WARNING', 403, '/api/admin'),
        ('ERROR', 500, '/api/users'),
        ('INFO', 200, '/api/posts'),
        ('ERROR', 500, '/api/database'),
        ('ERROR', 404, '/api/posts'),
        ('INFO', 200, '/api/users'),
    ]
    
    # Count by level
    levels = Counter(log[0] for log in logs)
    print("Logs by level:")
    for level, count in levels.most_common():
        print(f"  {level}: {count}")
    
    # Count status codes
    status_codes = Counter(log[1] for log in logs)
    print("\nStatus codes:")
    for code, count in status_codes.most_common():
        print(f"  {code}: {count}")
    
    # Count errors by endpoint
    error_endpoints = Counter(
        log[2] for log in logs if log[0] == 'ERROR'
    )
    print("\nMost problematic endpoints:")
    for endpoint, count in error_endpoints.most_common(3):
        print(f"  {endpoint}: {count} errors")
    
    print()

# ============================================================
# EXERCISE 7: Elements and Iteration
# ============================================================

def counter_elements():
    """
    Use elements() to expand Counter back to list.
    
    TODO: Practice elements() method
    """
    print("--- Exercise 7: Counter Elements ---")
    
    # Create counter
    fruit_basket = Counter({'apple': 3, 'banana': 2, 'orange': 1})
    print(f"Fruit basket: {fruit_basket}")
    
    # Expand to list
    all_fruits = list(fruit_basket.elements())
    print(f"All fruits: {all_fruits}")
    
    # Sorted expansion
    sorted_fruits = sorted(fruit_basket.elements())
    print(f"Sorted: {sorted_fruits}")
    
    print()

# ============================================================
# BONUS CHALLENGE: N-gram Frequency
# ============================================================

def ngram_frequency(text: str, n: int = 2) -> Counter:
    """
    Count n-gram frequency in text.
    
    TODO: Implement n-gram counting
    
    Args:
        text: Input text
        n: Size of n-grams (2 for bigrams, 3 for trigrams)
    
    Returns:
        Counter of n-grams
    """
    words = text.lower().split()
    
    # Generate n-grams
    ngrams = []
    for i in range(len(words) - n + 1):
        ngram = tuple(words[i:i+n])
        ngrams.append(ngram)
    
    return Counter(ngrams)

def test_ngram_frequency():
    """Test n-gram frequency"""
    print("--- Bonus Challenge: N-gram Frequency ---")
    
    text = "the quick brown fox jumps over the lazy dog the quick fox"
    
    # Bigrams
    bigrams = ngram_frequency(text, n=2)
    print("Most common bigrams:")
    for ngram, count in bigrams.most_common(5):
        print(f"  {' '.join(ngram)}: {count}")
    
    # Trigrams
    trigrams = ngram_frequency(text, n=3)
    print("\nMost common trigrams:")
    for ngram, count in trigrams.most_common(3):
        print(f"  {' '.join(ngram)}: {count}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Counter Operations:
    - Creation from iterable: O(n)
    - Access/update single item: O(1) average
    - most_common(k): O(n log k) using heap
    - most_common() (all items): O(n log n) for sorting
    
    Arithmetic Operations:
    - Addition/Subtraction: O(n + m)
    - Intersection/Union: O(min(n, m))
    
    Space Complexity:
    - O(k) where k is number of unique items
    - Much more efficient than storing all items
    
    Benefits:
    - Cleaner code than manual dict counting
    - Returns 0 for missing keys (no KeyError)
    - Built-in arithmetic operations
    - most_common() is very efficient
    
    Use Cases:
    - Frequency analysis
    - Finding top-k items
    - Comparing distributions
    - Inventory management
    - Log analysis
    
    Security Considerations:
    - Validate input size to prevent memory exhaustion
    - Be careful with user-provided keys
    - Counter can grow large with unique items
    - Consider limiting unique key count
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 3, Day 1: Counter")
    print("=" * 60)
    print()
    
    counter_basics()
    most_common_examples()
    counter_arithmetic()
    updating_counters()
    test_word_frequency()
    analyze_logs()
    counter_elements()
    test_ngram_frequency()
    
    print("=" * 60)
    print("✅ Day 1 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Counter is a dict subclass for counting")
    print("2. most_common(n) efficiently finds top n items")
    print("3. Supports arithmetic: +, -, &, |")
    print("4. Returns 0 for missing keys (no KeyError)")

