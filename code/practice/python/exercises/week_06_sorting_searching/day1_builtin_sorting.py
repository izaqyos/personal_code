"""
Week 6, Day 1: Built-in Sorting (sorted, list.sort, key functions)

Learning Objectives:
- Master sorted() and list.sort()
- Learn key functions for custom sorting
- Understand stable sorting
- Practice sorting complex data structures
- Compare sorting performance

Time: 10-15 minutes
"""

import operator
from functools import cmp_to_key
import time

# ============================================================
# EXERCISE 1: sorted() vs list.sort()
# ============================================================

def sorted_vs_sort():
    """
    Learn differences between sorted() and list.sort().
    
    sorted(): Returns new sorted list
    list.sort(): Sorts in-place, returns None
    """
    print("--- Exercise 1: sorted() vs list.sort() ---")
    
    # Original list
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    
    # sorted() - returns new list
    sorted_nums = sorted(numbers)
    print(f"Original: {numbers}")
    print(f"sorted(): {sorted_nums}")
    print(f"Original unchanged: {numbers}")
    
    # list.sort() - in-place
    numbers.sort()
    print(f"\nAfter list.sort(): {numbers}")
    
    # sorted() works on any iterable
    print(f"\nsorted('python'): {sorted('python')}")
    print(f"sorted({{3, 1, 4}}): {sorted({3, 1, 4})}")
    
    print("\n💡 Use sorted() for new list, list.sort() for in-place")
    
    print()

# ============================================================
# EXERCISE 2: Reverse Sorting
# ============================================================

def reverse_sorting():
    """
    Sort in descending order.
    
    TODO: Practice reverse parameter
    """
    print("--- Exercise 2: Reverse Sorting ---")
    
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    
    # Ascending (default)
    asc = sorted(numbers)
    print(f"Ascending: {asc}")
    
    # Descending
    desc = sorted(numbers, reverse=True)
    print(f"Descending: {desc}")
    
    # Words
    words = ['banana', 'apple', 'cherry', 'date']
    print(f"\nWords ascending: {sorted(words)}")
    print(f"Words descending: {sorted(words, reverse=True)}")
    
    print()

# ============================================================
# EXERCISE 3: Key Functions
# ============================================================

def key_functions():
    """
    Use key parameter for custom sorting.
    
    key: Function to extract comparison key from each element
    """
    print("--- Exercise 3: Key Functions ---")
    
    words = ['banana', 'pie', 'Washington', 'book']
    
    # Sort by length
    by_length = sorted(words, key=len)
    print(f"By length: {by_length}")
    
    # Sort case-insensitive
    by_alpha = sorted(words, key=str.lower)
    print(f"Case-insensitive: {by_alpha}")
    
    # Sort by last letter
    by_last = sorted(words, key=lambda w: w[-1])
    print(f"By last letter: {by_last}")
    
    # Sort by length, then alphabetically
    by_len_alpha = sorted(words, key=lambda w: (len(w), w.lower()))
    print(f"By length, then alpha: {by_len_alpha}")
    
    print()

# ============================================================
# EXERCISE 4: Sorting Complex Data
# ============================================================

def sorting_complex_data():
    """
    Sort lists of dictionaries and tuples.
    
    TODO: Practice sorting structured data
    """
    print("--- Exercise 4: Sorting Complex Data ---")
    
    students = [
        {'name': 'Alice', 'grade': 85, 'age': 20},
        {'name': 'Bob', 'grade': 92, 'age': 19},
        {'name': 'Charlie', 'grade': 78, 'age': 21},
        {'name': 'Diana', 'grade': 95, 'age': 20},
    ]
    
    # Sort by grade (descending)
    by_grade = sorted(students, key=lambda s: s['grade'], reverse=True)
    print("By grade (high to low):")
    for s in by_grade:
        print(f"  {s['name']}: {s['grade']}")
    
    # Sort by age, then grade
    by_age_grade = sorted(students, key=lambda s: (s['age'], -s['grade']))
    print("\nBy age, then grade:")
    for s in by_age_grade:
        print(f"  {s['name']}: age {s['age']}, grade {s['grade']}")
    
    # Using operator.itemgetter (faster)
    by_name = sorted(students, key=operator.itemgetter('name'))
    print("\nBy name (using itemgetter):")
    for s in by_name:
        print(f"  {s['name']}")
    
    print()

# ============================================================
# EXERCISE 5: Stable Sorting
# ============================================================

def stable_sorting():
    """
    Understand stable sorting behavior.
    
    Stable: Equal elements maintain relative order
    """
    print("--- Exercise 5: Stable Sorting ---")
    
    # Data with ties
    data = [
        ('Alice', 'A', 85),
        ('Bob', 'B', 92),
        ('Charlie', 'A', 78),
        ('Diana', 'B', 95),
        ('Eve', 'A', 88),
    ]
    
    print("Original order:")
    for name, section, grade in data:
        print(f"  {name} (Section {section}): {grade}")
    
    # Sort by section (stable - maintains grade order within section)
    by_section = sorted(data, key=lambda x: x[1])
    print("\nSorted by section (stable):")
    for name, section, grade in by_section:
        print(f"  {name} (Section {section}): {grade}")
    
    # Multi-level sort using stability
    # First sort by grade, then by section
    by_grade = sorted(data, key=lambda x: x[2], reverse=True)
    by_section_then_grade = sorted(by_grade, key=lambda x: x[1])
    
    print("\nBy section, then grade (using stability):")
    for name, section, grade in by_section_then_grade:
        print(f"  {name} (Section {section}): {grade}")
    
    print()

# ============================================================
# EXERCISE 6: operator Module for Sorting
# ============================================================

