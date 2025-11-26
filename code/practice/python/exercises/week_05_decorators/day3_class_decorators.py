"""
Week 5, Day 3: Class-Based Decorators

Learning Objectives:
- Learn to create decorators using classes
- Understand __call__ method for callable objects
- Master stateful decorators
- Practice decorator classes with parameters
- Compare class vs function decorators

Time: 10-15 minutes
"""

from functools import wraps
import time

# ============================================================
# EXERCISE 1: Basic Class Decorator
# ============================================================

def basic_class_decorator():
    """
    Learn to create decorators using classes.
    
    Class decorator: Implements __call__ to be callable
    """
    print("--- Exercise 1: Basic Class Decorator ---")
    
    class SimpleDecorator:
        """Simple class-based decorator"""
        
        def __init__(self, func):
            self.func = func
            self.__name__ = func.__name__
            self.__doc__ = func.__doc__
        
        def __call__(self, *args, **kwargs):
            print(f"Before {self.func.__name__}")
            result = self.func(*args, **kwargs)
            print(f"After {self.func.__name__}")
            return result
    
    @SimpleDecorator
    def greet(name):
        """Greet someone"""
        print(f"Hello, {name}!")
    
    print("Calling decorated function:")
    greet("Alice")
    
    print(f"\nFunction name: {greet.__name__}")
    print(f"Function doc: {greet.__doc__}")
    
    print()

# ============================================================
# EXERCISE 2: Stateful Decorator
# ============================================================

class CallCounter:
    """
    Count how many times a function is called.
    
    TODO: Implement stateful decorator using class
    """
    
    def __init__(self, func):
        self.func = func
        self.count = 0
        self.__name__ = func.__name__
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call #{self.count} to {self.func.__name__}")
        return self.func(*args, **kwargs)
    
    def reset(self):
        """Reset counter"""
        self.count = 0

def test_call_counter():
    """Test call counter decorator"""
    print("--- Exercise 2: Stateful Decorator ---")
    
    @CallCounter
    def say_hello():
        return "Hello!"
    
    print("Making multiple calls:")
    for _ in range(3):
        say_hello()
    
    print(f"\nTotal calls: {say_hello.count}")
    
    say_hello.reset()
    print(f"After reset: {say_hello.count}")
    
    print()

# ============================================================
# EXERCISE 3: Class Decorator with Parameters
# ============================================================

class Retry:
    """
    Retry decorator with configurable attempts.
    
    TODO: Implement parametrized class decorator
    """
    
    def __init__(self, max_attempts=3, delay=0.1):
        self.max_attempts = max_attempts
        self.delay = delay
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, self.max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == self.max_attempts:
                        print(f"  Failed after {self.max_attempts} attempts")
                        raise
                    print(f"  Attempt {attempt} failed: {e}. Retrying...")
                    time.sleep(self.delay)
        return wrapper

def test_retry_class():
    """Test retry class decorator"""
    print("--- Exercise 3: Class Decorator with Parameters ---")
    
    call_count = 0
    
    @Retry(max_attempts=3, delay=0.05)
    def unreliable_function():
        nonlocal call_count
        call_count += 1
        print(f"  Attempt {call_count}")
        if call_count < 3:
            raise ValueError("Not yet!")
        return "Success!"
    
    result = unreliable_function()
    print(f"Result: {result}")
    
    print()

# ============================================================
# EXERCISE 4: Timer with Statistics
# ============================================================

class Timer:
    """
    Timer decorator that tracks statistics.
    
    TODO: Track min, max, average execution time
    """
    
    def __init__(self, func):
        self.func = func
        self.times = []
        self.__name__ = func.__name__
    
    def __call__(self, *args, **kwargs):
        start = time.perf_counter()
        result = self.func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        
        self.times.append(elapsed)
        print(f"{self.func.__name__} took {elapsed:.6f}s")
        
        return result
    
    def stats(self):
        """Get timing statistics"""
        if not self.times:
            return "No calls yet"
        
        return {
            'calls': len(self.times),
            'total': sum(self.times),
            'average': sum(self.times) / len(self.times),
            'min': min(self.times),
            'max': max(self.times)
        }

