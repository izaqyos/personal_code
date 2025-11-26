"""
Week 6, Day 2: Binary Search and bisect Module

Learning Objectives:
- Master binary search algorithm
- Learn bisect module for sorted lists
- Understand bisect_left vs bisect_right
- Practice insertion into sorted lists
- Apply binary search to real problems

Time: 10-15 minutes
"""

import bisect
from typing import List

# ============================================================
# EXERCISE 1: Binary Search Implementation
# ============================================================

def binary_search_implementation():
    """
    Implement binary search from scratch.
    
    Binary search: O(log n) search in sorted array
    """
    print("--- Exercise 1: Binary Search Implementation ---")
    
    def binary_search(arr, target):
        """Find target in sorted array"""
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1  # Not found
    
    numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    
    print(f"Array: {numbers}")
    
    test_values = [7, 10, 1, 19, 20]
    for val in test_values:
        index = binary_search(numbers, val)
        if index != -1:
            print(f"  {val} found at index {index}")
        else:
            print(f"  {val} not found")
    
    print()

# ============================================================
# EXERCISE 2: Recursive Binary Search
# ============================================================

def recursive_binary_search():
    """
    Implement recursive binary search.
    
    TODO: Practice recursive approach
    """
    print("--- Exercise 2: Recursive Binary Search ---")
    
    def binary_search_recursive(arr, target, left=0, right=None):
        """Recursive binary search"""
        if right is None:
            right = len(arr) - 1
        
        if left > right:
            return -1
        
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            return binary_search_recursive(arr, target, mid + 1, right)
        else:
            return binary_search_recursive(arr, target, left, mid - 1)
    
    numbers = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    
    print(f"Array: {numbers}")
    
    for val in [8, 15, 2, 20]:
        index = binary_search_recursive(numbers, val)
        result = f"found at index {index}" if index != -1 else "not found"
        print(f"  {val}: {result}")
    
    print()

# ============================================================
# EXERCISE 3: bisect Module Basics
# ============================================================

def bisect_module_basics():
    """
    Learn bisect module for sorted lists.
    
    bisect: Find insertion point in sorted list
    """
    print("--- Exercise 3: bisect Module Basics ---")
    
    numbers = [1, 3, 5, 7, 9]
    
    print(f"Sorted list: {numbers}")
    
    # bisect_right (default): Insert after existing values
    pos_right = bisect.bisect_right(numbers, 5)
    print(f"\nbisect_right(5): {pos_right}")
    print(f"  Would insert after existing 5")
    
    # bisect_left: Insert before existing values
    pos_left = bisect.bisect_left(numbers, 5)
    print(f"\nbisect_left(5): {pos_left}")
    print(f"  Would insert before existing 5")
    
    # For non-existing value, both are same
    pos = bisect.bisect(numbers, 6)
    print(f"\nbisect(6): {pos}")
    print(f"  Value doesn't exist, so left==right")
    
    print()

# ============================================================
# EXERCISE 4: Inserting into Sorted List
# ============================================================

def inserting_sorted():
    """
    Use bisect.insort to maintain sorted order.
    
    TODO: Practice maintaining sorted lists
    """
    print("--- Exercise 4: Inserting into Sorted List ---")
    
    numbers = [1, 3, 5, 7, 9]
    print(f"Initial: {numbers}")
    
    # Insert values while maintaining sort
    values_to_insert = [4, 2, 8, 5]
    
    for val in values_to_insert:
        bisect.insort(numbers, val)
        print(f"After inserting {val}: {numbers}")
    
    # insort_left vs insort_right for duplicates
    numbers2 = [1, 3, 5, 5, 5, 7, 9]
    print(f"\nWith duplicates: {numbers2}")
    
    bisect.insort_left(numbers2, 5)
    print(f"After insort_left(5): {numbers2}")
    
    bisect.insort_right(numbers2, 5)
    print(f"After insort_right(5): {numbers2}")
    
    print()

# ============================================================
# EXERCISE 5: Finding Range of Values
# ============================================================

def finding_range():
    """
    Find range of values in sorted array.
    
    TODO: Find first and last occurrence
    """
    print("--- Exercise 5: Finding Range ---")
    
    def find_range(arr, target):
        """Find first and last index of target"""
        left = bisect.bisect_left(arr, target)
        right = bisect.bisect_right(arr, target)
        
        if left == right:  # Not found
            return -1, -1
        
        return left, right - 1
    
    numbers = [1, 2, 2, 2, 3, 4, 4, 5]
    
    print(f"Array: {numbers}")
    
    for val in [2, 4, 6]:
        first, last = find_range(numbers, val)
        if first == -1:
            print(f"  {val}: not found")
        else:
            print(f"  {val}: indices {first} to {last} (count: {last - first + 1})")
    
    print()

