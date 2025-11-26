"""
Week 4, Day 6: itertools for Functional Programming

Learning Objectives:
- Master itertools for functional operations
- Learn infinite iterators (count, cycle, repeat)
- Understand combinatoric iterators
- Practice functional data processing
- Build efficient iterator pipelines

Time: 10-15 minutes
"""

import itertools
from typing import Iterable

# ============================================================
# EXERCISE 1: Infinite Iterators
# ============================================================

def infinite_iterators():
    """
    Learn infinite iterators from itertools.
    
    count, cycle, repeat - generate infinite sequences
    """
    print("--- Exercise 1: Infinite Iterators ---")
    
    # count - infinite counter
    counter = itertools.count(start=10, step=2)
    print("count(10, 2):", list(itertools.islice(counter, 5)))
    
    # cycle - repeat sequence infinitely
    colors = itertools.cycle(['red', 'green', 'blue'])
    print("cycle(['red', 'green', 'blue']):", list(itertools.islice(colors, 7)))
    
    # repeat - repeat value
    repeated = itertools.repeat('hello', 3)
    print("repeat('hello', 3):", list(repeated))
    
    # Practical use: enumerate with custom start
    items = ['a', 'b', 'c']
    indexed = zip(itertools.count(1), items)
    print(f"\nIndexed from 1: {list(indexed)}")
    
    # Round-robin assignment
    tasks = ['Task1', 'Task2', 'Task3', 'Task4', 'Task5']
    workers = itertools.cycle(['Alice', 'Bob', 'Charlie'])
    assignments = list(zip(tasks, workers))
    print("\nRound-robin assignments:")
    for task, worker in assignments:
        print(f"  {task} → {worker}")
    
    print()

# ============================================================
# EXERCISE 2: Terminating Iterators
# ============================================================

def terminating_iterators():
    """
    Learn terminating iterators from itertools.
    
    accumulate, chain, compress, dropwhile, takewhile, etc.
    """
    print("--- Exercise 2: Terminating Iterators ---")
    
    # accumulate - running totals
    numbers = [1, 2, 3, 4, 5]
    totals = list(itertools.accumulate(numbers))
    print(f"accumulate({numbers}): {totals}")
    
    # accumulate with custom function
    products = list(itertools.accumulate(numbers, lambda x, y: x * y))
    print(f"accumulate (multiply): {products}")
    
    # chain - concatenate iterables
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    chained = list(itertools.chain(list1, list2))
    print(f"\nchain({list1}, {list2}): {chained}")
    
    # compress - filter by selector
    data = ['A', 'B', 'C', 'D', 'E']
    selectors = [1, 0, 1, 0, 1]
    filtered = list(itertools.compress(data, selectors))
    print(f"\ncompress({data}, {selectors}): {filtered}")
    
    # dropwhile - drop until condition false
    numbers = [1, 3, 5, 2, 4, 6, 1]
    dropped = list(itertools.dropwhile(lambda x: x < 5, numbers))
    print(f"\ndropwhile(< 5, {numbers}): {dropped}")
    
    # takewhile - take until condition false
    taken = list(itertools.takewhile(lambda x: x < 5, numbers))
    print(f"takewhile(< 5, {numbers}): {taken}")
    
    print()

# ============================================================
# EXERCISE 3: Combinatoric Iterators
# ============================================================

def combinatoric_iterators():
    """
    Learn combinatoric iterators.
    
    product, permutations, combinations, combinations_with_replacement
    """
    print("--- Exercise 3: Combinatoric Iterators ---")
    
    # product - Cartesian product
    colors = ['red', 'blue']
    sizes = ['S', 'M', 'L']
    products = list(itertools.product(colors, sizes))
    print(f"product({colors}, {sizes}):")
    for p in products:
        print(f"  {p}")
    
    # permutations - all orderings
    items = ['A', 'B', 'C']
    perms = list(itertools.permutations(items, 2))
    print(f"\npermutations({items}, 2): {perms}")
    
    # combinations - unique selections (order doesn't matter)
    combs = list(itertools.combinations(items, 2))
    print(f"combinations({items}, 2): {combs}")
    
    # combinations_with_replacement - allow repeats
    combs_rep = list(itertools.combinations_with_replacement(['A', 'B'], 2))
    print(f"combinations_with_replacement(['A', 'B'], 2): {combs_rep}")
    
    print()

# ============================================================
# EXERCISE 4: groupby for Data Aggregation
# ============================================================