def operator_module_sorting():
    """
    Use operator module for efficient sorting.
    
    operator.itemgetter, operator.attrgetter
    """
    print("--- Exercise 6: operator Module ---")
    
    # itemgetter for sequences
    pairs = [(1, 'one'), (3, 'three'), (2, 'two')]
    
    # Sort by first element
    by_first = sorted(pairs, key=operator.itemgetter(0))
    print(f"By first: {by_first}")
    
    # Sort by second element
    by_second = sorted(pairs, key=operator.itemgetter(1))
    print(f"By second: {by_second}")
    
    # Multiple keys
    data = [
        ('Alice', 85, 20),
        ('Bob', 92, 19),
        ('Charlie', 85, 21),
    ]
    by_grade_age = sorted(data, key=operator.itemgetter(1, 2))
    print(f"\nBy grade, then age: {by_grade_age}")
    
    # attrgetter for objects
    from collections import namedtuple
    Student = namedtuple('Student', ['name', 'grade'])
    students = [
        Student('Alice', 85),
        Student('Bob', 92),
        Student('Charlie', 78),
    ]
    
    by_grade_attr = sorted(students, key=operator.attrgetter('grade'))
    print(f"\nBy grade (attrgetter): {by_grade_attr}")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - Log Sorting
# ============================================================

def sort_logs():
    """
    Sort log entries by timestamp and severity.
    
    TODO: Multi-level sorting of logs
    """
    print("--- Exercise 7: Log Sorting ---")
    
    logs = [
        {'timestamp': '2024-01-01 10:05', 'level': 'ERROR', 'message': 'Connection failed'},
        {'timestamp': '2024-01-01 10:01', 'level': 'INFO', 'message': 'Server started'},
        {'timestamp': '2024-01-01 10:03', 'level': 'WARNING', 'message': 'High memory'},
        {'timestamp': '2024-01-01 10:02', 'level': 'ERROR', 'message': 'Timeout'},
        {'timestamp': '2024-01-01 10:04', 'level': 'INFO', 'message': 'Request processed'},
    ]
    
    # Sort by timestamp
    by_time = sorted(logs, key=lambda log: log['timestamp'])
    print("By timestamp:")
    for log in by_time:
        print(f"  [{log['timestamp']}] {log['level']}: {log['message']}")
    
    # Sort by severity (custom order)
    severity_order = {'ERROR': 0, 'WARNING': 1, 'INFO': 2}
    by_severity = sorted(logs, key=lambda log: severity_order[log['level']])
    print("\nBy severity:")
    for log in by_severity:
        print(f"  [{log['timestamp']}] {log['level']}: {log['message']}")
    
    # Sort by severity, then timestamp
    by_severity_time = sorted(
        logs,
        key=lambda log: (severity_order[log['level']], log['timestamp'])
    )
    print("\nBy severity, then timestamp:")
    for log in by_severity_time:
        print(f"  [{log['timestamp']}] {log['level']}: {log['message']}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Custom Comparison Function
# ============================================================

def custom_comparison():
    """
    Use cmp_to_key for complex comparisons.
    
    TODO: Implement custom comparison logic
    """
    print("--- Bonus Challenge: Custom Comparison ---")
    
    def compare_versions(v1, v2):
        """Compare version strings like '1.2.3'"""
        parts1 = [int(x) for x in v1.split('.')]
        parts2 = [int(x) for x in v2.split('.')]
        
        if parts1 < parts2:
            return -1
        elif parts1 > parts2:
            return 1
        return 0
    
    versions = ['1.10.0', '1.2.0', '1.2.1', '2.0.0', '1.9.0']
    
    sorted_versions = sorted(versions, key=cmp_to_key(compare_versions))
    print(f"Versions: {versions}")
    print(f"Sorted: {sorted_versions}")
    
    # Alternative: use tuple key
    sorted_versions2 = sorted(
        versions,
        key=lambda v: tuple(int(x) for x in v.split('.'))
    )
    print(f"Sorted (tuple key): {sorted_versions2}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Python's sort (Timsort):
    - Best case: O(n) - already sorted
    - Average case: O(n log n)
    - Worst case: O(n log n)
    - Space: O(n)
    - Stable: Yes
    
    sorted() vs list.sort():
    - sorted(): O(n) extra space for new list
    - list.sort(): O(n) space for sorting, no new list
    
    Key Function:
    - Called once per element: O(n) total
    - Should be O(1) if possible
    - Avoid expensive key functions
    
    Benefits:
    - Timsort is adaptive (fast on partially sorted)
    - Stable sorting preserves order
    - Key functions are flexible
    - operator module is faster than lambda
    
    Use Cases:
    - sorted(): Need original list, sort any iterable
    - list.sort(): In-place, save memory
    - key: Custom sorting logic
    - reverse: Descending order
    
    Best Practices:
    - Use operator.itemgetter/attrgetter when possible
    - Keep key functions simple
    - Use tuple keys for multi-level sorting
    - Consider stability for tied elements
    
    Performance Tips:
    - operator module faster than lambda
    - Avoid repeated sorting (cache if needed)
    - Use key instead of cmp (Python 3)
    - Consider partial sorting (heapq) for top-k
    
    Security Considerations:
    - Validate input data
    - Be careful with user-provided key functions
    - Consider memory limits for large datasets
    - Watch for worst-case inputs
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 6, Day 1: Built-in Sorting")
    print("=" * 60)
    print()
    
    sorted_vs_sort()
    reverse_sorting()
    key_functions()
    sorting_complex_data()
    stable_sorting()
    operator_module_sorting()
    sort_logs()
    custom_comparison()
    
    print("=" * 60)
    print("✅ Day 1 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. sorted() returns new list, list.sort() is in-place")
    print("2. key parameter for custom sorting")
    print("3. Python uses stable Timsort (O(n log n))")
    print("4. operator module faster than lambda for keys")

