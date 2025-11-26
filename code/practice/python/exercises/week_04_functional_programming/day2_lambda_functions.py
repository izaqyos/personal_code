"""
Week 4, Day 2: Lambda Functions and Anonymous Functions

Learning Objectives:
- Master lambda syntax and use cases
- Understand lambda vs def functions
- Learn when to use lambdas appropriately
- Practice lambda with map, filter, sorted
- Avoid lambda anti-patterns

Time: 10-15 minutes
"""

from typing import Callable
import operator

# ============================================================
# EXERCISE 1: Lambda Basics
# ============================================================

def lambda_basics():
    """
    Learn basic lambda syntax.
    
    lambda arguments: expression
    """
    print("--- Exercise 1: Lambda Basics ---")
    
    # Simple lambda
    square = lambda x: x ** 2
    print(f"square(5) = {square(5)}")
    
    # Multiple arguments
    add = lambda x, y: x + y
    print(f"add(3, 4) = {add(3, 4)}")
    
    # No arguments
    get_pi = lambda: 3.14159
    print(f"get_pi() = {get_pi()}")
    
    # With default arguments
    power = lambda x, n=2: x ** n
    print(f"power(3) = {power(3)}")
    print(f"power(3, 3) = {power(3, 3)}")
    
    # Immediately invoked
    result = (lambda x, y: x * y)(5, 6)
    print(f"\nImmediately invoked: (lambda x, y: x * y)(5, 6) = {result}")
    
    print()

# ============================================================
# EXERCISE 2: Lambda vs def
# ============================================================

def lambda_vs_def():
    """
    Compare lambda with regular functions.
    
    TODO: Understand when to use each
    """
    print("--- Exercise 2: Lambda vs def ---")
    
    # Lambda (single expression)
    double_lambda = lambda x: x * 2
    
    # def (can have multiple statements)
    def double_def(x):
        """Double a number"""
        result = x * 2
        return result
    
    print(f"double_lambda(5) = {double_lambda(5)}")
    print(f"double_def(5) = {double_def(5)}")
    
    # Lambda limitations
    print("\nLambda limitations:")
    print("  • Single expression only")
    print("  • No statements (no if/while/for/try)")
    print("  • No docstrings")
    print("  • No annotations")
    print("  • Anonymous (no name in tracebacks)")
    
    # def advantages
    print("\ndef advantages:")
    print("  • Multiple statements")
    print("  • Docstrings")
    print("  • Type annotations")
    print("  • Named (better debugging)")
    print("  • More readable for complex logic")
    
    print()

# ============================================================
# EXERCISE 3: Lambda with Built-in Functions
# ============================================================

def lambda_with_builtins():
    """
    Use lambda with map, filter, sorted.
    
    TODO: Practice common lambda patterns
    """
    print("--- Exercise 3: Lambda with Built-ins ---")
    
    numbers = [1, 2, 3, 4, 5]
    
    # With map
    squared = list(map(lambda x: x ** 2, numbers))
    print(f"Squared: {squared}")
    
    # With filter
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Evens: {evens}")
    
    # With sorted
    words = ['banana', 'pie', 'Washington', 'book']
    
    # Sort by length
    by_length = sorted(words, key=lambda w: len(w))
    print(f"\nSorted by length: {by_length}")
    
    # Sort case-insensitive
    by_alpha = sorted(words, key=lambda w: w.lower())
    print(f"Sorted alphabetically: {by_alpha}")
    
    # Sort by last letter
    by_last = sorted(words, key=lambda w: w[-1])
    print(f"Sorted by last letter: {by_last}")
    
    # Sort tuples by second element
    pairs = [(1, 'one'), (3, 'three'), (2, 'two')]
    by_second = sorted(pairs, key=lambda p: p[1])
    print(f"\nPairs sorted by second: {by_second}")
    
    print()

# ============================================================
# EXERCISE 4: Lambda with Data Structures
# ============================================================

