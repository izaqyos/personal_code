"""
Week 4, Day 1: map, filter, and reduce

Learning Objectives:
- Master map() for transforming sequences
- Learn filter() for selecting elements
- Understand reduce() for accumulation
- Compare with list comprehensions
- Practice functional composition

Time: 10-15 minutes
"""

from functools import reduce
from typing import Callable, Iterable, Any
import time

# ============================================================
# EXERCISE 1: map() Basics
# ============================================================

def map_basics():
    """
    Learn basic map() operations.
    
    map(function, iterable) - apply function to each element
    """
    print("--- Exercise 1: map() Basics ---")
    
    numbers = [1, 2, 3, 4, 5]
    
    # Square each number
    squared = map(lambda x: x ** 2, numbers)
    print(f"Original: {numbers}")
    print(f"Squared: {list(squared)}")
    
    # Convert to strings
    strings = map(str, numbers)
    print(f"As strings: {list(strings)}")
    
    # Multiple iterables
    a = [1, 2, 3]
    b = [10, 20, 30]
    sums = map(lambda x, y: x + y, a, b)
    print(f"\n{a} + {b} = {list(sums)}")
    
    # map returns iterator (lazy)
    print("\n💡 map() returns an iterator (lazy evaluation)")
    big_map = map(lambda x: x ** 2, range(1000000))
    print(f"Created map for 1M items: {big_map}")
    print(f"Taking first 5: {list(zip(range(5), big_map))}")
    
    print()

# ============================================================
# EXERCISE 2: filter() Basics
# ============================================================

def filter_basics():
    """
    Learn basic filter() operations.
    
    filter(predicate, iterable) - keep elements where predicate is True
    """
    print("--- Exercise 2: filter() Basics ---")
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Filter even numbers
    evens = filter(lambda x: x % 2 == 0, numbers)
    print(f"Original: {numbers}")
    print(f"Evens: {list(evens)}")
    
    # Filter numbers > 5
    greater_than_5 = filter(lambda x: x > 5, numbers)
    print(f"Greater than 5: {list(greater_than_5)}")
    
    # Filter with None (removes falsy values)
    mixed = [0, 1, False, True, '', 'hello', None, [], [1, 2]]
    truthy = filter(None, mixed)
    print(f"\nMixed: {mixed}")
    print(f"Truthy values: {list(truthy)}")
    
    # filter returns iterator (lazy)
    print("\n💡 filter() returns an iterator (lazy evaluation)")
    
    print()

# ============================================================
# EXERCISE 3: reduce() Basics
# ============================================================

def reduce_basics():
    """
    Learn basic reduce() operations.
    
    reduce(function, iterable, [initial]) - accumulate values
    """
    print("--- Exercise 3: reduce() Basics ---")
    
    numbers = [1, 2, 3, 4, 5]
    
    # Sum all numbers
    total = reduce(lambda acc, x: acc + x, numbers)
    print(f"Numbers: {numbers}")
    print(f"Sum: {total}")
    
    # Product of all numbers
    product = reduce(lambda acc, x: acc * x, numbers)
    print(f"Product: {product}")
    
    # With initial value
    total_with_init = reduce(lambda acc, x: acc + x, numbers, 100)
    print(f"\nSum with initial 100: {total_with_init}")
    
    # Find maximum
    max_val = reduce(lambda acc, x: x if x > acc else acc, numbers)
    print(f"Maximum: {max_val}")
    
    # Build a string
    words = ['Hello', 'functional', 'world']
    sentence = reduce(lambda acc, word: f"{acc} {word}", words)
    print(f"\nWords: {words}")
    print(f"Sentence: {sentence}")
    
    print()

# ============================================================
# EXERCISE 4: map vs List Comprehension
# ============================================================

def map_vs_comprehension():
    """
    Compare map() with list comprehensions.
    
    TODO: Understand when to use each
    """
    print("--- Exercise 4: map vs List Comprehension ---")
    
    numbers = range(10)
    
    # Using map
    squared_map = list(map(lambda x: x ** 2, numbers))
    print(f"Using map: {squared_map}")
    
    # Using list comprehension
    squared_comp = [x ** 2 for x in numbers]
    print(f"Using comprehension: {squared_comp}")
    
    # Performance comparison
    n = 100000
    
    start = time.perf_counter()
    result1 = list(map(lambda x: x ** 2, range(n)))
    time_map = time.perf_counter() - start
    
    start = time.perf_counter()
    result2 = [x ** 2 for x in range(n)]
    time_comp = time.perf_counter() - start
    
    print(f"\nPerformance ({n:,} items):")
    print(f"  map: {time_map:.6f}s")
    print(f"  comprehension: {time_comp:.6f}s")
    
    print("\n💡 List comprehensions are often:")
    print("  • More Pythonic")
    print("  • More readable")
    print("  • Slightly faster")
    print("\n💡 Use map() when:")
    print("  • You have an existing function (not lambda)")
    print("  • You want lazy evaluation")
    print("  • Working with multiple iterables")
    
    print()

