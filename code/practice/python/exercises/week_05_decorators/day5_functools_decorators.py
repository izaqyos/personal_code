"""
Week 5, Day 5: functools Decorators (lru_cache, singledispatch, etc.)

Learning Objectives:
- Master functools.lru_cache for memoization
- Learn functools.singledispatch for function overloading
- Understand functools.total_ordering
- Practice functools.cached_property
- Use built-in functools decorators effectively

Time: 10-15 minutes
"""

from functools import lru_cache, singledispatch, total_ordering, cached_property, wraps
import time

# ============================================================
# EXERCISE 1: lru_cache Basics
# ============================================================

def lru_cache_basics():
    """
    Learn functools.lru_cache for memoization.
    
    lru_cache: Least Recently Used cache decorator
    """
    print("--- Exercise 1: lru_cache Basics ---")
    
    @lru_cache(maxsize=128)
    def fibonacci(n):
        """Calculate fibonacci number"""
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    print("Computing fibonacci(10):")
    start = time.perf_counter()
    result = fibonacci(10)
    elapsed = time.perf_counter() - start
    print(f"  Result: {result}")
    print(f"  Time: {elapsed:.6f}s")
    
    print("\nComputing again (cached):")
    start = time.perf_counter()
    result = fibonacci(10)
    elapsed = time.perf_counter() - start
    print(f"  Result: {result}")
    print(f"  Time: {elapsed:.6f}s")
    
    # Cache info
    info = fibonacci.cache_info()
    print(f"\nCache info:")
    print(f"  Hits: {info.hits}")
    print(f"  Misses: {info.misses}")
    print(f"  Size: {info.currsize}/{info.maxsize}")
    
    print()

# ============================================================
# EXERCISE 2: lru_cache with maxsize
# ============================================================

def lru_cache_maxsize():
    """
    Understand maxsize parameter.
    
    TODO: Test cache eviction with small maxsize
    """
    print("--- Exercise 2: lru_cache with maxsize ---")
    
    @lru_cache(maxsize=3)
    def expensive_function(n):
        """Simulate expensive computation"""
        print(f"  Computing for n={n}")
        time.sleep(0.05)
        return n ** 2
    
    print("Making calls (maxsize=3):")
    for i in range(5):
        result = expensive_function(i)
        print(f"  f({i}) = {result}")
    
    print("\nRepeating some calls:")
    for i in [0, 1, 4]:  # 0,1 evicted, 4 cached
        result = expensive_function(i)
        print(f"  f({i}) = {result}")
    
    info = expensive_function.cache_info()
    print(f"\nCache info: hits={info.hits}, misses={info.misses}")
    
    # Clear cache
    expensive_function.cache_clear()
    print("Cache cleared")
    
    print()

# ============================================================
# EXERCISE 3: singledispatch for Function Overloading
# ============================================================

def singledispatch_basics():
    """
    Learn functools.singledispatch for type-based dispatch.
    
    singledispatch: Function overloading based on first argument type
    """
    print("--- Exercise 3: singledispatch Basics ---")
    
    @singledispatch
    def process(data):
        """Default implementation"""
        print(f"  Processing unknown type: {type(data).__name__}")
        return str(data)
    
    @process.register(int)
    def _(data):
        """Process integer"""
        print(f"  Processing int: {data}")
        return data * 2
    
    @process.register(str)
    def _(data):
        """Process string"""
        print(f"  Processing str: {data}")
        return data.upper()
    
    @process.register(list)
    def _(data):
        """Process list"""
        print(f"  Processing list: {data}")
        return [x * 2 for x in data]
    
    # Test different types
    print("Testing singledispatch:")
    print(f"  Result: {process(5)}")
    print(f"  Result: {process('hello')}")
    print(f"  Result: {process([1, 2, 3])}")
    print(f"  Result: {process(3.14)}")
    
    print()

# ============================================================
# EXERCISE 4: singledispatch with Classes
# ============================================================

