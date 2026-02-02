# Sorting Algorithm Comparison - Beginner

Comparing sorting algorithms with real performance numbers.

## Learning Objectives
- Understand Big-O vs real performance
- Calculate sorting times for different sizes
- Choose the right algorithm for the job

## Background

### Sorting Complexity
| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Mergesort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Heapsort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Timsort | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| Radix | O(nk) | O(nk) | O(nk) | O(n+k) | Yes |

### Real-World Performance (ns per element)
| n | Quicksort | Mergesort | Std::sort | Python sorted |
|---|-----------|-----------|-----------|---------------|
| 1K | 50 | 60 | 45 | 500 |
| 1M | 80 | 100 | 70 | 800 |
| 1B | 100 | 120 | 90 | 1000 |

---

## Exercise 1: Time Calculation

**Question:** Sort arrays of different sizes using Quicksort.
Assume ~100 ns per element for large arrays.

1. 1,000 elements
2. 1,000,000 elements
3. 1,000,000,000 elements

**Your Answer:**
```
1K elements = ?
1M elements = ?
1B elements = ?
```

<details>
<summary>Solution</summary>

```
Formula: Time ≈ n × log(n) × constant

For quick estimation with 100 ns/element:

1,000 elements:
  n log n = 1,000 × 10 = 10,000 ops
  Time ≈ 1,000 × 100 ns = 100 μs = 0.1 ms

1,000,000 elements:
  n log n = 1M × 20 = 20M ops
  Time ≈ 1M × 100 ns = 100 ms

1,000,000,000 elements:
  n log n = 1B × 30 = 30B ops
  Time ≈ 1B × 100 ns = 100 seconds

Note: Memory becomes the bottleneck for 1B elements
(4 GB of integers won't fit in cache).
```
</details>

---

## Exercise 2: Algorithm Selection

**Question:** Which sort for each scenario?

1. Sort 100 elements that are almost sorted
2. Sort 1 billion integers (0-1000 range)
3. Sort strings where stability matters
4. Sort in embedded system with 1 KB RAM
5. Sort during game loop (must be consistent time)

**Your Answer:**
```
1. Almost sorted = ?
2. Billion integers = ?
3. Stable string sort = ?
4. Minimal RAM = ?
5. Consistent time = ?
```

<details>
<summary>Solution</summary>

```
1. Almost Sorted (100 elements):
   Timsort or Insertion Sort
   Reason: Timsort is O(n) for sorted data
   Insertion sort also O(n) for nearly sorted

2. Billion Integers (0-1000 range):
   Counting Sort or Radix Sort
   Reason: O(n) vs O(n log n)
   1B × 30 = 30B ops (comparison) vs 1B × 3 = 3B ops (radix)
   10x faster!

3. Stable String Sort:
   Mergesort or Timsort
   Reason: Both stable and efficient
   Python's sorted() uses Timsort

4. Minimal RAM (1 KB):
   Heapsort
   Reason: O(1) extra space
   Quicksort needs O(log n) stack space

5. Game Loop (Consistent Time):
   Heapsort or Mergesort
   Reason: Guaranteed O(n log n) worst case
   Quicksort can degrade to O(n²)
   Games need predictable frame times
```
</details>

---

## Exercise 3: Constant Factors

**Question:** Two algorithms:
- Mergesort: n log n comparisons, but extra memory allocation
- Heapsort: n log n comparisons, but poor cache behavior

For 1 million integers:
- Mergesort: 20M comparisons + 4 MB allocation (1 μs)
- Heapsort: 25M comparisons, but 2x cache misses

Comparison: 5 ns, Cache miss: 100 ns

**Your Answer:**
```
Mergesort time = ?
Heapsort time = ?
Which is faster = ?
```

<details>
<summary>Solution</summary>

```
Mergesort:
  Comparisons: 20M × 5 ns = 100 ms
  Allocation: 1 μs (negligible)
  Cache: Good locality, ~10% miss rate
  Cache miss cost: 20M × 0.1 × 100 ns = 200 ms
  Total: ~300 ms

Heapsort:
  Comparisons: 25M × 5 ns = 125 ms
  Cache: Poor locality, ~30% miss rate
  Cache miss cost: 25M × 0.3 × 100 ns = 750 ms
  Total: ~875 ms

Mergesort is ~3x faster despite extra memory!

Key insight: Cache behavior often matters more than
operation count. This is why Mergesort and Timsort
are preferred in practice.
```
</details>

