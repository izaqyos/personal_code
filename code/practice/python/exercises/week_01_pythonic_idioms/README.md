# Week 1: Pythonic Idioms

Master the art of writing clean, idiomatic Python code.

## Overview

This week focuses on Python-specific patterns and idioms that make code more readable, efficient, and "Pythonic". These are the building blocks of professional Python development.

## Daily Exercises

### Day 1: List Comprehensions vs Generator Expressions
**File:** `day1_list_vs_generator.py`

Learn when to use list comprehensions vs generator expressions for memory efficiency.

**Key Concepts:**
- List comprehensions for small to medium datasets
- Generator expressions for large datasets or streaming
- Memory profiling with `sys.getsizeof()`
- Performance trade-offs

**Exercises:**
- Compare memory usage between lists and generators
- Implement filtering and transformation patterns
- Process large file simulations
- Build generator pipelines

---

### Day 2: Dictionary Comprehensions and defaultdict
**File:** `day2_dict_defaultdict.py`

Master dictionary operations and learn when to use `defaultdict`.

**Key Concepts:**
- Dictionary comprehensions for transformations
- `defaultdict` for avoiding KeyError
- Grouping and counting patterns
- Dictionary merging techniques

**Exercises:**
- Transform data with dict comprehensions
- Group data by keys
- Count frequencies
- Analyze log files

---

### Day 3: Unpacking and Tuple Swapping
**File:** `day3_unpacking_tuples.py`

Learn advanced unpacking patterns for cleaner code.

**Key Concepts:**
- Basic and extended unpacking with `*`
- Tuple vs list usage
- Unpacking in function calls
- Nested structure destructuring

**Exercises:**
- Swap variables without temp
- Unpack function returns
- Process CSV-like data
- Use `*args` and `**kwargs`

---

### Day 4: Context Managers
**File:** `day4_context_managers.py`

Implement custom context managers for resource management.

**Key Concepts:**
- `__enter__` and `__exit__` protocol
- Guaranteed cleanup with exceptions
- Custom context managers
- Nested contexts

**Exercises:**
- Build a Timer context manager
- Implement database connection manager
- Create file lock mechanism
- Handle temporary resources

---

### Day 5: EAFP vs LBYL
**File:** `day5_eafp_lbyl.py`

Understand Pythonic exception handling patterns.

**Key Concepts:**
- EAFP: Easier to Ask for Forgiveness than Permission
- LBYL: Look Before You Leap
- When to use each approach
- Duck typing with EAFP

**Exercises:**
- Compare both approaches
- Handle file operations
- Implement duck typing
- Parse API responses safely

---

### Day 6: Chaining Comparisons and Walrus Operator
**File:** `day6_chaining_walrus.py`

Master comparison chaining and the walrus operator (`:=`).

**Key Concepts:**
- Chained comparisons: `a < b < c`
- Walrus operator for assignment expressions
- Avoiding duplicate computation
- When NOT to use walrus

**Exercises:**
- Write readable range checks
- Use `:=` in comprehensions
- Process files with walrus
- Combine chaining and walrus

---

### Day 7: Review & Mini-Challenge
**File:** `day7_review_challenge.py`

Apply all Week 1 concepts in comprehensive challenges.

**Challenges:**
1. Refactor non-Pythonic code
2. Build data processing pipeline
3. Create performance monitor
4. Comprehensive user activity analyzer

**Assessment:**
- Self-assessment checklist
- Performance comparisons
- Real-world scenarios

---

## Running the Exercises

Each day's file can be run independently:

```bash
# Run a specific day
python day1_list_vs_generator.py

# Or run all days in sequence
for day in day*.py; do
    echo "Running $day"
    python "$day"
    echo ""
done
```

## Key Takeaways

1. **List vs Generator**: Use generators for large datasets to save memory
2. **defaultdict**: Eliminates key existence checks for cleaner code
3. **Unpacking**: Makes code more readable and Pythonic
4. **Context Managers**: Guarantee resource cleanup
5. **EAFP**: More Pythonic than LBYL, handles race conditions
6. **Walrus Operator**: Avoid duplicate computation in expressions
7. **Chaining**: Write readable range checks

## Performance Tips

- Generators use ~200 bytes regardless of data size
- Lists use ~8 bytes per element + overhead
- `defaultdict` is faster than manual key checks
- EAFP is faster when exceptions are rare (<1%)
- Walrus operator can provide 2x speedup by avoiding recomputation

## Security Considerations

- Validate input sizes when building collections from external data
- Use EAFP to prevent TOCTOU (Time-of-Check-Time-of-Use) vulnerabilities
- Be careful with `pickle` and untrusted data
- Sanitize user input before using in dict keys or file operations

## Next Steps

After completing Week 1, you should be comfortable with:
- Writing Pythonic code that's readable and efficient
- Choosing the right data structure for the task
- Managing resources properly
- Handling errors gracefully

**Continue to:** Week 2 - Iterator Protocol & Generators

---

## Additional Resources

- [PEP 8](https://peps.python.org/pep-0008/) - Style Guide for Python Code
- [PEP 20](https://peps.python.org/pep-0020/) - The Zen of Python
- [PEP 572](https://peps.python.org/pep-0572/) - Assignment Expressions (Walrus Operator)
- [Python Documentation](https://docs.python.org/3/) - Official Python docs

## Practice Tips

1. Try to refactor your existing code using these idioms
2. Do code reviews looking for non-Pythonic patterns
3. Practice explaining why one approach is more Pythonic
4. Time yourself - aim to complete each day in 10-15 minutes

---

**Week 1 Status:** ✅ Complete  
**Estimated Time:** 10-15 minutes per day  
**Difficulty:** ⭐⭐☆☆☆ (Beginner to Intermediate)

