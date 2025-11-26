"""
Week 4, Day 5: Higher-Order Functions

Learning Objectives:
- Master functions that take/return functions
- Learn common higher-order function patterns
- Understand closures and scope
- Practice building function factories
- Create reusable function combinators

Time: 10-15 minutes
"""

from typing import Callable, Any, List
from functools import wraps

# ============================================================
# EXERCISE 1: Functions as Arguments
# ============================================================

def functions_as_arguments():
    """
    Learn to pass functions as arguments.
    
    Higher-order function: Takes functions as parameters
    """
    print("--- Exercise 1: Functions as Arguments ---")
    
    def apply_operation(x, y, operation):
        """Apply operation to two numbers"""
        return operation(x, y)
    
    # Different operations
    result_add = apply_operation(10, 5, lambda x, y: x + y)
    result_mul = apply_operation(10, 5, lambda x, y: x * y)
    result_pow = apply_operation(10, 5, lambda x, y: x ** y)
    
    print(f"apply_operation(10, 5, add) = {result_add}")
    print(f"apply_operation(10, 5, mul) = {result_mul}")
    print(f"apply_operation(10, 5, pow) = {result_pow}")
    
    # Process list with custom function
    def process_list(items, processor):
        """Process each item with processor function"""
        return [processor(item) for item in items]
    
    numbers = [1, 2, 3, 4, 5]
    squared = process_list(numbers, lambda x: x ** 2)
    doubled = process_list(numbers, lambda x: x * 2)
    
    print(f"\nprocess_list({numbers}, square) = {squared}")
    print(f"process_list({numbers}, double) = {doubled}")
    
    print()

# ============================================================
# EXERCISE 2: Functions as Return Values
# ============================================================

def functions_as_return_values():
    """
    Learn to return functions from functions.
    
    Function factory: Returns new functions
    """
    print("--- Exercise 2: Functions as Return Values ---")
    
    def make_multiplier(n):
        """Create a multiplier function"""
        def multiplier(x):
            return x * n
        return multiplier
    
    times_2 = make_multiplier(2)
    times_10 = make_multiplier(10)
    
    print(f"times_2 = make_multiplier(2)")
    print(f"times_2(5) = {times_2(5)}")
    
    print(f"\ntimes_10 = make_multiplier(10)")
    print(f"times_10(5) = {times_10(5)}")
    
    # Power function factory
    def make_power(exponent):
        """Create a power function"""
        return lambda x: x ** exponent
    
    square = make_power(2)
    cube = make_power(3)
    
    print(f"\nsquare = make_power(2)")
    print(f"square(5) = {square(5)}")
    print(f"cube(5) = {cube(5)}")
    
    print()

# ============================================================
# EXERCISE 3: Closures and Scope
# ============================================================

def closures_and_scope():
    """
    Understand closures and variable capture.
    
    Closure: Function that remembers its enclosing scope
    """
    print("--- Exercise 3: Closures and Scope ---")
    
    def make_counter(start=0):
        """Create a counter with state"""
        count = start
        
        def increment():
            nonlocal count
            count += 1
            return count
        
        def decrement():
            nonlocal count
            count -= 1
            return count
        
        def get_count():
            return count
        
        return increment, decrement, get_count
    
    inc, dec, get = make_counter(10)
    
    print(f"Starting count: {get()}")
    print(f"After increment: {inc()}")
    print(f"After increment: {inc()}")
    print(f"After decrement: {dec()}")
    print(f"Final count: {get()}")
    
    # Multiple independent counters
    inc1, _, get1 = make_counter(0)
    inc2, _, get2 = make_counter(100)
    
    inc1()
    inc1()
    inc2()
    
    print(f"\nCounter 1: {get1()}")
    print(f"Counter 2: {get2()}")
    
    print()

# ============================================================
# EXERCISE 4: Function Decorators (Higher-Order Functions)
# ============================================================

