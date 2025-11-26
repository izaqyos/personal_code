# Week 2: Iterator Protocol & Generators

Master Python's iterator protocol and generator functions for memory-efficient data processing.

## Overview

This week dives deep into iterators and generators - the foundation of Python's lazy evaluation and memory-efficient data processing. You'll learn to create custom iterators, use generator functions, leverage the powerful itertools module, and build sophisticated data pipelines.

## Daily Exercises

### Day 1: Implementing Custom Iterators
**File:** `day1_custom_iterators.py`

Learn the iterator protocol and implement custom iterators from scratch.

**Key Concepts:**
- `__iter__()` and `__next__()` methods
- StopIteration exception
- Reusable iterators vs one-time iterators
- Iterator vs iterable distinction

**Exercises:**
- Build a simple counter iterator
- Implement Fibonacci iterator
- Create reverse iterator
- Build filtered file reader
- Implement batch iterator

---

### Day 2: Generator Functions and yield
**File:** `day2_generator_functions.py`

Master generator functions and the yield keyword for lazy evaluation.

**Key Concepts:**
- yield keyword mechanics
- Generator functions vs regular functions
- Generator state and resumption
- send() method for two-way communication
- Memory efficiency (O(1) space)

**Exercises:**
- Create Fibonacci generator
- Read large files efficiently
- Implement running average generator
- Build generator pipelines
- Process logs with generators

---

### Day 3: itertools Module Deep Dive
**File:** `day3_itertools_deep_dive.py`

Explore the powerful itertools module for efficient iteration patterns.

**Key Concepts:**
- islice for slicing iterators
- chain for combining iterables
- groupby for grouping (requires sorting!)
- Combinatorics: product, permutations, combinations
- Infinite iterators: count, cycle, repeat

**Exercises:**
- Use islice to limit sequences
- Chain multiple iterables
- Group data with groupby
- Generate combinations
- Build data processing pipelines

---

### Day 4: Generator Expressions for Pipelines
**File:** `day4_generator_pipelines.py`

Build memory-efficient data processing pipelines using generator expressions.

**Key Concepts:**
- Generator expressions vs list comprehensions
- Chaining generator expressions
- Lazy evaluation throughout pipeline
- Nested generator expressions
- Pipeline performance benefits

**Exercises:**
- Build multi-stage pipelines
- Process files with generators
- Aggregate data efficiently
- Handle CSV data streams
- Performance comparisons

---

### Day 5: yield from and Generator Delegation
**File:** `day5_yield_from.py`

Learn generator delegation with yield from for composable generators.

**Key Concepts:**
- yield from syntax
- Generator delegation
- Recursive generators
- Flattening nested structures
- Capturing return values

**Exercises:**
- Flatten nested lists recursively
- Traverse tree structures
- Compose multiple generators
- Build parsers with delegation
- Walk directory trees

---

### Day 6: Infinite Generators
**File:** `day6_infinite_generators.py`

Create and safely use infinite generators for streams and continuous data.

**Key Concepts:**
- Creating infinite generators
- itertools.count, cycle, repeat
- Limiting infinite sequences
- Safe usage patterns
- Practical applications

**Exercises:**
- Build infinite counters
- Use cycle for round-robin
- Create ID generators
- Simulate data streams
- Implement rate limiting

---

### Day 7: Review & Challenge
**File:** `day7_review_challenge.py`

Apply all Week 2 concepts in comprehensive challenges.

**Challenges:**
1. Moving average iterator
2. Log processing pipeline
3. Data aggregation with groupby
4. Recursive file tree traversal
5. Infinite event stream processing
6. Complete sales data pipeline

**Assessment:**
- Self-assessment checklist
- Performance comparisons
- Real-world applications

---

## Running the Exercises

Each day's file can be run independently:

```bash
# Run a specific day
python day1_custom_iterators.py

# Or run all days in sequence
for day in day*.py; do
    echo "Running $day"
    python "$day"
    echo ""
done
```

## Key Takeaways

