"""
Week 5, Day 2: Parametrized Decorators

Learning Objectives:
- Learn to create decorators that accept parameters
- Understand the three-level function pattern
- Master decorator factories
- Practice configurable decorators
- Build reusable decorator templates

Time: 10-15 minutes
"""

from functools import wraps
import time

# ============================================================
# EXERCISE 1: Decorator Factory Pattern
# ============================================================

def decorator_factory_pattern():
    """
    Learn the three-level function pattern for parametrized decorators.
    
    Pattern: decorator_factory(params) → decorator → wrapper
    """
    print("--- Exercise 1: Decorator Factory Pattern ---")
    
    def repeat(times):
        """Decorator factory that repeats function execution"""
        print(f"  [Factory] Creating decorator with times={times}")
        
        def decorator(func):
            print(f"  [Decorator] Wrapping {func.__name__}")
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(f"  [Wrapper] Executing {func.__name__} {times} times")
                results = []
                for i in range(times):
                    result = func(*args, **kwargs)
                    results.append(result)
                return results
            return wrapper
        return decorator
    
    print("Defining function:")
    
    @repeat(times=3)
    def greet(name):
        return f"Hello, {name}!"
    
    print("\nCalling function:")
    results = greet("Alice")
    for r in results:
        print(f"  {r}")
    
    print("\n💡 Three levels:")
    print("  1. Factory: accepts parameters")
    print("  2. Decorator: accepts function")
    print("  3. Wrapper: accepts function arguments")
    
    print()

# ============================================================
# EXERCISE 2: Retry Decorator
# ============================================================

def retry(max_attempts=3, delay=0.1):
    """
    Retry function on failure.
    
    TODO: Implement retry logic with configurable attempts
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        print(f"  Failed after {max_attempts} attempts")
                        raise
                    print(f"  Attempt {attempts} failed: {e}. Retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator

def test_retry():
    """Test retry decorator"""
    print("--- Exercise 2: Retry Decorator ---")
    
    call_count = 0
    
    @retry(max_attempts=3, delay=0.05)
    def unreliable_function():
        """Function that fails first 2 times"""
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
# EXERCISE 3: Timeout Decorator
# ============================================================

def timeout(seconds):
    """
    Timeout decorator (simplified - just logs).
    
    TODO: Implement timeout warning
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            
            if elapsed > seconds:
                print(f"  ⚠️  {func.__name__} exceeded timeout ({elapsed:.2f}s > {seconds}s)")
            else:
                print(f"  ✓ {func.__name__} completed in {elapsed:.2f}s")
            
            return result
        return wrapper
    return decorator

def test_timeout():
    """Test timeout decorator"""
    print("--- Exercise 3: Timeout Decorator ---")
    
    @timeout(seconds=0.1)
    def fast_function():
        time.sleep(0.05)
        return "Fast"
    
    @timeout(seconds=0.1)
    def slow_function():
        time.sleep(0.15)
        return "Slow"
    
    fast_function()
    slow_function()
    
    print()

# ============================================================
# EXERCISE 4: Rate Limiter Decorator
# ============================================================

def rate_limit(max_calls, period):
    """
    Rate limit function calls.
    
    TODO: Limit calls to max_calls per period (seconds)
    """
    def decorator(func):
        calls = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # Remove old calls outside period
            while calls and calls[0] < now - period:
                calls.pop(0)
            
            # Check rate limit
            if len(calls) >= max_calls:
                wait_time = period - (now - calls[0])
                print(f"  Rate limit exceeded. Wait {wait_time:.2f}s")
                return None
            
            # Record call and execute
            calls.append(now)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

def test_rate_limit():
    """Test rate limiter"""
    print("--- Exercise 4: Rate Limiter ---")
    
    @rate_limit(max_calls=3, period=1.0)
    def api_call(endpoint):
        print(f"  Calling {endpoint}")
        return f"Response from {endpoint}"
    
    print("Making 5 rapid calls (limit: 3 per second):")
    for i in range(5):
        result = api_call(f"/api/endpoint{i}")
        if result:
            print(f"    {result}")
        time.sleep(0.1)
    
    print()