# ============================================================
# EXERCISE 6: Real-World Scenario - Grade Boundaries
# ============================================================

def grade_boundaries():
    """
    Assign grades based on score boundaries.
    
    TODO: Use bisect for grade assignment
    """
    print("--- Exercise 6: Grade Boundaries ---")
    
    # Grade boundaries (sorted)
    boundaries = [60, 70, 80, 90]
    grades = ['F', 'D', 'C', 'B', 'A']
    
    def get_grade(score):
        """Get letter grade for score"""
        index = bisect.bisect(boundaries, score)
        return grades[index]
    
    students = [
        ('Alice', 95),
        ('Bob', 82),
        ('Charlie', 67),
        ('Diana', 58),
        ('Eve', 91),
    ]
    
    print("Grade assignments:")
    for name, score in students:
        grade = get_grade(score)
        print(f"  {name}: {score} → {grade}")
    
    print()

# ============================================================
# EXERCISE 7: Searching in Rotated Array
# ============================================================

def search_rotated():
    """
    Search in rotated sorted array.
    
    TODO: Modified binary search for rotated array
    """
    print("--- Exercise 7: Rotated Array Search ---")
    
    def search_rotated_array(arr, target):
        """Search in rotated sorted array"""
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return mid
            
            # Determine which half is sorted
            if arr[left] <= arr[mid]:  # Left half is sorted
                if arr[left] <= target < arr[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:  # Right half is sorted
                if arr[mid] < target <= arr[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        
        return -1
    
    # Rotated sorted array
    arr = [4, 5, 6, 7, 0, 1, 2]
    
    print(f"Rotated array: {arr}")
    
    for val in [0, 3, 5, 7]:
        index = search_rotated_array(arr, val)
        result = f"found at index {index}" if index != -1 else "not found"
        print(f"  {val}: {result}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Finding Peak Element
# ============================================================

def find_peak():
    """
    Find peak element using binary search.
    
    Peak: Element greater than neighbors
    """
    print("--- Bonus Challenge: Find Peak Element ---")
    
    def find_peak_element(arr):
        """Find any peak element"""
        left, right = 0, len(arr) - 1
        
        while left < right:
            mid = (left + right) // 2
            
            if arr[mid] < arr[mid + 1]:
                # Peak is on right
                left = mid + 1
            else:
                # Peak is on left (or mid is peak)
                right = mid
        
        return left
    
    arrays = [
        [1, 2, 3, 1],
        [1, 2, 1, 3, 5, 6, 4],
        [1, 2, 3, 4, 5],
    ]
    
    for arr in arrays:
        peak_idx = find_peak_element(arr)
        print(f"Array: {arr}")
        print(f"  Peak at index {peak_idx}: {arr[peak_idx]}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Binary Search:
    - Time: O(log n)
    - Space: O(1) iterative, O(log n) recursive (call stack)
    - Requires: Sorted array
    
    bisect Module:
    - bisect_left/right: O(log n)
    - insort: O(n) - insertion is O(n), finding position is O(log n)
    
    Linear Search vs Binary Search:
    - Linear: O(n), works on unsorted
    - Binary: O(log n), requires sorted
    - Breakeven: ~7 elements
    
    Benefits:
    - Much faster than linear for large datasets
    - Predictable performance
    - Simple to implement
    
    Limitations:
    - Requires sorted data
    - Random access needed (arrays, not linked lists)
    - Sorting cost: O(n log n)
    
    Use Cases:
    - Searching sorted data
    - Finding insertion points
    - Range queries
    - Closest value searches
    - Threshold/boundary problems
    
    Best Practices:
    - Use bisect module (well-tested, optimized)
    - Consider sorting cost
    - Handle edge cases (empty, single element)
    - Use bisect_left for "at least" queries
    - Use bisect_right for "at most" queries
    
    Common Patterns:
    - Find exact match
    - Find insertion point
    - Find range (first/last occurrence)
    - Find closest value
    - Threshold-based decisions
    
    Security Considerations:
    - Validate array bounds
    - Handle integer overflow in mid calculation
    - Consider worst-case performance
    - Validate sorted assumption
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 6, Day 2: Binary Search")
    print("=" * 60)
    print()
    
    binary_search_implementation()
    recursive_binary_search()
    bisect_module_basics()
    inserting_sorted()
    finding_range()
    grade_boundaries()
    search_rotated()
    find_peak()
    
    print("=" * 60)
    print("✅ Day 2 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Binary search: O(log n) on sorted arrays")
    print("2. bisect module for insertion points")
    print("3. bisect_left vs bisect_right for duplicates")
    print("4. Many problems reduce to binary search")

