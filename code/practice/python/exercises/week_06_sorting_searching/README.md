# Week 6: Sorting & Searching Algorithms

Master essential sorting and searching algorithms for efficient data processing.

## Overview

This week focuses on sorting and searching - fundamental algorithms every programmer must know. Learn Python's built-in tools, classic algorithms, and advanced techniques for solving real-world problems efficiently.

## Daily Breakdown

### Day 1: Built-in Sorting
**File:** `day1_builtin_sorting.py`

Master Python's sorting capabilities:
- `sorted()` vs `list.sort()`
- Key functions for custom sorting
- Stable sorting with Timsort
- `operator` module for efficient keys
- Sorting complex data structures

**Key Concepts:**
- Timsort: O(n log n), stable
- Key functions extract comparison values
- `operator.itemgetter/attrgetter` faster than lambda

---

### Day 2: Binary Search
**File:** `day2_binary_search.py`

Learn efficient searching:
- Binary search implementation
- `bisect` module for sorted lists
- `bisect_left` vs `bisect_right`
- Finding ranges in sorted arrays
- Rotated array search

**Complexity:**
- Binary search: O(log n)
- Requires sorted data
- Much faster than linear for large datasets

---

### Day 3: heapq and Priority Queues
**File:** `day3_heapq_priority.py`

Master heap operations:
- Min-heap with `heapq`
- Top-k problems efficiently
- Priority queue implementation
- Merge k sorted lists
- Running median with two heaps

**Key Operations:**
- heappush/heappop: O(log n)
- nlargest/nsmallest: O(n log k)
- Better than full sorting for top-k

---

### Day 4: Custom Sorting Algorithms
**File:** `day4_custom_sorting.py`

Implement classic algorithms:
- Bubble, Selection, Insertion Sort
- Merge Sort (divide and conquer)
- Quick Sort (partitioning)
- Counting Sort (non-comparison)
- Radix Sort (digit-by-digit)

**Comparison:**
- Simple sorts: O(n²)
- Efficient sorts: O(n log n)
- Special cases: O(n) possible

---

### Day 5: Advanced Search Algorithms
**File:** `day5_search_algorithms.py`

Learn search variants:
- Linear search and variants
- Jump search: O(√n)
- Interpolation search
- Exponential search
- Ternary search
- 2D matrix search

**When to Use:**
- Binary: Sorted data (most common)
- Interpolation: Uniform distribution
- Exponential: Unbounded arrays

---

### Day 6: Two Pointers Technique
**File:** `day6_two_pointers.py`

Master pointer techniques:
- Two pointers pattern
- Fast/slow pointers
- Sliding window
- Array manipulation
- Three sum problem
- Container with most water

**Benefits:**
- O(n) time, O(1) space
- Elegant solutions
- Common interview pattern

---

### Day 7: Review & Challenge
**File:** `day7_review_challenge.py`

Apply all concepts:
- **Challenge 1:** Top k frequent elements
- **Challenge 2:** Merge intervals
- **Challenge 3:** Meeting rooms
- **Challenge 4:** Rotated array search
- **Challenge 5:** Kth largest element
- **Challenge 6:** Sort colors (Dutch flag)
- **Challenge 7:** Median from stream

---

## Quick Reference

### Sorting

```python
# Built-in sorting
sorted(items)  # Returns new list
items.sort()   # In-place

# With key function
sorted(words, key=len)
sorted(students, key=lambda s: s['grade'])

# operator module (faster)
import operator
sorted(pairs, key=operator.itemgetter(0))
sorted(students, key=operator.attrgetter('grade'))
```

### Binary Search

```python
import bisect

# Find insertion point
pos = bisect.bisect_left(arr, x)   # Before existing
pos = bisect.bisect_right(arr, x)  # After existing

# Insert maintaining sort
bisect.insort(arr, x)

# Manual binary search
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

### Heap Operations

```python
import heapq

# Create heap
heap = []
heapq.heappush(heap, item)
smallest = heapq.heappop(heap)

# Heapify list
heapq.heapify(list)

# Top k elements
largest = heapq.nlargest(k, items)
smallest = heapq.nsmallest(k, items)
```

### Two Pointers

```python
# Opposite ends
left, right = 0, len(arr) - 1
while left < right:
    # Process
    if condition:
        left += 1
    else:
        right -= 1

# Same direction (fast/slow)
slow = fast = 0
while fast < len(arr):
    # Process
    slow += 1
    fast += 2

# Sliding window
left = 0
for right in range(len(arr)):
    # Expand window
    while condition:
        # Shrink window
        left += 1
```

---

## Algorithm Complexity Summary

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| **Timsort (Python)** | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| **Insertion Sort** | O(n) | O(n²) | O(n²) | O(1) | Yes |
| **Counting Sort** | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |
| **Binary Search** | O(1) | O(log n) | O(log n) | O(1) | - |
| **Linear Search** | O(1) | O(n) | O(n) | O(1) | - |

---

## Common Patterns

### Top K Elements
```python
# Using heap - O(n log k)
k_largest = heapq.nlargest(k, items)

# Using sort - O(n log n)
k_largest = sorted(items, reverse=True)[:k]
```

### Finding Duplicates
```python
# Two pointers on sorted array
def find_duplicates(arr):
    arr.sort()
    duplicates = []
    for i in range(1, len(arr)):
        if arr[i] == arr[i-1]:
            duplicates.append(arr[i])
    return duplicates
```

### Merge Intervals
```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        if current[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], current[1])
        else:
            merged.append(current)
    
    return merged
```

---

## When to Use Each

| Problem Type | Best Algorithm |
|--------------|----------------|
| General sorting | Python's `sorted()` (Timsort) |
| Search in sorted | Binary search |
| Top k elements | Heap (nlargest/nsmallest) |
| Small range integers | Counting sort |
| Nearly sorted | Insertion sort |
| Two sum (sorted) | Two pointers |
| Subarray problems | Sliding window |
| Cycle detection | Fast/slow pointers |

---

## Learning Outcomes

After completing Week 6, you should be able to:

✅ Use Python's sorting effectively  
✅ Implement binary search variants  
✅ Apply heap operations for top-k problems  
✅ Understand classic sorting algorithms  
✅ Choose appropriate search algorithms  
✅ Use two pointers technique  
✅ Solve complex algorithmic problems  
✅ Optimize time and space complexity  

---

## Running the Exercises

```bash
# Run individual days
python day1_builtin_sorting.py
python day2_binary_search.py
python day3_heapq_priority.py
python day4_custom_sorting.py
python day5_search_algorithms.py
python day6_two_pointers.py
python day7_review_challenge.py

# Run all
for day in day*.py; do python "$day"; done
```

---

## Additional Resources

**Official Documentation:**
- [Sorting HOW TO](https://docs.python.org/3/howto/sorting.html)
- [bisect module](https://docs.python.org/3/library/bisect.html)
- [heapq module](https://docs.python.org/3/library/heapq.html)

**Further Reading:**
- [Sorting Algorithms](https://realpython.com/sorting-algorithms-python/)
- [Binary Search](https://realpython.com/binary-search-python/)

---

## Next Steps

🎯 **Week 7:** Graph & Tree Algorithms  
Learn to work with graph and tree data structures.

---

## Notes

- Python's Timsort is excellent for general use
- Binary search requires sorted data
- Heaps are perfect for top-k problems
- Two pointers solve many array problems elegantly
- Choose algorithm based on data characteristics

**Time Investment:** ~10-15 minutes per day, 15-20 minutes for Day 7  
**Total:** ~90 minutes for the week

---

*Happy sorting and searching! 🐍*

