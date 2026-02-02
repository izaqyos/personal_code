# Big-O Analysis

Understanding algorithmic complexity for performance prediction.

## Time Complexity Classes

| Complexity | Name | 1K | 1M | 1B |
|------------|------|-----|-----|-----|
| O(1) | Constant | 1 | 1 | 1 |
| O(log n) | Logarithmic | 10 | 20 | 30 |
| O(n) | Linear | 1K | 1M | 1B |
| O(n log n) | Linearithmic | 10K | 20M | 30B |
| O(n²) | Quadratic | 1M | 1T | 1E18 |
| O(n³) | Cubic | 1B | 1E18 | 1E27 |
| O(2ⁿ) | Exponential | 1E301 | ∞ | ∞ |

## Common Operations

### Data Structures

| Structure | Access | Search | Insert | Delete |
|-----------|--------|--------|--------|--------|
| Array | O(1) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1) | O(1) |
| Hash Table | O(1)* | O(1)* | O(1)* | O(1)* |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) |
| Heap | O(n) | O(n) | O(log n) | O(log n) |

*Average case; worst case O(n)

### Sorting Algorithms

| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Mergesort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Heapsort | O(n log n) | O(n log n) | O(n log n) | O(1) |
| Timsort | O(n) | O(n log n) | O(n log n) | O(n) |
| Radix | O(nk) | O(nk) | O(nk) | O(n+k) |

## Beyond Big-O

### Constants Matter
```python
# Both O(n), but very different performance
def fast_sum(arr):  # ~1 op per element
    return sum(arr)

def slow_sum(arr):  # ~100 ops per element
    total = 0
    for x in arr:
        for _ in range(100):
            total += x / 100
    return total
```

### Cache Effects
```python
# Both O(n), vastly different real performance
def sequential(arr):  # Cache-friendly
    return sum(arr)

def random_access(arr, indices):  # Cache-hostile
    return sum(arr[i] for i in indices)

# Random can be 10-100x slower for large arrays
```

### Memory Allocation
```python
# O(n) but allocates n times
def slow_build():
    result = []
    for i in range(1000000):
        result.append(i)  # May reallocate
    return result

# O(n) with pre-allocation
def fast_build():
    return list(range(1000000))  # Single allocation
```

## Amortized Analysis

### Dynamic Array (list.append)
```
Most appends: O(1)
Occasionally: O(n) when resizing

Amortized: O(1) per operation
Total for n appends: O(n)
```

### Hash Table Resize
```
Most inserts: O(1)
Resize (when load factor exceeded): O(n)

Amortized: O(1) per operation
```

## Space Complexity

### In-Place vs Extra Space
```python
# O(1) space (in-place)
def reverse_inplace(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

# O(n) space
def reverse_copy(arr):
    return arr[::-1]  # Creates new array
```

### Recursive Space
```python
# O(n) stack space
def factorial_recursive(n):
    if n <= 1: return 1
    return n * factorial_recursive(n - 1)

# O(1) space
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

## Practical Time Estimates

### At 1 Billion Operations/Second

| n | O(n) | O(n log n) | O(n²) |
|---|------|------------|-------|
| 100 | 100 ns | 664 ns | 10 μs |
| 10,000 | 10 μs | 133 μs | 100 ms |
| 1,000,000 | 1 ms | 20 ms | 16 min |
| 100,000,000 | 100 ms | 2.6 s | 115 days |

### What's Feasible?

| Time Budget | O(n) max | O(n log n) max | O(n²) max |
|-------------|----------|----------------|-----------|
| 1 ms | 1M | 50K | 1K |
| 1 second | 1B | 50M | 32K |
| 1 minute | 60B | 2B | 250K |
| 1 hour | 3.6T | 100B | 1.9M |

## Common Patterns

### Two Pointers: O(n)
```python
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return (left, right)
        elif s < target:
            left += 1
        else:
            right -= 1
```

### Binary Search: O(log n)
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

### Divide and Conquer: O(n log n)
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)  # O(n) merge
```

### Dynamic Programming: Often O(n²) or O(n × m)
```python
def longest_common_subsequence(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

## Quick Reference

### Complexity from Code Patterns
```python
# O(1): No loops depending on n
x = arr[0]

# O(log n): Halving each iteration
while n > 0:
    n //= 2

# O(n): Single loop
for x in arr:
    process(x)

# O(n log n): Linear × logarithmic
for x in arr:           # n
    binary_search(x)    # log n

# O(n²): Nested loops
for i in range(n):
    for j in range(n):
        process(i, j)

# O(2ⁿ): Recursive with branching
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)  # Two recursive calls
```

## Related Topics
- [Language Performance](language_performance.md)
- [Memory Allocation](memory_allocation.md)