def groupby_examples():
    """
    Use groupby for data aggregation.
    
    TODO: Group and aggregate data functionally
    """
    print("--- Exercise 4: groupby for Aggregation ---")
    
    # Group consecutive items
    data = [1, 1, 2, 2, 2, 3, 1, 1]
    groups = [(key, list(group)) for key, group in itertools.groupby(data)]
    print(f"groupby({data}):")
    for key, group in groups:
        print(f"  {key}: {group}")
    
    # Group by property
    words = ['apple', 'apricot', 'banana', 'blueberry', 'cherry']
    words_sorted = sorted(words, key=lambda w: w[0])
    
    print(f"\nGroup words by first letter:")
    for letter, group in itertools.groupby(words_sorted, key=lambda w: w[0]):
        print(f"  {letter}: {list(group)}")
    
    # Group students by grade
    students = [
        ('Alice', 'A'),
        ('Bob', 'B'),
        ('Charlie', 'A'),
        ('Diana', 'B'),
        ('Eve', 'A'),
    ]
    students_sorted = sorted(students, key=lambda s: s[1])
    
    print(f"\nStudents by grade:")
    for grade, group in itertools.groupby(students_sorted, key=lambda s: s[1]):
        names = [name for name, _ in group]
        print(f"  Grade {grade}: {names}")
    
    print()

# ============================================================
# EXERCISE 5: Building Functional Pipelines
# ============================================================

def functional_pipelines():
    """
    Build data processing pipelines with itertools.
    
    TODO: Create efficient iterator chains
    """
    print("--- Exercise 5: Functional Pipelines ---")
    
    # Pipeline: generate, filter, transform, accumulate
    pipeline = itertools.accumulate(
        map(lambda x: x ** 2,
            filter(lambda x: x % 2 == 0,
                   range(1, 11))),
        lambda x, y: x + y
    )
    
    result = list(pipeline)
    print("Pipeline: range(1,11) → filter(even) → square → accumulate")
    print(f"  Evens: {[x for x in range(1, 11) if x % 2 == 0]}")
    print(f"  Squared: {[x**2 for x in range(1, 11) if x % 2 == 0]}")
    print(f"  Accumulated: {result}")
    
    # Sliding window
    def sliding_window(iterable, n):
        """Create sliding window of size n"""
        iterators = itertools.tee(iterable, n)
        for i, it in enumerate(iterators):
            for _ in range(i):
                next(it, None)
        return zip(*iterators)
    
    data = [1, 2, 3, 4, 5, 6]
    windows = list(sliding_window(data, 3))
    print(f"\nSliding window (size 3) of {data}:")
    for window in windows:
        print(f"  {window}")
    
    print()

# ============================================================
# EXERCISE 6: Real-World Scenario - Log Processing
# ============================================================

def process_logs():
    """
    Process log data using itertools.
    
    TODO: Analyze logs functionally
    """
    print("--- Exercise 6: Log Processing ---")
    
    # Simulated log entries
    logs = [
        ('2024-01-01 10:00', 'INFO', 'Server started'),
        ('2024-01-01 10:01', 'INFO', 'Request received'),
        ('2024-01-01 10:02', 'ERROR', 'Connection failed'),
        ('2024-01-01 10:03', 'ERROR', 'Timeout'),
        ('2024-01-01 10:04', 'INFO', 'Request completed'),
        ('2024-01-01 10:05', 'WARNING', 'High memory usage'),
        ('2024-01-01 10:06', 'ERROR', 'Database error'),
    ]
    
    # Filter errors only
    errors = list(filter(lambda log: log[1] == 'ERROR', logs))
    print(f"Errors ({len(errors)}):")
    for timestamp, level, message in errors:
        print(f"  [{timestamp}] {message}")
    
    # Group by level
    logs_sorted = sorted(logs, key=lambda log: log[1])
    print("\nLogs by level:")
    for level, group in itertools.groupby(logs_sorted, key=lambda log: log[1]):
        count = len(list(group))
        print(f"  {level}: {count} entries")
    
    # Running count of errors
    is_error = (1 if log[1] == 'ERROR' else 0 for log in logs)
    error_counts = list(itertools.accumulate(is_error))
    print(f"\nRunning error count: {error_counts}")
    
    print()

# ============================================================
# EXERCISE 7: Pairwise and Batching
# ============================================================

