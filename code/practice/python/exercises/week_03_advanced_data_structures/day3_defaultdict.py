"""
Week 3, Day 3: defaultdict - Avoiding KeyError Gracefully

Learning Objectives:
- Master defaultdict for automatic default values
- Learn common factory functions (list, int, set)
- Understand when to use defaultdict vs regular dict
- Practice grouping and accumulation patterns

Time: 10-15 minutes
"""

from collections import defaultdict
from typing import List, Dict
import time

# ============================================================
# EXERCISE 1: defaultdict Basics
# ============================================================

def defaultdict_basics():
    """
    Learn basic defaultdict operations.
    
    defaultdict: dict subclass that calls factory function for missing keys
    """
    print("--- Exercise 1: defaultdict Basics ---")
    
    # Regular dict - KeyError
    print("Regular dict:")
    regular_dict = {}
    try:
        value = regular_dict['missing_key']
    except KeyError as e:
        print(f"  KeyError: {e}")
    
    # defaultdict with list
    print("\ndefaultdict(list):")
    dd_list = defaultdict(list)
    dd_list['key'].append(1)  # No KeyError!
    print(f"  After append: {dict(dd_list)}")
    
    # defaultdict with int
    print("\ndefaultdict(int):")
    dd_int = defaultdict(int)
    dd_int['count'] += 1  # Starts at 0
    print(f"  After increment: {dict(dd_int)}")
    
    # defaultdict with set
    print("\ndefaultdict(set):")
    dd_set = defaultdict(set)
    dd_set['items'].add('a')
    dd_set['items'].add('b')
    print(f"  After adds: {dict(dd_set)}")
    
    print()

# ============================================================
# EXERCISE 2: Grouping with defaultdict(list)
# ============================================================

def grouping_examples():
    """
    Use defaultdict(list) for grouping data.
    
    TODO: Practice grouping patterns
    """
    print("--- Exercise 2: Grouping with defaultdict(list) ---")
    
    # Group students by grade
    students = [
        ('Alice', 'A'),
        ('Bob', 'B'),
        ('Charlie', 'A'),
        ('Diana', 'C'),
        ('Eve', 'B'),
        ('Frank', 'A'),
    ]
    
    # With regular dict (verbose)
    print("Regular dict approach:")
    grades_regular = {}
    for name, grade in students:
        if grade not in grades_regular:
            grades_regular[grade] = []
        grades_regular[grade].append(name)
    print(f"  {grades_regular}")
    
    # With defaultdict (clean)
    print("\ndefaultdict approach:")
    grades_default = defaultdict(list)
    for name, grade in students:
        grades_default[grade].append(name)
    print(f"  {dict(grades_default)}")
    
    print()

# ============================================================
# EXERCISE 3: Counting with defaultdict(int)
# ============================================================

def counting_examples():
    """
    Use defaultdict(int) for counting.
    
    TODO: Practice counting patterns
    """
    print("--- Exercise 3: Counting with defaultdict(int) ---")
    
    text = "the quick brown fox jumps over the lazy dog"
    
    # Count word frequency
    word_count = defaultdict(int)
    for word in text.split():
        word_count[word] += 1
    
    print("Word frequencies:")
    for word, count in sorted(word_count.items()):
        print(f"  {word}: {count}")
    
    # Count letter frequency
    letter_count = defaultdict(int)
    for char in text:
        if char.isalpha():
            letter_count[char.lower()] += 1
    
    print("\nMost common letters:")
    top_letters = sorted(letter_count.items(), key=lambda x: x[1], reverse=True)[:5]
    for letter, count in top_letters:
        print(f"  {letter}: {count}")
    
    print()

# ============================================================
# EXERCISE 4: Nested defaultdict
# ============================================================

def nested_defaultdict():
    """
    Create nested defaultdict structures.
    
    TODO: Practice nested defaultdict patterns
    """
    print("--- Exercise 4: Nested defaultdict ---")
    
    # Two-level grouping: department -> role -> [employees]
    employees = [
        ('Alice', 'Engineering', 'Developer'),
        ('Bob', 'Engineering', 'Manager'),
        ('Charlie', 'Engineering', 'Developer'),
        ('Diana', 'Sales', 'Manager'),
        ('Eve', 'Sales', 'Representative'),
        ('Frank', 'Engineering', 'Developer'),
    ]
    
    # Nested defaultdict
    org = defaultdict(lambda: defaultdict(list))
    
    for name, dept, role in employees:
        org[dept][role].append(name)
    
    print("Organization structure:")
    for dept, roles in org.items():
        print(f"\n{dept}:")
        for role, people in roles.items():
            print(f"  {role}: {people}")
    
    print()

