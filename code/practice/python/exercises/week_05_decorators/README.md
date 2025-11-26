# Week 5: Decorators

Master Python decorators for clean, reusable, and powerful code.

## Overview

This week focuses on decorators - one of Python's most powerful features. Learn to write function and class decorators, understand the descriptor protocol, and build production-ready decorator libraries.

## Daily Breakdown

### Day 1: Decorator Basics
**File:** `day1_decorator_basics.py`

Learn fundamental decorator concepts:
- What decorators are and how they work
- @decorator syntax
- functools.wraps importance
- Handling function arguments
- Decorator execution order
- Stacking multiple decorators

**Key Concepts:**
- Decorator: function that wraps another function
- @decorator is sugar for `func = decorator(func)`
- Always use @wraps to preserve metadata

---

### Day 2: Parametrized Decorators
**File:** `day2_parametrized_decorators.py`

Create configurable decorators:
- Three-level function pattern
- Decorator factories
- @retry, @timeout, @rate_limit patterns
- Validation decorators
- Cache with TTL
- Optional parameters

**Key Pattern:**
```python
def decorator_factory(params):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Use params here
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

---

### Day 3: Class-Based Decorators
**File:** `day3_class_decorators.py`

Use classes for stateful decorators:
- __call__ method for callability
- Stateful decorators (counters, timers)
- Class decorators with parameters
- Comparison with function decorators
- Descriptor protocol basics

**Benefits:**
- Maintain state across calls
- Multiple methods for state management
- More readable for complex decorators

---

### Day 4: @property and Descriptors
**File:** `day4_property_descriptors.py`

Master computed attributes and validation:
- @property for computed attributes
- Getter/setter/deleter pattern
- Descriptor protocol (__get__, __set__, __delete__)
- Validation descriptors
- Type-checked descriptors
- Lazy properties

**Use Cases:**
- Computed properties
- Attribute validation
- Type checking
- Lazy initialization

---

### Day 5: functools Decorators
**File:** `day5_functools_decorators.py`

Leverage built-in functools decorators:
- @lru_cache for memoization
- @singledispatch for function overloading
- @total_ordering for comparison methods
- @cached_property for lazy loading
- Custom implementations

**Key Tools:**
- lru_cache: Automatic memoization
- singledispatch: Type-based dispatch
- total_ordering: Generate comparisons
- cached_property: Lazy computed attributes

---

### Day 6: Advanced Decorator Patterns
**File:** `day6_advanced_patterns.py`

Build sophisticated decorator systems:
- Registry pattern for function discovery
- Plugin systems
- Decorator composition
- Context-aware decorators
- Conditional decorators
- State machines

**Patterns:**
- Registry: Collect decorated functions
- Plugins: Extensible architecture
- Composition: Combine decorators
- Stateful: Track across calls

---

### Day 7: Review & Challenge
**File:** `day7_review_challenge.py`

Apply all concepts:
- **Challenge 1:** Complete decorator library
- **Challenge 2:** API framework with decorators
- **Challenge 3:** Performance monitoring system
- **Challenge 4:** Validation framework

**Skills Practiced:**
- Combining decorator patterns
- Production-ready implementations
- Real-world applications

---

## Quick Reference

### Basic Decorator
```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Before
        result = func(*args, **kwargs)
        # After
        return result
    return wrapper

@my_decorator
def my_function():
    pass
```

### Parametrized Decorator
```python
def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet():
    print("Hello!")
```

### Class Decorator
```python
class CallCounter:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

@CallCounter
def my_function():
    pass
```

### Property
```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Too cold!")
        self._celsius = value
```

### Descriptor
```python
class Validated:
    def __init__(self, validator):
        self.validator = validator
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not self.validator(value):
            raise ValueError(f"Invalid {self.name}")
        instance.__dict__[self.name] = value

class Person:
    age = Validated(lambda x: 0 < x < 150)
```

---

## Common Decorator Patterns

### Timer
```python
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.6f}s")
        return result
    return wrapper
```

### Retry
```python
def retry(max_attempts=3, delay=0.1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator
```

### Cache
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### Validation
```python
def validate(**validators):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Validate arguments
            # ...
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate(x=lambda v: v > 0, y=lambda v: v > 0)
def divide(x, y):
    return x / y
```

---

## Best Practices

1. **Always use @wraps**
   - Preserves function metadata
   - Essential for debugging

2. **Handle *args and **kwargs**
   - Makes decorators flexible
   - Works with any function signature

3. **Keep decorators focused**
   - Single responsibility
   - Easy to understand and test

4. **Document decorator behavior**
   - What it does
   - Parameters
   - Side effects

5. **Consider performance**
   - Minimize overhead
   - Use caching when appropriate

6. **Provide introspection**
   - Methods to inspect state
   - Cache info, statistics, etc.

---

## When to Use Each Type

| Type | Use When |
|------|----------|
| **Function** | Simple, stateless decoration |
| **Parametrized** | Need configuration |
| **Class** | Need state, multiple methods |
| **@property** | Computed attributes |
| **Descriptor** | Reusable attribute logic |

---

## Learning Outcomes

After completing Week 5, you should be able to:

✅ Write basic and parametrized decorators  
✅ Create class-based decorators  
✅ Use @property for computed attributes  
✅ Implement custom descriptors  
✅ Leverage functools decorators  
✅ Build decorator registries and plugins  
✅ Compose decorators effectively  
✅ Apply decorators to real-world problems  

---

## Running the Exercises

```bash
# Run individual days
python day1_decorator_basics.py
python day2_parametrized_decorators.py
python day3_class_decorators.py
python day4_property_descriptors.py
python day5_functools_decorators.py
python day6_advanced_patterns.py
python day7_review_challenge.py

# Run all
for day in day*.py; do python "$day"; done
```

---

## Additional Resources

**Official Documentation:**
- [Decorators](https://docs.python.org/3/glossary.html#term-decorator)
- [functools module](https://docs.python.org/3/library/functools.html)
- [Descriptor HowTo](https://docs.python.org/3/howto/descriptor.html)

**Further Reading:**
- [Python Decorators](https://realpython.com/primer-on-python-decorators/)
- [Descriptor Guide](https://docs.python.org/3/howto/descriptor.html)

---

## Next Steps

🎯 **Week 6:** Sorting & Searching  
Learn efficient algorithms for sorting and searching data.

---

## Notes

- Decorators are powerful but can be overused
- Keep them simple and focused
- Document behavior clearly
- Consider performance impact
- Test decorators thoroughly

**Time Investment:** ~10-15 minutes per day, 15-20 minutes for Day 7  
**Total:** ~90 minutes for the week

---

*Happy decorating! 🐍*

