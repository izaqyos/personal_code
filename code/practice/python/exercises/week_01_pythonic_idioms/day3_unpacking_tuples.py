"""
Week 1, Day 3: Unpacking and Tuple Swapping Idioms

Learning Objectives:
- Master tuple unpacking and extended unpacking (*)
- Learn multiple assignment patterns
- Understand when to use tuples vs lists
- Practice destructuring in function returns and loops

Time: 10-15 minutes
"""

import sys
from typing import Tuple, List

# ============================================================
# EXERCISE 1: Basic Unpacking
# ============================================================

def basic_unpacking():
    """
    Practice fundamental unpacking patterns.
    
    TODO: Complete the unpacking exercises
    """
    print("--- Exercise 1: Basic Unpacking ---")
    
    # 1. Simple tuple unpacking
    coordinates = (10, 20, 30)
    # TODO: Unpack into x, y, z
    # x, y, z = ...
    print(f"Coordinates: x={coordinates[0]}, y={coordinates[1]}, z={coordinates[2]}")
    
    # 2. Swapping variables (Pythonic way)
    a, b = 5, 10
    print(f"Before swap: a={a}, b={b}")
    # TODO: Swap a and b in one line without temp variable
    # a, b = ...
    print(f"After swap: a={a}, b={b}")
    
    # 3. Unpacking from function return
    def get_user_info():
        return "Alice", 30, "alice@example.com"
    
    # TODO: Unpack into name, age, email
    # name, age, email = ...
    name, age, email = get_user_info()
    print(f"User: {name}, {age}, {email}")
    
    # 4. Unpacking in loops
    users = [("Bob", 25), ("Charlie", 35), ("Diana", 28)]
    print("Users:")
    for user in users:
        # TODO: Unpack directly in the loop
        print(f"  {user[0]} is {user[1]} years old")
    
    print()

# ============================================================
# EXERCISE 2: Extended Unpacking with *
# ============================================================

def extended_unpacking():
    """
    Master the * operator for extended unpacking.
    
    TODO: Practice various * unpacking patterns
    """
    print("--- Exercise 2: Extended Unpacking with * ---")
    
    # 1. Capture rest of items
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # TODO: Get first, second, and rest
    # first, second, *rest = ...
    first, second, rest = numbers[0], numbers[1], numbers[2:]
    print(f"First: {first}, Second: {second}, Rest: {rest}")
    
    # 2. Capture middle items
    # TODO: Get first, last, and middle
    # first, *middle, last = ...
    first, middle, last = numbers[0], numbers[1:-1], numbers[-1]
    print(f"First: {first}, Middle: {middle}, Last: {last}")
    
    # 3. Ignore unwanted items with _
    person = ("Alice", 30, "Engineer", "New York", "USA")
    # TODO: Get only name and profession, ignore rest
    # name, _, profession, *_ = ...
    name, profession = person[0], person[2]
    print(f"Name: {name}, Profession: {profession}")
    
    # 4. Unpacking in function arguments
    def process_scores(first, second, *others):
        print(f"  Top score: {first}")
        print(f"  Second: {second}")
        print(f"  Others: {others}")
        return sum([first, second] + list(others)) / (2 + len(others))
    
    scores = [95, 87, 82, 78, 91]
    # TODO: Call process_scores with unpacked scores
    avg = None  # process_scores(...)
    print(f"Average: {avg}")
    
    print()

# ============================================================
# EXERCISE 3: Nested Unpacking
# ============================================================

def nested_unpacking():
    """
    Unpack nested structures in a single statement.
    
    TODO: Practice nested unpacking patterns
    """
    print("--- Exercise 3: Nested Unpacking ---")
    
    # 1. Nested tuples
    person = ("Alice", (30, "Engineer"), ("New York", "USA"))
    # TODO: Unpack all in one line
    # name, (age, job), (city, country) = ...
    name = person[0]
    age, job = person[1]
    city, country = person[2]
    print(f"{name}, {age}, {job} from {city}, {country}")
    
    # 2. Unpacking from nested lists
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # TODO: Get first row and unpack it
    # first_row = ...
    # a, b, c = first_row
    first_row = matrix[0]
    print(f"First row: {first_row}")
    
    # 3. Complex nested structure
    data = [
        ("Alice", {"age": 30, "city": "NYC"}),
        ("Bob", {"age": 25, "city": "LA"}),
    ]
    
    for person in data:
        # TODO: Unpack name and info dict
        name, info = person
        print(f"  {name}: {info['age']} years old, lives in {info['city']}")
    
    print()

