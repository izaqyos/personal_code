"""
Week 2, Day 2: Generator Functions and yield

Learning Objectives:
- Understand how generator functions work
- Master the yield keyword
- Learn when to use generators vs regular functions
- Practice creating memory-efficient data pipelines

Time: 10-15 minutes
"""

import sys
import time
from typing import Generator, List

# ============================================================
# EXERCISE 1: Basic Generator Functions
# ============================================================

def basic_generator_example():
    """
    Understand the difference between regular functions and generators.
    
    Regular function: Uses 'return', executes completely, returns value
    Generator function: Uses 'yield', pauses execution, returns generator object
    """
    print("--- Exercise 1: Basic Generator Functions ---")
    
    # Regular function
    def regular_function():
        """Returns a list of numbers"""
        result = []
        for i in range(5):
            result.append(i)
        return result
    
    # Generator function
    def generator_function():
        """Yields numbers one at a time"""
        for i in range(5):
            yield i
    
    # Compare behavior
    print("Regular function:")
    result = regular_function()
    print(f"  Type: {type(result)}")
    print(f"  Value: {result}")
    
    print("\nGenerator function:")
    gen = generator_function()
    print(f"  Type: {type(gen)}")
    print(f"  Values: {list(gen)}")
    
    print()

# ============================================================
# EXERCISE 2: yield Keyword Mechanics
# ============================================================

def yield_mechanics():
    """
    Understand how yield pauses and resumes execution.
    
    TODO: Observe generator state between yields
    """
    print("--- Exercise 2: yield Mechanics ---")
    
    def count_with_messages():
        """Generator that shows execution flow"""
        print("    [Generator started]")
        yield 1
        print("    [After first yield]")
        yield 2
        print("    [After second yield]")
        yield 3
        print("    [After third yield]")
        print("    [Generator ending]")
    
    # TODO: Call next() manually to see execution flow
    print("Creating generator:")
    gen = count_with_messages()
    print(f"  Generator object: {gen}")
    
    print("\nCalling next() manually:")
    print(f"  First: {next(gen)}")
    print(f"  Second: {next(gen)}")
    print(f"  Third: {next(gen)}")
    
    try:
        print(f"  Fourth: {next(gen)}")
    except StopIteration:
        print("  StopIteration raised")
    
    print()

# ============================================================
# EXERCISE 3: Generator for Large Sequences
# ============================================================

def fibonacci_generator(limit: int) -> Generator[int, None, None]:
    """
    Generate Fibonacci sequence using a generator.
    
    TODO: Implement Fibonacci generator
    """
    # TODO: Yield Fibonacci numbers up to limit
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

def test_fibonacci_generator():
    """Test the Fibonacci generator"""
    print("--- Exercise 3: Fibonacci Generator ---")
    
    # TODO: Generate first 10 Fibonacci numbers
    print("First 10 Fibonacci numbers:")
    for num in fibonacci_generator(10):
        print(f"  {num}")
    
    # Memory comparison
    print("\nMemory comparison:")
    
    # List version
    def fib_list(n):
        result = []
        a, b = 0, 1
        for _ in range(n):
            result.append(a)
            a, b = b, a + b
        return result
    
    fib_l = fib_list(1000)
    fib_g = fibonacci_generator(1000)
    
    print(f"  List (1000 items): {sys.getsizeof(fib_l)} bytes")
    print(f"  Generator: {sys.getsizeof(fib_g)} bytes")
    
    print()

# ============================================================
# EXERCISE 4: Reading Large Files with Generators
# ============================================================

def read_large_file(filename: str) -> Generator[str, None, None]:
    """
    Read a large file line by line using a generator.
    
    TODO: Implement file reading generator
    """
    # TODO: Yield lines one at a time
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()

