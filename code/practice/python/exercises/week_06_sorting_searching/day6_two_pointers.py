"""
Week 6, Day 6: Two Pointers Technique

Learning Objectives:
- Master two pointers pattern
- Learn fast/slow pointer technique
- Understand sliding window
- Practice array manipulation
- Solve problems efficiently

Time: 10-15 minutes
"""

# ============================================================
# EXERCISE 1: Two Pointers Basics
# ============================================================

def two_pointers_basics():
    """
    Learn basic two pointers technique.
    
    Two pointers: Use two indices to traverse array
    """
    print("--- Exercise 1: Two Pointers Basics ---")
    
    def two_sum_sorted(arr, target):
        """Find two numbers that sum to target in sorted array"""
        left, right = 0, len(arr) - 1
        
        while left < right:
            current_sum = arr[left] + arr[right]
            if current_sum == target:
                return [left, right]
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        
        return None
    
    numbers = [2, 7, 11, 15]
    target = 9
    
    print(f"Array: {numbers}")
    print(f"Target: {target}")
    
    result = two_sum_sorted(numbers, target)
    if result:
        print(f"Indices: {result}, values: [{numbers[result[0]]}, {numbers[result[1]]}]")
    
    print("\n💡 Two Pointers: O(n) time, O(1) space")
    
    print()

# ============================================================
# EXERCISE 2: Remove Duplicates
# ============================================================

def remove_duplicates():
    """
    Remove duplicates from sorted array in-place.
    
    TODO: Use two pointers for in-place modification
    """
    print("--- Exercise 2: Remove Duplicates ---")
    
    def remove_duplicates_sorted(arr):
        """Remove duplicates, return new length"""
        if not arr:
            return 0
        
        write = 1  # Position to write next unique element
        
        for read in range(1, len(arr)):
            if arr[read] != arr[read - 1]:
                arr[write] = arr[read]
                write += 1
        
        return write
    
    numbers = [1, 1, 2, 2, 2, 3, 4, 4, 5]
    print(f"Original: {numbers}")
    
    length = remove_duplicates_sorted(numbers)
    print(f"After removing duplicates: {numbers[:length]}")
    print(f"New length: {length}")
    
    print()

# ============================================================
# EXERCISE 3: Fast and Slow Pointers
# ============================================================

def fast_slow_pointers():
    """
    Use fast and slow pointers (Floyd's algorithm).
    
    Fast/slow: Fast moves 2x speed of slow
    """
    print("--- Exercise 3: Fast and Slow Pointers ---")
    
    def find_middle(arr):
        """Find middle element using fast/slow pointers"""
        slow = fast = 0
        
        while fast < len(arr) - 1 and fast + 1 < len(arr):
            slow += 1
            fast += 2
        
        return slow
    
    def has_cycle_simulation(arr):
        """Simulate cycle detection (for demonstration)"""
        # In real linked list, would check if fast catches slow
        return False
    
    numbers = [1, 2, 3, 4, 5, 6, 7]
    mid_idx = find_middle(numbers)
    
    print(f"Array: {numbers}")
    print(f"Middle element: index {mid_idx}, value {numbers[mid_idx]}")
    
    print("\n💡 Fast/Slow Pointers:")
    print("  • Find middle: O(n) time, O(1) space")
    print("  • Cycle detection: Floyd's algorithm")
    
    print()

# ============================================================
# EXERCISE 4: Sliding Window
# ============================================================

def sliding_window():
    """
    Use sliding window technique.
    
    Sliding window: Maintain window of elements
    """
    print("--- Exercise 4: Sliding Window ---")
    
    def max_sum_subarray(arr, k):
        """Find maximum sum of k consecutive elements"""
        if len(arr) < k:
            return None
        
        # Initial window
        window_sum = sum(arr[:k])
        max_sum = window_sum
        
        # Slide window
        for i in range(k, len(arr)):
            window_sum = window_sum - arr[i - k] + arr[i]
            max_sum = max(max_sum, window_sum)
        
        return max_sum
    
    def longest_substring_k_distinct(s, k):
        """Longest substring with at most k distinct characters"""
        if not s or k == 0:
            return 0
        
        char_count = {}
        left = 0
        max_length = 0
        
        for right in range(len(s)):
            # Add right character
            char_count[s[right]] = char_count.get(s[right], 0) + 1
            
            # Shrink window if too many distinct
            while len(char_count) > k:
                char_count[s[left]] -= 1
                if char_count[s[left]] == 0:
                    del char_count[s[left]]
                left += 1
            
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    numbers = [1, 4, 2, 10, 23, 3, 1, 0, 20]
    k = 4
    
    print(f"Array: {numbers}")
    print(f"Max sum of {k} consecutive: {max_sum_subarray(numbers, k)}")
    
    string = "eceba"
    print(f"\nString: '{string}'")
    print(f"Longest substring with ≤2 distinct: {longest_substring_k_distinct(string, 2)}")
    
    print()

# ============================================================
# EXERCISE 5: Three Sum Problem
# ============================================================