# ============================================================
# EXERCISE 5: Chaining map, filter, reduce
# ============================================================

def chaining_operations():
    """
    Chain map, filter, and reduce together.
    
    TODO: Build functional pipelines
    """
    print("--- Exercise 5: Chaining Operations ---")
    
    numbers = range(1, 11)
    
    # Sum of squares of even numbers
    result = reduce(
        lambda acc, x: acc + x,
        map(
            lambda x: x ** 2,
            filter(lambda x: x % 2 == 0, numbers)
        )
    )
    
    print(f"Numbers: {list(numbers)}")
    print(f"Sum of squares of evens: {result}")
    print(f"  (2² + 4² + 6² + 8² + 10² = {2**2 + 4**2 + 6**2 + 8**2 + 10**2})")
    
    # Same with comprehension (more readable)
    result_comp = sum(x ** 2 for x in numbers if x % 2 == 0)
    print(f"\nSame with comprehension: {result_comp}")
    
    # Another example: average of positive numbers
    values = [-5, 3, -2, 8, -1, 6, 0, 4]
    positive = list(filter(lambda x: x > 0, values))
    average = reduce(lambda acc, x: acc + x, positive) / len(positive)
    
    print(f"\nValues: {values}")
    print(f"Positive: {positive}")
    print(f"Average of positive: {average:.2f}")
    
    print()

# ============================================================
# EXERCISE 6: Real-World Scenario - Data Processing
# ============================================================

def process_employee_data():
    """
    Process employee data using functional programming.
    
    TODO: Calculate total salary of senior engineers
    """
    print("--- Exercise 6: Employee Data Processing ---")
    
    employees = [
        {'name': 'Alice', 'role': 'Engineer', 'years': 6, 'salary': 95000},
        {'name': 'Bob', 'role': 'Manager', 'years': 8, 'salary': 110000},
        {'name': 'Charlie', 'role': 'Engineer', 'years': 3, 'salary': 75000},
        {'name': 'Diana', 'role': 'Engineer', 'years': 7, 'salary': 105000},
        {'name': 'Eve', 'role': 'Designer', 'years': 5, 'salary': 85000},
    ]
    
    # Total salary of senior engineers (years >= 5)
    total_salary = reduce(
        lambda acc, emp: acc + emp['salary'],
        filter(
            lambda emp: emp['role'] == 'Engineer' and emp['years'] >= 5,
            employees
        ),
        0
    )
    
    print("Senior Engineers (years >= 5):")
    senior_engineers = list(filter(
        lambda emp: emp['role'] == 'Engineer' and emp['years'] >= 5,
        employees
    ))
    for emp in senior_engineers:
        print(f"  {emp['name']}: ${emp['salary']:,}")
    
    print(f"\nTotal salary: ${total_salary:,}")
    
    # Average salary by role
    print("\nAverage salary by role:")
    roles = set(emp['role'] for emp in employees)
    
    for role in roles:
        role_emps = list(filter(lambda e: e['role'] == role, employees))
        avg_salary = reduce(lambda acc, e: acc + e['salary'], role_emps, 0) / len(role_emps)
        print(f"  {role}: ${avg_salary:,.0f}")
    
    print()

# ============================================================
# EXERCISE 7: Custom map/filter/reduce
# ============================================================

def custom_map(func: Callable, iterable: Iterable) -> Iterable:
    """
    Implement custom map function.
    
    TODO: Understand how map works internally
    """
    for item in iterable:
        yield func(item)

def custom_filter(predicate: Callable, iterable: Iterable) -> Iterable:
    """
    Implement custom filter function.
    
    TODO: Understand how filter works internally
    """
    for item in iterable:
        if predicate(item):
            yield item