def decorator_examples():
    """
    Use decorators as higher-order functions.
    
    Decorator: Function that wraps another function
    """
    print("--- Exercise 4: Decorators as Higher-Order Functions ---")
    
    def timer(func):
        """Time function execution"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"  {func.__name__} took {elapsed:.6f}s")
            return result
        return wrapper
    
    @timer
    def slow_function():
        """Simulate slow operation"""
        import time
        time.sleep(0.1)
        return "Done"
    
    print("Calling slow_function():")
    result = slow_function()
    print(f"  Result: {result}")
    
    # Parametrized decorator
    def repeat(times):
        """Repeat function execution"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                results = []
                for _ in range(times):
                    results.append(func(*args, **kwargs))
                return results
            return wrapper
        return decorator
    
    @repeat(3)
    def greet(name):
        return f"Hello, {name}!"
    
    print(f"\ngreet('Alice') with @repeat(3):")
    results = greet('Alice')
    for r in results:
        print(f"  {r}")
    
    print()

# ============================================================
# EXERCISE 5: Function Combinators
# ============================================================

def function_combinators():
    """
    Build function combinators.
    
    Combinator: Higher-order function that combines functions
    """
    print("--- Exercise 5: Function Combinators ---")
    
    def compose(f, g):
        """Compose two functions: f(g(x))"""
        return lambda x: f(g(x))
    
    def chain(*functions):
        """Chain multiple functions"""
        def chained(x):
            result = x
            for func in functions:
                result = func(result)
            return result
        return chained
    
    # Use combinators
    add_10 = lambda x: x + 10
    multiply_2 = lambda x: x * 2
    square = lambda x: x ** 2
    
    # Compose two functions
    add_then_multiply = compose(multiply_2, add_10)
    print(f"compose(multiply_2, add_10)(5) = {add_then_multiply(5)}")
    print(f"  Steps: 5 → 15 → 30")
    
    # Chain multiple functions
    transform = chain(add_10, multiply_2, square)
    print(f"\nchain(add_10, multiply_2, square)(5) = {transform(5)}")
    print(f"  Steps: 5 → 15 → 30 → 900")
    
    print()

# ============================================================
# EXERCISE 6: Real-World Scenario - Validation Pipeline
# ============================================================

def validation_pipeline():
    """
    Build validation pipeline using higher-order functions.
    
    TODO: Create composable validators
    """
    print("--- Exercise 6: Validation Pipeline ---")
    
    def validator(predicate, error_message):
        """Create a validator function"""
        def validate(value):
            if not predicate(value):
                raise ValueError(error_message)
            return value
        return validate
    
    # Create validators
    not_empty = validator(
        lambda s: len(s) > 0,
        "Value cannot be empty"
    )
    
    min_length = lambda n: validator(
        lambda s: len(s) >= n,
        f"Value must be at least {n} characters"
    )
    
    max_length = lambda n: validator(
        lambda s: len(s) <= n,
        f"Value must be at most {n} characters"
    )
    
    is_numeric = validator(
        lambda s: s.isdigit(),
        "Value must be numeric"
    )
    
    def compose_validators(*validators):
        """Compose multiple validators"""
        def validate(value):
            for validator_func in validators:
                value = validator_func(value)
            return value
        return validate
    
    # Build validation pipelines
    username_validator = compose_validators(
        not_empty,
        min_length(3),
        max_length(20)
    )
    
    pin_validator = compose_validators(
        not_empty,
        is_numeric,
        min_length(4),
        max_length(4)
    )
    
    # Test validators
    print("Testing username_validator:")
    test_usernames = ["alice", "ab", "a" * 25, ""]
    for username in test_usernames:
        try:
            username_validator(username)
            print(f"  '{username}' ✓ Valid")
        except ValueError as e:
            print(f"  '{username}' ✗ {e}")
    
    print("\nTesting pin_validator:")
    test_pins = ["1234", "123", "12345", "abcd"]
    for pin in test_pins:
        try:
            pin_validator(pin)
            print(f"  '{pin}' ✓ Valid")
        except ValueError as e:
            print(f"  '{pin}' ✗ {e}")
    
    print()

# ============================================================
# EXERCISE 7: Memoization (Higher-Order Function)
# ============================================================

