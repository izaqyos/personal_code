"""
Week 1, Day 6: Chaining Comparisons and Walrus Operator (:=)

Learning Objectives:
- Master comparison chaining for readable conditions
- Understand the walrus operator (assignment expressions)
- Learn when and where to use := effectively
- Practice writing more concise and readable code

Time: 10-15 minutes
"""

import re
import time
from typing import List, Optional

# ============================================================
# EXERCISE 1: Comparison Chaining
# ============================================================

def comparison_chaining_basics():
    """
    Practice chaining comparisons for cleaner code.
    
    Python allows: a < b < c instead of: a < b and b < c
    """
    print("--- Exercise 1: Comparison Chaining ---")
    
    # Example 1: Range checking
    age = 25
    
    # Non-Pythonic
    if age >= 18 and age <= 65:
        print(f"  Age {age}: Working age (non-Pythonic)")
    
    # Pythonic - chained comparison
    if 18 <= age <= 65:
        print(f"  Age {age}: Working age (Pythonic)")
    
    # Example 2: Multiple comparisons
    x, y, z = 5, 10, 15
    
    # TODO: Check if x < y < z using chaining
    if x < y < z:
        print(f"  {x} < {y} < {z}: Ascending order")
    
    # Example 3: Equality chain
    a = b = c = 10
    if a == b == c:
        print(f"  All equal: {a}, {b}, {c}")
    
    # Example 4: Mixed comparisons
    score = 85
    if 0 <= score < 60:
        grade = "F"
    elif 60 <= score < 70:
        grade = "D"
    elif 70 <= score < 80:
        grade = "C"
    elif 80 <= score < 90:
        grade = "B"
    elif 90 <= score <= 100:
        grade = "A"
    else:
        grade = "Invalid"
    
    print(f"  Score {score}: Grade {grade}")
    
    print()

# ============================================================
# EXERCISE 2: Walrus Operator Basics
# ============================================================

def walrus_operator_basics():
    """
    Introduction to the walrus operator := (Python 3.8+)
    
    Allows assignment within expressions
    """
    print("--- Exercise 2: Walrus Operator Basics ---")
    
    # Example 1: Avoid duplicate computation
    data = [1, 2, 3, 4, 5]
    
    # Without walrus operator
    result = sum(data)
    if result > 10:
        print(f"  Sum {result} is greater than 10")
    
    # With walrus operator - assign and check in one line
    if (result := sum(data)) > 10:
        print(f"  Sum {result} is greater than 10 (using :=)")
    
    # Example 2: In while loops
    print("\n  Reading input (simulated):")
    inputs = ["hello", "world", "quit"]
    index = 0
    
    # TODO: Use walrus operator in while condition
    while (line := inputs[index] if index < len(inputs) else "quit") != "quit":
        print(f"    Processing: {line}")
        index += 1
    
    print()

# ============================================================
# EXERCISE 3: Walrus in List Comprehensions
# ============================================================

def walrus_in_comprehensions():
    """
    Use walrus operator to avoid recomputation in comprehensions.
    
    TODO: Practice using := in list comprehensions
    """
    print("--- Exercise 3: Walrus in Comprehensions ---")
    
    # Example 1: Filter and transform with expensive operation
    def expensive_operation(x):
        """Simulate expensive computation"""
        time.sleep(0.001)
        return x ** 2
    
    numbers = list(range(10))
    
    # Without walrus - computes twice
    start = time.perf_counter()
    result1 = [expensive_operation(x) for x in numbers if expensive_operation(x) > 25]
    time1 = time.perf_counter() - start
    
    # With walrus - computes once
    start = time.perf_counter()
    result2 = [y for x in numbers if (y := expensive_operation(x)) > 25]
    time2 = time.perf_counter() - start
    
    print(f"  Without :=: {result1} ({time1:.4f}s)")
    print(f"  With :=:    {result2} ({time2:.4f}s)")
    print(f"  Speedup: {time1/time2:.2f}x")
    
    # Example 2: Capture intermediate values
    texts = ["hello", "world", "python", "programming"]
    
    # TODO: Get lengths > 5 along with the length
    result = [(text, length) for text in texts if (length := len(text)) > 5]
    print(f"\n  Long words: {result}")
    
    print()

