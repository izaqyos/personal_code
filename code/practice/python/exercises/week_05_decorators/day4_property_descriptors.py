"""
Week 5, Day 4: @property and Descriptors

Learning Objectives:
- Master @property for computed attributes
- Learn getter, setter, deleter pattern
- Understand descriptor protocol
- Practice creating custom descriptors
- Build validation with descriptors

Time: 10-15 minutes
"""

from functools import wraps

# ============================================================
# EXERCISE 1: @property Basics
# ============================================================

def property_basics():
    """
    Learn @property for computed attributes.
    
    @property: Make method accessible like an attribute
    """
    print("--- Exercise 1: @property Basics ---")
    
    class Circle:
        def __init__(self, radius):
            self._radius = radius
        
        @property
        def radius(self):
            """Get radius"""
            return self._radius
        
        @property
        def diameter(self):
            """Computed diameter"""
            return self._radius * 2
        
        @property
        def area(self):
            """Computed area"""
            import math
            return math.pi * self._radius ** 2
    
    circle = Circle(5)
    
    print(f"Radius: {circle.radius}")
    print(f"Diameter: {circle.diameter}")
    print(f"Area: {circle.area:.2f}")
    
    print("\n💡 @property makes methods look like attributes")
    print("💡 Great for computed values")
    
    print()

# ============================================================
# EXERCISE 2: Property with Setter
# ============================================================

def property_with_setter():
    """
    Learn getter/setter pattern with @property.
    
    TODO: Implement validation in setter
    """
    print("--- Exercise 2: Property with Setter ---")
    
    class Temperature:
        def __init__(self, celsius):
            self._celsius = celsius
        
        @property
        def celsius(self):
            """Get temperature in Celsius"""
            return self._celsius
        
        @celsius.setter
        def celsius(self, value):
            """Set temperature in Celsius with validation"""
            if value < -273.15:
                raise ValueError("Temperature below absolute zero!")
            self._celsius = value
        
        @property
        def fahrenheit(self):
            """Get temperature in Fahrenheit"""
            return self._celsius * 9/5 + 32
        
        @fahrenheit.setter
        def fahrenheit(self, value):
            """Set temperature in Fahrenheit"""
            self.celsius = (value - 32) * 5/9
    
    temp = Temperature(25)
    
    print(f"Initial: {temp.celsius}°C = {temp.fahrenheit}°F")
    
    temp.celsius = 0
    print(f"After setting celsius to 0: {temp.celsius}°C = {temp.fahrenheit}°F")
    
    temp.fahrenheit = 212
    print(f"After setting fahrenheit to 212: {temp.celsius}°C = {temp.fahrenheit}°F")
    
    print("\nTrying invalid value:")
    try:
        temp.celsius = -300
    except ValueError as e:
        print(f"  Error: {e}")
    
    print()

# ============================================================
# EXERCISE 3: Property with Deleter
# ============================================================

def property_with_deleter():
    """
    Learn complete getter/setter/deleter pattern.
    
    TODO: Implement property deletion
    """
    print("--- Exercise 3: Property with Deleter ---")
    
    class Person:
        def __init__(self, name):
            self._name = name
            self._email = None
        
        @property
        def name(self):
            """Get name"""
            return self._name
        
        @property
        def email(self):
            """Get email"""
            return self._email
        
        @email.setter
        def email(self, value):
            """Set email with validation"""
            if value and '@' not in value:
                raise ValueError("Invalid email format")
            self._email = value
        
        @email.deleter
        def email(self):
            """Delete email"""
            print(f"  Deleting email: {self._email}")
            self._email = None
    
    person = Person("Alice")
    
    print(f"Name: {person.name}")
    print(f"Email: {person.email}")
    
    person.email = "alice@example.com"
    print(f"After setting email: {person.email}")
    
    del person.email
    print(f"After deleting email: {person.email}")
    
    print()

# ============================================================
# EXERCISE 4: Descriptor Protocol
# ============================================================

