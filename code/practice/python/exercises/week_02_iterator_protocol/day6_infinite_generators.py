"""
Week 2, Day 6: Infinite Generators and itertools.cycle

Learning Objectives:
- Create and use infinite generators safely
- Master itertools infinite iterators (count, cycle, repeat)
- Learn to limit infinite sequences
- Build practical infinite data sources

Time: 10-15 minutes
"""

import itertools
from typing import Generator, Any
import time

# ============================================================
# EXERCISE 1: Basic Infinite Generators
# ============================================================

def basic_infinite_generators():
    """
    Create simple infinite generators.
    
    WARNING: Infinite generators never stop - always limit them!
    """
    print("--- Exercise 1: Basic Infinite Generators ---")
    
    def infinite_counter(start=0):
        """Count infinitely from start"""
        current = start
        while True:
            yield current
            current += 1
    
    # TODO: Use with limit
    print("First 10 numbers:")
    counter = infinite_counter(1)
    for i, num in enumerate(counter):
        if i >= 10:
            break
        print(f"  {num}", end=" ")
    print("\n")

# ============================================================
# EXERCISE 2: itertools.count
# ============================================================

def itertools_count_examples():
    """
    Use itertools.count for infinite counting.
    
    count(start=0, step=1)
    """
    print("--- Exercise 2: itertools.count ---")
    
    # Basic counting
    print("count(1) - first 5:")
    for i, num in enumerate(itertools.count(1)):
        if i >= 5:
            break
        print(f"  {num}", end=" ")
    print()
    
    # Count with step
    print("\ncount(0, 5) - first 5:")
    for i, num in enumerate(itertools.count(0, 5)):
        if i >= 5:
            break
        print(f"  {num}", end=" ")
    print()
    
    # Negative step
    print("\ncount(10, -2) - first 5:")
    for i, num in enumerate(itertools.count(10, -2)):
        if i >= 5:
            break
        print(f"  {num}", end=" ")
    print()
    
    # TODO: Use with zip for enumeration
    print("\nUsing count with zip:")
    items = ['a', 'b', 'c', 'd', 'e']
    for index, item in zip(itertools.count(1), items):
        print(f"  {index}: {item}")
    
    print()

# ============================================================
# EXERCISE 3: itertools.cycle
# ============================================================

def itertools_cycle_examples():
    """
    Use itertools.cycle to repeat a sequence infinitely.
    
    cycle(iterable)
    """
    print("--- Exercise 3: itertools.cycle ---")
    
    # Cycle through colors
    colors = ['red', 'green', 'blue']
    print(f"Cycling through {colors} - first 10:")
    for i, color in enumerate(itertools.cycle(colors)):
        if i >= 10:
            break
        print(f"  {i}: {color}")
    
    # TODO: Round-robin task assignment
    print("\nRound-robin task assignment:")
    workers = ['Alice', 'Bob', 'Charlie']
    tasks = [f'Task{i}' for i in range(1, 8)]
    
    for task, worker in zip(tasks, itertools.cycle(workers)):
        print(f"  {task} → {worker}")
    
    print()

# ============================================================
# EXERCISE 4: itertools.repeat
# ============================================================

def itertools_repeat_examples():
    """
    Use itertools.repeat to repeat a value.
    
    repeat(object, times=None)
    """
    print("--- Exercise 4: itertools.repeat ---")
    
    # Repeat finite times
    print("repeat('X', 5):")
    for item in itertools.repeat('X', 5):
        print(f"  {item}", end=" ")
    print()
    
    # Repeat infinitely (with limit)
    print("\nrepeat(42) - first 3:")
    for i, num in enumerate(itertools.repeat(42)):
        if i >= 3:
            break
        print(f"  {num}", end=" ")
    print()
    
    # TODO: Use with map for constant argument
    print("\nUsing repeat with map:")
    numbers = [1, 2, 3, 4, 5]
    # Multiply each number by 10
    result = list(map(lambda x, y: x * y, numbers, itertools.repeat(10)))
    print(f"  {numbers} * 10 = {result}")
    
    print()

# ============================================================
# EXERCISE 5: Custom Infinite Generators
# ============================================================