---

## Exercise 4: Partial Sorting

**Question:** Find top 100 from 1 million elements.

Compare:
1. Full sort, take first 100
2. Partial sort (heap-based selection)

**Your Answer:**
```
Full sort time = ?
Partial sort time = ?
Speedup = ?
```

<details>
<summary>Solution</summary>

```
Full Sort:
  Operations: 1M × log(1M) = 20M
  Time: 100 ms (from previous)

Partial Sort (Heap Selection):
  Build min-heap of k elements: 100 ops
  Scan remaining: n - k comparisons
  Each might replace heap top: log k
  Worst case: (n - k) × log k = 1M × 7 = 7M ops
  
  Or use: Quickselect (average O(n))
  Operations: ~3 × n = 3M
  Time: 3M × 5 ns = 15 ms

Speedup:
  Full sort: 100 ms
  Partial sort: 15 ms
  Speedup: 6-7x faster!

Use std::partial_sort or heapq.nsmallest for this.
```
</details>

---

## Exercise 5: Sorting Strings vs Integers

**Question:** Sort 1 million elements:
1. Integers (4 bytes each)
2. Strings (average 50 characters)

Both using comparison-based sort.

**Your Answer:**
```
Integer sort time = ?
String sort time = ?
Why the difference = ?
```

<details>
<summary>Solution</summary>

```
Integer Sort:
  Comparisons: 20M
  Time per comparison: 1-2 cycles = 1 ns
  Total: 20 ms

String Sort:
  Comparisons: 20M
  Time per comparison: 
    - String compare: ~50 character comparisons
    - Or early exit at first difference
    - Average: ~10 character comparisons
    - Plus: Cache miss for string data
  Time per comparison: ~100-500 ns
  Total: 2-10 seconds!

Difference: 100-500x slower for strings!

Why:
1. String comparison is O(length)
2. Strings are scattered in memory (pointer chasing)
3. Each string access may cache miss

Optimization:
- Radix sort on strings
- Sort indices with string comparison
- Use string hashing for grouping
```
</details>

---

## Exercise 6: Python vs C Performance

**Question:** Sort 1 million integers:
- C++ std::sort: 70 ms
- Python sorted(): 700 ms

Why 10x difference? What can you do?

**Your Answer:**
```
Reason for difference = ?
Ways to improve Python = ?
```

<details>
<summary>Solution</summary>

```
Reasons for Difference:
1. Interpreter overhead: Each comparison is Python bytecode
2. Object overhead: Python int is 28 bytes, not 4
3. Indirection: List contains pointers to objects
4. Type checking: Dynamic typing on each operation

Ways to Improve:

1. Use NumPy:
   import numpy as np
   arr = np.array(data)
   np.sort(arr)  # C implementation
   Time: ~80 ms (near C speed!)

2. Use key functions wisely:
   # Bad: Creates intermediate list
   sorted(data, key=lambda x: x.value)
   
   # Good: operator.attrgetter is C
   from operator import attrgetter
   sorted(data, key=attrgetter('value'))

3. Use itemgetter for tuples:
   from operator import itemgetter
   sorted(tuples, key=itemgetter(0))

4. For extreme cases: Cython or PyPy
   PyPy: 3-10x faster for pure Python
   Cython: Near C performance

NumPy brings Python within 10-20% of C for numeric work.
```
</details>

---

## Key Takeaways

1. **Big-O isn't everything**: Constants and cache matter
2. **Timsort wins for real data**: Usually partially sorted
3. **Radix sort for integers**: O(n) beats O(n log n) for large n
4. **Strings are expensive**: Comparison cost + cache misses
5. **Use NumPy for Python**: 10x speedup for numeric sorting

## Quick Reference
```
1M integers (C++): ~70 ms
1M integers (Python): ~700 ms
1M integers (NumPy): ~80 ms

Top-K selection: Use partial_sort (6x faster than full sort)
```

## Next Steps
- Try [Intermediate: Search Algorithm Comparison](../intermediate/search_comparison.md)
- Learn about [Platform Comparison](../../07_platform_comparison/beginner/x86_vs_arm.md)
