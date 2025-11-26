"""
Week 3, Day 4: OrderedDict vs dict (Python 3.7+)

Learning Objectives:
- Understand OrderedDict and its history
- Learn differences between OrderedDict and regular dict
- Know when to use OrderedDict in modern Python
- Practice order-preserving operations

Time: 10-15 minutes
"""

from collections import OrderedDict
import sys

# ============================================================
# EXERCISE 1: OrderedDict Basics
# ============================================================

def ordereddict_basics():
    """
    Learn basic OrderedDict operations.
    
    Note: Since Python 3.7+, regular dicts maintain insertion order!
    """
    print("--- Exercise 1: OrderedDict Basics ---")
    
    # Create OrderedDict
    od = OrderedDict()
    od['c'] = 3
    od['a'] = 1
    od['b'] = 2
    
    print(f"OrderedDict: {od}")
    print(f"Keys in order: {list(od.keys())}")
    
    # Regular dict (Python 3.7+)
    rd = {}
    rd['c'] = 3
    rd['a'] = 1
    rd['b'] = 2
    
    print(f"\nRegular dict: {rd}")
    print(f"Keys in order: {list(rd.keys())}")
    
    print("\n💡 Since Python 3.7, regular dicts maintain insertion order!")
    
    print()

# ============================================================
# EXERCISE 2: move_to_end() Method
# ============================================================

def move_to_end_examples():
    """
    Use move_to_end() - unique to OrderedDict.
    
    TODO: Practice moving items to end or beginning
    """
    print("--- Exercise 2: move_to_end() Method ---")
    
    # OrderedDict has move_to_end()
    od = OrderedDict([('a', 1), ('b', 2), ('c', 3), ('d', 4)])
    print(f"Original: {od}")
    
    # Move to end (default)
    od.move_to_end('b')
    print(f"After move_to_end('b'): {od}")
    
    # Move to beginning
    od.move_to_end('c', last=False)
    print(f"After move_to_end('c', last=False): {od}")
    
    # Use case: LRU cache implementation
    print("\nLRU Cache simulation:")
    cache = OrderedDict([('page1', 'data1'), ('page2', 'data2'), ('page3', 'data3')])
    
    # Access page1 (move to end = most recent)
    cache.move_to_end('page1')
    print(f"After accessing page1: {list(cache.keys())}")
    
    # Add new page (evict oldest if needed)
    if len(cache) >= 3:
        oldest = next(iter(cache))
        print(f"Evicting oldest: {oldest}")
        del cache[oldest]
    cache['page4'] = 'data4'
    print(f"After adding page4: {list(cache.keys())}")
    
    print()

# ============================================================
# EXERCISE 3: Equality Comparison
# ============================================================

def equality_comparison():
    """
    Compare OrderedDict vs dict equality.
    
    TODO: Understand order-sensitive equality
    """
    print("--- Exercise 3: Equality Comparison ---")
    
    # OrderedDict: order matters for equality
    od1 = OrderedDict([('a', 1), ('b', 2)])
    od2 = OrderedDict([('b', 2), ('a', 1)])
    
    print(f"od1: {od1}")
    print(f"od2: {od2}")
    print(f"od1 == od2: {od1 == od2}")  # False - different order!
    
    # Regular dict: order doesn't matter for equality
    d1 = {'a': 1, 'b': 2}
    d2 = {'b': 2, 'a': 1}
    
    print(f"\nd1: {d1}")
    print(f"d2: {d2}")
    print(f"d1 == d2: {d1 == d2}")  # True - same content
    
    # OrderedDict vs dict comparison
    print(f"\nod1 == d1: {od1 == d1}")  # True - compares content only
    
    print()

# ============================================================
# EXERCISE 4: popitem() with LIFO/FIFO
# ============================================================

