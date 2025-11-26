"""
Week 3, Day 6: namedtuple and typing.NamedTuple

Learning Objectives:
- Master namedtuple for readable data structures
- Learn typing.NamedTuple for type hints
- Understand when to use namedtuple vs dataclass
- Practice immutable record patterns

Time: 10-15 minutes
"""

from collections import namedtuple
from typing import NamedTuple
import sys

# ============================================================
# EXERCISE 1: namedtuple Basics
# ============================================================

def namedtuple_basics():
    """
    Learn basic namedtuple operations.
    
    namedtuple: Factory function for creating tuple subclasses with named fields
    """
    print("--- Exercise 1: namedtuple Basics ---")
    
    # Create namedtuple class
    Point = namedtuple('Point', ['x', 'y'])
    
    # Create instances
    p1 = Point(10, 20)
    p2 = Point(x=30, y=40)
    
    print(f"p1: {p1}")
    print(f"p2: {p2}")
    
    # Access by name
    print(f"\np1.x = {p1.x}")
    print(f"p1.y = {p1.y}")
    
    # Access by index (still a tuple!)
    print(f"\np1[0] = {p1[0]}")
    print(f"p1[1] = {p1[1]}")
    
    # Unpacking
    x, y = p1
    print(f"\nUnpacked: x={x}, y={y}")
    
    # Immutable
    try:
        p1.x = 100
    except AttributeError as e:
        print(f"\nImmutable: {e}")
    
    print()

# ============================================================
# EXERCISE 2: typing.NamedTuple with Type Hints
# ============================================================

def typing_namedtuple():
    """
    Use typing.NamedTuple for type-safe namedtuples.
    
    TODO: Practice with type hints
    """
    print("--- Exercise 2: typing.NamedTuple ---")
    
    # Define with type hints
    class Person(NamedTuple):
        name: str
        age: int
        email: str = "unknown@example.com"  # Default value
    
    # Create instances
    p1 = Person("Alice", 30, "alice@example.com")
    p2 = Person("Bob", 25)  # Uses default email
    
    print(f"p1: {p1}")
    print(f"p2: {p2}")
    
    # Type hints help IDEs and type checkers
    print(f"\np1.name: {p1.name} (type: {type(p1.name).__name__})")
    print(f"p1.age: {p1.age} (type: {type(p1.age).__name__})")
    
    # Access annotations
    print(f"\nAnnotations: {Person.__annotations__}")
    
    print()

# ============================================================
# EXERCISE 3: namedtuple Methods
# ============================================================

def namedtuple_methods():
    """
    Use built-in namedtuple methods.
    
    TODO: Practice _make, _asdict, _replace, _fields
    """
    print("--- Exercise 3: namedtuple Methods ---")
    
    Point = namedtuple('Point', ['x', 'y', 'z'])
    p = Point(1, 2, 3)
    
    print(f"Original: {p}")
    
    # _fields: Get field names
    print(f"\n_fields: {p._fields}")
    
    # _asdict: Convert to dict
    d = p._asdict()
    print(f"\n_asdict(): {d}")
    
    # _make: Create from iterable
    p2 = Point._make([10, 20, 30])
    print(f"\n_make([10, 20, 30]): {p2}")
    
    # _replace: Create new instance with changed values
    p3 = p._replace(x=100)
    print(f"\n_replace(x=100): {p3}")
    print(f"Original unchanged: {p}")
    
    print()

# ============================================================
# EXERCISE 4: Real-World Scenario - Database Records
# ============================================================

class Employee(NamedTuple):
    """
    Employee record with type hints.
    
    TODO: Define employee structure
    """
    id: int
    name: str
    department: str
    salary: float
    years: int
    
    def annual_bonus(self) -> float:
        """Calculate annual bonus"""
        return self.salary * 0.1 * min(self.years, 5)
    
    def is_senior(self) -> bool:
        """Check if employee is senior"""
        return self.years >= 5