def memoization_example():
    """
    Implement memoization as higher-order function.
    
    TODO: Cache function results
    """
    print("--- Exercise 7: Memoization ---")
    
    def memoize(func):
        """Cache function results"""
        cache = {}
        
        @wraps(func)
        def wrapper(*args):
            if args not in cache:
                print(f"  Computing {func.__name__}{args}...")
                cache[args] = func(*args)
            else:
                print(f"  Cached {func.__name__}{args}")
            return cache[args]
        
        wrapper.cache = cache
        return wrapper
    
    @memoize
    def fibonacci(n):
        """Calculate fibonacci number"""
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    print("Calculating fibonacci(5):")
    result = fibonacci(5)
    print(f"Result: {result}")
    
    print("\nCalculating fibonacci(5) again:")
    result = fibonacci(5)
    print(f"Result: {result}")
    
    print(f"\nCache size: {len(fibonacci.cache)}")
    print(f"Cache contents: {dict(sorted(fibonacci.cache.items()))}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Function Builder
# ============================================================

class FunctionBuilder:
    """
    Builder for creating complex functions.
    
    TODO: Implement fluent function builder
    """
    
    def __init__(self):
        self._operations = []
    
    def add(self, n):
        """Add operation"""
        self._operations.append(lambda x: x + n)
        return self
    
    def multiply(self, n):
        """Multiply operation"""
        self._operations.append(lambda x: x * n)
        return self
    
    def power(self, n):
        """Power operation"""
        self._operations.append(lambda x: x ** n)
        return self
    
    def filter_positive(self):
        """Filter positive numbers"""
        self._operations.append(lambda x: x if x > 0 else 0)
        return self
    
    def build(self):
        """Build the final function"""
        def composed(x):
            result = x
            for op in self._operations:
                result = op(result)
            return result
        return composed

def test_function_builder():
    """Test function builder"""
    print("--- Bonus Challenge: Function Builder ---")
    
    # Build custom function
    func = (FunctionBuilder()
            .add(10)
            .multiply(2)
            .power(2)
            .build())
    
    print("func = FunctionBuilder()")
    print("  .add(10)")
    print("  .multiply(2)")
    print("  .power(2)")
    print("  .build()")
    
    result = func(5)
    print(f"\nfunc(5) = {result}")
    print(f"  Steps: 5 → 15 → 30 → 900")
    
    # Build another function
    func2 = (FunctionBuilder()
             .multiply(3)
             .add(5)
             .build())
    
    print(f"\nfunc2(10) = {func2(10)}")
    print(f"  Steps: 10 → 30 → 35")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Higher-Order Functions:
    - Creation: O(1)
    - Execution: Depends on wrapped function
    - Closure overhead: Minimal
    
    Closures:
    - Space: O(k) where k = captured variables
    - Access: O(1)
    - Independent instances don't share state
    
    Memoization:
    - Time: O(1) for cached results
    - Space: O(n) where n = unique calls
    - Trade-off: Memory for speed
    
    Benefits:
    - Code reuse
    - Abstraction
    - Separation of concerns
    - Testability
    - Composability
    
    Use Cases:
    - Decorators
    - Callbacks
    - Event handlers
    - Strategy pattern
    - Factory pattern
    - Middleware
    
    Best Practices:
    - Keep functions pure when possible
    - Use @wraps for decorators
    - Document closure behavior
    - Be careful with mutable closures
    - Consider memory with memoization
    
    Common Patterns:
    - Function factories
    - Decorators
    - Callbacks
    - Currying
    - Partial application
    - Memoization
    
    Security Considerations:
    - Validate function arguments
    - Be careful with user-provided functions
    - Consider resource limits for memoization
    - Handle exceptions in wrapped functions
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 4, Day 5: Higher-Order Functions")
    print("=" * 60)
    print()
    
    functions_as_arguments()
    functions_as_return_values()
    closures_and_scope()
    decorator_examples()
    function_combinators()
    validation_pipeline()
    memoization_example()
    test_function_builder()
    
    print("=" * 60)
    print("✅ Day 5 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Higher-order functions take/return functions")
    print("2. Closures capture enclosing scope")
    print("3. Decorators are powerful higher-order functions")
    print("4. Enable code reuse and abstraction")