def popitem_examples():
    """
    Use popitem() with last parameter.
    
    TODO: Practice LIFO and FIFO patterns
    """
    print("--- Exercise 4: popitem() with LIFO/FIFO ---")
    
    # LIFO (Last In, First Out) - Stack behavior
    od_lifo = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
    print(f"Original: {od_lifo}")
    
    item = od_lifo.popitem(last=True)  # Default
    print(f"popitem(last=True): {item}")
    print(f"Remaining: {od_lifo}")
    
    # FIFO (First In, First Out) - Queue behavior
    od_fifo = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
    print(f"\nOriginal: {od_fifo}")
    
    item = od_fifo.popitem(last=False)
    print(f"popitem(last=False): {item}")
    print(f"Remaining: {od_fifo}")
    
    print()

# ============================================================
# EXERCISE 5: When to Use OrderedDict Today
# ============================================================

def when_to_use_ordereddict():
    """
    Understand when OrderedDict is still useful in Python 3.7+.
    """
    print("--- Exercise 5: When to Use OrderedDict ---")
    
    print("Use OrderedDict when you need:")
    print("  1. move_to_end() method (not available in dict)")
    print("  2. popitem(last=False) for FIFO behavior")
    print("  3. Order-sensitive equality (od1 == od2 checks order)")
    print("  4. Backwards compatibility with Python < 3.7")
    print("  5. Explicit signal that order matters")
    
    print("\nUse regular dict when:")
    print("  1. You just need insertion order preserved")
    print("  2. You don't need special OrderedDict methods")
    print("  3. You want slightly better performance")
    print("  4. You want less memory usage")
    
    # Memory comparison
    od = OrderedDict((i, i) for i in range(1000))
    d = {i: i for i in range(1000)}
    
    print(f"\nMemory usage (1000 items):")
    print(f"  OrderedDict: {sys.getsizeof(od):,} bytes")
    print(f"  Regular dict: {sys.getsizeof(d):,} bytes")
    print(f"  Difference: {sys.getsizeof(od) - sys.getsizeof(d):,} bytes")
    
    print()

# ============================================================
# EXERCISE 6: Real-World Scenario - Configuration Manager
# ============================================================