# ============================================================
# EXERCISE 4: Walrus in Conditionals
# ============================================================

def walrus_in_conditionals():
    """
    Use walrus operator for cleaner conditional logic.
    
    TODO: Refactor conditionals using :=
    """
    print("--- Exercise 4: Walrus in Conditionals ---")
    
    # Example 1: Regex matching
    text = "Email: alice@example.com"
    pattern = r'(\w+@\w+\.\w+)'
    
    # Without walrus
    match = re.search(pattern, text)
    if match:
        email = match.group(1)
        print(f"  Found email: {email}")
    
    # With walrus - more concise
    if (match := re.search(pattern, text)):
        print(f"  Found email: {match.group(1)} (using :=)")
    
    # Example 2: Processing optional data
    def get_user_data(user_id: int) -> Optional[dict]:
        """Simulate database lookup"""
        users = {
            1: {"name": "Alice", "age": 30},
            2: {"name": "Bob", "age": 25},
        }
        return users.get(user_id)
    
    # Without walrus
    user_data = get_user_data(1)
    if user_data:
        print(f"\n  User: {user_data['name']}, Age: {user_data['age']}")
    
    # With walrus
    if (user_data := get_user_data(2)):
        print(f"  User: {user_data['name']}, Age: {user_data['age']} (using :=)")
    
    print()

# ============================================================
# EXERCISE 5: Real-World Scenario - File Processing
# ============================================================

def process_file_with_walrus():
    """
    Process a file using walrus operator for cleaner code.
    
    TODO: Implement file processing with :=
    """
    print("--- Exercise 5: File Processing with Walrus ---")
    
    # Create a test file
    test_file = "test_walrus.txt"
    with open(test_file, 'w') as f:
        f.write("Line 1: Important data\n")
        f.write("Line 2: Skip this\n")
        f.write("Line 3: More important data\n")
        f.write("Line 4: Skip this too\n")
        f.write("Line 5: Final important data\n")
    
    # Traditional approach
    print("Traditional approach:")
    with open(test_file, 'r') as f:
        line = f.readline()
        while line:
            if "important" in line.lower():
                print(f"  {line.strip()}")
            line = f.readline()
    
    # With walrus operator - cleaner
    print("\nWith walrus operator:")
    with open(test_file, 'r') as f:
        # TODO: Use walrus in while condition
        while (line := f.readline()):
            if "important" in line.lower():
                print(f"  {line.strip()}")
    
    # Cleanup
    import os
    os.remove(test_file)
    
    print()

# ============================================================
# EXERCISE 6: Combining Chaining and Walrus
# ============================================================

def combining_features():
    """
    Combine comparison chaining and walrus operator.
    
    TODO: Practice combining both features
    """
    print("--- Exercise 6: Combining Chaining and Walrus ---")
    
    # Example: Validate and process scores
    scores = [45, 78, 92, 105, -5, 88, 67]
    
    print("Valid scores (0-100) with grades:")
    for score in scores:
        # TODO: Combine walrus and chaining
        if 0 <= (s := score) <= 100:
            if 90 <= s <= 100:
                grade = "A"
            elif 80 <= s < 90:
                grade = "B"
            elif 70 <= s < 80:
                grade = "C"
            elif 60 <= s < 70:
                grade = "D"
            else:
                grade = "F"
            print(f"  Score {s}: {grade}")
        else:
            print(f"  Score {score}: Invalid")
    
    print()

# ============================================================
# EXERCISE 7: When NOT to Use Walrus
# ============================================================

