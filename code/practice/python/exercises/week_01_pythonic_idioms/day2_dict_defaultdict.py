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
    squares = {i: i*i for i in range(1, 11)}
    print(f"Squares: {squares}")
    
    # 2. Filter: Create dict of only even numbers and their cubes from 1-20
    # TODO: even_cubes = {...}
    even_cubes = {i: i**3 for i in range(1, 21) if i % 2 == 0}
    print(f"Even cubes: {even_cubes}")
    
    # 3. Transform: Convert list of words to dict with word length as value
    words = ["python", "java", "rust", "go", "javascript"]
    # TODO: word_lengths = {...}
    word_lengths = {k: len(k) for k in words}
    print(f"Word lengths: {word_lengths}")
    
    # 4. Invert: Swap keys and values from a dictionary
    original = {"a": 1, "b": 2, "c": 3}
    # TODO: inverted = {...}
    inverted = {v:k for k,v in original.items()}
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
        if first_letter in groups_v1:
            groups_v1[first_letter].append(word)
        else:
            groups_v1[first_letter] = [word]
    print(f"Groups v1: {groups_v1}")
    
    # Approach 2: Using .setdefault()
    print("\nApproach 2: setdefault pattern")
    groups_v2 = {}
    for word in words:
        first_letter = word[0]
        # TODO: Use setdefault to group words
        groups_v2.setdefault(first_letter, []).append(word)
    print(f"Groups v2: {groups_v2}")
    
    # Approach 3: defaultdict
    print("\nApproach 3: defaultdict pattern, gr8 4 grouping")
    groups_v3 = defaultdict(list)
    for word in words:
        first_letter = word[0]
        # TODO: Use defaultdict to group words
        groups_v3[first_letter].append(word)
    print(f"Groups v3: {dict(groups_v3)}")
    
    # Question: Which approach is most readable? Most efficient?
    print("\n💡 Reflection: Which pattern do you prefer and why?")
    print("I prefer the defaultdict pattern because it is more readable and efficient for grouping data.")
    
    print("""
    ============================================================
    INSIGHTS: When to use each pattern
    ============================================================
    
    Pattern 1 (if-else) is better when:
      - You need custom initialization logic per key
      - You want to track "first seen" explicitly (only store first occurrence)
      - Complex init: groups[key] = {'count': 0, 'created_at': datetime.now()}
    
    Pattern 2 (.get/.setdefault) is better when:
      - You need a one-liner without import
      - Read-only default (don't want to modify dict): config.get('timeout', 30)
      - Working with JSON/API responses (regular dicts, not defaultdict)
      - Chained access: response.get('user', {}).get('name', 'Anonymous')
    
    defaultdict drawbacks:
      - Accidental key creation: if dd['typo']: creates key 'typo'
      - Not JSON serializable: json.dumps(dd) needs dict(dd) first
      - Overkill for simple lookups: .get(key, default) is simpler
    
    Rule of Thumb:
      - Building/accumulating data → defaultdict ✅
      - Reading with fallback → .get() ✅
      - Complex per-key init → if-else ✅
      - Working with JSON/APIs → .get() ✅
    """)
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
        word_count[word] += 1
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
    grade_subject_students = defaultdict(lambda: defaultdict(list))
    for (name, grade, subject) in students:
        grade_subject_students[grade][subject].append(name)
    print(f"Nested grouping: {grade_subject_students}")
    
    # Pattern 3: defaultdict with lambda for complex defaults
    # Create a dict that tracks both count and sum for averaging
    # TODO: Use defaultdict(lambda: {'count': 0, 'sum': 0, 'max': float('-inf')})
    stats = defaultdict(lambda: {'count': 0, 'sum': 0, 'max': float('-inf')})
    numbers = [("a", 10), ("b", 20), ("a", 15), ("b", 25), ("a", 5)]
    for number in numbers:
        stats[number[0]]['count'] += 1
        stats[number[0]]['sum'] += number[1]
        stats[number[0]]['max'] += max(stats[number[0]]['max'], number[1])
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
    endpoint_counts = defaultdict(int)
    for log in logs:
        endpoint_counts[log[0]] += 1
    print(f"Requests per endpoint: {dict(endpoint_counts)}")
    
    # Task 2: Group errors (status >= 400) by status code
    # TODO: Use defaultdict(list) to store endpoints
    errors_by_code = defaultdict(list)
    for log in logs:
        if log[1] >= 400:
            errors_by_code[log[1]].append(log[0])
    print(f"Errors by status code: {dict(errors_by_code)}")
    
    # Task 3: Calculate average response time per endpoint
    # TODO: Track sum and count, then compute averages with dict comprehension
    endpoint_times = defaultdict(tuple) # (sum, count)
    endpoint_times = {log[0]: (endpoint_times[log[0]][0] + log[2],endpoint_times[log[0]][1] +1 ) for log in logs}
    avg_response_times = {k: v[0]/v[1] for k,v in endpoint_times.items()}
    print(f"Average response times: {avg_response_times}")
    
    # Task 4: Find slowest endpoint
    # TODO: Use max() with key parameter
    my_slowest = max(avg_response_times, key=avg_response_times.get)
    #slowest = max(endpoint_times, key=lambda x: endpoint_times[x][0]/endpoint_times[x][1])
    print(f"Slowest endpoint: {my_slowest}")
    
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
    merged1 = {**dict1, **dict2}
    print(f"Method 1 (** unpacking): {merged1}")
    
    # Method 2: Using | operator (Python 3.9+)
    # TODO: merged2 = dict1 | dict2
    merged2 = dict1 | dict2
    print(f"Method 2 (| operator): {merged2}")
    
    # Method 3: Using dict.update() (in-place)
    merged3 = dict1.copy()
    merged3.update(dict2)
    # TODO: Update merged3 with dict2
    print(f"Method 3 (.update()): {merged3}")
    
    # Method 4: Custom merge with conflict resolution
    # TODO: If key exists in both, sum the values
    merged4 = defaultdict(int, dict1)
    for k,v in dict2.items():
        merged4[k] += v
    print(f"Method 4 (custom merge): {merged4}")
    
    print() # <- I'm here 

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
    #dict_merging_patterns()
    #test_word_frequency()
    #performance_analysis()
    
    print("=" * 60)
    print("✅ Day 2 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Dict comprehensions are concise for transformations")
    print("2. defaultdict eliminates key existence checks")
    print("3. Choose the right pattern for readability and performance")
    print("4. defaultdict is typically faster for accumulation patterns")