class ConfigManager:
    """
    Configuration manager that preserves order and tracks access.
    
    TODO: Implement config manager with OrderedDict
    """
    
    def __init__(self):
        self.config = OrderedDict()
        self.access_count = {}
    
    def set(self, key: str, value: any):
        """Set configuration value"""
        self.config[key] = value
    
    def get(self, key: str, default=None):
        """Get configuration value and track access"""
        # Track access
        self.access_count[key] = self.access_count.get(key, 0) + 1
        
        # Move to end (most recently accessed)
        if key in self.config:
            self.config.move_to_end(key)
        
        return self.config.get(key, default)
    
    def get_all(self):
        """Get all config in order"""
        return dict(self.config)
    
    def get_recently_accessed(self, n: int = 5):
        """Get n most recently accessed configs"""
        # Last n items (most recent)
        items = list(self.config.items())
        return items[-n:] if len(items) >= n else items
    
    def get_most_accessed(self, n: int = 5):
        """Get n most frequently accessed configs"""
        sorted_by_access = sorted(
            self.access_count.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_by_access[:n]

def test_config_manager():
    """Test the ConfigManager"""
    print("--- Exercise 6: Configuration Manager ---")
    
    config = ConfigManager()
    
    # Set configurations
    config.set('database_url', 'localhost:5432')
    config.set('cache_size', 1000)
    config.set('debug_mode', True)
    config.set('log_level', 'INFO')
    
    print("Initial config:")
    for key, value in config.get_all().items():
        print(f"  {key}: {value}")
    
    # Access some configs
    config.get('debug_mode')
    config.get('database_url')
    config.get('debug_mode')
    config.get('cache_size')
    config.get('debug_mode')
    
    print("\nRecently accessed (order):")
    for key, value in config.get_recently_accessed(3):
        print(f"  {key}: {value}")
    
    print("\nMost accessed (frequency):")
    for key, count in config.get_most_accessed(3):
        print(f"  {key}: {count} times")
    
    print()

# ============================================================
# EXERCISE 7: Reversing OrderedDict
# ============================================================

def reversing_ordereddict():
    """
    Reverse the order of OrderedDict.
    
    TODO: Practice reversing operations
    """
    print("--- Exercise 7: Reversing OrderedDict ---")
    
    od = OrderedDict([('a', 1), ('b', 2), ('c', 3), ('d', 4)])
    print(f"Original: {od}")
    
    # Method 1: Using reversed()
    reversed_od = OrderedDict(reversed(list(od.items())))
    print(f"Reversed (method 1): {reversed_od}")
    
    # Method 2: Using move_to_end() in loop
    od2 = OrderedDict([('a', 1), ('b', 2), ('c', 3), ('d', 4)])
    for key in list(od2.keys()):
        od2.move_to_end(key, last=False)
    print(f"Reversed (method 2): {od2}")
    
    print()

# ============================================================
# BONUS CHALLENGE: OrderedDict as LRU Cache
# ============================================================

class SimpleLRUCache:
    """
    Simple LRU cache using OrderedDict.
    
    TODO: Implement LRU cache with maxsize
    """
    
    def __init__(self, maxsize: int = 128):
        self.cache = OrderedDict()
        self.maxsize = maxsize
    
    def get(self, key):
        """Get value and mark as recently used"""
        if key not in self.cache:
            return None
        
        # Move to end (most recent)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        """Put value in cache"""
        if key in self.cache:
            # Update and move to end
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.maxsize:
            # Evict least recently used (first item)
            self.cache.popitem(last=False)
        
        self.cache[key] = value
    
    def __repr__(self):
        return f"LRUCache({list(self.cache.items())})"

def test_lru_cache():
    """Test LRU cache"""
    print("--- Bonus Challenge: LRU Cache with OrderedDict ---")
    
    cache = SimpleLRUCache(maxsize=3)
    
    print("Operations:")
    cache.put('a', 1)
    print(f"  put(a, 1): {cache}")
    
    cache.put('b', 2)
    print(f"  put(b, 2): {cache}")
    
    cache.put('c', 3)
    print(f"  put(c, 3): {cache}")
    
    val = cache.get('a')
    print(f"  get(a) = {val}: {cache}")
    
    cache.put('d', 4)  # Evicts 'b'
    print(f"  put(d, 4): {cache}")
    
    val = cache.get('b')
    print(f"  get(b) = {val} (evicted)")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    OrderedDict Operations:
    - Access/Insert/Delete: O(1) average
    - move_to_end(): O(1)
    - popitem(): O(1)
    - Iteration: O(n)
    
    Regular dict (Python 3.7+):
    - Access/Insert/Delete: O(1) average
    - No move_to_end() or popitem(last=False)
    - Slightly faster than OrderedDict
    
    Space Complexity:
    - OrderedDict: O(n) + overhead for doubly-linked list
    - Regular dict: O(n)
    - OrderedDict uses ~25% more memory
    
    Benefits of OrderedDict:
    - move_to_end() for LRU patterns
    - popitem(last=False) for FIFO
    - Order-sensitive equality
    - Explicit about order importance
    
    Benefits of Regular dict (3.7+):
    - Faster (no linked list overhead)
    - Less memory
    - Simpler (order is implicit)
    
    Use Cases for OrderedDict:
    - LRU cache implementation
    - Recently accessed tracking
    - Configuration with access order
    - FIFO queue behavior
    - When order matters for equality
    
    Migration from OrderedDict:
    - Most code can use regular dict now
    - Keep OrderedDict if using special methods
    - Consider backwards compatibility needs
    
    Security Considerations:
    - Same as regular dict
    - Validate maxsize in LRU implementations
    - Be careful with move_to_end() in concurrent code
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 3, Day 4: OrderedDict vs dict")
    print("=" * 60)
    print()
    
    ordereddict_basics()
    move_to_end_examples()
    equality_comparison()
    popitem_examples()
    when_to_use_ordereddict()
    test_config_manager()
    reversing_ordereddict()
    test_lru_cache()
    
    print("=" * 60)
    print("✅ Day 4 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Python 3.7+ dicts maintain insertion order")
    print("2. OrderedDict still useful for move_to_end() and popitem(last=False)")
    print("3. OrderedDict equality is order-sensitive")
    print("4. Perfect for LRU cache and access tracking")