def singledispatch_classes():
    """
    Use singledispatch with custom classes.
    
    TODO: Implement type-specific formatting
    """
    print("--- Exercise 4: singledispatch with Classes ---")
    
    class User:
        def __init__(self, name, email):
            self.name = name
            self.email = email
    
    class Product:
        def __init__(self, name, price):
            self.name = name
            self.price = price
    
    @singledispatch
    def format_item(item):
        """Default formatter"""
        return str(item)
    
    @format_item.register(User)
    def _(user):
        """Format user"""
        return f"User({user.name}, {user.email})"
    
    @format_item.register(Product)
    def _(product):
        """Format product"""
        return f"Product({product.name}, ${product.price:.2f})"
    
    @format_item.register(dict)
    def _(data):
        """Format dictionary"""
        items = [f"{k}={v}" for k, v in data.items()]
        return f"Dict({', '.join(items)})"
    
    # Test formatting
    user = User("Alice", "alice@example.com")
    product = Product("Widget", 19.99)
    data = {"x": 10, "y": 20}
    
    print("Formatted outputs:")
    print(f"  {format_item(user)}")
    print(f"  {format_item(product)}")
    print(f"  {format_item(data)}")
    
    print()

# ============================================================
# EXERCISE 5: total_ordering for Comparison Methods
# ============================================================

def total_ordering_example():
    """
    Use functools.total_ordering to generate comparison methods.
    
    total_ordering: Generates missing comparison methods
    """
    print("--- Exercise 5: total_ordering ---")
    
    @total_ordering
    class Version:
        """Version number with comparison"""
        
        def __init__(self, major, minor, patch):
            self.major = major
            self.minor = minor
            self.patch = patch
        
        def __eq__(self, other):
            """Equal comparison"""
            if not isinstance(other, Version):
                return NotImplemented
            return (self.major, self.minor, self.patch) == \
                   (other.major, other.minor, other.patch)
        
        def __lt__(self, other):
            """Less than comparison"""
            if not isinstance(other, Version):
                return NotImplemented
            return (self.major, self.minor, self.patch) < \
                   (other.major, other.minor, other.patch)
        
        def __repr__(self):
            return f"Version({self.major}.{self.minor}.{self.patch})"
    
    # Test comparisons
    v1 = Version(1, 0, 0)
    v2 = Version(1, 2, 0)
    v3 = Version(2, 0, 0)
    
    print(f"{v1} < {v2}: {v1 < v2}")
    print(f"{v2} < {v3}: {v2 < v3}")
    print(f"{v1} <= {v2}: {v1 <= v2}")
    print(f"{v3} > {v2}: {v3 > v2}")
    print(f"{v3} >= {v2}: {v3 >= v2}")
    print(f"{v1} == {v1}: {v1 == v1}")
    print(f"{v1} != {v2}: {v1 != v2}")
    
    # Sorting
    versions = [v3, v1, v2]
    sorted_versions = sorted(versions)
    print(f"\nSorted: {sorted_versions}")
    
    print()

# ============================================================
# EXERCISE 6: cached_property for Lazy Loading
# ============================================================

def cached_property_example():
    """
    Use functools.cached_property for lazy-loaded attributes.
    
    cached_property: Property that caches its value
    """
    print("--- Exercise 6: cached_property ---")
    
    class DataAnalyzer:
        def __init__(self, data):
            self.data = data
        
        @cached_property
        def mean(self):
            """Calculate mean (cached)"""
            print("  Computing mean...")
            time.sleep(0.1)
            return sum(self.data) / len(self.data)
        
        @cached_property
        def variance(self):
            """Calculate variance (cached)"""
            print("  Computing variance...")
            time.sleep(0.1)
            mean = self.mean
            return sum((x - mean) ** 2 for x in self.data) / len(self.data)
        
        @cached_property
        def std_dev(self):
            """Calculate standard deviation (cached)"""
            print("  Computing std_dev...")
            time.sleep(0.1)
            return self.variance ** 0.5
    
    analyzer = DataAnalyzer([1, 2, 3, 4, 5])
    
    print("First access to mean:")
    print(f"  Mean: {analyzer.mean}")
    
    print("\nSecond access (cached):")
    print(f"  Mean: {analyzer.mean}")
    
    print("\nAccessing std_dev (uses cached mean):")
    print(f"  Std Dev: {analyzer.std_dev:.2f}")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - API Client
# ============================================================

