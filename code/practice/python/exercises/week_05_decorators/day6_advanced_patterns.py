"""
Week 5, Day 6: Advanced Decorator Patterns

Learning Objectives:
- Master decorator chaining and composition
- Learn context-aware decorators
- Understand decorator registration patterns
- Practice plugin systems with decorators
- Build decorator utilities

Time: 10-15 minutes
"""

from functools import wraps
import time
from typing import Callable, Any

# ============================================================
# EXERCISE 1: Decorator Registry Pattern
# ============================================================

def decorator_registry():
    """
    Learn to register functions with decorators.
    
    Registry pattern: Collect decorated functions
    """
    print("--- Exercise 1: Decorator Registry Pattern ---")
    
    # Registry to store handlers
    handlers = {}
    
    def register(event_type):
        """Register handler for event type"""
        def decorator(func):
            handlers[event_type] = func
            return func
        return decorator
    
    # Register handlers
    @register('user_login')
    def handle_login(user):
        return f"User {user} logged in"
    
    @register('user_logout')
    def handle_logout(user):
        return f"User {user} logged out"
    
    @register('purchase')
    def handle_purchase(user, item):
        return f"User {user} purchased {item}"
    
    # Dispatch events
    print("Registered handlers:", list(handlers.keys()))
    
    print("\nDispatching events:")
    print(f"  {handlers['user_login']('Alice')}")
    print(f"  {handlers['purchase']('Bob', 'Widget')}")
    print(f"  {handlers['user_logout']('Alice')}")
    
    print()

# ============================================================
# EXERCISE 2: Plugin System
# ============================================================

class PluginSystem:
    """
    Plugin system using decorator registration.
    
    TODO: Implement plugin discovery and loading
    """
    
    def __init__(self):
        self.plugins = {}
    
    def register(self, name):
        """Register a plugin"""
        def decorator(func):
            self.plugins[name] = func
            print(f"  Registered plugin: {name}")
            return func
        return decorator
    
    def execute(self, name, *args, **kwargs):
        """Execute a plugin"""
        if name not in self.plugins:
            raise ValueError(f"Plugin '{name}' not found")
        return self.plugins[name](*args, **kwargs)
    
    def list_plugins(self):
        """List all registered plugins"""
        return list(self.plugins.keys())

def test_plugin_system():
    """Test plugin system"""
    print("--- Exercise 2: Plugin System ---")
    
    plugins = PluginSystem()
    
    print("Registering plugins:")
    
    @plugins.register('markdown')
    def markdown_processor(text):
        return f"<p>{text}</p>"
    
    @plugins.register('uppercase')
    def uppercase_processor(text):
        return text.upper()
    
    @plugins.register('reverse')
    def reverse_processor(text):
        return text[::-1]
    
    print(f"\nAvailable plugins: {plugins.list_plugins()}")
    
    print("\nExecuting plugins:")
    text = "hello world"
    print(f"  Original: {text}")
    print(f"  markdown: {plugins.execute('markdown', text)}")
    print(f"  uppercase: {plugins.execute('uppercase', text)}")
    print(f"  reverse: {plugins.execute('reverse', text)}")
    
    print()

# ============================================================
# EXERCISE 3: Context-Aware Decorators
# ============================================================

