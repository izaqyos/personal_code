"""
Week 2, Day 1: Implementing Custom Iterators (__iter__, __next__)

Learning Objectives:
- Understand the iterator protocol
- Implement __iter__ and __next__ methods
- Learn about StopIteration exception
- Create reusable and composable iterators

Time: 10-15 minutes
"""

from typing import Any, Iterator

# ============================================================
# EXERCISE 1: Understanding the Iterator Protocol
# ============================================================

def iterator_protocol_basics():
    """
    Understand how Python's iterator protocol works.
    
    Iterator Protocol:
    - __iter__(): Returns the iterator object (usually self)
    - __next__(): Returns the next item or raises StopIteration
    """
    print("--- Exercise 1: Iterator Protocol Basics ---")
    
    # Built-in iterators
    numbers = [1, 2, 3, 4, 5]
    
    # Get iterator from iterable
    iterator = iter(numbers)  # Calls __iter__()
    
    # Manual iteration
    print("Manual iteration:")
    try:
        print(f"  {next(iterator)}")  # Calls __next__()
        print(f"  {next(iterator)}")
        print(f"  {next(iterator)}")
        print(f"  {next(iterator)}")
        print(f"  {next(iterator)}")
        print(f"  {next(iterator)}")  # This will raise StopIteration
    except StopIteration:
        print("  StopIteration raised - no more items")
    
    print()

# ============================================================
# EXERCISE 2: Simple Custom Iterator
# ============================================================

class CountUp:
    """
    A simple iterator that counts from start to end.
    
    TODO: Implement __iter__ and __next__
    """
    
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.current = start
    
    def __iter__(self):
        """Return the iterator object (self)"""
        # TODO: Return self
        return self
    
    def __next__(self):
        """Return the next value or raise StopIteration"""
        # TODO: Implement counting logic
        if self.current > self.end:
            raise StopIteration
        
        value = self.current
        self.current += 1
        return value

def test_count_up():
    """Test the CountUp iterator"""
    print("--- Exercise 2: Simple Custom Iterator ---")
    
    # TODO: Use CountUp iterator
    counter = CountUp(1, 5)
    
    print("Using for loop:")
    for num in counter:
        print(f"  {num}")
    
    # Note: Iterator is exhausted after first use
    print("\nTrying to iterate again:")
    for num in counter:
        print(f"  {num}")
    print("  (Iterator is exhausted)")
    
    print()

# ============================================================
# EXERCISE 3: Reusable Iterator (Iterable vs Iterator)
# ============================================================

class CountUpIterable:
    """
    An iterable that creates a new iterator each time.
    
    This is reusable - you can iterate multiple times.
    
    TODO: Separate iterable from iterator
    """
    
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
    
    def __iter__(self):
        """Return a NEW iterator each time"""
        # TODO: Return a new CountUpIterator instance
        return CountUpIterator(self.start, self.end)

class CountUpIterator:
    """The actual iterator"""
    
    def __init__(self, start: int, end: int):
        self.current = start
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

def test_reusable_iterator():
    """Test the reusable iterable"""
    print("--- Exercise 3: Reusable Iterator ---")
    
    # TODO: Use CountUpIterable
    counter = CountUpIterable(1, 3)
    
    print("First iteration:")
    for num in counter:
        print(f"  {num}")
    
    print("\nSecond iteration (works!):")
    for num in counter:
        print(f"  {num}")
    
    print()

# ============================================================
# EXERCISE 4: Fibonacci Iterator
# ============================================================

class Fibonacci:
    """
    Iterator that generates Fibonacci sequence.
    
    TODO: Implement Fibonacci iterator with optional limit
    """
    
    def __init__(self, limit: int = None):
        """
        Args:
            limit: Maximum number of terms to generate (None for infinite)
        """
        self.limit = limit
        self.count = 0
        self.a = 0
        self.b = 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        """Generate next Fibonacci number"""
        # TODO: Implement Fibonacci logic
        if self.limit is not None and self.count >= self.limit:
            raise StopIteration
        
        if self.count == 0:
            self.count += 1
            return self.a
        elif self.count == 1:
            self.count += 1
            return self.b
        else:
            self.a, self.b = self.b, self.a + self.b
            self.count += 1
            return self.b

def test_fibonacci():
    """Test the Fibonacci iterator"""
    print("--- Exercise 4: Fibonacci Iterator ---")
    
    # TODO: Generate first 10 Fibonacci numbers
    print("First 10 Fibonacci numbers:")
    fib = Fibonacci(limit=10)
    for num in fib:
        print(f"  {num}")
    
    print()

# ============================================================
# EXERCISE 5: Reverse Iterator
# ============================================================

class ReverseIterator:
    """
    Iterator that traverses a sequence in reverse.
    
    TODO: Implement reverse iteration
    """
    
    def __init__(self, data):
        self.data = data
        self.index = len(data)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        """Return items in reverse order"""
        # TODO: Implement reverse logic
        if self.index <= 0:
            raise StopIteration
        
        self.index -= 1
        return self.data[self.index]

