"""
Week 4, Day 3: functools.partial - Partial Function Application

Learning Objectives:
- Master functools.partial for creating specialized functions
- Learn partial application vs currying
- Understand use cases for partial
- Practice creating function factories
- Compare with lambda closures

Time: 10-15 minutes
"""

from functools import partial
import operator

# ============================================================
# EXERCISE 1: partial Basics
# ============================================================

def partial_basics():
    """
    Learn basic partial function application.
    
    partial(func, *args, **kwargs) - freeze some arguments
    """
    print("--- Exercise 1: partial Basics ---")
    
    # Original function
    def power(base, exponent):
        return base ** exponent
    
    print(f"power(2, 3) = {power(2, 3)}")
    
    # Create specialized functions
    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)
    
    print(f"\nsquare(5) = {square(5)}")
    print(f"cube(5) = {cube(5)}")
    
    # Partial with positional args
    double = partial(operator.mul, 2)
    print(f"\ndouble(7) = {double(7)}")
    
    # Multiple arguments
    def greet(greeting, name, punctuation):
        return f"{greeting}, {name}{punctuation}")
    
    say_hello = partial(greet, "Hello")
    say_hello_excited = partial(greet, "Hello", punctuation="!")
    
    print(f"\nsay_hello('Alice', '.') = {say_hello('Alice', '.')}")
    print(f"say_hello_excited('Bob') = {say_hello_excited('Bob')}")
    
    print()

# ============================================================
# EXERCISE 2: partial vs Lambda
# ============================================================

def partial_vs_lambda():
    """
    Compare partial with lambda closures.
    
    TODO: Understand when to use each
    """
    print("--- Exercise 2: partial vs Lambda ---")
    
    def multiply(x, y):
        return x * y
    
    # Using partial
    double_partial = partial(multiply, 2)
    
    # Using lambda
    double_lambda = lambda y: multiply(2, y)
    
    print(f"double_partial(5) = {double_partial(5)}")
    print(f"double_lambda(5) = {double_lambda(5)}")
    
    # Introspection
    print(f"\npartial function: {double_partial}")
    print(f"  func: {double_partial.func}")
    print(f"  args: {double_partial.args}")
    print(f"  keywords: {double_partial.keywords}")
    
    print(f"\nlambda function: {double_lambda}")
    print(f"  (no introspection available)")
    
    print("\n💡 partial advantages:")
    print("  • Better introspection")
    print("  • Clearer intent")
    print("  • Can inspect frozen arguments")
    print("  • More efficient")
    
    print("\n💡 lambda advantages:")
    print("  • More flexible (any expression)")
    print("  • Can reorder arguments")
    print("  • Familiar to most developers")
    
    print()

# ============================================================
# EXERCISE 3: partial with Built-in Functions
# ============================================================

def partial_with_builtins():
    """
    Use partial with built-in functions.
    
    TODO: Create specialized versions of built-ins
    """
    print("--- Exercise 3: partial with Built-ins ---")
    
    # int with specific base
    binary_to_int = partial(int, base=2)
    hex_to_int = partial(int, base=16)
    
    print(f"binary_to_int('1010') = {binary_to_int('1010')}")
    print(f"hex_to_int('FF') = {hex_to_int('FF')}")
    
    # sorted with fixed key
    words = ['banana', 'Pie', 'Washington', 'book']
    
    sort_by_length = partial(sorted, key=len)
    sort_case_insensitive = partial(sorted, key=str.lower)
    
    print(f"\nWords: {words}")
    print(f"By length: {sort_by_length(words)}")
    print(f"Case-insensitive: {sort_case_insensitive(words)}")
    
    # print with fixed separator
    print_csv = partial(print, sep=', ')
    print_tabs = partial(print, sep='\t')
    
    print("\nprint_csv:")
    print_csv('apple', 'banana', 'cherry')
    
    print("\nprint_tabs:")
    print_tabs('Name', 'Age', 'City')
    print_tabs('Alice', 30, 'NYC')
    
    print()

# ============================================================
# EXERCISE 4: Function Factories with partial
# ============================================================