def context_aware_decorator():
    """
    Create decorators that adapt based on context.
    
    TODO: Implement environment-aware behavior
    """
    print("--- Exercise 3: Context-Aware Decorators ---")
    
    # Global context
    context = {'environment': 'development'}
    
    def environment_specific(prod_func, dev_func):
        """Execute different functions based on environment"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if context['environment'] == 'production':
                    return prod_func(*args, **kwargs)
                else:
                    return dev_func(*args, **kwargs)
            return wrapper
        return decorator
    
    @environment_specific(
        prod_func=lambda msg: f"[PROD] {msg}",
        dev_func=lambda msg: f"[DEV] {msg} (verbose)"
    )
    def log_message(msg):
        return msg
    
    print("Development environment:")
    print(f"  {log_message('Hello')}")
    
    context['environment'] = 'production'
    print("\nProduction environment:")
    print(f"  {log_message('Hello')}")
    
    print()

# ============================================================
# EXERCISE 4: Decorator Composition
# ============================================================

def compose_decorators(*decorators):
    """
    Compose multiple decorators into one.
    
    TODO: Create decorator combinator
    """
    def composed(func):
        for decorator in reversed(decorators):
            func = decorator(func)
        return func
    return composed

def test_decorator_composition():
    """Test decorator composition"""
    print("--- Exercise 4: Decorator Composition ---")
    
    def uppercase(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result.upper()
        return wrapper
    
    def exclaim(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"{result}!!!"
        return wrapper
    
    def quote(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f'"{result}"'
        return wrapper
    
    # Compose decorators
    enhance = compose_decorators(quote, exclaim, uppercase)
    
    @enhance
    def greet(name):
        return f"hello, {name}"
    
    print(f"greet('alice'): {greet('alice')}")
    
    print()

# ============================================================
# EXERCISE 5: Conditional Decorator
# ============================================================

def conditional_decorator(condition):
    """
    Apply decorator only if condition is True.
    
    TODO: Implement conditional decoration
    """
    def decorator(dec):
        def wrapper(func):
            if condition:
                return dec(func)
            return func
        return wrapper
    return decorator

def test_conditional_decorator():
    """Test conditional decorator"""
    print("--- Exercise 5: Conditional Decorator ---")
    
    DEBUG = True
    
    def debug(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"  [DEBUG] Calling {func.__name__}{args}")
            result = func(*args, **kwargs)
            print(f"  [DEBUG] Returned {result}")
            return result
        return wrapper
    
    @conditional_decorator(DEBUG)(debug)
    def add(a, b):
        return a + b
    
    print("With DEBUG=True:")
    result = add(3, 5)
    print(f"Result: {result}")
    
    # Without debug
    DEBUG = False
    
    @conditional_decorator(DEBUG)(debug)
    def multiply(a, b):
        return a * b
    
    print("\nWith DEBUG=False:")
    result = multiply(3, 5)
    print(f"Result: {result}")
    
    print()

# ============================================================
# EXERCISE 6: Decorator with State Machine
# ============================================================

class StatefulDecorator:
    """
    Decorator that maintains state across calls.
    
    TODO: Implement state machine decorator
    """
    
    def __init__(self, max_calls=3):
        self.max_calls = max_calls
        self.calls = 0
        self.state = 'active'
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.state == 'exhausted':
                raise RuntimeError(f"{func.__name__} has been exhausted")
            
            self.calls += 1
            
            if self.calls >= self.max_calls:
                self.state = 'exhausted'
                print(f"  [WARNING] {func.__name__} exhausted after {self.calls} calls")
            
            return func(*args, **kwargs)
        
        wrapper.reset = lambda: (setattr(self, 'calls', 0), setattr(self, 'state', 'active'))
        wrapper.get_state = lambda: {'calls': self.calls, 'state': self.state}
        
        return wrapper

def test_stateful_decorator():
    """Test stateful decorator"""
    print("--- Exercise 6: Stateful Decorator ---")
    
    @StatefulDecorator(max_calls=3)
    def limited_function():
        return "Success"
    
    print("Making calls (limit: 3):")
    for i in range(4):
        try:
            result = limited_function()
            print(f"  Call {i+1}: {result}")
        except RuntimeError as e:
            print(f"  Call {i+1}: {e}")
    
    print(f"\nState: {limited_function.get_state()}")
    
    print("\nResetting...")
    limited_function.reset()
    print(f"State after reset: {limited_function.get_state()}")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - API Rate Limiting
# ============================================================

class APIRateLimiter:
    """
    Sophisticated rate limiter with multiple strategies.
    
    TODO: Implement rate limiting with burst allowance
    """
    
    def __init__(self, calls_per_second=10, burst=5):
        self.calls_per_second = calls_per_second
        self.burst = burst
        self.tokens = burst
        self.last_update = time.time()
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Refill tokens
            now = time.time()
            elapsed = now - self.last_update
            self.tokens = min(
                self.burst,
                self.tokens + elapsed * self.calls_per_second
            )
            self.last_update = now
            
            # Check if we have tokens
            if self.tokens < 1:
                wait_time = (1 - self.tokens) / self.calls_per_second
                raise RuntimeError(
                    f"Rate limit exceeded. "
                    f"Wait {wait_time:.2f}s before retrying."
                )
            
            # Consume token
            self.tokens -= 1
            return func(*args, **kwargs)
        
        wrapper.get_tokens = lambda: self.tokens
        
        return wrapper

def test_api_rate_limiter():
    """Test API rate limiter"""
    print("--- Exercise 7: API Rate Limiter ---")
    
    @APIRateLimiter(calls_per_second=5, burst=3)
    def api_call(endpoint):
        return f"Response from {endpoint}"
    
    print("Making rapid calls (burst=3, rate=5/s):")
    for i in range(6):
        try:
            result = api_call(f"/api/endpoint{i}")
            print(f"  Call {i+1}: Success (tokens: {api_call.get_tokens():.2f})")
        except RuntimeError as e:
            print(f"  Call {i+1}: {e}")
        time.sleep(0.1)
    
    print()

# ============================================================
# BONUS CHALLENGE: Decorator Factory Factory
# ============================================================

def make_decorator_factory(wrapper_func):
    """
    Create a decorator factory from a wrapper function.
    
    TODO: Meta-decorator for creating decorators
    """
    def decorator_factory(*factory_args, **factory_kwargs):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return wrapper_func(
                    func, args, kwargs,
                    factory_args, factory_kwargs
                )
            return wrapper
        return decorator
    return decorator_factory

def test_decorator_factory_factory():
    """Test decorator factory factory"""
    print("--- Bonus Challenge: Decorator Factory Factory ---")
    
    @make_decorator_factory
    def repeat_wrapper(func, args, kwargs, factory_args, factory_kwargs):
        """Wrapper that repeats function execution"""
        times = factory_args[0] if factory_args else 1
        results = []
        for _ in range(times):
            results.append(func(*args, **kwargs))
        return results
    
    @repeat_wrapper(3)
    def greet(name):
        return f"Hello, {name}!"
    
    results = greet("Alice")
    print(f"Results: {results}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Registry Pattern:
    - Registration: O(1)
    - Lookup: O(1) with dict
    - Space: O(n) where n = registered functions
    
    Plugin System:
    - Same as registry
    - Execution: O(f) where f = plugin function time
    
    Decorator Composition:
    - Composition: O(n) where n = decorators
    - Execution: O(sum of decorator overhead)
    
    Stateful Decorators:
    - State access: O(1)
    - Space: O(1) per decorator instance
    
    Rate Limiting:
    - Token bucket: O(1) per call
    - Space: O(1)
    
    Benefits:
    - Registry: Dynamic function discovery
    - Plugins: Extensible architecture
    - Composition: Reusable decorator combinations
    - Stateful: Track behavior across calls
    
    Use Cases:
    - Registry: Event handlers, command patterns
    - Plugins: Extensible applications
    - Composition: Complex behavior from simple parts
    - Stateful: Rate limiting, quotas, caching
    
    Best Practices:
    - Keep decorators focused
    - Document decorator behavior
    - Consider decorator order
    - Handle edge cases
    - Provide introspection methods
    
    Common Patterns:
    - Registry for dynamic dispatch
    - Plugin system for extensibility
    - Composition for complex behavior
    - State machines for lifecycle management
    
    Security Considerations:
    - Validate registered functions
    - Limit plugin capabilities
    - Prevent resource exhaustion
    - Handle malicious inputs
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 5, Day 6: Advanced Decorator Patterns")
    print("=" * 60)
    print()
    
    decorator_registry()
    test_plugin_system()
    context_aware_decorator()
    test_decorator_composition()
    test_conditional_decorator()
    test_stateful_decorator()
    test_api_rate_limiter()
    test_decorator_factory_factory()
    
    print("=" * 60)
    print("✅ Day 6 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Registry pattern for dynamic function discovery")
    print("2. Plugin systems enable extensibility")
    print("3. Decorator composition builds complex behavior")
    print("4. Stateful decorators track behavior across calls")

