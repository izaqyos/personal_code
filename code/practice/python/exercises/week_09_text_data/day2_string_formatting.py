"""
Week 9, Day 2: String Formatting & Templates

Learning Objectives:
- Master f-strings and format()
- Learn string.Template
- Practice formatting options
- Understand locale formatting
- Build formatted output

Time: 10-15 minutes
"""

import string
from datetime import datetime
from decimal import Decimal

# ============================================================
# EXERCISE 1: F-Strings (Python 3.6+)
# ============================================================

def fstring_basics():
    """
    Master f-string formatting.
    
    F-strings: Fast, readable string interpolation
    """
    print("--- Exercise 1: F-Strings ---")
    
    name = "Alice"
    age = 30
    
    # Basic interpolation
    print(f"Name: {name}, Age: {age}")
    
    # Expressions
    print(f"Next year: {age + 1}")
    print(f"Uppercase: {name.upper()}")
    
    # Formatting specifiers
    pi = 3.14159265359
    print(f"Pi: {pi:.2f}")  # 2 decimal places
    print(f"Pi: {pi:.4f}")  # 4 decimal places
    
    # Width and alignment
    print(f"Left: {name:<10}|")
    print(f"Right: {name:>10}|")
    print(f"Center: {name:^10}|")
    
    # Numbers
    num = 1234567
    print(f"Comma: {num:,}")
    print(f"Binary: {num:b}")
    print(f"Hex: {num:x}")
    
    print()

# ============================================================
# EXERCISE 2: Format Method
# ============================================================

def format_method():
    """
    Learn str.format() method.
    
    TODO: Positional and keyword arguments
    """
    print("--- Exercise 2: Format Method ---")
    
    # Positional arguments
    result = "Hello, {}! You are {} years old.".format("Bob", 25)
    print(result)
    
    # Indexed arguments
    result2 = "{0} {1} {0}".format("Python", "rocks")
    print(result2)
    
    # Keyword arguments
    result3 = "{name} is {age} years old".format(name="Carol", age=28)
    print(result3)
    
    # Dictionary unpacking
    person = {"name": "Dave", "age": 32}
    result4 = "{name} is {age} years old".format(**person)
    print(result4)
    
    # Formatting options
    print("\nFormatting options:")
    print("{:>10}".format("right"))
    print("{:<10}".format("left"))
    print("{:^10}".format("center"))
    print("{:*^10}".format("pad"))
    
    # Numbers
    print("\nNumbers:")
    print("{:,.2f}".format(1234567.89))
    print("{:e}".format(1234567.89))
    print("{:%}".format(0.25))
    
    print()

# ============================================================
# EXERCISE 3: String Template
# ============================================================

def string_template():
    """
    Use string.Template for safe substitution.
    
    TODO: Safe string substitution
    """
    print("--- Exercise 3: String Template ---")
    
    # Basic template
    template = string.Template("Hello, $name!")
    result = template.substitute(name="Eve")
    print(result)
    
    # Multiple substitutions
    template2 = string.Template("$greeting, $name! Welcome to $place.")
    result2 = template2.substitute(
        greeting="Hi",
        name="Frank",
        place="Python"
    )
    print(result2)
    
    # Safe substitute (no error on missing)
    template3 = string.Template("Hello, $name! You have $count messages.")
    result3 = template3.safe_substitute(name="Grace")
    print(result3)  # $count remains
    
    # Use case: User-provided templates
    print("\n💡 Use Template for user-provided strings (safer)")
    print("💡 Use f-strings for code-controlled strings (faster)")
    
    print()

# ============================================================
# EXERCISE 4: Advanced Formatting
# ============================================================

def advanced_formatting():
    """
    Advanced formatting techniques.
    
    TODO: Nested, conversion, custom
    """
    print("--- Exercise 4: Advanced Formatting ---")
    
    # Nested formatting
    width = 10
    value = "test"
    print(f"{value:>{width}}")
    
    # Conversion flags
    class Person:
        def __init__(self, name):
            self.name = name
        def __repr__(self):
            return f"Person('{self.name}')"
        def __str__(self):
            return self.name
    
    p = Person("Helen")
    print(f"str: {p!s}")
    print(f"repr: {p!r}")
    
    # Date formatting
    now = datetime.now()
    print(f"\nDate: {now:%Y-%m-%d}")
    print(f"Time: {now:%H:%M:%S}")
    print(f"Full: {now:%Y-%m-%d %H:%M:%S}")
    
    # Decimal formatting
    amount = Decimal("1234.5678")
    print(f"\nDecimal: {amount:.2f}")
    
    # Padding with zeros
    num = 42
    print(f"\nPadded: {num:05d}")
    
    print()

# ============================================================
# EXERCISE 5: Table Formatting
# ============================================================

