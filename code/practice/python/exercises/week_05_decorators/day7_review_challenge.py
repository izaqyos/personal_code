"""
Week 5, Day 7: Review & Challenge - Build a Complete Decorator Library

Learning Objectives:
- Review all Week 5 concepts
- Build comprehensive decorator library
- Apply decorators to real-world scenarios
- Practice combining multiple decorator patterns
- Create production-ready decorators

Challenge: Build a decorator library with timing, caching, validation, and more

Time: 15-20 minutes
"""

from functools import wraps, lru_cache
from collections import OrderedDict
import time
from typing import Callable, Any

# ============================================================
# REVIEW: Week 5 Concepts
# ============================================================

def week5_review():
    """
    Quick review of all Week 5 concepts.
    """
    print("=" * 60)
    print("WEEK 5 REVIEW")
    print("=" * 60)
    
    print("\nDay 1: Decorator Basics")
    print("  • @decorator syntax")
    print("  • functools.wraps")
    print("  • Decorator execution order")
    
    print("\nDay 2: Parametrized Decorators")
    print("  • Three-level pattern")
    print("  • Configurable decorators")
    print("  • @retry, @timeout, @rate_limit")
    
    print("\nDay 3: Class-Based Decorators")
    print("  • __call__ method")
    print("  • Stateful decorators")
    print("  • Class vs function decorators")
    
    print("\nDay 4: @property and Descriptors")
    print("  • @property for computed attributes")
    print("  • Descriptor protocol")
    print("  • Validation descriptors")
    
    print("\nDay 5: functools Decorators")
    print("  • @lru_cache for memoization")
    print("  • @singledispatch for overloading")
    print("  • @total_ordering, @cached_property")
    
    print("\nDay 6: Advanced Patterns")
    print("  • Registry pattern")
    print("  • Plugin systems")
    print("  • Decorator composition")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# CHALLENGE 1: Complete Decorator Library
# ============================================================