def descriptor_protocol():
    """
    Learn the descriptor protocol.
    
    Descriptor: Object with __get__, __set__, __delete__
    """
    print("--- Exercise 4: Descriptor Protocol ---")
    
    class Descriptor:
        """Simple descriptor"""
        
        def __init__(self, name):
            self.name = name
        
        def __get__(self, instance, owner):
            """Get attribute value"""
            if instance is None:
                return self
            print(f"  Getting {self.name}")
            return instance.__dict__.get(f"_{self.name}")
        
        def __set__(self, instance, value):
            """Set attribute value"""
            print(f"  Setting {self.name} = {value}")
            instance.__dict__[f"_{self.name}"] = value
        
        def __delete__(self, instance):
            """Delete attribute"""
            print(f"  Deleting {self.name}")
            del instance.__dict__[f"_{self.name}"]
    
    class MyClass:
        x = Descriptor("x")
        y = Descriptor("y")
    
    obj = MyClass()
    
    print("Setting values:")
    obj.x = 10
    obj.y = 20
    
    print("\nGetting values:")
    print(f"x = {obj.x}")
    print(f"y = {obj.y}")
    
    print("\nDeleting x:")
    del obj.x
    
    print()

# ============================================================
# EXERCISE 5: Validation Descriptor
# ============================================================

class Validated:
    """
    Descriptor for validated attributes.
    
    TODO: Implement validation in descriptor
    """
    
    def __init__(self, validator, name=None):
        self.validator = validator
        self.name = name
    
    def __set_name__(self, owner, name):
        """Called when descriptor is assigned to class attribute"""
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not self.validator(value):
            raise ValueError(f"Validation failed for {self.name}")
        instance.__dict__[self.name] = value

def test_validated_descriptor():
    """Test validation descriptor"""
    print("--- Exercise 5: Validation Descriptor ---")
    
    class Person:
        name = Validated(lambda x: isinstance(x, str) and len(x) > 0)
        age = Validated(lambda x: isinstance(x, int) and 0 < x < 150)
        email = Validated(lambda x: isinstance(x, str) and '@' in x)
    
    person = Person()
    
    print("Setting valid values:")
    person.name = "Alice"
    person.age = 30
    person.email = "alice@example.com"
    print(f"  name={person.name}, age={person.age}, email={person.email}")
    
    print("\nTrying invalid values:")
    try:
        person.age = 200
    except ValueError as e:
        print(f"  age=200 → {e}")
    
    try:
        person.email = "invalid"
    except ValueError as e:
        print(f"  email='invalid' → {e}")
    
    print()

# ============================================================
# EXERCISE 6: Typed Descriptor
# ============================================================

class Typed:
    """
    Descriptor for type-checked attributes.
    
    TODO: Implement type checking
    """
    
    def __init__(self, expected_type, name=None):
        self.expected_type = expected_type
        self.name = name
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        instance.__dict__[self.name] = value

def test_typed_descriptor():
    """Test typed descriptor"""
    print("--- Exercise 6: Typed Descriptor ---")
    
    class Product:
        name = Typed(str)
        price = Typed(float)
        quantity = Typed(int)
    
    product = Product()
    
    print("Setting values with correct types:")
    product.name = "Widget"
    product.price = 19.99
    product.quantity = 100
    print(f"  {product.name}: ${product.price} ({product.quantity} in stock)")
    
    print("\nTrying wrong types:")
    try:
        product.price = "19.99"
    except TypeError as e:
        print(f"  price='19.99' → {e}")
    
    try:
        product.quantity = 100.5
    except TypeError as e:
        print(f"  quantity=100.5 → {e}")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - Model with Validation
# ============================================================

class Range:
    """Descriptor for range-validated numbers"""
    
    def __init__(self, min_value=None, max_value=None, name=None):
        self.min_value = min_value
        self.max_value = max_value
        self.name = name
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be a number")
        
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} must be >= {self.min_value}")
        
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} must be <= {self.max_value}")
        
        instance.__dict__[self.name] = value