def three_sum_problem():
    """
    Find three numbers that sum to zero.
    
    TODO: Use sorting + two pointers
    """
    print("--- Exercise 5: Three Sum ---")
    
    def three_sum(arr):
        """Find all unique triplets that sum to zero"""
        arr.sort()
        result = []
        
        for i in range(len(arr) - 2):
            # Skip duplicates
            if i > 0 and arr[i] == arr[i - 1]:
                continue
            
            # Two pointers for remaining elements
            left, right = i + 1, len(arr) - 1
            target = -arr[i]
            
            while left < right:
                current_sum = arr[left] + arr[right]
                
                if current_sum == target:
                    result.append([arr[i], arr[left], arr[right]])
                    
                    # Skip duplicates
                    while left < right and arr[left] == arr[left + 1]:
                        left += 1
                    while left < right and arr[right] == arr[right - 1]:
                        right -= 1
                    
                    left += 1
                    right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
        
        return result
    
    numbers = [-1, 0, 1, 2, -1, -4]
    print(f"Array: {numbers}")
    
    triplets = three_sum(numbers)
    print(f"Triplets that sum to 0:")
    for triplet in triplets:
        print(f"  {triplet}")
    
    print()

# ============================================================
# EXERCISE 6: Container With Most Water
# ============================================================

def container_most_water():
    """
    Find container that holds most water.
    
    TODO: Two pointers from ends
    """
    print("--- Exercise 6: Container With Most Water ---")
    
    def max_area(heights):
        """Find maximum water container area"""
        left, right = 0, len(heights) - 1
        max_water = 0
        
        while left < right:
            # Calculate area
            width = right - left
            height = min(heights[left], heights[right])
            area = width * height
            max_water = max(max_water, area)
            
            # Move pointer with smaller height
            if heights[left] < heights[right]:
                left += 1
            else:
                right -= 1
        
        return max_water
    
    heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    
    print(f"Heights: {heights}")
    print(f"Max water area: {max_area(heights)}")
    
    print("\n💡 Move pointer with smaller height to find larger area")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - Merge Sorted Arrays
# ============================================================

def merge_sorted_arrays():
    """
    Merge two sorted arrays.
    
    TODO: Use two pointers for merging
    """
    print("--- Exercise 7: Merge Sorted Arrays ---")
    
    def merge(arr1, arr2):
        """Merge two sorted arrays"""
        result = []
        i = j = 0
        
        while i < len(arr1) and j < len(arr2):
            if arr1[i] <= arr2[j]:
                result.append(arr1[i])
                i += 1
            else:
                result.append(arr2[j])
                j += 1
        
        # Add remaining elements
        result.extend(arr1[i:])
        result.extend(arr2[j:])
        
        return result
    
    arr1 = [1, 3, 5, 7]
    arr2 = [2, 4, 6, 8]
    
    print(f"Array 1: {arr1}")
    print(f"Array 2: {arr2}")
    print(f"Merged: {merge(arr1, arr2)}")
    
    print()

# ============================================================
# BONUS CHALLENGE: Trapping Rain Water
# ============================================================

def trapping_rain_water():
    """
    Calculate trapped rain water.
    
    TODO: Two pointers from ends
    """
    print("--- Bonus Challenge: Trapping Rain Water ---")
    
    def trap(heights):
        """Calculate total trapped water"""
        if not heights:
            return 0
        
        left, right = 0, len(heights) - 1
        left_max = right_max = 0
        water = 0
        
        while left < right:
            if heights[left] < heights[right]:
                if heights[left] >= left_max:
                    left_max = heights[left]
                else:
                    water += left_max - heights[left]
                left += 1
            else:
                if heights[right] >= right_max:
                    right_max = heights[right]
                else:
                    water += right_max - heights[right]
                right -= 1
        
        return water
    
    heights = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    
    print(f"Heights: {heights}")
    print(f"Trapped water: {trap(heights)} units")
    
    # Visualization
    print("\nVisualization:")
    max_height = max(heights)
    for level in range(max_height, 0, -1):
        line = ""
        for h in heights:
            if h >= level:
                line += "█"
            else:
                line += " "
        print(f"  {line}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    Two Pointers:
    - Time: O(n) typically
    - Space: O(1)
    - Single pass through array
    
    Fast/Slow Pointers:
    - Time: O(n)
    - Space: O(1)
    - Useful for cycle detection
    
    Sliding Window:
    - Time: O(n)
    - Space: O(k) for window state
    - Efficient for subarray problems
    
    Benefits:
    - Linear time complexity
    - Constant space
    - Elegant solutions
    - Easy to implement
    
    Use Cases:
    - Two sum (sorted array)
    - Remove duplicates
    - Find middle element
    - Merge sorted arrays
    - Subarray problems
    - String problems
    
    Common Patterns:
    - Opposite ends: left=0, right=n-1
    - Same direction: slow, fast
    - Sliding window: left, right expand/contract
    
    Best Practices:
    - Check array bounds
    - Handle edge cases (empty, single element)
    - Skip duplicates when needed
    - Consider sorted vs unsorted
    
    Security Considerations:
    - Validate array bounds
    - Handle integer overflow
    - Check for null/empty inputs
    - Consider worst-case scenarios
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 6, Day 6: Two Pointers Technique")
    print("=" * 60)
    print()
    
    two_pointers_basics()
    remove_duplicates()
    fast_slow_pointers()
    sliding_window()
    three_sum_problem()
    container_most_water()
    merge_sorted_arrays()
    trapping_rain_water()
    
    print("=" * 60)
    print("✅ Day 6 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Two pointers: O(n) time, O(1) space")
    print("2. Fast/slow for cycle detection and middle finding")
    print("3. Sliding window for subarray problems")
    print("4. Elegant solutions to complex problems")

