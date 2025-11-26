"""
Week 4, Day 4: Function Composition and Pipelines

Learning Objectives:
- Master function composition patterns
- Learn to build data pipelines
- Understand compose vs pipe
- Practice chaining transformations
- Build reusable composition utilities

Time: 10-15 minutes
"""

from functools import reduce
from typing import Callable, Any

# ============================================================
# EXERCISE 1: Basic Function Composition
# ============================================================

def composition_basics():
    """
    Learn basic function composition.
    
    compose(f, g)(x) = f(g(x))
    """
    print("--- Exercise 1: Basic Function Composition ---")
    
    # Simple functions
    def add_10(x):
        return x + 10
    
    def multiply_2(x):
        return x * 2
    
    def square(x):
        return x ** 2
    
    # Manual composition
    x = 5
    result1 = square(multiply_2(add_10(x)))
    print(f"square(multiply_2(add_10({x}))) = {result1}")
    print(f"  Steps: {x} → {add_10(x)} → {multiply_2(add_10(x))} → {result1}")
    
    # Different order
    result2 = add_10(multiply_2(square(x)))
    print(f"\nadd_10(multiply_2(square({x}))) = {result2}")
    print(f"  Steps: {x} → {square(x)} → {multiply_2(square(x))} → {result2}")
    
    print("\n💡 Composition order matters!")
    print("  f(g(x)) ≠ g(f(x)) in general")
    
    print()

# ============================================================
# EXERCISE 2: Implementing compose()
# ============================================================

def compose(*functions):
    """
    Compose functions right-to-left.
    
    compose(f, g, h)(x) = f(g(h(x)))
    """
    def inner(arg):
        result = arg
        for func in reversed(functions):
            result = func(result)
        return result
    return inner

def compose_reduce(*functions):
    """
    Compose using reduce (more functional).
    """
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def test_compose():
    """Test compose implementations"""
    print("--- Exercise 2: Implementing compose() ---")
    
    # Helper functions
    add_10 = lambda x: x + 10
    multiply_2 = lambda x: x * 2
    square = lambda x: x ** 2
    
    # Create composed function
    transform = compose(square, multiply_2, add_10)
    
    print("transform = compose(square, multiply_2, add_10)")
    print(f"transform(5) = {transform(5)}")
    print(f"  Execution: 5 → add_10 → multiply_2 → square")
    print(f"  Steps: 5 → 15 → 30 → 900")
    
    # Using reduce version
    transform_reduce = compose_reduce(square, multiply_2, add_10)
    print(f"\nUsing reduce version: {transform_reduce(5)}")
    
    # String operations
    strip = str.strip
    upper = str.upper
    reverse = lambda s: s[::-1]
    
    process_string = compose(reverse, upper, strip)
    result = process_string("  hello  ")
    print(f"\nString processing: '  hello  ' → '{result}'")
    
    print()

# ============================================================
# EXERCISE 3: Implementing pipe()
# ============================================================

def pipe(*functions):
    """
    Pipe functions left-to-right (more intuitive).
    
    pipe(f, g, h)(x) = h(g(f(x)))
    """
    def inner(arg):
        result = arg
        for func in functions:
            result = func(result)
        return result
    return inner

def test_pipe():
    """Test pipe implementation"""
    print("--- Exercise 3: Implementing pipe() ---")
    
    # Helper functions
    add_10 = lambda x: x + 10
    multiply_2 = lambda x: x * 2
    square = lambda x: x ** 2
    
    # Create pipeline (reads left-to-right)
    transform = pipe(add_10, multiply_2, square)
    
    print("transform = pipe(add_10, multiply_2, square)")
    print(f"transform(5) = {transform(5)}")
    print(f"  Execution: 5 → add_10 → multiply_2 → square")
    print(f"  Steps: 5 → 15 → 30 → 900")
    
    # Data processing pipeline
    data = [1, 2, 3, 4, 5]
    
    filter_evens = lambda lst: [x for x in lst if x % 2 == 0]
    square_all = lambda lst: [x ** 2 for x in lst]
    sum_all = sum
    
    process = pipe(filter_evens, square_all, sum_all)
    result = process(data)
    
    print(f"\nData pipeline: {data}")
    print(f"  → filter_evens → square_all → sum_all")
    print(f"  → {filter_evens(data)} → {square_all(filter_evens(data))} → {result}")
    
    print()

# ============================================================
# EXERCISE 4: Pipeline Class
# ============================================================