def test_employee_records():
    """Test employee records"""
    print("--- Exercise 4: Employee Records ---")
    
    employees = [
        Employee(1, "Alice", "Engineering", 95000, 6),
        Employee(2, "Bob", "Marketing", 75000, 3),
        Employee(3, "Charlie", "Engineering", 105000, 8),
        Employee(4, "Diana", "Sales", 85000, 4),
    ]
    
    print("Employee records:")
    for emp in employees:
        print(f"\n{emp.name} (ID: {emp.id}):")
        print(f"  Department: {emp.department}")
        print(f"  Salary: ${emp.salary:,.0f}")
        print(f"  Years: {emp.years}")
        print(f"  Bonus: ${emp.annual_bonus():,.0f}")
        print(f"  Senior: {emp.is_senior()}")
    
    # Group by department
    from collections import defaultdict
    by_dept = defaultdict(list)
    for emp in employees:
        by_dept[emp.department].append(emp)
    
    print("\nBy department:")
    for dept, emps in by_dept.items():
        avg_salary = sum(e.salary for e in emps) / len(emps)
        print(f"  {dept}: {len(emps)} employees, avg salary: ${avg_salary:,.0f}")
    
    print()

# ============================================================
# EXERCISE 5: Coordinates and Geometry
# ============================================================

class Point2D(NamedTuple):
    """2D point"""
    x: float
    y: float
    
    def distance_from_origin(self) -> float:
        """Calculate distance from origin"""
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def distance_to(self, other: 'Point2D') -> float:
        """Calculate distance to another point"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

class Rectangle(NamedTuple):
    """Rectangle defined by two points"""
    top_left: Point2D
    bottom_right: Point2D
    
    def width(self) -> float:
        """Calculate width"""
        return abs(self.bottom_right.x - self.top_left.x)
    
    def height(self) -> float:
        """Calculate height"""
        return abs(self.bottom_right.y - self.top_left.y)
    
    def area(self) -> float:
        """Calculate area"""
        return self.width() * self.height()

def test_geometry():
    """Test geometry classes"""
    print("--- Exercise 5: Geometry with NamedTuple ---")
    
    # Points
    p1 = Point2D(0, 0)
    p2 = Point2D(3, 4)
    p3 = Point2D(6, 8)
    
    print(f"p1: {p1}")
    print(f"  Distance from origin: {p1.distance_from_origin():.2f}")
    
    print(f"\np2: {p2}")
    print(f"  Distance from origin: {p2.distance_from_origin():.2f}")
    print(f"  Distance to p3: {p2.distance_to(p3):.2f}")
    
    # Rectangle
    rect = Rectangle(Point2D(0, 10), Point2D(5, 0))
    print(f"\nRectangle: {rect}")
    print(f"  Width: {rect.width()}")
    print(f"  Height: {rect.height()}")
    print(f"  Area: {rect.area()}")
    
    print()

# ============================================================
# EXERCISE 6: namedtuple vs dict vs class
# ============================================================

def comparison_with_alternatives():
    """
    Compare namedtuple with dict and regular class.
    
    TODO: Understand trade-offs
    """
    print("--- Exercise 6: namedtuple vs dict vs class ---")
    
    # namedtuple
    Point_nt = namedtuple('Point', ['x', 'y'])
    
    # typing.NamedTuple
    class Point_tnt(NamedTuple):
        x: int
        y: int
    
    # Regular class
    class Point_class:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    # Create instances
    p_nt = Point_nt(10, 20)
    p_tnt = Point_tnt(10, 20)
    p_class = Point_class(10, 20)
    p_dict = {'x': 10, 'y': 20}
    
    # Memory usage
    print("Memory usage:")
    print(f"  namedtuple: {sys.getsizeof(p_nt)} bytes")
    print(f"  typing.NamedTuple: {sys.getsizeof(p_tnt)} bytes")
    print(f"  class: {sys.getsizeof(p_class)} bytes")
    print(f"  dict: {sys.getsizeof(p_dict)} bytes")
    
    # Immutability
    print("\nImmutability:")
    print(f"  namedtuple: Immutable ✓")
    print(f"  typing.NamedTuple: Immutable ✓")
    print(f"  class: Mutable")
    print(f"  dict: Mutable")
    
    # Type hints
    print("\nType hints:")
    print(f"  namedtuple: No")
    print(f"  typing.NamedTuple: Yes ✓")
    print(f"  class: Optional")
    print(f"  dict: No")
    
    # Use cases
    print("\nBest use cases:")
    print("  namedtuple: Simple immutable records (Python < 3.6)")
    print("  typing.NamedTuple: Modern immutable records with types ✓")
    print("  class: Complex objects with methods")
    print("  dict: Dynamic/flexible data")
    
    print()

# ============================================================
# EXERCISE 7: CSV to namedtuple
# ============================================================

def csv_to_namedtuple():
    """
    Parse CSV data into namedtuples.
    
    TODO: Convert CSV rows to typed records
    """
    print("--- Exercise 7: CSV to namedtuple ---")
    
    # CSV data
    csv_data = """name,age,city,salary