def custom_reduce(func: Callable, iterable: Iterable, initial: Any = None) -> Any:
    """
    Implement custom reduce function.
    
    TODO: Understand how reduce works internally
    """
    it = iter(iterable)
    
    if initial is None:
        try:
            accumulator = next(it)
        except StopIteration:
            raise TypeError("reduce() of empty sequence with no initial value")
    else:
        accumulator = initial
    
    for item in it:
        accumulator = func(accumulator, item)
    
    return accumulator

def test_custom_functions():
    """Test custom implementations"""
    print("--- Exercise 7: Custom Implementations ---")
    
    numbers = [1, 2, 3, 4, 5]
    
    # Custom map
    squared = list(custom_map(lambda x: x ** 2, numbers))
    print(f"Custom map (square): {squared}")
    
    # Custom filter
    evens = list(custom_filter(lambda x: x % 2 == 0, numbers))
    print(f"Custom filter (evens): {evens}")
    
    # Custom reduce
    total = custom_reduce(lambda acc, x: acc + x, numbers)
    print(f"Custom reduce (sum): {total}")
    
    # With initial value
    total_init = custom_reduce(lambda acc, x: acc + x, numbers, 100)
    print(f"Custom reduce (sum with init): {total_init}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Functional Pipeline
# ============================================================

class Pipeline:
    """
    Functional pipeline for chaining operations.
    
    TODO: Implement fluent pipeline API
    """
    
    def __init__(self, data):
        self.data = data
    
    def map(self, func):
        """Apply map operation"""
        self.data = map(func, self.data)
        return self
    
    def filter(self, predicate):
        """Apply filter operation"""
        self.data = filter(predicate, self.data)
        return self
    
    def reduce(self, func, initial=None):
        """Apply reduce operation and return result"""
        if initial is None:
            return reduce(func, self.data)
        return reduce(func, self.data, initial)
    
    def collect(self):
        """Collect results into list"""
        return list(self.data)

def test_pipeline():
    """Test functional pipeline"""
    print("--- Bonus Challenge: Functional Pipeline ---")
    
    # Sum of squares of even numbers
    result = (Pipeline(range(1, 11))
              .filter(lambda x: x % 2 == 0)
              .map(lambda x: x ** 2)
              .reduce(lambda acc, x: acc + x))
    
    print(f"Sum of squares of evens (1-10): {result}")
    
    # Get top 3 squared odd numbers
    result = (Pipeline(range(1, 11))
              .filter(lambda x: x % 2 == 1)
              .map(lambda x: x ** 2)
              .collect())
    
    print(f"Squared odd numbers: {result}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    map(func, iterable):
    - Time: O(n) to consume
    - Space: O(1) - lazy iterator
    - Returns iterator immediately: O(1)
    
    filter(pred, iterable):
    - Time: O(n) to consume
    - Space: O(1) - lazy iterator
    - Returns iterator immediately: O(1)
    
    reduce(func, iterable):
    - Time: O(n)
    - Space: O(1)
    - Eager evaluation (returns result)
    
    List Comprehension:
    - Time: O(n)
    - Space: O(n) - creates list immediately
    - Eager evaluation
    
    Benefits:
    - Lazy evaluation (map/filter)
    - Composable operations
    - Functional style (no side effects)
    - Works with any iterable
    
    Drawbacks:
    - Less Pythonic than comprehensions
    - Lambda functions can be less readable
    - Debugging can be harder
    
    Use Cases:
    - Transforming data (map)
    - Selecting data (filter)
    - Aggregating data (reduce)
    - Functional pipelines
    - Working with infinite iterators
    
    When to Use Comprehensions Instead:
    - More readable for simple operations
    - Need immediate list/dict/set
    - Multiple conditions
    - Pythonic code style
    
    Performance:
    - map/filter: Slightly slower than comprehensions
    - reduce: No comprehension alternative for general case
    - Comprehensions: Optimized in CPython
    
    Security Considerations:
    - Validate input data before processing
    - Be careful with user-provided functions
    - Consider memory limits for large datasets
    - Use itertools for infinite sequences
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 4, Day 1: map, filter, and reduce")
    print("=" * 60)
    print()
    
    map_basics()
    filter_basics()
    reduce_basics()
    map_vs_comprehension()
    chaining_operations()
    process_employee_data()
    test_custom_functions()
    test_pipeline()
    
    print("=" * 60)
    print("✅ Day 1 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. map() transforms elements lazily")
    print("2. filter() selects elements lazily")
    print("3. reduce() accumulates values eagerly")
    print("4. List comprehensions often more Pythonic")