# ============================================================
# EXERCISE 5: defaultdict with Custom Factory
# ============================================================

def custom_factory_examples():
    """
    Use custom factory functions with defaultdict.
    
    TODO: Practice custom factories
    """
    print("--- Exercise 5: Custom Factory Functions ---")
    
    # Factory that returns a dict with default structure
    def user_factory():
        return {'name': '', 'age': 0, 'email': ''}
    
    users = defaultdict(user_factory)
    users[1]['name'] = 'Alice'
    users[1]['age'] = 30
    users[2]['name'] = 'Bob'
    
    print("Users with default structure:")
    for user_id, user_data in users.items():
        print(f"  User {user_id}: {user_data}")
    
    # Factory for statistics
    def stats_factory():
        return {'count': 0, 'sum': 0, 'min': float('inf'), 'max': float('-inf')}
    
    stats = defaultdict(stats_factory)
    
    # Track statistics per category
    data = [
        ('A', 10), ('B', 20), ('A', 15), ('B', 25), ('A', 5)
    ]
    
    for category, value in data:
        stats[category]['count'] += 1
        stats[category]['sum'] += value
        stats[category]['min'] = min(stats[category]['min'], value)
        stats[category]['max'] = max(stats[category]['max'], value)
    
    print("\nStatistics by category:")
    for category, s in stats.items():
        avg = s['sum'] / s['count']
        print(f"  {category}: count={s['count']}, avg={avg:.1f}, "
              f"min={s['min']}, max={s['max']}")
    
    print()

# ============================================================
# EXERCISE 6: Real-World Scenario - Log Analysis
# ============================================================

def analyze_server_logs():
    """
    Analyze server logs using defaultdict.
    
    TODO: Track errors by service and endpoint
    """
    print("--- Exercise 6: Server Log Analysis ---")
    
    # Simulated log entries: (timestamp, service, endpoint, status, response_time)
    logs = [
        (1000, 'api', '/users', 200, 45),
        (1001, 'api', '/users', 404, 10),
        (1002, 'database', '/query', 200, 120),
        (1003, 'api', '/posts', 500, 200),
        (1004, 'cache', '/get', 200, 5),
        (1005, 'api', '/users', 200, 50),
        (1006, 'database', '/query', 500, 300),
        (1007, 'api', '/posts', 500, 180),
    ]
    
    # Group errors by service
    errors_by_service = defaultdict(list)
    
    # Track response times by endpoint
    response_times = defaultdict(list)
    
    # Count status codes
    status_counts = defaultdict(int)
    
    for timestamp, service, endpoint, status, response_time in logs:
        # Track errors
        if status >= 400:
            errors_by_service[service].append((endpoint, status))
        
        # Track response times
        response_times[endpoint].append(response_time)
        
        # Count statuses
        status_counts[status] += 1
    
    # Report results
    print("Errors by service:")
    for service, errors in errors_by_service.items():
        print(f"  {service}: {len(errors)} errors")
        for endpoint, status in errors:
            print(f"    {endpoint} → {status}")
    
    print("\nAverage response times:")
    for endpoint, times in response_times.items():
        avg = sum(times) / len(times)
        print(f"  {endpoint}: {avg:.1f}ms")
    
    print("\nStatus code distribution:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    
    print()

# ============================================================
# EXERCISE 7: Graph Representation
# ============================================================

def graph_with_defaultdict():
    """
    Represent a graph using defaultdict.
    
    TODO: Build adjacency list representation
    """
    print("--- Exercise 7: Graph Representation ---")
    
    # Build graph as adjacency list
    graph = defaultdict(list)
    
    # Add edges
    edges = [
        ('A', 'B'), ('A', 'C'),
        ('B', 'D'), ('B', 'E'),
        ('C', 'F'),
        ('D', 'E'),
    ]
    
    for src, dst in edges:
        graph[src].append(dst)
    
    print("Graph adjacency list:")
    for node, neighbors in sorted(graph.items()):
        print(f"  {node} → {neighbors}")
    
    # Find all nodes (including isolated ones)
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)
    
    print(f"\nAll nodes: {sorted(all_nodes)}")
    print(f"Isolated nodes: {sorted(all_nodes - set(graph.keys()))}")
    
    print()