class Pipeline:
    """
    Fluent pipeline for chaining operations.
    
    TODO: Implement chainable pipeline
    """
    
    def __init__(self, data):
        self._data = data
    
    def map(self, func):
        """Apply function to each element"""
        self._data = [func(x) for x in self._data]
        return self
    
    def filter(self, predicate):
        """Keep elements matching predicate"""
        self._data = [x for x in self._data if predicate(x)]
        return self
    
    def reduce(self, func, initial=None):
        """Reduce to single value"""
        if initial is None:
            return reduce(func, self._data)
        return reduce(func, self._data, initial)
    
    def sort(self, key=None, reverse=False):
        """Sort elements"""
        self._data = sorted(self._data, key=key, reverse=reverse)
        return self
    
    def take(self, n):
        """Take first n elements"""
        self._data = self._data[:n]
        return self
    
    def value(self):
        """Get current value"""
        return self._data

def test_pipeline_class():
    """Test Pipeline class"""
    print("--- Exercise 4: Pipeline Class ---")
    
    # Process numbers
    result = (Pipeline([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
              .filter(lambda x: x % 2 == 0)
              .map(lambda x: x ** 2)
              .sort(reverse=True)
              .take(3)
              .value())
    
    print("Pipeline([1..10])")
    print("  .filter(even)")
    print("  .map(square)")
    print("  .sort(reverse=True)")
    print("  .take(3)")
    print(f"  Result: {result}")
    
    # Process strings
    words = ["hello", "world", "python", "programming"]
    result = (Pipeline(words)
              .filter(lambda w: len(w) > 5)
              .map(str.upper)
              .sort()
              .value())
    
    print(f"\nPipeline({words})")
    print("  .filter(len > 5)")
    print("  .map(upper)")
    print("  .sort()")
    print(f"  Result: {result}")
    
    print()

# ============================================================
# EXERCISE 5: Real-World Scenario - Data Processing
# ============================================================

def process_sales_data():
    """
    Process sales data using pipelines.
    
    TODO: Build data transformation pipeline
    """
    print("--- Exercise 5: Sales Data Processing ---")
    
    sales = [
        {'product': 'Laptop', 'price': 999, 'quantity': 2, 'discount': 0.1},
        {'product': 'Mouse', 'price': 25, 'quantity': 5, 'discount': 0.0},
        {'product': 'Keyboard', 'price': 75, 'quantity': 3, 'discount': 0.15},
        {'product': 'Monitor', 'price': 299, 'quantity': 1, 'discount': 0.05},
        {'product': 'USB Cable', 'price': 10, 'quantity': 10, 'discount': 0.0},
    ]
    
    # Pipeline functions
    def calculate_total(sale):
        """Calculate total after discount"""
        subtotal = sale['price'] * sale['quantity']
        discount_amount = subtotal * sale['discount']
        return {**sale, 'total': subtotal - discount_amount}
    
    def is_high_value(sale):
        """Check if sale is high value (>= $200)"""
        return sale['total'] >= 200
    
    def format_sale(sale):
        """Format sale for display"""
        return f"{sale['product']}: ${sale['total']:.2f}"
    
    # Build pipeline
    process = pipe(
        lambda sales: [calculate_total(s) for s in sales],
        lambda sales: [s for s in sales if is_high_value(s)],
        lambda sales: sorted(sales, key=lambda s: s['total'], reverse=True),
        lambda sales: [format_sale(s) for s in sales]
    )
    
    result = process(sales)
    
    print("High-value sales (>= $200):")
    for sale in result:
        print(f"  {sale}")
    
    # Calculate total revenue
    total_revenue = pipe(
        lambda sales: [calculate_total(s) for s in sales],
        lambda sales: sum(s['total'] for s in sales)
    )(sales)
    
    print(f"\nTotal revenue: ${total_revenue:.2f}")
    
    print()

# ============================================================
# EXERCISE 6: Composing with Decorators
# ============================================================

def trace(func):
    """Decorator to trace function calls"""
    def wrapper(arg):
        result = func(arg)
        print(f"  {func.__name__}({arg}) → {result}")
        return result
    wrapper.__name__ = func.__name__
    return wrapper

def test_traced_composition():
    """Test composition with tracing"""
    print("--- Exercise 6: Traced Composition ---")
    
    @trace
    def add_10(x):
        return x + 10
    
    @trace
    def multiply_2(x):
        return x * 2
    
    @trace
    def square(x):
        return x ** 2
    
    # Compose with tracing
    transform = pipe(add_10, multiply_2, square)
    
    print("Executing: pipe(add_10, multiply_2, square)(5)")
    result = transform(5)
    print(f"Final result: {result}")
    
    print()

# ============================================================
# EXERCISE 7: Advanced Composition Patterns
# ============================================================

def curry(func):
    """
    Curry a function (partial application).
    
    TODO: Implement currying for composition
    """
    def curried(*args):
        if len(args) >= func.__code__.co_argcount:
            return func(*args)
        return lambda *more: curried(*(args + more))
    return curried

@curry
def add(x, y):
    return x + y

@curry
def multiply(x, y):
    return x * y

def test_curried_composition():
    """Test composition with curried functions"""
    print("--- Exercise 7: Curried Composition ---")
    
    # Create specialized functions
    add_10 = add(10)
    multiply_2 = multiply(2)
    
    print(f"add_10 = add(10)")
    print(f"add_10(5) = {add_10(5)}")
    
    print(f"\nmultiply_2 = multiply(2)")
    print(f"multiply_2(5) = {multiply_2(5)}")
    
    # Compose curried functions
    transform = pipe(add_10, multiply_2)
    print(f"\ntransform = pipe(add_10, multiply_2)")
    print(f"transform(5) = {transform(5)}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Async Pipeline
# ============================================================

class AsyncPipeline:
    """
    Pipeline that can handle both sync and async operations.
    
    TODO: Implement async-aware pipeline
    """
    
    def __init__(self, data):
        self._data = data
        self._operations = []
    
    def map(self, func):
        """Add map operation"""
        self._operations.append(('map', func))
        return self
    
    def filter(self, predicate):
        """Add filter operation"""
        self._operations.append(('filter', predicate))
        return self
    
    def execute(self):
        """Execute all operations"""
        result = self._data
        for op_type, func in self._operations:
            if op_type == 'map':
                result = [func(x) for x in result]
            elif op_type == 'filter':
                result = [x for x in result if func(x)]
        return result

def test_async_pipeline():
    """Test async pipeline"""
    print("--- Bonus Challenge: Async Pipeline ---")
    
    result = (AsyncPipeline([1, 2, 3, 4, 5])
              .filter(lambda x: x % 2 == 0)
              .map(lambda x: x ** 2)
              .execute())
    
    print(f"AsyncPipeline([1, 2, 3, 4, 5])")
    print(f"  .filter(even)")
    print(f"  .map(square)")
    print(f"  .execute()")
    print(f"  Result: {result}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Function Composition:
    - compose/pipe creation: O(1)
    - Execution: O(n) where n = number of functions
    - Each function's complexity adds up
    
    Pipeline Class:
    - Each operation: Depends on operation
    - map: O(n) where n = elements
    - filter: O(n)
    - sort: O(n log n)
    - Chaining: Executes eagerly (each step processes all)
    
    Benefits:
    - Readable data transformations
    - Reusable function combinations
    - Declarative style
    - Easy to test individual functions
    - Composable and modular
    
    Drawbacks:
    - Can be harder to debug
    - May create intermediate collections
    - Performance overhead for small datasets
    - Learning curve for team
    
    Use Cases:
    - Data transformation pipelines
    - ETL processes
    - Request/response processing
    - Validation chains
    - Text processing
    
    compose vs pipe:
    - compose: Right-to-left (mathematical)
    - pipe: Left-to-right (more intuitive)
    - Choose based on team preference
    
    Best Practices:
    - Keep functions pure (no side effects)
    - Name functions descriptively
    - Test functions individually
    - Consider lazy evaluation for large datasets
    - Use type hints for clarity
    
    Performance:
    - Eager evaluation: Processes all data at each step
    - Lazy evaluation: Use generators for efficiency
    - Consider itertools for large datasets
    
    Security Considerations:
    - Validate input data
    - Be careful with user-provided functions
    - Consider resource limits
    - Handle errors at each stage
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 4, Day 4: Function Composition and Pipelines")
    print("=" * 60)
    print()
    
    composition_basics()
    test_compose()
    test_pipe()
    test_pipeline_class()
    process_sales_data()
    test_traced_composition()
    test_curried_composition()
    test_async_pipeline()
    
    print("=" * 60)
    print("✅ Day 4 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. compose: right-to-left function composition")
    print("2. pipe: left-to-right (more readable)")
    print("3. Pipelines enable declarative data transformation")
    print("4. Keep functions pure for composability")