# ============================================================
# EXERCISE 5: Validation Decorator
# ============================================================

def validate(*validators):
    """
    Validate function arguments.
    
    TODO: Apply validators to function arguments
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Validate positional arguments
            for i, (arg, validator) in enumerate(zip(args, validators)):
                if not validator(arg):
                    raise ValueError(f"Argument {i} failed validation")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def test_validate():
    """Test validation decorator"""
    print("--- Exercise 5: Validation Decorator ---")
    
    @validate(
        lambda x: isinstance(x, int),
        lambda x: isinstance(x, int),
    )
    def add(a, b):
        return a + b
    
    @validate(
        lambda s: isinstance(s, str) and len(s) > 0,
    )
    def greet(name):
        return f"Hello, {name}!"
    
    print("Valid calls:")
    print(f"  add(3, 5) = {add(3, 5)}")
    print(f"  greet('Alice') = {greet('Alice')}")
    
    print("\nInvalid calls:")
    try:
        add("3", 5)
    except ValueError as e:
        print(f"  add('3', 5) → {e}")
    
    try:
        greet("")
    except ValueError as e:
        print(f"  greet('') → {e}")
    
    print()

# ============================================================
# EXERCISE 6: Cache Decorator with TTL
# ============================================================

def cache_with_ttl(ttl_seconds):
    """
    Cache function results with time-to-live.
    
    TODO: Implement caching with expiration
    """
    def decorator(func):
        cache = {}
        
        @wraps(func)
        def wrapper(*args):
            now = time.time()
            
            # Check cache
            if args in cache:
                result, timestamp = cache[args]
                if now - timestamp < ttl_seconds:
                    print(f"  Cache hit for {func.__name__}{args}")
                    return result
                else:
                    print(f"  Cache expired for {func.__name__}{args}")
            
            # Compute and cache
            print(f"  Computing {func.__name__}{args}")
            result = func(*args)
            cache[args] = (result, now)
            return result
        
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
    return decorator

def test_cache_ttl():
    """Test cache with TTL"""
    print("--- Exercise 6: Cache with TTL ---")
    
    @cache_with_ttl(ttl_seconds=0.5)
    def expensive_function(n):
        time.sleep(0.1)
        return n ** 2
    
    print("First call:")
    result1 = expensive_function(5)
    print(f"  Result: {result1}")
    
    print("\nSecond call (cached):")
    result2 = expensive_function(5)
    print(f"  Result: {result2}")
    
    print("\nWaiting for cache to expire...")
    time.sleep(0.6)
    
    print("\nThird call (expired):")
    result3 = expensive_function(5)
    print(f"  Result: {result3}")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - API Decorator
# ============================================================

def api_endpoint(method, auth_required=True, rate_limit_calls=100):
    """
    Decorator for API endpoints with multiple features.
    
    TODO: Combine multiple decorator features
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Log request
            print(f"[API] {method} {func.__name__}")
            
            # Check auth
            if auth_required:
                auth_token = kwargs.get('auth_token')
                if not auth_token:
                    print(f"  ✗ Authentication required")
                    return {"error": "Authentication required"}
                print(f"  ✓ Authenticated")
            
            # Execute
            try:
                result = func(*args, **kwargs)
                print(f"  ✓ Success")
                return {"success": True, "data": result}
            except Exception as e:
                print(f"  ✗ Error: {e}")
                return {"success": False, "error": str(e)}
        
        return wrapper
    return decorator

