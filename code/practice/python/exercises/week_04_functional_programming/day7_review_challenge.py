"""
Week 4, Day 7: Review & Challenge - Functional Data Pipeline

Learning Objectives:
- Review all Week 4 concepts
- Build complete functional data pipeline
- Apply map, filter, reduce, compose, higher-order functions
- Use itertools for efficiency
- Practice real-world functional programming

Challenge: Build a functional ETL (Extract, Transform, Load) pipeline

Time: 15-20 minutes
"""

from functools import reduce, partial, wraps
from collections import Counter, defaultdict
from typing import Callable, Any, List, Dict
import itertools
import time

# ============================================================
# REVIEW: Week 4 Concepts
# ============================================================

def week4_review():
    """
    Quick review of all Week 4 concepts.
    """
    print("=" * 60)
    print("WEEK 4 REVIEW")
    print("=" * 60)
    
    print("\nDay 1: map, filter, reduce")
    print("  • map: transform elements")
    print("  • filter: select elements")
    print("  • reduce: accumulate values")
    
    print("\nDay 2: Lambda Functions")
    print("  • Anonymous functions")
    print("  • Use for simple operations")
    print("  • operator module alternatives")
    
    print("\nDay 3: functools.partial")
    print("  • Freeze function arguments")
    print("  • Create specialized functions")
    print("  • Better than lambda for simple cases")
    
    print("\nDay 4: Function Composition")
    print("  • compose: f(g(x))")
    print("  • pipe: left-to-right composition")
    print("  • Build data pipelines")
    
    print("\nDay 5: Higher-Order Functions")
    print("  • Functions as arguments/return values")
    print("  • Closures and scope")
    print("  • Decorators")
    
    print("\nDay 6: itertools")
    print("  • Infinite iterators: count, cycle, repeat")
    print("  • Combinatorics: product, permutations, combinations")
    print("  • groupby for aggregation")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# CHALLENGE 1: Functional Data Transformation Pipeline
# ============================================================

def pipe(*functions):
    """Pipe functions left-to-right"""
    def inner(arg):
        result = arg
        for func in functions:
            result = func(result)
        return result
    return inner

def challenge_data_pipeline():
    """
    Build functional ETL pipeline for sales data.
    
    TODO: Extract, Transform, Load using functional approach
    """
    print("--- Challenge 1: ETL Pipeline ---")
    
    # Raw data (Extract)
    raw_data = [
        "2024-01-01,Laptop,999.99,2",
        "2024-01-01,Mouse,25.00,5",
        "2024-01-02,Keyboard,75.00,3",
        "2024-01-02,Monitor,299.99,1",
        "2024-01-03,Laptop,999.99,1",
        "2024-01-03,Mouse,25.00,10",
    ]
    
    # Transform functions
    def parse_line(line):
        """Parse CSV line"""
        date, product, price, quantity = line.split(',')
        return {
            'date': date,
            'product': product,
            'price': float(price),
            'quantity': int(quantity)
        }
    
    def calculate_total(record):
        """Add total field"""
        return {**record, 'total': record['price'] * record['quantity']}
    
    def is_high_value(record):
        """Filter high-value sales (>= $200)"""
        return record['total'] >= 200
    
    def format_record(record):
        """Format for display"""
        return f"{record['date']} | {record['product']:10} | ${record['total']:8.2f}"
    
    # Build pipeline
    transform = pipe(
        lambda data: map(parse_line, data),
        lambda data: map(calculate_total, data),
        lambda data: filter(is_high_value, data),
        lambda data: sorted(data, key=lambda r: r['total'], reverse=True),
        lambda data: map(format_record, data),
        list
    )
    
    # Execute pipeline
    result = transform(raw_data)
    
    print("High-value sales (>= $200):")
    for line in result:
        print(f"  {line}")
    
    print()

# ============================================================
# CHALLENGE 2: Functional Aggregation
# ============================================================

