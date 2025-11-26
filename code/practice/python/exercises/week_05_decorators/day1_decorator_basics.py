"""
Week 5, Day 1: Decorator Basics

Learning Objectives:
- Understand what decorators are
- Learn decorator syntax (@decorator)
- Master function wrapping with functools.wraps
- Practice writing simple decorators
- Understand decorator execution order

Time: 10-15 minutes
"""

from functools import wraps
import time

# ============================================================
# EXERCISE 1: What is a Decorator?
# ============================================================

def what_is_decorator():
    """
    Understand decorators as functions that wrap other functions.
    
    Decorator: A function that takes a function and returns a modified version
    """
    print("--- Exercise 1: What is a Decorator? ---")
    
    def my_decorator(func):
        """Simple decorator that wraps a function"""
        def wrapper():
            print("Before function call")
            result = func()
            print("After function call")
            return result
        return wrapper
    
    # Manual decoration
    def say_hello():
        print("Hello!")
    
    decorated = my_decorator(say_hello)
    
    print("Calling decorated function:")
    decorated()
    
    # Using @ syntax
    @my_decorator
    def say_goodbye():
        print("Goodbye!")
    
    print("\nUsing @ syntax:")
    say_goodbye()
    
    print("\n💡 @decorator is syntactic sugar for:")
    print("   func = decorator(func)")
    
    print()

# ============================================================
# EXERCISE 2: Decorators with Arguments
# ============================================================

def decorators_with_arguments():
    """
    Learn to handle function arguments in decorators.
    
    Use *args and **kwargs to accept any arguments
    """
    print("--- Exercise 2: Decorators with Arguments ---")
    
    def trace(func):
        """Trace function calls with arguments"""
        def wrapper(*args, **kwargs):
            args_str = ', '.join(repr(a) for a in args)
            kwargs_str = ', '.join(f"{k}={v!r}" for k, v in kwargs.items())
            all_args = ', '.join(filter(None, [args_str, kwargs_str]))
            
            print(f"Calling {func.__name__}({all_args})")
            result = func(*args, **kwargs)
            print(f"  → returned {result!r}")
            return result
        return wrapper
    
    @trace
    def add(a, b):
        return a + b
    
    @trace
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"
    
    print("Testing traced functions:")
    add(3, 5)
    greet("Alice")
    greet("Bob", greeting="Hi")
    
    print()

# ============================================================
# EXERCISE 3: functools.wraps
# ============================================================

def wraps_importance():
    """
    Learn why functools.wraps is important.
    
    @wraps preserves original function metadata
    """
    print("--- Exercise 3: functools.wraps ---")
    
    # Without @wraps
    def bad_decorator(func):
        def wrapper(*args, **kwargs):
            """Wrapper function"""
            return func(*args, **kwargs)
        return wrapper
    
    # With @wraps
    def good_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper function"""
            return func(*args, **kwargs)
        return wrapper
    
    @bad_decorator
    def function_bad():
        """Original docstring"""
        pass
    
    @good_decorator
    def function_good():
        """Original docstring"""
        pass
    
    print("Without @wraps:")
    print(f"  Name: {function_bad.__name__}")
    print(f"  Doc: {function_bad.__doc__}")
    
    print("\nWith @wraps:")
    print(f"  Name: {function_good.__name__}")
    print(f"  Doc: {function_good.__doc__}")
    
    print("\n💡 Always use @wraps to preserve function metadata!")
    
    print()

# ============================================================
# EXERCISE 4: Timer Decorator
# ============================================================

def timer(func):
    """
    Time function execution.
    
    TODO: Implement timing decorator
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.6f}s")
        return result
    return wrapper

def test_timer():
    """Test timer decorator"""
    print("--- Exercise 4: Timer Decorator ---")
    
    @timer
    def slow_function():
        """Simulate slow operation"""
        time.sleep(0.1)
        return "Done"
    
    @timer
    def fast_function():
        """Fast operation"""
        return sum(range(1000))
    
    print("Testing timer:")
    slow_function()
    fast_function()
    
    print()

# ============================================================
# EXERCISE 5: Decorator Execution Order
# ============================================================

def execution_order():
    """
    Understand when decorators execute.
    
    Decorators run at function definition time, not call time
    """
    print("--- Exercise 5: Decorator Execution Order ---")
    
    def decorator_factory(name):
        """Create a decorator with a name"""
        print(f"  Creating decorator: {name}")
        
        def decorator(func):
            print(f"  Decorating {func.__name__} with {name}")
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(f"  [{name}] Before {func.__name__}")
                result = func(*args, **kwargs)
                print(f"  [{name}] After {func.__name__}")
                return result
            return wrapper
        return decorator
    
    print("Defining function with decorators:")
    
    @decorator_factory("outer")
    @decorator_factory("inner")
    def my_function():
        print("  [Function] Executing")
    
    print("\nCalling function:")
    my_function()
    
    print("\n💡 Decorators execute at definition time")
    print("💡 Multiple decorators apply bottom-to-top")
    
    print()