Alice,30,NYC,95000
Bob,25,LA,75000
Charlie,35,SF,105000"""
    
    lines = csv_data.strip().split('\n')
    header = lines[0].split(',')
    
    # Create namedtuple class from header
    Person = namedtuple('Person', header)
    
    # Parse rows
    people = []
    for line in lines[1:]:
        values = line.split(',')
        # Convert types
        values[1] = int(values[1])  # age
        values[3] = int(values[3])  # salary
        people.append(Person(*values))
    
    print("Parsed records:")
    for person in people:
        print(f"  {person}")
    
    # Query data
    high_earners = [p for p in people if int(p.salary) > 80000]
    print(f"\nHigh earners (>$80k): {len(high_earners)}")
    for person in high_earners:
        print(f"  {person.name}: ${person.salary}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Nested NamedTuples
# ============================================================

class Address(NamedTuple):
    """Address information"""
    street: str
    city: str
    state: str
    zip_code: str

class Contact(NamedTuple):
    """Contact information"""
    email: str
    phone: str

class Customer(NamedTuple):
    """Customer with nested structures"""
    id: int
    name: str
    address: Address
    contact: Contact
    
    def full_address(self) -> str:
        """Format full address"""
        return f"{self.address.street}, {self.address.city}, {self.address.state} {self.address.zip_code}"

def test_nested_namedtuples():
    """Test nested namedtuples"""
    print("--- Bonus Challenge: Nested NamedTuples ---")
    
    customer = Customer(
        id=1,
        name="Alice Johnson",
        address=Address(
            street="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001"
        ),
        contact=Contact(
            email="alice@example.com",
            phone="555-0123"
        )
    )
    
    print(f"Customer: {customer.name}")
    print(f"  ID: {customer.id}")
    print(f"  Address: {customer.full_address()}")
    print(f"  Email: {customer.contact.email}")
    print(f"  Phone: {customer.contact.phone}")
    
    # Update with _replace
    new_customer = customer._replace(
        contact=customer.contact._replace(phone="555-9999")
    )
    
    print(f"\nUpdated phone:")
    print(f"  Original: {customer.contact.phone}")
    print(f"  New: {new_customer.contact.phone}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    namedtuple Operations:
    - Creation: O(1)
    - Access by name: O(1)
    - Access by index: O(1)
    - _replace: O(n) where n is number of fields
    - _asdict: O(n)
    
    Memory:
    - Same as regular tuple
    - More efficient than dict or class
    - Immutable (can't add fields)
    
    Benefits:
    - Readable code (named fields)
    - Immutable (thread-safe, hashable)
    - Memory efficient
    - Can be used as dict keys
    - Supports all tuple operations
    
    typing.NamedTuple Benefits:
    - Type hints for better IDE support
    - Type checking with mypy
    - More Pythonic syntax
    - Can add methods easily
    - Default values supported
    
    Use Cases:
    - Database records
    - CSV/JSON parsing
    - Function return multiple values
    - Configuration objects
    - Coordinate systems
    - API responses
    
    When NOT to Use:
    - Need mutable objects (use dataclass)
    - Need many methods (use class)
    - Dynamic fields (use dict)
    - Need inheritance (use class)
    
    namedtuple vs dataclass:
    - namedtuple: Immutable, tuple-based, lighter
    - dataclass: Mutable by default, more features
    
    Security Considerations:
    - Immutability prevents accidental modifications
    - Safe to use as dict keys
    - Thread-safe for reading
    - Validate data in __new__ if needed
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 3, Day 6: namedtuple and typing.NamedTuple")
    print("=" * 60)
    print()
    
    namedtuple_basics()
    typing_namedtuple()
    namedtuple_methods()
    test_employee_records()
    test_geometry()
    comparison_with_alternatives()
    csv_to_namedtuple()
    test_nested_namedtuples()
    
    print("=" * 60)
    print("✅ Day 6 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. namedtuple creates immutable records with named fields")
    print("2. typing.NamedTuple adds type hints and better syntax")
    print("3. More readable than tuples, more efficient than dicts")
    print("4. Perfect for simple data structures and return values")

