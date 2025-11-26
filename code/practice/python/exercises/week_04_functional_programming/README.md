## Week 4: Functional Programming

Master functional programming concepts in Python for cleaner, more composable code.

## Overview

This week focuses on functional programming paradigms in Python. Learn to write pure functions, compose operations, and build efficient data processing pipelines using map, filter, reduce, and itertools.

## Daily Breakdown

### Day 1: map, filter, and reduce
**File:** `day1_map_filter_reduce.py`

Learn the foundational functional operations:
- `map()` for transforming sequences
- `filter()` for selecting elements
- `reduce()` for accumulation
- Comparison with list comprehensions
- Chaining functional operations

**Key Concepts:**
- Lazy evaluation with iterators
- Functional data transformation
- When to use comprehensions vs functional tools

**Complexity:**
- map/filter: O(n) with lazy evaluation
- reduce: O(n) eager evaluation

---

### Day 2: Lambda Functions
**File:** `day2_lambda_functions.py`

Master anonymous functions:
- Lambda syntax and limitations
- Lambda vs def functions
- Using lambda with built-ins (sorted, max, min)
- Lambda anti-patterns to avoid
- operator module alternatives

**Key Concepts:**
- Single expression functions
- When to use lambda appropriately
- Avoiding complex lambdas

**Best Practices:**
- Keep lambdas simple
- Use def for complex logic
- Consider operator module

---

### Day 3: functools.partial
**File:** `day3_partial_functions.py`

Learn partial function application:
- Freezing function arguments
- Creating specialized functions
- Function factories
- partial vs lambda
- Chaining partial applications

**Key Concepts:**
- Partial application pattern
- Configuration with partial
- Better introspection than lambda

**Use Cases:**
- API clients
- Configuration
- Function specialization

---

### Day 4: Function Composition and Pipelines
**File:** `day4_compose_pipe.py`

Build composable data pipelines:
- Implementing compose() and pipe()
- Left-to-right vs right-to-left composition
- Pipeline class for fluent API
- Real-world data transformation
- Currying and composition

**Key Concepts:**
- compose: f(g(x))
- pipe: left-to-right (more intuitive)
- Declarative data processing

**Benefits:**
- Readable transformations
- Reusable components
- Easy testing

---

### Day 5: Higher-Order Functions
**File:** `day5_higher_order_functions.py`

Master functions that take/return functions:
- Functions as arguments
- Functions as return values
- Closures and scope
- Decorators as higher-order functions
- Function combinators
- Memoization pattern

**Key Concepts:**
- Higher-order function: takes/returns functions
- Closure: captures enclosing scope
- Function factories

**Use Cases:**
- Decorators
- Callbacks
- Strategy pattern
- Middleware

---

### Day 6: itertools for Functional Programming
**File:** `day6_itertools_functional.py`

Leverage itertools for efficient iteration:
- Infinite iterators (count, cycle, repeat)
- Terminating iterators (accumulate, chain, compress)
- Combinatoric iterators (product, permutations, combinations)
- groupby for aggregation
- Building iterator pipelines
- Custom iterator combinators

**Key Concepts:**
- Lazy evaluation for efficiency
- Memory-efficient processing
- Functional composition with iterators

**Complexity:**
- Most operations: O(1) per element
- groupby: O(n), requires sorted input
- Combinatorics: exponential

---

### Day 7: Review & Challenge
**File:** `day7_review_challenge.py`

Apply all Week 4 concepts:
- **Challenge 1:** ETL data pipeline
- **Challenge 2:** Functional aggregation
- **Challenge 3:** Validation pipeline
- **Challenge 4:** Memoization and performance
- **Challenge 5:** itertools processing
- **Challenge 6:** Complete ETL system

**Skills Practiced:**
- Combining functional techniques
- Real-world data processing
- Performance optimization
- Pipeline architecture

---

## Quick Reference

### Core Functional Operations

```python
# map - transform elements
squared = list(map(lambda x: x ** 2, numbers))

# filter - select elements
evens = list(filter(lambda x: x % 2 == 0, numbers))

# reduce - accumulate
from functools import reduce
total = reduce(lambda acc, x: acc + x, numbers)

# Chaining
result = reduce(
    lambda acc, x: acc + x,
    map(lambda x: x ** 2,
        filter(lambda x: x % 2 == 0, numbers))
)
```

### Lambda Functions

```python
# Basic lambda
square = lambda x: x ** 2

# Multiple arguments
add = lambda x, y: x + y

# With built-ins
sorted(words, key=lambda w: len(w))
max(students, key=lambda s: s['grade'])
```

### Partial Application

```python
from functools import partial

# Create specialized function
double = partial(operator.mul, 2)

# With keyword arguments
format_usd = partial(format_currency, symbol='$', decimals=2)
```