# ============================================================
# EXERCISE 4: Real-World Scenario - CSV Processing
# ============================================================

def process_csv_data():
    """
    Process CSV-like data using unpacking patterns.
    
    Scenario: Parse employee records and extract specific fields
    
    TODO: Use unpacking to process records efficiently
    """
    print("--- Exercise 4: CSV Processing ---")
    
    # CSV format: id, name, department, salary, years, city
    employees = [
        "001,Alice,Engineering,95000,5,NYC",
        "002,Bob,Marketing,75000,3,LA",
        "003,Charlie,Engineering,105000,8,SF",
        "004,Diana,Sales,85000,4,Chicago",
        "005,Eve,Engineering,92000,6,Boston",
    ]
    
    # Task 1: Parse and extract name, department, salary
    print("Employee Summary:")
    for record in employees:
        fields = record.split(',')
        # TODO: Unpack only needed fields, ignore others
        # emp_id, name, dept, salary, *_ = fields
        print(f"  {fields[1]}: {fields[2]} - ${fields[3]}")
    
    # Task 2: Find engineering employees with salary > 90k
    print("\nHigh-earning Engineers:")
    for record in employees:
        fields = record.split(',')
        # TODO: Unpack and filter
        emp_id, name, dept, salary, years, city = fields
        if dept == "Engineering" and int(salary) > 90000:
            print(f"  {name} (${salary}) - {years} years in {city}")
    
    # Task 3: Calculate average salary by department
    from collections import defaultdict
    dept_salaries = defaultdict(list)
    
    for record in employees:
        # TODO: Unpack and group by department
        fields = record.split(',')
        _, _, dept, salary, *_ = fields
        dept_salaries[dept].append(int(salary))
    
    print("\nAverage Salary by Department:")
    for dept, salaries in dept_salaries.items():
        avg = sum(salaries) / len(salaries)
        print(f"  {dept}: ${avg:,.0f}")
    
    print()

# ============================================================
# EXERCISE 5: Function Signatures with Unpacking
# ============================================================

def function_unpacking_patterns():
    """
    Use unpacking in function definitions and calls.
    
    TODO: Practice *args and **kwargs patterns
    """
    print("--- Exercise 5: Function Unpacking ---")
    
    # Pattern 1: *args for variable positional arguments
    def calculate_total(*prices):
        """Sum all prices"""
        # TODO: Calculate total
        return sum(prices)
    
    # TODO: Call with unpacked list
    items = [10.99, 5.49, 3.99, 12.50]
    total = None  # calculate_total(...)
    print(f"Total: ${total}")
    
    # Pattern 2: **kwargs for variable keyword arguments
    def create_user(**user_info):
        """Create user with arbitrary fields"""
        print(f"  Creating user: {user_info}")
        return user_info
    
    # TODO: Call with unpacked dict
    user_data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
    user = None  # create_user(...)
    
    # Pattern 3: Combining positional, *args, and **kwargs
    def api_request(endpoint, method="GET", *params, **headers):
        print(f"  {method} {endpoint}")
        print(f"  Params: {params}")
        print(f"  Headers: {headers}")
    
    # TODO: Call with various argument types
    # api_request("/users", "POST", "param1", "param2", auth="token", content_type="json")
    
    print()

# ============================================================
# EXERCISE 6: Tuple vs List - When to Use Which
# ============================================================

def tuple_vs_list():
    """
    Understand when to use tuples vs lists.
    
    Tuples:
    - Immutable (hashable, can be dict keys)
    - Slightly faster than lists
    - Used for heterogeneous data (records)
    - Unpacking works naturally
    
    Lists:
    - Mutable
    - Used for homogeneous data (collections)
    - More methods available
    """
    print("--- Exercise 6: Tuple vs List ---")
    
    # Good use of tuple: Representing a fixed record
    person = ("Alice", 30, "Engineer")  # name, age, job
    
    # Good use of list: Collection of similar items
    scores = [95, 87, 92, 88, 91]
    
    # Tuples as dict keys (lists can't be keys)
    locations = {
        (40.7128, -74.0060): "New York",
        (34.0522, -118.2437): "Los Angeles",
    }
    
    print(f"Person: {person}")
    print(f"Scores: {scores}")
    print(f"Locations: {locations}")
    
    # Memory comparison
    import sys
    tuple_data = (1, 2, 3, 4, 5)
    list_data = [1, 2, 3, 4, 5]
    print(f"\nMemory: tuple={sys.getsizeof(tuple_data)}B, list={sys.getsizeof(list_data)}B")
    
    print()