def table_formatting():
    """
    Format data as tables.
    
    TODO: Aligned columns
    """
    print("--- Exercise 5: Table Formatting ---")
    
    # Simple table
    data = [
        ("Name", "Age", "Score"),
        ("Alice", 25, 95.5),
        ("Bob", 30, 87.3),
        ("Carol", 28, 92.1),
    ]
    
    print("Simple table:")
    for row in data:
        print(f"{row[0]:<10} {row[1]:>5} {row[2]:>7.1f}")
    
    # Dynamic column widths
    print("\nDynamic widths:")
    col_widths = [max(len(str(row[i])) for row in data) for i in range(3)]
    
    for row in data:
        print(f"{str(row[0]):<{col_widths[0]}} "
              f"{str(row[1]):>{col_widths[1]}} "
              f"{str(row[2]):>{col_widths[2]}}")
    
    # With separators
    print("\nWith separators:")
    header = data[0]
    print(f"{header[0]:<10} | {header[1]:>5} | {header[2]:>7}")
    print("-" * 30)
    for row in data[1:]:
        print(f"{row[0]:<10} | {row[1]:>5} | {row[2]:>7.1f}")
    
    print()

# ============================================================
# EXERCISE 6: Multiline Strings
# ============================================================

def multiline_strings():
    """
    Format multiline strings.
    
    TODO: Triple quotes, dedent
    """
    print("--- Exercise 6: Multiline Strings ---")
    
    # Triple quotes
    text = """
    This is a multiline string.
    It can span multiple lines.
    Indentation is preserved.
    """
    print("Triple quotes:")
    print(text)
    
    # With f-string
    name = "Ian"
    age = 35
    message = f"""
    Name: {name}
    Age: {age}
    Status: Active
    """
    print("F-string multiline:")
    print(message)
    
    # Dedent for cleaner code
    from textwrap import dedent
    
    text2 = dedent("""
        This text is dedented.
        All common leading whitespace
        is removed.
    """)
    print("Dedented:")
    print(text2)
    
    print()

# ============================================================
# EXERCISE 7: Real-World - Report Generator
# ============================================================

def report_generator():
    """
    Generate formatted reports.
    
    TODO: Complex formatting
    """
    print("--- Exercise 7: Report Generator ---")
    
    # Sales report data
    sales = [
        {"product": "Widget A", "qty": 150, "price": 29.99},
        {"product": "Widget B", "qty": 200, "price": 39.99},
        {"product": "Widget C", "qty": 75, "price": 49.99},
    ]
    
    # Generate report
    print("=" * 60)
    print(f"{'SALES REPORT':^60}")
    print(f"{'Generated: ' + datetime.now().strftime('%Y-%m-%d %H:%M'):^60}")
    print("=" * 60)
    print()
    
    print(f"{'Product':<20} {'Quantity':>10} {'Price':>10} {'Total':>15}")
    print("-" * 60)
    
    grand_total = 0
    for item in sales:
        total = item['qty'] * item['price']
        grand_total += total
        print(f"{item['product']:<20} {item['qty']:>10} "
              f"${item['price']:>9.2f} ${total:>14.2f}")
    
    print("-" * 60)
    print(f"{'GRAND TOTAL':>45} ${grand_total:>14.2f}")
    print("=" * 60)
    
    print()

# ============================================================
# FORMATTING CHEAT SHEET
# ============================================================

def formatting_cheatsheet():
    """
    Quick reference for formatting.
    """
    print("--- Formatting Cheat Sheet ---")
    
    print("\nAlignment:")
    print("  {:<10}  Left align")
    print("  {:>10}  Right align")
    print("  {:^10}  Center align")
    print("  {:*^10} Center with padding")
    
    print("\nNumbers:")
    print("  {:d}     Integer")
    print("  {:f}     Float")
    print("  {:.2f}   2 decimal places")
    print("  {:,}     Thousands separator")
    print("  {:%}     Percentage")
    print("  {:e}     Scientific notation")
    print("  {:b}     Binary")
    print("  {:x}     Hexadecimal")
    
    print("\nDates:")
    print("  {:%Y-%m-%d}      Date")
    print("  {:%H:%M:%S}      Time")
    print("  {:%Y-%m-%d %H:%M} DateTime")
    
    print("\nConversion:")
    print("  {!s}     str()")
    print("  {!r}     repr()")
    print("  {!a}     ascii()")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    String Formatting Complexity:
    
    Time Complexity:
    - F-strings: O(n) where n is result length
    - format(): O(n) similar to f-strings
    - Template: O(n) for substitution
    
    Space Complexity:
    - O(n) for result string
    - Strings are immutable
    
    Performance:
    - F-strings: Fastest (compiled)
    - format(): Slightly slower
    - Template: Slower but safer
    - % formatting: Legacy, avoid
    
    Best Practices:
    - Use f-strings for code
    - Use Template for user input
    - Compile templates if reused
    - Avoid concatenation in loops
    
    Security:
    - Validate user input
    - Use Template for user strings
    - Avoid eval() with strings
    - Sanitize format specifiers
    
    When to Use:
    - F-strings: Fast, readable, code-controlled
    - format(): Compatibility, dynamic
    - Template: User-provided, safe
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 9, Day 2: String Formatting & Templates")
    print("=" * 60)
    print()
    
    fstring_basics()
    format_method()
    string_template()
    advanced_formatting()
    table_formatting()
    multiline_strings()
    report_generator()
    formatting_cheatsheet()
    
    print("=" * 60)
    print("✅ Day 2 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. F-strings: Fast and readable")
    print("2. format(): Dynamic and flexible")
    print("3. Template: Safe for user input")
    print("4. Choose based on use case")