def challenge_aggregation():
    """
    Aggregate data using functional programming.
    
    TODO: Calculate statistics functionally
    """
    print("--- Challenge 2: Functional Aggregation ---")
    
    sales = [
        {'product': 'Laptop', 'category': 'Electronics', 'amount': 1999.98},
        {'product': 'Mouse', 'category': 'Electronics', 'amount': 125.00},
        {'product': 'Desk', 'category': 'Furniture', 'amount': 299.99},
        {'product': 'Chair', 'category': 'Furniture', 'amount': 199.99},
        {'product': 'Keyboard', 'category': 'Electronics', 'amount': 225.00},
    ]
    
    # Group by category
    by_category = defaultdict(list)
    for sale in sales:
        by_category[sale['category']].append(sale['amount'])
    
    # Calculate statistics per category
    def calculate_stats(amounts):
        """Calculate statistics for amounts"""
        return {
            'count': len(amounts),
            'total': sum(amounts),
            'average': sum(amounts) / len(amounts),
            'min': min(amounts),
            'max': max(amounts)
        }
    
    stats = {
        category: calculate_stats(amounts)
        for category, amounts in by_category.items()
    }
    
    print("Sales statistics by category:")
    for category, stat in stats.items():
        print(f"\n{category}:")
        print(f"  Count: {stat['count']}")
        print(f"  Total: ${stat['total']:.2f}")
        print(f"  Average: ${stat['average']:.2f}")
        print(f"  Range: ${stat['min']:.2f} - ${stat['max']:.2f}")
    
    print()

# ============================================================
# CHALLENGE 3: Function Composition with Validation
# ============================================================

def challenge_validation():
    """
    Build validation pipeline using composition.
    
    TODO: Create composable validators
    """
    print("--- Challenge 3: Validation Pipeline ---")
    
    def validator(name, predicate, error_msg):
        """Create named validator"""
        def validate(value):
            if not predicate(value):
                raise ValueError(f"{name}: {error_msg}")
            return value
        validate.__name__ = name
        return validate
    
    # Create validators
    not_empty = validator(
        "not_empty",
        lambda s: len(s) > 0,
        "Value cannot be empty"
    )
    
    is_email = validator(
        "is_email",
        lambda s: '@' in s and '.' in s.split('@')[1],
        "Invalid email format"
    )
    
    min_length = lambda n: validator(
        f"min_length_{n}",
        lambda s: len(s) >= n,
        f"Must be at least {n} characters"
    )
    
    # Compose validators
    def compose_validators(*validators):
        """Compose multiple validators"""
        def validate(value):
            for validator_func in validators:
                try:
                    value = validator_func(value)
                except ValueError as e:
                    return False, str(e)
            return True, value
        return validate
    
    # Test data
    email_validator = compose_validators(not_empty, min_length(5), is_email)
    
    test_emails = [
        "user@example.com",
        "invalid",
        "",
        "a@b.c",
        "valid.email@domain.com"
    ]
    
    print("Email validation:")
    for email in test_emails:
        valid, result = email_validator(email)
        status = "✓" if valid else "✗"
        print(f"  {status} '{email}': {result if not valid else 'Valid'}")
    
    print()

# ============================================================
# CHALLENGE 4: Memoization and Performance
# ============================================================

def challenge_memoization():
    """
    Implement memoization for performance.
    
    TODO: Cache expensive computations
    """
    print("--- Challenge 4: Memoization ---")
    
    def memoize(func):
        """Memoization decorator"""
        cache = {}
        
        @wraps(func)
        def wrapper(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]
        
        wrapper.cache = cache
        wrapper.cache_info = lambda: {
            'hits': len(cache),
            'size': len(cache)
        }
        return wrapper
    
    @memoize
    def expensive_computation(n):
        """Simulate expensive computation"""
        time.sleep(0.01)  # Simulate work
        return n ** 2
    
    # Test memoization
    print("Computing squares (with memoization):")
    
    start = time.perf_counter()
    for i in range(5):
        result = expensive_computation(i)
        print(f"  expensive_computation({i}) = {result}")
    first_run = time.perf_counter() - start
    
    print("\nComputing again (cached):")
    start = time.perf_counter()
    for i in range(5):
        result = expensive_computation(i)
        print(f"  expensive_computation({i}) = {result}")
    second_run = time.perf_counter() - start
    
    print(f"\nFirst run: {first_run:.4f}s")
    print(f"Second run: {second_run:.4f}s")
    print(f"Speedup: {first_run/second_run:.1f}x")
    print(f"Cache info: {expensive_computation.cache_info()}")
    
    print()

# ============================================================
# CHALLENGE 5: itertools Data Processing
# ============================================================