class DecoratorLibrary:
    """
    Comprehensive decorator library.
    
    TODO: Implement production-ready decorators
    """
    
    @staticmethod
    def timer(func=None, *, label=None):
        """Time function execution"""
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = f(*args, **kwargs)
                elapsed = time.perf_counter() - start
                name = label or f.__name__
                print(f"[TIMER] {name} took {elapsed:.6f}s")
                return result
            return wrapper
        
        if func is None:
            return decorator
        return decorator(func)
    
    @staticmethod
    def retry(max_attempts=3, delay=0.1, exceptions=(Exception,)):
        """Retry on failure"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(1, max_attempts + 1):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        if attempt == max_attempts:
                            raise
                        print(f"[RETRY] Attempt {attempt} failed: {e}. Retrying...")
                        time.sleep(delay)
            return wrapper
        return decorator
    
    @staticmethod
    def cache(maxsize=128, ttl=None):
        """Cache with optional TTL"""
        def decorator(func):
            cache = OrderedDict()
            
            @wraps(func)
            def wrapper(*args):
                now = time.time()
                
                # Check cache
                if args in cache:
                    result, timestamp = cache[args]
                    if ttl is None or now - timestamp < ttl:
                        return result
                
                # Compute and cache
                result = func(*args)
                
                if len(cache) >= maxsize:
                    cache.popitem(last=False)
                
                cache[args] = (result, now)
                return result
            
            wrapper.cache_clear = lambda: cache.clear()
            return wrapper
        return decorator
    
    @staticmethod
    def validate(**validators):
        """Validate function arguments"""
        def decorator(func):
            import inspect
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                sig = inspect.signature(func)
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()
                
                for param_name, value in bound.arguments.items():
                    if param_name in validators:
                        validator = validators[param_name]
                        if not validator(value):
                            raise ValueError(
                                f"Validation failed for {param_name}={value!r}"
                            )
                
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    @staticmethod
    def rate_limit(calls=10, period=1.0):
        """Rate limit function calls"""
        def decorator(func):
            calls_list = []
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                now = time.time()
                
                # Remove old calls
                while calls_list and calls_list[0] < now - period:
                    calls_list.pop(0)
                
                # Check limit
                if len(calls_list) >= calls:
                    wait = period - (now - calls_list[0])
                    raise RuntimeError(f"Rate limit exceeded. Wait {wait:.2f}s")
                
                calls_list.append(now)
                return func(*args, **kwargs)
            
            return wrapper
        return decorator

def test_decorator_library():
    """Test decorator library"""
    print("--- Challenge 1: Decorator Library ---")
    
    lib = DecoratorLibrary()
    
    @lib.timer
    @lib.cache(maxsize=10)
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    @lib.validate(x=lambda v: v > 0, y=lambda v: v > 0)
    def divide(x, y):
        return x / y
    
    print("Testing fibonacci with timer and cache:")
    result = fibonacci(10)
    print(f"  Result: {result}")
    
    print("\nTesting validation:")
    try:
        divide(10, 2)
        print(f"  divide(10, 2) = {divide(10, 2)}")
    except ValueError as e:
        print(f"  Error: {e}")
    
    try:
        divide(10, -1)
    except ValueError as e:
        print(f"  divide(10, -1) → {e}")
    
    print()

# ============================================================
# CHALLENGE 2: API Framework with Decorators
# ============================================================

class APIFramework:
    """
    Simple API framework using decorators.
    
    TODO: Build REST API framework
    """
    
    def __init__(self):
        self.routes = {}
        self.middleware = []
    
    def route(self, path, methods=None):
        """Register route"""
        if methods is None:
            methods = ['GET']
        
        def decorator(func):
            self.routes[path] = {
                'handler': func,
                'methods': methods
            }
            return func
        return decorator
    
    def use_middleware(self, func):
        """Add middleware"""
        self.middleware.append(func)
        return func
    
    def handle_request(self, path, method='GET', **kwargs):
        """Handle HTTP request"""
        if path not in self.routes:
            return {'error': 'Not Found', 'status': 404}
        
        route = self.routes[path]
        if method not in route['methods']:
            return {'error': 'Method Not Allowed', 'status': 405}
        
        # Apply middleware
        for mw in self.middleware:
            result = mw(path, method, kwargs)
            if result is not None:
                return result
        
        # Call handler
        try:
            result = route['handler'](**kwargs)
            return {'data': result, 'status': 200}
        except Exception as e:
            return {'error': str(e), 'status': 500}

def test_api_framework():
    """Test API framework"""
    print("--- Challenge 2: API Framework ---")
    
    app = APIFramework()
    
    @app.use_middleware
    def auth_middleware(path, method, kwargs):
        """Check authentication"""
        if 'auth_token' not in kwargs:
            print(f"  [MIDDLEWARE] No auth token for {path}")
            return {'error': 'Unauthorized', 'status': 401}
        print(f"  [MIDDLEWARE] Authenticated for {path}")
        return None
    
    @app.route('/users', methods=['GET'])
    def get_users():
        return [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
    
    @app.route('/users/<id>', methods=['GET'])
    def get_user(id):
        return {'id': id, 'name': f'User{id}'}
    
    print("Testing API:")
    
    print("\n1. Without auth:")
    response = app.handle_request('/users', 'GET')
    print(f"  {response}")
    
    print("\n2. With auth:")
    response = app.handle_request('/users', 'GET', auth_token='secret')
    print(f"  {response}")
    
    print()

# ============================================================
# CHALLENGE 3: Performance Monitoring System
# ============================================================

class PerformanceMonitor:
    """
    Monitor function performance.
    
    TODO: Track timing, calls, errors
    """
    
    def __init__(self):
        self.stats = {}
    
    def monitor(self, func):
        """Monitor function performance"""
        name = func.__name__
        self.stats[name] = {
            'calls': 0,
            'total_time': 0,
            'errors': 0,
            'min_time': float('inf'),
            'max_time': 0
        }
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            
            try:
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start
                
                # Update stats
                stats = self.stats[name]
                stats['calls'] += 1
                stats['total_time'] += elapsed
                stats['min_time'] = min(stats['min_time'], elapsed)
                stats['max_time'] = max(stats['max_time'], elapsed)
                
                return result
            
            except Exception as e:
                self.stats[name]['errors'] += 1
                raise
        
        return wrapper
    
    def report(self):
        """Generate performance report"""
        print("\nPerformance Report:")
        print("=" * 60)
        
        for name, stats in self.stats.items():
            if stats['calls'] == 0:
                continue
            
            avg_time = stats['total_time'] / stats['calls']
            
            print(f"\n{name}:")
            print(f"  Calls: {stats['calls']}")
            print(f"  Total time: {stats['total_time']:.6f}s")
            print(f"  Average: {avg_time:.6f}s")
            print(f"  Min: {stats['min_time']:.6f}s")
            print(f"  Max: {stats['max_time']:.6f}s")
            print(f"  Errors: {stats['errors']}")

def test_performance_monitor():
    """Test performance monitor"""
    print("--- Challenge 3: Performance Monitor ---")
    
    monitor = PerformanceMonitor()
    
    @monitor.monitor
    def fast_function():
        time.sleep(0.01)
        return "fast"
    
    @monitor.monitor
    def slow_function():
        time.sleep(0.05)
        return "slow"
    
    print("Making monitored calls:")
    for _ in range(3):
        fast_function()
    for _ in range(2):
        slow_function()
    
    monitor.report()
    
    print()

# ============================================================
# CHALLENGE 4: Validation Framework
# ============================================================

class ValidationFramework:
    """
    Comprehensive validation framework.
    
    TODO: Build reusable validators
    """
    
    @staticmethod
    def is_type(expected_type):
        """Type validator"""
        return lambda v: isinstance(v, expected_type)
    
    @staticmethod
    def in_range(min_val, max_val):
        """Range validator"""
        return lambda v: min_val <= v <= max_val
    
    @staticmethod
    def matches_pattern(pattern):
        """Regex validator"""
        import re
        regex = re.compile(pattern)
        return lambda v: regex.match(str(v)) is not None
    
    @staticmethod
    def min_length(length):
        """Minimum length validator"""
        return lambda v: len(v) >= length
    
    @staticmethod
    def validate(**rules):
        """Validate decorator"""
        def decorator(func):
            import inspect
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                sig = inspect.signature(func)
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()
                
                for param, value in bound.arguments.items():
                    if param in rules:
                        validators = rules[param]
                        if not isinstance(validators, list):
                            validators = [validators]
                        
                        for validator in validators:
                            if not validator(value):
                                raise ValueError(
                                    f"Validation failed for {param}={value!r}"
                                )
                
                return func(*args, **kwargs)
            return wrapper
        return decorator

def test_validation_framework():
    """Test validation framework"""
    print("--- Challenge 4: Validation Framework ---")
    
    val = ValidationFramework()
    
    @val.validate(
        username=[val.is_type(str), val.min_length(3)],
        age=[val.is_type(int), val.in_range(0, 150)],
        email=[val.is_type(str), val.matches_pattern(r'^[\w\.-]+@[\w\.-]+\.\w+$')]
    )
    def create_user(username, age, email):
        return {'username': username, 'age': age, 'email': email}
    
    print("Valid user:")
    user = create_user('alice', 30, 'alice@example.com')
    print(f"  {user}")
    
    print("\nInvalid users:")
    test_cases = [
        ('ab', 30, 'alice@example.com', 'username too short'),
        ('alice', 200, 'alice@example.com', 'age out of range'),
        ('alice', 30, 'invalid-email', 'invalid email'),
    ]
    
    for username, age, email, reason in test_cases:
        try:
            create_user(username, age, email)
        except ValueError as e:
            print(f"  {reason}: {e}")
    
    print()

# ============================================================
# SELF-ASSESSMENT
# ============================================================

def self_assessment():
    """
    Self-assessment checklist for Week 5.
    """
    print("=" * 60)
    print("WEEK 5 SELF-ASSESSMENT")
    print("=" * 60)
    
    checklist = [
        ("Basic decorators", "Can you write simple decorators with @wraps?"),
        ("Parametrized decorators", "Can you create decorators that accept parameters?"),
        ("Class decorators", "Can you implement decorators using classes?"),
        ("@property", "Can you create computed attributes?"),
        ("Descriptors", "Do you understand the descriptor protocol?"),
        ("functools", "Can you use lru_cache, singledispatch, etc.?"),
        ("Advanced patterns", "Can you build plugin systems and registries?"),
    ]
    
    print("\nRate yourself (1-5) on these concepts:\n")
    for i, (topic, question) in enumerate(checklist, 1):
        print(f"{i}. {topic}")
        print(f"   {question}")
        print()
    
    print("=" * 60)
    print()

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 5, Day 7: Review & Challenge")
    print("=" * 60)
    print()
    
    week5_review()
    
    print("\n" + "=" * 60)
    print("CHALLENGES")
    print("=" * 60 + "\n")
    
    test_decorator_library()
    test_api_framework()
    test_performance_monitor()
    test_validation_framework()
    
    self_assessment()
    
    print("=" * 60)
    print("✅ Week 5 Complete!")
    print("=" * 60)
    print("\n🎉 Congratulations! You've mastered decorators!")
    print("\n📚 Next: Week 6 - Sorting & Searching")
    print("\n💡 Keep using decorators for clean, maintainable code!")