def function_factories():
    """
    Create function factories using partial.
    
    TODO: Build specialized function generators
    """
    print("--- Exercise 4: Function Factories ---")
    
    # Math operations factory
    def make_math_op(operation):
        """Create math operation functions"""
        ops = {
            'add': partial(operator.add),
            'sub': partial(operator.sub),
            'mul': partial(operator.mul),
            'truediv': partial(operator.truediv),
        }
        return ops.get(operation)
    
    add_5 = partial(operator.add, 5)
    multiply_by_3 = partial(operator.mul, 3)
    
    print(f"add_5(10) = {add_5(10)}")
    print(f"multiply_by_3(7) = {multiply_by_3(7)}")
    
    # Validator factory
    def in_range(value, min_val, max_val):
        """Check if value is in range"""
        return min_val <= value <= max_val
    
    is_percentage = partial(in_range, min_val=0, max_val=100)
    is_adult_age = partial(in_range, min_val=18, max_val=120)
    
    print(f"\nis_percentage(50) = {is_percentage(50)}")
    print(f"is_percentage(150) = {is_percentage(150)}")
    print(f"is_adult_age(25) = {is_adult_age(25)}")
    print(f"is_adult_age(10) = {is_adult_age(10)}")
    
    # String formatter factory
    def format_currency(amount, symbol, decimal_places):
        return f"{symbol}{amount:.{decimal_places}f}"
    
    format_usd = partial(format_currency, symbol='$', decimal_places=2)
    format_eur = partial(format_currency, symbol='€', decimal_places=2)
    format_btc = partial(format_currency, symbol='₿', decimal_places=8)
    
    print(f"\nformat_usd(1234.5) = {format_usd(1234.5)}")
    print(f"format_eur(1234.5) = {format_eur(1234.5)}")
    print(f"format_btc(0.12345678) = {format_btc(0.12345678)}")
    
    print()

# ============================================================
# EXERCISE 5: Real-World Scenario - API Client
# ============================================================

class APIClient:
    """
    API client using partial for endpoint-specific methods.
    
    TODO: Create specialized API methods
    """
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
    
    def request(self, method, endpoint, params=None):
        """Simulate API request"""
        url = f"{self.base_url}{endpoint}"
        return {
            'method': method,
            'url': url,
            'params': params,
            'api_key': self.api_key
        }
    
    def get(self, endpoint, params=None):
        """GET request"""
        return self.request('GET', endpoint, params)
    
    def post(self, endpoint, params=None):
        """POST request"""
        return self.request('POST', endpoint, params)

def test_api_client():
    """Test API client with partial"""
    print("--- Exercise 5: API Client with partial ---")
    
    client = APIClient('https://api.example.com', 'secret-key-123')
    
    # Create endpoint-specific methods
    get_users = partial(client.get, '/users')
    get_user_by_id = partial(client.get, '/users')
    create_user = partial(client.post, '/users')
    
    # Use specialized methods
    print("get_users():")
    print(f"  {get_users()}")
    
    print("\nget_user_by_id(params={'id': 42}):")
    print(f"  {get_user_by_id(params={'id': 42})}")
    
    print("\ncreate_user(params={'name': 'Alice'}):")
    print(f"  {create_user(params={'name': 'Alice'})}")
    
    print()

# ============================================================
# EXERCISE 6: partial with Methods
# ============================================================

def partial_with_methods():
    """
    Use partial with class methods.
    
    TODO: Create specialized method versions
    """
    print("--- Exercise 6: partial with Methods ---")
    
    class Calculator:
        def __init__(self, precision=2):
            self.precision = precision
        
        def calculate(self, operation, a, b):
            """Perform calculation"""
            result = {
                'add': a + b,
                'sub': a - b,
                'mul': a * b,
                'div': a / b if b != 0 else float('inf')
            }[operation]
            return round(result, self.precision)
    
    calc = Calculator(precision=2)
    
    # Create specialized methods
    add = partial(calc.calculate, 'add')
    multiply = partial(calc.calculate, 'mul')
    
    print(f"add(10, 5) = {add(10, 5)}")
    print(f"multiply(10, 5) = {multiply(10, 5)}")
    
    # Partial with keyword arguments
    add_10 = partial(calc.calculate, 'add', 10)
    print(f"\nadd_10(5) = {add_10(5)}")
    print(f"add_10(15) = {add_10(15)}")
    
    print()