def challenge_itertools():
    """
    Process data efficiently with itertools.
    
    TODO: Build efficient iterator pipeline
    """
    print("--- Challenge 5: itertools Pipeline ---")
    
    # Generate data
    data = range(1, 101)
    
    # Pipeline: filter → map → accumulate → take top 5
    pipeline = itertools.islice(
        sorted(
            itertools.accumulate(
                map(lambda x: x ** 2,
                    filter(lambda x: x % 3 == 0, data))
            ),
            reverse=True
        ),
        5
    )
    
    result = list(pipeline)
    
    print("Pipeline: range(1,101)")
    print("  → filter(divisible by 3)")
    print("  → map(square)")
    print("  → accumulate(sum)")
    print("  → sort(descending)")
    print("  → take(5)")
    print(f"\nTop 5 results: {result}")
    
    # Groupby example
    words = ['apple', 'apricot', 'banana', 'blueberry', 'cherry', 'cranberry']
    words_sorted = sorted(words, key=len)
    
    print("\nWords grouped by length:")
    for length, group in itertools.groupby(words_sorted, key=len):
        print(f"  {length} letters: {list(group)}")
    
    print()

# ============================================================
# CHALLENGE 6: Complete ETL System
# ============================================================

class FunctionalETL:
    """
    Complete ETL system using functional programming.
    
    TODO: Build production-ready ETL pipeline
    """
    
    def __init__(self):
        self.extractors = []
        self.transformers = []
        self.loaders = []
    
    def add_extractor(self, func):
        """Add extraction function"""
        self.extractors.append(func)
        return self
    
    def add_transformer(self, func):
        """Add transformation function"""
        self.transformers.append(func)
        return self
    
    def add_loader(self, func):
        """Add loading function"""
        self.loaders.append(func)
        return self
    
    def execute(self, source):
        """Execute ETL pipeline"""
        # Extract
        data = source
        for extractor in self.extractors:
            data = extractor(data)
        
        # Transform
        for transformer in self.transformers:
            data = transformer(data)
        
        # Load
        for loader in self.loaders:
            data = loader(data)
        
        return data

def test_functional_etl():
    """Test functional ETL system"""
    print("--- Challenge 6: Complete ETL System ---")
    
    # Source data
    raw_logs = [
        "2024-01-01 10:00:00 INFO User login: alice",
        "2024-01-01 10:05:00 ERROR Database connection failed",
        "2024-01-01 10:10:00 INFO User login: bob",
        "2024-01-01 10:15:00 ERROR Timeout",
        "2024-01-01 10:20:00 INFO User logout: alice",
    ]
    
    # Build ETL pipeline
    etl = FunctionalETL()
    
    # Extractors
    etl.add_extractor(lambda logs: [log.split(' ', 3) for log in logs])
    
    # Transformers
    etl.add_transformer(lambda logs: [
        {'date': date, 'time': time, 'level': level, 'message': msg}
        for date, time, level, msg in logs
    ])
    etl.add_transformer(lambda logs: [log for log in logs if log['level'] == 'ERROR'])
    
    # Loaders
    etl.add_loader(lambda logs: sorted(logs, key=lambda l: l['time']))
    
    # Execute
    errors = etl.execute(raw_logs)
    
    print("Extracted errors:")
    for error in errors:
        print(f"  [{error['date']} {error['time']}] {error['message']}")
    
    print()

# ============================================================
# SELF-ASSESSMENT
# ============================================================

def self_assessment():
    """
    Self-assessment checklist for Week 4.
    """
    print("=" * 60)
    print("WEEK 4 SELF-ASSESSMENT")
    print("=" * 60)
    
    checklist = [
        ("map/filter/reduce", "Can you transform and aggregate data functionally?"),
        ("Lambda functions", "Do you know when to use lambda vs def?"),
        ("functools.partial", "Can you create specialized functions?"),
        ("Function composition", "Can you build data pipelines?"),
        ("Higher-order functions", "Can you write functions that take/return functions?"),
        ("itertools", "Can you process data efficiently with iterators?"),
        ("Functional style", "Can you write pure, composable functions?"),
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
    print("Week 4, Day 7: Review & Challenge")
    print("=" * 60)
    print()
    
    week4_review()
    
    print("\n" + "=" * 60)
    print("CHALLENGES")
    print("=" * 60 + "\n")
    
    challenge_data_pipeline()
    challenge_aggregation()
    challenge_validation()
    challenge_memoization()
    challenge_itertools()
    test_functional_etl()
    
    self_assessment()
    
    print("=" * 60)
    print("✅ Week 4 Complete!")
    print("=" * 60)
    print("\n🎉 Congratulations! You've mastered functional programming!")
    print("\n📚 Next: Week 5 - Decorators")
    print("\n💡 Keep using functional patterns for cleaner code!")