### Function Composition

```python
def pipe(*functions):
    """Left-to-right composition"""
    def inner(arg):
        result = arg
        for func in functions:
            result = func(result)
        return result
    return inner

# Use pipeline
transform = pipe(parse, validate, process, format)
result = transform(data)
```

### itertools Essentials

```python
import itertools

# Infinite iterators
itertools.count(start=0, step=1)
itertools.cycle(['a', 'b', 'c'])
itertools.repeat('x', times=3)

# Terminating iterators
itertools.accumulate([1, 2, 3, 4])  # [1, 3, 6, 10]
itertools.chain([1, 2], [3, 4])     # [1, 2, 3, 4]

# Combinatorics
itertools.product(['A', 'B'], [1, 2])  # Cartesian product
itertools.permutations(['A', 'B', 'C'], 2)
itertools.combinations(['A', 'B', 'C'], 2)

# Grouping (requires sorted input)
for key, group in itertools.groupby(data, key=lambda x: x['category']):
    print(key, list(group))
```

---

## Functional Programming Principles

### Pure Functions
- No side effects
- Same input → same output
- Easier to test and reason about

```python
# ✅ Pure
def add(x, y):
    return x + y

# ❌ Impure (side effect)
total = 0
def add_to_total(x):
    global total
    total += x
```

### Immutability
- Don't modify data in place
- Create new data structures

```python
# ✅ Immutable
def add_item(items, item):
    return items + [item]

# ❌ Mutable
def add_item(items, item):
    items.append(item)
    return items
```

### Function Composition
- Build complex operations from simple ones
- Each function does one thing well

```python
# Compose simple functions
transform = pipe(
    parse_csv,
    filter_valid,
    calculate_totals,
    format_output
)
```

---

## Performance Considerations

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| map/filter | O(n) | O(1) | Lazy (iterator) |
| List comp | O(n) | O(n) | Eager (list) |
| reduce | O(n) | O(1) | Eager |
| partial | O(1) | O(k) | k = frozen args |
| compose | O(n) | O(1) | n = functions |
| groupby | O(n) | O(k) | k = group size |

**When to Use Each:**
- **List comprehensions:** Most Pythonic, readable
- **map/filter:** Existing function, lazy evaluation needed
- **reduce:** No comprehension alternative
- **itertools:** Large datasets, memory efficiency

---

## Common Patterns

### Pipeline Pattern
```python
result = pipe(
    extract,
    transform,
    validate,
    load
)(data)
```

### Validation Chain
```python
validate = compose_validators(
    not_empty,
    min_length(5),
    is_email
)
```

### Memoization
```python
@memoize
def expensive_function(n):
    return complex_calculation(n)
```

### Partial Configuration
```python
api_get = partial(api_request, method='GET', headers=default_headers)
api_post = partial(api_request, method='POST', headers=default_headers)
```

---

## Learning Outcomes

After completing Week 4, you should be able to:

✅ Transform data with map, filter, reduce  
✅ Write appropriate lambda functions  
✅ Create specialized functions with partial  
✅ Build composable data pipelines  
✅ Implement higher-order functions  
✅ Use itertools efficiently  
✅ Apply functional programming principles  
✅ Choose between functional and imperative styles  

---

## Running the Exercises

```bash
# Run individual days
python day1_map_filter_reduce.py
python day2_lambda_functions.py
python day3_partial_functions.py
python day4_compose_pipe.py
python day5_higher_order_functions.py
python day6_itertools_functional.py
python day7_review_challenge.py

# Run all at once
for day in day*.py; do
    echo "Running $day..."
    python "$day"
    echo ""
done
```

---

## Additional Resources

**Official Documentation:**
- [functools module](https://docs.python.org/3/library/functools.html)
- [itertools module](https://docs.python.org/3/library/itertools.html)
- [operator module](https://docs.python.org/3/library/operator.html)
- [Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html)

**Further Reading:**
- [Functional Programming in Python](https://realpython.com/python-functional-programming/)
- [Python Functional Programming](https://www.oreilly.com/library/view/functional-programming-in/9781492048633/)

---

## Next Steps

🎯 **Week 5:** Decorators  
Learn to write powerful decorators for cross-cutting concerns.

---

## Notes

- Functional programming is a tool, not a religion
- Use when it improves clarity and maintainability
- Python is multi-paradigm - mix styles appropriately
- Comprehensions are often more Pythonic than map/filter
- itertools is your friend for large datasets

**Time Investment:** ~10-15 minutes per day, 15-20 minutes for Day 7  
**Total:** ~90 minutes for the week

---

*Happy functional programming! 🐍*

