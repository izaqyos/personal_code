"""
Week 1, Day 5: EAFP vs LBYL - Exception Handling Patterns

Learning Objectives:
- Understand EAFP (Easier to Ask for Forgiveness than Permission)
- Understand LBYL (Look Before You Leap)
- Learn when to use each approach
- Practice Pythonic exception handling

EAFP: Try the operation, handle exceptions if they occur
LBYL: Check conditions before attempting the operation

Time: 10-15 minutes
"""

import os
import time
from typing import Dict, Any, Optional

# ============================================================
# EXERCISE 1: EAFP vs LBYL Comparison
# ============================================================

def compare_approaches():
    """
    Compare EAFP and LBYL approaches for the same task.
    
    Task: Access a dictionary key safely
    """
    print("--- Exercise 1: EAFP vs LBYL Comparison ---")
    
    data = {"name": "Alice", "age": 30}
    
    # LBYL Approach: Look Before You Leap
    print("LBYL Approach:")
    if "email" in data:
        email = data["email"]
        print(f"  Email: {email}")
    else:
        print("  Email not found")
    
    # EAFP Approach: Easier to Ask for Forgiveness than Permission
    print("\nEAFP Approach:")
    try:
        email = data["email"]
        print(f"  Email: {email}")
    except KeyError:
        print("  Email not found")
    
    # Pythonic alternative: dict.get()
    print("\nPythonic Alternative:")
    email = data.get("email", "Not found")
    print(f"  Email: {email}")
    
    print()

# ============================================================
# EXERCISE 2: File Operations - EAFP vs LBYL
# ============================================================

def file_operations_comparison():
    """
    Compare approaches for file operations.
    
    TODO: Implement both LBYL and EAFP approaches
    """
    print("--- Exercise 2: File Operations ---")
    
    filename = "test_data.txt"
    
    # LBYL: Check if file exists before opening
    print("LBYL Approach:")
    # TODO: Check if file exists, then open
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.read()
            print(f"  File content: {content[:50]}...")
    else:
        print(f"  File {filename} does not exist")
    
    # EAFP: Try to open, handle exception
    print("\nEAFP Approach (Pythonic):")
    # TODO: Try to open file, catch FileNotFoundError
    try:
        with open(filename, 'r') as f:
            content = f.read()
            print(f"  File content: {content[:50]}...")
    except FileNotFoundError:
        print(f"  File {filename} does not exist")
    
    # Why EAFP is better here:
    # 1. Race condition: file could be deleted between check and open
    # 2. Handles other file errors (permissions, etc.)
    # 3. More concise and readable
    
    print()

# ============================================================
# EXERCISE 3: Type Checking - Duck Typing
# ============================================================

def duck_typing_examples():
    """
    Demonstrate duck typing with EAFP.
    
    "If it walks like a duck and quacks like a duck, it's a duck"
    
    TODO: Implement functions using duck typing
    """
    print("--- Exercise 3: Duck Typing with EAFP ---")
    
    # LBYL: Check type explicitly
    def process_sequence_lbyl(seq):
        """Process a sequence - LBYL approach"""
        if isinstance(seq, (list, tuple)):
            return [x * 2 for x in seq]
        else:
            raise TypeError("Expected list or tuple")
    
    # EAFP: Try to iterate, let it fail naturally
    def process_sequence_eafp(seq):
        """Process a sequence - EAFP approach (Pythonic)"""
        # TODO: Just try to iterate and process
        try:
            return [x * 2 for x in seq]
        except TypeError:
            raise TypeError("Object is not iterable")
    
    # Test with various types
    test_data = [
        [1, 2, 3],
        (4, 5, 6),
        range(7, 10),
        "abc",  # Strings are iterable too!
    ]
    
    for data in test_data:
        try:
            result = process_sequence_eafp(data)
            print(f"  {type(data).__name__}: {result}")
        except TypeError as e:
            print(f"  {type(data).__name__}: {e}")
    
    print()

# ============================================================
# EXERCISE 4: Attribute Access
# ============================================================