def pairwise_and_batching():
    """
    Create pairwise and batched iterators.
    
    TODO: Implement useful iterator patterns
    """
    print("--- Exercise 7: Pairwise and Batching ---")
    
    # Pairwise (Python 3.10+) or custom
    def pairwise(iterable):
        """Return successive overlapping pairs"""
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)
    
    data = [1, 2, 3, 4, 5]
    pairs = list(pairwise(data))
    print(f"pairwise({data}): {pairs}")
    
    # Calculate differences
    differences = [b - a for a, b in pairs]
    print(f"Differences: {differences}")
    
    # Batching
    def batched(iterable, n):
        """Batch data into tuples of length n"""
        it = iter(iterable)
        while True:
            batch = tuple(itertools.islice(it, n))
            if not batch:
                return
            yield batch
    
    data = range(1, 11)
    batches = list(batched(data, 3))
    print(f"\nbatched(range(1,11), 3): {batches}")
    
    # Flatten batches
    flattened = list(itertools.chain.from_iterable(batches))
    print(f"Flattened: {flattened}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Custom Iterator Combinators
# ============================================================

def custom_combinators():
    """
    Build custom iterator combinators.
    
    TODO: Create reusable iterator utilities
    """
    print("--- Bonus Challenge: Custom Combinators ---")
    
    def take(n, iterable):
        """Take first n elements"""
        return itertools.islice(iterable, n)
    
    def drop(n, iterable):
        """Drop first n elements"""
        return itertools.islice(iterable, n, None)
    
    def partition(predicate, iterable):
        """Partition into two lists based on predicate"""
        t1, t2 = itertools.tee(iterable)
        return (filter(predicate, t1), itertools.filterfalse(predicate, t2))
    
    # Test take and drop
    data = range(1, 11)
    print(f"take(3, {list(data)}): {list(take(3, data))}")
    print(f"drop(3, {list(data)}): {list(drop(3, range(1, 11)))}")
    
    # Test partition
    numbers = range(1, 11)
    evens, odds = partition(lambda x: x % 2 == 0, numbers)
    print(f"\npartition(even, {list(range(1, 11))}):")
    print(f"  Evens: {list(evens)}")
    print(f"  Odds: {list(odds)}")
    
    # Interleave
    def interleave(*iterables):
        """Interleave multiple iterables"""
        return (item for items in itertools.zip_longest(*iterables, fillvalue=None)
                for item in items if item is not None)
    
    list1 = [1, 2, 3]
    list2 = ['a', 'b', 'c']
    interleaved = list(interleave(list1, list2))
    print(f"\ninterleave({list1}, {list2}): {interleaved}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    itertools Iterators:
    - All return iterators (lazy evaluation)
    - Space: O(1) for iterator itself
    - Time: O(1) per element
    
    Specific Functions:
    - count/cycle/repeat: O(1) per element, infinite
    - accumulate: O(n) total, O(1) per element
    - chain: O(1) per element
    - groupby: O(n), requires sorted input
    - product: O(n^k) where k = number of iterables
    - permutations: O(n!)
    - combinations: O(n choose k)
    
    Benefits:
    - Memory efficient (lazy)
    - Composable
    - Fast (C implementation)
    - Functional style
    - No intermediate lists
    
    Use Cases:
    - Large dataset processing
    - Infinite sequences
    - Combinatorial problems
    - Data pipelines
    - Functional programming
    
    Best Practices:
    - Use islice to limit infinite iterators
    - Sort before groupby
    - Use tee carefully (memory)
    - Chain operations for efficiency
    - Consider memory vs readability
    
    Common Patterns:
    - Pipeline: chain → filter → map → accumulate
    - Sliding windows: tee + zip
    - Batching: islice in loop
    - Pairwise: tee + zip
    - Flatten: chain.from_iterable
    
    Security Considerations:
    - Limit infinite iterators
    - Validate input sizes
    - Be careful with combinatorics (exponential)
    - Consider memory for tee
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 4, Day 6: itertools for Functional Programming")
    print("=" * 60)
    print()
    
    infinite_iterators()
    terminating_iterators()
    combinatoric_iterators()
    groupby_examples()
    functional_pipelines()
    process_logs()
    pairwise_and_batching()
    custom_combinators()
    
    print("=" * 60)
    print("✅ Day 6 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. itertools provides efficient iterator building blocks")
    print("2. Lazy evaluation saves memory")
    print("3. Combinators enable functional pipelines")
    print("4. groupby requires sorted input")

