"""
Week 1 Day 1: List Comprehensions vs Generator Expressions
Date: [Fill in when you start]
Time: 10-15 minutes

Concept: Understanding memory and performance trade-offs between
list comprehensions and generator expressions.

Goal: 
- Compare memory usage
- Compare execution speed
- Understand when to use each
"""

import sys
import time
import tracemalloc
from collections import Counter

# ============================================================
# EXERCISE 1: Basic Comparison
# ============================================================

one_million = 1_000_000
def compare_memory_usage(n=one_million):
    """
    Compare memory usage between list comprehension and generator.
    
    TODO: Implement this function to:
    1. Create a list of squares using list comprehension
    2. Create a generator of squares using generator expression
    3. Measure memory used by each
    4. Print results
    
    Hint: Use sys.getsizeof() for rough estimates
    Hint: Use tracemalloc for accurate memory profiling
    """
    list_squares = [x**2 for x in range(n)]
    gen_squares = (x**2 for x in range(n))
    print("Comaprisons of list and generator:")
    print("--------------------------------")
    print("usage example:")
    print("list:")
    for i in list_squares[:10]:
        print(i, end=" ")

    print()
    print("generator:")
    i = 0
    while i<10:
        print(next(gen_squares), end=" ")
        i += 1

    print()
    print("Memory usage:")
    print(f"list: {sys.getsizeof(list_squares)} roughly bytes")
    print(f"generator: {sys.getsizeof(gen_squares)} roughly bytes")
    print("--------------------------------")

# ============================================================
# EXERCISE 2: Performance Comparison
# ============================================================

def compare_speed(n=one_million):
    """
    Compare execution speed for common operations.
    
    TODO: Compare time to:
    1. Create and sum all values (list vs generator)
    2. Get first 10 values
    3. Filter and transform a pipeline
    
    Hint: Use time.perf_counter() for timing
    """
    print("Time comparisons of list and generator, for creation, iteration and sum, and filter and transform pipeline:")

    print("creation:")
    print("list:")
    start_time = time.perf_counter()
    list_n = [x for x in range(n)]
    end_time = time.perf_counter()
    print(f"list creation: {end_time - start_time:.4f} seconds")
    print("generator:")
    start_time = time.perf_counter()
    gen_n = (x for x in range(n))
    end_time = time.perf_counter()
    print(f"generator creation: {end_time - start_time:.4f} seconds")

    print("iteration and sum:")
    print("list:")
    start_time = time.perf_counter()
    sum = 0
    for n in list_n:
        sum += n
    end_time = time.perf_counter()
    print(f"list iteration and sum took {end_time - start_time:.4f} seconds")

    gen_n = (x for x in range(n))
    print("generator:")
    start_time = time.perf_counter()
    sum = 0
    for n in gen_n:
        sum += n
    end_time = time.perf_counter()
    print(f"generator iteration and sum took {end_time - start_time:.4f} seconds")

    print("filter and transform pipeline:")
    print("list:")
    start_time = time.perf_counter()
    numbers = [n*n*n for n in list_n if n % 2 == 0]
    end_time = time.perf_counter()
    print(f"list filter and transform pipeline took {end_time - start_time:.4f} seconds")

    print("generator:")
    start_time = time.perf_counter()
    numbers_gen = (n*n*n for n in list_n if n % 2 == 0)
    end_time = time.perf_counter()
    print(f"generator filter and transform pipeline took {end_time - start_time:.4f} seconds")
    print("--------------------------------")

# ============================================================
# EXERCISE 3: Reusability
# ============================================================

def test_reusability():
    """
    Demonstrate that generators are single-use while lists are reusable.
    
    TODO: 
    1. Create a generator and try to iterate twice
    2. Create a list and iterate twice
    3. Show how to convert generator to list when needed
    """
    print("Reusability comparisons of list and generator:")
    print("--------------------------------")
    print("generator:")
    gen_n = (num**4 for num in range(100) if num % 5 == 0)
    for num in gen_n:
        print(num, end=" ")
    print()
    print("list:")
    list_n = [num**4 for num in range(100) if num % 5 == 0]
    for num in list_n:
        print(num, end=" ")
    print()
    print("try to reuse the generator. iteration will do nothing. calling next() will raise StopIteration.")
    #next(gen_n)
    for num in gen_n:
        print(num, end=" ")
    print()
    print("try to reuse the list:")
    for num in list_n:
        print(num, end=" ")
    print()
    print("--------------------------------")

# ============================================================
# EXERCISE 4: Real-World Scenario
# ============================================================