def test_file_reading_generator():
    """Test the file reading generator"""
    print("--- Exercise 4: File Reading Generator ---")
    
    # Create a test file
    test_file = "test_large_file.txt"
    with open(test_file, 'w') as f:
        for i in range(100):
            f.write(f"Line {i}: Some data here\n")
    
    # TODO: Read file using generator
    print("Reading file with generator (first 5 lines):")
    for i, line in enumerate(read_large_file(test_file)):
        if i >= 5:
            break
        print(f"  {line}")
    
    # Cleanup
    import os
    os.remove(test_file)
    
    print()

# ============================================================
# EXERCISE 5: Generator with State
# ============================================================

def running_average() -> Generator[float, float, None]:
    """
    Generator that maintains running average.
    
    TODO: Implement generator that tracks running average
    Uses send() to receive values
    """
    total = 0.0
    count = 0
    average = 0.0
    
    while True:
        # TODO: Receive value via yield, update average
        value = yield average
        if value is not None:
            total += value
            count += 1
            average = total / count

def test_running_average():
    """Test the running average generator"""
    print("--- Exercise 5: Generator with State ---")
    
    # TODO: Use send() to pass values to generator
    avg_gen = running_average()
    next(avg_gen)  # Prime the generator
    
    values = [10, 20, 30, 40, 50]
    print("Calculating running average:")
    for val in values:
        avg = avg_gen.send(val)
        print(f"  Added {val}, average: {avg:.2f}")
    
    print()

# ============================================================
# EXERCISE 6: Generator Pipeline
# ============================================================

def read_numbers(filename: str) -> Generator[int, None, None]:
    """Read numbers from file"""
    with open(filename, 'r') as f:
        for line in f:
            yield int(line.strip())

def filter_even(numbers: Generator[int, None, None]) -> Generator[int, None, None]:
    """Filter even numbers"""
    # TODO: Yield only even numbers
    for num in numbers:
        if num % 2 == 0:
            yield num

def square_numbers(numbers: Generator[int, None, None]) -> Generator[int, None, None]:
    """Square each number"""
    # TODO: Yield squared numbers
    for num in numbers:
        yield num ** 2

def test_generator_pipeline():
    """Test chaining generators"""
    print("--- Exercise 6: Generator Pipeline ---")
    
    # Create test file
    test_file = "test_numbers.txt"
    with open(test_file, 'w') as f:
        for i in range(1, 11):
            f.write(f"{i}\n")
    
    # TODO: Chain generators together
    print("Pipeline: read → filter even → square")
    pipeline = square_numbers(filter_even(read_numbers(test_file)))
    
    result = list(pipeline)
    print(f"  Result: {result}")
    
    # Cleanup
    import os
    os.remove(test_file)
    
    print()

# ============================================================
# EXERCISE 7: Infinite Generators
# ============================================================

def infinite_counter(start: int = 0) -> Generator[int, None, None]:
    """
    Generate infinite sequence of numbers.
    
    TODO: Implement infinite counter
    """
    # TODO: Yield numbers infinitely
    current = start
    while True:
        yield current
        current += 1