def lambda_with_data_structures():
    """
    Use lambda with dictionaries and lists.
    
    TODO: Practice sorting complex data
    """
    print("--- Exercise 4: Lambda with Data Structures ---")
    
    students = [
        {'name': 'Alice', 'grade': 85, 'age': 20},
        {'name': 'Bob', 'grade': 92, 'age': 19},
        {'name': 'Charlie', 'grade': 78, 'age': 21},
        {'name': 'Diana', 'grade': 95, 'age': 20},
    ]
    
    # Sort by grade
    by_grade = sorted(students, key=lambda s: s['grade'], reverse=True)
    print("Sorted by grade (high to low):")
    for s in by_grade:
        print(f"  {s['name']}: {s['grade']}")
    
    # Sort by age, then grade
    by_age_grade = sorted(students, key=lambda s: (s['age'], -s['grade']))
    print("\nSorted by age, then grade:")
    for s in by_age_grade:
        print(f"  {s['name']}: age {s['age']}, grade {s['grade']}")
    
    # Find max by grade
    top_student = max(students, key=lambda s: s['grade'])
    print(f"\nTop student: {top_student['name']} ({top_student['grade']})")
    
    # Group by age using dict
    from collections import defaultdict
    by_age = defaultdict(list)
    for student in students:
        by_age[student['age']].append(student['name'])
    
    print("\nStudents by age:")
    for age in sorted(by_age.keys()):
        print(f"  {age}: {by_age[age]}")
    
    print()

# ============================================================
# EXERCISE 5: Lambda Anti-Patterns
# ============================================================

def lambda_antipatterns():
    """
    Learn what NOT to do with lambdas.
    
    TODO: Avoid common mistakes
    """
    print("--- Exercise 5: Lambda Anti-Patterns ---")
    
    print("❌ BAD: Assigning lambda to variable")
    print("   square = lambda x: x ** 2")
    print("\n✅ GOOD: Use def instead")
    print("   def square(x): return x ** 2")
    
    print("\n❌ BAD: Complex lambda")
    print("   lambda x: x if x > 0 else -x if x < 0 else 0")
    print("\n✅ GOOD: Use def for clarity")
    print("   def abs_value(x):")
    print("       if x > 0: return x")
    print("       elif x < 0: return -x")
    print("       else: return 0")
    
    print("\n❌ BAD: Lambda with side effects")
    print("   results = []")
    print("   map(lambda x: results.append(x*2), numbers)")
    print("\n✅ GOOD: Use list comprehension or loop")
    print("   results = [x*2 for x in numbers]")
    
    print("\n❌ BAD: Overly nested lambdas")
    print("   lambda x: (lambda y: x + y)")
    print("\n✅ GOOD: Use def or partial")
    print("   def make_adder(x):")
    print("       return lambda y: x + y")
    
    print("\n💡 Use lambda when:")
    print("  • Simple, single expression")
    print("  • Used once (e.g., as key function)")
    print("  • Improves readability")
    
    print("\n💡 Use def when:")
    print("  • Multiple statements needed")
    print("  • Complex logic")
    print("  • Reused multiple times")
    print("  • Needs docstring/annotations")
    
    print()

# ============================================================
# EXERCISE 6: Lambda Alternatives with operator module
# ============================================================

def lambda_alternatives():
    """
    Use operator module instead of simple lambdas.
    
    TODO: Learn more efficient alternatives
    """
    print("--- Exercise 6: Lambda Alternatives (operator module) ---")
    
    numbers = [5, 2, 8, 1, 9]
    
    # Lambda for getting item
    pairs = [(1, 'one'), (3, 'three'), (2, 'two')]
    
    # ❌ Using lambda
    sorted_lambda = sorted(pairs, key=lambda x: x[0])
    print(f"With lambda: {sorted_lambda}")
    
    # ✅ Using operator.itemgetter
    sorted_operator = sorted(pairs, key=operator.itemgetter(0))
    print(f"With operator.itemgetter: {sorted_operator}")
    
    # Multiple keys
    students = [
        ('Alice', 85, 20),
        ('Bob', 92, 19),
        ('Charlie', 85, 21),
    ]
    
    # Sort by grade, then age
    sorted_students = sorted(students, key=operator.itemgetter(1, 2))
    print(f"\nSorted by grade, age: {sorted_students}")
    
    # operator.attrgetter for objects
    from collections import namedtuple
    Student = namedtuple('Student', ['name', 'grade'])
    students_nt = [Student('Alice', 85), Student('Bob', 92)]
    
    sorted_by_grade = sorted(students_nt, key=operator.attrgetter('grade'))
    print(f"\nSorted by grade attribute: {sorted_by_grade}")
    
    # operator.methodcaller
    words = ['hello', 'world', 'python']
    uppercased = list(map(operator.methodcaller('upper'), words))
    print(f"\nUppercased: {uppercased}")
    
    print("\n💡 operator module benefits:")
    print("  • Faster than lambda")
    print("  • More readable")
    print("  • Better for simple operations")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - Data Transformation
# ============================================================