def process_large_file_simulation():
    """
    Simulate processing a large file (1 million lines).
    
    Scenario: Read lines, filter those starting with 'ERROR', 
              extract error codes, count frequency.
    
    TODO: Implement using:
    1. List comprehension approach
    2. Generator expression approach
    3. Compare memory usage
    
    Question: When would you use each approach?
    """
    
    # Simulate 1 million log lines
    def generate_logs(n):
        """Simulate log entries"""
        import random
        levels = ['INFO', 'WARNING', 'ERROR', 'DEBUG']
        for i in range(n):
            level = random.choice(levels)
            code = random.randint(100, 999)
            yield f"{level}:{code} - Log message {i}"

    num_lines = one_million
    print(f"Real-world scenario of processing a large file ({num_lines} lines):")
    print("--------------------------------")
    print("list comprehension approach:")
    start_time = time.perf_counter()
    all_logs_list = [line for line in generate_logs(num_lines) ]
    print(f"list of logs takes {sys.getsizeof(all_logs_list)} bytes")
    error_codes_counter = Counter()
    for log in all_logs_list:
        if log.startswith('ERROR'):
            error_code = log.split(':')[1].split(' -')[0]
            error_codes_counter[error_code] += 1
    print(f"error codes counter calculated by list comprehension: {error_codes_counter.most_common(10)}")
    end_time = time.perf_counter()
    print(f"list comprehension approach took {end_time - start_time:.4f} seconds")
    print("generator expression approach:")
    start_time = time.perf_counter()
    all_logs_gen = (line for line in generate_logs(num_lines))
    print(f"generator of logs takes {sys.getsizeof(all_logs_gen)} bytes")
    error_codes_counter = Counter()
    for log in all_logs_gen:
        if log.startswith('ERROR'):
            error_code = log.split(':')[1].split(' -')[0]
            error_codes_counter[error_code] += 1
    print(f"error codes counter calculated by generator expression: {error_codes_counter.most_common(10)}")
    end_time = time.perf_counter()
    print(f"generator expression approach took {end_time - start_time:.4f} seconds")    
    print("--------------------------------")

# ============================================================
# EXERCISE 5: Advanced Patterns
# ============================================================

def generator_pipeline():
    """
    Build a data processing pipeline using generators.
    
    TODO: Create a pipeline that:
    1. Generates numbers 1 to 1,000,000
    2. Filters even numbers
    3. Squares them
    4. Takes first 10
    
    Implement this:
    - Using nested generator expressions (one-liner)
    - Using separate generator functions
    - Using itertools
    
    Which is most readable?
    """
    print("Generator pipeline:")
    print("--------------------------------")
    print("generator pipeline one-liner:")
    start_time = time.perf_counter()
    # Pipeline: range(one_million) generates numbers → inner genexp filters evens & squares → 
    # zip pairs with range(10) stopping after 10 items → outer genexp discards index, keeps values
    pipeline_result = (v for _,v in zip(range(10), (n*n for n in range(one_million) if n % 2 == 0)))
    print(f"pipeline result: {list(pipeline_result)}")
    end_time = time.perf_counter()
    print(f"generator pipeline took {end_time - start_time:.4f} seconds")
    print("--------------------------------")
    # Todo, add separate generator functions for each step.

    # Todo, add example using itertools 

# ============================================================
# BONUS CHALLENGE
# ============================================================

def custom_range(start, stop, step=1):
    """
    Implement your own range() function that returns a generator.
    
    TODO: Implement this without using range()
    Should support:
    - custom_range(5) -> 0, 1, 2, 3, 4
    - custom_range(2, 5) -> 2, 3, 4
    - custom_range(0, 10, 2) -> 0, 2, 4, 6, 8
    
    Bonus: Handle negative steps
    """
    pass

# ============================================================
# TESTS
# ============================================================

def test_basic():
    """Basic sanity checks"""
    # Uncomment and implement tests as you complete exercises
    # assert compare_memory_usage() is not None
    print("✅ Tests passed (implement more tests as you go)")

# ============================================================
# PERFORMANCE ANALYSIS
# ============================================================

def analyze_complexity():
    """
    Write your analysis here:
    
    List Comprehension:
    - Time Complexity: O(n) to create, O(1) to access
    - Space Complexity: O(n) - stores all items
    - Use When: Need to access multiple times, small to medium data
    
    Generator Expression:
    - Time Complexity: O(1) to create, O(n) to consume
    - Space Complexity: O(1) - one item at a time
    - Use When: Large data, single pass, memory constrained
    
    Trade-offs:
    - TODO: Fill in your observations
    """
    pass

# ============================================================
# NOTES & INSIGHTS
# ============================================================

"""
What I learned:
- 

Gotchas:
- 

Questions:
- 

Real-world application:
- 

Performance observations:
- 
"""

# ============================================================
# HELPER FUNCTIONS (Feel free to use these)
# ============================================================

def measure_memory(func):
    """Decorator to measure memory usage"""
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"Current memory: {current / 1024 / 1024:.2f} MB")
        print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")
        return result
    return wrapper

def measure_time(func):
    """Decorator to measure execution time"""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Execution time: {end - start:.4f} seconds")
        return result
    return wrapper

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 1 Day 1: List Comprehensions vs Generator Expressions")
    print("=" * 60)
    
    print("\n--- Exercise 1: Memory Usage ---")
    compare_memory_usage()
    
    print("\n--- Exercise 2: Speed Comparison ---")
    compare_speed()
    
    print("\n--- Exercise 3: Reusability ---")
    test_reusability()
    
    print("\n--- Exercise 4: Real-World Scenario ---")
    process_large_file_simulation()
    
    print("\n--- Exercise 5: Generator Pipeline ---")
    generator_pipeline()
    
    # print("\n--- Bonus Challenge ---")
    # test_custom_range()
    
    print("\n✅ Session complete! Update your PRACTICE_LOG.md")

