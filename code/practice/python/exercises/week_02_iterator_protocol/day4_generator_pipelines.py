"""
Week 2, Day 4: Generator Expressions for Pipeline Processing

Learning Objectives:
- Master generator expressions for data pipelines
- Learn to chain multiple generator expressions
- Understand lazy evaluation benefits
- Build memory-efficient processing pipelines

Time: 10-15 minutes
"""

import sys
import time
from typing import Generator

# ============================================================
# EXERCISE 1: Generator Expression Basics
# ============================================================

def generator_expression_basics():
    """
    Compare list comprehensions with generator expressions.
    
    List comp: [expr for item in iterable]
    Gen expr:  (expr for item in iterable)
    """
    print("--- Exercise 1: Generator Expression Basics ---")
    
    # List comprehension
    list_comp = [x**2 for x in range(10)]
    print(f"List comprehension: {list_comp}")
    print(f"  Type: {type(list_comp)}")
    print(f"  Size: {sys.getsizeof(list_comp)} bytes")
    
    # Generator expression
    gen_expr = (x**2 for x in range(10))
    print(f"\nGenerator expression: {gen_expr}")
    print(f"  Type: {type(gen_expr)}")
    print(f"  Size: {sys.getsizeof(gen_expr)} bytes")
    print(f"  Values: {list(gen_expr)}")
    
    print()

# ============================================================
# EXERCISE 2: Simple Pipeline
# ============================================================

def simple_pipeline():
    """
    Build a simple data processing pipeline.
    
    TODO: Chain generator expressions
    """
    print("--- Exercise 2: Simple Pipeline ---")
    
    # Data source
    numbers = range(1, 21)
    
    # TODO: Build pipeline: filter evens → square → take first 5
    evens = (x for x in numbers if x % 2 == 0)
    squared = (x**2 for x in evens)
    first_five = list(x for i, x in enumerate(squared) if i < 5)
    
    print(f"Pipeline: range(1,21) → filter evens → square → take 5")
    print(f"Result: {first_five}")
    
    # One-liner version
    result = list((x**2 for x in range(1, 21) if x % 2 == 0))[:5]
    print(f"One-liner: {result}")
    
    print()

# ============================================================
# EXERCISE 3: Multi-Stage Pipeline
# ============================================================

def multi_stage_pipeline():
    """
    Build a multi-stage data processing pipeline.
    
    TODO: Process text data through multiple stages
    """
    print("--- Exercise 3: Multi-Stage Pipeline ---")
    
    # Sample text data
    text_data = [
        "  HELLO WORLD  ",
        "python programming",
        "  DATA SCIENCE  ",
        "machine learning",
        "  ARTIFICIAL INTELLIGENCE  "
    ]
    
    # TODO: Build pipeline
    # Stage 1: Strip whitespace
    stripped = (text.strip() for text in text_data)
    
    # Stage 2: Convert to lowercase
    lowercased = (text.lower() for text in stripped)
    
    # Stage 3: Filter lines with more than 10 characters
    filtered = (text for text in lowercased if len(text) > 10)
    
    # Stage 4: Split into words
    words = (word for text in filtered for word in text.split())
    
    print("Pipeline stages:")
    print("  1. Strip whitespace")
    print("  2. Convert to lowercase")
    print("  3. Filter length > 10")
    print("  4. Split into words")
    print(f"\nResult: {list(words)}")
    
    print()

# ============================================================
# EXERCISE 4: File Processing Pipeline
# ============================================================

def file_processing_pipeline():
    """
    Process a file using generator pipeline.
    
    TODO: Build pipeline to process log file
    """
    print("--- Exercise 4: File Processing Pipeline ---")
    
    # Create test file
    test_file = "test_pipeline.log"
    with open(test_file, 'w') as f:
        f.write("INFO: Application started\n")
        f.write("DEBUG: Loading configuration\n")
        f.write("ERROR: Database connection failed\n")
        f.write("INFO: Retrying connection\n")
        f.write("ERROR: Connection timeout\n")
        f.write("WARNING: Using fallback mode\n")
        f.write("INFO: Application ready\n")
    
    # TODO: Build pipeline to extract error messages
    with open(test_file, 'r') as f:
        # Stage 1: Read lines
        lines = (line.strip() for line in f)
        
        # Stage 2: Filter ERROR lines
        errors = (line for line in lines if line.startswith('ERROR'))
        
        # Stage 3: Extract message (after colon)
        messages = (line.split(':', 1)[1].strip() for line in errors)
        
        print("Error messages:")
        for msg in messages:
            print(f"  - {msg}")
    
    # Cleanup
    import os
    os.remove(test_file)
    
    print()