def test_reverse_iterator():
    """Test the ReverseIterator"""
    print("--- Exercise 5: Reverse Iterator ---")
    
    # TODO: Reverse iterate over a list
    data = [1, 2, 3, 4, 5]
    
    print(f"Original: {data}")
    print("Reversed:")
    for item in ReverseIterator(data):
        print(f"  {item}")
    
    print()

# ============================================================
# EXERCISE 6: File Line Iterator with Filtering
# ============================================================

class FilteredFileIterator:
    """
    Iterator that reads file lines and filters them.
    
    TODO: Implement file iterator with filtering
    """
    
    def __init__(self, filename: str, filter_func=None):
        """
        Args:
            filename: Path to file
            filter_func: Function to filter lines (returns True to include)
        """
        self.filename = filename
        self.filter_func = filter_func or (lambda x: True)
        self.file = None
    
    def __iter__(self):
        """Open file and return iterator"""
        self.file = open(self.filename, 'r')
        return self
    
    def __next__(self):
        """Return next filtered line"""
        # TODO: Read lines and apply filter
        while True:
            line = self.file.readline()
            
            if not line:  # EOF
                self.file.close()
                raise StopIteration
            
            line = line.strip()
            if self.filter_func(line):
                return line
    
    def __del__(self):
        """Ensure file is closed"""
        if self.file:
            self.file.close()

def test_filtered_file_iterator():
    """Test the FilteredFileIterator"""
    print("--- Exercise 6: Filtered File Iterator ---")
    
    # Create test file
    test_file = "test_iterator.txt"
    with open(test_file, 'w') as f:
        f.write("ERROR: Something went wrong\n")
        f.write("INFO: Application started\n")
        f.write("ERROR: Database connection failed\n")
        f.write("DEBUG: Processing request\n")
        f.write("ERROR: Timeout occurred\n")
    
    # TODO: Read only ERROR lines
    print("Error lines only:")
    for line in FilteredFileIterator(test_file, lambda l: l.startswith("ERROR")):
        print(f"  {line}")
    
    # Cleanup
    import os
    os.remove(test_file)
    
    print()

# ============================================================
# EXERCISE 7: Infinite Iterator with Cycle
# ============================================================

class Cycle:
    """
    Iterator that cycles through items infinitely.
    
    TODO: Implement cycling iterator
    """
    
    def __init__(self, items):
        self.items = list(items)
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        """Cycle through items infinitely"""
        # TODO: Implement cycling logic
        if not self.items:
            raise StopIteration
        
        value = self.items[self.index]
        self.index = (self.index + 1) % len(self.items)
        return value

def test_cycle():
    """Test the Cycle iterator"""
    print("--- Exercise 7: Infinite Cycle Iterator ---")
    
    # TODO: Cycle through colors
    colors = Cycle(['red', 'green', 'blue'])
    
    print("First 10 colors:")
    for i, color in enumerate(colors):
        if i >= 10:
            break
        print(f"  {i}: {color}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Batch Iterator
# ============================================================

class BatchIterator:
    """
    Iterator that yields items in batches.
    
    TODO: Implement batching iterator
    
    Example:
        BatchIterator([1,2,3,4,5,6,7], batch_size=3)
        yields: [1,2,3], [4,5,6], [7]
    """
    
    def __init__(self, data, batch_size: int):
        self.data = list(data)
        self.batch_size = batch_size
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        """Return next batch"""
        # TODO: Implement batching logic
        if self.index >= len(self.data):
            raise StopIteration
        
        batch = self.data[self.index:self.index + self.batch_size]
        self.index += self.batch_size
        return batch

def test_batch_iterator():
    """Test the BatchIterator"""
    print("--- Bonus Challenge: Batch Iterator ---")
    
    # TODO: Process data in batches
    data = list(range(1, 11))
    
    print(f"Data: {data}")
    print("Batches of 3:")
    for batch in BatchIterator(data, batch_size=3):
        print(f"  {batch}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Iterator Protocol:
    - __iter__(): O(1) - just returns self
    - __next__(): O(1) per call (depends on implementation)
    - Total iteration: O(n) for n items
    
    Space Complexity:
    - Iterator object: O(1) - only stores current state
    - vs List: O(n) - stores all items
    
    Benefits:
    - Lazy evaluation - compute on demand
    - Memory efficient for large datasets
    - Can represent infinite sequences
    - Composable - can chain iterators
    
    Security Considerations:
    - Close file handles in __del__ or use context managers
    - Be careful with infinite iterators
    - Validate input in __init__ to prevent resource exhaustion
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 2, Day 1: Custom Iterators")
    print("=" * 60)
    print()
    
    iterator_protocol_basics()
    test_count_up()
    test_reusable_iterator()
    test_fibonacci()
    test_reverse_iterator()
    test_filtered_file_iterator()
    test_cycle()
    test_batch_iterator()
    
    print("=" * 60)
    print("✅ Day 1 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Iterator protocol: __iter__() and __next__()")
    print("2. Raise StopIteration when done")
    print("3. Separate iterable from iterator for reusability")
    print("4. Iterators are memory efficient (lazy evaluation)")

