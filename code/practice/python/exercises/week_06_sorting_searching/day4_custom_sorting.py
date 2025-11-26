"""
Week 6, Day 4: Custom Sorting Algorithms

Learning Objectives:
- Implement classic sorting algorithms
- Understand time/space complexity trade-offs
- Learn when to use each algorithm
- Practice algorithm implementation
- Compare with Python's built-in sort

Time: 10-15 minutes
"""

import random
import time

# ============================================================
# EXERCISE 1: Bubble Sort
# ============================================================

def bubble_sort_demo():
    """
    Implement bubble sort.
    
    Bubble sort: Compare adjacent elements, swap if wrong order
    """
    print("--- Exercise 1: Bubble Sort ---")
    
    def bubble_sort(arr):
        """Sort array using bubble sort"""
        n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            if not swapped:  # Optimization: stop if no swaps
                break
        return arr
    
    numbers = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {numbers}")
    
    sorted_nums = bubble_sort(numbers.copy())
    print(f"Sorted: {sorted_nums}")
    
    print("\n💡 Bubble Sort:")
    print("  Time: O(n²) worst/average, O(n) best")
    print("  Space: O(1)")
    print("  Stable: Yes")
    
    print()

# ============================================================
# EXERCISE 2: Selection Sort
# ============================================================

def selection_sort_demo():
    """
    Implement selection sort.
    
    Selection sort: Find minimum, swap with first unsorted
    """
    print("--- Exercise 2: Selection Sort ---")
    
    def selection_sort(arr):
        """Sort array using selection sort"""
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr
    
    numbers = [64, 25, 12, 22, 11]
    print(f"Original: {numbers}")
    
    sorted_nums = selection_sort(numbers.copy())
    print(f"Sorted: {sorted_nums}")
    
    print("\n💡 Selection Sort:")
    print("  Time: O(n²) always")
    print("  Space: O(1)")
    print("  Stable: No (can be made stable)")
    
    print()

# ============================================================
# EXERCISE 3: Insertion Sort
# ============================================================

def insertion_sort_demo():
    """
    Implement insertion sort.
    
    Insertion sort: Insert each element into sorted portion
    """
    print("--- Exercise 3: Insertion Sort ---")
    
    def insertion_sort(arr):
        """Sort array using insertion sort"""
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr
    
    numbers = [12, 11, 13, 5, 6]
    print(f"Original: {numbers}")
    
    sorted_nums = insertion_sort(numbers.copy())
    print(f"Sorted: {sorted_nums}")
    
    print("\n💡 Insertion Sort:")
    print("  Time: O(n²) worst, O(n) best (nearly sorted)")
    print("  Space: O(1)")
    print("  Stable: Yes")
    print("  Good for: Small arrays, nearly sorted data")
    
    print()

# ============================================================
# EXERCISE 4: Merge Sort
# ============================================================