# ============================================================
# EXERCISE 5: Nested Generator Expressions
# ============================================================

def nested_generator_expressions():
    """
    Use nested generator expressions for complex transformations.
    
    TODO: Flatten and process nested data
    """
    print("--- Exercise 5: Nested Generator Expressions ---")
    
    # Nested data structure
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    # TODO: Flatten matrix using nested generator
    flattened = (num for row in matrix for num in row)
    print(f"Matrix: {matrix}")
    print(f"Flattened: {list(flattened)}")
    
    # TODO: Filter and transform
    # Get even numbers, square them
    result = (num**2 for row in matrix for num in row if num % 2 == 0)
    print(f"Even numbers squared: {list(result)}")
    
    # TODO: Create pairs from two lists
    list1 = ['a', 'b', 'c']
    list2 = [1, 2, 3]
    pairs = ((letter, num) for letter in list1 for num in list2)
    print(f"\nPairs: {list(pairs)}")
    
    print()

# ============================================================
# EXERCISE 6: Pipeline with Aggregation
# ============================================================

def pipeline_with_aggregation():
    """
    Build pipeline that aggregates results.
    
    TODO: Calculate statistics using pipeline
    """
    print("--- Exercise 6: Pipeline with Aggregation ---")
    
    # Sample data: test scores
    scores = [
        ("Alice", 85), ("Bob", 92), ("Charlie", 78),
        ("Diana", 95), ("Eve", 88), ("Frank", 72),
        ("Grace", 90), ("Henry", 85), ("Iris", 93)
    ]
    
    # TODO: Pipeline to get high scorers (>= 85)
    high_scorers = ((name, score) for name, score in scores if score >= 85)
    
    print("High scorers (>= 85):")
    high_scorers_list = list(high_scorers)
    for name, score in high_scorers_list:
        print(f"  {name}: {score}")
    
    # TODO: Calculate average of high scores
    high_scores_only = (score for name, score in scores if score >= 85)
    high_scores_list = list(high_scores_only)
    avg = sum(high_scores_list) / len(high_scores_list)
    print(f"\nAverage high score: {avg:.2f}")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - CSV Processing
# ============================================================

def csv_processing_pipeline():
    """
    Process CSV data using generator pipeline.
    
    TODO: Build efficient CSV processing pipeline
    """
    print("--- Exercise 7: CSV Processing Pipeline ---")
    
    # Create test CSV file
    test_file = "test_data.csv"
    with open(test_file, 'w') as f:
        f.write("name,age,salary,department\n")
        f.write("Alice,30,75000,Engineering\n")
        f.write("Bob,25,65000,Marketing\n")
        f.write("Charlie,35,85000,Engineering\n")
        f.write("Diana,28,70000,Sales\n")
        f.write("Eve,32,80000,Engineering\n")
    
    # TODO: Build pipeline to analyze data
    with open(test_file, 'r') as f:
        # Skip header
        next(f)
        
        # Parse lines
        lines = (line.strip() for line in f)
        
        # Split into fields
        records = (line.split(',') for line in lines)
        
        # Convert to dict
        employees = (
            {
                'name': fields[0],
                'age': int(fields[1]),
                'salary': int(fields[2]),
                'department': fields[3]
            }
            for fields in records
        )
        
        # Filter Engineering department
        engineers = (emp for emp in employees if emp['department'] == 'Engineering')
        
        # Extract salaries
        salaries = [emp['salary'] for emp in engineers]
        
        print("Engineering salaries:")
        for salary in salaries:
            print(f"  ${salary:,}")
        
        if salaries:
            print(f"\nAverage: ${sum(salaries) / len(salaries):,.2f}")
    
    # Cleanup
    import os
    os.remove(test_file)
    
    print()

# ============================================================
# EXERCISE 8: Pipeline Performance
# ============================================================