# ============================================================
# EXERCISE 8: Performance Comparison
# ============================================================

def performance_comparison():
    """
    Compare defaultdict vs regular dict performance.
    """
    print("--- Exercise 8: Performance Comparison ---")
    
    words = ['apple', 'banana', 'apple', 'cherry'] * 10000
    
    # Regular dict with if-else
    start = time.perf_counter()
    count1 = {}
    for word in words:
        if word in count1:
            count1[word] += 1
        else:
            count1[word] = 1
    time1 = time.perf_counter() - start
    
    # Regular dict with get()
    start = time.perf_counter()
    count2 = {}
    for word in words:
        count2[word] = count2.get(word, 0) + 1
    time2 = time.perf_counter() - start
    
    # defaultdict
    start = time.perf_counter()
    count3 = defaultdict(int)
    for word in words:
        count3[word] += 1
    time3 = time.perf_counter() - start
    
    print(f"Counting {len(words):,} words:")
    print(f"  if-else:      {time1:.6f}s")
    print(f"  get():        {time2:.6f}s ({time1/time2:.2f}x faster)")
    print(f"  defaultdict:  {time3:.6f}s ({time1/time3:.2f}x faster)")
    
    print()

# ============================================================
# BONUS CHALLENGE: Tree Structure
# ============================================================

def build_tree_structure():
    """
    Build a tree structure using nested defaultdict.
    
    TODO: Create file system tree
    """
    print("--- Bonus Challenge: Tree Structure ---")
    
    # Recursive defaultdict for tree
    def tree():
        return defaultdict(tree)
    
    # Build file system structure
    fs = tree()
    
    # Add files and directories
    fs['home']['user']['documents']['file1.txt'] = 'content1'
    fs['home']['user']['documents']['file2.txt'] = 'content2'
    fs['home']['user']['pictures']['photo.jpg'] = 'image_data'
    fs['etc']['config.conf'] = 'config_data'
    
    # Print tree structure
    def print_tree(d, indent=0):
        for key, value in sorted(d.items()):
            print('  ' * indent + f"├─ {key}")
            if isinstance(value, defaultdict):
                print_tree(value, indent + 1)
            else:
                print('  ' * (indent + 1) + f"   ({value})")
    
    print("File system tree:")
    print_tree(fs)
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    defaultdict Operations:
    - Access/Insert: O(1) average (same as dict)
    - No KeyError overhead for missing keys
    - Factory function call: O(1) typically
    
    vs Regular dict:
    - Same time complexity
    - Cleaner code (no if-else checks)
    - Slightly more memory (stores factory function)
    
    Common Factory Functions:
    - list: O(1) to create empty list
    - int: O(1) to create 0
    - set: O(1) to create empty set
    - lambda: O(1) for simple factories
    
    Benefits:
    - Eliminates KeyError checks
    - Cleaner, more readable code
    - Perfect for grouping and counting
    - Natural for nested structures
    
    Use Cases:
    - Grouping data (defaultdict(list))
    - Counting (defaultdict(int))
    - Unique items per key (defaultdict(set))
    - Nested structures (defaultdict(dict))
    - Graph adjacency lists
    - Inverted indices
    
    When NOT to Use:
    - Need to distinguish missing vs default value
    - Want KeyError for debugging
    - Simple one-time operations
    - Need to serialize (pickle handles it, JSON doesn't)
    
    Security Considerations:
    - Factory function should be simple and safe
    - Be careful with lambda factories (harder to debug)
    - Validate input keys to prevent memory exhaustion
    - Consider maxsize limits for user-facing collections
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 3, Day 3: defaultdict")
    print("=" * 60)
    print()
    
    defaultdict_basics()
    grouping_examples()
    counting_examples()
    nested_defaultdict()
    custom_factory_examples()
    analyze_server_logs()
    graph_with_defaultdict()
    performance_comparison()
    build_tree_structure()
    
    print("=" * 60)
    print("✅ Day 3 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. defaultdict eliminates KeyError for missing keys")
    print("2. Use list for grouping, int for counting, set for unique items")
    print("3. Cleaner code than if-else or get() patterns")
    print("4. Perfect for nested structures with lambda factories")

