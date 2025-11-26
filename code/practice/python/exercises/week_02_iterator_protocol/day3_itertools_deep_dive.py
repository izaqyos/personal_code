"""
Week 2, Day 3: itertools Module Deep Dive

Learning Objectives:
- Master key itertools functions (islice, chain, groupby)
- Learn combinatoric iterators (product, permutations, combinations)
- Understand infinite iterators (count, cycle, repeat)
- Build efficient data processing pipelines

Time: 10-15 minutes
"""

import itertools
from typing import Iterable, List, Tuple

# ============================================================
# EXERCISE 1: islice - Slicing Iterators
# ============================================================

def islice_examples():
    """
    Use islice to slice iterators without loading into memory.
    
    islice(iterable, stop)
    islice(iterable, start, stop, step)
    """
    print("--- Exercise 1: islice ---")
    
    # Get first 5 items from infinite range
    print("First 5 items from range(1000000):")
    for num in itertools.islice(range(1000000), 5):
        print(f"  {num}")
    
    # Get items 10-15
    print("\nItems 10-15:")
    for num in itertools.islice(range(100), 10, 15):
        print(f"  {num}")
    
    # Every 3rd item from first 20
    print("\nEvery 3rd item from first 20:")
    for num in itertools.islice(range(100), 0, 20, 3):
        print(f"  {num}")
    
    # TODO: Get items 5-10 from a generator
    def fibonacci():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    
    print("\nFibonacci numbers 5-10:")
    for num in itertools.islice(fibonacci(), 5, 10):
        print(f"  {num}")
    
    print()

# ============================================================
# EXERCISE 2: chain - Combining Iterables
# ============================================================

def chain_examples():
    """
    Use chain to combine multiple iterables into one.
    
    chain(*iterables) - chains iterables together
    chain.from_iterable(iterable) - chains nested iterables
    """
    print("--- Exercise 2: chain ---")
    
    # Chain multiple lists
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    list3 = [7, 8, 9]
    
    print("Chaining three lists:")
    for num in itertools.chain(list1, list2, list3):
        print(f"  {num}", end=" ")
    print()
    
    # Chain from nested iterable
    nested = [[1, 2], [3, 4], [5, 6]]
    print("\nChaining from nested lists:")
    for num in itertools.chain.from_iterable(nested):
        print(f"  {num}", end=" ")
    print()
    
    # TODO: Chain different types of iterables
    print("\nChaining mixed types:")
    for item in itertools.chain(range(3), "abc", [10, 20]):
        print(f"  {item}", end=" ")
    print("\n")

# ============================================================
# EXERCISE 3: groupby - Grouping Consecutive Items
# ============================================================

def groupby_examples():
    """
    Use groupby to group consecutive items by a key function.
    
    IMPORTANT: groupby only groups CONSECUTIVE items!
    Sort first if needed.
    """
    print("--- Exercise 3: groupby ---")
    
    # Group consecutive identical items
    data = [1, 1, 1, 2, 2, 3, 3, 3, 3, 1, 1]
    print("Grouping consecutive identical items:")
    for key, group in itertools.groupby(data):
        print(f"  {key}: {list(group)}")
    
    # Group by property (must sort first!)
    people = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 30},
        {"name": "Diana", "age": 25},
    ]
    
    # TODO: Group by age (sort first!)
    print("\nGrouping people by age:")
    people_sorted = sorted(people, key=lambda p: p["age"])
    for age, group in itertools.groupby(people_sorted, key=lambda p: p["age"]):
        names = [p["name"] for p in group]
        print(f"  Age {age}: {names}")
    
    # Group strings by first letter
    words = ["apple", "apricot", "banana", "blueberry", "cherry", "coconut"]
    print("\nGrouping words by first letter:")
    for letter, group in itertools.groupby(sorted(words), key=lambda w: w[0]):
        print(f"  {letter}: {list(group)}")
    
    print()

# ============================================================
# EXERCISE 4: Combinatoric Iterators
# ============================================================

