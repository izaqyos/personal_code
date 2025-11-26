"""
Week 1, Day 2: Dictionary Comprehensions and defaultdict Patterns

Learning Objectives:
- Master dictionary comprehensions for transforming data
- Understand when to use defaultdict vs regular dict
- Learn common patterns for grouping and counting
- Practice nested dictionary operations

Time: 10-15 minutes
"""

import sys
from collections import defaultdict
from typing import Dict, List

# ============================================================
# EXERCISE 1: Dictionary Comprehensions Basics
# ============================================================

def dict_comprehension_basics():
    """
    Practice basic dictionary comprehension patterns.
    
    TODO: Complete the following transformations using dict comprehensions
    """
    print("--- Exercise 1: Dictionary Comprehension Basics ---")
    
    # 1. Create a dict mapping numbers 1-10 to their squares
    # TODO: squares = {...}
    squares = None
    print(f"Squares: {squares}")
    
    # 2. Filter: Create dict of only even numbers and their cubes from 1-20
    # TODO: even_cubes = {...}
    even_cubes = None
    print(f"Even cubes: {even_cubes}")
    
    # 3. Transform: Convert list of words to dict with word length as value
    words = ["python", "java", "rust", "go", "javascript"]
    # TODO: word_lengths = {...}
    word_lengths = None
    print(f"Word lengths: {word_lengths}")
    
    # 4. Invert: Swap keys and values from a dictionary
    original = {"a": 1, "b": 2, "c": 3}
    # TODO: inverted = {...}
    inverted = None
    print(f"Inverted: {inverted}")
    
    print()

# ============================================================
# EXERCISE 2: defaultdict vs Regular Dict
# ============================================================

def compare_dict_patterns():
    """
    Compare different patterns for handling missing keys.
    
    TODO: Implement the same logic using three different approaches:
    1. Regular dict with if-else
    2. Regular dict with .get() and .setdefault()
    3. defaultdict
    
    Task: Group words by their first letter
    """
    print("--- Exercise 2: defaultdict vs Regular Dict ---")
    
    words = ["apple", "banana", "avocado", "cherry", "apricot", "blueberry", "coconut"]
    
    # Approach 1: Regular dict with if-else
    print("Approach 1: if-else pattern")
    groups_v1 = {}
    for word in words:
        first_letter = word[0]
        # TODO: Add logic to group words
        pass
    print(f"Groups v1: {groups_v1}")
    
    # Approach 2: Using .setdefault()
    print("\nApproach 2: setdefault pattern")
    groups_v2 = {}
    for word in words:
        first_letter = word[0]
        # TODO: Use setdefault to group words
        pass
    print(f"Groups v2: {groups_v2}")
    
    # Approach 3: defaultdict
    print("\nApproach 3: defaultdict pattern")
    groups_v3 = defaultdict(list)
    for word in words:
        first_letter = word[0]
        # TODO: Use defaultdict to group words
        pass
    print(f"Groups v3: {dict(groups_v3)}")
    
    # Question: Which approach is most readable? Most efficient?
    print("\n💡 Reflection: Which pattern do you prefer and why?")
    print()

# ============================================================
# EXERCISE 3: Advanced defaultdict Patterns
# ============================================================

def advanced_defaultdict_patterns():
    """
    Explore nested defaultdict and other factory functions.
    
    TODO: Implement various defaultdict patterns
    """
    print("--- Exercise 3: Advanced defaultdict Patterns ---")
    
    # Pattern 1: Counting with defaultdict(int)
    text = "the quick brown fox jumps over the lazy dog"
    word_count = defaultdict(int)
    # TODO: Count word frequencies
    for word in text.split():
        pass
    print(f"Word frequencies: {dict(word_count)}")
    
    # Pattern 2: Nested defaultdict for 2D grouping
    # Group students by grade and then by subject
    students = [
        ("Alice", "A", "Math"),
        ("Bob", "B", "Math"),
        ("Charlie", "A", "Science"),
        ("Diana", "A", "Math"),
        ("Eve", "B", "Science"),
    ]
    
    # TODO: Create nested defaultdict: grade -> subject -> [students]
    grade_subject_students = None
    
    print(f"Nested grouping: {grade_subject_students}")
    
    # Pattern 3: defaultdict with lambda for complex defaults
    # Create a dict that tracks both count and sum for averaging
    # TODO: Use defaultdict(lambda: {'count': 0, 'sum': 0})
    stats = None
    numbers = [("a", 10), ("b", 20), ("a", 15), ("b", 25), ("a", 5)]
    
    # TODO: Calculate running stats
    
    print(f"Statistics: {dict(stats)}")
    print()

# ============================================================
# EXERCISE 4: Real-World Scenario - Log Analysis
# ============================================================