1. **Iterator Protocol**: `__iter__()` returns iterator, `__next__()` returns next item
2. **Generators**: Use `yield` for lazy evaluation and O(1) space
3. **itertools**: Powerful tools for efficient iteration patterns
4. **Generator Pipelines**: Chain expressions for memory-efficient processing
5. **yield from**: Delegate to sub-generators for composition
6. **Infinite Generators**: Represent infinite sequences safely
7. **Memory Efficiency**: Generators use constant space vs O(n) for lists

## Performance Benefits

| Approach | Memory | Speed | Use Case |
|----------|--------|-------|----------|
| List comprehension | O(n) | Fast | Small datasets, need random access |
| Generator expression | O(1) | Fast | Large datasets, sequential access |
| Custom iterator | O(1) | Fast | Complex iteration logic |
| itertools | O(1) | Very fast | Standard patterns |

## Common Patterns

### Reading Large Files
```python
def read_large_file(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()
```

### Filtering Pipeline
```python
data = range(1_000_000)
filtered = (x for x in data if x % 2 == 0)
squared = (x**2 for x in filtered)
result = list(itertools.islice(squared, 10))
```

### Grouping Data
```python
from itertools import groupby

data = sorted(items, key=lambda x: x['category'])
for category, group in groupby(data, key=lambda x: x['category']):
    print(f"{category}: {list(group)}")
```

### Infinite Sequences
```python
from itertools import count, islice

# Safe usage with limit
for i in islice(count(1), 10):
    print(i)
```

## Complexity Analysis

### Iterators
- Creation: O(1)
- Iteration: O(n) for n items
- Space: O(1) - only current state

### Generators
- Creation: O(1)
- Each yield: O(1)
- Space: O(1) - no intermediate storage

### itertools.groupby
- Time: O(n) to iterate
- Space: O(1) for iterator
- **IMPORTANT**: Requires sorted input!

## Security Considerations

1. **Infinite Generators**: Always limit with islice or takewhile
2. **File Handles**: Use context managers to ensure cleanup
3. **Memory**: Generators prevent memory exhaustion attacks
4. **Recursion**: Limit depth for recursive generators
5. **Validation**: Validate input before processing

## Common Pitfalls

1. **Exhausted Generators**: Can only iterate once
   ```python
   gen = (x for x in range(5))
   list(gen)  # [0, 1, 2, 3, 4]
   list(gen)  # [] - exhausted!
   ```

2. **groupby Without Sorting**: Only groups consecutive items
   ```python
   # Wrong - not sorted
   for k, g in groupby([1, 2, 1, 2]):
       print(k, list(g))  # Groups: 1, 2, 1, 2
   
   # Correct - sorted first
   for k, g in groupby(sorted([1, 2, 1, 2])):
       print(k, list(g))  # Groups: 1, 2
   ```

3. **Infinite Generators Without Limits**: Will run forever
   ```python
   # Dangerous!
   for i in count():
       process(i)  # Never stops!
   
   # Safe
   for i in islice(count(), 1000):
       process(i)  # Stops after 1000
   ```

## Next Steps

After completing Week 2, you should be comfortable with:
- Creating custom iterators and generators
- Using itertools for efficient data processing
- Building memory-efficient pipelines
- Working with infinite sequences safely
- Applying lazy evaluation patterns

**Continue to:** Week 3 - Advanced Data Structures (collections module)

---

## Additional Resources

- [PEP 255](https://peps.python.org/pep-0255/) - Simple Generators
- [PEP 342](https://peps.python.org/pep-0342/) - Coroutines via Enhanced Generators
- [PEP 380](https://peps.python.org/pep-0380/) - Syntax for Delegating to a Subgenerator
- [itertools Documentation](https://docs.python.org/3/library/itertools.html)
- [Iterator Types](https://docs.python.org/3/library/stdtypes.html#iterator-types)

## Practice Tips

1. Always prefer generators for large datasets
2. Use itertools before writing custom solutions
3. Remember to sort before using groupby
4. Limit infinite generators immediately
5. Profile memory usage with sys.getsizeof()

---

**Week 2 Status:** ✅ Complete  
**Estimated Time:** 10-15 minutes per day  
**Difficulty:** ⭐⭐⭐☆☆ (Intermediate)