def data_transformation():
    """
    Transform data using lambdas appropriately.
    
    TODO: Process API response data
    """
    print("--- Exercise 7: Data Transformation ---")
    
    # API response (simulated)
    api_response = [
        {'id': 1, 'name': 'Product A', 'price': 29.99, 'stock': 15},
        {'id': 2, 'name': 'Product B', 'price': 49.99, 'stock': 0},
        {'id': 3, 'name': 'Product C', 'price': 19.99, 'stock': 8},
        {'id': 4, 'name': 'Product D', 'price': 99.99, 'stock': 3},
    ]
    
    # Filter in-stock products
    in_stock = list(filter(lambda p: p['stock'] > 0, api_response))
    print("In-stock products:")
    for p in in_stock:
        print(f"  {p['name']}: ${p['price']} ({p['stock']} available)")
    
    # Get product names
    names = list(map(lambda p: p['name'], in_stock))
    print(f"\nProduct names: {names}")
    
    # Calculate total inventory value
    total_value = sum(map(lambda p: p['price'] * p['stock'], in_stock))
    print(f"\nTotal inventory value: ${total_value:.2f}")
    
    # Find most expensive in-stock product
    most_expensive = max(in_stock, key=lambda p: p['price'])
    print(f"\nMost expensive: {most_expensive['name']} (${most_expensive['price']})")
    
    # Sort by price (low to high)
    by_price = sorted(in_stock, key=lambda p: p['price'])
    print("\nSorted by price:")
    for p in by_price:
        print(f"  {p['name']}: ${p['price']}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Lambda Closures
# ============================================================

def lambda_closures():
    """
    Understand lambda closures and variable capture.
    
    TODO: Learn closure behavior
    """
    print("--- Bonus Challenge: Lambda Closures ---")
    
    # Closure example
    def make_multiplier(n):
        return lambda x: x * n
    
    times_2 = make_multiplier(2)
    times_5 = make_multiplier(5)
    
    print(f"times_2(10) = {times_2(10)}")
    print(f"times_5(10) = {times_5(10)}")
    
    # Common closure pitfall
    print("\n⚠️  Common pitfall with loops:")
    
    # ❌ WRONG: All lambdas capture same variable
    functions_wrong = []
    for i in range(3):
        functions_wrong.append(lambda x: x + i)
    
    print("Wrong way (all use final i=2):")
    for f in functions_wrong:
        print(f"  f(10) = {f(10)}")
    
    # ✅ CORRECT: Use default argument
    functions_correct = []
    for i in range(3):
        functions_correct.append(lambda x, i=i: x + i)
    
    print("\nCorrect way (each captures its own i):")
    for idx, f in enumerate(functions_correct):
        print(f"  f(10) with i={idx}: {f(10)}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Lambda Functions:
    - Creation: O(1)
    - Execution: Depends on expression
    - No overhead vs def for execution
    - Slightly faster to create than def
    
    operator Module:
    - itemgetter/attrgetter: O(1) access
    - Faster than equivalent lambda
    - Implemented in C
    
    Benefits:
    - Concise for simple operations
    - Good for one-time use
    - Works well with functional tools
    - No need to name simple functions
    
    Drawbacks:
    - Limited to single expression
    - No docstrings
    - Harder to debug (no name)
    - Can reduce readability if complex
    
    Use Cases:
    - key functions for sorted/max/min
    - Simple transformations with map/filter
    - Event handlers (GUI)
    - Callbacks
    - Functional composition
    
    When NOT to Use:
    - Complex logic (use def)
    - Multiple statements needed
    - Reused many times (use def)
    - Needs documentation
    - Side effects required
    
    Best Practices:
    - Keep lambdas simple (1 line, obvious)
    - Use operator module when possible
    - Prefer def for anything complex
    - Don't assign lambda to variable
    - Avoid side effects in lambdas
    
    Security Considerations:
    - Don't eval() user input to create lambdas
    - Validate data before lambda processing
    - Be careful with closures and mutable state
    - Consider using operator module for safety
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 4, Day 2: Lambda Functions")
    print("=" * 60)
    print()
    
    lambda_basics()
    lambda_vs_def()
    lambda_with_builtins()
    lambda_with_data_structures()
    lambda_antipatterns()
    lambda_alternatives()
    data_transformation()
    lambda_closures()
    
    print("=" * 60)
    print("✅ Day 2 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Lambda: single expression anonymous functions")
    print("2. Use for simple, one-time operations")
    print("3. Prefer def for complex logic")
    print("4. operator module often better than simple lambdas")

