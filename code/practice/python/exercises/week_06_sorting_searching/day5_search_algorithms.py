"""
Week 6, Day 5: Advanced Search Algorithms

Learning Objectives:
- Master linear search variants
- Learn interpolation search
- Understand exponential search
- Practice jump search
- Apply search algorithms to problems

Time: 10-15 minutes
"""

import math

# ============================================================
# EXERCISE 1: Linear Search Variants
# ============================================================

def linear_search_variants():
    """
    Implement linear search and variants.
    
    Linear search: Check each element sequentially
    """
    print("--- Exercise 1: Linear Search Variants ---")
    
    def linear_search(arr, target):
        """Basic linear search"""
        for i, val in enumerate(arr):
            if val == target:
                return i
        return -1
    
    def linear_search_all(arr, target):
        """Find all occurrences"""
        return [i for i, val in enumerate(arr) if val == target]
    
    def linear_search_sentinel(arr, target):
        """Linear search with sentinel"""
        n = len(arr)
        last = arr[n - 1]
        arr[n - 1] = target
        
        i = 0
        while arr[i] != target:
            i += 1
        
        arr[n - 1] = last
        
        if i < n - 1 or arr[n - 1] == target:
            return i
        return -1
    
    numbers = [4, 2, 7, 1, 9, 2, 5]
    
    print(f"Array: {numbers}")
    print(f"Find 7: index {linear_search(numbers, 7)}")
    print(f"Find all 2: indices {linear_search_all(numbers, 2)}")
    
    print("\n💡 Linear Search: O(n) time, works on unsorted")
    
    print()

# ============================================================
# EXERCISE 2: Jump Search
# ============================================================

def jump_search_demo():
    """
    Implement jump search.
    
    Jump search: Jump ahead by blocks, then linear search
    """
    print("--- Exercise 2: Jump Search ---")
    
    def jump_search(arr, target):
        """Jump search on sorted array"""
        n = len(arr)
        step = int(math.sqrt(n))
        prev = 0
        
        # Jump to find block
        while arr[min(step, n) - 1] < target:
            prev = step
            step += int(math.sqrt(n))
            if prev >= n:
                return -1
        
        # Linear search in block
        while arr[prev] < target:
            prev += 1
            if prev == min(step, n):
                return -1
        
        if arr[prev] == target:
            return prev
        
        return -1
    
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print(f"Sorted array: {numbers}")
    
    for target in [6, 11]:
        index = jump_search(numbers, target)
        result = f"found at {index}" if index != -1 else "not found"
        print(f"  Search {target}: {result}")
    
    print("\n💡 Jump Search:")
    print("  Time: O(√n)")
    print("  Better than linear, worse than binary")
    print("  Good for: Arrays where jumping is cheaper than comparison")
    
    print()

# ============================================================
# EXERCISE 3: Interpolation Search
# ============================================================

def interpolation_search_demo():
    """
    Implement interpolation search.
    
    Interpolation: Estimate position based on value
    """
    print("--- Exercise 3: Interpolation Search ---")
    
    def interpolation_search(arr, target):
        """Interpolation search on uniformly distributed sorted array"""
        low = 0
        high = len(arr) - 1
        
        while low <= high and target >= arr[low] and target <= arr[high]:
            if low == high:
                if arr[low] == target:
                    return low
                return -1
            
            # Estimate position
            pos = low + int(((target - arr[low]) / (arr[high] - arr[low])) * (high - low))
            
            if arr[pos] == target:
                return pos
            elif arr[pos] < target:
                low = pos + 1
            else:
                high = pos - 1
        
        return -1
    
    # Uniformly distributed array
    numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    
    print(f"Array: {numbers}")
    
    for target in [50, 55]:
        index = interpolation_search(numbers, target)
        result = f"found at {index}" if index != -1 else "not found"
        print(f"  Search {target}: {result}")
    
    print("\n💡 Interpolation Search:")
    print("  Time: O(log log n) for uniform data, O(n) worst")
    print("  Better than binary for uniform distribution")
    print("  Good for: Uniformly distributed data")
    
    print()