def combinatoric_examples():
    """
    Use product, permutations, combinations, combinations_with_replacement.
    """
    print("--- Exercise 4: Combinatoric Iterators ---")
    
    # product - Cartesian product
    print("product([1,2], ['a','b']):")
    for item in itertools.product([1, 2], ['a', 'b']):
        print(f"  {item}")
    
    # permutations - All orderings
    print("\npermutations([1,2,3], 2):")
    for perm in itertools.permutations([1, 2, 3], 2):
        print(f"  {perm}")
    
    # combinations - Choose r items (order doesn't matter)
    print("\ncombinations([1,2,3,4], 2):")
    for comb in itertools.combinations([1, 2, 3, 4], 2):
        print(f"  {comb}")
    
    # combinations_with_replacement - Can repeat items
    print("\ncombinations_with_replacement([1,2,3], 2):")
    for comb in itertools.combinations_with_replacement([1, 2, 3], 2):
        print(f"  {comb}")
    
    print()

# ============================================================
# EXERCISE 5: Infinite Iterators
# ============================================================

def infinite_iterators():
    """
    Use count, cycle, repeat for infinite sequences.
    """
    print("--- Exercise 5: Infinite Iterators ---")
    
    # count - Infinite counter
    print("count(10, 2) - first 5:")
    for i, num in enumerate(itertools.count(10, 2)):
        if i >= 5:
            break
        print(f"  {num}")
    
    # cycle - Cycle through items infinitely
    print("\ncycle(['A','B','C']) - first 7:")
    for i, item in enumerate(itertools.cycle(['A', 'B', 'C'])):
        if i >= 7:
            break
        print(f"  {item}", end=" ")
    print()
    
    # repeat - Repeat item n times (or infinitely)
    print("\nrepeat('X', 5):")
    for item in itertools.repeat('X', 5):
        print(f"  {item}", end=" ")
    print("\n")

# ============================================================
# EXERCISE 6: Filtering Iterators
# ============================================================

def filtering_examples():
    """
    Use filterfalse, takewhile, dropwhile, compress.
    """
    print("--- Exercise 6: Filtering Iterators ---")
    
    # filterfalse - Opposite of filter
    print("filterfalse(lambda x: x % 2 == 0, range(10)):")
    for num in itertools.filterfalse(lambda x: x % 2 == 0, range(10)):
        print(f"  {num}", end=" ")
    print()
    
    # takewhile - Take while condition is true
    print("\ntakewhile(lambda x: x < 5, [1,2,3,4,5,6,3,2,1]):")
    for num in itertools.takewhile(lambda x: x < 5, [1, 2, 3, 4, 5, 6, 3, 2, 1]):
        print(f"  {num}", end=" ")
    print()
    
    # dropwhile - Drop while condition is true, then take rest
    print("\ndropwhile(lambda x: x < 5, [1,2,3,4,5,6,3,2,1]):")
    for num in itertools.dropwhile(lambda x: x < 5, [1, 2, 3, 4, 5, 6, 3, 2, 1]):
        print(f"  {num}", end=" ")
    print()
    
    # compress - Filter by selector
    print("\ncompress('ABCDEF', [1,0,1,0,1,1]):")
    for char in itertools.compress('ABCDEF', [1, 0, 1, 0, 1, 1]):
        print(f"  {char}", end=" ")
    print("\n")

# ============================================================
# EXERCISE 7: Real-World Scenario - Data Processing
# ============================================================

def process_sales_data():
    """
    Process sales data using itertools.
    
    TODO: Use groupby, chain, and other itertools functions
    """
    print("--- Exercise 7: Sales Data Processing ---")
    
    # Sales data: (date, product, amount)
    sales = [
        ("2024-01-01", "laptop", 1200),
        ("2024-01-01", "mouse", 25),
        ("2024-01-01", "laptop", 1200),
        ("2024-01-02", "keyboard", 75),
        ("2024-01-02", "laptop", 1200),
        ("2024-01-02", "mouse", 25),
        ("2024-01-03", "laptop", 1200),
        ("2024-01-03", "keyboard", 75),
    ]
    
    # TODO: Group sales by date
    print("Sales by date:")
    sales_sorted = sorted(sales, key=lambda x: x[0])
    for date, group in itertools.groupby(sales_sorted, key=lambda x: x[0]):
        daily_sales = list(group)
        total = sum(sale[2] for sale in daily_sales)
        print(f"  {date}: ${total:,} ({len(daily_sales)} transactions)")
    
    # TODO: Group by product
    print("\nSales by product:")
    sales_by_product = sorted(sales, key=lambda x: x[1])
    for product, group in itertools.groupby(sales_by_product, key=lambda x: x[1]):
        product_sales = list(group)
        total = sum(sale[2] for sale in product_sales)
        count = len(product_sales)
        print(f"  {product}: ${total:,} ({count} units)")
    
    print()

# ============================================================
# EXERCISE 8: Pairwise Iteration
# ============================================================

