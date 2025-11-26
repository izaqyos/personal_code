# Week 3: Advanced Data Structures

Master Python's `collections` module and advanced data structures for cleaner, more efficient code.

## Overview

This week focuses on Python's powerful `collections` module, which provides specialized container datatypes beyond the built-in list, dict, tuple, and set. These data structures solve common programming problems elegantly and efficiently.

## Daily Breakdown

### Day 1: Counter - Frequency Counting Made Easy
**File:** `day1_counter.py`

Learn to count frequencies efficiently with Counter:
- Basic counting operations
- `most_common()` for top items
- Counter arithmetic (+, -, &, |)
- Real-world applications (word frequency, error tracking)
- Performance characteristics

**Key Concepts:**
- `Counter(iterable)` - count hashable objects
- `most_common(n)` - get top n items
- Counter as multiset
- Streaming accumulation

**Complexity:**
- Count: O(n)
- most_common: O(n log k) for top k items
- Arithmetic: O(n)

---

### Day 2: deque - Efficient Double-Ended Queue
**File:** `day2_deque.py`

Master deque for O(1) operations at both ends:
- append/appendleft and pop/popleft
- rotate() for circular operations
- maxlen for bounded queues
- Queue and Stack implementations
- Sliding window problems

**Key Concepts:**
- O(1) operations at both ends
- Rotation for round-robin
- Bounded deque with maxlen
- Thread-safe append/pop

**Complexity:**
- append/pop (both ends): O(1)
- Access by index: O(n)
- rotate(k): O(k)

**Use Cases:**
- FIFO queues
- LIFO stacks
- Recent history tracking
- Sliding window algorithms
- Browser history

---

### Day 3: defaultdict - Eliminate KeyError
**File:** `day3_defaultdict.py`

Use defaultdict to avoid KeyError checks:
- Factory functions (list, int, set)
- Grouping data patterns
- Counting patterns
- Nested defaultdict
- Custom factories

**Key Concepts:**
- `defaultdict(list)` for grouping
- `defaultdict(int)` for counting
- `defaultdict(set)` for unique items
- Lambda factories for nested structures

**Complexity:**
- Same as dict: O(1) average
- Cleaner code, no if-else checks

**Use Cases:**
- Grouping data by key
- Frequency counting
- Graph adjacency lists
- Inverted indices
- Log analysis

---

### Day 4: OrderedDict - Order-Aware Dictionary
**File:** `day4_ordereddict.py`

Understand OrderedDict in modern Python:
- OrderedDict vs dict (Python 3.7+)
- `move_to_end()` for LRU patterns
- `popitem(last=False)` for FIFO
- Order-sensitive equality
- When to still use OrderedDict

**Key Concepts:**
- move_to_end() - unique to OrderedDict
- Order matters for equality
- FIFO with popitem(last=False)
- LRU cache implementation

**Complexity:**
- Same as dict: O(1) average
- move_to_end: O(1)
- ~25% more memory than dict

**Use Cases:**
- LRU cache
- Recently accessed tracking
- Configuration with access order
- FIFO queue behavior

---

### Day 5: ChainMap - Layered Dictionary Lookups
**File:** `day5_chainmap.py`

Master ChainMap for hierarchical lookups:
- Layered dictionary searches
- Configuration hierarchies
- `new_child()` for nested scopes
- Scope chain implementations
- Template variable resolution

**Key Concepts:**
- Groups multiple dicts into single view
- Searches in order (first to last)
- new_child() for scope management
- No data copying (memory efficient)

**Complexity:**
- Lookup: O(m) where m = number of maps
- new_child: O(1)
- Space: O(1) - just references

**Use Cases:**
- Configuration (CLI > env > config > defaults)
- Variable scope chains
- Template engines
- Context management
- Layered defaults

---

### Day 6: namedtuple - Readable Immutable Records
**File:** `day6_namedtuple.py`

Create readable, immutable data structures:
- namedtuple basics
- typing.NamedTuple with type hints
- Built-in methods (_make, _asdict, _replace)
- namedtuple vs dict vs class
- Nested namedtuples

**Key Concepts:**
- Immutable records with named fields
- typing.NamedTuple for modern Python
- More readable than tuples
- More efficient than dicts
- Can add methods

**Complexity:**
- Same as tuple: O(1) access
- Memory efficient
- Immutable (thread-safe)

**Use Cases:**
- Database records
- CSV/JSON parsing
- Function return values
- Configuration objects
- Coordinate systems
- API responses

---