def fibonacci_infinite() -> Generator[int, None, None]:
    """
    Generate Fibonacci sequence infinitely.
    
    TODO: Implement infinite Fibonacci generator
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def primes_infinite() -> Generator[int, None, None]:
    """
    Generate prime numbers infinitely.
    
    TODO: Implement infinite prime generator
    """
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1

def test_custom_infinite():
    """Test custom infinite generators"""
    print("--- Exercise 5: Custom Infinite Generators ---")
    
    # Fibonacci
    print("First 10 Fibonacci numbers:")
    for i, num in enumerate(fibonacci_infinite()):
        if i >= 10:
            break
        print(f"  {num}", end=" ")
    print()
    
    # Primes
    print("\nFirst 10 prime numbers:")
    for i, num in enumerate(primes_infinite()):
        if i >= 10:
            break
        print(f"  {num}", end=" ")
    print("\n")

# ============================================================
# EXERCISE 6: Limiting Infinite Generators
# ============================================================

def limiting_infinite_generators():
    """
    Different ways to limit infinite generators.
    """
    print("--- Exercise 6: Limiting Infinite Generators ---")
    
    # Method 1: islice
    print("Method 1: Using islice")
    result = list(itertools.islice(itertools.count(1), 5))
    print(f"  {result}")
    
    # Method 2: takewhile
    print("\nMethod 2: Using takewhile")
    result = list(itertools.takewhile(lambda x: x < 10, itertools.count(1)))
    print(f"  {result}")
    
    # Method 3: zip with finite iterable
    print("\nMethod 3: Using zip")
    result = list(zip(range(5), itertools.count(1)))
    print(f"  {result}")
    
    # Method 4: Manual break in loop
    print("\nMethod 4: Manual break")
    result = []
    for i, num in enumerate(itertools.count(1)):
        if i >= 5:
            break
        result.append(num)
    print(f"  {result}")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - ID Generator
# ============================================================

class IDGenerator:
    """
    Generate unique IDs with prefix.
    
    TODO: Implement ID generator using infinite counter
    """
    
    def __init__(self, prefix: str = "ID", start: int = 1):
        self.prefix = prefix
        self.counter = itertools.count(start)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        """Generate next ID"""
        return f"{self.prefix}{next(self.counter):06d}"
    
    def get_id(self):
        """Get next ID"""
        return next(self)

def test_id_generator():
    """Test the ID generator"""
    print("--- Exercise 7: ID Generator ---")
    
    # Generate user IDs
    user_ids = IDGenerator("USER", start=1)
    
    print("Generated user IDs:")
    for _ in range(5):
        print(f"  {user_ids.get_id()}")
    
    # Generate order IDs
    order_ids = IDGenerator("ORDER", start=1000)
    
    print("\nGenerated order IDs:")
    for _ in range(5):
        print(f"  {order_ids.get_id()}")
    
    print()

# ============================================================
# EXERCISE 8: Infinite Data Stream Simulation
# ============================================================

def sensor_data_stream() -> Generator[dict, None, None]:
    """
    Simulate infinite sensor data stream.
    
    TODO: Generate infinite sensor readings
    """
    import random
    
    for timestamp in itertools.count(1):
        yield {
            'timestamp': timestamp,
            'temperature': round(20 + random.uniform(-5, 5), 2),
            'humidity': round(50 + random.uniform(-10, 10), 2),
            'pressure': round(1013 + random.uniform(-20, 20), 2)
        }

def test_sensor_stream():
    """Test sensor data stream"""
    print("--- Exercise 8: Sensor Data Stream ---")
    
    print("Sensor readings (first 5):")
    for reading in itertools.islice(sensor_data_stream(), 5):
        print(f"  Time {reading['timestamp']}: "
              f"Temp={reading['temperature']}°C, "
              f"Humidity={reading['humidity']}%, "
              f"Pressure={reading['pressure']}hPa")
    
    print()

# ============================================================
# EXERCISE 9: Combining Infinite Generators
# ============================================================

def combining_infinite_generators():
    """
    Combine multiple infinite generators.
    """
    print("--- Exercise 9: Combining Infinite Generators ---")
    
    # Interleave two infinite sequences
    def interleave(gen1, gen2):
        """Interleave two generators"""
        while True:
            yield next(gen1)
            yield next(gen2)
    
    # TODO: Interleave numbers and letters
    numbers = itertools.count(1)
    letters = itertools.cycle(['A', 'B', 'C'])
    
    print("Interleaved sequence (first 10):")
    combined = interleave(numbers, letters)
    for i, item in enumerate(combined):
        if i >= 10:
            break
        print(f"  {item}", end=" ")
    print("\n")

# ============================================================
# BONUS CHALLENGE: Rate-Limited Generator
# ============================================================

def rate_limited_generator(generator: Generator, rate: float) -> Generator:
    """
    Wrap a generator to limit its rate.
    
    TODO: Implement rate limiting
    
    Args:
        generator: Source generator
        rate: Items per second
    """
    delay = 1.0 / rate
    for item in generator:
        yield item
        time.sleep(delay)

def test_rate_limited():
    """Test rate-limited generator"""
    print("--- Bonus Challenge: Rate-Limited Generator ---")
    
    # Generate numbers at 5 per second
    print("Generating 5 numbers at 2/second:")
    start = time.time()
    
    limited = rate_limited_generator(itertools.count(1), rate=2.0)
    for i, num in enumerate(limited):
        if i >= 5:
            break
        elapsed = time.time() - start
        print(f"  {elapsed:.2f}s: {num}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Infinite Generators:
    - Creation: O(1) - just creates generator object
    - Each next(): O(1) typically
    - Space: O(1) - only stores current state
    
    itertools.count:
    - Time: O(1) per item
    - Space: O(1)
    
    itertools.cycle:
    - Time: O(1) per item (after first cycle)
    - Space: O(n) where n is length of cycled sequence
    
    itertools.repeat:
    - Time: O(1) per item
    - Space: O(1)
    
    Benefits:
    - Represent infinite sequences with finite memory
    - Generate data on-demand
    - Perfect for streams and continuous data
    - Can be combined and composed
    
    Use Cases:
    - ID generation
    - Round-robin scheduling
    - Sensor data streams
    - Pagination
    - Testing with infinite data
    - Event loops
    
    Safety Considerations:
    - ALWAYS limit infinite generators
    - Use islice, takewhile, or manual breaks
    - Set timeouts for long-running operations
    - Monitor memory if cycle() uses large sequences
    - Validate termination conditions
    
    Security Considerations:
    - Infinite generators can cause DoS if not limited
    - Always validate input to limiting conditions
    - Set maximum iteration counts
    - Use timeouts in production code
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 2, Day 6: Infinite Generators")
    print("=" * 60)
    print()
    
    basic_infinite_generators()
    itertools_count_examples()
    itertools_cycle_examples()
    itertools_repeat_examples()
    test_custom_infinite()
    limiting_infinite_generators()
    test_id_generator()
    test_sensor_stream()
    combining_infinite_generators()
    test_rate_limited()
    
    print("=" * 60)
    print("✅ Day 6 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Infinite generators use O(1) space")
    print("2. ALWAYS limit them with islice, takewhile, or breaks")
    print("3. Perfect for streams, IDs, and continuous data")
    print("4. itertools provides count, cycle, repeat")