def walrus_antipatterns():
    """
    Learn when NOT to use the walrus operator.
    
    Avoid overusing := - it can reduce readability
    """
    print("--- Exercise 7: When NOT to Use Walrus ---")
    
    # Bad: Overuse makes code hard to read
    # if (x := 5) > 3 and (y := x * 2) < 15 and (z := y + x) > 10:
    #     print(f"Too complex: {x}, {y}, {z}")
    
    # Good: Use separate lines for clarity
    x = 5
    if x > 3:
        y = x * 2
        if y < 15:
            z = y + x
            if z > 10:
                print(f"  Clear logic: {x}, {y}, {z}")
    
    # Bad: Walrus in function arguments (confusing)
    # result = some_function(x := 10, y := x * 2)  # Don't do this
    
    # Good: Assign before calling
    x = 10
    y = x * 2
    # result = some_function(x, y)
    
    print("\n  Guidelines:")
    print("  ✓ Use := to avoid duplicate computation")
    print("  ✓ Use := in while loops and comprehensions")
    print("  ✓ Use := when assignment + condition makes sense")
    print("  ✗ Don't chain multiple := in one expression")
    print("  ✗ Don't use := if it reduces readability")
    
    print()

# ============================================================
# BONUS CHALLENGE
# ============================================================

def parse_log_entries(log_lines: List[str]) -> List[dict]:
    """
    Parse log entries efficiently using walrus operator.
    
    TODO: Implement log parsing with :=
    
    Log format: "LEVEL: message [timestamp]"
    Extract entries where level is ERROR or WARNING
    """
    pattern = r'(ERROR|WARNING): (.+) \[(\d+)\]'
    
    # TODO: Use walrus operator in list comprehension
    return [
        {"level": match.group(1), "message": match.group(2), "timestamp": match.group(3)}
        for line in log_lines
        if (match := re.search(pattern, line))
    ]

def test_log_parsing():
    """Test the log parsing function"""
    print("--- Bonus Challenge: Log Parsing ---")
    
    logs = [
        "INFO: Application started [1234567890]",
        "ERROR: Database connection failed [1234567891]",
        "WARNING: High memory usage [1234567892]",
        "DEBUG: Processing request [1234567893]",
        "ERROR: Timeout occurred [1234567894]",
    ]
    
    parsed = parse_log_entries(logs)
    
    print("Parsed errors and warnings:")
    for entry in parsed:
        print(f"  [{entry['timestamp']}] {entry['level']}: {entry['message']}")
    
    print()

# ============================================================
# PERFORMANCE COMPARISON
# ============================================================

def performance_comparison():
    """
    Compare performance with and without walrus operator.
    """
    print("--- Performance Comparison ---")
    
    data = list(range(10000))
    
    def expensive_check(x):
        return x ** 2
    
    # Without walrus - double computation
    start = time.perf_counter()
    result1 = [expensive_check(x) for x in data if expensive_check(x) > 5000]
    time1 = time.perf_counter() - start
    
    # With walrus - single computation
    start = time.perf_counter()
    result2 = [y for x in data if (y := expensive_check(x)) > 5000]
    time2 = time.perf_counter() - start
    
    print(f"Without :=: {time1:.6f}s")
    print(f"With :=:    {time2:.6f}s")
    print(f"Speedup:    {time1/time2:.2f}x")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Comparison Chaining:
    - Time: O(n) for n comparisons (short-circuits)
    - Space: O(1)
    - More readable than multiple 'and' operators
    
    Walrus Operator:
    - Time: Same as without, but avoids duplicate computation
    - Space: O(1) - just creates a binding
    - Can reduce time complexity by eliminating redundant calls
    
    Best Practices:
    - Use chaining for range checks and ordered comparisons
    - Use := to avoid duplicate expensive operations
    - Don't sacrifice readability for brevity
    - := is especially useful in while loops and comprehensions
    
    Security Considerations:
    - Walrus operator doesn't introduce security issues
    - Be careful with side effects in assigned expressions
    - Ensure expressions in := are idempotent when possible
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 1, Day 6: Chaining Comparisons and Walrus Operator")
    print("=" * 60)
    print()
    
    comparison_chaining_basics()
    walrus_operator_basics()
    walrus_in_comprehensions()
    walrus_in_conditionals()
    process_file_with_walrus()
    combining_features()
    walrus_antipatterns()
    test_log_parsing()
    performance_comparison()
    
    print("=" * 60)
    print("✅ Day 6 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Chain comparisons for readable range checks")
    print("2. Use := to avoid duplicate computation")
    print("3. Walrus operator shines in while loops and comprehensions")
    print("4. Don't overuse := - readability matters")