# ============================================================
# BONUS CHALLENGE
# ============================================================

def parallel_assignment_challenge():
    """
    Implement advanced unpacking patterns.
    
    TODO: Solve these challenges using unpacking
    """
    print("--- Bonus Challenge: Advanced Unpacking ---")
    
    # Challenge 1: Rotate a list left by n positions using unpacking
    def rotate_left(lst: List, n: int) -> List:
        """Rotate list left by n positions"""
        # TODO: Use unpacking to rotate
        # Hint: lst[n:] + lst[:n] can be done with unpacking
        return lst[n:] + lst[:n]
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    rotated = rotate_left(numbers, 3)
    print(f"Rotated: {rotated}")
    
    # Challenge 2: Merge and unpack multiple iterables
    def merge_alternating(*iterables):
        """Merge iterables by alternating elements"""
        # TODO: Use zip and unpacking
        # Hint: zip(*iterables) transposes
        return [item for sublist in zip(*iterables) for item in sublist]
    
    list1 = [1, 2, 3]
    list2 = ['a', 'b', 'c']
    list3 = [10, 20, 30]
    merged = merge_alternating(list1, list2, list3)
    print(f"Merged alternating: {merged}")
    
    # Challenge 3: Flatten nested structure using unpacking
    nested = [[1, 2], [3, 4], [5, 6]]
    # TODO: Flatten in one line using unpacking
    flattened = [item for sublist in nested for item in sublist]
    print(f"Flattened: {flattened}")
    
    print()

# ============================================================
# PERFORMANCE ANALYSIS
# ============================================================

def performance_analysis():
    """
    Compare performance of different unpacking patterns.
    """
    import time
    
    print("--- Performance Analysis ---")
    
    data = list(range(1000000))
    
    # Test 1: Index access
    start = time.perf_counter()
    for _ in range(100):
        a = data[0]
        b = data[1]
        c = data[2]
    time1 = time.perf_counter() - start
    
    # Test 2: Unpacking
    start = time.perf_counter()
    for _ in range(100):
        a, b, c, *rest = data
    time2 = time.perf_counter() - start
    
    # Test 3: Slice
    start = time.perf_counter()
    for _ in range(100):
        first_three = data[:3]
        a, b, c = first_three
    time3 = time.perf_counter() - start
    
    print(f"Index access: {time1:.6f}s")
    print(f"Unpacking:    {time2:.6f}s")
    print(f"Slice:        {time3:.6f}s")
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Basic Unpacking:
    - Time: O(n) where n is number of elements to unpack
    - Space: O(1) - just creates references
    
    Extended Unpacking (*rest):
    - Time: O(n) where n is size of rest
    - Space: O(n) - creates new list for rest
    
    Tuple vs List:
    - Tuple creation: Slightly faster (immutable)
    - List creation: Slightly slower (mutable overhead)
    - Both have O(1) access time
    
    Security Considerations:
    - Unpacking unknown-length sequences can cause memory issues
    - Validate input size before unpacking from external sources
    - Use * carefully with large datasets
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 1, Day 3: Unpacking and Tuple Swapping Idioms")
    print("=" * 60)
    print()
    
    basic_unpacking()
    extended_unpacking()
    nested_unpacking()
    process_csv_data()
    function_unpacking_patterns()
    tuple_vs_list()
    parallel_assignment_challenge()
    performance_analysis()
    
    print("=" * 60)
    print("✅ Day 3 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Unpacking makes code more readable and Pythonic")
    print("2. Use * for flexible unpacking of variable-length sequences")
    print("3. Tuples are for heterogeneous records, lists for collections")
    print("4. Unpacking works in assignments, loops, and function calls")