# ============================================================
# EXERCISE 6: Stacking Decorators
# ============================================================

def stacking_decorators():
    """
    Learn to stack multiple decorators.
    
    Order matters: bottom decorator wraps first
    """
    print("--- Exercise 6: Stacking Decorators ---")
    
    def uppercase(func):
        """Convert result to uppercase"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result.upper()
        return wrapper
    
    def exclaim(func):
        """Add exclamation marks"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"{result}!!!"
        return wrapper
    
    @exclaim
    @uppercase
    def greet(name):
        return f"hello, {name}"
    
    print(f"greet('alice'): {greet('alice')}")
    
    # Different order
    @uppercase
    @exclaim
    def greet2(name):
        return f"hello, {name}"
    
    print(f"greet2('alice'): {greet2('alice')}")
    
    print("\n💡 Decorator order matters!")
    print("  @exclaim")
    print("  @uppercase")
    print("  def func(): ...")
    print("  → uppercase(func) then exclaim(uppercase(func))")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - Logging Decorator
# ============================================================

def logging_decorator(func):
    """
    Log function calls with arguments and results.
    
    TODO: Implement comprehensive logging
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Format arguments
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        
        print(f"[LOG] Calling {func.__name__}({signature})")
        
        try:
            result = func(*args, **kwargs)
            print(f"[LOG] {func.__name__} returned {result!r}")
            return result
        except Exception as e:
            print(f"[LOG] {func.__name__} raised {type(e).__name__}: {e}")
            raise
    
    return wrapper

def test_logging():
    """Test logging decorator"""
    print("--- Exercise 7: Logging Decorator ---")
    
    @logging_decorator
    def divide(a, b):
        """Divide two numbers"""
        return a / b
    
    @logging_decorator
    def process_data(items, multiplier=2):
        """Process list of items"""
        return [x * multiplier for x in items]
    
    print("Testing logging:")
    divide(10, 2)
    process_data([1, 2, 3], multiplier=3)
    
    print("\nTesting error logging:")
    try:
        divide(10, 0)
    except ZeroDivisionError:
        pass
    
    print()

# ============================================================
# BONUS CHALLENGE: Debug Decorator
# ============================================================

def debug(func):
    """
    Debug decorator showing detailed execution info.
    
    TODO: Implement debug decorator
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Show function info
        print(f"\n{'='*60}")
        print(f"DEBUG: {func.__name__}")
        print(f"{'='*60}")
        
        # Show arguments
        print(f"Arguments:")
        for i, arg in enumerate(args):
            print(f"  args[{i}] = {arg!r}")
        for key, value in kwargs.items():
            print(f"  {key} = {value!r}")
        
        # Execute
        print(f"\nExecuting...")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        
        # Show result
        print(f"\nResult: {result!r}")
        print(f"Time: {elapsed:.6f}s")
        print(f"{'='*60}\n")
        
        return result
    
    return wrapper

def test_debug():
    """Test debug decorator"""
    print("--- Bonus Challenge: Debug Decorator ---")
    
    @debug
    def calculate(x, y, operation='add'):
        """Perform calculation"""
        if operation == 'add':
            return x + y
        elif operation == 'multiply':
            return x * y
        return None
    
    calculate(5, 3, operation='multiply')
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Decorator Definition:
    - Time: O(1) - executed once at definition
    - Space: O(1) - creates wrapper function
    
    Decorator Execution:
    - Time: O(f) where f = wrapped function time
    - Space: O(1) additional (closure overhead minimal)
    - Overhead: Usually negligible
    
    Benefits:
    - Separation of concerns
    - Code reuse
    - Clean syntax
    - Aspect-oriented programming
    
    Use Cases:
    - Logging
    - Timing/profiling
    - Authentication/authorization
    - Caching/memoization
    - Input validation
    - Retry logic
    - Rate limiting
    
    Best Practices:
    - Always use @wraps
    - Handle *args, **kwargs
    - Preserve function signature
    - Document decorator behavior
    - Keep decorators simple
    
    Common Patterns:
    - @timer - measure execution time
    - @log - log function calls
    - @retry - retry on failure
    - @cache - memoize results
    - @validate - validate inputs
    
    Security Considerations:
    - Validate decorator inputs
    - Be careful with logging sensitive data
    - Consider performance impact
    - Handle exceptions properly
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 5, Day 1: Decorator Basics")
    print("=" * 60)
    print()
    
    what_is_decorator()
    decorators_with_arguments()
    wraps_importance()
    test_timer()
    execution_order()
    stacking_decorators()
    test_logging()
    test_debug()
    
    print("=" * 60)
    print("✅ Day 1 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Decorators wrap functions to add behavior")
    print("2. @decorator is sugar for func = decorator(func)")
    print("3. Always use @wraps to preserve metadata")
    print("4. Decorators execute at definition time")