def test_timer_stats():
    """Test timer with statistics"""
    print("--- Exercise 4: Timer with Statistics ---")
    
    @Timer
    def variable_time(n):
        time.sleep(n * 0.01)
        return n
    
    print("Making timed calls:")
    for i in range(1, 4):
        variable_time(i)
    
    stats = variable_time.stats()
    print(f"\nStatistics:")
    print(f"  Calls: {stats['calls']}")
    print(f"  Total: {stats['total']:.6f}s")
    print(f"  Average: {stats['average']:.6f}s")
    print(f"  Min: {stats['min']:.6f}s")
    print(f"  Max: {stats['max']:.6f}s")
    
    print()

# ============================================================
# EXERCISE 5: Cache with LRU Policy
# ============================================================

class LRUCache:
    """
    LRU cache decorator using class.
    
    TODO: Implement LRU caching
    """
    
    def __init__(self, maxsize=128):
        self.maxsize = maxsize
    
    def __call__(self, func):
        from collections import OrderedDict
        cache = OrderedDict()
        
        @wraps(func)
        def wrapper(*args):
            if args in cache:
                # Move to end (most recent)
                cache.move_to_end(args)
                print(f"  Cache hit for {func.__name__}{args}")
                return cache[args]
            
            # Compute and cache
            print(f"  Computing {func.__name__}{args}")
            result = func(*args)
            
            if len(cache) >= self.maxsize:
                # Remove least recently used
                cache.popitem(last=False)
            
            cache[args] = result
            return result
        
        wrapper.cache = cache
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper

def test_lru_cache():
    """Test LRU cache decorator"""
    print("--- Exercise 5: LRU Cache ---")
    
    @LRUCache(maxsize=3)
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    print("Computing fibonacci(5):")
    result = fibonacci(5)
    print(f"Result: {result}")
    
    print(f"\nCache size: {len(fibonacci.cache)}")
    print(f"Cached values: {dict(fibonacci.cache)}")
    
    print()

# ============================================================
# EXERCISE 6: Validator with Multiple Rules
# ============================================================

class Validator:
    """
    Validator decorator with multiple rules.
    
    TODO: Validate function arguments against rules
    """
    
    def __init__(self, **rules):
        """
        Initialize with validation rules.
        
        Example: Validator(x=lambda v: v > 0, y=lambda v: isinstance(v, int))
        """
        self.rules = rules
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get function parameter names
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate each argument
            for param_name, value in bound_args.arguments.items():
                if param_name in self.rules:
                    validator = self.rules[param_name]
                    if not validator(value):
                        raise ValueError(
                            f"Validation failed for parameter '{param_name}' "
                            f"with value {value!r}"
                        )
            
            return func(*args, **kwargs)
        return wrapper

def test_validator():
    """Test validator decorator"""
    print("--- Exercise 6: Validator ---")
    
    @Validator(
        x=lambda v: isinstance(v, int) and v > 0,
        y=lambda v: isinstance(v, int) and v > 0
    )
    def add(x, y):
        return x + y
    
    @Validator(
        name=lambda v: isinstance(v, str) and len(v) > 0,
        age=lambda v: isinstance(v, int) and 0 < v < 150
    )
    def create_person(name, age):
        return {"name": name, "age": age}
    
    print("Valid calls:")
    print(f"  add(3, 5) = {add(3, 5)}")
    print(f"  create_person('Alice', 30) = {create_person('Alice', 30)}")
    
    print("\nInvalid calls:")
    try:
        add(-1, 5)
    except ValueError as e:
        print(f"  add(-1, 5) → {e}")
    
    try:
        create_person("", 30)
    except ValueError as e:
        print(f"  create_person('', 30) → {e}")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - Rate Limiter