def test_api_endpoint():
    """Test API endpoint decorator"""
    print("--- Exercise 7: API Endpoint Decorator ---")
    
    @api_endpoint(method="GET", auth_required=True)
    def get_user(user_id, auth_token=None):
        """Get user by ID"""
        return {"id": user_id, "name": "Alice"}
    
    @api_endpoint(method="POST", auth_required=False)
    def create_post(title, content):
        """Create a post"""
        return {"id": 123, "title": title}
    
    print("Test 1: Authenticated request")
    result1 = get_user(42, auth_token="secret")
    print(f"  Result: {result1}")
    
    print("\nTest 2: Missing authentication")
    result2 = get_user(42)
    print(f"  Result: {result2}")
    
    print("\nTest 3: No auth required")
    result3 = create_post("Hello", "World")
    print(f"  Result: {result3}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Decorator with Optional Parameters
# ============================================================

def smart_cache(func=None, *, maxsize=128, ttl=None):
    """
    Cache decorator that works with or without parameters.
    
    TODO: Support both @smart_cache and @smart_cache(maxsize=256)
    """
    def decorator(f):
        cache = {}
        
        @wraps(f)
        def wrapper(*args):
            # Check cache
            if args in cache:
                result, timestamp = cache[args]
                if ttl is None or time.time() - timestamp < ttl:
                    return result
            
            # Compute and cache
            result = f(*args)
            
            # Enforce maxsize
            if len(cache) >= maxsize:
                # Remove oldest (simple FIFO)
                cache.pop(next(iter(cache)))
            
            cache[args] = (result, time.time())
            return result
        
        return wrapper
    
    # Handle both @smart_cache and @smart_cache()
    if func is None:
        return decorator
    else:
        return decorator(func)

def test_smart_cache():
    """Test smart cache decorator"""
    print("--- Bonus Challenge: Smart Cache ---")
    
    # Without parameters
    @smart_cache
    def fib(n):
        if n <= 1:
            return n
        return fib(n-1) + fib(n-2)
    
    # With parameters
    @smart_cache(maxsize=3, ttl=1.0)
    def square(n):
        print(f"  Computing square({n})")
        return n ** 2
    
    print("Fibonacci (no params):")
    print(f"  fib(10) = {fib(10)}")
    
    print("\nSquare (with params):")
    print(f"  square(5) = {square(5)}")
    print(f"  square(5) = {square(5)}")  # Cached
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Parametrized Decorators:
    - Factory: O(1) - creates decorator
    - Decorator: O(1) - creates wrapper
    - Wrapper: O(f) where f = function time
    
    Specific Decorators:
    - retry: O(n*f) where n = attempts
    - rate_limit: O(k) where k = calls in period
    - cache: O(1) lookup, O(n) space for n cached results
    
    Benefits:
    - Configurable behavior
    - Reusable across functions
    - Clean separation of concerns
    - Declarative configuration
    
    Use Cases:
    - Retry logic with configurable attempts
    - Rate limiting with custom limits
    - Caching with TTL
    - Validation with custom rules
    - Timeouts with custom durations
    - Authentication with different levels
    
    Best Practices:
    - Use keyword-only arguments for clarity
    - Provide sensible defaults
    - Document parameters
    - Keep decorator logic simple
    - Consider performance impact
    
    Common Patterns:
    - @retry(max_attempts=3)
    - @cache(maxsize=128, ttl=3600)
    - @rate_limit(calls=100, period=60)
    - @timeout(seconds=30)
    - @validate(rules=[...])
    
    Security Considerations:
    - Validate decorator parameters
    - Be careful with caching sensitive data
    - Consider resource limits (cache size)
    - Handle edge cases (zero attempts, etc.)
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 5, Day 2: Parametrized Decorators")
    print("=" * 60)
    print()
    
    decorator_factory_pattern()
    test_retry()
    test_timeout()
    test_rate_limit()
    test_validate()
    test_cache_ttl()
    test_api_endpoint()
    test_smart_cache()
    
    print("=" * 60)
    print("✅ Day 2 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Parametrized decorators use three-level pattern")
    print("2. Factory → Decorator → Wrapper")
    print("3. Enable configurable behavior")
    print("4. Can work with or without parameters")