def pipeline_performance():
    """
    Compare performance of different approaches.
    """
    print("--- Exercise 8: Pipeline Performance ---")
    
    n = 1_000_000
    
    # Approach 1: Multiple list comprehensions (memory intensive)
    start = time.perf_counter()
    data1 = [x for x in range(n)]
    filtered1 = [x for x in data1 if x % 2 == 0]
    squared1 = [x**2 for x in filtered1]
    result1 = squared1[:10]
    time1 = time.perf_counter() - start
    
    # Approach 2: Chained generator expressions (memory efficient)
    start = time.perf_counter()
    pipeline = (x**2 for x in range(n) if x % 2 == 0)
    result2 = list(x for i, x in enumerate(pipeline) if i < 10)
    time2 = time.perf_counter() - start
    
    # Approach 3: Generator with islice (most efficient)
    import itertools
    start = time.perf_counter()
    pipeline = (x**2 for x in range(n) if x % 2 == 0)
    result3 = list(itertools.islice(pipeline, 10))
    time3 = time.perf_counter() - start
    
    print(f"Processing {n:,} numbers, getting first 10 even squares:")
    print(f"  Multiple lists: {time1:.4f}s")
    print(f"  Generator chain: {time2:.4f}s ({time1/time2:.2f}x faster)")
    print(f"  With islice: {time3:.4f}s ({time1/time3:.2f}x faster)")
    
    print()

# ============================================================
# BONUS CHALLENGE: Complex Data Pipeline
# ============================================================

def complex_pipeline_challenge():
    """
    Build a complex data processing pipeline.
    
    TODO: Process transaction data with multiple stages
    """
    print("--- Bonus Challenge: Complex Pipeline ---")
    
    # Transaction data: (user_id, amount, category, date)
    transactions = [
        (1, 100.0, "food", "2024-01-01"),
        (2, 50.0, "transport", "2024-01-01"),
        (1, 75.0, "food", "2024-01-02"),
        (3, 200.0, "entertainment", "2024-01-02"),
        (2, 30.0, "food", "2024-01-03"),
        (1, 120.0, "transport", "2024-01-03"),
        (3, 80.0, "food", "2024-01-04"),
        (1, 45.0, "food", "2024-01-04"),
    ]
    
    # TODO: Build pipeline to analyze spending
    # 1. Filter food category
    food_transactions = (t for t in transactions if t[2] == "food")
    
    # 2. Group by user (need to sort first)
    from itertools import groupby
    sorted_trans = sorted(food_transactions, key=lambda t: t[0])
    
    # 3. Calculate total per user
    print("Food spending by user:")
    for user_id, group in groupby(sorted_trans, key=lambda t: t[0]):
        trans_list = list(group)
        total = sum(t[1] for t in trans_list)
        count = len(trans_list)
        avg = total / count
        print(f"  User {user_id}: ${total:.2f} ({count} transactions, avg ${avg:.2f})")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Generator Expressions:
    - Creation: O(1) - just creates generator object
    - Consumption: O(n) for n items
    - Space: O(1) - only stores current state
    
    Chained Generators:
    - Each stage: O(1) space
    - Total pipeline: O(k) where k is number of stages
    - Much better than intermediate lists: O(n) per stage
    
    Example Pipeline:
    data = range(1000000)
    filtered = (x for x in data if x % 2 == 0)  # O(1) space
    squared = (x**2 for x in filtered)           # O(1) space
    result = list(squared)                       # O(n) space only at end
    
    vs List Comprehensions:
    filtered = [x for x in data if x % 2 == 0]  # O(n) space
    squared = [x**2 for x in filtered]           # O(n) space
    Total: O(2n) = O(n) space for intermediates
    
    Benefits:
    - Lazy evaluation - compute only when needed
    - Memory efficient - no intermediate lists
    - Can process infinite streams
    - Composable - easy to add/remove stages
    
    When to Use:
    - Large datasets that don't fit in memory
    - Streaming data processing
    - When you don't need all data at once
    - Building flexible, reusable pipelines
    
    Security Considerations:
    - Generators prevent memory exhaustion
    - Validate input size before processing
    - Be careful with infinite generators
    - Use timeouts for long-running pipelines
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 2, Day 4: Generator Expressions for Pipelines")
    print("=" * 60)
    print()
    
    generator_expression_basics()
    simple_pipeline()
    multi_stage_pipeline()
    file_processing_pipeline()
    nested_generator_expressions()
    pipeline_with_aggregation()
    csv_processing_pipeline()
    pipeline_performance()
    complex_pipeline_challenge()
    
    print("=" * 60)
    print("✅ Day 4 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Generator expressions are memory-efficient (O(1) space)")
    print("2. Chain generators to build powerful pipelines")
    print("3. Each stage processes items lazily")
    print("4. Much faster than multiple list comprehensions")