def api_client_example():
    """
    Build API client using functools decorators.
    
    TODO: Combine lru_cache and singledispatch
    """
    print("--- Exercise 7: API Client with functools ---")
    
    class APIClient:
        @lru_cache(maxsize=100)
        def get(self, endpoint):
            """Get data from API (cached)"""
            print(f"  Fetching {endpoint}...")
            time.sleep(0.1)
            return {"endpoint": endpoint, "data": "..."}
        
        @singledispatch
        @staticmethod
        def serialize(data):
            """Serialize data (default)"""
            return str(data)
        
        @serialize.register(dict)
        @staticmethod
        def _(data):
            """Serialize dictionary"""
            import json
            return json.dumps(data)
        
        @serialize.register(list)
        @staticmethod
        def _(data):
            """Serialize list"""
            return ','.join(str(x) for x in data)
    
    client = APIClient()
    
    print("First request:")
    result1 = client.get("/users")
    print(f"  {result1}")
    
    print("\nSecond request (cached):")
    result2 = client.get("/users")
    print(f"  {result2}")
    
    print("\nSerialization:")
    print(f"  Dict: {client.serialize({'x': 1, 'y': 2})}")
    print(f"  List: {client.serialize([1, 2, 3])}")
    print(f"  Other: {client.serialize(42)}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Custom lru_cache
# ============================================================

def custom_lru_cache(maxsize=128):
    """
    Implement simplified lru_cache.
    
    TODO: Build basic LRU cache decorator
    """
    def decorator(func):
        from collections import OrderedDict
        cache = OrderedDict()
        
        @wraps(func)
        def wrapper(*args):
            if args in cache:
                # Move to end (most recent)
                cache.move_to_end(args)
                wrapper.hits += 1
                return cache[args]
            
            # Compute and cache
            result = func(*args)
            wrapper.misses += 1
            
            if len(cache) >= maxsize:
                # Remove least recently used
                cache.popitem(last=False)
            
            cache[args] = result
            return result
        
        wrapper.hits = 0
        wrapper.misses = 0
        wrapper.cache = cache
        wrapper.cache_clear = lambda: cache.clear()
        wrapper.cache_info = lambda: f"hits={wrapper.hits}, misses={wrapper.misses}, size={len(cache)}"
        
        return wrapper
    return decorator

def test_custom_lru_cache():
    """Test custom LRU cache"""
    print("--- Bonus Challenge: Custom lru_cache ---")
    
    @custom_lru_cache(maxsize=3)
    def square(n):
        print(f"  Computing square({n})")
        return n ** 2
    
    print("Making calls:")
    for i in range(5):
        result = square(i)
        print(f"  square({i}) = {result}")
    
    print("\nRepeating calls:")
    for i in [0, 2, 4]:
        result = square(i)
        print(f"  square({i}) = {result}")
    
    print(f"\nCache info: {square.cache_info()}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    lru_cache:
    - Cache hit: O(1)
    - Cache miss: O(f) where f = function time
    - Space: O(maxsize)
    - Eviction: O(1) with OrderedDict
    
    singledispatch:
    - Dispatch: O(1) lookup
    - Registration: O(1)
    - Space: O(n) where n = registered types
    
    total_ordering:
    - No runtime overhead
    - Generates methods at class definition time
    
    cached_property:
    - First access: O(f) where f = property computation
    - Subsequent: O(1)
    - Space: O(1) per property
    
    Benefits:
    - lru_cache: Automatic memoization
    - singledispatch: Type-based polymorphism
    - total_ordering: Less boilerplate
    - cached_property: Lazy loading
    
    Use Cases:
    - lru_cache: Expensive pure functions
    - singledispatch: Type-specific behavior
    - total_ordering: Comparable classes
    - cached_property: Expensive computed attributes
    
    Best Practices:
    - lru_cache: Use for pure functions only
    - singledispatch: Register all needed types
    - total_ordering: Implement __eq__ and one comparison
    - cached_property: For expensive, immutable computations
    
    Common Patterns:
    - @lru_cache(maxsize=None) - unlimited cache
    - @lru_cache(maxsize=128) - default size
    - @singledispatch for polymorphism
    - @total_ordering for sortable classes
    
    Security Considerations:
    - lru_cache: Can cause memory issues with large maxsize
    - Don't cache sensitive data
    - Be careful with mutable arguments
    - Consider cache invalidation needs
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 5, Day 5: functools Decorators")
    print("=" * 60)
    print()
    
    lru_cache_basics()
    lru_cache_maxsize()
    singledispatch_basics()
    singledispatch_classes()
    total_ordering_example()
    cached_property_example()
    api_client_example()
    test_custom_lru_cache()
    
    print("=" * 60)
    print("✅ Day 5 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. lru_cache: Automatic memoization")
    print("2. singledispatch: Type-based function overloading")
    print("3. total_ordering: Generate comparison methods")
    print("4. cached_property: Lazy-loaded properties")