def pairwise_examples():
    """
    Create sliding windows using itertools.
    
    TODO: Implement pairwise iteration
    """
    print("--- Exercise 8: Pairwise Iteration ---")
    
    # Python 3.10+ has itertools.pairwise
    # For older versions, implement manually
    def pairwise(iterable):
        """Return successive overlapping pairs"""
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)
    
    # TODO: Find differences between consecutive items
    numbers = [1, 3, 6, 10, 15, 21]
    print(f"Numbers: {numbers}")
    print("Differences:")
    for a, b in pairwise(numbers):
        print(f"  {b} - {a} = {b - a}")
    
    # Sliding window of size 3
    def sliding_window(iterable, n):
        """Return sliding window of size n"""
        iterators = itertools.tee(iterable, n)
        for i, it in enumerate(iterators):
            for _ in range(i):
                next(it, None)
        return zip(*iterators)
    
    print("\nSliding window of size 3:")
    for window in sliding_window(range(1, 8), 3):
        print(f"  {window}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Build a Data Pipeline
# ============================================================

def data_pipeline_challenge():
    """
    Build a complex data pipeline using multiple itertools functions.
    
    TODO: Process log data efficiently
    """
    print("--- Bonus Challenge: Data Pipeline ---")
    
    # Simulate log entries
    def generate_logs():
        """Generate sample log entries"""
        import random
        levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
        services = ["api", "database", "cache"]
        
        for i in range(100):
            level = random.choice(levels)
            service = random.choice(services)
            response_time = random.randint(10, 500)
            yield (level, service, response_time)
    
    # TODO: Build pipeline with itertools
    
    # 1. Filter only errors and warnings
    logs = generate_logs()
    important = itertools.filterfalse(
        lambda x: x[0] in ["INFO", "DEBUG"],
        logs
    )
    
    # 2. Take first 20
    limited = itertools.islice(important, 20)
    
    # 3. Group by service
    by_service = sorted(limited, key=lambda x: x[1])
    
    print("Important logs by service (first 20):")
    for service, group in itertools.groupby(by_service, key=lambda x: x[1]):
        logs_list = list(group)
        count = len(logs_list)
        avg_time = sum(log[2] for log in logs_list) / count if count > 0 else 0
        print(f"  {service}: {count} issues, avg response: {avg_time:.1f}ms")
    
    print()

# ============================================================
# PERFORMANCE TIPS
# ============================================================

def performance_tips():
    """
    Performance considerations when using itertools.
    """
    print("--- Performance Tips ---")
    
    print("✓ itertools functions are implemented in C - very fast")
    print("✓ All are lazy - don't consume memory until needed")
    print("✓ Chain multiple operations for efficient pipelines")
    print("✓ Use islice instead of list slicing for large data")
    print("✓ groupby requires sorted data - sort first!")
    print("✓ tee() creates independent iterators but uses memory")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    islice(iterable, n):
    - Time: O(n) to get n items
    - Space: O(1)
    
    chain(*iterables):
    - Time: O(1) to create, O(n) to consume all
    - Space: O(1)
    
    groupby(iterable, key):
    - Time: O(n) to iterate
    - Space: O(1) for iterator, O(k) for each group
    - MUST sort first for correct grouping: O(n log n)
    
    product(*iterables):
    - Time: O(n^m) where m is number of iterables
    - Space: O(1) for iterator
    
    permutations(iterable, r):
    - Time: O(n!/(n-r)!) items generated
    - Space: O(1) for iterator
    
    combinations(iterable, r):
    - Time: O(n!/(r!(n-r)!)) items generated
    - Space: O(1) for iterator
    
    Security Considerations:
    - Be careful with combinatoric functions - they grow FAST
    - Limit input size for product, permutations, combinations
    - Use islice to limit infinite iterators
    - Validate input before processing with itertools
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 2, Day 3: itertools Module Deep Dive")
    print("=" * 60)
    print()
    
    islice_examples()
    chain_examples()
    groupby_examples()
    combinatoric_examples()
    infinite_iterators()
    filtering_examples()
    process_sales_data()
    pairwise_examples()
    data_pipeline_challenge()
    performance_tips()
    
    print("=" * 60)
    print("✅ Day 3 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. itertools provides powerful, memory-efficient tools")
    print("2. All itertools functions are lazy (don't consume memory)")
    print("3. groupby requires sorted data for correct grouping")
    print("4. Chain itertools functions for efficient pipelines")