def test_model_validation():
    """Test model with validation"""
    print("--- Exercise 7: Model with Validation ---")
    
    class User:
        username = Validated(lambda x: isinstance(x, str) and 3 <= len(x) <= 20)
        age = Range(min_value=0, max_value=150)
        score = Range(min_value=0, max_value=100)
    
    user = User()
    
    print("Creating valid user:")
    user.username = "alice"
    user.age = 30
    user.score = 95
    print(f"  {user.username}: age={user.age}, score={user.score}")
    
    print("\nValidation errors:")
    try:
        user.username = "ab"  # Too short
    except ValueError as e:
        print(f"  username='ab' → {e}")
    
    try:
        user.age = -5
    except ValueError as e:
        print(f"  age=-5 → {e}")
    
    try:
        user.score = 150
    except ValueError as e:
        print(f"  score=150 → {e}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Lazy Property
# ============================================================

class LazyProperty:
    """
    Descriptor for lazy-loaded properties.
    
    TODO: Compute value only once, then cache
    """
    
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # Check if already computed
        if self.name not in instance.__dict__:
            print(f"  Computing {self.name}...")
            instance.__dict__[self.name] = self.func(instance)
        else:
            print(f"  Using cached {self.name}")
        
        return instance.__dict__[self.name]

def test_lazy_property():
    """Test lazy property"""
    print("--- Bonus Challenge: Lazy Property ---")
    
    class DataProcessor:
        def __init__(self, data):
            self.data = data
        
        @LazyProperty
        def processed_data(self):
            """Expensive computation"""
            import time
            time.sleep(0.1)
            return [x * 2 for x in self.data]
        
        @LazyProperty
        def summary(self):
            """Another expensive computation"""
            import time
            time.sleep(0.1)
            return {
                'count': len(self.data),
                'sum': sum(self.data),
                'avg': sum(self.data) / len(self.data)
            }
    
    processor = DataProcessor([1, 2, 3, 4, 5])
    
    print("First access to processed_data:")
    print(f"  {processor.processed_data}")
    
    print("\nSecond access (cached):")
    print(f"  {processor.processed_data}")
    
    print("\nFirst access to summary:")
    print(f"  {processor.summary}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    @property:
    - Access: O(f) where f = getter function time
    - Setting: O(f) where f = setter function time
    - No additional space overhead
    
    Descriptors:
    - __get__/__set__: O(1) typically
    - Can add validation overhead
    - Space: O(1) per descriptor instance
    
    Benefits:
    - Encapsulation
    - Computed attributes
    - Validation
    - Lazy loading
    - Backward compatibility
    
    Use Cases:
    - Computed properties
    - Validated attributes
    - Type checking
    - Lazy initialization
    - Read-only attributes
    - Attribute access logging
    
    @property vs Descriptor:
    - @property: Simpler, per-attribute
    - Descriptor: Reusable, multiple attributes
    
    Best Practices:
    - Use @property for simple cases
    - Use descriptors for reusable validation
    - Keep getters fast (no heavy computation)
    - Document property behavior
    - Consider lazy loading for expensive operations
    
    Common Patterns:
    - @property for computed values
    - Descriptors for validation
    - LazyProperty for expensive computations
    - Typed descriptors for type safety
    
    Security Considerations:
    - Validate all inputs in setters
    - Be careful with computed properties (DOS)
    - Consider access control
    - Handle edge cases
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 5, Day 4: @property and Descriptors")
    print("=" * 60)
    print()
    
    property_basics()
    property_with_setter()
    property_with_deleter()
    descriptor_protocol()
    test_validated_descriptor()
    test_typed_descriptor()
    test_model_validation()
    test_lazy_property()
    
    print("=" * 60)
    print("✅ Day 4 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. @property makes methods look like attributes")
    print("2. Descriptors enable reusable attribute logic")
    print("3. Use for validation, type checking, lazy loading")
    print("4. __get__, __set__, __delete__ define descriptor protocol")