def analyze_logs():
    """
    Analyze server logs to extract insights.
    
    Scenario: Parse log entries and generate statistics:
    - Count requests per endpoint
    - Group errors by status code
    - Track response times per endpoint
    
    TODO: Implement using dict comprehensions and defaultdict
    """
    print("--- Exercise 4: Real-World Log Analysis ---")
    
    # Simulated log entries: (endpoint, status_code, response_time_ms)
    logs = [
        ("/api/users", 200, 45),
        ("/api/posts", 200, 120),
        ("/api/users", 404, 10),
        ("/api/posts", 200, 95),
        ("/api/users", 200, 50),
        ("/api/comments", 500, 200),
        ("/api/posts", 200, 110),
        ("/api/users", 200, 48),
        ("/api/comments", 500, 180),
        ("/api/posts", 404, 15),
    ]
    
    # Task 1: Count requests per endpoint
    # TODO: Use defaultdict(int)
    endpoint_counts = None
    
    print(f"Requests per endpoint: {dict(endpoint_counts)}")
    
    # Task 2: Group errors (status >= 400) by status code
    # TODO: Use defaultdict(list) to store endpoints
    errors_by_code = None
    
    print(f"Errors by status code: {dict(errors_by_code)}")
    
    # Task 3: Calculate average response time per endpoint
    # TODO: Track sum and count, then compute averages with dict comprehension
    endpoint_times = None
    
    avg_response_times = None  # Use dict comprehension to calculate averages
    
    print(f"Average response times: {avg_response_times}")
    
    # Task 4: Find slowest endpoint
    # TODO: Use max() with key parameter
    slowest = None
    print(f"Slowest endpoint: {slowest}")
    
    print()

# ============================================================
# EXERCISE 5: Dictionary Merging and Updates
# ============================================================

def dict_merging_patterns():
    """
    Explore different ways to merge and update dictionaries.
    
    TODO: Compare different merging techniques
    """
    print("--- Exercise 5: Dictionary Merging ---")
    
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"b": 20, "d": 4, "e": 5}
    
    # Method 1: Using ** unpacking (Python 3.5+)
    # TODO: merged1 = {...}
    merged1 = None
    print(f"Method 1 (** unpacking): {merged1}")
    
    # Method 2: Using | operator (Python 3.9+)
    # TODO: merged2 = dict1 | dict2
    merged2 = None
    print(f"Method 2 (| operator): {merged2}")
    
    # Method 3: Using dict.update() (in-place)
    merged3 = dict1.copy()
    # TODO: Update merged3 with dict2
    print(f"Method 3 (.update()): {merged3}")
    
    # Method 4: Custom merge with conflict resolution
    # TODO: If key exists in both, sum the values
    merged4 = None
    print(f"Method 4 (custom merge): {merged4}")
    
    print()

# ============================================================
# BONUS CHALLENGE
# ============================================================

def word_frequency_analyzer(text: str) -> Dict[str, int]:
    """
    Build a word frequency analyzer with the following features:
    
    TODO: Implement a function that:
    1. Converts text to lowercase
    2. Removes punctuation
    3. Counts word frequencies
    4. Returns dict sorted by frequency (descending)
    
    Bonus: Return only words that appear more than once
    """
    # TODO: Implement
    pass

def test_word_frequency():
    """Test the word frequency analyzer"""
    text = """
    Python is an amazing programming language. Python is easy to learn
    and Python is powerful. Many developers love Python because Python
    has a simple syntax.
    """
    
    result = word_frequency_analyzer(text)
    print("--- Bonus Challenge: Word Frequency Analyzer ---")
    print(f"Word frequencies: {result}")
    print()

# ============================================================
# PERFORMANCE COMPARISON
# ============================================================

def performance_analysis():
    """
    Analyze performance differences between dict patterns.
    
    Compare:
    - Regular dict with if-else
    - dict.setdefault()
    - defaultdict
    """
    import time
    
    print("--- Performance Analysis ---")
    
    # Generate test data
    data = ["key" + str(i % 1000) for i in range(100000)]
    
    # Test 1: if-else pattern
    start = time.perf_counter()
    d1 = {}
    for key in data:
        if key in d1:
            d1[key] += 1
        else:
            d1[key] = 1
    time1 = time.perf_counter() - start
    
    # Test 2: setdefault pattern
    start = time.perf_counter()
    d2 = {}
    for key in data:
        d2.setdefault(key, 0)
        d2[key] += 1
    time2 = time.perf_counter() - start
    
    # Test 3: defaultdict pattern
    start = time.perf_counter()
    d3 = defaultdict(int)
    for key in data:
        d3[key] += 1
    time3 = time.perf_counter() - start
    
    print(f"if-else pattern:     {time1:.4f}s")
    print(f"setdefault pattern:  {time2:.4f}s")
    print(f"defaultdict pattern: {time3:.4f}s")
    print(f"\nFastest: defaultdict is {time1/time3:.2f}x faster than if-else")
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Dictionary Comprehension:
    - Time: O(n) where n is the size of input iterable
    - Space: O(n) for the resulting dictionary
    
    defaultdict:
    - Time: O(1) for insert/lookup (same as regular dict)
    - Space: O(n) for n unique keys
    - Advantage: Eliminates key existence checks
    
    Dict Merging:
    - ** unpacking: O(n + m) where n, m are dict sizes
    - | operator: O(n + m)
    - .update(): O(m) where m is size of updating dict
    
    Security Considerations:
    - Be cautious with user-provided keys (can cause memory issues)
    - Validate input size when building dicts from external data
    - Use dict size limits for untrusted input
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 1, Day 2: Dictionary Comprehensions and defaultdict")
    print("=" * 60)
    print()
    
    dict_comprehension_basics()
    compare_dict_patterns()
    advanced_defaultdict_patterns()
    analyze_logs()
    dict_merging_patterns()
    test_word_frequency()
    performance_analysis()
    
    print("=" * 60)
    print("✅ Day 2 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Dict comprehensions are concise for transformations")
    print("2. defaultdict eliminates key existence checks")
    print("3. Choose the right pattern for readability and performance")
    print("4. defaultdict is typically faster for accumulation patterns")