# ============================================================
# EXERCISE 7: Chaining partial Applications
# ============================================================

def chaining_partials():
    """
    Chain multiple partial applications.
    
    TODO: Build progressively specialized functions
    """
    print("--- Exercise 7: Chaining partial Applications ---")
    
    def log_message(level, category, user, message):
        """Log a message"""
        return f"[{level}] {category} - {user}: {message}"
    
    # Progressive specialization
    error_log = partial(log_message, 'ERROR')
    error_auth_log = partial(error_log, 'AUTH')
    error_auth_admin_log = partial(error_auth_log, 'admin')
    
    print("Full function:")
    print(f"  {log_message('INFO', 'DB', 'user1', 'Query executed')}")
    
    print("\nPartially applied (level):")
    print(f"  {error_log('DB', 'user2', 'Connection failed')}")
    
    print("\nPartially applied (level + category):")
    print(f"  {error_auth_log('user3', 'Invalid token')}")
    
    print("\nFully specialized (level + category + user):")
    print(f"  {error_auth_admin_log('Unauthorized access attempt')}")
    
    # Inspect the chain
    print(f"\nerror_auth_admin_log.func: {error_auth_admin_log.func}")
    print(f"error_auth_admin_log.args: {error_auth_admin_log.args}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Partial for Configuration
# ============================================================

class ConfigurableProcessor:
    """
    Processor with configurable behavior using partial.
    
    TODO: Create configured processor instances
    """
    
    @staticmethod
    def process(data, uppercase=False, strip=False, prefix='', suffix=''):
        """Process string data"""
        result = data
        
        if strip:
            result = result.strip()
        if uppercase:
            result = result.upper()
        if prefix:
            result = prefix + result
        if suffix:
            result = result + suffix
        
        return result

def test_configurable_processor():
    """Test configurable processor"""
    print("--- Bonus Challenge: Configurable Processor ---")
    
    # Create specialized processors
    clean_processor = partial(
        ConfigurableProcessor.process,
        strip=True
    )
    
    title_processor = partial(
        ConfigurableProcessor.process,
        uppercase=True,
        strip=True
    )
    
    tag_processor = partial(
        ConfigurableProcessor.process,
        prefix='<tag>',
        suffix='</tag>',
        strip=True
    )
    
    data = "  hello world  "
    
    print(f"Original: '{data}'")
    print(f"clean_processor: '{clean_processor(data)}'")
    print(f"title_processor: '{title_processor(data)}'")
    print(f"tag_processor: '{tag_processor(data)}'")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    partial Creation:
    - Time: O(1)
    - Space: O(k) where k = frozen arguments
    
    partial Execution:
    - Same as original function
    - No additional overhead
    
    Benefits:
    - Code reuse
    - Better than lambda for simple cases
    - Introspectable (can see frozen args)
    - More efficient than closures
    - Clearer intent
    
    Use Cases:
    - Creating specialized functions
    - Function factories
    - Configuration
    - API clients
    - Callbacks with fixed parameters
    - Adapting function signatures
    
    partial vs Lambda:
    - partial: Better for freezing arguments
    - lambda: Better for arbitrary expressions
    
    partial vs Closures:
    - partial: More explicit, introspectable
    - Closures: More flexible, can access outer scope
    
    When to Use partial:
    - Freezing some arguments
    - Creating function variants
    - Adapting APIs
    - Configuration
    
    When NOT to Use:
    - Complex logic needed (use def)
    - Need to transform arguments
    - Closure over mutable state
    
    Best Practices:
    - Use for simple argument freezing
    - Combine with operator module
    - Document frozen arguments
    - Consider naming conventions
    
    Security Considerations:
    - Validate frozen arguments
    - Be careful with user-provided functions
    - Consider immutability of frozen args
    - Document expected argument types
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 4, Day 3: functools.partial")
    print("=" * 60)
    print()
    
    partial_basics()
    partial_vs_lambda()
    partial_with_builtins()
    function_factories()
    test_api_client()
    partial_with_methods()
    chaining_partials()
    test_configurable_processor()
    
    print("=" * 60)
    print("✅ Day 3 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. partial freezes some function arguments")
    print("2. Creates specialized function variants")
    print("3. More introspectable than lambda")
    print("4. Perfect for configuration and function factories")