def merge_sort_demo():
    """
    Implement merge sort.
    
    Merge sort: Divide and conquer, merge sorted halves
    """
    print("--- Exercise 4: Merge Sort ---")
    
    def merge_sort(arr):
        """Sort array using merge sort"""
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        
        return merge(left, right)
    
    def merge(left, right):
        """Merge two sorted arrays"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    numbers = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original: {numbers}")
    
    sorted_nums = merge_sort(numbers)
    print(f"Sorted: {sorted_nums}")
    
    print("\n💡 Merge Sort:")
    print("  Time: O(n log n) always")
    print("  Space: O(n)")
    print("  Stable: Yes")
    print("  Good for: Large datasets, linked lists")
    
    print()

# ============================================================
# EXERCISE 5: Quick Sort
# ============================================================

def quick_sort_demo():
    """
    Implement quick sort.
    
    Quick sort: Partition around pivot, recursively sort
    """
    print("--- Exercise 5: Quick Sort ---")
    
    def quick_sort(arr):
        """Sort array using quick sort"""
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return quick_sort(left) + middle + quick_sort(right)
    
    def quick_sort_inplace(arr, low=0, high=None):
        """In-place quick sort"""
        if high is None:
            high = len(arr) - 1
        
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_inplace(arr, low, pi - 1)
            quick_sort_inplace(arr, pi + 1, high)
        
        return arr
    
    def partition(arr, low, high):
        """Partition array around pivot"""
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    numbers = [10, 7, 8, 9, 1, 5]
    print(f"Original: {numbers}")
    
    sorted_nums = quick_sort(numbers)
    print(f"Sorted (list comp): {sorted_nums}")
    
    numbers2 = [10, 7, 8, 9, 1, 5]
    quick_sort_inplace(numbers2)
    print(f"Sorted (in-place): {numbers2}")
    
    print("\n💡 Quick Sort:")
    print("  Time: O(n log n) average, O(n²) worst")
    print("  Space: O(log n) stack")
    print("  Stable: No (typically)")
    print("  Good for: General purpose, cache-friendly")
    
    print()

# ============================================================
# EXERCISE 6: Counting Sort
# ============================================================

def counting_sort_demo():
    """
    Implement counting sort.
    
    Counting sort: Count occurrences, reconstruct sorted array
    """
    print("--- Exercise 6: Counting Sort ---")
    
    def counting_sort(arr):
        """Sort array using counting sort (for non-negative integers)"""
        if not arr:
            return arr
        
        max_val = max(arr)
        min_val = min(arr)
        range_size = max_val - min_val + 1
        
        # Count occurrences
        count = [0] * range_size
        for num in arr:
            count[num - min_val] += 1
        
        # Reconstruct sorted array
        result = []
        for i, c in enumerate(count):
            result.extend([i + min_val] * c)
        
        return result
    
    numbers = [4, 2, 2, 8, 3, 3, 1]
    print(f"Original: {numbers}")
    
    sorted_nums = counting_sort(numbers)
    print(f"Sorted: {sorted_nums}")
    
    print("\n💡 Counting Sort:")
    print("  Time: O(n + k) where k = range")
    print("  Space: O(k)")
    print("  Stable: Yes (with modification)")
    print("  Good for: Small range of integers")
    
    print()

# ============================================================
# EXERCISE 7: Performance Comparison
# ============================================================

def performance_comparison():
    """
    Compare sorting algorithm performance.
    
    TODO: Benchmark different algorithms
    """
    print("--- Exercise 7: Performance Comparison ---")
    
    # Algorithms to test
    algorithms = {
        'Bubble': bubble_sort_demo.__code__.co_consts[1],
        'Selection': selection_sort_demo.__code__.co_consts[1],
        'Insertion': insertion_sort_demo.__code__.co_consts[1],
        'Python built-in': lambda arr: sorted(arr),
    }
    
    # Test data
    sizes = [10, 50, 100]
    
    print("Performance (seconds):")
    print(f"{'Algorithm':<15} {'n=10':<10} {'n=50':<10} {'n=100':<10}")
    print("-" * 50)
    
    for name in ['Python built-in']:
        times = []
        for size in sizes:
            data = [random.randint(1, 100) for _ in range(size)]
            
            start = time.perf_counter()
            sorted(data)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        
        print(f"{name:<15} {times[0]:<10.6f} {times[1]:<10.6f} {times[2]:<10.6f}")
    
    print("\n💡 For production: Use Python's built-in sort (Timsort)")
    print("💡 Custom sorts useful for: Learning, special cases")
    
    print()

# ============================================================
# BONUS CHALLENGE: Radix Sort
# ============================================================

def radix_sort_demo():
    """
    Implement radix sort.
    
    Radix sort: Sort by each digit, stable counting sort
    """
    print("--- Bonus Challenge: Radix Sort ---")
    
    def counting_sort_by_digit(arr, exp):
        """Counting sort by specific digit"""
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        
        # Count occurrences
        for num in arr:
            index = (num // exp) % 10
            count[index] += 1
        
        # Cumulative count
        for i in range(1, 10):
            count[i] += count[i - 1]
        
        # Build output (backwards for stability)
        for i in range(n - 1, -1, -1):
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
        
        return output
    
    def radix_sort(arr):
        """Sort using radix sort"""
        if not arr:
            return arr
        
        max_val = max(arr)
        exp = 1
        
        while max_val // exp > 0:
            arr = counting_sort_by_digit(arr, exp)
            exp *= 10
        
        return arr
    
    numbers = [170, 45, 75, 90, 802, 24, 2, 66]
    print(f"Original: {numbers}")
    
    sorted_nums = radix_sort(numbers)
    print(f"Sorted: {sorted_nums}")
    
    print("\n💡 Radix Sort:")
    print("  Time: O(d * (n + k)) where d = digits")
    print("  Space: O(n + k)")
    print("  Stable: Yes")
    print("  Good for: Fixed-length integers/strings")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_summary():
    """
    Summary of sorting algorithms.
    """
    print("=" * 70)
    print("SORTING ALGORITHMS SUMMARY")
    print("=" * 70)
    
    algorithms = [
        ("Bubble Sort", "O(n²)", "O(n²)", "O(n)", "O(1)", "Yes"),
        ("Selection Sort", "O(n²)", "O(n²)", "O(n²)", "O(1)", "No"),
        ("Insertion Sort", "O(n²)", "O(n²)", "O(n)", "O(1)", "Yes"),
        ("Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)", "Yes"),
        ("Quick Sort", "O(n log n)", "O(n²)", "O(n log n)", "O(log n)", "No"),
        ("Heap Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(1)", "No"),
        ("Counting Sort", "O(n+k)", "O(n+k)", "O(n+k)", "O(k)", "Yes"),
        ("Radix Sort", "O(d(n+k))", "O(d(n+k))", "O(d(n+k))", "O(n+k)", "Yes"),
        ("Timsort (Python)", "O(n log n)", "O(n log n)", "O(n)", "O(n)", "Yes"),
    ]
    
    print(f"\n{'Algorithm':<18} {'Best':<12} {'Worst':<12} {'Avg':<12} {'Space':<10} {'Stable'}")
    print("-" * 70)
    
    for name, best, worst, avg, space, stable in algorithms:
        print(f"{name:<18} {best:<12} {worst:<12} {avg:<12} {space:<10} {stable}")
    
    print("\n" + "=" * 70)
    print()

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 6, Day 4: Custom Sorting Algorithms")
    print("=" * 60)
    print()
    
    bubble_sort_demo()
    selection_sort_demo()
    insertion_sort_demo()
    merge_sort_demo()
    quick_sort_demo()
    counting_sort_demo()
    performance_comparison()
    radix_sort_demo()
    complexity_summary()
    
    print("=" * 60)
    print("✅ Day 4 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Different algorithms for different scenarios")
    print("2. Python's Timsort is excellent for general use")
    print("3. O(n log n) is optimal for comparison-based sorting")
    print("4. Counting/Radix sort can be O(n) for special cases")