def test_infinite_generator():
    """Test infinite generator"""
    print("--- Exercise 7: Infinite Generators ---")
    
    # TODO: Use infinite generator with limit
    print("First 10 numbers from infinite counter:")
    counter = infinite_counter(1)
    
    for i, num in enumerate(counter):
        if i >= 10:
            break
        print(f"  {num}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Data Processing Pipeline
# ============================================================

def process_log_file(filename: str) -> Generator[dict, None, None]:
    """
    Process log file and yield parsed entries.
    
    TODO: Implement log processing pipeline
    
    Log format: "TIMESTAMP|LEVEL|MESSAGE"
    """
    # TODO: Read file, parse lines, yield dicts
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 3:
                yield {
                    'timestamp': parts[0],
                    'level': parts[1],
                    'message': parts[2]
                }

def filter_by_level(logs: Generator[dict, None, None], level: str) -> Generator[dict, None, None]:
    """Filter logs by level"""
    # TODO: Yield only logs matching level
    for log in logs:
        if log['level'] == level:
            yield log

def test_log_processing():
    """Test log processing pipeline"""
    print("--- Bonus Challenge: Log Processing Pipeline ---")
    
    # Create test log file
    test_file = "test_logs.txt"
    with open(test_file, 'w') as f:
        f.write("2024-01-01 10:00:00|INFO|Application started\n")
        f.write("2024-01-01 10:00:01|ERROR|Database connection failed\n")
        f.write("2024-01-01 10:00:02|INFO|Retrying connection\n")
        f.write("2024-01-01 10:00:03|ERROR|Connection timeout\n")
        f.write("2024-01-01 10:00:04|INFO|Using fallback database\n")
    
    # TODO: Process logs and filter errors
    print("Error logs only:")
    errors = filter_by_level(process_log_file(test_file), 'ERROR')
    
    for log in errors:
        print(f"  [{log['timestamp']}] {log['message']}")
    
    # Cleanup
    import os
    os.remove(test_file)
    
    print()

# ============================================================
# PERFORMANCE COMPARISON
# ============================================================

def performance_comparison():
    """
    Compare performance of generators vs lists.
    """
    print("--- Performance Comparison ---")
    
    # List version - loads all into memory
    def process_with_list(n):
        data = list(range(n))
        filtered = [x for x in data if x % 2 == 0]
        squared = [x ** 2 for x in filtered]
        return squared
    
    # Generator version - processes on demand
    def process_with_generator(n):
        data = range(n)
        filtered = (x for x in data if x % 2 == 0)
        squared = (x ** 2 for x in filtered)
        return squared
    
    n = 1_000_000
    
    # Time list version
    start = time.perf_counter()
    result_list = process_with_list(n)
    time_list = time.perf_counter() - start
    
    # Time generator version (must consume to compare fairly)
    start = time.perf_counter()
    result_gen = list(process_with_generator(n))
    time_gen = time.perf_counter() - start
    
    print(f"Processing {n:,} numbers:")
    print(f"  List version: {time_list:.4f}s")
    print(f"  Generator version: {time_gen:.4f}s")
    
    # Memory usage
    gen = process_with_generator(n)
    print(f"\nMemory usage:")
    print(f"  List: {sys.getsizeof(result_list):,} bytes")
    print(f"  Generator: {sys.getsizeof(gen)} bytes")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Generator Functions:
    - Time: O(1) to create generator object
    - Time: O(n) to consume all n items
    - Space: O(1) - only stores current state
    
    vs Regular Functions:
    - Time: O(n) to create list of n items
    - Space: O(n) - stores all items
    
    Benefits of Generators:
    - Lazy evaluation - compute only when needed
    - Memory efficient for large datasets
    - Can represent infinite sequences
    - Composable - easy to chain
    - Better for streaming data
    
    When to Use Generators:
    - Processing large files
    - Infinite sequences
    - Data pipelines
    - When you don't need all data at once
    
    When NOT to Use Generators:
    - Need random access to elements
    - Need to iterate multiple times
    - Need to know total count upfront
    - Small datasets where memory isn't a concern
    
    Security Considerations:
    - Generators can help prevent memory exhaustion attacks
    - Be careful with infinite generators - always have exit condition
    - Close file handles properly (use context managers)
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 2, Day 2: Generator Functions and yield")
    print("=" * 60)
    print()
    
    basic_generator_example()
    yield_mechanics()
    test_fibonacci_generator()
    test_file_reading_generator()
    test_running_average()
    test_generator_pipeline()
    test_infinite_generator()
    test_log_processing()
    performance_comparison()
    
    print("=" * 60)
    print("✅ Day 2 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Generators use 'yield' to pause and resume execution")
    print("2. Generators are memory efficient - O(1) space")
    print("3. Use generators for large datasets and streaming")
    print("4. Chain generators to build data pipelines")