### Day 7: Review & Challenge
**File:** `day7_review_challenge.py`

Apply all Week 3 concepts together:
- **Challenge 1:** LRU Cache with statistics
- **Challenge 2:** Word frequency analyzer
- **Challenge 3:** Request rate limiter
- **Challenge 4:** Configuration manager
- **Challenge 5:** Comprehensive data pipeline

**Skills Practiced:**
- Combining multiple collections
- Real-world system design
- Performance optimization
- Statistics tracking

---

## Quick Reference

### When to Use Each Collection

| Collection | Best For | Key Benefit |
|------------|----------|-------------|
| **Counter** | Frequency counting | Automatic counting, arithmetic |
| **deque** | Queue/Stack, sliding window | O(1) at both ends |
| **defaultdict** | Grouping, counting | No KeyError |
| **OrderedDict** | LRU cache, access tracking | move_to_end() |
| **ChainMap** | Config hierarchy, scopes | Layered lookups |
| **namedtuple** | Immutable records | Readable, efficient |

### Performance Cheat Sheet

```python
# Counter
Counter(items)              # O(n)
counter.most_common(k)      # O(n log k)

# deque
deque.append()              # O(1)
deque.popleft()             # O(1)
deque.rotate(k)             # O(k)

# defaultdict
dd[key]                     # O(1) - no KeyError

# OrderedDict
od.move_to_end(key)         # O(1)
od.popitem(last=False)      # O(1)

# ChainMap
cm[key]                     # O(m) - m maps
cm.new_child()              # O(1)

# namedtuple
nt.field                    # O(1)
nt._replace(field=val)      # O(n) - n fields
```

### Common Patterns

**Grouping:**
```python
from collections import defaultdict

groups = defaultdict(list)
for item in items:
    groups[item.category].append(item)
```

**Counting:**
```python
from collections import Counter

counts = Counter(items)
top_10 = counts.most_common(10)
```

**LRU Cache:**
```python
from collections import OrderedDict

cache = OrderedDict()
cache.move_to_end(key)  # Mark as recent
if len(cache) > maxsize:
    cache.popitem(last=False)  # Evict oldest
```

**Configuration Hierarchy:**
```python
from collections import ChainMap

config = ChainMap(cli_args, env_vars, config_file, defaults)
value = config['key']  # Searches in order
```

**Immutable Records:**
```python
from typing import NamedTuple

class Person(NamedTuple):
    name: str
    age: int
    
person = Person("Alice", 30)
```

---

## Learning Outcomes

After completing Week 3, you should be able to:

✅ Choose the right collection for the problem  
✅ Implement efficient counting and grouping  
✅ Build queues and stacks with deque  
✅ Create LRU caches with OrderedDict  
✅ Design configuration hierarchies with ChainMap  
✅ Define clean data structures with namedtuple  
✅ Combine multiple collections effectively  
✅ Understand time/space complexity trade-offs  

---

## Running the Exercises

Each day's file is self-contained and executable:

```bash
# Run individual days
python day1_counter.py
python day2_deque.py
python day3_defaultdict.py
python day4_ordereddict.py
python day5_chainmap.py
python day6_namedtuple.py
python day7_review_challenge.py

# Or run all at once
for day in day*.py; do
    echo "Running $day..."
    python "$day"
    echo ""
done
```

---

## Additional Resources

**Official Documentation:**
- [collections module](https://docs.python.org/3/library/collections.html)
- [Counter](https://docs.python.org/3/library/collections.html#collections.Counter)
- [deque](https://docs.python.org/3/library/collections.html#collections.deque)
- [defaultdict](https://docs.python.org/3/library/collections.html#collections.defaultdict)
- [OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict)
- [ChainMap](https://docs.python.org/3/library/collections.html#collections.ChainMap)
- [namedtuple](https://docs.python.org/3/library/collections.html#collections.namedtuple)

**Further Reading:**
- [Python Data Structures Deep Dive](https://realpython.com/python-data-structures/)
- [Effective Python: Item 46 - Use collections](https://effectivepython.com/)

---

## Next Steps

🎯 **Week 4:** Functional Programming  
Learn map, filter, reduce, partial, and functional composition.

---

## Notes

- All exercises include complexity analysis
- Security considerations are discussed
- Real-world scenarios demonstrate practical usage
- Performance comparisons show trade-offs
- Code is production-ready and well-documented

**Time Investment:** ~10-15 minutes per day, 15-20 minutes for Day 7  
**Total:** ~90 minutes for the week

---

*Happy coding! 🐍*