def attribute_access_patterns():
    """
    Compare approaches for accessing object attributes.
    
    TODO: Implement both approaches
    """
    print("--- Exercise 4: Attribute Access ---")
    
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
    
    person = Person("Alice", 30)
    
    # LBYL: Check if attribute exists
    print("LBYL Approach:")
    # TODO: Use hasattr() to check
    if hasattr(person, "email"):
        print(f"  Email: {person.email}")
    else:
        print("  Email attribute not found")
    
    # EAFP: Try to access, handle AttributeError
    print("\nEAFP Approach (Pythonic):")
    # TODO: Try to access attribute
    try:
        print(f"  Email: {person.email}")
    except AttributeError:
        print("  Email attribute not found")
    
    # Pythonic alternative: getattr()
    print("\nUsing getattr():")
    email = getattr(person, "email", "no-email@example.com")
    print(f"  Email: {email}")
    
    print()

# ============================================================
# EXERCISE 5: Real-World Scenario - API Response Parsing
# ============================================================

def parse_api_response():
    """
    Parse API responses with nested data structures.
    
    TODO: Implement robust parsing using EAFP
    """
    print("--- Exercise 5: API Response Parsing ---")
    
    # Simulated API responses with varying structures
    responses = [
        {
            "user": {
                "name": "Alice",
                "profile": {
                    "email": "alice@example.com",
                    "age": 30
                }
            }
        },
        {
            "user": {
                "name": "Bob"
                # Missing profile
            }
        },
        {
            "user": {
                "name": "Charlie",
                "profile": {
                    # Missing email
                    "age": 25
                }
            }
        },
    ]
    
    # LBYL Approach: Nested checks
    print("LBYL Approach:")
    for response in responses:
        # TODO: Check each level before accessing
        if "user" in response:
            if "profile" in response["user"]:
                if "email" in response["user"]["profile"]:
                    email = response["user"]["profile"]["email"]
                    print(f"  {response['user']['name']}: {email}")
                else:
                    print(f"  {response['user']['name']}: No email")
            else:
                print(f"  {response['user']['name']}: No profile")
    
    # EAFP Approach: Try to access, handle exceptions
    print("\nEAFP Approach (Pythonic):")
    for response in responses:
        # TODO: Try to access nested data
        try:
            name = response["user"]["name"]
            email = response["user"]["profile"]["email"]
            print(f"  {name}: {email}")
        except KeyError:
            name = response.get("user", {}).get("name", "Unknown")
            print(f"  {name}: No email")
    
    print()

# ============================================================
# EXERCISE 6: Performance Comparison
# ============================================================

def performance_comparison():
    """
    Compare performance of EAFP vs LBYL.
    
    Result: EAFP is faster when exceptions are rare
    """
    print("--- Exercise 6: Performance Comparison ---")
    
    data = {str(i): i for i in range(1000)}
    
    # Scenario 1: Key exists (common case)
    print("Scenario 1: Key exists (90% of the time)")
    
    # LBYL
    start = time.perf_counter()
    for _ in range(10000):
        if "500" in data:
            value = data["500"]
    lbyl_time = time.perf_counter() - start
    
    # EAFP
    start = time.perf_counter()
    for _ in range(10000):
        try:
            value = data["500"]
        except KeyError:
            pass
    eafp_time = time.perf_counter() - start
    
    print(f"  LBYL: {lbyl_time:.6f}s")
    print(f"  EAFP: {eafp_time:.6f}s")
    print(f"  EAFP is {lbyl_time/eafp_time:.2f}x faster")
    
    # Scenario 2: Key doesn't exist (exception case)
    print("\nScenario 2: Key doesn't exist (exception thrown)")
    
    # LBYL
    start = time.perf_counter()
    for _ in range(10000):
        if "nonexistent" in data:
            value = data["nonexistent"]
    lbyl_time = time.perf_counter() - start
    
    # EAFP
    start = time.perf_counter()
    for _ in range(10000):
        try:
            value = data["nonexistent"]
        except KeyError:
            pass
    eafp_time = time.perf_counter() - start
    
    print(f"  LBYL: {lbyl_time:.6f}s")
    print(f"  EAFP: {eafp_time:.6f}s")
    print(f"  LBYL is {eafp_time/lbyl_time:.2f}x faster (when exceptions are common)")
    
    print()