# ============================================================

class RateLimiter:
    """
    Rate limiter with per-function state.
    
    TODO: Implement rate limiting with sliding window
    """
    
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
    
    def __call__(self, func):
        calls = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # Remove old calls
            while calls and calls[0] < now - self.period:
                calls.pop(0)
            
            # Check limit
            if len(calls) >= self.max_calls:
                wait_time = self.period - (now - calls[0])
                raise RuntimeError(
                    f"Rate limit exceeded. "
                    f"Wait {wait_time:.2f}s before calling again."
                )
            
            # Record call
            calls.append(now)
            return func(*args, **kwargs)
        
        wrapper.calls = calls
        return wrapper

def test_rate_limiter():
    """Test rate limiter"""
    print("--- Exercise 7: Rate Limiter ---")
    
    @RateLimiter(max_calls=3, period=1.0)
    def api_call(endpoint):
        print(f"  Calling {endpoint}")
        return f"Response from {endpoint}"
    
    print("Making calls (limit: 3 per second):")
    for i in range(5):
        try:
            result = api_call(f"/api/endpoint{i}")
            print(f"    Success: {result}")
        except RuntimeError as e:
            print(f"    Blocked: {e}")
        time.sleep(0.2)
    
    print()

# ============================================================
# BONUS CHALLENGE: Decorator with __get__ (Descriptor)
# ============================================================

class Method:
    """
    Method decorator that works with instance methods.
    
    TODO: Implement descriptor protocol for methods
    """
    
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        """Descriptor protocol for binding to instance"""
        if instance is None:
            return self
        
        # Return bound method
        def bound_method(*args, **kwargs):
            print(f"  Calling {self.func.__name__} on {instance}")
            return self.func(instance, *args, **kwargs)
        
        return bound_method

def test_method_decorator():
    """Test method decorator with descriptor protocol"""
    print("--- Bonus Challenge: Method Decorator ---")
    
    class Counter:
        def __init__(self):
            self.count = 0
        
        @Method
        def increment(self):
            self.count += 1
            return self.count
    
    counter = Counter()
    print(f"increment(): {counter.increment()}")
    print(f"increment(): {counter.increment()}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Class Decorators:
    - Instantiation: O(1)
    - __call__: O(f) where f = function time
    - State storage: O(1) per instance
    
    Benefits:
    - Can maintain state
    - More readable for complex decorators
    - Can have multiple methods
    - Natural for stateful operations
    
    Drawbacks:
    - Slightly more verbose
    - Need to handle __name__, __doc__ manually
    - Or use functools.wraps in __call__
    
    Use Cases:
    - Stateful decorators (counters, caches)
    - Complex configuration
    - Multiple related methods
    - When state needs to be inspected/modified
    
    Class vs Function Decorators:
    - Class: Better for state, multiple methods
    - Function: Simpler, more common
    - Choose based on complexity
    
    Best Practices:
    - Preserve function metadata
    - Use __name__ and __doc__ attributes
    - Or use @wraps in __call__
    - Provide methods to inspect/modify state
    - Document state behavior
    
    Common Patterns:
    - @CallCounter - track invocations
    - @Timer - timing with statistics
    - @Cache - caching with policies
    - @RateLimiter - rate limiting
    - @Validator - input validation
    
    Security Considerations:
    - Validate decorator parameters
    - Be careful with shared state
    - Consider thread safety
    - Handle resource cleanup
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 5, Day 3: Class-Based Decorators")
    print("=" * 60)
    print()
    
    basic_class_decorator()
    test_call_counter()
    test_retry_class()
    test_timer_stats()
    test_lru_cache()
    test_validator()
    test_rate_limiter()
    test_method_decorator()
    
    print("=" * 60)
    print("✅ Day 3 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Class decorators use __call__ to be callable")
    print("2. Great for stateful decorators")
    print("3. Can have multiple methods for state management")
    print("4. Remember to preserve function metadata")