# ============================================================
# EXERCISE 4: Exponential Search
# ============================================================

def exponential_search_demo():
    """
    Implement exponential search.
    
    Exponential: Find range, then binary search
    """
    print("--- Exercise 4: Exponential Search ---")
    
    def binary_search(arr, target, left, right):
        """Binary search in range"""
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    
    def exponential_search(arr, target):
        """Exponential search on sorted array"""
        if not arr:
            return -1
        
        if arr[0] == target:
            return 0
        
        # Find range for binary search
        i = 1
        while i < len(arr) and arr[i] <= target:
            i *= 2
        
        # Binary search in range
        return binary_search(arr, target, i // 2, min(i, len(arr) - 1))
    
    numbers = list(range(1, 101))
    
    print(f"Array: [1, 2, 3, ..., 100]")
    
    for target in [50, 101]:
        index = exponential_search(numbers, target)
        result = f"found at {index}" if index != -1 else "not found"
        print(f"  Search {target}: {result}")
    
    print("\n💡 Exponential Search:")
    print("  Time: O(log n)")
    print("  Good for: Unbounded/infinite arrays")
    print("  Better than binary when target is near beginning")
    
    print()

# ============================================================
# EXERCISE 5: Ternary Search
# ============================================================

def ternary_search_demo():
    """
    Implement ternary search.
    
    Ternary: Divide into 3 parts instead of 2
    """
    print("--- Exercise 5: Ternary Search ---")
    
    def ternary_search(arr, target):
        """Ternary search on sorted array"""
        left, right = 0, len(arr) - 1
        
        while left <= right:
            # Two midpoints
            mid1 = left + (right - left) // 3
            mid2 = right - (right - left) // 3
            
            if arr[mid1] == target:
                return mid1
            if arr[mid2] == target:
                return mid2
            
            if target < arr[mid1]:
                right = mid1 - 1
            elif target > arr[mid2]:
                left = mid2 + 1
            else:
                left = mid1 + 1
                right = mid2 - 1
        
        return -1
    
    numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    
    print(f"Array: {numbers}")
    
    for target in [7, 10]:
        index = ternary_search(numbers, target)
        result = f"found at {index}" if index != -1 else "not found"
        print(f"  Search {target}: {result}")
    
    print("\n💡 Ternary Search:")
    print("  Time: O(log₃ n) ≈ O(log n)")
    print("  More comparisons than binary search")
    print("  Useful for: Finding maximum/minimum in unimodal functions")
    
    print()

# ============================================================
# EXERCISE 6: Real-World Scenario - Finding Rotation Point
# ============================================================

def find_rotation_point():
    """
    Find rotation point in rotated sorted array.
    
    TODO: Find minimum element (rotation point)
    """
    print("--- Exercise 6: Find Rotation Point ---")
    
    def find_min(arr):
        """Find minimum in rotated sorted array"""
        left, right = 0, len(arr) - 1
        
        while left < right:
            mid = (left + right) // 2
            
            if arr[mid] > arr[right]:
                # Minimum is in right half
                left = mid + 1
            else:
                # Minimum is in left half (or mid)
                right = mid
        
        return left
    
    arrays = [
        [4, 5, 6, 7, 0, 1, 2],
        [3, 4, 5, 1, 2],
        [1, 2, 3, 4, 5],
    ]
    
    for arr in arrays:
        min_idx = find_min(arr)
        print(f"Array: {arr}")
        print(f"  Rotation point (min): index {min_idx}, value {arr[min_idx]}")
    
    print()

# ============================================================
# EXERCISE 7: Search in 2D Matrix
# ============================================================

def search_2d_matrix():
    """
    Search in sorted 2D matrix.
    
    TODO: Efficient search in matrix
    """
    print("--- Exercise 7: Search in 2D Matrix ---")
    
    def search_matrix(matrix, target):
        """Search in row-wise and column-wise sorted matrix"""
        if not matrix or not matrix[0]:
            return False
        
        rows, cols = len(matrix), len(matrix[0])
        row, col = 0, cols - 1  # Start top-right
        
        while row < rows and col >= 0:
            if matrix[row][col] == target:
                return True, (row, col)
            elif matrix[row][col] > target:
                col -= 1  # Move left
            else:
                row += 1  # Move down
        
        return False, None
    
    matrix = [
        [1,  4,  7,  11],
        [2,  5,  8,  12],
        [3,  6,  9,  16],
        [10, 13, 14, 17]
    ]
    
    print("Matrix:")
    for row in matrix:
        print(f"  {row}")
    
    for target in [5, 20]:
        found, pos = search_matrix(matrix, target)
        if found:
            print(f"\n{target} found at {pos}")
        else:
            print(f"\n{target} not found")
    
    print()

# ============================================================
# BONUS CHALLENGE: Find Peak in 2D Array
# ============================================================

def find_peak_2d():
    """
    Find peak element in 2D array.
    
    Peak: Greater than all neighbors
    """
    print("--- Bonus Challenge: Find Peak in 2D ---")
    
    def find_peak_element_2d(matrix):
        """Find a peak element in 2D matrix"""
        if not matrix or not matrix[0]:
            return None
        
        rows, cols = len(matrix), len(matrix[0])
        low, high = 0, cols - 1
        
        while low <= high:
            mid = (low + high) // 2
            
            # Find max in column mid
            max_row = 0
            for i in range(rows):
                if matrix[i][mid] > matrix[max_row][mid]:
                    max_row = i
            
            # Check if it's a peak
            left_ok = mid == 0 or matrix[max_row][mid] > matrix[max_row][mid - 1]
            right_ok = mid == cols - 1 or matrix[max_row][mid] > matrix[max_row][mid + 1]
            
            if left_ok and right_ok:
                return (max_row, mid), matrix[max_row][mid]
            elif not left_ok:
                high = mid - 1
            else:
                low = mid + 1
        
        return None
    
    matrix = [
        [10, 8,  10, 10],
        [14, 13, 12, 11],
        [15, 9,  11, 21],
        [16, 17, 19, 20]
    ]
    
    print("Matrix:")
    for row in matrix:
        print(f"  {row}")
    
    result = find_peak_2d(matrix)
    if result:
        pos, val = result
        print(f"\nPeak found at {pos}: value {val}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_summary():
    """
    Summary of search algorithms.
    """
    print("=" * 60)
    print("SEARCH ALGORITHMS SUMMARY")
    print("=" * 60)
    
    algorithms = [
        ("Linear Search", "O(n)", "Unsorted", "Simple"),
        ("Binary Search", "O(log n)", "Sorted", "Most common"),
        ("Jump Search", "O(√n)", "Sorted", "Block jumping"),
        ("Interpolation", "O(log log n)*", "Sorted+Uniform", "Value-based"),
        ("Exponential", "O(log n)", "Sorted+Unbounded", "Range finding"),
        ("Ternary", "O(log n)", "Sorted/Unimodal", "3-way split"),
    ]
    
    print(f"\n{'Algorithm':<18} {'Time':<15} {'Requirement':<20} {'Note'}")
    print("-" * 60)
    
    for name, time, req, note in algorithms:
        print(f"{name:<18} {time:<15} {req:<20} {note}")
    
    print("\n* O(n) worst case for interpolation")
    print("\n" + "=" * 60)
    print()

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 6, Day 5: Advanced Search Algorithms")
    print("=" * 60)
    print()
    
    linear_search_variants()
    jump_search_demo()
    interpolation_search_demo()
    exponential_search_demo()
    ternary_search_demo()
    find_rotation_point()
    search_2d_matrix()
    find_peak_2d()
    complexity_summary()
    
    print("=" * 60)
    print("✅ Day 5 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Binary search is most common for sorted data")
    print("2. Interpolation good for uniform distribution")
    print("3. Exponential good for unbounded arrays")
    print("4. Choose algorithm based on data characteristics")