# ============================================================
# EXERCISE 7: When to Use Each Approach
# ============================================================

def when_to_use_each():
    """
    Guidelines for choosing between EAFP and LBYL.
    """
    print("--- Exercise 7: When to Use Each ---")
    
    print("Use EAFP when:")
    print("  ✓ Exceptions are rare (happy path is common)")
    print("  ✓ Race conditions are possible (file operations)")
    print("  ✓ You want duck typing (more flexible)")
    print("  ✓ The check is as expensive as the operation")
    
    print("\nUse LBYL when:")
    print("  ✓ Exceptions are expensive and common")
    print("  ✓ You need to avoid exceptions for control flow")
    print("  ✓ Pre-validation is required (user input)")
    print("  ✓ The check is much cheaper than the operation")
    
    print("\nPython Philosophy:")
    print("  'It's easier to ask for forgiveness than permission.'")
    print("  - Grace Hopper")
    
    print()

# ============================================================
# BONUS CHALLENGE
# ============================================================

def safe_chain_access(data: Dict, *keys, default=None):
    """
    Safely access nested dictionary keys using EAFP.
    
    TODO: Implement safe nested access
    
    Example:
        data = {"a": {"b": {"c": 42}}}
        safe_chain_access(data, "a", "b", "c") -> 42
        safe_chain_access(data, "a", "x", "y", default=0) -> 0
    """
    # TODO: Implement using EAFP
    try:
        result = data
        for key in keys:
            result = result[key]
        return result
    except (KeyError, TypeError):
        return default

def test_safe_chain_access():
    """Test the safe chain access function"""
    print("--- Bonus Challenge: Safe Chain Access ---")
    
    data = {
        "user": {
            "profile": {
                "email": "alice@example.com",
                "settings": {
                    "theme": "dark"
                }
            }
        }
    }
    
    # Test successful access
    email = safe_chain_access(data, "user", "profile", "email")
    print(f"Email: {email}")
    
    # Test missing key with default
    phone = safe_chain_access(data, "user", "profile", "phone", default="N/A")
    print(f"Phone: {phone}")
    
    # Test deep missing path
    theme = safe_chain_access(data, "user", "profile", "settings", "theme")
    print(f"Theme: {theme}")
    
    missing = safe_chain_access(data, "user", "billing", "card", default="No card")
    print(f"Card: {missing}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    EAFP:
    - Normal case: O(1) for dict access
    - Exception case: O(1) but with higher constant factor
    - Exception overhead: ~10-100x slower than normal operation
    
    LBYL:
    - Check + access: 2 * O(1) = O(1)
    - Always performs two operations
    
    Rule of Thumb:
    - If exceptions are rare (<1%), EAFP is faster
    - If exceptions are common (>10%), LBYL may be faster
    - For most Python code, EAFP is preferred (more Pythonic)
    
    Security Considerations:
    - EAFP prevents race conditions (TOCTOU vulnerabilities)
    - Don't use exceptions for control flow in hot loops
    - Validate user input before processing (LBYL for validation)
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 1, Day 5: EAFP vs LBYL")
    print("=" * 60)
    print()
    
    compare_approaches()
    file_operations_comparison()
    duck_typing_examples()
    attribute_access_patterns()
    parse_api_response()
    performance_comparison()
    when_to_use_each()
    test_safe_chain_access()
    
    print("=" * 60)
    print("✅ Day 5 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. EAFP is more Pythonic and handles race conditions")
    print("2. EAFP is faster when exceptions are rare")
    print("3. Use LBYL for validation and when exceptions are common")
    print("4. Duck typing with EAFP makes code more flexible")

